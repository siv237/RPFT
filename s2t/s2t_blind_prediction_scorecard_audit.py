import json
import math
from pathlib import Path


PDG_2024 = "S. Navas et al. (Particle Data Group), Phys. Rev. D 110, 030001 (2024)"


tome2 = json.loads(Path("s2t_tome2_results.json").read_text())
closed = tome2["closed_rows"]
fermi = json.loads(Path("s2t_blind_fermi_constant_results.json").read_text())

predictions = {
    "m_tau_MeV": closed["m_tau_MeV"],
    "G_F_GeV_minus_2": fermi["frozen_prediction"]["G_F_prediction_GeV_minus_2"],
    "M_H_GeV": closed["M_H_GeV"],
    "lambda_H": closed["lambda_H_S2T"],
    "sin2_thetaW_tree_at_MZ": 0.217181,
    "alpha_s_MZ": 0.086898,
    "M_W_GeV": 79.923,
    "M_Z_GeV": 90.332,
    "delta_m2_21_eV2": 7.35648e-5,
    "delta_m2_32_eV2": 2.49051e-3,
}

controls = {
    "m_tau_MeV": {
        "value": 1776.93,
        "sigma": 0.09,
        "source": "PDG 2024 tau listing",
    },
    "G_F_GeV_minus_2": {
        "value": 1.1663788e-5,
        "sigma": 6.0e-12,
        "source": "PDG 2024 electroweak review",
    },
    "M_H_GeV": {
        "value": 125.20,
        "sigma": 0.11,
        "source": "PDG 2024 Higgs listing",
    },
    "alpha_s_MZ": {
        "value": 0.1180,
        "sigma": 0.0009,
        "source": "PDG 2024 QCD review",
    },
    "M_W_GeV": {
        "value": 80.3692,
        "sigma": 0.0133,
        "source": "PDG 2024 non-CDF-II average",
    },
    "M_Z_GeV": {
        "value": 91.1880,
        "sigma": 0.0020,
        "source": "PDG 2024 world average",
    },
    "delta_m2_21_eV2": {
        "value": 7.41e-5,
        "sigma": 0.205e-5,
        "source": "PDG 2024 neutrino global analysis, normal ordering",
    },
    "delta_m2_32_eV2": {
        "value": 2.437e-3,
        "sigma": 0.0275e-3,
        "source": "PDG 2024 neutrino global analysis, normal ordering",
    },
}

mw_control = controls["M_W_GeV"]
mz_control = controls["M_Z_GeV"]
sin2_on_shell = 1.0 - (mw_control["value"] / mz_control["value"]) ** 2
sin2_on_shell_sigma = math.sqrt(
    (
        -2.0
        * mw_control["value"]
        / mz_control["value"] ** 2
        * mw_control["sigma"]
    )
    ** 2
    + (
        2.0
        * mw_control["value"] ** 2
        / mz_control["value"] ** 3
        * mz_control["sigma"]
    )
    ** 2
)
controls["sin2_thetaW_tree_at_MZ"] = {
    "value": sin2_on_shell,
    "sigma": sin2_on_shell_sigma,
    "source": "derived on-shell proxy from the frozen PDG M_W and M_Z controls",
}

v_fermi = fermi["experimental_comparison"]["v_from_G_F_GeV"]
lambda_proxy = controls["M_H_GeV"]["value"] ** 2 / (2.0 * v_fermi**2)
lambda_proxy_sigma = (
    lambda_proxy * 2.0 * controls["M_H_GeV"]["sigma"] / controls["M_H_GeV"]["value"]
)
controls["lambda_H"] = {
    "value": lambda_proxy,
    "sigma": lambda_proxy_sigma,
    "source": "tree-level proxy M_H^2/(2 v_F^2) from PDG M_H and G_F",
}

status_metadata = {
    "m_tau_MeV": ("strong_conditional_tau_relation", "medium"),
    "G_F_GeV_minus_2": ("blind_matching_gate", "high"),
    "M_H_GeV": ("conditional_Higgs_bridge_inherits_tau_and_Svac", "medium"),
    "lambda_H": ("derived_tree_level_proxy", "medium"),
    "sin2_thetaW_tree_at_MZ": ("open_one_loop_no_threshold", "high"),
    "alpha_s_MZ": ("open_one_loop_no_threshold", "high"),
    "M_W_GeV": ("open_one_loop_no_threshold", "high"),
    "M_Z_GeV": ("open_one_loop_no_threshold", "high"),
    "delta_m2_21_eV2": ("conditional_neutrino_model", "low"),
    "delta_m2_32_eV2": ("conditional_neutrino_model", "low"),
}


def diagnostic_class(pull):
    absolute_pull = abs(pull)
    if absolute_pull < 2.0:
        return "close"
    if absolute_pull < 5.0:
        return "tension"
    return "fails_zero_theory_uncertainty_test"


rows = []
for observable, prediction in predictions.items():
    control = controls[observable]
    difference = prediction - control["value"]
    relative_difference = difference / control["value"]
    pull = difference / control["sigma"]
    model_status, evidence_weight = status_metadata[observable]
    rows.append(
        {
            "observable": observable,
            "prediction": prediction,
            "control": control["value"],
            "control_sigma": control["sigma"],
            "relative_difference": relative_difference,
            "experimental_pull_if_theory_uncertainty_is_zero": pull,
            "diagnostic_class": diagnostic_class(pull),
            "model_status": model_status,
            "evidence_weight": evidence_weight,
            "control_source": control["source"],
        }
    )

rows_by_name = {row["observable"]: row for row in rows}

v_scale_factor = fermi["required_matching"]["multiplicative_v_factor"]
mw_after_v_fix = predictions["M_W_GeV"] * v_scale_factor
mz_after_v_fix = predictions["M_Z_GeV"] * v_scale_factor
g2_required_factor = controls["M_W_GeV"]["value"] / mw_after_v_fix
gz_required_factor = controls["M_Z_GeV"]["value"] / mz_after_v_fix
g3_required_factor = math.sqrt(
    controls["alpha_s_MZ"]["value"] / predictions["alpha_s_MZ"]
)

results = {
    "status": "blind_scorecard_reveals_close_lepton_scalar_rows_and_failed_gauge_running_sector",
    "date": "2026-08-04",
    "control_policy": {
        "prediction_freeze": (
            "all S2T values were already present in Tome II or generated before loading controls"
        ),
        "control_reference": PDG_2024,
        "pull_warning": (
            "pulls use experimental uncertainties only and diagnose zero-matching predictions; "
            "they are not a complete theory chi-square"
        ),
    },
    "rows": rows,
    "sector_summary": {
        "close_rows": [
            row["observable"]
            for row in rows
            if row["diagnostic_class"] == "close"
        ],
        "failed_rows": [
            row["observable"]
            for row in rows
            if row["diagnostic_class"] == "fails_zero_theory_uncertainty_test"
        ],
        "lepton_scalar_pattern": (
            "m_tau, M_H, the tree-level lambda proxy and both conditional neutrino splittings "
            "lie within two experimental sigmas"
        ),
        "gauge_pattern": (
            "G_F, the weak angle proxy, M_W, M_Z and alpha_s fail together, identifying the "
            "low-energy gauge matching/RG sector rather than the scalar quartic as the dominant gap"
        ),
    },
    "missing_sector_diagnostics": {
        "v_matching_factor": v_scale_factor,
        "g2_factor_after_v_is_fixed": g2_required_factor,
        "gZ_factor_after_v_is_fixed": gz_required_factor,
        "g3_factor_from_alpha_s": g3_required_factor,
        "interpretation": [
            "The weak-scale mismatch is not one-dimensional: fixing v still requires distinct corrections to g2 and sqrt(g2^2+gY^2).",
            "The strong coupling requires about a 16.5 percent increase in g3, too large to describe as the same small scale renormalization that fixes G_F.",
            "The promising scalar relation is lambda_H: its S2T value differs from the M_H/G_F tree proxy by only about 4.6e-4 relatively.",
            "The next model ingredient should be a derived gauge/KK threshold spectrum with representation-dependent corrections, not another universal scalar factor.",
        ],
    },
    "scientific_verdict": (
        "The scorecard is not empty and not uniformly successful. It contains a coherent close cluster "
        "in the charged-lepton/scalar sector, while every genuinely gauge-running observable misses "
        "in the same direction or by a large amount. This localizes the main defect to the mapping "
        "from high-scale spectral normalizations to low-energy gauge couplings. Conditional neutrino "
        "agreement is encouraging but has low evidential weight until its action is fixed independently."
    ),
}

assert rows_by_name["m_tau_MeV"]["diagnostic_class"] == "close"
assert rows_by_name["M_H_GeV"]["diagnostic_class"] == "close"
assert rows_by_name["lambda_H"]["diagnostic_class"] == "close"
assert rows_by_name["alpha_s_MZ"]["diagnostic_class"] == "fails_zero_theory_uncertainty_test"
assert g3_required_factor > 1.16

Path("s2t_blind_prediction_scorecard_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "close_rows": results["sector_summary"]["close_rows"],
            "failed_rows": results["sector_summary"]["failed_rows"],
            "g2_required_factor": g2_required_factor,
            "gZ_required_factor": gz_required_factor,
            "g3_required_factor": g3_required_factor,
        },
        indent=2,
        ensure_ascii=False,
    )
)