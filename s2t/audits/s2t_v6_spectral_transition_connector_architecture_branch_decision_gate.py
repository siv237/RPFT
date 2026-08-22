#!/usr/bin/env python3
"""Reproducible ledger for the post-connector architecture decision.

The audit does not invent a new interaction.  It reads the three completed
connector audits and checks which architectural options remain compatible
with their verdicts and with the no-hidden-extension rule.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / (
    "s2t_v6_spectral_transition_connector_architecture_"
    "branch_decision_gate_results.json"
)


def load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def main() -> None:
    localization = load(
        "s2t_v6_spectral_transition_rank_change_localization_gate_results.json"
    )
    direct = load(
        "s2t_v6_spectral_transition_radial_bridge_vortex_connector_gate_results.json"
    )
    two_step = load(
        "s2t_v6_spectral_transition_morita_two_step_connector_gate_results.json"
    )
    support = load(
        "s2t_v6_spectral_transition_higgs_resolved_support_gate_results.json"
    )
    vortex = load(
        "s2t_v6_bosonic_defect_full_tensor_internal_gap_gate_results.json"
    )

    certificates = {
        "radial_bridge_localizes_rank_change": localization["verdict"][
            "existing_vortex_localizes_neutrino_rank_change"
        ],
        "direct_connector_exists": direct["verdict"][
            "canonical_direct_family_vortex_Higgs_connector_in_established_fields"
        ],
        "mixed_module_selects_unique_connector": direct["verdict"][
            "mixed_module_selects_unique_nonzero_connector"
        ],
        "two_step_connector_exists": two_step["verdict"][
            "current_architecture_has_internal_vortex_Higgs_connector"
        ],
        "new_bifundamental_extends_model": direct["verdict"][
            "new_bifundamental_would_extend_the_model"
        ],
        "Higgs_resolved_support_exists": support["verdict"][
            "Higgs_resolved_split_passes"
        ],
        "straight_vortex_transversely_stable": vortex["verdict"][
            "full_transverse_linear_stability_closed"
        ],
    }

    assert certificates["radial_bridge_localizes_rank_change"] is False
    assert certificates["direct_connector_exists"] is False
    assert certificates["mixed_module_selects_unique_connector"] is False
    assert certificates["two_step_connector_exists"] is False
    assert certificates["new_bifundamental_extends_model"] is True
    assert certificates["Higgs_resolved_support_exists"] is True
    assert certificates["straight_vortex_transversely_stable"] is True

    options = {
        "continue_hidden_connector_search": {
            "compatible_with_completed_ledger": False,
            "reason": (
                "radial, direct degree-one and graded degree-two mechanisms "
                "have all failed independently"
            ),
        },
        "insert_portal_or_bifundamental_without_new_version": {
            "compatible_with_no_hidden_extension_rule": False,
            "reason": (
                "the coefficient or nonzero mixed section is not selected by "
                "the current trace, calculus or carrier"
            ),
        },
        "separate_spectral_and_vortex_sectors_in_version6": {
            "compatible_with_completed_ledger": True,
            "preserves_Higgs_resolved_spectral_support": True,
            "preserves_stable_bosonic_vortex": True,
            "claims_observed_matter_identification": False,
        },
    }

    selected = "separate_spectral_and_vortex_sectors_in_version6"
    assert options[selected]["compatible_with_completed_ledger"] is True

    result = {
        "gate": (
            "version6_spectral_transition_connector_architecture_"
            "branch_decision_gate"
        ),
        "input_certificates": certificates,
        "architecture_options": options,
        "decision": {
            "selected_option": selected,
            "search_for_another_hidden_current-parent_connector": False,
            "new_portal_or_bifundamental_requires_declared_new_model": True,
            "spectral_transition_remains_active": True,
            "bosonic_vortex_remains_active_as_independent_sector": True,
            "bosonic_vortex_identified_with_observed_particle": False,
            "universal_gravitational_coupling_derived": False,
            "physical_closure": False,
        },
        "next_gate": (
            "version6_spectral_transition_higgs_vacuum_topology_"
            "localization_gate"
        ),
        "next_null_hypothesis": (
            "after the electroweak gauge quotient, one Higgs doublet has no "
            "topological class supporting a stable wall, string or monopole "
            "that forces H=0 and localizes the rank-changing support"
        ),
    }

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()