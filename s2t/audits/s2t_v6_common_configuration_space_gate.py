#!/usr/bin/env python3
"""Audit the finite-rank exchange bridge for the balanced Toeplitz pair."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def rectangular_shift(size: int) -> np.ndarray:
    """Isometry C^size -> C^(size+1), e_j -> e_(j+1)."""
    shift = np.zeros((size + 1, size), dtype=float)
    for column in range(size):
        shift[column + 1, column] = 1.0
    return shift


def main() -> None:
    cutoff = 12
    coefficient_rank = 15
    coefficient_ambient_rank = 105
    identity_q = np.eye(coefficient_rank)

    shift = rectangular_shift(cutoff)
    defect_projection = np.zeros((cutoff + 1, cutoff + 1), dtype=float)
    defect_projection[0, 0] = 1.0

    shift_q = np.kron(shift, identity_q)
    projection_q = np.kron(defect_projection, identity_q)

    domain_plus = cutoff * coefficient_rank
    domain_minus = (cutoff + 1) * coefficient_rank
    codomain_plus = domain_minus
    codomain_minus = domain_plus
    total_dimension = domain_plus + domain_minus

    zero_top_right = np.zeros((codomain_plus, domain_minus))
    zero_bottom_left = np.zeros((codomain_minus, domain_plus))
    pair = np.block(
        [
            [shift_q, zero_top_right],
            [zero_bottom_left, shift_q.T],
        ]
    )
    bridge = np.block(
        [
            [np.zeros_like(shift_q), projection_q],
            [zero_bottom_left, np.zeros_like(shift_q.T)],
        ]
    )

    pair_rank = int(np.linalg.matrix_rank(pair, tol=1e-10))
    pair_nullity = total_dimension - pair_rank
    pair_cokernel = total_dimension - pair_rank
    bridge_rank = int(np.linalg.matrix_rank(bridge, tol=1e-10))

    samples: list[dict[str, float | int | bool]] = []
    for coupling in (0.0, 0.1, 0.25, 0.5, 1.0):
        operator = pair + coupling * bridge
        singular_values = np.linalg.svd(operator, compute_uv=False)
        samples.append(
            {
                "coupling": coupling,
                "rank": int(np.linalg.matrix_rank(operator, tol=1e-10)),
                "nullity": total_dimension
                - int(np.linalg.matrix_rank(operator, tol=1e-10)),
                "smallest_singular_value": float(np.min(singular_values)),
                "expected_smallest_singular_value": coupling,
                "invertible": bool(np.min(singular_values) > 1e-10),
            }
        )

    completed = pair + bridge
    identity_total = np.eye(total_dimension)
    left_unitarity_residual = float(
        np.linalg.norm(completed.T @ completed - identity_total)
    )
    right_unitarity_residual = float(
        np.linalg.norm(completed @ completed.T - identity_total)
    )

    # Canonical exchange identification from the domain ordering
    # C^(N r) + C^((N+1) r) to the codomain ordering in the reverse order.
    exchange = np.block(
        [
            [np.zeros((codomain_plus, domain_plus)), np.eye(domain_minus)],
            [np.eye(domain_plus), np.zeros((codomain_minus, domain_minus))],
        ]
    )
    exchange_identified = exchange.T @ completed
    exchange_selfadjoint_residual = float(
        np.linalg.norm(exchange_identified.T - exchange_identified)
    )
    exchange_involution_residual = float(
        np.linalg.norm(exchange_identified @ exchange_identified - identity_total)
    )

    result = {
        "gate": "version6_common_configuration_space_gate",
        "finite_rectangular_model": {
            "cutoff": cutoff,
            "coefficient_rank": coefficient_rank,
            "coefficient_ambient_rank": coefficient_ambient_rank,
            "total_square_dimension": total_dimension,
            "oriented_plus_rectangular_dimensions": [
                codomain_plus,
                domain_plus,
            ],
            "oriented_minus_rectangular_dimensions": [
                codomain_minus,
                domain_minus,
            ],
        },
        "uncoupled_balanced_pair": {
            "ordinary_index": 0,
            "kernel_dimension": pair_nullity,
            "cokernel_dimension": pair_cokernel,
            "positive_defect_dimension": pair_nullity + pair_cokernel,
            "normalized_block_deficit": (pair_nullity + pair_cokernel)
            / (2 * coefficient_ambient_rank),
            "each_oriented_branch_dimension_obstruction": coefficient_rank,
            "branch_preserving_invertibility": False,
        },
        "exchange_bridge": {
            "rank": bridge_rank,
            "maps_kernel_to_cokernel": True,
            "path_samples": samples,
            "unitary_at_coupling_one": left_unitarity_residual < 1e-10
            and right_unitarity_residual < 1e-10,
            "left_unitarity_residual": left_unitarity_residual,
            "right_unitarity_residual": right_unitarity_residual,
            "exchange_identified_selfadjoint": exchange_selfadjoint_residual
            < 1e-10,
            "exchange_identified_involution": exchange_involution_residual
            < 1e-10,
            "exchange_selfadjoint_residual": exchange_selfadjoint_residual,
            "exchange_involution_residual": exchange_involution_residual,
        },
        "infinite_operator_identities": {
            "T_lambda_invertible_for_lambda_positive": True,
            "minimum_singular_value": "min(1, lambda)",
            "T_one_unitary": True,
            "non_Fredholm_crossing_needed_to_remove_pair_zero_modes": False,
        },
        "topological_interpretation": {
            "oriented_half_indices": [-coefficient_rank, coefficient_rank],
            "full_ordinary_index": 0,
            "complex_K_homology_class_changed_by_finite_rank_bridge": False,
            "invertible_representative_implies_zero_KO_class": False,
            "project_KO6_class": coefficient_rank,
            "project_normalized_KO_weight": coefficient_rank
            / coefficient_ambient_rank,
            "real_KO_class_preserved_if_full_symmetry_compatible": True,
            "full_real_and_Clifford_compatibility_verified": False,
            "kernel_cokernel_one_seventh_is_global_pair_invariant": False,
            "kernel_cokernel_one_seventh_is_oriented_block_invariant": True,
        },
        "configuration_space_fork": {
            "orientation_block_diagonal_space": "defect_protected",
            "exchange_compact_bridge_space": "invertible_completion_exists",
            "physical_zero_vacuum_space": "not_yet_identified",
            "latent_nonzero_class_exposure_mechanism": "reopened",
        },
        "remaining_obligations": {
            "bridge_is_parent_one_form": False,
            "full_project_J_and_Clifford_compatibility": False,
            "gauge_and_BV_BRST_compatibility": False,
            "single_parent_potential_for_bridge": False,
            "vacuum_KO_class_selected": False,
        },
        "verdict": {
            "common_operator_space": "partial_pass",
            "new_mechanism": "latent_KO_class_exposed_by_bridge_closure",
            "physical_closure": False,
            "next_gate": "version6_exchange_bridge_parent_admissibility_gate",
        },
    }

    assert pair_nullity == coefficient_rank
    assert pair_cokernel == coefficient_rank
    assert bridge_rank == coefficient_rank
    assert abs(result["uncoupled_balanced_pair"]["normalized_block_deficit"] - 1 / 7) < 1e-14
    assert all(
        abs(sample["smallest_singular_value"] - sample["expected_smallest_singular_value"])
        < 1e-10
        for sample in samples
    )
    assert left_unitarity_residual < 1e-10
    assert right_unitarity_residual < 1e-10
    assert exchange_selfadjoint_residual < 1e-10
    assert exchange_involution_residual < 1e-10

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_common_configuration_space_gate_results.json"
    )
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()