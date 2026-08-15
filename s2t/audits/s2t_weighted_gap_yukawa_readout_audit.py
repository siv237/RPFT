#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np

from s2t_two_layer_physical_ckm_redteam_audit import (
    phased_edge,
    standard_parameters,
)


def exp_pattern(eigenvalues, beta):
    ordered = np.sort(np.real(eigenvalues))
    weights = np.exp(-beta * (ordered - ordered[0]))
    return np.sort(weights / weights.max())


def hierarchy_score(prediction, target):
    return float(
        np.sqrt(np.mean(np.log(prediction[:-1] / target[:-1]) ** 2))
    )


def main():
    factor = json.loads(
        Path("s2t_family_factor_operator_results.json").read_text(
            encoding="utf-8"
        )
    )
    hierarchy = factor["hierarchy_comparison"]
    target_up = np.array(
        hierarchy["up_quarks_at_declared_scales"]["target"]
    )
    target_down = np.array(
        hierarchy["down_quarks_at_declared_scales"]["target"]
    )
    wilson = json.loads(
        Path("s2t_continuous_wilson_gap_action_results.json").read_text(
            encoding="utf-8"
        )
    )
    flux = math.acos(
        wilson["continuous_two_sector_solution"]["cos_theta_numeric"]
    )
    beta_menu = {"unit": 1.0, "RP3_length": math.pi, "S1_length": 2 * math.pi}

    structural = []
    for kernel in factor["factor_laplacian"]["kernel_tests"]:
        eigenvalues = np.sort(np.array(kernel["eigenvalues"]))
        levels = (eigenvalues - eigenvalues[0]) / (
            eigenvalues[-1] - eigenvalues[0]
        )
        gaps = np.diff(levels)
        base = np.diag(levels).astype(complex)
        for orientation in ["forward", "reverse"]:
            edge_10, edge_21 = (
                gaps if orientation == "forward" else gaps[::-1]
            )
            chord_weight = edge_10 * edge_21
            chain = (
                base
                + edge_10 * phased_edge((1, 0), 0.0)
                + edge_21 * phased_edge((2, 1), 0.0)
            )
            chord = base + chord_weight * phased_edge((2, 0), -flux)
            for assignment in ["chord_up", "chain_up"]:
                yukawa_up, yukawa_down = (
                    (chord, chain)
                    if assignment == "chord_up"
                    else (chain, chord)
                )
                mass_up, vectors_up = np.linalg.eigh(
                    yukawa_up @ yukawa_up.conjugate().T
                )
                mass_down, vectors_down = np.linalg.eigh(
                    yukawa_down @ yukawa_down.conjugate().T
                )
                mixing = (
                    vectors_up[:, ::-1].conjugate().T
                    @ vectors_down[:, ::-1]
                )
                structural.append(
                    {
                        "kernel": kernel["kernel"],
                        "levels": levels.tolist(),
                        "orientation": orientation,
                        "edge_10": float(edge_10),
                        "edge_21": float(edge_21),
                        "chord_weight": float(chord_weight),
                        "assignment": assignment,
                        "mass_squared_up": mass_up,
                        "mass_squared_down": mass_down,
                        "mixing": mixing,
                    }
                )

    rows = []
    for candidate in structural:
        for beta_up_name, beta_up in beta_menu.items():
            for beta_down_name, beta_down in beta_menu.items():
                pattern_up = exp_pattern(
                    candidate["mass_squared_up"], beta_up
                )
                pattern_down = exp_pattern(
                    candidate["mass_squared_down"], beta_down
                )
                score_up = hierarchy_score(pattern_up, target_up)
                score_down = hierarchy_score(pattern_down, target_down)
                rows.append(
                    {
                        **candidate,
                        "beta_up": beta_up_name,
                        "beta_down": beta_down_name,
                        "up_pattern": pattern_up.tolist(),
                        "down_pattern": pattern_down.tolist(),
                        "up_log_RMS": score_up,
                        "down_log_RMS": score_down,
                        "combined_log_RMS": math.sqrt(
                            (score_up**2 + score_down**2) / 2
                        ),
                    }
                )

    ordered = sorted(rows, key=lambda row: row["combined_log_RMS"])
    selected = ordered[0]
    ckm = json.loads(
        Path("s2t_two_layer_physical_ckm_redteam_results.json").read_text(
            encoding="utf-8"
        )
    )["post_blind_PDG_2024_control"]
    parameters = standard_parameters(selected["mixing"])
    target_angles = np.array(
        [ckm["sin_theta_12"], ckm["sin_theta_23"], ckm["sin_theta_13"]]
    )
    selected_angles = np.array(
        [
            parameters["sin_theta_12"],
            parameters["sin_theta_23"],
            parameters["sin_theta_13"],
        ]
    )
    ratio_errors = [
        prediction / target
        for prediction, target in zip(
            selected["up_pattern"][:-1] + selected["down_pattern"][:-1],
            target_up[:-1].tolist() + target_down[:-1].tolist(),
        )
    ]
    within_factor_five = sum(
        all(
            0.2 <= prediction / target <= 5.0
            for prediction, target in zip(
                row["up_pattern"][:-1] + row["down_pattern"][:-1],
                target_up[:-1].tolist() + target_down[:-1].tolist(),
            )
        )
        for row in rows
    )
    equal_gap_best = min(
        row["combined_log_RMS"]
        for row in rows
        if row["kernel"] == "inverse_length_laplacian"
    )

    def compact(row):
        return {
            key: value
            for key, value in row.items()
            if key
            not in {"mass_squared_up", "mass_squared_down", "mixing"}
        }

    results = {
        "status": "gap_derived_unequal_edges_plus_exponential_readout_close_four_quark_ratios_within_factor_five_but_mass_selected_candidate_fails_blind_CKM",
        "date": "2026-08-06",
        "protocol": {
            "edge_rule": (
                "affinely normalize each factor spectrum to [0,1], use adjacent "
                "gap fractions as A3 edge weights, and use their product for "
                "the composed E21 E10 = E20 chord"
            ),
            "beta_menu": beta_menu,
            "train": "four light up/down quark hierarchy ratios",
            "blind": "CKM angles and Jarlskog invariant",
            "continuous_fit": False,
        },
        "scan": {
            "structural_candidates": len(structural),
            "mass_readout_candidates": len(rows),
            "within_factor_five_count": within_factor_five,
            "best_rows": [compact(row) for row in ordered[:12]],
            "equal_gap_ablation_best_log_RMS": equal_gap_best,
        },
        "mass_selected_candidate": {
            **compact(selected),
            "multiplicative_errors": ratio_errors,
            "improvement_over_equal_gap": (
                equal_gap_best / selected["combined_log_RMS"]
            ),
        },
        "blind_CKM_gate": {
            "angles": selected_angles.tolist(),
            "angle_ratios": (selected_angles / target_angles).tolist(),
            "absolute_Jarlskog": abs(parameters["Jarlskog"]),
            "Jarlskog_ratio": abs(parameters["Jarlskog"])
            / ckm["Jarlskog"],
            "finding": (
                "The weighted edge metric improves mass hierarchy but predicts "
                "large nonhierarchical CKM mixing."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "A source-derived unequal edge metric is the first tested "
                "noncommuting insertion to place all four light quark ratios "
                "within factor five without continuous fitting."
            ),
            "negative": (
                "The same mass-selected candidate fails every blind CKM scale."
            ),
            "next_gate": (
                "The edge metric must become sector-relative rather than one "
                "chain-versus-chord split; derive two correlated noncommuting "
                "Yukawa graphs from one finite action."
            ),
        },
    }
    assert len(structural) == 12
    assert len(rows) == 108
    assert selected["kernel"] == "inverse_square_laplacian"
    assert selected["orientation"] == "forward"
    assert selected["assignment"] == "chain_up"
    assert selected["beta_up"] == "S1_length"
    assert selected["beta_down"] == "S1_length"
    assert within_factor_five > 0
    assert max(ratio_errors) < 5.0
    assert results["blind_CKM_gate"]["Jarlskog_ratio"] > 500
    assert max(results["blind_CKM_gate"]["angle_ratios"]) > 100

    Path("s2t_weighted_gap_yukawa_readout_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "structural_candidates": len(structural),
                "mass_candidates": len(rows),
                "within_factor_five": within_factor_five,
                "best_mass_score": selected["combined_log_RMS"],
                "mass_errors": ratio_errors,
                "Jarlskog_ratio": results["blind_CKM_gate"][
                    "Jarlskog_ratio"
                ],
                "angle_ratios": results["blind_CKM_gate"]["angle_ratios"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()