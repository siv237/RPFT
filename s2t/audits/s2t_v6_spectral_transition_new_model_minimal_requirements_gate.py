#!/usr/bin/env python3
"""Audit the admission contract for a new spectral-birth model."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_new_model_minimal_requirements_gate_results.json"


def main() -> None:
    requirements = {
        "R0_typed_physical_carrier": "mandatory",
        "R1_single_parent_functional": "mandatory",
        "R2_endogenous_trigger": "mandatory",
        "R3_path_measure_and_rate": "mandatory",
        "R4_stable_localized_endpoint": "mandatory",
        "R5_blind_numeric_prediction": "mandatory",
        "R6_prefixed_failure_certificates": "mandatory",
    }
    current = {
        "R0_typed_physical_carrier": "partial",
        "R1_single_parent_functional": False,
        "R2_endogenous_trigger": False,
        "R3_path_measure_and_rate": False,
        "R4_stable_localized_endpoint": False,
        "R5_blind_numeric_prediction": False,
        "R6_prefixed_failure_certificates": True,
    }
    rejected_shortcuts = [
        "rank_insertion",
        "hidden_portal",
        "external_quench_without_dynamic_source",
        "topology_interpreted_as_probability",
        "unstable_saddle_interpreted_as_matter",
    ]
    admitted = all(value is True for value in current.values())
    result = {
        "gate": "version6_spectral_transition_new_model_minimal_requirements_gate",
        "contract": requirements,
        "current_version_assessment": current,
        "rejected_shortcuts": rejected_shortcuts,
        "verdict": {
            "contract_is_necessary": True,
            "contract_is_sufficient": False,
            "current_version_admitted_as_dynamic_birth_model": admitted,
            "current_version_remains_valid_classification_kinematics_base": True,
            "candidate_comparison_may_start": True,
        },
        "next_gate": "version6_spectral_transition_new_model_candidate_menu_gate",
    }
    assert len(requirements) == 7
    assert len(rejected_shortcuts) == 5
    assert not admitted
    assert result["verdict"]["contract_is_necessary"]
    assert not result["verdict"]["contract_is_sufficient"]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()