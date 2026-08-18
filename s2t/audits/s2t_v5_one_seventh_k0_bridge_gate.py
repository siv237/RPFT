#!/usr/bin/env python3
"""Audit the two exact 1/7 readings in a common stabilized K0 ledger."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    corner_left = 20
    corner_right = 15
    family_rank = 3
    holonomy_zero_rank = 1
    parent_rank = corner_left + corner_right

    corner_numerator = corner_left - corner_right
    corner_weight = corner_numerator / parent_rank
    holonomy_weight = (corner_right / parent_rank) * (
        holonomy_zero_rank / family_rank
    )

    comparison_rank = parent_rank * family_rank
    stabilized_corner_rank = corner_numerator * family_rank
    stabilized_holonomy_rank = corner_right * holonomy_zero_rank

    # Known central J/family-compatible reductions of H20 use a conjugate
    # singlet pair (rank 2) and three conjugate triplet pairs (rank 6 each).
    known_reduction_ranks = sorted(
        {2 * singlet + 6 * triplets for singlet in (0, 1) for triplets in range(4)}
    )

    result = {
        "gate": "version5_one_seventh_k0_bridge_gate",
        "two_readings": {
            "corner_superdimension": "(20-15)/35=1/7",
            "holonomy_line_weight": "(15/35)*(1/3)=1/7",
            "weights_equal": corner_weight == holonomy_weight,
            "cross_multiplied_identity": "(20-15)*3=15*1=15",
        },
        "common_comparison_algebra": {
            "bookkeeping_algebra": "M35 tensor M3 = M105",
            "total_matrix_rank": comparison_rank,
            "corner_virtual_class_representative_rank": stabilized_corner_rank,
            "holonomy_projection_rank": stabilized_holonomy_rank,
            "K0_ranks_equal": stabilized_corner_rank == stabilized_holonomy_rank,
            "normalized_trace_each": stabilized_corner_rank / comparison_rank,
            "bookkeeping_algebra_is_current_physical_parent": False,
        },
        "positive_representative_problem": {
            "corner_difference_is_virtual_not_a_projection": True,
            "rank5_subprojection_of_H20_needed_before_tensoring": True,
            "known_J_and_family_compatible_reduction_ranks": known_reduction_ranks,
            "canonical_rank5_reduction_present": 5 in known_reduction_ranks,
            "complex_grassmannian_choice_space": "Gr(5,20)",
            "real_dimension_Gr_5_20": 2 * 5 * (20 - 5),
        },
        "partial_isometry_problem": {
            "partial_isometry_exists_after_arbitrary_equal_rank_choices": True,
            "fixed_endpoint_isometry_torsor": "U(15)",
            "real_dimension_U15": 15 * 15,
            "canonical_partial_isometry_derived": False,
            "gauge_J_holonomy_equivariance_derived": False,
        },
        "verdict": {
            "one_seventh_is_accidental_decimal_coincidence": False,
            "exact_trace_identity": True,
            "exact_stable_rank_identity": True,
            "operator_level_bridge": False,
            "physical_closure": False,
            "status": "stable_K0_clue_without_canonical_transgression_map",
        },
        "next_gate": "version5_one_seventh_boundary_transgression_gate",
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_one_seventh_k0_bridge_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert parent_rank == 35
    assert corner_numerator == 5
    assert corner_weight == holonomy_weight == 1 / 7
    assert comparison_rank == 105
    assert stabilized_corner_rank == stabilized_holonomy_rank == 15
    assert known_reduction_ranks == [0, 2, 6, 8, 12, 14, 18, 20]
    assert 5 not in known_reduction_ranks
    print(output)


if __name__ == "__main__":
    main()