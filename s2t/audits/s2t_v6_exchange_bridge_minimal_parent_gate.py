#!/usr/bin/env python3
"""Audit the minimal parent and canonical action of the exchange bridge."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def matrix_unit(size: int, row: int, column: int) -> np.ndarray:
    unit = np.zeros((size, size), dtype=complex)
    unit[row, column] = 1.0
    return unit


def realification(matrix: np.ndarray) -> np.ndarray:
    """Real matrix of a complex-linear operator."""
    return np.block(
        [[matrix.real, -matrix.imag], [matrix.imag, matrix.real]]
    )


def nullity(matrix: np.ndarray, tolerance: float = 1e-10) -> int:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return int(matrix.shape[1] - np.count_nonzero(singular_values > tolerance))


def main() -> None:
    # If finite matrix units are admitted in the coordinate algebra, represented
    # one-forms a[N,b] span the whole finite matrix algebra at every cutoff.
    cutoff = 7
    number = np.diag(np.arange(cutoff, dtype=float))
    represented_oneforms: list[np.ndarray] = []
    for a_row in range(cutoff):
        for a_column in range(cutoff):
            a = matrix_unit(cutoff, a_row, a_column)
            for b_row in range(cutoff):
                for b_column in range(cutoff):
                    b = matrix_unit(cutoff, b_row, b_column)
                    oneform = a @ (number @ b - b @ number)
                    if np.linalg.norm(oneform) > 1e-12:
                        represented_oneforms.append(oneform.reshape(-1))
    oneform_span = np.stack(represented_oneforms, axis=1)
    oneform_span_dimension = int(np.linalg.matrix_rank(oneform_span, tol=1e-10))

    # Intertwiners between the standard and conjugate standard modules of
    # M_n(C), regarded as a real algebra.  Real exchange removes the residual
    # complex phase and leaves one real scalar bridge amplitude.
    coefficient_test_rank = 3
    real_dimension = 2 * coefficient_test_rank
    identity_real = np.eye(real_dimension)
    equations: list[np.ndarray] = []
    algebra_basis: list[np.ndarray] = []
    for row in range(coefficient_test_rank):
        for column in range(coefficient_test_rank):
            unit = matrix_unit(coefficient_test_rank, row, column)
            algebra_basis.extend([unit, 1j * unit])
    for element in algebra_basis:
        left = realification(element)
        conjugate_right = realification(np.conjugate(element))
        equations.append(
            np.kron(conjugate_right.T, identity_real)
            - np.kron(identity_real, left)
        )
    intertwiner_system = np.vstack(equations)
    intertwiner_dimension = nullity(intertwiner_system)

    conjugation = np.diag(
        np.concatenate(
            [np.ones(coefficient_test_rank), -np.ones(coefficient_test_rank)]
        )
    )
    exchange_equation = np.kron(identity_real, conjugation) - np.kron(
        conjugation, identity_real
    )
    real_exchange_system = np.vstack([intertwiner_system, exchange_equation])
    real_exchange_dimension = nullity(real_exchange_system)

    # Canonical positive curvature action of the completed Toeplitz pair.
    coefficient_rank = 15
    coefficient_ambient_rank = 105
    weight = coefficient_rank / coefficient_ambient_rank

    def action(coupling: float) -> float:
        return 2.0 * weight * (1.0 - coupling**2) ** 2

    samples = [
        {"coupling": coupling, "action": action(coupling)}
        for coupling in (0.0, 0.25, 0.5, 0.75, 1.0)
    ]
    hessian_at_defect = -8.0 * weight
    hessian_at_closed_bridge = 16.0 * weight

    result = {
        "gate": "version6_exchange_bridge_minimal_parent_gate",
        "compact_coordinate_extension": {
            "cutoff": cutoff,
            "represented_oneform_span_dimension": oneform_span_dimension,
            "full_matrix_dimension": cutoff**2,
            "span_is_full_finite_compact_algebra": oneform_span_dimension
            == cutoff**2,
            "single_projector_bridge_is_isolated": False,
            "minimal_parent_status": "fail",
        },
        "real_superconnection_parent": {
            "coefficient_test_rank": coefficient_test_rank,
            "real_intertwiner_dimension_before_exchange": intertwiner_dimension,
            "real_intertwiner_dimension_after_exchange": real_exchange_dimension,
            "canonical_bridge_amplitude_dimension": 1,
            "coordinate_algebra_enlarged": False,
            "H15_charged_oneform_module_enlarged": False,
            "kinematic_parent_status": "pass",
        },
        "canonical_positive_action": {
            "formula": "2*(1/7)*(1-lambda^2)^2",
            "samples": samples,
            "action_at_defect_lambda_zero": action(0.0),
            "action_at_closed_bridge_lambda_one": action(1.0),
            "hessian_at_defect_lambda_zero": hessian_at_defect,
            "hessian_at_closed_bridge_lambda_one": hessian_at_closed_bridge,
            "defect_pair_is_unstable": hessian_at_defect < 0.0,
            "closed_bridge_is_stable": hessian_at_closed_bridge > 0.0,
            "spontaneous_matter_birth_from_this_action": False,
        },
        "verdict": {
            "minimal_kinematic_parent": "real_odd_superconnection_endomorphism",
            "compact_coordinate_parent": "rejected_as_nonminimal",
            "canonical_action_direction": "defect_annihilation_not_birth",
            "mechanism_status": "kinematically_open_dynamically_not_selected",
            "next_gate": "version6_closed_bridge_destabilization_gate",
        },
    }

    assert oneform_span_dimension == cutoff**2
    assert intertwiner_dimension == 2
    assert real_exchange_dimension == 1
    assert abs(action(0.0) - 2 / 7) < 1e-14
    assert action(1.0) == 0.0
    assert abs(hessian_at_defect + 8 / 7) < 1e-14
    assert abs(hessian_at_closed_bridge - 16 / 7) < 1e-14

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_exchange_bridge_minimal_parent_gate_results.json"
    )
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()