#!/usr/bin/env python3
"""Audit whether an already computed family tensor can seed Tome VIII."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_second_family_tensor_inheritance_no_go_gate_results.json"


def load(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def main():
    loop = load("s2t_v4_common_updown_krajewski_loop_gate_results.json")
    commutator = load("s2t_v4_moment_commutator_modular_gate_results.json")
    incidence = load("s2t_v4_incidence_operator_menu_gate_results.json")
    cycle = load("s2t_v7_higher_cycle_character_mixing_freeze_gate_results.json")

    assert loop["common_loop_generates_cross_word"] is True
    assert loop["nonzero_common_connector_assumed"] is True
    assert loop["orientation_sign_selected"] is False
    assert loop["selected_loop_phases_are_cp_even"] is True
    assert commutator["mass_train_pass"] is False
    assert commutator["ckm_blind_pass"] is False
    assert commutator["ckm_angles"][0] > 0.99
    assert incidence["successful_full_M3_count"] == 12
    assert incidence["selector_exists"] is False
    assert incidence["all_orbit_averages_restore_reducible_algebra"] is True
    assert cycle["verdict"]["single_conjugacy_class_can_select_CKM_eigenvectors"] is False
    assert cycle["verdict"]["family_mixing_branch_frozen_in_current_single_cycle_parent"] is True

    result = {
        "gate": "version8_second_family_tensor_inheritance_no_go_gate",
        "candidate_a_krajewski_cross_loop": {
            "cross_word_derived": loop["common_loop_generates_cross_word"],
            "common_connector_assumed": loop["nonzero_common_connector_assumed"],
            "orientation_selected": loop["orientation_sign_selected"],
            "cp_even_degenerate_minima": loop["selected_loop_phases_are_cp_even"],
            "inheritable_without_new_connector": False,
        },
        "candidate_b_moment_commutator": {
            "formula": commutator["constraint"],
            "independent_eigenvector_sensitive_tensor_exists": True,
            "mass_selected_branch_s12": commutator["ckm_angles"][0],
            "mass_train_pass": commutator["mass_train_pass"],
            "ckm_blind_pass": commutator["ckm_blind_pass"],
            "usable_frozen_physical_branch": False,
        },
        "candidate_c_incidence_menu": {
            "outside_candidates": incidence["outside_candidate_count"],
            "full_M3_candidates": incidence["successful_full_M3_count"],
            "selector_exists": incidence["selector_exists"],
            "orbit_average_restores_reducible_algebra": incidence["all_orbit_averages_restore_reducible_algebra"],
            "canonical_tensor_selected": False,
        },
        "current_tome7_cycle": {
            "single_holonomy_class_function": cycle["exact_walk_character_structure"]["single_holonomy_class_function"],
            "depends_on_eigenvectors": not cycle["exact_walk_character_structure"]["depends_on_eigenphases_not_eigenvectors"],
            "can_select_ckm_eigenvectors": cycle["verdict"]["single_conjugacy_class_can_select_CKM_eigenvectors"],
        },
        "scope": {
            "claim_is_universal_no_go_for_all_future_geometries": False,
            "claim_covers_recorded_concrete_project_candidates": True,
        },
        "verdict": {
            "independent_family_tensor_examples_exist": True,
            "canonical_selected_tensor_in_current_parent_exists": False,
            "blind_validated_inherited_branch_exists": False,
            "primitive_B_inherited_from_project_base": False,
            "all_three_tome8_entry_primitives_current_architecture_closed": True,
            "status": "recorded_family_tensors_exist_but_none_is_canonical_and_blind_validated",
            "next_step": "do_not_open_tome8_until_a_genuinely_new_typed_operator_with_a_predeclared_stop_test_is_proposed",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()