#!/usr/bin/env python3
import json
import math
from fractions import Fraction
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def circle_logdet_ratio(rho, beta):
    numerator = math.cosh(2.0 * math.pi * rho) - math.cos(
        2.0 * math.pi * beta
    )
    denominator = math.cosh(2.0 * math.pi * rho) - 1.0
    return math.log(numerator / denominator)


def main():
    tome2 = load_json("s2t_tome2_results.json")
    spin = load_json("s2t_spin_generation_selector_results.json")
    eta_gate = load_json("s2t_eta_phase_mass_gate_results.json")
    conformal = load_json("s2t_conformal_majorana_rank_gate_results.json")
    aps = load_json("s2t_aps_orbifold_inflow_redteam_results.json")
    projection = load_json("s2t_anomaly_free_holonomy_projection_results.json")
    six_channel = load_json("s2t_six_channel_inverse_susceptibility_results.json")
    bl_extension = load_json("s2t_bl_root_extension_gate_results.json")
    trilemma = load_json("s2t_root_mass_condensate_trilemma_results.json")
    nonuniform = load_json("s2t_nonuniform_pairing_saddle_results.json")
    stiffness = load_json("s2t_spectral_pairing_stiffness_gate_results.json")
    threshold = load_json("s2t_finite_threshold_sign_cone_results.json")
    tau = load_json("s2t_tau_uniqueness_normalization_results.json")

    alpha_inverse = tome2["inputs"]["alpha_inv"]
    alpha = 1.0 / alpha_inverse
    eta_menu = spin["spectral_cross_check"]["RP3_spin_eta_invariants"]
    one_twelfth = Fraction(1, 12)
    one_third = Fraction(1, 3)
    eta_arithmetic = {}
    for eta in (Fraction(-1, 4), Fraction(1, 4)):
        value = -eta / 2 + one_twelfth
        eta_arithmetic[str(eta)] = {
            "value": str(value),
            "float": float(value),
            "deficit_to_one_third": str(one_third - value),
        }

    rho = 1.0
    beta = 0.25
    conjugate_errors = {
        "beta_vs_minus_beta": abs(
            circle_logdet_ratio(rho, beta)
            - circle_logdet_ratio(rho, -beta)
        ),
        "beta_vs_one_minus_beta": abs(
            circle_logdet_ratio(rho, beta)
            - circle_logdet_ratio(rho, 1.0 - beta)
        ),
    }
    half_shift = circle_logdet_ratio(rho, 0.5)
    quarter_shift = circle_logdet_ratio(rho, 0.25)
    twice_quarter = 2.0 * quarter_shift

    two_loop_required_x = math.pi**2 / (3.0 * alpha)
    projection_candidate = 12.0 * math.pi / 7.0
    projection_required = tau["qed_integral_audit"][
        "required_jacobian_magnitude"
    ]

    results = {
        "status": "batch_hypothesis_run_reproduces_existing_no_go_results_and_adds_three_precision_pruners_without_new_closed_physics",
        "date": "2026-08-07",
        "frozen_conventions": {
            "train_anchors": ["alpha_inverse", "m_e", "m_mu"],
            "alpha_inverse": alpha_inverse,
            "unit_radii": True,
            "RP3_eta_menu": eta_menu,
            "circle_logdet": "I_rho(beta)=log[(cosh(2*pi*rho)-cos(2*pi*beta))/(cosh(2*pi*rho)-1)]",
        },
        "hypotheses": {
            "G1_APS_real_mass_shift": {
                "eta_menu_arithmetic": eta_arithmetic,
                "eta_minus_one_half_in_menu": -0.5 in eta_menu,
                "blockwise_phase_cancellation": eta_gate[
                    "blockwise_phase_cancellation"
                ]["phase_cancels"],
                "verdict": "rejected_by_frozen_eta_convention_and_vectorlike_reality_gate",
                "precision_note": (
                    "The value 5/24 uses eta=-1/4 only. For eta=+1/4 the "
                    "same expression is -1/24. Neither branch gives 1/3."
                ),
            },
            "G2_rank_24_minus_one": {
                "majorana_rank_after_gravity_quotient": conformal[
                    "majorana_direct_sum_gate"
                ]["Majorana_rank_after_gravity_gauge_quotient"],
                "gauge_image_has_majorana_component": conformal[
                    "majorana_direct_sum_gate"
                ]["gauge_image_has_Majorana_component"],
                "verdict": "rejected",
            },
            "G3_SU5_orbifold_projection": {
                "proposed_matrix_determinant": -1,
                "proposed_matrix_is_SU5": False,
                "corrected_projection_passes_representation_direction": aps[
                    "orbifold_gate"
                ]["passes_representation_direction"],
                "projected_beta_direction": projection["zero_mode_content"]
                ["beta_vector_Y_2_3"],
                "threshold_magnitude_closed": aps["orbifold_gate"]
                ["passes_threshold_magnitude"],
                "verdict": "partial_representation_pass_only",
            },
            "G4_five_dimensional_CS": {
                "proposed_integrand_degrees": aps["exact_checks"]
                ["form_degree"]["proposed_integrand_degrees"],
                "is_five_form": aps["exact_checks"]["form_degree"]
                ["is_five_form"],
                "dimensionally_defined": aps["inflow_gate"]["passes"],
                "verdict": "rejected_dimensionally",
            },
            "G5_six_channel_inverse_susceptibility": {
                "identity_matches": six_channel["gaussian_average_model"]
                ["matches_one_over_pi4"],
                "ordinary_trace_variance": six_channel[
                    "gaussian_average_model"
                ]["qbar_variance"],
                "normalized_trace_variance": six_channel[
                    "trace_normalization_gate"
                ]["qbar_variance"],
                "two_sector_parent_action_passes": six_channel[
                    "unified_parent_action_gate"
                ]["passes_two_sector_requirement"],
                "verdict": "exact_lemma_without_physical_closure",
            },
            "G6_minimal_BL_root": {
                "continuous_anomalies_cancel": bl_extension[
                    "continuous_anomaly_gate_passes"
                ],
                "sterile_root_phase": bl_extension["root_holonomy"]
                ["sterile_generator_phase"],
                "majorana_vertex_charge_sum": bl_extension["root_holonomy"]
                ["Majorana_vertex_charge_sum"],
                "kinetic_mixing_trace": bl_extension["abelian_mixing"]
                ["trace_Y_times_B_minus_L_per_generation"]["fraction"],
                "homogeneous_condensate_closed": trilemma[
                    "logical_no_go"
                ]["simultaneously_possible_with_scalar_Yukawa"]
                is False,
                "verdict": "representation_and_root_pass_nonuniform_branch_only",
                "precision_note": (
                    "Kinetic mixing is a future normalization-sensitive second "
                    "gate, not a second sector already passed."
                ),
            },
            "G7_nonuniform_GL_saddle": {
                "threshold": nonuniform["analytic_saddle"]
                ["condensation_condition"],
                "unit_RP3_critical_value": nonuniform["analytic_saddle"]
                ["critical_v_squared"],
                "degenerate_windings": nonuniform["geometry"]
                ["degenerate_minimum_windings"],
                "equal_energy": nonuniform[
                    "explicit_stable_control_x_equals_2"
                ]["equal_energy"],
                "orientation_selected": not stiffness["orientation_no_go"]
                ["all_even_invariants_equal"],
                "verdict": "exact_reduced_saddle_lemma_without_action_closure",
            },
            "G8_torsion_orientation_selector": {
                "rho": rho,
                "beta": beta,
                "conjugate_errors": conjugate_errors,
                "exact_evenness": max(conjugate_errors.values()) < 1e-15,
                "I1_half": half_shift,
                "I1_quarter": quarter_shift,
                "two_I1_quarter": twice_quarter,
                "half_to_two_quarter_ratio": half_shift / twice_quarter,
                "half_minus_two_quarter": half_shift - twice_quarter,
                "verdict": "rejected_exactly_for_the_declared_circle_determinant",
                "precision_note": (
                    "I_rho(beta)=I_rho(-beta) is the orientation pruner. "
                    "Comparing I_1(1/2) with 2 I_1(1/4) is a separate failed "
                    "arithmetic identity, not the proof of conjugate degeneracy."
                ),
            },
            "G9_two_loop_replacement": {
                "equation": "(alpha/pi)^2 X=alpha/3",
                "required_X": two_loop_required_x,
                "depends_on_train_alpha": True,
                "verdict": "rejected_as_circular_without_an_independent_operator",
                "precision_note": (
                    "The strict objection is not aesthetic unnaturalness: solving "
                    "for X imports the train anchor alpha into the coefficient."
                ),
            },
            "G10_projection_weight_12pi_over_7": {
                "candidate": projection_candidate,
                "required": projection_required,
                "absolute_deficit": projection_required
                - projection_candidate,
                "relative_deficit": (
                    projection_required - projection_candidate
                )
                / projection_required,
                "exact_identity": False,
                "verdict": "rejected_as_a_nonexact_post_hoc_candidate",
            },
        },
        "additional_claim_gate": {
            "axis_difference_shift_identically_zero": {
                "registered_as_new_result": False,
                "reason": (
                    "No operator formula for this shift was supplied in the batch. "
                    "The existing residual-axis audit proves one symmetry orbit and "
                    "the relative-orbit audit leaves a free two-family angle; neither "
                    "statement alone is an identically zero axis-shift theorem."
                ),
            }
        },
        "summary": {
            "closed_physical_predictions_added": 0,
            "exact_or_conditional_lemmas_retained": [
                "six-channel ordinary-trace variance pi^-4",
                "anomaly-free B-L representation and sterile root phase",
                "nonuniform GL threshold and conjugate degeneracy",
                "corrected Z2/Z4 representation projection direction",
            ],
            "new_precision_pruners": [
                "circle determinant is exactly even under beta to minus beta",
                "two-loop coefficient X is circular if solved from the train alpha",
                "12*pi/7 misses the required projection weight by about 0.318 percent",
            ],
            "program_status": (
                "The batch narrows the search but does not change N_closed_physical=0. "
                "The next admissible step remains a prior parent action rather than "
                "another target-designed operator insertion."
            ),
        },
        "crosschecks": {
            "finite_threshold_cone_status": threshold["status"],
            "existing_eta_gate_status": eta_gate["status"],
        },
    }

    assert eta_arithmetic["-1/4"]["value"] == "5/24"
    assert eta_arithmetic["1/4"]["value"] == "-1/24"
    assert -0.5 not in eta_menu
    assert results["hypotheses"]["G2_rank_24_minus_one"][
        "majorana_rank_after_gravity_quotient"
    ] == 24
    projected_direction = results["hypotheses"][
        "G3_SU5_orbifold_projection"
    ]["projected_beta_direction"]
    assert max(
        abs(actual - expected)
        for actual, expected in zip(projected_direction, [17 / 6, 1 / 6, 2])
    ) < 1e-15
    assert results["hypotheses"]["G5_six_channel_inverse_susceptibility"][
        "identity_matches"
    ] is True
    assert results["hypotheses"]["G6_minimal_BL_root"][
        "continuous_anomalies_cancel"
    ] is True
    assert max(conjugate_errors.values()) < 1e-15
    assert abs(half_shift - 0.007469779610066302) < 1e-15
    assert abs(twice_quarter - 0.007483728979491194) < 1e-15
    assert abs(two_loop_required_x - 450.83036686166565) < 1e-10
    assert results["summary"]["closed_physical_predictions_added"] == 0

    Path("s2t_hypothesis_batch_pruner_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()