#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar


INPUT_PATH = Path("s2t_v4_spectral_gauge_normalization_gate_results.json")
OUTPUT_PATH = Path("s2t_v4_spectral_pati_salam_bridge_gate_results.json")


def inverse_running(inverse_at_start, beta_coefficient, log_ratio):
    return inverse_at_start - beta_coefficient * log_ratio / (8.0 * math.pi**2)


def sm_inverse_couplings(inputs, scale):
    log_ratio = math.log(scale / inputs["MZ_GeV"])
    couplings = inputs["couplings_at_MZ"]
    return {
        "Y": inverse_running(1.0 / couplings["gY"] ** 2, 41.0 / 6.0, log_ratio),
        "L": inverse_running(1.0 / couplings["g2"] ** 2, -19.0 / 6.0, log_ratio),
        "4": inverse_running(1.0 / couplings["g3"] ** 2, -7.0, log_ratio),
    }


def pati_salam_boundary(inputs, breaking_scale):
    sm_inverse = sm_inverse_couplings(inputs, breaking_scale)
    inverse_r = sm_inverse["Y"] - (2.0 / 3.0) * sm_inverse["4"]
    if inverse_r <= 0.0:
        raise ValueError("Pati-Salam matching gives a non-positive inverse right coupling")
    return {"R": inverse_r, "L": sm_inverse["L"], "4": sm_inverse["4"]}


def ps_couplings_at_scale(boundary, beta_coefficients, breaking_scale, scale):
    log_ratio = math.log(scale / breaking_scale)
    inverse = {
        key: boundary[key] + beta_coefficients[key] * log_ratio / (8.0 * math.pi**2)
        for key in ("R", "L", "4")
    }
    if min(inverse.values()) <= 0.0:
        return None
    return np.array([1.0 / math.sqrt(inverse[key]) for key in ("R", "L", "4")])


def relative_spread(couplings):
    return float((np.max(couplings) - np.min(couplings)) / np.mean(couplings))


def best_unification_for_fixed_breaking(inputs, beta_coefficients, breaking_scale):
    boundary = pati_salam_boundary(inputs, breaking_scale)
    upper_log = math.log(1.0e19 / breaking_scale)

    def objective(log_ratio):
        couplings = ps_couplings_at_scale(
            boundary, beta_coefficients, breaking_scale, breaking_scale * math.exp(log_ratio)
        )
        return 1.0e6 if couplings is None else relative_spread(couplings)

    optimum = minimize_scalar(objective, bounds=(0.0, upper_log), method="bounded")
    scale = breaking_scale * math.exp(optimum.x)
    couplings = ps_couplings_at_scale(boundary, beta_coefficients, breaking_scale, scale)
    return {
        "breaking_scale_GeV": breaking_scale,
        "best_unification_scale_GeV": scale,
        "couplings_R_L_4": couplings.tolist(),
        "relative_spread": relative_spread(couplings),
    }


def best_breaking_scale(inputs, beta_coefficients):
    def objective(log_breaking_scale):
        breaking_scale = math.exp(log_breaking_scale)
        return best_unification_for_fixed_breaking(
            inputs, beta_coefficients, breaking_scale
        )["relative_spread"]

    optimum = minimize_scalar(
        objective,
        bounds=(math.log(1.0e9), math.log(1.0e16)),
        method="bounded",
        options={"xatol": 1.0e-12},
    )
    result = best_unification_for_fixed_breaking(
        inputs, beta_coefficients, math.exp(optimum.x)
    )
    result["breaking_scale_was_fitted"] = True
    return result


def main():
    gauge = json.loads(INPUT_PATH.read_text())
    inputs = {
        "MZ_GeV": gauge["inputs"]["MZ_GeV"],
        "couplings_at_MZ": gauge["couplings_at_MZ"],
    }
    fixed_scale = gauge["pairwise_crossings"]["g1_g2"]["scale_GeV"]

    scenarios = {
        "composite": {"R": 7.0 / 3.0, "L": 3.0, "4": 31.0 / 3.0},
        "composite_plus_1_1_15": {"R": 7.0 / 3.0, "L": 3.0, "4": 9.0},
        "fundamental": {"R": -26.0 / 3.0, "L": -2.0, "4": 2.0},
        "left_right_fundamental": {
            "R": -26.0 / 3.0,
            "L": -26.0 / 3.0,
            "4": -4.0 / 3.0,
        },
    }

    fixed_results = {
        name: best_unification_for_fixed_breaking(inputs, beta, fixed_scale)
        for name, beta in scenarios.items()
    }
    fitted_results = {
        name: best_breaking_scale(inputs, beta) for name, beta in scenarios.items()
    }
    fixed_spreads = [item["relative_spread"] for item in fixed_results.values()]

    output = {
        "gate": "version4_spectral_pati_salam_bridge",
        "sources": [
            "arXiv:1507.08161",
            "arXiv:1905.04533",
            "arXiv:hep-ph/0611196",
            "arXiv:hep-th/0407014",
        ],
        "matching": "g3=g4, g2=gL, 1/gY^2=1/gR^2+2/(3 g4^2)",
        "scenario_beta_coefficients_paper_convention": scenarios,
        "fixed_project_breaking_scale": {
            "origin": "existing one-loop SM g1=g2 crossing",
            "scale_GeV": fixed_scale,
        },
        "fixed_scale_results": fixed_results,
        "freely_optimized_breaking_scale_results": fitted_results,
        "fixed_scale_spread_range": [min(fixed_spreads), max(fixed_spreads)],
        "passes_without_new_scale_fit": min(fixed_spreads) < 0.01,
        "architecture_verdict": (
            "Pati-Salam is a coherent spectral bridge candidate, but the existing project scale "
            "leaves 2.6-4.9 percent mismatch. Exact one-loop unification reappears only after "
            "choosing the intermediate scale, so the bridge is not yet a prediction."
        ),
        "next_gate": (
            "derive the Pati-Salam breaking scale and a viable Pati-Salam-to-SM vacuum from the "
            "finite Dirac/scalar sector before rerunning gauge unification"
        ),
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")

    print("fixed project scale:", f"{fixed_scale:.12e}", "GeV")
    for name, item in fixed_results.items():
        print(
            name,
            "spread=",
            f"{100.0 * item['relative_spread']:.4f}%",
            "Lambda=",
            f"{item['best_unification_scale_GeV']:.12e}",
        )
    print("\nfree-scale diagnostic:")
    for name, item in fitted_results.items():
        print(
            name,
            "mR=",
            f"{item['breaking_scale_GeV']:.12e}",
            "Lambda=",
            f"{item['best_unification_scale_GeV']:.12e}",
            "spread=",
            f"{100.0 * item['relative_spread']:.6g}%",
        )


if __name__ == "__main__":
    main()