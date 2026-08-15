#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

f0, f2, cutoff, radius = sp.symbols(
    "f0 f2 Lambda R", positive=True, real=True
)
scalar_curvature = sp.Integer(6) / radius**2

a2_phi2 = sp.Integer(-4)
a4_kinetic = sp.Integer(2)
a4_phi4 = sp.Integer(2)
a4_R_phi2 = sp.Rational(1, 3)

normalized_quartic = sp.simplify(a4_phi4 / a4_kinetic)
normalized_phi2 = sp.simplify(
    (
        f2 * cutoff**2 * a2_phi2
        + f0 * a4_R_phi2 * scalar_curvature
    )
    / (f0 * a4_kinetic)
)
chi_squared = sp.simplify(-normalized_phi2 / 2)
chi_radius_squared = sp.simplify(chi_squared * radius**2)

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "compact_a2_a4_reduces_bare_freedom_to_one_moment_combination",
    "heat_kernel_ledger": {
        "a0_phi_dependence": False,
        "a2_phi2_spin_traced": int(a2_phi2),
        "a4_kinetic_spin_traced": int(a4_kinetic),
        "a4_phi4_spin_traced": int(a4_phi4),
        "a4_R_phi2_spin_traced": str(a4_R_phi2),
    },
    "normalized_action": {
        "quartic_coefficient": str(normalized_quartic),
        "phi2_coefficient": str(normalized_phi2),
        "chi_squared": str(chi_squared),
        "chi_radius_squared": str(chi_radius_squared),
    },
    "vacuum_condition": {
        "inequality": "(f2/f0)*(Lambda*R)^2 > 1/2",
    },
    "closure": {
        "independent_bare_lambda2_lambda4": False,
        "remaining_combination": "(f2/f0)*(Lambda*R)^2",
        "parameter_free_scale": False,
        "finite_quantum_matching_open": True,
    },
    "verdict": {
        "external_route_partial_pass": True,
        "next_gate": "spectral function moment menu",
    },
}

assert normalized_quartic == 1
assert chi_squared == f2 * cutoff**2 / f0 - scalar_curvature / 12
assert sp.simplify(
    chi_radius_squared
    - (f2 * cutoff**2 * radius**2 / f0 - sp.Rational(1, 2))
) == 0

Path("s2t_v3_compact_a2_a4_moment_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)