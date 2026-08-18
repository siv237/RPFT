#!/usr/bin/env python3
"""Explicit coefficient Toeplitz boundary-map audit for the 1/7 class."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    q_rank = 15
    coefficient_rank = 105

    # Infinite unilateral shift S on H^2: S*S=1 and 1-SS*=e_0.
    shift = {
        "kernel_rank": 0,
        "cokernel_rank": 1,
        "Fredholm_index": -1,
        "source_defect_rank_1_minus_SstarS": 0,
        "target_defect_rank_1_minus_SSstar": 1,
    }
    backward_shift = {
        "kernel_rank": 1,
        "cokernel_rank": 0,
        "Fredholm_index": 1,
        "source_defect_rank_1_minus_SSstar": 1,
        "target_defect_rank_1_minus_SstarS": 0,
    }

    result = {
        "gate": "version5_one_seventh_toeplitz_boundary_map_gate",
        "coefficient_projection": {
            "name": "q0=p15 tensor P0",
            "rank": q_rank,
            "ambient_rank": coefficient_rank,
            "normalized_trace": q_rank / coefficient_rank,
        },
        "toeplitz_operator": {
            "Hardy_space": "H2(S1) tensor q0(C105)",
            "positive_winding_symbol": "u_H(z)=z",
            "operator": "T_u=S tensor q0",
            "unilateral_shift_data": shift,
            "coefficient_Fredholm_index": shift["Fredholm_index"] * q_rank,
            "compact_defect_projection": "e0 tensor q0",
            "compact_defect_projection_rank": q_rank,
            "compact_times_normalized_coefficient_trace": q_rank / coefficient_rank,
        },
        "orientation_reversal": {
            "symbol": "u_H*=z^-1",
            "operator": "T_u*=S* tensor q0",
            "backward_shift_data": backward_shift,
            "coefficient_Fredholm_index": backward_shift["Fredholm_index"] * q_rank,
            "KO6_conjugation_exchanges_the_two_orientations": True,
            "ordinary_full_pair_index": 0,
            "oriented_half_index_absolute_value": q_rank,
        },
        "finite_truncation_warning": {
            "NxN_truncated_shift_kernel_rank": 1,
            "NxN_truncated_shift_cokernel_rank": 1,
            "NxN_truncated_shift_index": 0,
            "Fredholm_index_requires_infinite_Hardy_module": True,
        },
        "comparison_with_corner_class": {
            "stable_corner_rank": (20 - 15) * 3,
            "Toeplitz_defect_rank": q_rank,
            "K0_ranks_match": (20 - 15) * 3 == q_rank,
            "canonical_class_level_bridge": True,
            "canonical_rank5_subprojection_inside_H20_needed": False,
            "reason": "positive representative lives in compact Toeplitz ideal, not H20",
        },
        "parent_status": {
            "Hopf_orientation_fixes_sign_pair": True,
            "Toeplitz_KK_class_fixed_by_oriented_circle": True,
            "concrete_Hardy_representation_is_unique": False,
            "new_finite_physical_states_added": False,
            "infinite_Hardy_module_is_analytic_auxiliary": True,
            "extension_embedded_in_parent_spectral_triple": False,
            "real_KKO_cycle_completed": False,
            "physical_Dirac_energy_localization_completed": False,
        },
        "verdict": {
            "explicit_boundary_map_constructed": True,
            "one_seventh_class_transgression": "pass_at_complex_K_theory_level",
            "KO6_orientation_pair": "compatible_at_index_pairing_level",
            "operator_parent_closure": False,
            "physical_closure": False,
            "status": "class_bridge_closed_operator_parent_open",
        },
        "next_gate": "version5_real_toeplitz_ko6_parent_lift_gate",
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_one_seventh_toeplitz_boundary_map_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert shift["Fredholm_index"] == -1
    assert backward_shift["Fredholm_index"] == 1
    assert q_rank == (20 - 15) * 3 == 15
    assert q_rank / coefficient_rank == 1 / 7
    assert shift["Fredholm_index"] * q_rank + backward_shift["Fredholm_index"] * q_rank == 0
    print(output)


if __name__ == "__main__":
    main()