#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

r, s, phase, kappa = sp.symbols(
    "r s phase kappa", positive=True, real=True
)

kinetic_metric = sp.diag(4, 4, r**2 + s**2)
vacuum = {
    r: 1 / sp.sqrt(2),
    s: 1 / sp.sqrt(2),
    phase: sp.pi / 2,
}
kinetic_vacuum = sp.simplify(kinetic_metric.subs(vacuum))
potential_hessian = sp.diag(32, 32, 8)
mass_matrix = sp.simplify(kinetic_vacuum.inv() * potential_hessian)
scalar_mass_squared = list(mass_matrix.diagonal())

scalar_supertrace = 3 * 8**2
fermion_supertrace = -2 * 4
finite_numerator = scalar_supertrace + fermion_supertrace
finite_B = sp.simplify(
    sp.Rational(finite_numerator, 64) / sp.pi**2
)

general_numerator = sp.simplify(192 / kappa**2 - 8)
positive_threshold = sp.sqrt(24)

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "finite_zero_mode_B_positive_normalization_and_KK_open",
    "kinetic_metric": {
        "general": str(kinetic_metric),
        "vacuum": str(kinetic_vacuum),
    },
    "scalar_spectrum": {
        "potential_hessian": str(potential_hessian),
        "generalized_mass_matrix": str(mass_matrix),
        "mass_squared_over_chi_squared": [
            str(value) for value in scalar_mass_squared
        ],
        "real_scalar_count": 3,
    },
    "fermion_spectrum": {
        "physical_Dirac_pairs": 2,
        "mass_over_chi": 1,
        "weighted_M4": fermion_supertrace,
    },
    "canonical_supertrace": {
        "scalar_weighted_M4": scalar_supertrace,
        "fermion_weighted_M4": fermion_supertrace,
        "numerator": finite_numerator,
        "factorization": "8*23",
        "B0": str(finite_B),
        "positive": True,
    },
    "normalization_sensitivity": {
        "kinetic_coefficient": str(kappa),
        "supertrace_numerator": str(general_numerator),
        "positive_if": "kappa < sqrt(24)",
        "threshold": str(positive_threshold),
        "kappa_derived": False,
    },
    "omitted_sectors": [
        "finite gauge and ghosts",
        "dilaton-radion fluctuation",
        "nonzero KK towers",
        "common tower subtraction",
    ],
    "verdict": {
        "finite_seed_B_positive": True,
        "canonical_B0_equals_23_over_8pi2": True,
        "full_B_computed": False,
        "quantum_scale_gate_passed": False,
        "next_gate": "derive kappa and compute KK plus gauge correction",
    },
}

assert kinetic_vacuum == sp.diag(4, 4, 1)
assert mass_matrix == sp.diag(8, 8, 8)
assert finite_numerator == 184
assert finite_B == sp.Rational(23, 8) / sp.pi**2

Path("s2t_v3_finite_zero_mode_supertrace_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)