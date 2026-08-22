#!/usr/bin/env python3
"""Audit closure levels of the version VI spectral-transition branch."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_dynamic_closure_status_gate_results.json"


def main() -> None:
    levels = {
        "KO6_Toeplitz_classification": "closed",
        "rank_change_kinematics": "closed",
        "finite_transition_saddle": "control_only",
        "new_numeric_observable": "selection_rules_only",
        "endogenous_trigger": "open",
        "creation_probability_and_rate": "open",
        "stable_observed_endpoint": "open",
    }
    counts = {
        "closed": sum(value == "closed" for value in levels.values()),
        "partial_or_control": sum(value in {"control_only", "selection_rules_only"} for value in levels.values()),
        "open": sum(value == "open" for value in levels.values()),
    }
    result = {
        "gate": "version6_spectral_transition_dynamic_closure_status_gate",
        "closure_levels": levels,
        "counts": counts,
        "global_verdict": {
            "classification_closure": True,
            "kinematic_closure": True,
            "physical_transition_language_supported": True,
            "project_full_generation_saddle": False,
            "endogenous_trigger": False,
            "creation_rate": False,
            "stable_endpoint": False,
            "unified_matter_birth": False,
            "unchanged_architecture_must_stop": True,
            "physical_dynamic_closure": False,
        },
        "minimal_new_model_contract": [
            "gauge_and_Real_covariant_path_on_full_physical_carrier",
            "one_parent_functional_for_vacuum_saddle_and_endpoint",
            "derived_instability_or_quantum_nucleation",
            "computable_rate_with_measure_and_prefactor",
            "stable_localized_endpoint",
            "new_numeric_observable_not_inserted_as_input",
        ],
        "next_gate": "version6_spectral_transition_new_model_minimal_requirements_gate",
    }
    assert counts == {"closed": 2, "partial_or_control": 2, "open": 3}
    assert result["global_verdict"]["unchanged_architecture_must_stop"]
    assert not result["global_verdict"]["physical_dynamic_closure"]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()