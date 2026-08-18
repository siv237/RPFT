#!/usr/bin/env python3
"""Deterministic Gate V.0 architecture-selection ledger."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_architecture_selection_gate_results.json"


candidates = {
    "carrier_first_corrected_toe65": {
        "eligibility": {
            "no_failed_action_import": True,
            "single_N2_conjunction": True,
            "binary_early_gate": True,
            "bounded_initial_class": True,
        },
        "priority": {
            "targets_project_wide_measure_and_vacuum_gap": True,
            "minimal_new_representation_ontology": True,
            "explicit_coefficient_free_candidate_functional": True,
            "prephenomenological_first_test": True,
        },
        "closure": {
            "primary_semantics_frozen": False,
            "finite_gravitational_topology_weights_derived": False,
            "full_physical_hessian_computed": False,
            "two_sector_normalization_theorem": False,
        },
        "N2_target": (
            "one correlation operator jointly defines normalized state, carrier "
            "functional, fluctuation Hessian and finite topology weights"
        ),
        "first_kill_gate": "version5_carrier_measure_freeze_gate",
    },
    "boundary_source_wilson_defect": {
        "eligibility": {
            "no_failed_action_import": True,
            "single_N2_conjunction": True,
            "binary_early_gate": True,
            "bounded_initial_class": False,
        },
        "priority": {
            "targets_project_wide_measure_and_vacuum_gap": False,
            "minimal_new_representation_ontology": False,
            "explicit_coefficient_free_candidate_functional": False,
            "prephenomenological_first_test": True,
        },
        "closure": {
            "primary_semantics_frozen": False,
            "finite_gravitational_topology_weights_derived": False,
            "full_physical_hessian_computed": False,
            "two_sector_normalization_theorem": False,
        },
        "N2_target": (
            "one boundary trace derives fixed charge, condensate, family axis, "
            "exact-one Majorana kernel and an SM-sensitive second sector"
        ),
        "first_kill_gate": "freeze_minimal_boundary_Hilbert_BV_trace",
    },
    "new_finite_geometry": {
        "eligibility": {
            "no_failed_action_import": True,
            "single_N2_conjunction": True,
            "binary_early_gate": True,
            "bounded_initial_class": False,
        },
        "priority": {
            "targets_project_wide_measure_and_vacuum_gap": False,
            "minimal_new_representation_ontology": False,
            "explicit_coefficient_free_candidate_functional": False,
            "prephenomenological_first_test": False,
        },
        "closure": {
            "primary_semantics_frozen": False,
            "finite_gravitational_topology_weights_derived": False,
            "full_physical_hessian_computed": False,
            "two_sector_normalization_theorem": False,
        },
        "N2_target": (
            "a bounded finite-geometry classification derives the required "
            "relative sign and a full-rank physical Hessian"
        ),
        "first_kill_gate": "derive_finite_complexity_bound",
    },
}


def eligibility_pass(candidate):
    return all(candidate["eligibility"].values())


def priority_tuple(candidate):
    row = candidate["priority"]
    return (
        int(row["targets_project_wide_measure_and_vacuum_gap"]),
        int(row["minimal_new_representation_ontology"]),
        int(row["explicit_coefficient_free_candidate_functional"]),
        int(row["prephenomenological_first_test"]),
    )


eligible = [name for name, row in candidates.items() if eligibility_pass(row)]
ranked = sorted(
    candidates,
    key=lambda name: (eligibility_pass(candidates[name]), priority_tuple(candidates[name])),
    reverse=True,
)

primary = ranked[0]
assert primary == "carrier_first_corrected_toe65"
assert eligible == ["carrier_first_corrected_toe65"]
assert not any(all(row["closure"].values()) for row in candidates.values())

required_sources = [
    "s2t/gates/version5_problem_statement.tex",
    "s2t/gates/version5_project_literature_novelty_gate.tex",
    "s2t/gates/version4_tome_conclusion.tex",
    "s2t/results/s2t_v4_tome_conclusion_results.json",
]
source_presence = {path: (ROOT / path).exists() for path in required_sources}
assert all(source_presence.values())

result = {
    "date": "2026-08-15",
    "gate": "version5_architecture_selection_gate",
    "protocol": {
        "type": "lexicographic_prephenomenological_selection",
        "weighted_score_used": False,
        "observed_inputs_used": False,
        "selection_is_architecture_pass": False,
    },
    "candidates": candidates,
    "eligible_candidates": eligible,
    "ranking": ranked,
    "selection": {
        "primary_research_class": primary,
        "independent_control": "boundary_source_wilson_defect",
        "deferred_until_complexity_bound": "new_finite_geometry",
        "reason": [
            "directly targets the project-wide common-measure and vacuum-selection gap",
            "uses the smallest new representation ontology",
            "already has one explicit coefficient-free joint functional candidate",
            "admits a bounded comparison class and an early sign/counterterm gate",
        ],
    },
    "global_status": {
        "mathematical_architecture_passes": 0,
        "physical_closures": 0,
        "phenomenology_authorized": False,
    },
    "next_gate": {
        "name": "version5_carrier_measure_freeze_gate",
        "obligations": [
            "freeze the carrier comparison class and deformation space",
            "choose Gibbs or positive bare spectral semantics without a weighted sum",
            "derive or forbid finite Einstein, Weyl-squared, Euler and nonminimal-scalar coefficients",
            "freeze field and ghost statistics plus vector completion",
            "define the joint Hessian operator",
            "return a binary parent-measure pass or architecture closure",
        ],
    },
    "source_presence": source_presence,
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))