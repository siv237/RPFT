import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, root


PI = math.pi
LOOP = 16.0 * PI**2
ALPHA_EM_INVERSE = 137.035999177
T_EW = 29.919805079547
S_SPLIT = PI**2 + 1.0 / (2.0 * PI)
V_S2T = json.loads(Path("s2t_blind_fermi_constant_results.json").read_text())[
    "frozen_prediction"
]["v_S2T_GeV"]
SCORECARD = json.loads(Path("s2t_blind_prediction_scorecard_results.json").read_text())
ROWS = {row["observable"]: row for row in SCORECARD["rows"]}


def representation_data():
    fields_weyl = [
        ("Q", 3, 2, 3, Fraction(1, 6), Fraction(3, 4), Fraction(4, 3), Fraction(1, 2), Fraction(1, 2)),
        ("U", 3, 1, 3, Fraction(2, 3), 0, Fraction(4, 3), 0, Fraction(1, 2)),
        ("D", 3, 1, 3, Fraction(1, 3), 0, Fraction(4, 3), 0, Fraction(1, 2)),
        ("L", 3, 2, 1, Fraction(1, 2), Fraction(3, 4), 0, Fraction(1, 2), 0),
        ("E", 3, 1, 1, Fraction(1, 1), 0, 0, 0, 0),
    ]
    fields_scalar = [
        ("H", 1, 2, 1, Fraction(1, 2), Fraction(3, 4), 0, Fraction(1, 2), 0)
    ]
    split_weyl = [
        ("U_vectorlike", 2, 1, 3, Fraction(2, 3), 0, Fraction(4, 3), 0, Fraction(1, 2)),
        ("two_D_vectorlike", 4, 1, 3, Fraction(1, 3), 0, Fraction(4, 3), 0, Fraction(1, 2)),
    ]
    split_scalar = [
        ("H_extra", 1, 2, 1, Fraction(1, 2), Fraction(3, 4), 0, Fraction(1, 2), 0)
    ]
    return fields_weyl, fields_scalar, split_weyl, split_scalar


def invariants(field):
    _, multiplicity, dimension_2, dimension_3, hypercharge, casimir_2, casimir_3, index_2, index_3 = field
    casimirs = [hypercharge**2, casimir_2, casimir_3]
    indices = [
        hypercharge**2 * dimension_2 * dimension_3,
        index_2 * dimension_3,
        index_3 * dimension_2,
    ]
    return multiplicity, casimirs, indices


def beta_coefficients(weyl_fields, scalar_fields, include_gauge_term=True):
    gauge_casimirs = [Fraction(0), Fraction(2), Fraction(3)]
    one_loop = [
        -Fraction(11, 3) * gauge_casimir if include_gauge_term else Fraction(0)
        for gauge_casimir in gauge_casimirs
    ]
    two_loop = [
        [
            -Fraction(34, 3) * gauge_casimirs[i] ** 2
            if include_gauge_term and i == j
            else Fraction(0)
            for j in range(3)
        ]
        for i in range(3)
    ]

    for field in weyl_fields:
        multiplicity, casimirs, indices = invariants(field)
        for i in range(3):
            one_loop[i] += Fraction(2, 3) * multiplicity * indices[i]
            for j in range(3):
                if i == j:
                    two_loop[i][j] += multiplicity * (
                        2 * casimirs[i]
                        + Fraction(10, 3) * gauge_casimirs[i]
                    ) * indices[i]
                else:
                    two_loop[i][j] += (
                        2 * multiplicity * indices[i] * casimirs[j]
                    )

    for field in scalar_fields:
        multiplicity, casimirs, indices = invariants(field)
        for i in range(3):
            one_loop[i] += Fraction(1, 3) * multiplicity * indices[i]
            for j in range(3):
                if i == j:
                    two_loop[i][j] += multiplicity * (
                        4 * casimirs[i]
                        + Fraction(2, 3) * gauge_casimirs[i]
                    ) * indices[i]
                else:
                    two_loop[i][j] += (
                        4 * multiplicity * indices[i] * casimirs[j]
                    )
    return one_loop, two_loop


def fraction_matrix_to_float(matrix):
    return np.array([[float(value) for value in row] for row in matrix])


def gauge_beta(couplings, one_loop, two_loop, top_yukawa=None):
    couplings = np.asarray(couplings)
    derivative = couplings**3 / LOOP * one_loop
    derivative += couplings**3 / LOOP**2 * (two_loop @ couplings**2)
    if top_yukawa is not None:
        derivative -= (
            couplings**3
            / LOOP**2
            * np.array([17.0 / 6.0, 3.0 / 2.0, 2.0])
            * top_yukawa**2
        )
    return derivative


def integrate_gauge(high_g2, low_order, high_order, high_matrix, low_matrix):
    high = np.array([math.sqrt(3.0 / 5.0) * high_g2, high_g2, high_g2])
    middle = solve_ivp(
        lambda _, values: gauge_beta(values, high_order, high_matrix),
        (0.0, -S_SPLIT),
        high,
        rtol=1e-11,
        atol=1e-13,
    ).y[:, -1]
    return solve_ivp(
        lambda _, values: gauge_beta(values, low_order, low_matrix),
        (-S_SPLIT, -T_EW),
        middle,
        rtol=1e-11,
        atol=1e-13,
    ).y[:, -1]


def alpha_em_inverse(couplings):
    return 4.0 * PI * (1.0 / couplings[0] ** 2 + 1.0 / couplings[1] ** 2)


def solve_alpha_anchored(low_order, high_order, high_matrix, low_matrix):
    high_g2 = brentq(
        lambda value: alpha_em_inverse(
            integrate_gauge(value, low_order, high_order, high_matrix, low_matrix)
        )
        - ALPHA_EM_INVERSE,
        0.3,
        0.9,
        xtol=1e-14,
    )
    return high_g2, integrate_gauge(
        high_g2, low_order, high_order, high_matrix, low_matrix
    )


def integrate_with_top(high_g2, high_top, low_top_target, low_order, high_order, high_matrix, low_matrix):
    initial = np.array(
        [math.sqrt(3.0 / 5.0) * high_g2, high_g2, high_g2, high_top]
    )

    def right_hand_side(_, values, one_loop, two_loop):
        couplings = values[:3]
        top_yukawa = values[3]
        gauge = gauge_beta(couplings, one_loop, two_loop, top_yukawa)
        top = top_yukawa / LOOP * (
            4.5 * top_yukawa**2
            - 17.0 / 12.0 * couplings[0] ** 2
            - 9.0 / 4.0 * couplings[1] ** 2
            - 8.0 * couplings[2] ** 2
        )
        return np.concatenate([gauge, [top]])

    middle = solve_ivp(
        lambda scale, values: right_hand_side(
            scale, values, high_order, high_matrix
        ),
        (0.0, -S_SPLIT),
        initial,
        rtol=2e-10,
        atol=1e-12,
    ).y[:, -1]
    low = solve_ivp(
        lambda scale, values: right_hand_side(
            scale, values, low_order, low_matrix
        ),
        (-S_SPLIT, -T_EW),
        middle,
        rtol=2e-10,
        atol=1e-12,
    ).y[:, -1]
    return low


def solve_top_bracket(target, low_order, high_order, high_matrix, low_matrix):
    solution = root(
        lambda values: [
            alpha_em_inverse(
                integrate_with_top(
                    values[0],
                    values[1],
                    target,
                    low_order,
                    high_order,
                    high_matrix,
                    low_matrix,
                )[:3]
            )
            - ALPHA_EM_INVERSE,
            integrate_with_top(
                values[0],
                values[1],
                target,
                low_order,
                high_order,
                high_matrix,
                low_matrix,
            )[3]
            - target,
        ],
        np.array([0.54, 0.55]),
    )
    low = integrate_with_top(
        solution.x[0],
        solution.x[1],
        target,
        low_order,
        high_order,
        high_matrix,
        low_matrix,
    )
    return solution, low


def observable_block(couplings):
    hypercharge, weak, strong = couplings
    m_w = 0.5 * weak * V_S2T
    m_z = 0.5 * math.sqrt(hypercharge**2 + weak**2) * V_S2T
    sin_squared = hypercharge**2 / (hypercharge**2 + weak**2)
    alpha_s = strong**2 / (4.0 * PI)
    controls = {
        "M_W_GeV": ROWS["M_W_GeV"]["control"],
        "M_Z_GeV": ROWS["M_Z_GeV"]["control"],
        "sin2_thetaW_on_shell_proxy": ROWS["sin2_thetaW_tree_at_MZ"]["control"],
        "alpha_s_MZ": ROWS["alpha_s_MZ"]["control"],
        "alpha_em_inverse": ALPHA_EM_INVERSE,
    }
    predictions = {
        "M_W_GeV": m_w,
        "M_Z_GeV": m_z,
        "sin2_thetaW_on_shell_proxy": sin_squared,
        "alpha_s_MZ": alpha_s,
        "alpha_em_inverse": alpha_em_inverse(couplings),
    }
    return {
        "couplings_gY_g2_g3": couplings.tolist(),
        "inverse_couplings_alphaY_alpha2_alpha3": (
            4.0 * PI / couplings**2
        ).tolist(),
        "predictions": predictions,
        "relative_residuals": {
            key: predictions[key] / controls[key] - 1.0 for key in predictions
        },
    }


def main():
    sm_weyl, sm_scalar, split_weyl, split_scalar = representation_data()
    sm_b_fraction, sm_B_fraction = beta_coefficients(sm_weyl, sm_scalar)
    split_b_fraction, split_B_fraction = beta_coefficients(
        split_weyl, split_scalar, include_gauge_term=False
    )
    sm_b = np.array([float(value) for value in sm_b_fraction])
    sm_B = fraction_matrix_to_float(sm_B_fraction)
    split_b = np.array([float(value) for value in split_b_fraction])
    split_B = fraction_matrix_to_float(split_B_fraction)
    zero_matrix = np.zeros((3, 3))

    no_threshold_one_high, no_threshold_one = solve_alpha_anchored(
        sm_b, sm_b, zero_matrix, zero_matrix
    )
    split_one_high, split_one = solve_alpha_anchored(
        sm_b, sm_b + split_b, zero_matrix, zero_matrix
    )
    no_threshold_two_high, no_threshold_two = solve_alpha_anchored(
        sm_b, sm_b, sm_B, sm_B
    )
    split_two_high, split_two = solve_alpha_anchored(
        sm_b, sm_b + split_b, sm_B + split_B, sm_B
    )

    frozen_uv_split_two = integrate_gauge(
        no_threshold_two_high, sm_b, sm_b + split_b, sm_B + split_B, sm_B
    )

    top_sensitivity = {}
    for target in [0.94, 1.00]:
        solution, low = solve_top_bracket(
            target, sm_b, sm_b + split_b, sm_B + split_B, sm_B
        )
        top_sensitivity[str(target)] = {
            "solver_success": bool(solution.success),
            "high_scale_g2": float(solution.x[0]),
            "high_scale_top_yukawa": float(solution.x[1]),
            "low_scale_top_yukawa": float(low[3]),
            **observable_block(low[:3]),
        }

    legacy = json.loads(
        Path("s2t_geometric_split_mass_action_results.json").read_text()
    )["minimal_action_fully_blind_v_S2T"]
    legacy_inverse = np.array(legacy["inverse_couplings_after_Y_2_3"])
    no_threshold_inverse = np.array(
        [107.27238393453474, 29.761393438727513, 1.0 / 0.086898]
    )

    results = {
        "status": "two_loop_stress_test_closes_intermediate_running_route_negative_sign_and_anchor_failure",
        "date": "2026-08-04",
        "conventions": {
            "normalization": "gY, g2, g3 with sin2_thetaW(Lambda)=3/8 and g3(Lambda)=g2(Lambda)",
            "train_anchor": "alpha_em_inverse(MZ)=137.035999177",
            "total_log_interval": T_EW,
            "split_log_interval": S_SPLIT,
            "split_scale_GeV": json.loads(
                Path("s2t_geometric_split_mass_action_results.json").read_text()
            )["minimal_action_fully_blind_v_S2T"]["split_scale_GeV"],
            "two_loop_scope": "MS-like gauge two-loop beta functions; split fields have no declared Yukawa couplings",
        },
        "beta_coefficients": {
            "SM_one_loop": [str(value) for value in sm_b_fraction],
            "SM_two_loop": [[str(value) for value in row] for row in sm_B_fraction],
            "split_one_loop_increment": [
                str(value) for value in split_b_fraction
            ],
            "split_two_loop_increment": [
                [str(value) for value in row] for row in split_B_fraction
            ],
            "SM_matrix_reproduction": "exactly reproduces [[199/18,9/2,44/3],[3/2,35/6,12],[11/6,9/2,-26]]",
        },
        "alpha_anchored_results": {
            "one_loop_no_threshold": {
                "high_scale_g2": no_threshold_one_high,
                **observable_block(no_threshold_one),
            },
            "one_loop_with_split": {
                "high_scale_g2": split_one_high,
                **observable_block(split_one),
            },
            "two_loop_no_threshold_gauge_only": {
                "high_scale_g2": no_threshold_two_high,
                **observable_block(no_threshold_two),
            },
            "two_loop_with_split_gauge_only": {
                "high_scale_g2": split_two_high,
                **observable_block(split_two),
            },
        },
        "top_yukawa_sensitivity_not_blind": top_sensitivity,
        "frozen_uv_normalization_test": {
            "policy": "calibrate the UV coupling in the two-loop no-threshold theory, then add the split sector without recalibration",
            **observable_block(frozen_uv_split_two),
        },
        "legacy_shortcut_audit": {
            "legacy_rule": "alpha_inverse_after=alpha_inverse_before-(S_split/2pi) Delta b",
            "correct_one_loop_running_sign": "alpha_inverse_low=alpha_inverse_high+(b/2pi) log(Lambda/low)",
            "legacy_inverse_shift": (legacy_inverse - no_threshold_inverse).tolist(),
            "expected_split_running_shift_sign": "positive for every positive component of Delta b",
            "legacy_alpha_em_inverse": float(legacy_inverse[0] + legacy_inverse[1]),
            "train_alpha_em_inverse": ALPHA_EM_INVERSE,
            "relative_anchor_violation": float(
                (legacy_inverse[0] + legacy_inverse[1]) / ALPHA_EM_INVERSE - 1.0
            ),
            "verdict": "the apparent four-row improvement used the opposite RG sign and changed the alpha_em train anchor",
        },
        "scientific_verdict": {
            "primary": "the U+2D+H intermediate-running repair fails before finite matching: correct-sign matter running moves inverse couplings in the opposite direction from the reconstructed residual",
            "two_loop": "with alpha_em preserved, the gauge-only two-loop split result gives approximately MW=82.02 GeV, MZ=92.06 GeV, sin2=0.2062 and alpha_s=0.08018",
            "yukawa_sensitivity": "varying y_t(MZ) from 0.94 to 1.00 changes alpha_s only at the 1e-5 level and cannot rescue the result",
            "theory_effect": "retain the anomaly-free projection and geometric saddle as mathematical constructions, but remove the claim that ordinary intermediate running repairs the gauge scorecard",
            "next_gate": "only a finite threshold with the required negative sign or a different high-scale normalization derived independently of alpha_em can reopen the gauge branch",
        },
    }

    expected_sm_B = [
        [Fraction(199, 18), Fraction(9, 2), Fraction(44, 3)],
        [Fraction(3, 2), Fraction(35, 6), Fraction(12)],
        [Fraction(11, 6), Fraction(9, 2), Fraction(-26)],
    ]
    expected_split_b = [Fraction(17, 6), Fraction(1, 6), Fraction(2)]
    assert sm_B_fraction == expected_sm_B
    assert split_b_fraction == expected_split_b
    assert np.all(
        np.array(results["legacy_shortcut_audit"]["legacy_inverse_shift"]) < 0.0
    )
    assert results["legacy_shortcut_audit"]["relative_anchor_violation"] < -0.03
    anchored = results["alpha_anchored_results"]["two_loop_with_split_gauge_only"]
    assert abs(anchored["relative_residuals"]["alpha_em_inverse"]) < 1e-10
    assert anchored["relative_residuals"]["alpha_s_MZ"] < -0.30
    assert anchored["relative_residuals"]["sin2_thetaW_on_shell_proxy"] < -0.07
    assert all(row["solver_success"] for row in top_sensitivity.values())

    Path("s2t_two_loop_split_stress_test_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "two_loop_split_predictions": anchored["predictions"],
                "two_loop_split_relative_residuals": anchored[
                    "relative_residuals"
                ],
                "legacy_alpha_anchor_violation": results[
                    "legacy_shortcut_audit"
                ]["relative_anchor_violation"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()