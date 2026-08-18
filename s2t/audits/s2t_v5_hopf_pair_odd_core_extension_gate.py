#!/usr/bin/env python3
"""Audit all equal-rank/relative options for an odd Hopf core operator."""

from __future__ import annotations

import json
from pathlib import Path


def rectangular_data(m: int, n: int, rank: int) -> dict[str, int]:
    """Data for T:C^n -> C^m and Q=[[0,T],[T*,0]]."""
    kernel = n - rank
    cokernel = m - rank
    return {
        "rank": rank,
        "kernel_T": kernel,
        "cokernel_T": cokernel,
        "Fredholm_index_T": kernel - cokernel,
        "nullity_selfadjoint_Q": kernel + cokernel,
    }


def main() -> None:
    asymptotic = rectangular_data(20, 15, 15)
    unit_rank_drop = rectangular_data(20, 15, 14)

    # J-compatible central reductions of the frozen family chain are built
    # from the conjugate singlet pair (rank 2) and three conjugate triplet
    # pairs (rank 6 each).
    canonical_reduction_ranks = sorted(
        {2 * singlet + 6 * triplets for singlet in (0, 1) for triplets in range(4)}
    )

    result = {
        "gate": "version5_hopf_pair_odd_core_extension_gate",
        "direct_rectangular_option": {
            "map": "T:C15 -> C20",
            "asymptotic_maximal_rank": asymptotic,
            "one_additional_rank_loss": unit_rank_drop,
            "index_changes_under_rank_drop": (
                asymptotic["Fredholm_index_T"] != unit_rank_drop["Fredholm_index_T"]
            ),
            "extra_zero_modes_from_one_rank_drop": (
                unit_rank_drop["nullity_selfadjoint_Q"]
                - asymptotic["nullity_selfadjoint_Q"]
            ),
            "asymptotic_mass_is_invertible": False,
            "Callias_full_gap_condition": False,
            "normalized_corner_superdimension": "(20-15)/35=1/7",
            "one_over_seven_is_localized_index": False,
        },
        "rank15_subcorner_option": {
            "known_J_and_family_compatible_reduction_ranks": canonical_reduction_ranks,
            "rank15_present": 15 in canonical_reduction_ranks,
            "canonical_reference_rank": 2,
            "canonical_physical_rank": 18,
            "manual_dimensions_to_remove_from_rank18": 3,
            "verdict": "no_derived_rank15_left_subcorner",
        },
        "arrow_conjugate_arrow_option": {
            "spaces": "E=M20x15 and E*=M15x20",
            "complex_dimensions": [300, 300],
            "star_identification_is_complex_linear": False,
            "star_identification_is_antilinear": True,
            "canonical_bimodule_isomorphism_E_to_E_star": False,
            "reason": "left/right factor algebras M20 and M15 are non-isomorphic",
            "state_carrier_if_direct_sum_is_used": 600,
            "current_transition_carrier": 300,
            "hidden_doubling": True,
        },
        "particle_conjugate_150_option": {
            "decomposition": "(H10 tensor H15) direct_sum J(H10 tensor H15)",
            "ranks": [150, 150],
            "canonical_identification": "anti-linear J only",
            "complex_linear_universal_mass_derived": False,
            "H15_contains_sterile_gauge_singlet_nuR": False,
            "full_SM_gauge_equivariant_particle_antiparticle_pairing": False,
        },
        "positive_compressions": {
            "T_star_T_shape": [15, 15],
            "T_T_star_shape": [20, 20],
            "carry_singular_values": True,
            "retain_Hopf_phase_orientation_by_themselves": False,
            "define_odd_map_between_L_and_L_star": False,
        },
        "relative_background_option": {
            "persistent_rank5_kernel_can_be_called_background": True,
            "canonical_projector_removing_it_derived": False,
            "full_asymptotic_operator_gapped_after_no_projection": False,
            "relative_subtraction_is_physical_derivation": False,
        },
        "verdict": {
            "direct_20x15_odd_Callias_operator": "fail_persistent_five_zero_channels",
            "derived_15x15_operator": False,
            "derived_300x300_operator": False,
            "derived_150x150_operator": False,
            "odd_core_extension_inside_version5": "fail",
            "boundary_Hopf_orientation_survives": True,
            "normalized_rank_imbalance_one_over_seven_survives_as_structural_invariant": True,
            "physical_closure": False,
            "status": "hopf_reopening_exhausted_without_gapped_odd_parent_operator",
        },
        "next_gate": "version5_hopf_reopening_final_status_freeze_gate",
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_hopf_pair_odd_core_extension_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert asymptotic == {
        "rank": 15,
        "kernel_T": 0,
        "cokernel_T": 5,
        "Fredholm_index_T": -5,
        "nullity_selfadjoint_Q": 5,
    }
    assert unit_rank_drop["Fredholm_index_T"] == -5
    assert unit_rank_drop["nullity_selfadjoint_Q"] == 7
    assert canonical_reduction_ranks == [0, 2, 6, 8, 12, 14, 18, 20]
    assert 15 not in canonical_reduction_ranks
    print(output)


if __name__ == "__main__":
    main()