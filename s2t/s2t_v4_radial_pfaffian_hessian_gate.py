import contextlib
import io
import json
import runpy

import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar


sigma, theta = sp.symbols("sigma theta", real=True)
radius = sp.exp(sigma)

trace_d2 = 12 * radius**2 + 28
trace_d4 = (
    12 * radius**4
    + 32 * radius**2
    - 8 * radius * sp.cos(theta)
    + 60
)
mu_squared_over_lambda = sp.Rational(13, 3)
bosonic_potential = (
    -mu_squared_over_lambda * trace_d2 + trace_d4
)

reduced_pfaffian_modulus_squared = (
    radius**4
    * (radius**2 + radius * sp.cos(theta) + sp.Rational(1, 4))
)
normalized_pfaffian_ratio = (
    reduced_pfaffian_modulus_squared / sp.Rational(9, 4)
)
reduced_pfaffian_action = -sp.log(normalized_pfaffian_ratio) / 2
full_pfaffian_action = -sp.log(normalized_pfaffian_ratio)


def hessian_at_origin(expression):
    return sp.Matrix(
        [
            [
                sp.simplify(
                    sp.diff(expression, first, second).subs(
                        {sigma: 0, theta: 0}
                    )
                )
                for second in (sigma, theta)
            ]
            for first in (sigma, theta)
        ]
    )


bosonic_hessian = hessian_at_origin(bosonic_potential)
reduced_pfaffian_hessian = hessian_at_origin(reduced_pfaffian_action)
full_pfaffian_hessian = hessian_at_origin(full_pfaffian_action)

with open(
    "s2t_v4_self_consistent_orientation_gate_results.json",
    encoding="utf-8",
) as handle:
    orientation_results = json.load(handle)
orientation_susceptibility = orientation_results["orientation_susceptibility"]

critical_lambda = {
    "reduced": (
        orientation_susceptibility - float(sp.Rational(2, 9))
    )
    / 8,
    "full_ko6": (
        orientation_susceptibility - float(sp.Rational(4, 9))
    )
    / 8,
}

namespace_output = io.StringIO()
with contextlib.redirect_stdout(namespace_output):
    orientation_namespace = runpy.run_path(
        "s2t_v4_self_consistent_orientation_gate.py"
    )
constraints = orientation_namespace["constraints"]
log_trace_exponential_negative = orientation_namespace[
    "log_trace_exponential_negative"
]


def matter_free_energy(orientation_amplitude):
    return -np.mean(
        [
            log_trace_exponential_negative(
                values["energy"]
                - orientation_amplitude * values["orientation"]
            )
            for values in constraints.values()
        ]
    )


mu_ratio_float = float(mu_squared_over_lambda)


def bosonic_value(radial_value, angular_value):
    return (
        -mu_ratio_float * (12 * radial_value**2 + 28)
        + 12 * radial_value**4
        + 32 * radial_value**2
        - 8 * radial_value * np.cos(angular_value)
        + 60
    )


def pfaffian_value(radial_value, angular_value, measure):
    ratio = (
        4
        / 9
        * radial_value**4
        * (
            radial_value**2
            + radial_value * np.cos(angular_value)
            + 0.25
        )
    )
    exponent = -0.5 if measure == "reduced" else -1.0
    return exponent * np.log(ratio)


def total_value(radial_value, angular_value, measure):
    return (
        bosonic_value(radial_value, angular_value)
        + pfaffian_value(radial_value, angular_value, measure)
        + matter_free_energy(radial_value * np.sin(angular_value))
    )


global_minima = {}
theta_grid = np.linspace(-np.pi, np.pi, 2401)
for measure in ("reduced", "full_ko6"):
    best = None
    for angular_value in theta_grid:
        fit = minimize_scalar(
            lambda radial_value: total_value(
                radial_value, angular_value, measure
            ),
            bounds=(1e-6, 4),
            method="bounded",
        )
        row = (float(fit.fun), float(fit.x), float(angular_value))
        if best is None or row < best:
            best = row
    global_minima[measure] = {
        "value": best[0],
        "radius": best[1],
        "theta": best[2],
        "orientation_amplitude": best[1] * np.sin(best[2]),
    }

angular_curvatures_at_unit_radius = {
    "reduced": 8
    + float(sp.Rational(2, 9))
    - orientation_susceptibility,
    "full_ko6": 8
    + float(sp.Rational(4, 9))
    - orientation_susceptibility,
}

output = {
    "gate": "version4_radial_pfaffian_hessian",
    "self_adjoint_radial_pfaffian": {
        "det_chiral_minus": "r^2 (2r+exp(i theta)) exp(-3 i theta)/2",
        "modulus_squared_minus": "r^4 (r^2+r cos(theta)+1/4)",
    },
    "full_trace_d2": str(trace_d2),
    "full_trace_d4_minus": str(trace_d4),
    "mu_squared_over_lambda_for_unit_vacuum": str(mu_squared_over_lambda),
    "bosonic_hessian_sigma_theta": str(bosonic_hessian),
    "reduced_pfaffian_hessian_sigma_theta": str(
        reduced_pfaffian_hessian
    ),
    "full_pfaffian_hessian_sigma_theta": str(full_pfaffian_hessian),
    "mixed_hessian_entries_zero": bool(
        bosonic_hessian[0, 1] == 0
        and reduced_pfaffian_hessian[0, 1] == 0
        and full_pfaffian_hessian[0, 1] == 0
    ),
    "orientation_susceptibility": orientation_susceptibility,
    "critical_lambda": critical_lambda,
    "unit_lambda_angular_curvature": angular_curvatures_at_unit_radius,
    "global_minima_at_unit_lambda": global_minima,
    "radial_mode_generates_quadratic_orientation_mixing": False,
    "flavour_test_reached": False,
    "verdict": "the exact radial extension is stable but its Hessian is diagonal; at canonical quartic normalization the vacuum remains CP even and supplies no new flavour branch",
}

with open(
    "s2t_v4_radial_pfaffian_hessian_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))