#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

kinetic_metric = sp.diag(4, 4, 1)
potential_hessian = sp.diag(32, 32, 8)
kappa = sp.Integer(2)
physical_metric = kappa * kinetic_metric
mass_matrix = sp.simplify(physical_metric.inv() * potential_hessian)

scalar_weighted_M4 = 3 * 4**2
fermion_weighted_M4 = -2 * 4
supertrace_numerator = scalar_weighted_M4 + fermion_weighted_M4
B0 = sp.simplify(sp.Rational(supertrace_numerator, 64) / sp.pi**2)

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "product_heat_kernel_kappa_closed_finite_B_positive",
    "heat_kernel": {
        "operator": "i gamma^mu d_mu + gamma5 Phi",
        "E": "-Phi^2-i gamma^mu gamma5 d_mu Phi",
        "spin_trace_E2": "4*((dPhi)^2+Phi^4)",
        "kinetic_quartic_coefficient_equal": True,
        "kappa_in_previous_convention": int(kappa),
    },
    "scalar_spectrum": {
        "kinetic_metric": str(kinetic_metric),
        "physical_metric": str(physical_metric),
        "potential_hessian": str(potential_hessian),
        "mass_squared_matrix_over_chi2": str(mass_matrix),
        "scalar_mass_squared_over_chi2": 4,
        "count": 3,
    },
    "finite_supertrace": {
        "scalar_weighted_M4": scalar_weighted_M4,
        "fermion_weighted_M4": fermion_weighted_M4,
        "numerator": supertrace_numerator,
        "B0": str(B0),
        "positive": True,
    },
    "status_correction": {
        "old_conditional_B0": "23/(8*pi^2)",
        "old_kappa": 1,
        "new_derived_B0": "5/(8*pi^2)",
        "number_23_robust": False,
    },
    "verdict": {
        "kappa_gate_closed": True,
        "finite_B_positive": True,
        "full_B_computed": False,
        "next_gate": "gauge ghost and KK correction",
    },
}

assert mass_matrix == sp.diag(4, 4, 4)
assert supertrace_numerator == 40
assert B0 == sp.Rational(5, 8) / sp.pi**2

Path("s2t_v3_product_heat_kernel_kappa_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)