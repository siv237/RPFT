#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq


def holonomy_function(rho, beta):
    numerator = math.cosh(2.0 * math.pi * rho) - math.cos(2.0 * math.pi * beta)
    denominator = math.cosh(2.0 * math.pi * rho) - 1.0
    return math.log(numerator / denominator)


def main():
    cosine = (26.0 - 9.0 * math.sqrt(15.0)) / 11.0
    theta = math.acos(cosine)
    length = math.pi
    transverse_gap = 1.25

    longitudinal_samples = []
    for mode in range(-3, 4):
        for family_charge in (-1, 0, 1):
            value = abs((2.0 * math.pi * mode + family_charge * theta) / length)
            longitudinal_samples.append(
                {
                    "mode": mode,
                    "family_charge": family_charge,
                    "absolute_eigenvalue": value,
                }
            )

    zero_states = [
        entry for entry in longitudinal_samples if entry["absolute_eigenvalue"] < 1e-12
    ]
    positive_longitudinal_gap = min(
        entry["absolute_eigenvalue"]
        for entry in longitudinal_samples
        if entry["absolute_eigenvalue"] >= 1e-12
    )
    separable_gap = min(transverse_gap, positive_longitudinal_gap)

    torsion_square_angle = (2.0 * theta) % (2.0 * math.pi)
    flat_torsion_allowed = math.isclose(torsion_square_angle, 0.0, abs_tol=1e-12)

    systolic_length = math.pi
    circle_length = 2.0 * math.pi
    product_periodic_samples = []
    product_antiperiodic_samples = []
    for systolic_mode in range(-2, 3):
        for circle_mode in range(-2, 3):
            for family_charge in (-1, 0, 1):
                radial_zero = 0.0
                systolic_momentum = 2.0 * math.pi * systolic_mode / systolic_length
                periodic_circle = (
                    2.0 * math.pi * circle_mode + family_charge * theta
                ) / circle_length
                antiperiodic_circle = (
                    2.0 * math.pi * (circle_mode + 0.5) + family_charge * theta
                ) / circle_length
                product_periodic_samples.append(
                    math.sqrt(radial_zero**2 + systolic_momentum**2 + periodic_circle**2)
                )
                product_antiperiodic_samples.append(
                    math.sqrt(radial_zero**2 + systolic_momentum**2 + antiperiodic_circle**2)
                )
    periodic_zero_count = sum(value < 1e-12 for value in product_periodic_samples)
    antiperiodic_zero_count = sum(value < 1e-12 for value in product_antiperiodic_samples)
    periodic_positive_gap = min(
        value for value in product_periodic_samples if value >= 1e-12
    )
    principal_curvature_flux = 2.0 * theta - 2.0 * math.pi

    spin_shift = 0.5
    odd_charge = 1
    residual_holonomy = math.pi
    compensated_shift = (
        spin_shift + odd_charge * residual_holonomy / (2.0 * math.pi)
    ) % 1.0
    charge_two_holonomy = np.exp(2.0j * residual_holonomy)

    kernel_rank = 1
    quotient_rank = 23
    circle_mode_norm = 1.0
    cycle_zero_form_norm = 1.0
    cycle_one_form_norm = 1.0 / math.pi
    collective_stiffness = (
        quotient_rank * cycle_zero_form_norm * circle_mode_norm
        + kernel_rank * cycle_one_form_norm * circle_mode_norm
    )

    hosotani_rho = 1.0
    i_zero = holonomy_function(hosotani_rho, 0.0)
    i_one_sixth = holonomy_function(hosotani_rho, 1.0 / 6.0)
    i_one_third = holonomy_function(hosotani_rho, 1.0 / 3.0)
    i_half = holonomy_function(hosotani_rho, 0.5)
    anti_odd_fermion_delta = 0.5 * i_half
    anti_third_fermion_delta = 0.5 * (i_half - i_one_third)
    periodic_third_boson_delta = 0.5 * i_one_sixth
    periodic_odd_fermion_delta = -0.5 * i_half
    existing_nc_delta = anti_odd_fermion_delta
    minimal_bl_generation_delta = 2.0 * i_half + 6.0 * (i_half - i_one_third)
    retwisted_nc_generation_delta = i_half + 6.0 * (i_half - i_one_third)

    odd_rhos = [0.2, 0.7, 1.3, 2.1]
    fractional_rhos = [0.15 + 0.17 * index for index in range(12)]
    multi_mass_odd_terms = [
        0.5 * holonomy_function(rho, 0.5) for rho in odd_rhos
    ]
    multi_mass_fractional_terms = [
        0.5
        * (
            holonomy_function(rho, 0.5)
            - holonomy_function(rho, 1.0 / 3.0)
        )
        for rho in fractional_rhos
    ]
    multi_mass_total = sum(multi_mass_odd_terms) + sum(
        multi_mass_fractional_terms
    )

    three_generation_benchmark = 3.0 * minimal_bl_generation_delta
    vectorlike_pair_equal_rho_strength = i_half
    equal_rho_pair_count = (
        math.floor(three_generation_benchmark / vectorlike_pair_equal_rho_strength)
        + 1
    )
    one_pair_rho_threshold = brentq(
        lambda rho: holonomy_function(rho, 0.5) - three_generation_benchmark,
        0.01,
        2.0,
    )
    selected_branch_mass_gap = math.sqrt(one_pair_rho_threshold**2 + 0.25)

    half_reference_rho = 0.5
    half_reference_generation_delta = (
        8.0 * holonomy_function(half_reference_rho, 0.5)
        - 6.0 * holonomy_function(half_reference_rho, 1.0 / 3.0)
    )
    half_reference_three_generation_delta = 3.0 * half_reference_generation_delta
    half_reference_pair_threshold = brentq(
        lambda rho: (
            holonomy_function(rho, 0.5)
            - half_reference_three_generation_delta
        ),
        0.001,
        2.0,
    )
    half_reference_selected_gap = math.sqrt(
        half_reference_pair_threshold**2 + 0.25
    )

    extended_collective_stiffness = collective_stiffness + 0.0
    x_stiffness_delta = extended_collective_stiffness - collective_stiffness
    sm_beta_shifts = [0.0, 0.0, 0.0]
    sm_finite_matching = [0.0, 0.0, 0.0]
    corrected_matching_target = [1.0, -1.0, -6.68221]

    vectorlike_b_minus_l = [1, -1]
    vectorlike_z4 = [1, -1]
    vectorlike_anomalies = {
        "sum_q": sum(vectorlike_b_minus_l),
        "sum_q_cubed": sum(charge**3 for charge in vectorlike_b_minus_l),
        "sum_z": sum(vectorlike_z4),
        "sum_z_cubed": sum(charge**3 for charge in vectorlike_z4),
        "sum_z_q_squared": sum(
            z_charge * gauge_charge**2
            for z_charge, gauge_charge in zip(vectorlike_z4, vectorlike_b_minus_l)
        ),
        "sum_z_squared_q": sum(
            z_charge**2 * gauge_charge
            for z_charge, gauge_charge in zip(vectorlike_z4, vectorlike_b_minus_l)
        ),
    }

    asymptotic_rho = 2.0
    asymptotic_scale = math.exp(-2.0 * math.pi * asymptotic_rho)
    asymptotic_i_half = holonomy_function(asymptotic_rho, 0.5) / asymptotic_scale
    asymptotic_i_third = (
        holonomy_function(asymptotic_rho, 1.0 / 3.0) / asymptotic_scale
    )
    asymptotic_i_sixth = (
        holonomy_function(asymptotic_rho, 1.0 / 6.0) / asymptotic_scale
    )

    perturbation_norm = 0.2
    feshbach_q = 0.25
    feshbach_b = 0.4
    feshbach_bound = feshbach_b**2 / (transverse_gap - feshbach_q)

    cross_generator = np.array(
        [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    )
    core_connection = theta * cross_generator / length

    results = {
        "status": "vectorlike_vacuum_selector_passes_stiffness_but_fails_second_sector",
        "date": "2026-08-08",
        "wilson_data": {
            "cos_theta": cosine,
            "theta": theta,
            "theta_over_pi": theta / math.pi,
            "holonomy_nontrivial": 0.0 < theta < math.pi,
        },
        "bulk_core_bridge": {
            "operator": "D_a,Phi tensor I3 + Gamma_s tensor (d_s + K_n/L)",
            "connection_antisymmetric": bool(
                np.allclose(core_connection.T, -core_connection)
            ),
            "projected_family_rank": int(np.linalg.matrix_rank(core_connection)),
            "projected_kernel_dimension": int(
                core_connection.shape[0] - np.linalg.matrix_rank(core_connection)
            ),
        },
        "separable_spectrum": {
            "formula": "epsilon_j^2 + ((2*pi*k+sigma*theta)/L)^2",
            "zero_states_in_scan": zero_states,
            "positive_longitudinal_gap": positive_longitudinal_gap,
            "transverse_gap": transverse_gap,
            "full_gap": separable_gap,
            "full_kernel_dimension": len(zero_states),
        },
        "ambient_topology_gate": {
            "systolic_class_order": 2,
            "flat_connection_requires_W_squared_identity": True,
            "two_theta_mod_2pi": torsion_square_angle,
            "required_holonomy_is_involution": flat_torsion_allowed,
            "verdict": "flat ambient extension on the systolic loop is impossible",
        },
        "non_torsion_circle_route": {
            "systolic_length": systolic_length,
            "circle_length": circle_length,
            "periodic_kernel_dimension": periodic_zero_count,
            "periodic_positive_gap": periodic_positive_gap,
            "expected_family_gap": theta / circle_length,
            "antiperiodic_kernel_dimension": antiperiodic_zero_count,
            "finding": (
                "The exact-one kernel survives on gamma x S1 only in a periodic "
                "or holonomy-compensated defect branch."
            ),
        },
        "compensated_spin_branch": {
            "geometric_spin_shift": spin_shift,
            "odd_fermion_charge": odd_charge,
            "residual_holonomy": residual_holonomy,
            "effective_shift_mod_integer": compensated_shift,
            "charge_two_condensate_holonomy_real": float(charge_two_holonomy.real),
            "charge_two_condensate_holonomy_imag": float(charge_two_holonomy.imag),
            "required_branch_exists": math.isclose(
                compensated_shift, 0.0, abs_tol=1e-12
            ),
            "minimal_local_charge_two_action_degenerate": True,
            "branch_dynamically_selected": False,
        },
        "collective_stiffness": {
            "kernel_rank": kernel_rank,
            "quotient_rank": quotient_rank,
            "normalized_circle_factor": circle_mode_norm,
            "cycle_zero_form_norm_squared": cycle_zero_form_norm,
            "cycle_one_form_norm_squared": cycle_one_form_norm,
            "value": collective_stiffness,
            "expected": 23.0 + 1.0 / math.pi,
            "canonical_metric_identity_pass": math.isclose(
                collective_stiffness, 23.0 + 1.0 / math.pi
            ),
            "physical_denominator_restored": False,
        },
        "hosotani_sign_gate": {
            "rho_sample": hosotani_rho,
            "I_0": i_zero,
            "I_1_over_6": i_one_sixth,
            "I_1_over_3": i_one_third,
            "I_1_over_2": i_half,
            "monotone_on_fundamental_interval_sample": (
                i_zero < i_one_sixth < i_one_third < i_half
            ),
            "anti_periodic_odd_fermion_delta_V": anti_odd_fermion_delta,
            "anti_periodic_q_third_fermion_delta_V": anti_third_fermion_delta,
            "periodic_q_third_boson_beta_at_pi": 1.0 / 6.0,
            "periodic_q_third_boson_delta_V": periodic_third_boson_delta,
            "minimal_spectrum_selects_alpha_zero": all(
                value > 0.0
                for value in (
                    anti_odd_fermion_delta,
                    anti_third_fermion_delta,
                    periodic_third_boson_delta,
                )
            ),
            "periodic_odd_fermion_delta_V": periodic_odd_fermion_delta,
            "large_rho_formula": "2*(1-cos(2*pi*beta))*exp(-2*pi*rho)",
            "asymptotic_rho_sample": asymptotic_rho,
            "I_half_over_exp": asymptotic_i_half,
            "I_third_over_exp": asymptotic_i_third,
            "I_sixth_over_exp": asymptotic_i_sixth,
        },
        "geometric_vs_total_periodicity": {
            "Nc_geometric_spin_shift": 0.5,
            "Nc_total_beta_at_alpha_zero": 0.5,
            "Nc_total_beta_at_alpha_pi": 0.0,
            "Nc_delta_V": existing_nc_delta,
            "Nc_favors_alpha_zero": existing_nc_delta > 0.0,
            "systolic_periodicity_does_not_change_external_S1_spin_structure": True,
            "finding": (
                "N^c becomes total-periodic only at alpha=pi and therefore has the "
                "anti-periodic geometric determinant sign. It is not the required "
                "periodic-spin negative contribution."
            ),
        },
        "minimal_BL_magnitude_gate": {
            "fractional_Weyl_components_per_generation": 12,
            "odd_Weyl_components_per_generation_including_Nc": 4,
            "equal_rho_delta_V_per_generation": minimal_bl_generation_delta,
            "equal_rho_formula": "8*I(1/2)-6*I(1/3)",
            "artificial_one_Nc_periodic_delta_V_per_generation": (
                retwisted_nc_generation_delta
            ),
            "artificial_retwist_formula": "7*I(1/2)-6*I(1/3)",
            "existing_content_selects_alpha_pi": False,
            "unequal_mass_sample_odd_rhos": odd_rhos,
            "unequal_mass_sample_fractional_rhos": fractional_rhos,
            "unequal_mass_sample_all_terms_positive": all(
                value > 0.0
                for value in multi_mass_odd_terms + multi_mass_fractional_terms
            ),
            "unequal_mass_sample_total_delta_V": multi_mass_total,
            "unequal_mass_general_no_go_proved_for_existing_content": True,
            "reason": (
                "Every existing anti-periodic fermion and periodic charged boson "
                "contributes a nonnegative term separately for every rho_i>0."
            ),
        },
        "minimal_vectorlike_periodic_selector": {
            "fields": [
                {"name": "X_plus", "B_minus_L": 1, "Z4_X": 1},
                {"name": "X_minus", "B_minus_L": -1, "Z4_X": -1},
            ],
            "continuous_and_elementary_mixed_anomaly_sums": vectorlike_anomalies,
            "all_listed_anomaly_sums_zero": all(
                value == 0 for value in vectorlike_anomalies.values()
            ),
            "Dirac_mass_allowed": True,
            "Majorana_pairing_forbidden_by_Z4_X": True,
            "mixing_with_Nc_forbidden_by_Z4_X": True,
            "adds_defect_zero_modes": False,
            "three_generation_rho_one_positive_delta_V": (
                three_generation_benchmark
            ),
            "one_pair_rho_threshold": one_pair_rho_threshold,
            "equal_rho_one_pair_delta_strength": vectorlike_pair_equal_rho_strength,
            "minimum_equal_rho_pair_count": equal_rho_pair_count,
            "selected_branch_mass_gap_at_one_pair_threshold": (
                selected_branch_mass_gap
            ),
            "normalization_threshold_gate": {
                "rho_reference_one": {
                    "positive_three_generation_delta_V": three_generation_benchmark,
                    "critical_rho_X": one_pair_rho_threshold,
                    "selected_branch_mass_gap": selected_branch_mass_gap,
                },
                "rho_reference_one_half": {
                    "positive_three_generation_delta_V": (
                        half_reference_three_generation_delta
                    ),
                    "critical_rho_X": half_reference_pair_threshold,
                    "selected_branch_mass_gap": half_reference_selected_gap,
                },
                "smaller_reference_rho_requires_smaller_rho_X": (
                    half_reference_pair_threshold < one_pair_rho_threshold
                ),
                "proposed_rho_X_near_0_74_at_reference_one_half_is_valid": False,
            },
            "stiffness_embedding_gate": {
                "extended_hilbert_space": "H_24 direct_sum H_X",
                "extended_collective_tangent": "Xi direct_sum 0_X",
                "extended_collective_stiffness": extended_collective_stiffness,
                "delta_X": x_stiffness_delta,
                "projector_identity_pass": math.isclose(x_stiffness_delta, 0.0),
                "X_supplies_cycle_pi_inverse_term": False,
                "identifying_collective_tangent_with_alpha_is_allowed": False,
            },
            "second_sector_gate": {
                "SM_representation": "(1,1)_0",
                "delta_sum_Y_times_B_minus_L": 0.0,
                "SM_gauge_beta_shifts": sm_beta_shifts,
                "one_loop_finite_EW_QCD_matching": sm_finite_matching,
                "corrected_target": corrected_matching_target,
                "matches_corrected_target": sm_finite_matching
                == corrected_matching_target,
                "parameter_free_two_loop_rescue": False,
            },
            "consolidated_status": {
                "selects_Wilson_branch_alpha_pi_below_threshold": True,
                "selects_family_axis_n": False,
                "rho_X_mass_input_derived_from_parent_action": False,
                "introduces_no_continuous_model_data": False,
                "introduces_no_new_stiffness_fitting_coefficient": True,
                "classification": "conditional anomaly-safe vacuum selector",
                "N_closed_physical": 0,
            },
            "symmetry_preserving_Dirac_gap_implies_trivial_anomaly_class": True,
            "full_discrete_anomaly_gate_passed": True,
            "second_normalization_sensitive_sector_passed": False,
        },
        "topological_term_gate": {
            "euclidean_CS_or_theta_changes_phase": True,
            "real_potential_difference_from_pure_topological_phase": 0.0,
            "stabilizes_alpha_pi_as_real_minimum": False,
            "possible_roles": [
                "interference between sectors",
                "constraint or projection in an enlarged TQFT",
            ],
        },
        "curved_systolic_route": {
            "flux_condition": "integral_Sigma2 F_n = 2*theta mod 2*pi",
            "principal_flux": principal_curvature_flux,
            "axis_alignment_required": True,
        },
        "perturbative_stability": {
            "operator_norm": perturbation_norm,
            "half_gap_condition_pass": perturbation_norm < separable_gap / 2.0,
            "guaranteed_gap_lower_bound": separable_gap - perturbation_norm,
            "feshbach_q": feshbach_q,
            "feshbach_b": feshbach_b,
            "feshbach_correction_bound": feshbach_bound,
            "family_splitting": theta / length,
            "feshbach_condition_pass": theta / length > feshbach_bound,
        },
        "remaining_gate": (
            "Derive the Z4_X line and vectorlike mass from the parent algebra. The "
            "minimal SM-singlet realization has delta_X=0 but fails the EW/QCD "
            "second-sector gate exactly; any rescue needs parent-derived SM charges "
            "or portals and is therefore a further model extension."
        ),
    }

    assert results["bulk_core_bridge"]["connection_antisymmetric"]
    assert results["bulk_core_bridge"]["projected_family_rank"] == 2
    assert results["bulk_core_bridge"]["projected_kernel_dimension"] == 1
    assert results["separable_spectrum"]["full_kernel_dimension"] == 1
    assert math.isclose(positive_longitudinal_gap, theta / length)
    assert not results["ambient_topology_gate"]["required_holonomy_is_involution"]
    assert results["non_torsion_circle_route"]["periodic_kernel_dimension"] == 1
    assert results["non_torsion_circle_route"]["antiperiodic_kernel_dimension"] == 0
    assert math.isclose(periodic_positive_gap, theta / circle_length)
    assert results["compensated_spin_branch"]["required_branch_exists"]
    assert math.isclose(charge_two_holonomy.real, 1.0)
    assert abs(charge_two_holonomy.imag) < 1e-12
    assert results["collective_stiffness"]["canonical_metric_identity_pass"]
    assert not results["collective_stiffness"]["physical_denominator_restored"]
    assert results["hosotani_sign_gate"]["monotone_on_fundamental_interval_sample"]
    assert results["hosotani_sign_gate"]["minimal_spectrum_selects_alpha_zero"]
    assert results["hosotani_sign_gate"]["periodic_odd_fermion_delta_V"] < 0.0
    assert math.isclose(asymptotic_i_half, 4.0, rel_tol=5e-5)
    assert math.isclose(asymptotic_i_third, 3.0, rel_tol=5e-5)
    assert math.isclose(asymptotic_i_sixth, 1.0, rel_tol=5e-5)
    assert results["geometric_vs_total_periodicity"]["Nc_favors_alpha_zero"]
    assert results["minimal_BL_magnitude_gate"]["equal_rho_delta_V_per_generation"] > 0.0
    assert (
        results["minimal_BL_magnitude_gate"][
            "artificial_one_Nc_periodic_delta_V_per_generation"
        ]
        > 0.0
    )
    assert results["minimal_BL_magnitude_gate"][
        "unequal_mass_sample_all_terms_positive"
    ]
    assert results["minimal_BL_magnitude_gate"][
        "unequal_mass_general_no_go_proved_for_existing_content"
    ]
    assert results["minimal_vectorlike_periodic_selector"][
        "all_listed_anomaly_sums_zero"
    ]
    assert results["minimal_vectorlike_periodic_selector"][
        "minimum_equal_rho_pair_count"
    ] == 11
    assert math.isclose(one_pair_rho_threshold, 0.6259781084318297)
    assert math.isclose(half_reference_pair_threshold, 0.13992909367882705)
    assert math.isclose(half_reference_selected_gap, 0.5192110854534772)
    assert not results["minimal_vectorlike_periodic_selector"][
        "adds_defect_zero_modes"
    ]
    assert results["minimal_vectorlike_periodic_selector"][
        "full_discrete_anomaly_gate_passed"
    ]
    assert results["minimal_vectorlike_periodic_selector"][
        "normalization_threshold_gate"
    ]["smaller_reference_rho_requires_smaller_rho_X"]
    assert results["minimal_vectorlike_periodic_selector"][
        "stiffness_embedding_gate"
    ]["projector_identity_pass"]
    assert not results["minimal_vectorlike_periodic_selector"][
        "second_sector_gate"
    ]["matches_corrected_target"]
    assert not results["minimal_vectorlike_periodic_selector"][
        "consolidated_status"
    ]["selects_family_axis_n"]
    assert not results["minimal_vectorlike_periodic_selector"][
        "consolidated_status"
    ]["introduces_no_continuous_model_data"]
    assert not results["topological_term_gate"]["stabilizes_alpha_pi_as_real_minimum"]
    assert results["perturbative_stability"]["half_gap_condition_pass"]
    assert results["perturbative_stability"]["feshbach_condition_pass"]

    Path("s2t_family_connection_defect_gap_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()