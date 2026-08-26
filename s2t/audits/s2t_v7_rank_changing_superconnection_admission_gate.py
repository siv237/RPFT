#!/usr/bin/env python3
"""Audit the Tome VII rank-changing superconnection admission gate."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


def odd_block(field: np.ndarray) -> np.ndarray:
    """Return [[0, X*], [X, 0]] for X : C^4 -> C^3."""
    return np.block(
        [
            [np.zeros((4, 4), dtype=complex), field.conj().T],
            [field, np.zeros((3, 3), dtype=complex)],
        ]
    )


def normalized_curvature_action(operator: np.ndarray) -> float:
    curvature = operator @ operator
    return float(
        np.real(np.trace(curvature.conj().T @ curvature)) / operator.shape[0]
    )


def main() -> None:
    u1 = np.array([1.0, -1.0, 0.0, 0.0]) / np.sqrt(2.0)
    u2 = np.array([1.0, 1.0, -2.0, 0.0]) / np.sqrt(6.0)
    u3 = np.array([1.0, 1.0, 1.0, -3.0]) / np.sqrt(12.0)
    inclusion = np.column_stack([u1, u2, u3])

    p1 = np.ones((4, 4)) / 4.0
    p3 = np.eye(4) - p1
    reconstructed_p3 = inclusion @ inclusion.T

    projector_residual = float(np.linalg.norm(p3 @ p3 - p3))
    basis_residual = float(np.linalg.norm(inclusion.T @ inclusion - np.eye(3)))
    reconstruction_residual = float(np.linalg.norm(reconstructed_p3 - p3))

    # Check the S4-covariance X -> rho_3(g) X rho_4(g)^(-1).
    test_field = (
        np.arange(12, dtype=float).reshape(3, 4)
        + 1j * np.arange(12, 24, dtype=float).reshape(3, 4)
    )
    covariance_residual = 0.0
    for permutation in itertools.permutations(range(4)):
        permutation_matrix = np.eye(4)[list(permutation)]
        triplet_representation = inclusion.T @ permutation_matrix @ inclusion
        transformed_field = (
            triplet_representation @ test_field @ permutation_matrix.T
        )
        carrier_representation = np.block(
            [
                [permutation_matrix, np.zeros((4, 3))],
                [np.zeros((3, 4)), triplet_representation],
            ]
        )
        covariance_residual = max(
            covariance_residual,
            float(
                np.linalg.norm(
                    odd_block(transformed_field)
                    - carrier_representation
                    @ odd_block(test_field)
                    @ carrier_representation.conj().T
                )
            ),
        )

    rank_strata: list[dict[str, int]] = []
    for field_rank in range(4):
        field = np.zeros((3, 4), dtype=complex)
        for index in range(field_rank):
            field[index, index] = 1.0
        rank_strata.append(
            {
                "field_rank": int(np.linalg.matrix_rank(field)),
                "odd_operator_rank": int(np.linalg.matrix_rank(odd_block(field))),
            }
        )

    block = odd_block(test_field)
    real_block = np.block(
        [
            [block, np.zeros_like(block)],
            [np.zeros_like(block), block.conj()],
        ]
    )
    real_exchange = np.block(
        [
            [np.zeros_like(block), np.eye(7)],
            [np.eye(7), np.zeros_like(block)],
        ]
    )
    selfadjoint_residual = float(np.linalg.norm(real_block - real_block.conj().T))
    real_condition_residual = float(
        np.linalg.norm(
            real_exchange @ real_block.conj() @ real_exchange - real_block
        )
    )

    grading = np.diag([1.0] * 4 + [-1.0] * 3).astype(complex)
    oddness_residual = float(np.linalg.norm(grading @ block + block @ grading))

    # Build the real 24-dimensional basis of M_(3x4)(C).
    tangent_basis: list[np.ndarray] = []
    for row in range(3):
        for column in range(4):
            real_direction = np.zeros((3, 4), dtype=complex)
            real_direction[row, column] = 1.0
            tangent_basis.append(odd_block(real_direction))

            imaginary_direction = np.zeros((3, 4), dtype=complex)
            imaginary_direction[row, column] = 1j
            tangent_basis.append(odd_block(imaginary_direction))

    vacuum_curvature = grading @ grading
    linear_curvatures = [
        grading @ direction + direction @ grading
        for direction in tangent_basis
    ]
    hessian = np.zeros((24, 24), dtype=float)
    for first, direction_first in enumerate(tangent_basis):
        for second, direction_second in enumerate(tangent_basis):
            mixed_quadratic_curvature = (
                direction_first @ direction_second
                + direction_second @ direction_first
            )
            hessian[first, second] = (
                2.0
                * np.real(
                    np.trace(
                        linear_curvatures[first].conj().T
                        @ linear_curvatures[second]
                    )
                )
                + 2.0
                * np.real(
                    np.trace(
                        vacuum_curvature.conj().T @ mixed_quadratic_curvature
                    )
                )
            ) / 7.0

    hessian_eigenvalues = np.linalg.eigvalsh(hessian)
    hessian_symmetry_residual = float(np.linalg.norm(hessian - hessian.T))

    direction = tangent_basis[0]
    step = 1.0e-4
    action_zero = normalized_curvature_action(grading)
    finite_difference_second_derivative = (
        normalized_curvature_action(grading + step * direction)
        - 2.0 * action_zero
        + normalized_curvature_action(grading - step * direction)
    ) / step**2

    result = {
        "gate": "version7_rank_changing_superconnection_admission_gate",
        "affine_carrier": {
            "P1_rank": int(np.linalg.matrix_rank(p1)),
            "P3_rank": int(np.linalg.matrix_rank(p3)),
            "E_aff_complex_dimension": 12,
            "E_aff_real_dimension": 24,
            "projector_residual": projector_residual,
            "orthonormal_basis_residual": basis_residual,
            "P3_reconstruction_residual": reconstruction_residual,
            "S4_covariance_residual": covariance_residual,
            "rank_strata": rank_strata,
        },
        "real_odd_completion": {
            "selfadjoint_residual": selfadjoint_residual,
            "real_condition_residual": real_condition_residual,
            "grading_oddness_residual": oddness_residual,
        },
        "single_parent_functional": {
            "definition": "normalized trace of F*F with F=A^2",
            "independent_sector_weights": 0,
            "vacuum_action_flat_surrogate": action_zero,
            "P1_specification_pass": True,
        },
        "flat_surrogate_hessian": {
            "real_dimension": 24,
            "minimum_eigenvalue": float(np.min(hessian_eigenvalues)),
            "maximum_eigenvalue": float(np.max(hessian_eigenvalues)),
            "expected_eigenvalue": 8.0 / 7.0,
            "negative_eigenvalue_count": int(np.sum(hessian_eigenvalues < -1e-10)),
            "zero_eigenvalue_count": int(np.sum(np.abs(hessian_eigenvalues) < 1e-10)),
            "hessian_symmetry_residual": hessian_symmetry_residual,
            "finite_difference_second_derivative": float(
                finite_difference_second_derivative
            ),
            "finite_difference_residual": float(
                abs(finite_difference_second_derivative - 8.0 / 7.0)
            ),
        },
        "entry_contract": {
            "P0_common_typed_carrier": "preliminary_pass",
            "P1_single_action_single_trace": "preliminary_pass",
            "P2_computable_hessian": "pass",
            "P2_flat_surrogate_negative_mode": False,
            "P3_to_P5": "not_tested",
            "P6_gate_audit_result_stop_rule": "pass",
        },
        "remaining_obligations": {
            "full_H15_physical_oneform_dimension": True,
            "gauge_real_junk_brst_bv_factorization": True,
            "noncentral_DF_and_spatial_curvature_hessian": True,
            "physical_negative_mode": True,
            "nonlinear_rank_change_endpoint": True,
        },
        "verdict": {
            "tome7_admission": "pass_for_full_physical_hessian_gate",
            "matter_birth": False,
            "flat_rank_variability_is_trigger": False,
            "next_gate": "version7_full_physical_rank_field_hessian_gate",
        },
    }

    tolerance = 1e-10
    assert result["affine_carrier"]["P1_rank"] == 1
    assert result["affine_carrier"]["P3_rank"] == 3
    assert projector_residual < tolerance
    assert basis_residual < tolerance
    assert reconstruction_residual < tolerance
    assert covariance_residual < tolerance
    assert [entry["odd_operator_rank"] for entry in rank_strata] == [0, 2, 4, 6]
    assert selfadjoint_residual < tolerance
    assert real_condition_residual < tolerance
    assert oddness_residual < tolerance
    assert hessian_symmetry_residual < tolerance
    assert np.max(np.abs(hessian_eigenvalues - 8.0 / 7.0)) < tolerance
    assert result["flat_surrogate_hessian"]["negative_eigenvalue_count"] == 0
    assert result["flat_surrogate_hessian"]["zero_eigenvalue_count"] == 0
    assert result["flat_surrogate_hessian"]["finite_difference_residual"] < 1e-6

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v7_rank_changing_superconnection_admission_gate_results.json"
    )
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()