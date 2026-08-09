import json
import math
from pathlib import Path

import numpy as np


scorecard = json.loads(Path("s2t_blind_prediction_scorecard_results.json").read_text())
cone = json.loads(Path("s2t_kk_representation_cone_results.json").read_text())
fermi = json.loads(Path("s2t_blind_fermi_constant_results.json").read_text())

rows = {row["observable"]: row for row in scorecard["rows"]}
required = np.array(
    cone["required_low_energy_threshold_vector"]["magnitudes_Y_2_3"]
)
split_beta = np.array([17.0 / 6.0, 1.0 / 6.0, 2.0])

alpha_inverse = 137.035999177
alpha = 1.0 / alpha_inverse
v_s2t = fermi["frozen_prediction"]["v_S2T_GeV"]
v_fermi = fermi["experimental_comparison"]["v_from_G_F_GeV"]

inverse_couplings_before = np.array(
    [
        107.27238393453474,
        29.761393438727513,
        1.0 / rows["alpha_s_MZ"]["prediction"],
    ]
)

volume_action = math.pi**2
half_cycle_action = 1.0 / (2.0 * math.pi)
minimal_action = volume_action + half_cycle_action
unsupported_qed_dressing = 0.5 * alpha * math.pi**2
dressed_action = minimal_action + unsupported_qed_dressing

reconstructed_action = 2.0 * math.pi * float(
    required @ split_beta / (split_beta @ split_beta)
)

t_ew = 29.919805079547
mz_control = rows["M_Z_GeV"]["control"]
lambda_s2t = mz_control * math.exp(t_ew)


def evaluate_action(action, electroweak_vev):
    amplitude = action / (2.0 * math.pi)
    inverse_after = inverse_couplings_before - amplitude * split_beta
    g_y, g_2, g_3 = [
        math.sqrt(4.0 * math.pi / value) for value in inverse_after
    ]
    m_w = 0.5 * g_2 * electroweak_vev
    m_z = 0.5 * math.sqrt(g_2**2 + g_y**2) * electroweak_vev
    sin2 = g_y**2 / (g_2**2 + g_y**2)
    alpha_s = g_3**2 / (4.0 * math.pi)
    values = {
        "M_W_GeV": m_w,
        "M_Z_GeV": m_z,
        "sin2_thetaW_on_shell_proxy": sin2,
        "alpha_s_MZ": alpha_s,
    }
    controls = {
        "M_W_GeV": rows["M_W_GeV"]["control"],
        "M_Z_GeV": rows["M_Z_GeV"]["control"],
        "sin2_thetaW_on_shell_proxy": rows[
            "sin2_thetaW_tree_at_MZ"
        ]["control"],
        "alpha_s_MZ": rows["alpha_s_MZ"]["control"],
    }
    sigmas = {
        "M_W_GeV": rows["M_W_GeV"]["control_sigma"],
        "M_Z_GeV": rows["M_Z_GeV"]["control_sigma"],
        "sin2_thetaW_on_shell_proxy": rows[
            "sin2_thetaW_tree_at_MZ"
        ]["control_sigma"],
        "alpha_s_MZ": rows["alpha_s_MZ"]["control_sigma"],
    }
    comparisons = {
        key: {
            "prediction": value,
            "control": controls[key],
            "relative_difference": (value - controls[key]) / controls[key],
            "experimental_pull_if_theory_uncertainty_is_zero": (
                value - controls[key]
            )
            / sigmas[key],
        }
        for key, value in values.items()
    }
    return {
        "action": action,
        "running_amplitude_action_over_2pi": amplitude,
        "inverse_couplings_after_Y_2_3": inverse_after.tolist(),
        "couplings_after_gY_g2_g3": [g_y, g_2, g_3],
        "split_scale_GeV": lambda_s2t * math.exp(-action),
        "comparisons": comparisons,
    }


minimal_blind = evaluate_action(minimal_action, v_s2t)
minimal_fermi_matched = evaluate_action(minimal_action, v_fermi)
dressed_blind = evaluate_action(dressed_action, v_s2t)

baseline_relative_errors = {
    "M_W_GeV": abs(rows["M_W_GeV"]["relative_difference"]),
    "M_Z_GeV": abs(rows["M_Z_GeV"]["relative_difference"]),
    "sin2_thetaW_on_shell_proxy": abs(
        rows["sin2_thetaW_tree_at_MZ"]["relative_difference"]
    ),
    "alpha_s_MZ": abs(rows["alpha_s_MZ"]["relative_difference"]),
}
improvement_factors = {
    key: baseline_relative_errors[key]
    / abs(minimal_blind["comparisons"][key]["relative_difference"])
    for key in baseline_relative_errors
}

results = {
    "status": "minimal_geometric_split_action_improves_all_gauge_rows_precision_closure_still_fails",
    "date": "2026-08-04",
    "epistemic_status": {
        "classification": "post_scorecard_zero_parameter_hypothesis",
        "warning": (
            "the action form was proposed after the required split exponent was known; numerical success is exploratory, not blind evidence"
        ),
    },
    "action_candidates": {
        "volume_only": volume_action,
        "half_cycle_term": half_cycle_action,
        "minimal_preexisting_invariants": {
            "formula": "S_split=Vol(RP3)+(1/2)||e1||^2=pi^2+1/(2pi)",
            "value": minimal_action,
            "difference_from_reconstructed_action": minimal_action
            - reconstructed_action,
            "split_scale_relative_error": math.exp(
                reconstructed_action - minimal_action
            )
            - 1.0,
        },
        "qed_dressed_candidate_rejected_as_underived": {
            "formula": "pi^2+1/(2pi)+alpha*pi^2/2",
            "extra_term": unsupported_qed_dressing,
            "value": dressed_action,
            "reason": (
                "the alpha/2 dressing coefficient was not fixed by an existing S2T action before this comparison"
            ),
        },
        "reconstructed_required_action": reconstructed_action,
    },
    "minimal_action_fully_blind_v_S2T": minimal_blind,
    "minimal_action_conditional_v_from_G_F": minimal_fermi_matched,
    "rejected_dressed_control_v_S2T": dressed_blind,
    "improvement_over_no_threshold_absolute_relative_error": improvement_factors,
    "diagnosis": {
        "positive": (
            "the minimal action improves M_W, M_Z, the weak-angle proxy and alpha_s simultaneously with no fitted continuous coefficient"
        ),
        "remaining_precision": (
            "using v_S2T, relative residuals are about -0.108 percent, -0.119 percent, -0.078 percent and +1.91 percent respectively"
        ),
        "dominant_remaining_gap": (
            "QCD is still high by about 1.9 percent, while M_Z remains many experimental sigmas away despite a small relative error"
        ),
        "next_gate": (
            "derive S_split from an explicit defect or tunneling action and compute two-loop plus finite electroweak matching before any further coefficient is added"
        ),
    },
    "verdict": (
        "The independently available geometric combination pi^2+1/(2pi) lands within 3.63 percent in the split mass scale and improves every gauge observable by factors between about 5 and 35 relative to the no-threshold scorecard. This is the strongest constructive lead in the gauge sector. It is not confirmation because the combination was proposed after the residual scale was known and its interpretation as a vectorlike mass action is not derived. The alpha-dressed variant matches the reconstructed exponent strikingly well but is rejected from the evidence ledger because its coefficient is underived."
    ),
}

assert minimal_action < reconstructed_action
assert abs(results["action_candidates"]["minimal_preexisting_invariants"]["split_scale_relative_error"]) < 0.04
assert all(value > 5.0 for value in improvement_factors.values())
assert minimal_blind["comparisons"]["alpha_s_MZ"]["relative_difference"] > 0.019

Path("s2t_geometric_split_mass_action_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "minimal_action": minimal_action,
            "reconstructed_action": reconstructed_action,
            "minimal_split_scale_GeV": minimal_blind["split_scale_GeV"],
            "blind_relative_residuals": {
                key: row["relative_difference"]
                for key, row in minimal_blind["comparisons"].items()
            },
            "improvement_factors": improvement_factors,
        },
        indent=2,
        ensure_ascii=False,
    )
)