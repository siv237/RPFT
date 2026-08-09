import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, lsq_linear


PI = math.pi
ALPHA_EM_INVERSE = 137.035999177
T_EW = 29.919805079547


def minimum_maximum_norm(matrix, target, nonnegative):
    column_count = matrix.shape[1]
    objective = np.concatenate([np.zeros(column_count), [1.0]])
    inequalities = []
    bounds = []
    for column in range(column_count):
        positive = np.zeros(column_count + 1)
        positive[column] = 1.0
        positive[-1] = -1.0
        inequalities.append(positive)
        if not nonnegative:
            negative = np.zeros(column_count + 1)
            negative[column] = -1.0
            negative[-1] = -1.0
            inequalities.append(negative)
    if nonnegative:
        bounds = [(0.0, None)] * column_count + [(0.0, None)]
    else:
        bounds = [(None, None)] * column_count + [(0.0, None)]
    return linprog(
        objective,
        A_ub=np.array(inequalities),
        b_ub=np.zeros(len(inequalities)),
        A_eq=np.column_stack([matrix, np.zeros(3)]),
        b_eq=target,
        bounds=bounds,
        method="highs",
    )


def main():
    two_loop = json.loads(
        Path("s2t_two_loop_split_stress_test_results.json").read_text()
    )
    scorecard = json.loads(
        Path("s2t_blind_prediction_scorecard_results.json").read_text()
    )
    fermi = json.loads(Path("s2t_blind_fermi_constant_results.json").read_text())
    rows = {row["observable"]: row for row in scorecard["rows"]}

    baseline_inverse = np.array(
        two_loop["alpha_anchored_results"][
            "two_loop_no_threshold_gauge_only"
        ]["inverse_couplings_alphaY_alpha2_alpha3"]
    )
    v_s2t = fermi["frozen_prediction"]["v_S2T_GeV"]
    target_g2 = 2.0 * rows["M_W_GeV"]["control"] / v_s2t
    target_alpha2_inverse = 4.0 * PI / target_g2**2
    target_alphaY_inverse = ALPHA_EM_INVERSE - target_alpha2_inverse
    target_alpha3_inverse = 1.0 / rows["alpha_s_MZ"]["control"]
    target_inverse = np.array(
        [target_alphaY_inverse, target_alpha2_inverse, target_alpha3_inverse]
    )
    required_shift = target_inverse - baseline_inverse

    target_gY = math.sqrt(4.0 * PI / target_alphaY_inverse)
    mz_implied_by_mw_alpha = (
        0.5 * math.sqrt(target_g2**2 + target_gY**2) * v_s2t
    )
    mz_control = rows["M_Z_GeV"]["control"]

    # Columns are x_J=-log(M_J/Lambda)>=0 for masses below the matching scale.
    # The ordering is XY, H3, Sigma8, Sigma3.
    below_scale_matrix = np.array(
        [
            [22.0, 2.0 / 5.0, 0.0, 0.0],
            [12.0, 0.0, 0.0, -1.0 / 3.0],
            [21.0, -1.0, -1.0 / 2.0, 0.0],
        ]
    ) / (12.0 * PI)
    original_log_matrix = -below_scale_matrix

    exact_below = minimum_maximum_norm(
        below_scale_matrix, required_shift, nonnegative=True
    )
    exact_unrestricted = minimum_maximum_norm(
        original_log_matrix, required_shift, nonnegative=False
    )

    physical_feasibility = linprog(
        np.zeros(4),
        A_eq=below_scale_matrix,
        b_eq=required_shift,
        bounds=[(0.0, T_EW)] * 4,
        method="highs",
    )
    best_physical = lsq_linear(
        below_scale_matrix,
        required_shift,
        bounds=(0.0, T_EW),
        tol=1e-14,
        lsmr_tol=1e-14,
        max_iter=10000,
    )

    exact_below_logs = exact_below.x[:4]
    exact_unrestricted_logs = exact_unrestricted.x[:4]
    best_physical_shift = below_scale_matrix @ best_physical.x
    best_physical_residual = best_physical_shift - required_shift

    lambda_s2t = rows["M_Z_GeV"]["control"] * math.exp(T_EW)
    exact_below_masses = lambda_s2t * np.exp(-exact_below_logs)

    result = {
        "status": "corrected_finite_threshold_cone_algebraically_feasible_physically_infeasible",
        "date": "2026-08-04",
        "target_construction": {
            "baseline": "alpha-anchored gauge-only two-loop SM without new thresholds",
            "baseline_inverse_couplings_Y_2_3": baseline_inverse.tolist(),
            "target_policy": "use measured M_W with frozen v_S2T, preserve alpha_em, and use measured alpha_s",
            "target_inverse_couplings_Y_2_3": target_inverse.tolist(),
            "required_finite_shift_Y_2_3": required_shift.tolist(),
            "normalized_direction_by_abs_SU2": (
                required_shift / abs(required_shift[1])
            ).tolist(),
            "MZ_implied_by_target_MW_alpha_GeV": mz_implied_by_mw_alpha,
            "MZ_control_GeV": mz_control,
            "MZ_relative_gap_not_fixable_by_gauge_couplings_alone": (
                mz_implied_by_mw_alpha / mz_control - 1.0
            ),
        },
        "threshold_basis": {
            "fields": ["XY", "H3", "Sigma8", "Sigma3"],
            "variables": "x_J=-log(M_J/Lambda)>=0 for M_J<=Lambda",
            "matrix_Y_2_3": below_scale_matrix.tolist(),
            "formula_source": "extended SU5-like finite matching block already declared in Tome II",
        },
        "unbounded_below_scale_cone": {
            "exactly_feasible": bool(exact_below.success),
            "minimum_possible_max_log": float(exact_below.fun),
            "logs_XY_H3_Sigma8_Sigma3": exact_below_logs.tolist(),
            "mass_ratios_to_Lambda": np.exp(-exact_below_logs).tolist(),
            "masses_GeV": exact_below_masses.tolist(),
            "reconstructed_shift": (
                below_scale_matrix @ exact_below_logs
            ).tolist(),
            "interpretation": "the algebraic cone works only by placing H3, Sigma3 and especially Sigma8 far below MZ",
        },
        "physical_window_MZ_to_Lambda": {
            "maximum_allowed_log": T_EW,
            "exactly_feasible": bool(physical_feasibility.success),
            "solver_message": physical_feasibility.message,
            "best_fit_logs_XY_H3_Sigma8_Sigma3": best_physical.x.tolist(),
            "best_fit_shift": best_physical_shift.tolist(),
            "residual": best_physical_residual.tolist(),
            "relative_L2_residual": float(
                np.linalg.norm(best_physical_residual)
                / np.linalg.norm(required_shift)
            ),
            "largest_component_residual_relative_to_target_max": float(
                np.max(np.abs(best_physical_residual))
                / np.max(np.abs(required_shift))
            ),
        },
        "masses_allowed_on_both_sides_of_Lambda": {
            "exactly_feasible": bool(exact_unrestricted.success),
            "minimum_possible_max_abs_log": float(exact_unrestricted.fun),
            "logs_log_M_over_Lambda_XY_H3_Sigma8_Sigma3": exact_unrestricted_logs.tolist(),
            "mass_ratios_to_Lambda": np.exp(exact_unrestricted_logs).tolist(),
            "comparison_to_available_log_interval": float(
                exact_unrestricted.fun / T_EW
            ),
        },
        "scientific_verdict": {
            "cone": "the sign cone is algebraically nonempty but physically empty when all threshold masses are required to lie between MZ and Lambda_S2T",
            "hierarchy": "the least extreme exact below-scale solution needs max log 116.05; even allowing masses above Lambda needs max abs log 56.30, versus the available interval 29.92",
            "best_physical": "saturating H3, Sigma8 and Sigma3 at MZ still leaves about 50.7 percent of the target vector unresolved in L2 norm",
            "additional_gap": "with frozen v_S2T and alpha_em, fitting M_W by gauge couplings alone predicts M_Z low by about 0.54 percent",
            "theory_effect": "the minimal XY/H3/Sigma8/Sigma3 finite-threshold basis is closed negatively as a simultaneous EW/QCD repair",
            "next_gate": "either derive genuinely nonlogarithmic finite matching with fixed coefficients or freeze the gauge branch and move effort to sectors with independent successes",
        },
    }

    assert exact_below.success
    assert exact_below.fun > 100.0
    assert not physical_feasibility.success
    assert result["physical_window_MZ_to_Lambda"]["relative_L2_residual"] > 0.5
    assert exact_unrestricted.fun > T_EW
    assert result["target_construction"][
        "MZ_relative_gap_not_fixable_by_gauge_couplings_alone"
    ] < -0.005

    Path("s2t_finite_threshold_sign_cone_results.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "required_shift": required_shift.tolist(),
                "minimum_below_scale_max_log": exact_below.fun,
                "physical_window_feasible": physical_feasibility.success,
                "best_physical_relative_residual": result[
                    "physical_window_MZ_to_Lambda"
                ]["relative_L2_residual"],
                "minimum_unrestricted_max_abs_log": exact_unrestricted.fun,
                "MZ_relative_gap": result["target_construction"][
                    "MZ_relative_gap_not_fixable_by_gauge_couplings_alone"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()