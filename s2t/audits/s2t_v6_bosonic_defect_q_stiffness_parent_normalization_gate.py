#!/usr/bin/env python3
"""Единая условная нормировка кинетик Q, T и семейной связности."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh


ROOT = Path(__file__).resolve().parents[2]
PROFILE_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_defect_profile_gate.py"
COUPLED_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_vacuum_gate.py"
EMBEDDING_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_minimal_spin_three_carrier_embedding_gate.py"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_q_stiffness_parent_normalization_gate_results.json"


def main() -> None:
    old_profile = runpy.run_path(str(PROFILE_AUDIT))
    coupled = runpy.run_path(str(COUPLED_AUDIT))
    embedding = runpy.run_path(str(EMBEDDING_AUDIT))

    q_basis = coupled["symmetric_traceless_basis"]()
    t_basis = embedding["symmetric_rank_three_basis"]()
    arrow_basis = [embedding["tensor_to_arrow"](tensor, embedding["spin_two_basis"]()) for tensor in t_basis]

    q_conditioned_gram = np.array(
        [[np.trace(left @ right) / 3.0 for right in q_basis] for left in q_basis]
    )
    t_conditioned_gram = np.array(
        [[np.trace(left.T @ right) / 3.0 for right in arrow_basis] for left in arrow_basis]
    )

    z_q = float(np.mean(np.diag(q_conditioned_gram)))
    z_t = float(np.mean(np.diag(t_conditioned_gram)))
    corrected_A = 128.0 / 243.0
    corrected_B = 160.0 / 243.0
    corrected_C = corrected_A
    gauge_G = 2.0 / 27.0
    polynomial = old_profile["POLYNOMIAL"]

    def potential(a, b):
        return sum(value * a**i * b**j for (i, j), value in polynomial.items())

    def derivative_a(a, b):
        return sum(value * i * a ** (i - 1) * b**j for (i, j), value in polynomial.items() if i)

    def derivative_b(a, b):
        return sum(value * j * a**i * b ** (j - 1) for (i, j), value in polynomial.items() if j)

    def second_a(a, b):
        return sum(value * i * (i - 1) * a ** (i - 2) * b**j
                   for (i, j), value in polynomial.items() if i >= 2)

    def second_b(a, b):
        return sum(value * j * (j - 1) * a**i * b ** (j - 2)
                   for (i, j), value in polynomial.items() if j >= 2)

    def mixed_ab(a, b):
        return sum(value * i * j * a ** (i - 1) * b ** (j - 1)
                   for (i, j), value in polynomial.items() if i and j)

    def equations(radius, value):
        k, kp, a, ap, b, bp = value
        return np.vstack([
            kp,
            kp / radius - (corrected_C / gauge_G) * a**2 * (1.0 - k),
            ap,
            -ap / radius + (1.0 - k) ** 2 * a / radius**2 + derivative_a(a, b) / corrected_A,
            bp,
            -bp / radius + derivative_b(a, b) / corrected_B,
        ])

    def boundary(left, right):
        return np.array([left[0], left[2], left[5], right[0] - 1.0, right[2] - 1.0, right[4] - 1.0])

    radius_initial = np.linspace(1.0e-5, 20.0, 700)
    k_initial = radius_initial**2 / (1.0 + radius_initial**2)
    a_initial = np.tanh(2.0 * radius_initial)
    b_initial = 1.0 + 0.1 * np.exp(-radius_initial**2)
    initial = np.vstack([
        k_initial, np.gradient(k_initial, radius_initial),
        a_initial, np.gradient(a_initial, radius_initial),
        b_initial, np.gradient(b_initial, radius_initial),
    ])
    solution = solve_bvp(
        equations, boundary, radius_initial, initial,
        tol=2.0e-7, max_nodes=50000,
    )

    radius = np.linspace(1.0e-5, 20.0, 30000)
    k, kp, a, ap, b, bp = solution.sol(radius)
    parts = {
        "radial_scalar": float(2.0 * np.pi * np.trapezoid(
            (0.5 * corrected_A * ap**2 + 0.5 * corrected_B * bp**2) * radius, radius
        )),
        "angular_scalar": float(2.0 * np.pi * np.trapezoid(
            0.5 * corrected_C * a**2 * (1.0 - k) ** 2 / radius, radius
        )),
        "gauge_curvature": float(2.0 * np.pi * np.trapezoid(
            0.5 * gauge_G * kp**2 / radius, radius
        )),
        "potential": float(2.0 * np.pi * np.trapezoid(potential(a, b) * radius, radius)),
    }
    tension = sum(parts.values())
    virial = abs(parts["gauge_curvature"] - parts["potential"]) / tension

    def radial_spectrum(node_count: int):
        coordinate = np.linspace(0.0, 1.0, node_count)
        radial_grid = 1.0e-4 + (20.0 - 1.0e-4) * coordinate**1.3
        kg, ag, bg = solution.sol(radial_grid)[[0, 2, 4]]
        dimension = 3 * node_count
        hessian = lil_matrix((dimension, dimension))
        metric = lil_matrix((dimension, dimension))
        for element in range(node_count - 1):
            left, right = radial_grid[element], radial_grid[element + 1]
            width = right - left
            middle = 0.5 * (left + right)
            km = 0.5 * (kg[element] + kg[element + 1])
            am = 0.5 * (ag[element] + ag[element + 1])
            bm = 0.5 * (bg[element] + bg[element + 1])
            derivative = np.array([[1.0, -1.0], [-1.0, 1.0]]) / width
            mass = width * np.array([[2.0, 1.0], [1.0, 2.0]]) / 6.0
            diagonal = [
                (gauge_G / middle, corrected_C * am**2 / middle, gauge_G / middle),
                (corrected_A * middle, corrected_C * (1.0 - km) ** 2 / middle + middle * second_a(am, bm), corrected_A * middle),
                (corrected_B * middle, middle * second_b(am, bm), corrected_B * middle),
            ]
            for field, (stiffness, local_potential, weight) in enumerate(diagonal):
                indices = [field * node_count + element, field * node_count + element + 1]
                for i in range(2):
                    for j in range(2):
                        hessian[indices[i], indices[j]] += stiffness * derivative[i, j] + local_potential * mass[i, j]
                        metric[indices[i], indices[j]] += weight * mass[i, j]
            for first, second, coupling in [
                (0, 1, -2.0 * corrected_C * am * (1.0 - km) / middle),
                (1, 2, middle * mixed_ab(am, bm)),
            ]:
                left_indices = [first * node_count + element, first * node_count + element + 1]
                right_indices = [second * node_count + element, second * node_count + element + 1]
                for i in range(2):
                    for j in range(2):
                        hessian[left_indices[i], right_indices[j]] += coupling * mass[i, j]
                        hessian[right_indices[j], left_indices[i]] += coupling * mass[i, j]

        fixed = {0, node_count - 1, node_count, 2 * node_count - 1, 3 * node_count - 1}
        keep = np.array([index for index in range(dimension) if index not in fixed])
        hessian = hessian.tocsr()[keep][:, keep]
        metric = metric.tocsr()[keep][:, keep]
        return np.sort(eigsh(
            hessian, k=8, M=metric, sigma=0.0, which="LM",
            return_eigenvectors=False,
        ))

    convergence = {str(n): radial_spectrum(n).tolist() for n in [100, 160, 240, 360, 500]}
    finest = np.array(convergence["500"])

    result = {
        "gate": "version6_bosonic_defect_q_stiffness_parent_normalization_gate",
        "conditioned_parent_trace": {
            "formula_Q": "Tr_3((DQ)^2)/3",
            "formula_T": "Tr_3((DZ_T)^* DZ_T)/3=||DT||^2/3",
            "Q_gram_eigenvalues": np.linalg.eigvalsh(q_conditioned_gram).tolist(),
            "T_gram_eigenvalues": np.linalg.eigvalsh(t_conditioned_gram).tolist(),
            "raw_frobenius_Z_Q": z_q,
            "raw_frobenius_Z_T": z_t,
            "relative_ratio_Z_Q_over_Z_T": z_q / z_t,
            "new_relative_weight_parameter_count": 0,
        },
        "normalization_correction": {
            "previous_profile_A": float(old_profile["A"]),
            "previous_profile_B": float(old_profile["B"]),
            "corrected_A": corrected_A,
            "corrected_B": corrected_B,
            "corrected_C": corrected_C,
            "unchanged_G": gauge_G,
            "previous_T_kinetic_overcount_factor": float(old_profile["A"] / corrected_A),
            "potential_already_conditioned_correctly": True,
            "previous_profile_certificate_is_canonical_after_correction": False,
        },
        "corrected_profile": {
            "solver_status": int(solution.status),
            "mesh_nodes": int(solution.x.size),
            "maximum_relative_residual": float(np.max(solution.rms_residuals)),
            "boundary_residual": float(np.linalg.norm(boundary(solution.y[:, 0], solution.y[:, -1]))),
            "core_b": float(b[0]),
            "core_a_slope": float(ap[0]),
            "dimensionless_tension": tension,
            "energy_parts": parts,
            "relative_virial_residual": virial,
        },
        "corrected_radial_stability": {
            "finite_element_node_counts": [100, 160, 240, 360, 500],
            "lowest_eigenvalue_convergence": {n: values[0] for n, values in convergence.items()},
            "finest_eigenvalues": finest.tolist(),
            "negative_mode_count_checked": int(np.sum(finest < -1.0e-6)),
            "zero_mode_count_checked": int(np.sum(np.abs(finest) < 1.0e-6)),
            "minimum_eigenvalue": float(finest[0]),
            "minimum_grid_drift_360_to_500": float(abs(np.array(convergence["360"])[0] - finest[0])),
        },
        "boundary": {
            "absolute_scale_derived": False,
            "corrected_nonradial_stability_checked": False,
            "closed_loop_stability_checked": False,
            "hopf_identification_checked": False,
        },
        "verdict": {
            "relative_Q_T_stiffness_derived_from_same_parent_trace": True,
            "canonical_Z_Q_equals_Z_T": True,
            "previous_profile_T_kinetic_normalization_consistent": False,
            "corrected_profile_exists": True,
            "corrected_radial_stability_passes": True,
            "full_vortex_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_corrected_vortex_nonradial_stability_gate",
        },
    }

    assert np.max(np.abs(q_conditioned_gram - np.eye(5) / 3.0)) < 1.0e-12
    assert np.max(np.abs(t_conditioned_gram - np.eye(7) / 3.0)) < 1.0e-12
    assert abs(z_q / z_t - 1.0) < 1.0e-12
    assert abs(result["normalization_correction"]["previous_T_kinetic_overcount_factor"] - 3.0) < 1.0e-12
    assert solution.status == 0
    assert virial < 1.0e-6
    assert result["corrected_radial_stability"]["negative_mode_count_checked"] == 0
    assert result["corrected_radial_stability"]["minimum_eigenvalue"] > 4.0
    assert result["corrected_radial_stability"]["minimum_grid_drift_360_to_500"] < 1.0e-4
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()