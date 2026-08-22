#!/usr/bin/env python3
"""Проверка угловой классификации мягких мод центрированного вихря."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.sparse.linalg import LinearOperator, eigsh


ROOT = Path(__file__).resolve().parents[2]
PARENT_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_corrected_vortex_nonradial_stability_gate.py"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_centered_angular_channel_decomposition_gate_results.json"


def main() -> None:
    parent = runpy.run_path(str(PARENT_AUDIT))
    solution, derivative_a, derivative_b = parent["corrected_profile"]()
    calculation = parent["calculate"](
        solution, derivative_a, derivative_b, 33,
        box_radius=10.0, eigen_count=4, gauge_sign=-1.0,
        return_state=True,
    )
    state = calculation["_state"]
    zero = state["background_vector"]
    energy = state["physical_energy"]
    gradient = state["physical_gradient"]
    gauge_action = state["gauge_fixing_action"]
    metric = state["metric_weights"]
    initial_energy = energy(zero)

    grid_size = 33
    interior_size = grid_size - 2
    block_size = interior_size**2
    center_local = grid_size // 2 - 1
    center_flat = center_local * interior_size + center_local
    fixed = np.array([center_flat, block_size + center_flat])
    fixed_set = set(int(index) for index in fixed)
    keep = np.array([index for index in range(zero.size) if index not in fixed_set])

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

    inverse_sqrt_metric = 1.0 / np.sqrt(metric[keep])
    sqrt_metric = np.sqrt(metric[keep])
    finite_difference_step = 2.0e-5

    def normalized_hessian_action(vector):
        full = np.zeros_like(zero)
        full[keep] = inverse_sqrt_metric * vector
        plus = jacobian(stationary + finite_difference_step * full)
        minus = jacobian(stationary - finite_difference_step * full)
        physical = (plus - minus) / (2.0 * finite_difference_step)
        return inverse_sqrt_metric * physical[keep]

    operator = LinearOperator((keep.size, keep.size), matvec=normalized_hessian_action, dtype=float)
    eigen_count = 24
    eigenvalues, eigenvectors = eigsh(
        operator, k=eigen_count, which="SA", tol=4.0e-6,
        maxiter=6000, ncv=80, return_eigenvectors=True,
    )
    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    def split_perturbation_fields(full_vector):
        fields = []
        for field_index in range(5):
            interior_values = full_vector[
                field_index * block_size:(field_index + 1) * block_size
            ].reshape(interior_size, interior_size)
            field = np.zeros((grid_size, grid_size))
            field[1:-1, 1:-1] = interior_values
            fields.append(field)
        return fields

    def rotate_fields(fields, quarter_turn, scalar_sign, vector_sign):
        pulled = [np.rot90(field, k=quarter_turn) for field in fields]
        rotated_scalar = (
            [-pulled[1], pulled[0]] if scalar_sign == 1
            else [pulled[1], -pulled[0]]
        )
        rotated_vector = (
            [-pulled[3], pulled[2]] if vector_sign == 1
            else [pulled[3], -pulled[2]]
        )
        return rotated_scalar + rotated_vector + [pulled[4]]

    stationary_fields = state["unpack_fields"](stationary)
    background_norm = np.sqrt(sum(
        np.sum(field[1:-1, 1:-1] ** 2) for field in stationary_fields
    ))
    candidate_residuals = {}
    candidates = []
    for quarter_turn in (-1, 1):
        for scalar_sign in (-1, 1):
            for vector_sign in (-1, 1):
                rotated = rotate_fields(
                    stationary_fields, quarter_turn, scalar_sign, vector_sign
                )
                residual = np.sqrt(sum(
                    np.sum((left[1:-1, 1:-1] - right[1:-1, 1:-1]) ** 2)
                    for left, right in zip(rotated, stationary_fields)
                )) / background_norm
                key = f"pull_{quarter_turn:+d}_scalar_{scalar_sign:+d}_vector_{vector_sign:+d}"
                candidate_residuals[key] = float(residual)
                candidates.append((residual, quarter_turn, scalar_sign, vector_sign, key))
    _, selected_quarter_turn, selected_scalar_sign, selected_vector_sign, selected_key = min(candidates)

    def rotate_physical_vector(full_vector):
        fields = split_perturbation_fields(full_vector)
        rotated = rotate_fields(
            fields, selected_quarter_turn, selected_scalar_sign, selected_vector_sign
        )
        return np.concatenate([field[1:-1, 1:-1].reshape(-1) for field in rotated])

    def rotate_normalized(vector):
        physical = np.zeros_like(zero)
        physical[keep] = inverse_sqrt_metric * vector
        rotated_physical = rotate_physical_vector(physical)
        return sqrt_metric * rotated_physical[keep]

    rotated_vectors = np.column_stack([
        rotate_normalized(eigenvectors[:, mode])
        for mode in range(eigen_count)
    ])
    projected_rotation = eigenvectors.T @ rotated_vectors
    leakage = 1.0 - np.sum(projected_rotation**2, axis=0)
    singular_values = np.linalg.svd(projected_rotation, compute_uv=False)

    rotation_fourth_power_residuals = []
    covariance_absolute_residuals = []
    covariance_relative_residuals = []
    for mode in range(eigen_count):
        vector = eigenvectors[:, mode]
        rotated = rotated_vectors[:, mode]
        fourth = vector.copy()
        for _ in range(4):
            fourth = rotate_normalized(fourth)
        rotation_fourth_power_residuals.append(float(np.linalg.norm(fourth - vector)))

        h_rotated = normalized_hessian_action(rotated)
        rotated_h = rotate_normalized(eigenvalues[mode] * vector)
        residual = np.linalg.norm(h_rotated - rotated_h)
        scale = max(np.linalg.norm(h_rotated), np.linalg.norm(rotated_h), 1.0e-12)
        covariance_absolute_residuals.append(float(residual))
        covariance_relative_residuals.append(float(residual / scale))

    # У точной C4-ковариантной схемы projected_rotation был бы почти
    # ортогонален уже в достаточно широком низкоэнергетическом подпространстве.
    mean_leakage = float(np.mean(leakage))
    maximum_leakage = float(np.max(leakage))
    minimum_singular_value = float(np.min(singular_values))
    maximum_covariance_residual = float(np.max(covariance_relative_residuals))
    classification_certified = bool(
        maximum_leakage < 0.1
        and minimum_singular_value > 0.9
        and maximum_covariance_residual < 0.1
    )

    result = {
        "gate": "version6_bosonic_defect_centered_angular_channel_decomposition_gate",
        "stationary_background": {
            "grid_size": grid_size,
            "spacing": float(state["spacing"]),
            "optimizer_success": bool(optimum.success),
            "optimizer_iterations": int(optimum.nit),
            "projected_gradient_rms": float(np.linalg.norm(projected_gradient) / np.sqrt(keep.size)),
        },
        "low_energy_spectrum": {
            "eigenvalue_count": eigen_count,
            "eigenvalues": eigenvalues.tolist(),
            "negative_mode_count": int(np.sum(eigenvalues < -1.0e-5)),
        },
        "quarter_turn_test": {
            "combined_action": "spatial pullback plus internal charged-scalar rotation and vector rotation",
            "background_candidate_relative_residuals": candidate_residuals,
            "selected_action": selected_key,
            "selected_background_relative_residual": candidate_residuals[selected_key],
            "rotation_fourth_power_maximum_residual": float(np.max(rotation_fourth_power_residuals)),
            "mode_leakage_outside_first_24": leakage.tolist(),
            "mean_leakage": mean_leakage,
            "maximum_leakage": maximum_leakage,
            "projected_rotation_singular_values": singular_values.tolist(),
            "minimum_singular_value": minimum_singular_value,
            "hessian_rotation_covariance_absolute_residuals": covariance_absolute_residuals,
            "hessian_rotation_covariance_relative_residuals": covariance_relative_residuals,
            "maximum_covariance_relative_residual": maximum_covariance_residual,
        },
        "verdict": {
            "quarter_turn_operator_itself_is_exact": bool(np.max(rotation_fourth_power_residuals) < 1.0e-12),
            "cartesian_hessian_is_quarter_turn_covariant": bool(maximum_covariance_residual < 0.1),
            "angular_channel_classification_certified": classification_certified,
            "negative_mode_found": bool(np.any(eigenvalues < -1.0e-5)),
            "square_grid_can_certify_continuum_angular_labels": classification_certified,
            "continuum_internal_gap_closed": False,
            "full_spin2_spin3_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_polar_angular_sturm_liouville_gate",
        },
    }

    assert optimum.success
    assert result["stationary_background"]["projected_gradient_rms"] < 1.0e-6
    assert result["low_energy_spectrum"]["negative_mode_count"] == 0
    assert result["verdict"]["quarter_turn_operator_itself_is_exact"]
    assert not result["verdict"]["continuum_internal_gap_closed"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()