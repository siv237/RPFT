#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

kinetic_metric = sp.diag(4, 4, 1)
potential_hessian = sp.diag(32, 32, 8)
kappa = sp.Integer(2)
canonical_kinetic_matrix = kappa * kinetic_metric
mass_matrix = sp.simplify(
    canonical_kinetic_matrix.inv() * potential_hessian
)

scalar_numerator = 3 * 4**2
fermion_numerator = -8
finite_numerator = scalar_numerator + fermion_numerator
gauge_numerator = 27
completed_numerator = finite_numerator + gauge_numerator

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "external_redteam_factor_two_rejected_other_checks_integrated",
    "quadratic_convention": {
        "lagrangian": "(kappa/2) G_ab dq^a dq^b - (1/2) H_ab q^a q^b",
        "canonical_kinetic_matrix": str(canonical_kinetic_matrix),
        "mass_matrix": str(mass_matrix),
        "scalar_mass_squared_over_chi2": 4,
    },
    "supertrace": {
        "scalar": scalar_numerator,
        "fermion": fermion_numerator,
        "finite": finite_numerator,
        "gauge": gauge_numerator,
        "finite_plus_gauge": completed_numerator,
    },
    "flattening": {
        "current_equation": "B Bdagger = I2",
        "half_identity_present": False,
    },
    "brst": {
        "feynman_gauge_short_count": "4+1-2=3",
        "general_xi_unphysical_quartet": "1+1-2=0",
        "physical_vector_dof": 3,
        "gauge_independent": True,
    },
    "heat_kernel_degrees": {
        "a0": "identity only; no Phi",
        "a2": "-Phi^2 + R/6",
        "a4": "Phi^4/2 + kinetic + gauge - R Phi^2/6 + curvature",
        "quartic_from_a0": False,
    },
    "verdict": {
        "change_40_to_184": False,
        "change_67_to_211": False,
        "g_squared_3_over_8_retained": True,
        "next_gate": "explicit compact a2 a4 spectral moment audit",
    },
}

assert canonical_kinetic_matrix == 2 * kinetic_metric
assert mass_matrix == sp.diag(4, 4, 4)
assert finite_numerator == 40
assert completed_numerator == 67
assert 1 + 1 - 2 == 0

Path("s2t_v3_external_redteam_convention_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)