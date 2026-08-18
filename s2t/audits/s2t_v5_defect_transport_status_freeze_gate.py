#!/usr/bin/env python3
"""Статусная заморозка дефектно-транспортной ветви Тома V."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_defect_transport_status_freeze_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


h15 = load_result("s2t_v5_h15_neutrino_degree_split_gate_results.json")
boundary = load_result("s2t_v5_massless_holonomy_defect_index_gate_results.json")
localization = load_result("s2t_v5_holonomy_zero_mode_localization_gate_results.json")
root_menu = load_result("s2t_majorana_root_source_menu_results.json")
bl = load_result("s2t_bl_root_extension_gate_results.json")
quiver = load_result("s2t_v4_family_defect_quiver_moment_map_gate_results.json")
ko6 = load_result("s2t_v4_family_defect_ko6_quiver_embedding_gate_results.json")
hs = load_result("s2t_v4_family_defect_fermionic_measure_hs_gate_results.json")

assert h15["architecture_comparison"]["H15"]["observed_dimension"] == 15
assert "nu_R" not in h15["architecture_comparison"]["H15"]["observed_blocks"]
assert h15["architecture_comparison"]["H16"]["observed_blocks"]["nu_R"] == 1
assert h15["nontrivial_change_under_H16"]["is_harmless_extension_of_current_parent"] is False
assert boundary["twisted_circle_spectrum"]["zero_level_count_single_chiral"] == 1
assert localization["verdict"]["parameter_free_localization_width"] == "fail"
assert root_menu["exhaustive_gate"]["existing_mandatory_root_sources"] == 0
assert bl["continuous_anomaly_gate_passes"]
assert ko6["status"]["ordinary_spectral_action_moment_map_origin"] == "fail_by_mixed_sign"
assert hs["verdict"]["imaginary_HS_origin"] == "not_derived"

h15_data = h15["architecture_comparison"]["H15"]
h16_data = h15["architecture_comparison"]["H16"]

requirements = [
    "compatible_with_current_M35_trace",
    "mandatory_root_assignment",
    "correct_charge_two_pairing_type",
    "invariant_Majorana_vertex",
    "parent_derived_kinetic_and_potential",
    "localized_variational_saddle",
]

candidates = [
    {
        "candidate": "current_H15_M35_transport",
        "passes": {
            "compatible_with_current_M35_trace": True,
            "mandatory_root_assignment": False,
            "correct_charge_two_pairing_type": False,
            "invariant_Majorana_vertex": False,
            "parent_derived_kinetic_and_potential": False,
            "localized_variational_saddle": False,
        },
        "finding": "It supplies the left chiral boundary zero and the 4/7,3/7 trace weights, but contains no nu_R and no degree-five Majorana correspondence.",
    },
    {
        "candidate": "H16_with_U1_B_minus_L",
        "passes": {
            "compatible_with_current_M35_trace": False,
            "mandatory_root_assignment": True,
            "correct_charge_two_pairing_type": True,
            "invariant_Majorana_vertex": True,
            "parent_derived_kinetic_and_potential": False,
            "localized_variational_saddle": False,
        },
        "finding": "It supplies N_c, the root charge and Phi N_c N_c, but changes the carrier to M20x16, the linking algebra to M36 and the trace weights to 5/9,4/9; its nonuniform condensate remains conditional.",
    },
    {
        "candidate": "family_moment_map_quiver",
        "passes": {
            "compatible_with_current_M35_trace": False,
            "mandatory_root_assignment": False,
            "correct_charge_two_pairing_type": True,
            "invariant_Majorana_vertex": False,
            "parent_derived_kinetic_and_potential": False,
            "localized_variational_saddle": False,
        },
        "finding": "The quiver fixes Y=Phi I3 and the desired algebraic square, but it is a separate 18-dimensional KO6 geometry; the ordinary spectral quartic has the wrong mixed sign.",
    },
    {
        "candidate": "relative_auxiliary_or_HS_completion",
        "passes": {
            "compatible_with_current_M35_trace": False,
            "mandatory_root_assignment": False,
            "correct_charge_two_pairing_type": True,
            "invariant_Majorana_vertex": False,
            "parent_derived_kinetic_and_potential": False,
            "localized_variational_saddle": False,
        },
        "finding": "The real auxiliary field has the wrong sign, the degree-two middle module is removed by junk, and the Gaussian Pfaffian does not derive the imaginary Hubbard-Stratonovich contour.",
    },
    {
        "candidate": "H15_degree_five_Weinberg_or_defect_correspondence",
        "passes": {
            "compatible_with_current_M35_trace": True,
            "mandatory_root_assignment": False,
            "correct_charge_two_pairing_type": False,
            "invariant_Majorana_vertex": False,
            "parent_derived_kinetic_and_potential": False,
            "localized_variational_saddle": False,
        },
        "finding": "This is the representation-compatible open target, not an existing construction: the gauge-invariant degree-five operator is allowed, but its family tensor, differential degree, normalization and defect saddle are not derived.",
    },
]

for candidate in candidates:
    assert set(candidate["passes"]) == set(requirements)
    candidate["pass_count"] = sum(candidate["passes"].values())
    candidate["all_requirements_pass"] = all(candidate["passes"].values())

assert not any(candidate["all_requirements_pass"] for candidate in candidates)

result = {
    "gate": "version5_defect_transport_status_freeze_gate",
    "frozen_positive_results": {
        "current_parent": "H15 on M20x15(C) inside M35(C)",
        "trace_weights": ["4/7", "3/7"],
        "massless_transport": "Dirac continuum retained",
        "C3_boundary_branches": ["-1/3", "0", "+1/3"],
        "single_left_chiral_zero_level": 1,
        "conditional_real_mod2_parity": 1,
    },
    "architecture_mismatch": {
        "old_vortex_vertex": "Phi N_c N_c",
        "old_vortex_requires_N_c": True,
        "N_c_present_in_H15": False,
        "H15_neutrino_route": "degree-five Weinberg operator or another higher-degree Majorana/defect correspondence",
        "H16_change": {
            "carrier": f'{h15_data["transition_carrier"]} -> {h16_data["transition_carrier"]}',
            "carrier_dimension": f'{h15_data["transition_dimension"]} -> {h16_data["transition_dimension"]}',
            "linking_algebra": f'{h15_data["linking_algebra"]} -> {h16_data["linking_algebra"]}',
            "trace_weights": f'({h15_data["family_corner_weight"]},{h15_data["observed_corner_weight"]}) -> ({h16_data["family_corner_weight"]},{h16_data["observed_corner_weight"]})',
        },
        "hidden_reuse_of_BL_vortex_inside_H15_allowed": False,
    },
    "candidate_ledger": {
        "requirements": requirements,
        "candidates": candidates,
        "complete_candidate_count": 0,
    },
    "missing_parent_object": {
        "not_merely": "one more scalar potential or one more radial profile",
        "H15_minimal_type": "a gauge-equivariant higher-degree Majorana pairing correspondence on Sym^2(L_L tensor H), compatible with the M35 trace and the C3 invariant family line",
        "required_components": [
            "a precisely represented charge-minus-two or lepton-number-minus-two pairing module/section",
            "a covariant derivative including the relevant root or defect sector",
            "a symmetric family pairing map fixed before neutrino data",
            "one parent trace or measure fixing kinetic norm, potential and fermionic coupling",
            "a variational nonuniform saddle and its transverse localization length",
        ],
    },
    "architecture_fork": {
        "branch_A_preserve_H15": "construct and kill-test the higher-degree Majorana pairing correspondence without adding nu_R",
        "branch_B_replace_by_H16": "register a new M36/B-L parent and repeat all trace, measure and normalization gates",
        "selected_next_by_minimal_change_rule": "branch_A_preserve_H15",
        "reason": "H15, M35 and the 4/7,3/7 weights are already derived, whereas H16 changes the parent architecture and adds normalization-sensitive gauge data.",
    },
    "verdict": {
        "defect_transport_part_positive_kinematics": "retained",
        "localized_neutrino_defect": "not_derived",
        "old_BL_vortex_is_a_completion_of_current_H15": False,
        "current_field_content_exhausted_for_direct_boundary_to_core_bridge": True,
        "physical_closure": False,
        "status": "Part II is frozen as a kinematic and topological transport result. The old Phi N_c N_c vortex belongs to H16/B-L, not to the current H15/M35 parent. The minimal compatible reopening target is a higher-degree H15 Majorana pairing correspondence.",
    },
    "next_gate": "version5_h15_majorana_pairing_correspondence_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))