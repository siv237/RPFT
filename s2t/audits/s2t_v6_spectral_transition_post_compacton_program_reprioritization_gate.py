#!/usr/bin/env python3
"""Reprioritize Tome VI after freezing the compacton as a matter endpoint."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_post_compacton_program_reprioritization_gate_results.json"


def load(name: str) -> dict[str, object]:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def main() -> None:
    freeze = load("s2t_v6_spectral_transition_discrete_compacton_branch_status_freeze_gate_results.json")
    cooling = load("s2t_v6_modular_cooling_projective_transition_gate_results.json")
    entropy = load("s2t_v6_internal_entropy_transfer_cooling_gate_results.json")
    clock = load("s2t_v6_clock_controlled_energy_conserving_quench_gate_results.json")
    multiplicity = load("s2t_v6_existing_multiplicity_resonant_sink_gate_results.json")
    radiation = load("s2t_v6_spectral_transition_discrete_compacton_character_resolved_radiation_form_factor_gate_results.json")
    degeneracy = load("s2t_v6_spectral_transition_discrete_compacton_energy_degeneracy_boundary_overlap_gate_results.json")
    scale = load("s2t_v6_spectral_transition_discrete_compacton_physical_scale_map_gate_results.json")

    assert freeze["verdict"]["compacton_branch_frozen"] is True
    assert freeze["freeze_rule"]["same_architecture_variants_allowed"] is False
    assert cooling["free_energy_landscape"]["isotropic_spinodal_exact"] == "21/2"
    assert cooling["verdict"]["internal_cooling_trigger_derived"] is False
    assert entropy["four_state_carrier"]["entropy_capacity_sufficient"] is True
    assert entropy["missing_parent_data"]["monotone_reduced_beta_law"] is False
    assert clock["verdict"]["canonical_order_four_clock_is_autonomous_refrigerator"] is False
    assert multiplicity["affine_triplet_certificate"]["P3_is_exactly_degenerate"] is True
    assert multiplicity["canonical_affine_coupling_test"]["creates_uniaxial_split"] is False
    assert radiation["verdict"]["dimensionless_radiation_coefficient_derived"] is True
    assert radiation["verdict"]["radiation_is_capture"] is False
    assert degeneracy["verdict"]["plus_minus_compacton_real_energies_exactly_degenerate"] is True
    assert scale["dimensional_rank_test"]["scale_nullity"] == 1

    criteria = [
        "obeys_compacton_freeze",
        "does_not_require_single_plus_minus_i_selection",
        "reuses_derived_project_data",
        "attacks_internal_cooling_gap",
        "attacks_R2_or_R3",
        "introduces_no_dimensionful_input_at_route_selection",
        "has_a_sharp_next_audit",
    ]
    routes = [
        {
            "route": "restore_compacton_as_particle_endpoint",
            "passes": {
                "obeys_compacton_freeze": False,
                "does_not_require_single_plus_minus_i_selection": False,
                "reuses_derived_project_data": True,
                "attacks_internal_cooling_gap": False,
                "attacks_R2_or_R3": False,
                "introduces_no_dimensionful_input_at_route_selection": True,
                "has_a_sharp_next_audit": False,
            },
            "decision": "rejected_by_freeze",
        },
        {
            "route": "insert_open_jump_or_select_one_character_branch",
            "passes": {
                "obeys_compacton_freeze": False,
                "does_not_require_single_plus_minus_i_selection": False,
                "reuses_derived_project_data": True,
                "attacks_internal_cooling_gap": False,
                "attacks_R2_or_R3": False,
                "introduces_no_dimensionful_input_at_route_selection": False,
                "has_a_sharp_next_audit": False,
            },
            "decision": "rejected_as_manual_gamma_or_boundary_choice",
        },
        {
            "route": "solve_absolute_scale_before_dynamics",
            "passes": {
                "obeys_compacton_freeze": False,
                "does_not_require_single_plus_minus_i_selection": True,
                "reuses_derived_project_data": True,
                "attacks_internal_cooling_gap": False,
                "attacks_R2_or_R3": False,
                "introduces_no_dimensionful_input_at_route_selection": False,
                "has_a_sharp_next_audit": True,
            },
            "decision": "deferred_because_scale_nullity_is_not_the_first_dynamic_obstruction",
        },
        {
            "route": "start_an_unconstrained_new_parent",
            "passes": {
                "obeys_compacton_freeze": True,
                "does_not_require_single_plus_minus_i_selection": True,
                "reuses_derived_project_data": False,
                "attacks_internal_cooling_gap": True,
                "attacks_R2_or_R3": True,
                "introduces_no_dimensionful_input_at_route_selection": True,
                "has_a_sharp_next_audit": False,
            },
            "decision": "admissible_in_principle_but_not_minimal_or_testable_yet",
        },
        {
            "route": "real_pair_radiative_cooling_parent",
            "passes": {
                "obeys_compacton_freeze": True,
                "does_not_require_single_plus_minus_i_selection": True,
                "reuses_derived_project_data": True,
                "attacks_internal_cooling_gap": True,
                "attacks_R2_or_R3": True,
                "introduces_no_dimensionful_input_at_route_selection": True,
                "has_a_sharp_next_audit": True,
            },
            "decision": "selected_as_next_audit_only_not_as_a_derived_mechanism",
        },
        {
            "route": "terminate_tome_without_one_last_bridge_test",
            "passes": {
                "obeys_compacton_freeze": True,
                "does_not_require_single_plus_minus_i_selection": True,
                "reuses_derived_project_data": False,
                "attacks_internal_cooling_gap": False,
                "attacks_R2_or_R3": False,
                "introduces_no_dimensionful_input_at_route_selection": True,
                "has_a_sharp_next_audit": False,
            },
            "decision": "fallback_if_selected_bridge_fails",
        },
    ]
    for route in routes:
        assert set(route["passes"]) == set(criteria)
        route["pass_count"] = sum(route["passes"].values())
    selected = [route for route in routes if route["decision"].startswith("selected")]
    assert len(selected) == 1
    assert selected[0]["pass_count"] == len(criteria)

    next_contract = {
        "role_assignment": {
            "projective_order_parameter": "system whose cooling and instability are to be derived",
            "real_pair": "globally neutral transition/output structure; no selection of one conjugate branch is requested",
            "compacton": "auxiliary finite-amplitude oscillator and source of an already measured radiation form factor, not a particle endpoint",
            "radiation_continuum": "candidate entropy/energy carrying channel, not assumed to be a thermal bath",
        },
        "required_derivations": [
            "a Real-even pair-summed radiation current that does not cancel under the full KO6 completion",
            "one parent energy balance coupling the projective order parameter, compacton oscillator and outgoing modes",
            "derivation of the excitation amplitude delta from the parent state or coupling rather than treating it as an input",
            "a reduced beta update or equivalent monotone obtained from the closed dynamics rather than prescribed beta(t)",
            "crossing of beta_c or beta_sp for a nonzero set of admissible initial states",
            "survival long enough of the auxiliary oscillator to complete the transfer",
        ],
        "immediate_stop_conditions": [
            "the plus/minus Real contributions cancel the pair-summed radiation current",
            "the conversion from radiation norm to projective energy requires a new free coefficient",
            "delta, gamma, beta(t), a C4 axis or a bath state must be inserted independently",
            "total energy cannot be conserved by one parent interaction",
            "the compacton source is destroyed before the projective system reaches coexistence or spinodal instability",
        ],
    }

    result = {
        "gate": "version6_spectral_transition_post_compacton_program_reprioritization_gate",
        "source_gate_count": 8,
        "route_selection_criteria": criteria,
        "route_ledger": routes,
        "selected_route": selected[0]["route"],
        "bridge_data": {
            "coexistence_beta": cooling["free_energy_landscape"]["coexistence_inverse_temperature"],
            "spinodal_beta": cooling["free_energy_landscape"]["isotropic_spinodal_inverse_temperature"],
            "entropy_export_required": entropy["ordering_budget"]["entropy_export_required"],
            "effective_energy_released_at_coexistence": entropy["ordering_budget"]["effective_energy_released"],
            "four_state_entropy_capacity": entropy["four_state_carrier"]["maximum_entropy_capacity_from_pure_state"],
            "minimal_clock_axis_ceiling": clock["energy_block_bound"]["exact_maximum_axis_weight"],
            "target_axis_weight": clock["target_phase"]["coexistence_axis_weight"],
            "affine_resonant_rank": multiplicity["affine_triplet_certificate"]["P3_rank"],
            "radiation_density": radiation["spectral_form_factor"]["spectral_density_at_multiplier_one"],
            "radiation_coefficient_per_cycle": radiation["spectral_form_factor"]["golden_rule_coefficient_per_four_step_cycle"],
            "absolute_scale_nullity": scale["dimensional_rank_test"]["scale_nullity"],
        },
        "next_gate_contract": next_contract,
        "verdict": {
            "compacton_particle_branch_reopened": False,
            "compacton_data_reused_in_new_role": True,
            "single_character_selection_required": False,
            "new_physical_mechanism_already_derived": False,
            "one_minimal_bridge_test_remains": True,
            "status": "the compacton remains frozen as a matter endpoint. The only minimal next test that obeys the freeze and attacks an existing dynamic gap is to ask whether the Real-pair-summed compacton radiation can be embedded in one energy-conserving parent as the internal cooling channel of the already derived projective first-order transition. This is a selected audit target, not a positive mechanism claim.",
            "next_gate": "version6_spectral_transition_real_pair_radiative_cooling_parent_gate",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()