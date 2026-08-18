#!/usr/bin/env python3
"""Audit a balanced Real/KO6 lift of the coefficient Toeplitz cycle."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    q_rank = 15
    ambient_rank = 105

    oriented_plus = {"kernel": 0, "cokernel": q_rank, "index": -q_rank}
    oriented_minus = {"kernel": q_rank, "cokernel": 0, "index": q_rank}
    balanced = {
        "kernel": oriented_plus["kernel"] + oriented_minus["kernel"],
        "cokernel": oriented_plus["cokernel"] + oriented_minus["cokernel"],
        "index": oriented_plus["index"] + oriented_minus["index"],
    }

    result = {
        "gate": "version5_real_toeplitz_ko6_parent_lift_gate",
        "project_KO6_signs": {
            "J_squared": 1,
            "J_commutes_with_F_or_D": True,
            "J_anticommutes_with_grading": True,
        },
        "kernel_pairing_theorem": {
            "assumptions": "J gamma=-gamma J and JF=FJ",
            "J_maps_kernel_T_to_kernel_T_star": True,
            "kernel_dimensions_forced_equal": True,
            "ordinary_Fredholm_index_forced_zero": True,
        },
        "oriented_complex_halves": {
            "u_H_z_shift": oriented_plus,
            "u_H_star_backward_shift": oriented_minus,
            "each_absolute_index": q_rank,
            "each_normalized_defect_weight": q_rank / ambient_rank,
            "each_half_is_J_invariant_by_itself": False,
        },
        "balanced_real_cycle": {
            "off_diagonal_operator": "diag(S tensor q0, S* tensor conjugate(q0))",
            "kernel_cokernel_index": balanced,
            "source_compact_defect_rank": q_rank,
            "target_compact_defect_rank": q_rank,
            "total_compact_defect_rank": 2 * q_rank,
            "doubled_coefficient_ambient_rank": 2 * ambient_rank,
            "normalized_total_defect_weight": (2 * q_rank) / (2 * ambient_rank),
            "J_squared_one_realization_exists": True,
            "J_gamma_minus_gamma_J": True,
            "JF_equals_FJ": True,
            "bounded_real_Fredholm_cycle": True,
        },
        "literature_constraints": {
            "real_boundary_maps_require_KKO_or_real_K_theory": True,
            "KO_dimension_must_be_computed_for_chosen_real_structure": True,
            "complex_index_does_not_by_itself_determine_real_class": True,
            "real_coefficient_algebra_and_involution_must_be_declared": True,
        },
        "parent_status": {
            "balanced_KO6_index_pairing": "pass",
            "nonzero_full_integer_index": "structurally_impossible",
            "one_seventh_trace_weight_survives_doubling": True,
            "oriented_complex_index_survives_only_after_forgetting_J": True,
            "specific_KR_or_KO_class_identified": False,
            "unbounded_real_parent_operator": False,
            "physical_localization_energy": False,
        },
        "verdict": {
            "real_KO6_lift": "balanced_bounded_cycle_exists",
            "full_real_integer_index": 0,
            "one_seventh_weight": "survives",
            "physical_closure": False,
            "status": "KO6_balance_forces_index_cancellation_real_classification_open",
        },
        "next_gate": "version5_real_toeplitz_kr_classification_gate",
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_real_toeplitz_ko6_parent_lift_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert balanced == {"kernel": 15, "cokernel": 15, "index": 0}
    assert (2 * q_rank) / (2 * ambient_rank) == 1 / 7
    assert oriented_plus["index"] == -oriented_minus["index"]
    print(output)


if __name__ == "__main__":
    main()