#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

B, chi, mu, c, lambda4, t = sp.symbols(
    "B chi mu c lambda4 t", positive=True, real=True
)

one_loop = B * chi**4 * (sp.log(chi**2 / mu**2) - c)
potential = one_loop + lambda4 * chi**4
stationary_factor = sp.simplify(sp.diff(potential, chi) / (4 * chi**3))
log_solution = sp.solve(
    sp.Eq(stationary_factor, 0),
    sp.log(chi**2 / mu**2),
)[0]

scaled_one_loop = sp.expand(
    B * chi**4 * (sp.log(chi**2 / (sp.exp(t) * mu) ** 2) - c)
)
scale_shift = sp.simplify(scaled_one_loop - one_loop)
counterterm_compensation = 2 * B * t * chi**4

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "base_K_subtraction_not_parameter_free",
    "one_loop": {
        "potential": str(one_loop),
        "stationary_factor": str(stationary_factor),
        "log_chi2_over_mu2": str(log_solution),
    },
    "zeta_scale": {
        "mu_transformation": "mu -> exp(t) mu",
        "potential_shift": str(scale_shift),
        "lambda4_compensation": "lambda4 -> lambda4 + 2 B t",
        "compensation_check": str(
            sp.simplify(scale_shift + counterterm_compensation)
        ),
    },
    "prescriptions": {
        "zeta_minimal": {
            "computationally_defined": True,
            "geometrically_unique": False,
        },
        "mu_equals_inverse_radius": {
            "new_dimensionful_input": False,
            "fixes_absolute_scale": False,
            "finite_lambda4_open": True,
        },
        "spectral_cutoff": {
            "can_set_boundary_condition": True,
            "continuous_inputs": ["Lambda", "f0", "f2"],
        },
    },
    "verdict": {
        "positive_B_allows_conditional_minimum": True,
        "vacuum_location_predicted": False,
        "open_data": "one scale-setting or finite subtraction condition",
        "next_choice": "one train scale or new dynamical normalization",
    },
}

assert log_solution == c - sp.Rational(1, 2) - lambda4 / B
assert scale_shift == -2 * B * chi**4 * t
assert sp.simplify(scale_shift + counterterm_compensation) == 0

Path("s2t_v3_base_k_spectral_renormalization_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)