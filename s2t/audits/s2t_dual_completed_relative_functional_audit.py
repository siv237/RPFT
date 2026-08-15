#!/usr/bin/env python3

import json
import math
from pathlib import Path


def stable_mode_log_ratio(rho, beta):
    q = math.exp(-2.0 * math.pi * rho)
    cosine = math.cos(2.0 * math.pi * beta)
    numerator = 1.0 - 2.0 * cosine * q + q * q
    denominator = (1.0 - q) ** 2
    return math.log(numerator / denominator)


def massive_relative_gamma(beta, radius_ratio, n_max=160):
    scalar = 0.0
    coexact = 0.0
    for n in range(1, n_max + 1):
        if n % 2 == 1:
            coexact += (
                2
                * n
                * (n + 2)
                * stable_mode_log_ratio(radius_ratio * (n + 1), beta)
            )
        elif n >= 2:
            scalar += (
                (n + 1) ** 2
                * stable_mode_log_ratio(
                    radius_ratio * math.sqrt(n * (n + 2)), beta
                )
            )
    return 0.5 * coexact - 0.5 * scalar


def winding_log(rho):
    return math.log1p(-math.exp(-2.0 * math.pi * rho))


def flat_bundle_relative_gamma(radius_ratio, n_max=160):
    coexact_untwisted = 0.0
    coexact_twisted = 0.0
    scalar_untwisted = 0.0
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
            scalar_untwisted += scalar_term
    return (coexact_twisted - coexact_untwisted) - (
        scalar_twisted - scalar_untwisted
    )


def dual_complete(function, radius_ratio, *args):
    return function(*args, radius_ratio) + function(*args, 1.0 / radius_ratio)


def log_derivatives(function, step=1e-4):
    upper = function(math.exp(step))
    center = function(1.0)
    lower = function(math.exp(-step))
    first = (upper - lower) / (2.0 * step)
    second = (upper - 2.0 * center + lower) / (step * step)
    return first, second


def logarithmic_grid(minimum=0.25, maximum=4.0, count=401):
    log_minimum = math.log(minimum)
    log_maximum = math.log(maximum)
    for index in range(count):
        fraction = index / (count - 1)
        yield math.exp(log_minimum + fraction * (log_maximum - log_minimum))


beta_rows = []
for beta in [0.125, 0.25, 0.375, 0.5]:
    function = lambda radius, selected_beta=beta: dual_complete(
        massive_relative_gamma, radius, selected_beta
    )
    first, second = log_derivatives(function)
    grid = [
        {"radius_ratio": radius, "dual_action": function(radius)}
        for radius in logarithmic_grid()
    ]
    minimum_row = min(grid, key=lambda row: row["dual_action"])
    beta_rows.append(
        {
            "beta": beta,
            "dual_action_at_unit_radius": function(1.0),
            "log_radius_first_derivative_at_1": first,
            "log_radius_second_derivative_at_1": second,
            "grid_minimum": minimum_row,
            "duality_error_max": max(
                abs(function(radius) - function(1.0 / radius))
                for radius in [0.4, 0.5, 0.75, 1.25, 2.0, 2.5]
            ),
            "sample": [
                {"radius_ratio": radius, "dual_action": function(radius)}
                for radius in [0.5, 0.75, 1.0, 1.25, 2.0]
            ],
        }
    )

flat_function = lambda radius: dual_complete(
    flat_bundle_relative_gamma, radius
)
flat_first, flat_second = log_derivatives(flat_function)
flat_grid = [
    {"radius_ratio": radius, "dual_action": flat_function(radius)}
    for radius in logarithmic_grid()
]
flat_minimum = min(flat_grid, key=lambda row: row["dual_action"])

quarter_row = next(row for row in beta_rows if row["beta"] == 0.25)

torsion = json.loads(
    Path("s2t_neutrino_torsion_square_root_defect_results.json").read_text(
        encoding="utf-8"
    )
)
qcycle = json.loads(
    Path("s2t_neutrino_qcycle_geodesic_gram_results.json").read_text(
        encoding="utf-8"
    )
)

quarter_sector_discrete = (
    torsion["existing_gauge_holonomy_match"]["beta"] == 0.25
    and torsion["parameter_audit"]["continuous_parameter_added"] is False
)
reciprocal_cycle_structure = (
    abs(qcycle["Qcycle"]["determinant"] - 1.0) < 1e-14
    and "exchanges" in qcycle["Qcycle"]["duality"]
)

results = {
    "status": "dual_completed_relative_functional_selects_unit_radius_conditionally",
    "date": "2026-08-03",
    "definition": {
        "single_response": "G_beta(r)=Delta Gamma_rel(beta;r)",
        "dual_completion": "F_beta(r)=G_beta(r)+G_beta(1/r)",
        "log_radius_coordinate": "x=log(r), so F_beta(x)=F_beta(-x)",
        "equal_weights": (
            "The two terms have unit relative weight because they are exchanged by "
            "the declared reciprocal involution; no continuous coefficient is introduced."
        ),
    },
    "analytic_result": {
        "duality": "F(r)=F(1/r)",
        "stationarity": "dF/d(log r)=0 at r=1 follows exactly from evenness in log r",
        "stability_status": (
            "positive curvature and global minimum are numerical spectral results, "
            "not yet an analytic convexity theorem"
        ),
    },
    "continuous_holonomy_sectors": beta_rows,
    "quarter_sector": {
        "topologically_available_without_fit": quarter_sector_discrete,
        "dual_action_at_unit_radius": quarter_row["dual_action_at_unit_radius"],
        "log_radius_curvature_at_1": quarter_row[
            "log_radius_second_derivative_at_1"
        ],
        "grid_minimum_radius_ratio": quarter_row["grid_minimum"]["radius_ratio"],
        "interpretation": (
            "The torsion square-root defect fixes beta=1/4 as a discrete sector label. "
            "Conditioned on that sector, reciprocal completion selects r=1 as a stable minimum."
        ),
    },
    "RP3_Z2_flat_bundle_dual_completion": {
        "dual_action_at_unit_radius": flat_function(1.0),
        "log_radius_first_derivative_at_1": flat_first,
        "log_radius_second_derivative_at_1": flat_second,
        "grid_minimum": flat_minimum,
        "duality_error_max": max(
            abs(flat_function(radius) - flat_function(1.0 / radius))
            for radius in [0.4, 0.5, 0.75, 1.25, 2.0, 2.5]
        ),
    },
    "source_checks": {
        "quarter_holonomy_is_discrete_defect_sector": quarter_sector_discrete,
        "Qcycle_has_determinant_one_reciprocal_structure": reciprocal_cycle_structure,
    },
    "checks": {
        "all_duality_errors_below_1e_14": all(
            row["duality_error_max"] < 1e-14 for row in beta_rows
        ),
        "all_log_derivatives_at_1_below_1e_10": all(
            abs(row["log_radius_first_derivative_at_1"]) < 1e-10
            for row in beta_rows
        ),
        "all_curvatures_positive": all(
            row["log_radius_second_derivative_at_1"] > 0.0 for row in beta_rows
        ),
        "all_grid_minima_at_1": all(
            abs(row["grid_minimum"]["radius_ratio"] - 1.0) < 1e-12
            for row in beta_rows
        ),
        "flat_bundle_minimum_at_1": abs(
            flat_minimum["radius_ratio"] - 1.0
        ) < 1e-12,
    },
    "theory_gate": {
        "positive": (
            "A no-fit reciprocal completion converts the previously monotone relative "
            "response into a stable unit-radius functional in every tested nontrivial phase sector."
        ),
        "remaining_bridge": (
            "The reciprocal involution is established for the intrinsic cycle Gram complex, "
            "but it has not yet been derived as an exact symmetry pairing the full Maxwell--FP "
            "determinant at r and 1/r."
        ),
        "zero_mode_gap": (
            "The true scalar zero-mode and gauge-volume measure remain outside the massive audit."
        ),
        "no_alpha_claim": (
            "The functional selects a shape ratio only. It is not normalized to alpha and "
            "must not be fitted to alpha before the reciprocal bridge and zero-mode measure are derived."
        ),
    },
    "verdict": (
        "The reciprocal completion is the first post-C6 construction that produces a stable "
        "r=1 configuration without a fitted coefficient. The stationarity is exact by duality, "
        "and the positive curvature/global minimum are robust numerically. This is a conditional "
        "structural success: the missing theorem is an ambient duality bridge from Qcycle to the "
        "full Maxwell--FP relative determinant, plus the scalar zero-mode measure."
    ),
}

assert results["checks"]["all_duality_errors_below_1e_14"]
assert results["checks"]["all_log_derivatives_at_1_below_1e_10"]
assert results["checks"]["all_curvatures_positive"]
assert results["checks"]["all_grid_minima_at_1"]
assert results["checks"]["flat_bundle_minimum_at_1"]
assert results["source_checks"]["quarter_holonomy_is_discrete_defect_sector"]
assert results["source_checks"]["Qcycle_has_determinant_one_reciprocal_structure"]

Path("s2t_dual_completed_relative_functional_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

print(
    json.dumps(
        {
            "status": results["status"],
            "quarter_sector": results["quarter_sector"],
            "flat_bundle": results["RP3_Z2_flat_bundle_dual_completion"],
            "checks": results["checks"],
        },
        ensure_ascii=False,
        indent=2,
    )
)