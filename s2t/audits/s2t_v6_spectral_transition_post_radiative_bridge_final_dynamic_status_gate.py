#!/usr/bin/env python3
"""Assemble the final dynamic status ledger of Tome VI after the radiative bridge test."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_post_radiative_bridge_final_dynamic_status_gate_results.json"


def load(name: str) -> dict[str, object]:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def main() -> None:
    earlier = load("s2t_v6_spectral_transition_dynamic_closure_status_gate_results.json")
    contract = load("s2t_v6_spectral_transition_new_model_minimal_requirements_gate_results.json")
    phase = load("s2t_v6_modular_cooling_projective_transition_gate_results.json")
    entropy = load("s2t_v6_internal_entropy_transfer_cooling_gate_results.json")
    field = load("s2t_v6_projective_order_parameter_field_spectrum_gate_results.json")
    compacton = load("s2t_v6_spectral_transition_discrete_compacton_branch_status_freeze_gate_results.json")
    reprioritization = load("s2t_v6_spectral_transition_post_compacton_program_reprioritization_gate_results.json")
    radiation = load("s2t_v6_spectral_transition_real_pair_radiative_cooling_parent_gate_results.json")
    carrier = load("s2t_v6_spectral_transition_radiative_cooling_common_carrier_attribution_gate_results.json")

    assert earlier["global_verdict"]["classification_closure"] is True
    assert earlier["global_verdict"]["kinematic_closure"] is True
    assert earlier["global_verdict"]["physical_dynamic_closure"] is False
    assert contract["verdict"]["current_version_admitted_as_dynamic_birth_model"] is False
    assert phase["verdict"]["static_transition_kinetics_classified"] is True
    assert phase["verdict"]["internal_cooling_trigger_derived"] is False
    assert entropy["verdict"]["four_state_carrier_can_absorb_ordering_entropy_kinematically"] is True
    assert entropy["verdict"]["autonomous_energy_conserving_cooling_derived"] is False
    assert field["physics_boundary"]["order_parameter_field_derived"] is True
    assert field["verdict"]["standard_model_field_content_derived"] is False
    assert compacton["verdict"]["exact_mathematical_branch_retained"] is True
    assert compacton["verdict"]["autonomous_matter_birth_mechanism_admitted"] is False
    assert reprioritization["selected_route"] == "real_pair_radiative_cooling_parent"
    assert radiation["verdict"]["Real_pair_positive_radiation_current_nonzero"] is True
    assert radiation["verdict"]["one_energy_conserving_cooling_parent_derived"] is False
    assert carrier["verdict"]["common_carrier_is_already_derived_as_one_parent"] is False
    assert carrier["verdict"]["radiative_cooling_route_closed_at_existing_parent_level"] is True

    final_contract = {
        "R0_typed_physical_carrier": {
            "status": "partial",
            "reason": "the family, H15 and walk carriers are individually explicit, but no single attributed interacting carrier contains all three sectors",
        },
        "R1_single_parent_functional": {
            "status": "failed",
            "reason": "the compacton rule, C4 boundary, affine map, projective free energy and outgoing channel do not arise from one parent action",
        },
        "R2_endogenous_trigger": {
            "status": "failed",
            "reason": "the cooling law and vacuum-compatible capture basin are absent; none of 36 generic compacton trials was captured",
        },
        "R3_path_measure_and_rate": {
            "status": "failed",
            "reason": "4pi2 is a walk radiation norm coefficient, not a normalized creation or cooling rate; delta, time and conversion remain free",
        },
        "R4_stable_localized_endpoint": {
            "status": "failed",
            "reason": "the compacton has a continuous neutral manifold and radiative escape and is frozen as a physical endpoint",
        },
        "R5_blind_numeric_prediction": {
            "status": "failed",
            "reason": "no absolute mass, size, lifetime, rate or defect abundance follows from the dynamic branch",
        },
        "R6_prefixed_failure_certificates": {
            "status": "passed",
            "reason": "all positive claims and stop conditions are linked to reproducible gate-audit-result certificates",
        },
    }
    counts = {
        status: sum(item["status"] == status for item in final_contract.values())
        for status in ("passed", "partial", "failed")
    }
    assert counts == {"passed": 1, "partial": 1, "failed": 5}

    strict_results = {
        "KO6_Toeplitz_classification": "closed",
        "rank_change_and_exchange_bridge_kinematics": "closed",
        "projective_static_transition_landscape": "closed_within_declared_functional",
        "projective_Q_field_and_mode_decomposition": "closed",
        "exact_discrete_compacton_branch": "closed_as_mathematical_solution_only",
        "Real_even_radiation_coefficient_4pi2": "closed",
        "factorized_common_carrier_no_go": "closed_negative_result",
    }
    physical_obligations = {
        "one_parent_action": False,
        "vacuum_compatible_endogenous_trigger": False,
        "normalized_creation_or_cooling_rate": False,
        "irreversible_internal_cooling_law": False,
        "unique_stable_localized_matter_endpoint": False,
        "absolute_dynamic_scale_or_blind_abundance": False,
    }
    assert not any(physical_obligations.values())

    result = {
        "gate": "version6_spectral_transition_post_radiative_bridge_final_dynamic_status_gate",
        "supersedes_status_gate": "version6_spectral_transition_dynamic_closure_status_gate",
        "strict_result_ledger": strict_results,
        "exact_numbers_retained": {
            "projective_coexistence_beta": phase["free_energy_landscape"]["coexistence_inverse_temperature"],
            "projective_spinodal_beta": phase["free_energy_landscape"]["isotropic_spinodal_inverse_temperature"],
            "ordering_entropy_export_required": entropy["ordering_budget"]["entropy_export_required"],
            "ordering_effective_energy_released": entropy["ordering_budget"]["effective_energy_released"],
            "minimal_compacton_coupling": compacton["exact_ledger"]["minimal_coupling"],
            "compacton_radiation_density": compacton["exact_ledger"]["radiation_density"],
            "Real_pair_radiation_coefficient": radiation["Real_pair_radiation_test"]["physical_half_trace_flux"],
            "factorized_lift_family_state_residual": carrier["factorized_lift_no_go"]["maximum_family_reduced_state_residual_after_I3_tensor_Uwalk"],
        },
        "physical_dynamic_obligations": physical_obligations,
        "final_R0_R6_contract": final_contract,
        "final_R0_R6_counts": counts,
        "status_transitions_after_earlier_closure": {
            "new_exact_nonlinear_solution_found": True,
            "compacton_endpoint_admitted": False,
            "Real_even_radiation_clue_survived": True,
            "radiation_became_projective_cooling": False,
            "single_parent_functional_status": "downgraded_from_partial_candidate_to_failed_after_common_carrier_attribution",
        },
        "freeze_rule": {
            "continue_same_dynamic_architecture": False,
            "new_gate_allowed_only_if_it_supplies": [
                "one gauge and Real compatible parent action on a common carrier",
                "a vacuum-compatible endogenous trigger",
                "a normalized measure and physical rate",
                "a unique stable localized endpoint",
                "one blind observable not inserted as input",
            ],
            "editorial_conclusion_of_tome6_allowed": True,
        },
        "verdict": {
            "Tome_VI_is_valid_classification_and_kinematics_base": True,
            "Tome_VI_contains_new_exact_nonlinear_and_radiative_results": True,
            "Tome_VI_derives_autonomous_matter_birth": False,
            "Tome_VI_physical_dynamic_branch_frozen": True,
            "unchanged_architecture_must_stop": True,
            "status": "after the earlier classification and kinematic closure, Tome VI tested an exact nonlinear compacton parent and the last Real-pair radiative bridge. The compacton is retained only as a mathematical solution and radiation benchmark. The positive coefficient 4pi2 survives the Real half-trace, but no common parent interaction changes the family state R. The final dynamic contract therefore has one pass, one partial item and five failures. Tome VI remains a reproducible classification, static phase and kinematic foundation, but it does not derive autonomous matter birth, a physical rate or a stable observed endpoint. The present dynamic architecture is frozen; only an editorial conclusion may follow without new parent input.",
            "next_gate": "version6_final_conclusion_and_next_program",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()