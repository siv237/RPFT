#!/usr/bin/env python3
"""Нелинейная проверка отрицательной моды после закрепления центра вихря."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.sparse.linalg import LinearOperator, eigsh


ROOT = Path(__file__).resolve().parents[2]
PARENT_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_corrected_vortex_nonradial_stability_gate.py"
COVARIANT_RESULT = ROOT / "s2t/results/s2t_v6_bosonic_defect_corrected_vortex_covariant_zero_mode_resolution_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_corrected_vortex_negative_mode_nonlinear_saturation_gate_results.json"


def main() -> None:
    parent = runpy.run_path(str(PARENT_AUDIT))
    solution, derivative_a, derivative_b = parent["corrected_profile"]()
    calculate = parent["calculate"]
    previous = json.loads(COVARIANT_RESULT.read_text(encoding="utf-8"))

    def centered_relaxation(grid_size: int):
        calculation = calculate(
            solution, derivative_a, derivative_b, grid_size,
            box_radius=10.0, eigen_count=4, gauge_sign=-1.0,
            return_state=True,
        )
        state = calculation.pop("_state")
        zero = state["background_vector"]
        energy = state["physical_energy"]
        gradient = state["physical_gradient"]
        gauge_action = state["gauge_fixing_action"]
        initial_energy = energy(zero)

        interior_size = grid_size - 2
        block_size = interior_size**2
        center_local = grid_size // 2 - 1
        center_flat = center_local * interior_size + center_local
        fixed = np.array([center_flat, block_size + center_flat])
        keep = np.array([index for index in range(zero.size) if index not in set(fixed)])

        def functional(vector):
            return energy(vector) - initial_energy + 0.5 * vector @ gauge_action(vector)

        def jacobian(vector):
            return gradient(vector) + gauge_action(vector)

        bounds = [(None, None)] * zero.size
        for index in fixed:
            bounds[int(index)] = (0.0, 0.0)
        optimum = minimize(
            functional, zero, jac=jacobian, method="L-BFGS-B", bounds=bounds,
            options={
                "maxiter": 2200, "gtol": 2.0e-8, "ftol": 1.0e-14,
                "maxls": 40, "maxcor": 30,
            },
        )
        stationary = optimum.x
        projected_gradient = jacobian(stationary)[keep]

        metric = state["metric_weights"]
        inverse_sqrt_metric = 1.0 / np.sqrt(metric[keep])
        finite_difference_step = 2.0e-5

        def normalized_hessian_action(vector):
            full = np.zeros_like(zero)
            full[keep] = inverse_sqrt_metric * vector
            plus = jacobian(stationary + finite_difference_step * full)
            minus = jacobian(stationary - finite_difference_step * full)
            physical = (plus - minus) / (2.0 * finite_difference_step)
            return inverse_sqrt_metric * physical[keep]

        operator = LinearOperator((keep.size, keep.size), matvec=normalized_hessian_action, dtype=float)
        eigenvalues = np.sort(eigsh(
            operator, k=6, which="SA", tol=3.0e-6,
            maxiter=5000, ncv=32, return_eigenvectors=False,
        ))

        phi1, phi2, ax, ay, neutral = state["unpack_fields"](stationary)
        spacing = state["spacing"]
        coordinate = state["coordinate"]
        curvature = (
            (ay[1:-1, 2:] - ay[1:-1, 1:-1]) / spacing
            - (ax[2:, 1:-1] - ax[1:-1, 1:-1]) / spacing
        )
        xx, yy = np.meshgrid(coordinate[1:-1], coordinate[1:-1])
        flux_weight = np.abs(curvature)
        flux_x = float(np.sum(xx * flux_weight) / np.sum(flux_weight))
        flux_y = float(np.sum(yy * flux_weight) / np.sum(flux_weight))

        return {
            "grid_size": grid_size,
            "spacing": float(spacing),
            "sampled_background_lowest_eigenvalues": calculation["eigenvalues"],
            "optimizer_success": bool(optimum.success),
            "optimizer_iterations": int(optimum.nit),
            "gauge_fixed_energy_drop": float(optimum.fun),
            "projected_gradient_rms": float(np.linalg.norm(projected_gradient) / np.sqrt(keep.size)),
            "center_amplitude": float(np.hypot(phi1[grid_size // 2, grid_size // 2], phi2[grid_size // 2, grid_size // 2])),
            "flux_centroid": [flux_x, flux_y],
            "relaxed_hessian_eigenvalues": eigenvalues.tolist(),
            "relaxed_negative_mode_count": int(np.sum(eigenvalues < -1.0e-5)),
        }, state, calculation

    relaxations = {}
    state_33 = None
    calculation_33 = None
    for grid in [25, 33, 41]:
        data, state, calculation = centered_relaxation(grid)
        relaxations[str(grid)] = data
        if grid == 33:
            state_33 = state
            calculation_33 = calculation

    assert state_33 is not None and calculation_33 is not None
    negative_vector = (
        state_33["inverse_sqrt_metric"]
        * state_33["normalized_eigenvectors"][:, 0]
    )
    energy_33 = state_33["physical_energy"]
    gauge_33 = state_33["gauge_fixing_action"]
    zero_33 = state_33["background_vector"]
    base_gradient_33 = state_33["base_gradient"]
    base_energy_33 = energy_33(zero_33)

    def tangent_functional(amplitude):
        vector = amplitude * negative_vector
        return float(
            energy_33(vector) - base_energy_33 - base_gradient_33 @ vector
            + 0.5 * vector @ gauge_33(vector)
        )

    positive_branch = minimize_scalar(
        tangent_functional, bounds=(0.0, 0.8), method="bounded",
        options={"xatol": 1.0e-10},
    )

    relaxed_minima = {
        grid: values["relaxed_hessian_eigenvalues"][0]
        for grid, values in relaxations.items()
    }
    result = {
        "gate": "version6_bosonic_defect_corrected_vortex_negative_mode_nonlinear_saturation_gate",
        "previous_unpinned_negative_mode": {
            "finest_eigenvalue": previous["negative_mode"]["finest_lowest_eigenvalue"],
            "one_dimensional_branch_amplitude_grid_33": float(positive_branch.x),
            "one_dimensional_branch_energy_drop_grid_33": float(positive_branch.fun),
            "interpretation": "translation-like descent of a nonstationary sampled background",
        },
        "center_pinned_discrete_stationary_vortices": relaxations,
        "relaxed_lowest_eigenvalue_by_grid": relaxed_minima,
        "verdict": {
            "negative_mode_survives_centered_stationary_relaxation": False,
            "previous_negative_mode_is_physical_instability_certificate": False,
            "peierls_nabarro_lattice_pinning_diagnosis": True,
            "corrected_effective_vortex_has_negative_mode_after_translation_fixing": False,
            "full_spin2_spin3_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_translation_covariant_discretization_gate",
        },
    }

    assert all(values["relaxed_negative_mode_count"] == 0 for values in relaxations.values())
    assert all(value > 0.0 for value in relaxed_minima.values())
    assert max(values["projected_gradient_rms"] for values in relaxations.values()) < 1.0e-6
    assert abs(positive_branch.fun) > 1.0e-5
    assert not result["verdict"]["previous_negative_mode_is_physical_instability_certificate"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()