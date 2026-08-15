#!/usr/bin/env python3
import json
import math
from pathlib import Path

from scipy.special import k1


def load(name):
    return json.loads(Path(name).read_text(encoding="utf-8"))


def main():
    alpha_inverse = 137.035999177
    alpha = 1.0 / alpha_inverse
    electron_mass = 0.51099895069
    muon_mass = 105.6583755
    s_geo = 4.0 * math.pi**3 + math.pi**2 + math.pi
    s_vac = (
        s_geo
        - 1.0 / (24.0 * s_geo)
        - 1.0 / (math.pi**4 * s_geo**2)
    )
    residual = alpha_inverse - s_vac
    j_required = load("s2t_parent_action_normalization_gate_results.json")[
        "normalization_data"
    ]["required_projection_weight_for_one_third"]

    eta_gate = load("s2t_eta_phase_mass_gate_results.json")
    defect_gate = load("s2t_majorana_defect_parent_action_gate_results.json")
    bv_gate = load("s2t_twisted_twoform_bv_complete_results.json")
    six_gate = load("s2t_six_channel_inverse_susceptibility_results.json")
    threshold_gate = load("s2t_finite_threshold_sign_cone_results.json")
    bl_gate = load("s2t_bl_root_extension_gate_results.json")
    two_loop_gate = load("s2t_two_loop_split_stress_test_results.json")

    single_eta = -0.25
    doubled_same_chirality_eta = 2.0 * single_eta
    k1_aps_arithmetic = (
        -doubled_same_chirality_eta / 2.0 + 1.0 / 12.0
    )

    k2_normalization_product = math.sqrt(2.0) ** 2 * 0.5
    k2_canonical_j = 1.0 * k2_normalization_product
    k2_rank9_j = 9.0 * k2_normalization_product

    k3_required_x = math.pi**2 / (3.0 * alpha)
    k4_candidates = {
        "27/5": 27.0 / 5.0,
        "17/pi": 17.0 / math.pi,
        "pi^2/2+pi/4": math.pi**2 / 2.0 + math.pi / 4.0,
        "pi*sqrt(3)": math.pi * math.sqrt(3.0),
    }
    k4_screen = {
        name: {
            "value": value,
            "relative_error": abs(value - j_required) / j_required,
        }
        for name, value in k4_candidates.items()
    }

    k13_variance = 1.0 / (
        6.0 * ((2.0**4 - 1.0) * math.pi**4 / 90.0)
    )
    k13_two_source_j = math.sqrt(2.0)
    k13_source_factor = k13_two_source_j**2 / 2.0

    target_m_dirac = (
        math.sqrt(math.pi + 1.0 / math.pi)
        * electron_mass**2
        / muon_mass
    )
    k14_radiative_m_dirac = alpha / (4.0 * math.pi) * target_m_dirac

    inverse_power = {
        "residual": residual,
        "S_inverse_3": s_geo**-3,
        "S_inverse_4": s_geo**-4,
        "c3": residual * s_geo**3,
        "c4": residual * s_geo**4,
        "pi2_over_8": math.pi**2 / 8.0,
    }
    inverse_power["c4_relative_to_pi2_over_8"] = (
        inverse_power["c4"] - inverse_power["pi2_over_8"]
    ) / inverse_power["pi2_over_8"]

    tower_data = load("s2t_coexact_tower_results.json")
    tower_n1 = tower_data["first_modes"][0]["contribution_rp3"]
    tower_n3 = tower_data["first_modes"][2]["contribution_rp3"]
    tower_total = tower_data["dimensionless_positive_sum"]["rp3_projected"]
    tower = {
        "n1": tower_n1,
        "n3": tower_n3,
        "total": tower_total,
        "n3_over_total": tower_n3 / tower_total,
        "higher_shells_are_loop_orders": False,
        "reason": (
            "Shell and winding indices label modes inside one determinant. "
            "They do not count Feynman-loop order."
        ),
    }

    candidates = {
        "K1": {
            "arithmetic": k1_aps_arithmetic,
            "arithmetic_hits_one_third": abs(
                k1_aps_arithmetic - 1.0 / 3.0
            )
            < 1e-15,
            "same_chirality_doubling_required": True,
            "real_mass_gate_passes": False,
            "status": "arithmetic_pass_phase_to_mass_fail",
            "reason": (
                "Eta is additive, so two identical eta=-1/4 blocks give -1/2. "
                "But this doubles a determinant phase; the vectorlike real-mass "
                "response still cancels eta blockwise. A conjugate physical doubling "
                "would cancel eta rather than produce -1/2."
            ),
            "evidence_status": eta_gate["status"],
        },
        "K2": {
            "proposed_sqrt2_half_product": k2_normalization_product,
            "canonical_J_after_product": k2_canonical_j,
            "rank9_J_after_product": k2_rank9_j,
            "target_J": j_required,
            "passes": False,
            "status": "normalization_factors_cancel_vertex_map_underdefined",
            "reason": (
                "(sqrt(2))^2 times 1/2 equals one, so the proposal leaves the "
                "canonical J unchanged. Rank division is not specified by an operator."
            ),
        },
        "K3": {
            "required_X": k3_required_x,
            "status": "closed_circular_pruner",
        },
        "K4": {
            "screen": k4_screen,
            "status": "numerical_screen_only_no_operator",
        },
        "K5": {
            "status": "representation_count_only_level_not_derived",
            "reason": "No action derives k=22 or a WZW level shift producing 23.",
        },
        "K6": {
            "status": "conditional_operator_success_parent_action_open",
            "rank_one_kernel_consistent": True,
            "rank23_complement_consistent": True,
            "reason": defect_gate["scientific_verdict"],
        },
        "K7": {
            "status": "regular_representation_not_derived",
            "correction": (
                "24 is the order of S4 and the dimension of its regular "
                "representation, not the dimension of the group itself."
            ),
        },
        "K8": {
            "value": math.e**math.pi,
            "relative_error_to_23": abs(math.e**math.pi - 23.0) / 23.0,
            "status": "closed_numerology_pruner",
        },
        "K9": {
            "status": threshold_gate["status"],
            "reason": threshold_gate["scientific_verdict"],
        },
        "K10": {
            "status": "BL_mixing_cannot_close_full_direction",
            "reason": (
                "B-L kinetic mixing adds a hypercharge-sensitive structure but "
                "does not independently supply the required SU2 and SU3 shifts."
            ),
            "BL_extension_status": bl_gate["status"],
        },
        "K11": {
            "status": "closed_pruner",
            "evidence_status": two_loop_gate["status"],
        },
        "K12": {
            "isolated_zero_shell_one_reversed_complex": math.pi**4 / 6.0,
            "six_copy_zero_shell": math.pi**4,
            "arithmetic_passes": True,
            "full_BV_passes": False,
            "status": "zero_shell_arithmetic_pass_full_BV_action_fail",
            "reason": bv_gate["scientific_verdict"],
        },
        "K13": {
            "variance": k13_variance,
            "target": math.pi**-4,
            "identity_passes": abs(k13_variance - math.pi**-4) < 1e-15,
            "two_source_J": k13_two_source_j,
            "J_squared_over_2": k13_source_factor,
            "source_map_derived": False,
            "status": "identity_pass_source_action_fail",
            "reason": six_gate["scientific_verdict"],
        },
        "K14": {
            "existing_target_mD_MeV": target_m_dirac,
            "radiative_candidate_mD_MeV": k14_radiative_m_dirac,
            "candidate_to_target_ratio": k14_radiative_m_dirac
            / target_m_dirac,
            "status": "extra_alpha_loop_factor_suppresses_existing_target",
            "reason": (
                "The proposed alpha/(4pi) factor makes the already conditional "
                "Dirac insertion smaller by alpha/(4pi), rather than deriving it."
            ),
        },
    }

    results = {
        "status": "K1_K14_priority_batch_closes_repeated_routes_and_rejects_loop_power_interpretation",
        "date": "2026-08-07",
        "candidates": candidates,
        "inverse_power_reverse": {
            **inverse_power,
            "classification": "inverse_power_fit_not_loop_counting",
            "loop_order_derived": False,
            "anchor_uncertainty_propagated": False,
            "conclusion": (
                "The numbers c3 and c4 describe two chosen inverse-power ansatzes. "
                "They neither prove nor disprove three- or four-loop physics."
            ),
        },
        "tower_test": tower,
        "priority_verdict": {
            "K1": "stop in minimal vectorlike model",
            "K2": "define an operator before more numerics",
            "K6": "highest-value live action-level gate",
            "K12": "new graded parent theory only; six copies by target are forbidden",
            "K13": "live parent-action candidate; source normalization remains open",
            "next_best_work": [
                "derive the BdG defect and rank quotient from one parent action",
                "derive a six-channel bosonic half-shifted carrier and source map",
                "externally reproduce R1 before opening more numerical constants",
            ],
            "R_sci": 5,
            "N_closed_physical": 0,
        },
    }

    assert candidates["K1"]["arithmetic_hits_one_third"] is True
    assert candidates["K1"]["real_mass_gate_passes"] is False
    assert abs(k2_normalization_product - 1.0) < 1e-15
    assert candidates["K6"]["rank_one_kernel_consistent"] is True
    assert candidates["K12"]["arithmetic_passes"] is True
    assert candidates["K12"]["full_BV_passes"] is False
    assert candidates["K13"]["identity_passes"] is True
    assert candidates["K13"]["source_map_derived"] is False
    assert tower["higher_shells_are_loop_orders"] is False
    assert results["priority_verdict"]["R_sci"] == 5
    assert results["priority_verdict"]["N_closed_physical"] == 0

    Path("s2t_k1_k14_loop_reverse_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()