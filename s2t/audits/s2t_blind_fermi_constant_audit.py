import json
import math
from pathlib import Path


PDG_SOURCE = "PDG 2024 Physical Constants, rpp2024-rev-phys-constants.pdf"
GF_EXPERIMENT_GEV_MINUS_2 = 1.1663788e-5
GF_EXPERIMENT_SIGMA_GEV_MINUS_2 = 0.0000006e-5
MW_EXPERIMENT_GEV = 80.3692
MZ_EXPERIMENT_GEV = 91.1880
MW_S2T_ONE_LOOP_GEV = 79.923
MZ_S2T_ONE_LOOP_GEV = 90.332


tome2_results = json.loads(Path("s2t_tome2_results.json").read_text())
v_s2t = tome2_results["closed_rows"]["v_S2T_GeV"]

gf_prediction = 1.0 / (math.sqrt(2.0) * v_s2t**2)
gf_absolute_difference = gf_prediction - GF_EXPERIMENT_GEV_MINUS_2
gf_relative_difference = gf_absolute_difference / GF_EXPERIMENT_GEV_MINUS_2
gf_experimental_pull = (
    gf_absolute_difference / GF_EXPERIMENT_SIGMA_GEV_MINUS_2
)

v_from_experiment = math.sqrt(
    1.0 / (math.sqrt(2.0) * GF_EXPERIMENT_GEV_MINUS_2)
)
required_gf_matching_factor = GF_EXPERIMENT_GEV_MINUS_2 / gf_prediction
required_v_scale_factor = v_from_experiment / v_s2t

mw_after_universal_v_matching = MW_S2T_ONE_LOOP_GEV * required_v_scale_factor
mz_after_universal_v_matching = MZ_S2T_ONE_LOOP_GEV * required_v_scale_factor

results = {
    "status": "tree_level_fermi_constant_blind_prediction_fails_precision_matching_gate_open",
    "date": "2026-08-04",
    "frozen_prediction": {
        "input_result_file": "s2t_tome2_results.json",
        "v_S2T_GeV": v_s2t,
        "relation": "G_F=1/(sqrt(2) v_S2T^2)",
        "G_F_prediction_GeV_minus_2": gf_prediction,
        "target_not_used_in_construction": True,
    },
    "experimental_comparison": {
        "source": PDG_SOURCE,
        "G_F_experiment_GeV_minus_2": GF_EXPERIMENT_GEV_MINUS_2,
        "G_F_experiment_sigma_GeV_minus_2": GF_EXPERIMENT_SIGMA_GEV_MINUS_2,
        "absolute_difference_GeV_minus_2": gf_absolute_difference,
        "relative_difference": gf_relative_difference,
        "difference_ppm": 1.0e6 * gf_relative_difference,
        "experimental_sigma_pull_if_theory_matching_is_zero": gf_experimental_pull,
        "v_from_G_F_GeV": v_from_experiment,
        "v_difference_GeV": v_s2t - v_from_experiment,
        "v_relative_difference": (v_s2t - v_from_experiment) / v_from_experiment,
    },
    "required_matching": {
        "multiplicative_G_F_factor": required_gf_matching_factor,
        "fractional_G_F_correction": required_gf_matching_factor - 1.0,
        "multiplicative_v_factor": required_v_scale_factor,
        "fractional_v_correction": required_v_scale_factor - 1.0,
        "interpretation": (
            "A finite electroweak matching correction of this fixed size must be derived before "
            "v_S2T can be identified with the measured charged-current weak scale."
        ),
    },
    "single_scale_stress_test": {
        "rule": "rescale all masses proportional to v by the factor fixed from G_F",
        "M_W_before_GeV": MW_S2T_ONE_LOOP_GEV,
        "M_W_after_GeV": mw_after_universal_v_matching,
        "M_W_experiment_GeV": MW_EXPERIMENT_GEV,
        "M_W_relative_difference_after": (
            mw_after_universal_v_matching - MW_EXPERIMENT_GEV
        )
        / MW_EXPERIMENT_GEV,
        "M_Z_before_GeV": MZ_S2T_ONE_LOOP_GEV,
        "M_Z_after_GeV": mz_after_universal_v_matching,
        "M_Z_experiment_GeV": MZ_EXPERIMENT_GEV,
        "M_Z_relative_difference_after": (
            mz_after_universal_v_matching - MZ_EXPERIMENT_GEV
        )
        / MZ_EXPERIMENT_GEV,
        "verdict": (
            "The universal scale correction fixed by G_F does not simultaneously close the existing "
            "one-loop W and Z mass residuals. Additional independently derived gauge/threshold "
            "matching is required."
        ),
    },
    "scientific_verdict": {
        "tree_level_standard_EFT_identification": "fails_at_0.184_percent",
        "full_model_status": (
            "not a final no-go because electroweak matching and renormalization scheme are not yet derived"
        ),
        "admissible_rescue": (
            "derive the correction from the frozen particle/KK/defect spectrum and test G_F, M_W, "
            "M_Z and sin^2(theta_W) together"
        ),
        "inadmissible_rescue": "fit one finite factor to G_F and count it as a prediction",
    },
}

assert gf_relative_difference > 0.001
assert gf_relative_difference < 0.003
assert abs(required_gf_matching_factor - 1.0) > 1.0e-3
assert abs(results["single_scale_stress_test"]["M_W_relative_difference_after"]) > 0.004
assert abs(results["single_scale_stress_test"]["M_Z_relative_difference_after"]) > 0.008

Path("s2t_blind_fermi_constant_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "G_F_prediction": gf_prediction,
            "G_F_experiment": GF_EXPERIMENT_GEV_MINUS_2,
            "relative_difference": gf_relative_difference,
            "required_G_F_matching": required_gf_matching_factor - 1.0,
            "M_W_relative_difference_after_scale_fix": results[
                "single_scale_stress_test"
            ]["M_W_relative_difference_after"],
            "M_Z_relative_difference_after_scale_fix": results[
                "single_scale_stress_test"
            ]["M_Z_relative_difference_after"],
        },
        indent=2,
        ensure_ascii=False,
    )
)