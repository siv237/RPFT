#!/usr/bin/env python3

import json
import math
from pathlib import Path


def stable_mode_log_ratio(rho, beta):
    x = 2.0 * math.pi * rho
    q = math.exp(-x)
    cosine = math.cos(2.0 * math.pi * beta)
    numerator = 1.0 - 2.0 * cosine * q + q * q
    denominator = (1.0 - q) ** 2
    return math.log(numerator / denominator)


def massive_scalar_modes(n_max):
    for n in range(2, n_max + 1, 2):
        yield math.sqrt(n * (n + 2)), (n + 1) ** 2


def coexact_one_form_modes(n_max):
    for n in range(1, n_max + 1, 2):
        yield float(n + 1), 2 * n * (n + 2)


def sector_ratio(mode_builder, beta, radius_ratio, n_max):
    total = 0.0
    for rho_unit, multiplicity in mode_builder(n_max):
        total += multiplicity * stable_mode_log_ratio(
            radius_ratio * rho_unit, beta
        )
    return total


def evaluate(beta, radius_ratio, n_max=160):
    scalar = sector_ratio(massive_scalar_modes, beta, radius_ratio, n_max)
    coexact = sector_ratio(coexact_one_form_modes, beta, radius_ratio, n_max)
    gamma_massive_fp = 0.5 * coexact - 0.5 * scalar
    return {
        "beta": beta,
        "radius_ratio_R1_over_R3": radius_ratio,
        "scalar_logdet_ratio_massive": scalar,
        "coexact_logdet_ratio": coexact,
        "standard_FP_Gamma_ratio_massive": gamma_massive_fp,
    }


def derivative_beta(beta, radius_ratio, step=1e-5):
    upper = evaluate(beta + step, radius_ratio)["standard_FP_Gamma_ratio_massive"]
    lower = evaluate(beta - step, radius_ratio)["standard_FP_Gamma_ratio_massive"]
    return (upper - lower) / (2.0 * step)


def curvature_beta(beta, radius_ratio, step=1e-4):
    upper = evaluate(beta + step, radius_ratio)["standard_FP_Gamma_ratio_massive"]
    center = evaluate(beta, radius_ratio)["standard_FP_Gamma_ratio_massive"]
    lower = evaluate(beta - step, radius_ratio)["standard_FP_Gamma_ratio_massive"]
    return (upper - 2.0 * center + lower) / (step * step)


def winding_log(rho):
    return math.log1p(-math.exp(-2.0 * math.pi * rho))


def rp3_flat_bundle_winding_ratio(radius_ratio, n_max=160):
    coexact_untwisted = 0.0
    coexact_twisted = 0.0
    scalar_untwisted_massive = 0.0
    scalar_twisted = 0.0
    for n in range(1, n_max + 1):
        coexact_term = (
            2 * n * (n + 2) * winding_log(radius_ratio * (n + 1))
        )
        scalar_term = (
            (n + 1) ** 2
            * winding_log(radius_ratio * math.sqrt(n * (n + 2)))
        )
        if n % 2 == 1:
            coexact_untwisted += coexact_term
            scalar_twisted += scalar_term
        else:
            coexact_twisted += coexact_term
            scalar_untwisted_massive += scalar_term
    coexact_difference = coexact_twisted - coexact_untwisted
    scalar_difference = scalar_twisted - scalar_untwisted_massive
    return {
        "radius_ratio_R1_over_R3": radius_ratio,
        "coexact_bosonic_Gamma_twisted_minus_untwisted": coexact_difference,
        "scalar_winding_sum_twisted_minus_untwisted": scalar_difference,
        "standard_FP_Gamma_twisted_minus_untwisted_massive": (
            coexact_difference - scalar_difference
        ),
    }


beta_grid = [0.0, 0.125, 0.25, 0.375, 0.5]
radius_grid = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]

holonomy_sweep_unit_radius = [evaluate(beta, 1.0) for beta in beta_grid]
radius_sweep_quarter_holonomy = [evaluate(0.25, ratio) for ratio in radius_grid]
radius_sweep_half_holonomy = [evaluate(0.5, ratio) for ratio in radius_grid]

convergence = []
for cutoff in [20, 40, 80, 160]:
    row = evaluate(0.25, 1.0, n_max=cutoff)
    convergence.append(
        {
            "n_max": cutoff,
            "standard_FP_Gamma_ratio_massive": row[
                "standard_FP_Gamma_ratio_massive"
            ],
        }
    )

symmetry_tests = []
for beta in [0.1, 0.2, 0.3, 0.4]:
    value = evaluate(beta, 1.0)["standard_FP_Gamma_ratio_massive"]
    reflected = evaluate(1.0 - beta, 1.0)["standard_FP_Gamma_ratio_massive"]
    periodic = evaluate(beta + 1.0, 1.0)["standard_FP_Gamma_ratio_massive"]
    symmetry_tests.append(
        {
            "beta": beta,
            "reflection_error": abs(value - reflected),
            "periodicity_error": abs(value - periodic),
        }
    )

stationary_points = []
for beta in [0.0, 0.25, 0.5]:
    stationary_points.append(
        {
            "beta": beta,
            "first_derivative": derivative_beta(beta, 1.0),
            "second_derivative": curvature_beta(beta, 1.0),
        }
    )

quarter_values = [
    row["standard_FP_Gamma_ratio_massive"]
    for row in radius_sweep_quarter_holonomy
]
half_values = [
    row["standard_FP_Gamma_ratio_massive"]
    for row in radius_sweep_half_holonomy
]

flat_bundle_radius_sweep = [
    rp3_flat_bundle_winding_ratio(ratio) for ratio in radius_grid
]
flat_bundle_values = [
    row["standard_FP_Gamma_twisted_minus_untwisted_massive"]
    for row in flat_bundle_radius_sweep
]
flat_bundle_convergence = []
for cutoff in [20, 40, 80, 160]:
    row = rp3_flat_bundle_winding_ratio(1.0, n_max=cutoff)
    flat_bundle_convergence.append(
        {
            "n_max": cutoff,
            "standard_FP_Gamma_twisted_minus_untwisted_massive": row[
                "standard_FP_Gamma_twisted_minus_untwisted_massive"
            ],
        }
    )

results = {
    "status": "relative_holonomy_determinant_finite_symmetric_but_no_radius_selection",
    "date": "2026-08-03",
    "observable": {
        "mode_formula": (
            "log[(cosh(2*pi*rho)-cos(2*pi*beta))/(cosh(2*pi*rho)-1)]"
        ),
        "Maxwell_FP_massive_ratio": (
            "Delta Gamma=1/2 Delta logdet(Delta_1,coex) "
            "-1/2 Delta logdet'(Delta_0,massive)"
        ),
        "reason_for_ratio": (
            "Twisted and untwisted operators have the same local heat coefficients, "
            "so their finite holonomy difference avoids an independent local subtraction."
        ),
        "excluded_branch": (
            "The constant scalar zero-mode branch is excluded from this first audit "
            "because comparing an unprimed twisted mode with a primed beta=0 mode "
            "requires an explicit zero-mode and gauge-volume measure."
        ),
    },
    "spectra": {
        "untwisted_RP3_scalar_massive": (
            "n even, n>=2, lambda=n(n+2)/R3^2, d=(n+1)^2"
        ),
        "untwisted_RP3_coexact_one_forms": (
            "n odd, n>=1, lambda=(n+1)^2/R3^2, d=2*n*(n+2)"
        ),
    },
    "holonomy_sweep_R1_over_R3_1": holonomy_sweep_unit_radius,
    "radius_sweep_beta_1_over_4": radius_sweep_quarter_holonomy,
    "radius_sweep_beta_1_over_2": radius_sweep_half_holonomy,
    "RP3_Z2_flat_bundle_winding_radius_sweep": flat_bundle_radius_sweep,
    "stationary_beta_tests_R1_over_R3_1": stationary_points,
    "convergence_beta_1_over_4_R1_over_R3_1": convergence,
    "RP3_Z2_flat_bundle_convergence_R1_over_R3_1": flat_bundle_convergence,
    "symmetry_tests": symmetry_tests,
    "checks": {
        "cutoff_80_to_160_error": abs(
            convergence[-1]["standard_FP_Gamma_ratio_massive"]
            - convergence[-2]["standard_FP_Gamma_ratio_massive"]
        ),
        "max_reflection_error": max(row["reflection_error"] for row in symmetry_tests),
        "max_periodicity_error": max(row["periodicity_error"] for row in symmetry_tests),
        "beta_zero_ratio": holonomy_sweep_unit_radius[0][
            "standard_FP_Gamma_ratio_massive"
        ],
        "quarter_radius_sweep_monotone_to_zero": all(
            quarter_values[index] > quarter_values[index + 1]
            for index in range(len(quarter_values) - 1)
        ),
        "half_radius_sweep_monotone_to_zero": all(
            half_values[index] > half_values[index + 1]
            for index in range(len(half_values) - 1)
        ),
        "flat_bundle_cutoff_80_to_160_error": abs(
            flat_bundle_convergence[-1][
                "standard_FP_Gamma_twisted_minus_untwisted_massive"
            ]
            - flat_bundle_convergence[-2][
                "standard_FP_Gamma_twisted_minus_untwisted_massive"
            ]
        ),
        "flat_bundle_radius_sweep_monotone_to_zero": all(
            flat_bundle_values[index] > flat_bundle_values[index + 1]
            for index in range(len(flat_bundle_values) - 1)
        ),
    },
    "interpretation": {
        "positive": (
            "The massive twisted/untwisted determinant ratio is finite, rapidly "
            "convergent, periodic and reflection symmetric without fitting alpha."
        ),
        "phase_selection": (
            "beta=0 and beta=1/2 are symmetry-enforced stationary branches; beta=1/4 "
            "is not selected by this determinant alone."
        ),
        "radius_selection": (
            "For beta=1/4 and beta=1/2 the relative action decreases monotonically "
            "toward zero as R1/R3 grows. The ratio alone does not stabilize a finite radius."
        ),
        "sector_warning": (
            "The coexact and scalar contributions are individually larger than their "
            "Maxwell-FP difference, so the gauge bookkeeping remains essential."
        ),
        "RP3_flat_bundle_result": (
            "The nontrivial-versus-trivial Z2 flat-bundle winding ratio is also finite "
            "and topology-selected, but it remains positive and monotone toward zero "
            "with increasing R1/R3. It supplies a discrete response observable, not a "
            "standalone radius potential."
        ),
    },
    "next_gate": [
        "add the constant scalar branch with a derived zero-mode/gauge-volume measure",
        "combine the relative determinant with the geometric configuration functional before testing radius stationarity",
        "test the nontrivial RP3 flat character as a separate bundle ratio, not as the standard Maxwell sector",
        "only after these steps ask whether one stationary configuration predicts more than one blind observable",
    ],
    "verdict": (
        "The relative determinant idea survives its first strict test as a clean finite "
        "holonomy observable, but it does not by itself select the quarter-holonomy or "
        "the unit radius. It is therefore a valid building block for a larger variational "
        "functional, not yet a replacement formula for alpha."
    ),
}

assert results["checks"]["cutoff_80_to_160_error"] < 1e-14
assert results["checks"]["max_reflection_error"] < 1e-14
assert results["checks"]["max_periodicity_error"] < 1e-14
assert abs(results["checks"]["beta_zero_ratio"]) < 1e-14
assert results["checks"]["quarter_radius_sweep_monotone_to_zero"]
assert results["checks"]["half_radius_sweep_monotone_to_zero"]
assert results["checks"]["flat_bundle_cutoff_80_to_160_error"] < 1e-14
assert results["checks"]["flat_bundle_radius_sweep_monotone_to_zero"]

Path("s2t_relative_holonomy_determinant_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

print(
    json.dumps(
        {
            "status": results["status"],
            "unit_radius_sweep": [
                {
                    "beta": row["beta"],
                    "Gamma_ratio": row["standard_FP_Gamma_ratio_massive"],
                }
                for row in holonomy_sweep_unit_radius
            ],
            "stationary_points": stationary_points,
            "RP3_Z2_flat_bundle_at_unit_radius": flat_bundle_radius_sweep[2],
            "checks": results["checks"],
        },
        ensure_ascii=False,
        indent=2,
    )
)