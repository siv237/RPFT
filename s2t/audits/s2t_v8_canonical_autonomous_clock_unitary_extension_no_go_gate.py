#!/usr/bin/env python3
"""LCF audit of the autonomous clock-unitary extension ambiguity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_canonical_autonomous_clock_unitary_extension_no_go_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_autonomous_clock_unitary import (  # noqa: E402
    build_certificate,
)
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.system_dimension == 21
    assert certificate.environment_dimension == 13
    assert certificate.complement_dimension == 252
    assert certificate.extension_parameter_dimension == 63504
    assert certificate.real_even_extension_count_lower_bound == 2
    ambiguity = certificate.ambiguity_theorem.proposition.data
    assert ambiguity["same_reduced_channel"]
    assert ambiguity["complex_phase_family"] == "U(1)"
    assert ambiguity["real_even_surviving_choices"] == ("+1", "-1")
    assert not ambiguity["unique_covariant_unitary_extension"]

    registry = verify_all()
    registered = next(
        gate
        for gate in registry["gates"]
        if gate["identifier"]
        == "version8_canonical_autonomous_clock_unitary_extension_no_go_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 4

    result = {
        "date": "2026-08-29",
        "gate": "version8_canonical_autonomous_clock_unitary_extension_no_go_gate",
        "stinespring_input": {
            "system_dimension": 21,
            "environment_dimension": 13,
            "ambient_dimension": 273,
            "image_dimension": 21,
            "complement_dimension": 252,
            "minimal_environment": True,
            "gauge_covariant_isometry": True,
        },
        "extension_family": {
            "formula": "V_z=P_W+z(I-P_W), U_z=V_z U_0",
            "condition": "abs(z)=1",
            "V_z_W_equals_W": True,
            "same_reduced_Kraus_channel": True,
            "gauge_covariant": True,
            "complex_ambiguity": "U(1)",
            "full_unconstrained_family": "U(252)",
            "full_family_real_parameter_dimension": 63504,
            "real_even_survivors": ["z=+1", "z=-1"],
            "real_even_ambiguity_at_least": 2,
        },
        "interpretation_boundary": {
            "finite_history_parent_exists": True,
            "channel_selects_unique_full_unitary": False,
            "gauge_covariance_selects_unique_full_unitary": False,
            "real_and_even_typing_select_unique_full_unitary": False,
            "canonical_clock_hamiltonian_log_U_selected": False,
            "additive_Page_Wootters_constraint_selected": False,
            "physical_tick_duration_selected": False,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "gate_count": registry["gate_count"],
            "total_obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][
                "version8_canonical_autonomous_clock_unitary_extension_no_go_gate"
            ],
        },
        "verdict": {
            "canonical_autonomous_clock_unitary_derived": False,
            "nonuniqueness_survives_gauge_real_and_even_constraints": True,
            "finite_conditional_history_bridge_remains_valid": True,
            "status": "lcf_checked_covariant_autonomous_clock_unitary_no_go",
            "next_gate": "microscopic_interaction_hamiltonian_or_clock_action_origin_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()