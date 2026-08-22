#!/usr/bin/env python3
"""Audit the R0--R6 candidate architecture menu."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_new_model_candidate_menu_gate_results.json"


def main() -> None:
    candidates = {
        "electroweak_sphaleron": {
            "R0": "partial", "hard_conflicts": ["no_full_H15_flow", "unstable_endpoint"],
            "role": "control_transition_saddle", "new_primitives": 0,
        },
        "explicit_QTB_Higgs_portal": {
            "R0": False, "hard_conflicts": ["current_intertwiner_space_zero", "manual_portal_parameter"],
            "role": "rejected_hidden_portal", "new_primitives": 2,
        },
        "Q_ball_or_fermion_bag": {
            "R0": False, "hard_conflicts": ["new_global_charge", "new_potential"],
            "role": "R4_control", "new_primitives": 3,
        },
        "Jackiw_Rebbi_defect_mode": {
            "R0": "partial", "hard_conflicts": ["background_defect_not_derived"],
            "role": "endpoint_submechanism", "new_primitives": 1,
        },
        "dynamical_finite_Dirac_field": {
            "R0": True, "hard_conflicts": [],
            "role": "selected_research_candidate", "new_primitives": 1,
            "open_requirements": ["R2", "R3", "R4", "R5"],
        },
        "discrete_spectral_transition_network": {
            "R0": "open", "hard_conflicts": [],
            "role": "deferred_foundational_rebuild", "new_primitives": 5,
        },
    }
    selected = [name for name, data in candidates.items() if data["role"] == "selected_research_candidate"]
    admitted = []
    result = {
        "gate": "version6_spectral_transition_new_model_candidate_menu_gate",
        "candidates": candidates,
        "decision": {
            "candidates_checked": len(candidates),
            "fully_admitted_R0_to_R6": admitted,
            "selected_for_next_derivation": selected,
            "selection_is_model_admission": False,
            "selection_reason": "preserves the typed H15 carrier and allows one operator parent with the fewest foreign primitives",
            "retrospectively_superseded": True,
        },
        "next_gate": "version6_spectral_transition_candidate_menu_retrospective_correction_gate",
    }
    assert len(candidates) == 6
    assert admitted == []
    assert selected == ["dynamical_finite_Dirac_field"]
    assert candidates[selected[0]]["R0"] is True
    assert candidates[selected[0]]["hard_conflicts"] == []
    assert not result["decision"]["selection_is_model_admission"]
    assert result["decision"]["retrospectively_superseded"]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()