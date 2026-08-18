#!/usr/bin/env python3
"""Literature-led audit of Toeplitz/mapping-cone routes for the 1/7 class."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    winding = 1
    coefficient_rank = 15
    comparison_rank = 105
    toeplitz_index_rank = winding * coefficient_rank

    sources = [
        {
            "arxiv": "1911.05823",
            "role": "Toeplitz extension, winding-index map, operator K-theory review",
            "directly_transferable": True,
        },
        {
            "arxiv": "1604.02337",
            "role": "boundary maps computed by Kasparov product with extension class",
            "directly_transferable": True,
        },
        {
            "arxiv": "0711.3028",
            "role": "mapping cone relates odd and even index pairings with APS data",
            "directly_transferable": "only_after_inclusion_and_Kasparov_module_are_given",
        },
        {
            "arxiv": "1605.08593",
            "role": "mapping-cone/Cuntz-Pimsner exact sequences and partial-isometry classes",
            "directly_transferable": "requires_a_self_correspondence_or_scalar_extension",
        },
        {
            "arxiv": "2512.08304v3",
            "role": "explicit Milnor connecting homomorphism for Hopf-Galois clutching",
            "directly_transferable": "class_level_only_without_project_specific_pullback",
        },
    ]

    result = {
        "gate": "version5_one_seventh_boundary_transgression_literature_gate",
        "literature_sources": sources,
        "toeplitz_candidate": {
            "extension": "0 -> K tensor M105 -> T tensor M105 -> C(S1) tensor M105 -> 0",
            "boundary_unitary": "u_H with winding +1",
            "coefficient_projection": "q0=p15 tensor P0",
            "coefficient_projection_rank": coefficient_rank,
            "boundary_formula": "delta_T([u_H] external_product [q0])=+/-[q0]",
            "image_absolute_rank": toeplitz_index_rank,
            "normalized_trace_absolute_value": toeplitz_index_rank / comparison_rank,
            "matches_stable_corner_rank": toeplitz_index_rank == (20 - 15) * 3,
            "sign_fixed_by_orientation_convention": True,
        },
        "what_is_canonical": {
            "K_theory_boundary_map_once_extension_is_fixed": True,
            "image_K0_class_once_u_H_and_q0_are_fixed": True,
            "individual_partial_isometry_representative": False,
            "physical_energy_or_Dirac_operator": False,
        },
        "project_gap": {
            "Hopf_clutching_unitary_available": True,
            "coefficient_projection_q0_available": True,
            "Toeplitz_or_mapping_cone_extension_inside_current_M35_parent": False,
            "Hardy_polarization_or_disk_filling_derived_from_parent": False,
            "canonical_rank5_subprojection_inside_H20_derived": False,
            "Cuntz_Pimsner_self_correspondence_specified": False,
            "project_specific_Milnor_pullback_specified": False,
        },
        "verdict": {
            "literature_contains_the_general_mechanism": True,
            "class_level_transgression_candidate_is_exact": True,
            "mechanism_is_novel_in_itself": False,
            "project_specific_input": "derive_the_extension_class_from_Hopf_Morita_parent",
            "operator_level_closure": False,
            "physical_closure": False,
            "status": "exact_Toeplitz_class_formula_without_derived_parent_extension",
        },
        "next_gate": "version5_one_seventh_toeplitz_boundary_map_gate",
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_one_seventh_boundary_transgression_literature_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert winding == 1
    assert coefficient_rank == (20 - 15) * 3 == 15
    assert toeplitz_index_rank / comparison_rank == 1 / 7
    assert len(sources) == 5
    print(output)


if __name__ == "__main__":
    main()