#!/usr/bin/env python3
"""Structured literature/novelty audit for the Hopf superconnection branch."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path


def main() -> None:
    sources = [
        {
            "id": "arXiv:2106.01591",
            "year": 2021,
            "status": "peer_reviewed_PTEP_2022",
            "role": "foundational",
            "established": [
                "spacetime-dependent matrix mass fits a Quillen superconnection",
                "superconnection Chern character controls anomaly",
                "Callias-type index is read from asymptotic mass data",
            ],
        },
        {
            "id": "arXiv:2607.24915",
            "year": 2026,
            "status": "recent_preprint",
            "role": "fresh_concrete_model",
            "established": [
                "generic complex matrix tachyon is the odd superconnection field",
                "defect locus is det(T)=0 / loss of invertibility",
                "Chern character localizes near the non-invertible locus",
                "topological charge is a superconnection Chern number",
            ],
        },
        {
            "id": "arXiv:2604.25821",
            "year": 2026,
            "status": "recent_preprint",
            "role": "fresh_operator_algebra_language",
            "established": [
                "Fell line bundles over groupoids encode twisted categorical symmetry data",
                "fibers over morphisms are correspondences",
            ],
        },
        {
            "id": "arXiv:2509.10822",
            "year": 2025,
            "status": "recent_preprint",
            "role": "fresh_Fell_correspondence_language",
            "established": [
                "actions of Fell bundles construct C-star correspondences",
            ],
        },
        {
            "id": "arXiv:2606.12693v2",
            "year": 2026,
            "status": "recent_non_peer_reviewed_preprint",
            "role": "close_conceptual_neighbor",
            "established": [
                "resolved worldline link CP1 and degree-one line are used for carrier reconstruction",
                "Dirac-Callias/Riesz/Schur-Berry completion is deferred rather than completed",
            ],
        },
    ]

    result = {
        "gate": "version5_recent_superconnection_defect_literature_novelty_gate",
        "audit_date": str(date(2026, 8, 17)),
        "sources": sources,
        "dictionary": {
            "project_forward_reverse_lines": "graded bundles L and L* / plus and minus sectors",
            "project_odd_transition": "matrix mass or tachyon T",
            "project_defect_core": "non-invertibility locus of T",
            "project_Hopf_charge": "asymptotic superconnection Chern character / Callias class",
            "project_Fell_line": "twist over transition groupoid",
        },
        "not_novel_individually": [
            "graded superconnection with gauge fields and an odd matrix field",
            "defect as a zero or non-invertibility locus of the odd field",
            "Callias index from asymptotic matrix mass",
            "Fell line bundles and correspondences on groupoids",
        ],
        "project_specific_candidate_novelty": [
            "derivation of transition orientation from unequal Morita corner grading p20-p15",
            "functorial assignment E to L and E* to L* without a fixed new family doublet",
            "joint comparison with the frozen H15/M35 carrier and its no-go ledger",
        ],
        "critical_rank_test": {
            "standard_equal_rank_superconnection_example": "T is N by N and can be invertible off the defect",
            "current_M35_odd_corner_shape": [20, 15],
            "rectangular_map_can_be_invertible": False,
            "minimum_persistent_cokernel_dimension": 5,
            "localized_defect_from_det_T_available": False,
            "possible_equal_rank_retypings": [
                "physical 15 by 15 subcorner",
                "arrow/conjugate-arrow 300 by 300 pair",
            ],
            "both_retypings_currently_derived": False,
        },
        "correction_of_preliminary_reading": {
            "Codazzi_preprint_completes_Dirac_Callias_Riesz": False,
            "actual_status": "lists the completion as subsequent work/output",
            "independent_validation_claim_allowed": False,
        },
        "roadmap_change": {
            "old_question": "can an even SO3 gauge connection smooth L through the core",
            "new_question": "can an existing odd square operator be invertible off the core and lose rank only at the defect",
            "energy_is_automatically_fixed_by_topological_superconnection": False,
            "reason": "fresh models still supply DBI/Yang-Mills or other dynamical terms separately",
        },
        "verdict": {
            "literature_language_support": "strong",
            "direct_solution_for_M35": False,
            "novelty_of_individual_ingredients": "mostly_no",
            "novelty_of_project_specific_assembly": "plausible_but_unproven",
            "status": "reframe_to_odd_noninvertibility_with_rank_balance_gate",
            "physical_closure": False,
        },
        "next_gate": "version5_hopf_pair_odd_core_extension_gate",
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_recent_superconnection_defect_literature_novelty_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert all(s["year"] <= 2026 for s in sources)
    assert result["critical_rank_test"]["minimum_persistent_cokernel_dimension"] == 5
    assert result["critical_rank_test"]["rectangular_map_can_be_invertible"] is False
    assert result["correction_of_preliminary_reading"]["Codazzi_preprint_completes_Dirac_Callias_Riesz"] is False
    print(output)


if __name__ == "__main__":
    main()