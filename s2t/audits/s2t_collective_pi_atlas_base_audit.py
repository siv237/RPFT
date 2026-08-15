#!/usr/bin/env python3
import json
import math

import numpy as np


ALPHA = 1 / 137.035999084
M_E_MEV = 0.51099895
M_MU_MEV = 105.6583755
M_TAU_MEV = 1776.86
M_PROTON_GEV = M_E_MEV * 1836.15267 / 1000


CLAIMS = [
    ("alpha_s", 0.1181, lambda x: 1 / (x * x / 4 + 6)),
    ("sin2_theta_w", 0.2312, lambda x: (8 - 3 / (4 * x)) / (21 + 4 * x)),
    ("bottom_over_proton", 4.18 / M_PROTON_GEV, lambda x: x + 4 / 3),
    ("strange_over_proton", 0.0934 / M_PROTON_GEV, lambda x: 1 / (x * x + 1 / 3)),
    ("down_over_electron", 4.67 / M_E_MEV, lambda x: x * x - 1),
    ("up_over_electron", 2.16 / M_E_MEV, lambda x: x + 1),
    (
        "tau_over_mu",
        M_TAU_MEV / M_MU_MEV,
        lambda x: x * x + 2 * x + 2 / 3 + 2 * ALPHA / 3,
    ),
    ("V_cb", 0.0410, lambda x: 1 / (24 - 1 / x)),
    ("Omega_Lambda", 0.685, lambda x: 1 - 1 / x),
    ("Omega_dm", 0.265, lambda x: 1 / x - 1 / (2 * x * x)),
    ("Omega_b", 0.049, lambda x: 1 / (2 * x * x)),
]


def log_errors(base, claims=CLAIMS):
    return np.array([math.log(formula(base) / target) for _, target, formula in claims])


def score(base, claims=CLAIMS):
    errors = log_errors(base, claims)
    return float(np.sqrt(np.mean(errors * errors)))


def grid_search(claims=CLAIMS, points=200001):
    grid = np.linspace(2.0, 4.0, points)
    scores = np.array([score(float(base), claims) for base in grid])
    best_index = int(np.argmin(scores))
    return grid, scores, float(grid[best_index]), float(scores[best_index])


def leave_one_out():
    rows = []
    for removed_index, (removed_name, _, _) in enumerate(CLAIMS):
        claims = [claim for index, claim in enumerate(CLAIMS) if index != removed_index]
        grid, scores, best_base, best_score = grid_search(claims, points=40001)
        pi_score = score(math.pi, claims)
        percentile = float(100 * np.mean(scores <= pi_score))
        rows.append(
            {
                "removed": removed_name,
                "best_base": best_base,
                "best_score": best_score,
                "pi_score": pi_score,
                "pi_low_error_percentile": percentile,
            }
        )
    return rows


def main():
    grid, scores, best_base, best_score = grid_search()
    pi_score = score(math.pi)
    pi_percentile = float(100 * np.mean(scores <= pi_score))
    named_bases = {
        "pi": math.pi,
        "sqrt_10": math.sqrt(10),
        "22_over_7": 22 / 7,
        "three": 3.0,
        "e": math.e,
    }
    result = {
        "status": "retrospective_common_base_compression_not_pi_uniqueness",
        "scope": {
            "claim_count": len(CLAIMS),
            "base_interval": [2.0, 4.0],
            "metric": "RMS natural-log relative error",
            "warning": "Targets and formula shapes were assembled retrospectively; this is not a blind test.",
        },
        "best_grid_base": best_base,
        "best_grid_score": best_score,
        "pi_score": pi_score,
        "pi_low_error_percentile": pi_percentile,
        "named_base_scores": {
            name: {"base": base, "score": score(base)}
            for name, base in named_bases.items()
        },
        "claims_at_pi": [
            {
                "name": name,
                "target": target,
                "prediction": formula(math.pi),
                "log_error": math.log(formula(math.pi) / target),
            }
            for name, target, formula in CLAIMS
        ],
        "leave_one_out": leave_one_out(),
        "preregistration": {
            "frozen_formula_count": len(CLAIMS),
            "frozen_score": "RMS natural-log relative error with equal claim weights",
            "frozen_base_interval": [2.0, 4.0],
            "forbidden_after_freeze": [
                "changing coefficients",
                "changing formula-to-observable assignments",
                "dropping failed claims",
                "adding a new base-dependent correction after seeing a target",
            ],
            "blocking_condition": "A prospective test still needs observable assignments derived independently of their measured values.",
        },
    }
    with open("s2t_collective_pi_atlas_base_results.json", "w", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "best_base": best_base,
                "best_score": best_score,
                "pi_score": pi_score,
                "pi_percentile": pi_percentile,
                "sqrt_10_score": result["named_base_scores"]["sqrt_10"]["score"],
                "loo_best_base_range": [
                    min(row["best_base"] for row in result["leave_one_out"]),
                    max(row["best_base"] for row in result["leave_one_out"]),
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()