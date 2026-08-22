#!/usr/bin/env python3
"""Architecture decision audit for the physical role of the class 15."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_class15_physical_role_branch_decision_gate_results.json"


def main() -> None:
    certificates = {
        "KO6_Toeplitz_class_15_exists": True,
        "class_15_is_physically_irreducible": False,
        "component_classes_12_and_3_exist": True,
        "components_are_dynamically_colocalized": False,
        "Higgs_resolved_supports_are_6_6_2_1": True,
        "single_Higgs_topologically_forces_zero": False,
        "sphaleron_has_Higgs_zero": True,
        "sphaleron_is_stable_particle": False,
        "physical_sphaleron_flow": 4,
        "formal_rank_decorated_product": 15,
        "physical_equivariant_product": 4,
    }

    options = {
        "class15_as_birth_multiplicity_in_version6": {
            "compatible": False,
            "contradictions": [
                "physical spectral flow is 4",
                "support decomposes as 12+3",
                "components are not dynamically colocalized",
                "formal product uses rank q0 as input",
                "sphaleron is an unstable saddle",
            ],
        },
        "insert_full_finite_operator_transition_without_new_model": {
            "compatible": False,
            "reason": "it requires a new operator, action, anomaly audit, KO6 audit and stability analysis",
        },
        "class15_as_classification_ledger_with_componentwise_physics": {
            "compatible": True,
            "preserves_KO6_Toeplitz_result": True,
            "preserves_component_classes": True,
            "does_not_claim_unified_birth_event": True,
        },
    }

    decision = {
        "selected_option": "class15_as_classification_ledger_with_componentwise_physics",
        "class15_is_generation_classification_ledger": True,
        "class15_is_particle_count": False,
        "class15_is_bound_state_rank": False,
        "class15_is_sphaleron_birth_multiplicity": False,
        "new_full_transition_dynamics_requires_declared_new_model": True,
        "version6_unified_generation_birth_is_proven": False,
        "physical_closure": False,
    }

    result = {
        "gate": "version6_spectral_transition_class15_physical_role_branch_decision_gate",
        "input_certificates": certificates,
        "architecture_options": options,
        "decision": decision,
        "surviving_roles": {
            "class15": "classification ledger of the full one-generation coefficient package",
            "classes12_and3": "independent component boundary classes",
            "sphaleron_flow4": "standard chiral electroweak transition observable",
            "rank_changing_Higgs_support": "local transition carrier, not a complete generation birth mechanism",
        },
        "next_gate": "version6_spectral_transition_componentwise_creation_observable_gate",
        "next_null_hypothesis": "the current parent fixes componentwise integer and charge selection rules but no parameter-free creation probability, mass or particle multiplicity",
    }

    assert certificates["KO6_Toeplitz_class_15_exists"]
    assert not certificates["class_15_is_physically_irreducible"]
    assert certificates["physical_sphaleron_flow"] == 4
    assert certificates["formal_rank_decorated_product"] == 15
    assert certificates["physical_equivariant_product"] == 4
    assert not options["class15_as_birth_multiplicity_in_version6"]["compatible"]
    assert not options["insert_full_finite_operator_transition_without_new_model"]["compatible"]
    assert options["class15_as_classification_ledger_with_componentwise_physics"]["compatible"]
    assert not decision["version6_unified_generation_birth_is_proven"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()