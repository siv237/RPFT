#!/usr/bin/env python3
import json
from pathlib import Path


def relative_error(prediction, reference):
    return (prediction - reference) / reference


def quantitative_row(observable, prediction, reference, status, source, note):
    return {
        "observable": observable,
        "prediction": prediction,
        "reference": reference,
        "relative_error": relative_error(prediction, reference),
        "absolute_relative_error": abs(relative_error(prediction, reference)),
        "status": status,
        "source": source,
        "note": note,
    }


def main():
    tome = Path("tome2_s2t_spectral_closure.tex").read_text(encoding="utf-8")
    tome2 = json.loads(Path("s2t_tome2_results.json").read_text(encoding="utf-8"))
    ew = json.loads(
        Path("s2t_two_loop_split_stress_test_results.json").read_text(
            encoding="utf-8"
        )
    )
    ckm = json.loads(
        Path("s2t_two_layer_physical_ckm_redteam_results.json").read_text(
            encoding="utf-8"
        )
    )
    neutrino = json.loads(
        Path("s2t_neutrino_majorana_dimension_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    atlas = json.loads(
        Path("s2t_collective_pi_atlas_base_results.json").read_text(
            encoding="utf-8"
        )
    )

    alpha_prediction = tome2["closed_rows"]["S_vac"]
    alpha_reference = tome2["reference_checks"]["alpha_inv_reference"]
    tau_prediction = tome2["closed_rows"]["m_tau_MeV"]
    tau_reference = tome2["reference_checks"]["m_tau_reference_MeV"]
    split = ew["alpha_anchored_results"]["two_loop_with_split_gauge_only"]
    split_predictions = split["predictions"]
    split_residuals = split["relative_residuals"]
    split_references = {
        key: split_predictions[key] / (1.0 + split_residuals[key])
        for key in [
            "M_W_GeV",
            "M_Z_GeV",
            "sin2_thetaW_on_shell_proxy",
            "alpha_s_MZ",
        ]
    }
    ckm_prediction = ckm["blind_stage"]["prediction"]
    ckm_control = ckm["post_blind_PDG_2024_control"]
    neutrino_prediction = neutrino["prediction_scenarios"][0]["R_nu"]
    neutrino_reference = neutrino["phenomenology_diagnostic"][
        "nufit6_ratio_benchmark"
    ]

    quantitative = [
        quantitative_row(
            "alpha_em_inverse",
            alpha_prediction,
            alpha_reference,
            "numerically_extreme_but_train_anchor_and_operator_closure_failed",
            "s2t_tome2_results.json",
            "The numerical equality is not an independent blind prediction; the exact pi^-4 determinant route is closed negative.",
        ),
        quantitative_row(
            "tau_mass_MeV",
            tau_prediction,
            tau_reference,
            "strong_conditional_relation",
            "s2t_tome2_results.json",
            "The seed rho_0 and the RP3 projection normalization remain unproved.",
        ),
        quantitative_row(
            "Fermi_constant_GeV_minus2",
            1.1685251e-5,
            1.1663788e-5,
            "precision_failure_and_matching_open",
            "tome2 blind table",
            "The relative mismatch is about 1.84e-3 and the weak-scale identification needs finite matching.",
        ),
        quantitative_row(
            "W_mass_GeV",
            split_predictions["M_W_GeV"],
            split_references["M_W_GeV"],
            "minimal_EW_QCD_branch_failed",
            "s2t_two_loop_split_stress_test_results.json",
            "Alpha-anchored two-loop split running overshoots the control by about 2.06 percent.",
        ),
        quantitative_row(
            "Z_mass_GeV",
            split_predictions["M_Z_GeV"],
            split_references["M_Z_GeV"],
            "minimal_EW_QCD_branch_failed",
            "s2t_two_loop_split_stress_test_results.json",
            "Alpha-anchored two-loop split running overshoots the control by about 0.96 percent.",
        ),
        quantitative_row(
            "sin2_thetaW_on_shell_proxy",
            split_predictions["sin2_thetaW_on_shell_proxy"],
            split_references["sin2_thetaW_on_shell_proxy"],
            "minimal_EW_QCD_branch_failed",
            "s2t_two_loop_split_stress_test_results.json",
            "The weak-angle proxy is low by about 7.62 percent.",
        ),
        quantitative_row(
            "alpha_s_MZ",
            split_predictions["alpha_s_MZ"],
            split_references["alpha_s_MZ"],
            "minimal_EW_QCD_branch_failed",
            "s2t_two_loop_split_stress_test_results.json",
            "The strong coupling is low by about 32.05 percent.",
        ),
        quantitative_row(
            "CKM_Jarlskog",
            ckm_prediction["Jarlskog"],
            ckm_control["Jarlskog"],
            "blind_texture_failed",
            "s2t_two_layer_physical_ckm_redteam_results.json",
            "The symmetric texture predicts nonhierarchical mixing and a Jarlskog invariant over three orders of magnitude too large.",
        ),
        quantitative_row(
            "CKM_sin_theta13",
            ckm_prediction["sin_theta_13"],
            ckm_control["sin_theta_13"],
            "blind_texture_failed",
            "s2t_two_layer_physical_ckm_redteam_results.json",
            "The smallest observed quark-mixing angle is predicted as an order-one angle.",
        ),
        quantitative_row(
            "neutrino_mass_splitting_ratio",
            neutrino_prediction,
            neutrino_reference,
            "numerically_close_but_dimension_selector_failed",
            "s2t_neutrino_majorana_dimension_gate_results.json",
            "The ratio is close, but the integer 23 is not representation-consistently derived and the absolute scale is not closed.",
        ),
        quantitative_row(
            "Higgs_mass_GeV",
            125.056486039,
            125.20,
            "numerically_close_but_conditional_scale_bridge",
            "tome2 Higgs EFT block; 2026 control rounded to 125.20 GeV",
            "The mass inherits the conditional tau and S_vac chain and is not independent of the unclosed absolute scale.",
        ),
    ]

    coverage = [
        {
            "domain": "electromagnetic_low_energy",
            "established_world_content": "massless U(1) gauge field, QED charges, running and scattering amplitudes",
            "model_status": "partial_numeric_compression_only",
            "missing": "a closed Maxwell-ghost determinant and a derived low-energy QED action with matter charges",
        },
        {
            "domain": "charged_lepton_spectrum",
            "established_world_content": "electron, muon and tau with distinct masses and weak couplings",
            "model_status": "one_conditional_tau_to_mu_relation",
            "missing": "a common Yukawa or mass operator deriving all three masses rather than using the muon scale as input",
        },
        {
            "domain": "quark_mass_spectrum",
            "established_world_content": "six quark flavours with hierarchical running masses",
            "model_status": "retrospective_atlas_contains_four_quark_mass_ratios_but_no_mass_operator",
            "missing": "selected up- and down-type Yukawa blocks and their renormalization-scale dependence",
        },
        {
            "domain": "CKM_mixing_and_CP",
            "established_world_content": "hierarchical nontrivial quark mixing and CP violation",
            "model_status": "retrospective_atlas_contains_Vcb_but_candidate_full_texture_fails",
            "missing": "a selector fixing the two Yukawa blocks and reproducing four CKM parameters",
        },
        {
            "domain": "neutrino_oscillations",
            "established_world_content": "two nonzero mass splittings and large three-flavour mixing",
            "model_status": "conditional_ratio_without_PMNS_or_absolute_scale",
            "missing": "a valid rank selector, absolute Dirac/Majorana scale, ordering and the PMNS matrix",
        },
        {
            "domain": "electroweak_precision",
            "established_world_content": "W and Z masses, Fermi constant and weak mixing angle",
            "model_status": "minimal_running_and_threshold_routes_failed",
            "missing": "parameter-free finite matching jointly closing G_F, M_W, M_Z and sin2 theta_W",
        },
        {
            "domain": "strong_interaction",
            "established_world_content": "QCD running, confinement, jets and a hadron spectrum",
            "model_status": "retrospective_atlas_matches_alpha_s_but_running_branch_fails_and_hadron_dynamics_are_absent",
            "missing": "correct running plus confinement and quantitative meson/baryon observables",
        },
        {
            "domain": "Higgs_sector",
            "established_world_content": "a scalar resonance near 125 GeV with measured couplings and width",
            "model_status": "conditional_mass_bridge",
            "missing": "independent absolute scale, finite matching, decay widths and coupling modifiers",
        },
        {
            "domain": "complete_standard_model_representation",
            "established_world_content": "chiral gauge representations with anomaly cancellation",
            "model_status": "partial_SU5_like_kinematic_construction",
            "missing": "one parent action reducing to the complete observed low-energy field content and interactions",
        },
        {
            "domain": "dynamical_spacetime_and_gravity",
            "established_world_content": "universal gravitational dynamics and propagating spacetime perturbations",
            "model_status": "not_in_tome2_closure",
            "missing": "Einstein or alternative field equations, Newton normalization and a controlled graviton sector",
        },
        {
            "domain": "cosmic_expansion",
            "established_world_content": "an expanding universe with a measured thermal and expansion history",
            "model_status": "retrospective_atlas_contains_three_density_fractions_but_no_cosmological_dynamics",
            "missing": "background cosmological equations and parameter predictions",
        },
        {
            "domain": "missing_mass_phenomenology",
            "established_world_content": "gravitational evidence for nonluminous matter beyond visible baryons",
            "model_status": "retrospective_atlas_contains_Omega_dm_but_no_dark_sector_or_structure_formation",
            "missing": "a stable sector or modified dynamics reproducing abundance and structure formation",
        },
        {
            "domain": "accelerated_expansion",
            "established_world_content": "late-time accelerated cosmic expansion",
            "model_status": "retrospective_atlas_contains_Omega_Lambda_but_no_acceleration_mechanism",
            "missing": "a vacuum-energy or dynamical-dark-energy prediction compatible with cosmology",
        },
        {
            "domain": "matter_antimatter_asymmetry",
            "established_world_content": "a baryon-dominated observable universe",
            "model_status": "not_derived",
            "missing": "a baryogenesis mechanism with quantified CP violation and out-of-equilibrium dynamics",
        },
        {
            "domain": "quantum_consistency",
            "established_world_content": "unitary, causal and precision-tested quantum amplitudes over a wide energy range",
            "model_status": "sectorwise_EFT_fragments_only",
            "missing": "a common Hilbert space, measure, BRST/BV completion, renormalization prescription and unitarity checks",
        },
    ]

    markers = {
        "new_predictions_absent": "новые физические предсказания отсутствуют",
        "unified_action_absent": "единое действие пока не построено",
        "CKM_selector_absent": "не создаёт selector",
        "EW_QCD_negative": "EW/QCD & отрицательно для минимальной ветви",
    }
    marker_counts = {name: tome.count(marker) for name, marker in markers.items()}

    attempted_precision_failures = [
        row
        for row in quantitative
        if row["status"]
        in {
            "precision_failure_and_matching_open",
            "minimal_EW_QCD_branch_failed",
            "blind_texture_failed",
        }
    ]
    unresolved_or_missing_domains = [
        row for row in coverage if row["model_status"] not in {"closed", "derived"}
    ]

    results = {
        "status": "observed_world_coverage_gate_failed_no_closed_independent_multisector_description",
        "date": "2026-08-06",
        "scope": {
            "question": "What established content of our world is absent, underived, or quantitatively inaccurate in the current S2T model?",
            "policy": "An input, postdiction, or numerically close conditional formula is not counted as a closed prediction.",
            "external_control": "Particle Data Group 2026 is the current reference framework; numerical rows reuse the frozen controls already declared by the project unless explicitly noted.",
        },
        "quantitative_scorecard": quantitative,
        "atlas_crosscheck": {
            "status": atlas["status"],
            "claim_count": atlas["scope"]["claim_count"],
            "claims": [row["name"] for row in atlas["claims_at_pi"]],
            "pi_score": atlas["pi_score"],
            "best_grid_base": atlas["best_grid_base"],
            "best_grid_score": atlas["best_grid_score"],
            "pi_low_error_percentile": atlas["pi_low_error_percentile"],
            "interpretation": (
                "The atlas already gives retrospective common-base numerical coverage of alpha_s, "
                "sin2 theta_W, four quark mass ratios, tau/muon, V_cb and three cosmological fractions. "
                "These entries must not be described as absent. They remain conditional compression "
                "rather than derived physics because the observable-to-formula addressing rule, "
                "parent action, scale dependence and dynamics are not selected."
            ),
        },
        "coverage_ledger": coverage,
        "summary": {
            "quantitative_rows": len(quantitative),
            "attempted_precision_failures": len(attempted_precision_failures),
            "coverage_domains": len(coverage),
            "unresolved_or_missing_domains": len(unresolved_or_missing_domains),
            "closed_independent_multisector_predictions": 0,
            "largest_relative_error": max(
                quantitative, key=lambda row: row["absolute_relative_error"]
            ),
            "existing_global_status": tome2["status"]["global_physical_status"],
        },
        "marker_counts": marker_counts,
        "existing_machine_status": {
            "zero_closed_predictions": tome2["status"]["global_physical_status"]
            == "IIA_rejected_zero_closed_independent_empirical_predictions"
        },
        "priority_order": [
            "derive one parent action and readout map before adding more constants",
            "close the low-energy gauge sector against M_W, M_Z, sin2 theta_W and alpha_s without fitting",
            "derive finite-algebra constraints selecting quark and lepton Yukawa blocks",
            "produce the CKM and PMNS matrices plus full fermion mass spectra",
            "derive gravity and cosmological background dynamics",
            "only then count a preregistered new observable as evidence for world inevitability",
        ],
        "verdict": (
            "The current model captures nontrivial mathematical structure and several striking numerical relations, "
            "including an eleven-row retrospective pi-atlas, but it does not yet recover the minimum established "
            "content of our world as an operator-derived theory. Its sharpest independent "
            "low-energy branch fails electroweak and QCD precision, its CKM texture fails strongly, the neutrino "
            "and Higgs successes are conditional, and whole established sectors remain underived."
        ),
    }

    assert all(count > 0 for count in marker_counts.values())
    assert results["existing_machine_status"]["zero_closed_predictions"]
    assert results["summary"]["closed_independent_multisector_predictions"] == 0
    assert results["summary"]["attempted_precision_failures"] >= 7
    assert results["summary"]["unresolved_or_missing_domains"] == len(coverage)
    assert results["atlas_crosscheck"]["claim_count"] == 11
    assert {"V_cb", "Omega_Lambda", "Omega_dm", "Omega_b"}.issubset(
        results["atlas_crosscheck"]["claims"]
    )
    Path("s2t_observed_world_coverage_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()