#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

u, a, cutoff_radius = sp.symbols(
    "u a LambdaR", positive=True, real=True
)

profiles = {
    "sharp": sp.Integer(1),
    "heat": sp.integrate(sp.exp(-u), (u, 0, sp.oo)),
    "gauss": sp.integrate(sp.exp(-u**2), (u, 0, sp.oo)),
    "heat2": sp.integrate((1 + u) * sp.exp(-u), (u, 0, sp.oo)),
}

chi_radius_squared_at_lock = {
    name: sp.simplify(moment - sp.Rational(1, 2))
    for name, moment in profiles.items()
}
thresholds = {
    name: sp.simplify(1 / sp.sqrt(2 * moment))
    for name, moment in profiles.items()
}

heat_family_moment = sp.integrate(sp.exp(-a * u), (u, 0, sp.oo))
moment_cutoff_invariant = sp.simplify(
    heat_family_moment * cutoff_radius**2
)

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "spectral_function_menu_does_not_select_unique_moment",
    "moment_convention": {
        "f0": "f(0)=1",
        "f2": "integral_0_infinity f(u) du",
    },
    "menu": {
        name: {
            "f2_over_f0": str(moment),
            "chiR_squared_at_LambdaR_1": str(
                chi_radius_squared_at_lock[name]
            ),
            "vacuum_pass_at_LambdaR_1": bool(
                sp.N(chi_radius_squared_at_lock[name]) > 0
            ),
            "LambdaR_threshold": str(thresholds[name]),
        }
        for name, moment in profiles.items()
    },
    "continuous_heat_family": {
        "profile": "exp(-a u)",
        "moment": str(heat_family_moment),
        "invariant": str(moment_cutoff_invariant),
        "shape_cutoff_degeneracy": True,
    },
    "verdict": {
        "unique_chiR_from_natural_menu": False,
        "remaining_train_combination": "zeta_mom=(f2/f0)*(Lambda R)^2",
        "next_gate": "physical representation and readout",
    },
}

assert profiles["sharp"] == 1
assert profiles["heat"] == 1
assert profiles["gauss"] == sp.sqrt(sp.pi) / 2
assert profiles["heat2"] == 2
assert heat_family_moment == 1 / a
assert moment_cutoff_invariant == cutoff_radius**2 / a

Path("s2t_v3_spectral_function_moment_menu_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)