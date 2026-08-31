#!/usr/bin/env python3
"""Audit the moving-kernel projector and its second fundamental form."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_moving_kernel_second_fundamental_form_gate_results.json"
TOL = 2.0e-7


def projector_kernel(x):
    return np.eye(x.shape[1], dtype=complex) - x.conj().T @ np.linalg.pinv(x @ x.conj().T) @ x


def differential_projector(x, tangent, step=1.0e-6):
    return (projector_kernel(x + step * tangent) - projector_kernel(x - step * tangent)) / (2.0 * step)


def random_unitary(rng, dimension):
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
    q, r = np.linalg.qr(raw)
    phases = np.diag(r)
    return q @ np.diag(np.conj(phases / np.abs(phases)))


def singular_path_matrix(epsilon, coordinate):
    angle = coordinate / epsilon
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, epsilon * np.cos(angle), epsilon * np.sin(angle)],
    ], dtype=complex)


def main():
    rng = np.random.default_rng(20260828)
    x = np.column_stack([np.eye(3), np.zeros(3)]).astype(complex)
    tangent = rng.normal(size=(3, 4)) + 1j * rng.normal(size=(3, 4))

    p = projector_kernel(x)
    dp = differential_projector(x, tangent)
    one_minus_p = np.eye(4) - p
    second_fundamental = one_minus_p @ dp @ p

    projector_residual = float(np.linalg.norm(p @ p - p))
    self_adjoint_residual = float(np.linalg.norm(p - p.conj().T))
    tangent_off_diagonal_residual = float(np.linalg.norm(dp - second_fundamental - second_fundamental.conj().T))
    diagonal_tangent_residual = float(np.linalg.norm(p @ dp @ p) + np.linalg.norm(one_minus_p @ dp @ one_minus_p))

    maximum_covariance_residual = 0.0
    for _ in range(20):
        u3 = random_unitary(rng, 3)
        u4 = random_unitary(rng, 4)
        transformed_x = u3 @ x @ u4.conj().T
        transformed_tangent = u3 @ tangent @ u4.conj().T
        transformed_p = projector_kernel(transformed_x)
        transformed_dp = differential_projector(transformed_x, transformed_tangent)
        transformed_b = (np.eye(4) - transformed_p) @ transformed_dp @ transformed_p
        maximum_covariance_residual = max(
            maximum_covariance_residual,
            float(np.linalg.norm(transformed_p - u4 @ p @ u4.conj().T)),
            float(np.linalg.norm(transformed_b - u4 @ second_fundamental @ u4.conj().T)),
        )

    edge_operator = rng.normal(size=(11, 11)) + 1j * rng.normal(size=(11, 11))
    extended_b = np.kron(second_fundamental, np.eye(11))
    extended_edge_operator = np.kron(np.eye(4), edge_operator)
    factor_commutator_residual = float(np.linalg.norm(
        extended_b @ extended_edge_operator - extended_edge_operator @ extended_b
    ))

    epsilons = [1.0, 0.5, 0.25, 0.125, 0.0625]
    singular_rows = []
    for epsilon in epsilons:
        x_epsilon = singular_path_matrix(epsilon, 0.0)
        coordinate_step = epsilon * 1.0e-6
        dp_epsilon = (
            projector_kernel(singular_path_matrix(epsilon, coordinate_step))
            - projector_kernel(singular_path_matrix(epsilon, -coordinate_step))
        ) / (2.0 * coordinate_step)
        p_epsilon = projector_kernel(x_epsilon)
        b_epsilon = (np.eye(4) - p_epsilon) @ dp_epsilon @ p_epsilon
        dx_epsilon = (
            singular_path_matrix(epsilon, coordinate_step)
            - singular_path_matrix(epsilon, -coordinate_step)
        ) / (2.0 * coordinate_step)
        singular_rows.append({
            "epsilon": epsilon,
            "minimum_singular_value": float(np.linalg.svd(x_epsilon, compute_uv=False)[-1]),
            "field_derivative_norm": float(np.linalg.norm(dx_epsilon)),
            "second_fundamental_norm": float(np.linalg.norm(b_epsilon)),
            "epsilon_times_second_fundamental_norm": float(epsilon * np.linalg.norm(b_epsilon)),
            "kinetic_density": float(np.linalg.norm(b_epsilon) ** 2),
        })

    rank_drop = singular_path_matrix(1.0, 0.0)
    rank_drop[2, :] = 0.0
    p_rank_drop = projector_kernel(rank_drop)
    p_positive = projector_kernel(singular_path_matrix(1.0e-4, 0.0))
    rank_jump_operator_norm = float(np.linalg.norm(p_rank_drop - p_positive, ord=2))

    assert np.linalg.matrix_rank(x) == 3
    assert round(np.trace(p).real) == 1
    assert projector_residual < TOL
    assert self_adjoint_residual < TOL
    assert tangent_off_diagonal_residual < TOL
    assert diagonal_tangent_residual < TOL
    assert np.linalg.matrix_rank(second_fundamental, TOL) <= 1
    assert maximum_covariance_residual < TOL
    assert factor_commutator_residual < TOL
    assert all(abs(row["field_derivative_norm"] - 1.0) < TOL for row in singular_rows)
    assert all(abs(row["epsilon_times_second_fundamental_norm"] - 1.0) < TOL for row in singular_rows)
    assert abs(rank_jump_operator_norm - 1.0) < TOL

    result = {
        "gate": "version8_moving_kernel_second_fundamental_form_gate",
        "full_rank_stratum": {
            "field_shape": [3, 4],
            "field_rank": int(np.linalg.matrix_rank(x)),
            "kernel_projector_formula": "P=I-X^*(XX^*)^{-1}X",
            "kernel_projector_rank": int(round(np.trace(p).real)),
            "projector_residual": projector_residual,
            "self_adjoint_residual": self_adjoint_residual,
        },
        "second_fundamental_form": {
            "formula": "B=(I-P)(nabla P)P",
            "rank_for_one_tangent_direction": int(np.linalg.matrix_rank(second_fundamental, TOL)),
            "maximum_possible_rank_for_kernel_line": 1,
            "tangent_off_diagonal_residual": tangent_off_diagonal_residual,
            "diagonal_tangent_residual": diagonal_tangent_residual,
            "maximum_basis_covariance_residual": maximum_covariance_residual,
            "vanishes_for_constant_field": True,
            "defines_kinetic_not_static_potential_data": True,
        },
        "physical_factor_test": {
            "extension": "B tensor I_edge",
            "edge_factor_dimension": 11,
            "commutator_with_full_edge_algebra_residual": factor_commutator_residual,
            "mixes_kernel_and_affine_complement": True,
            "mixes_edge_and_endpoint_carriers": False,
            "fixes_relative_mass_metric": False,
        },
        "rank_change_stress_test": {
            "path": "X_epsilon(x)=diag_rows(e1,e2,epsilon*(cos(x/epsilon)e3+sin(x/epsilon)e4))",
            "rows": singular_rows,
            "bounded_field_derivative": True,
            "second_fundamental_norm_scaling": "1/epsilon",
            "kinetic_density_scaling": "1/epsilon^2",
            "kernel_rank_before_drop": 1,
            "kernel_rank_at_drop": 2,
            "projector_jump_operator_norm": rank_jump_operator_norm,
            "universal_continuous_finite_energy_extension_across_rank_drop": False,
        },
        "verdict": {
            "canonical_moving_kernel_geometry_obtained": True,
            "new_arbitrary_identification_required": False,
            "missing_intersector_connector_obtained": False,
            "static_family_selector_obtained": False,
            "regular_rank_changing_parent_obtained": False,
            "status": "canonical_grassmannian_kinetic_geometry_but_factorized_and_rank_drop_singular",
            "next_step": "freeze_internal_tome8_search_unless_a_new_nonfactorized_operator_or_rank_regularized_projector_is_supplied",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()