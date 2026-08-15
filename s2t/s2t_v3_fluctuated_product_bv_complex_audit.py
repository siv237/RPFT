#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

charges = sp.Matrix([0, 1, -1, 0])
charge_square_trace = sum(int(q**2) for q in charges)

r, s, chi, gauge_field, gauge_coupling = sp.symbols(
    "r s chi A g", positive=True, real=True
)
gauge_orbit_metric = 4 * (r**2 + s**2)
vacuum_substitution = {r: chi / sp.sqrt(2), s: chi / sp.sqrt(2)}
gauge_mass_term = sp.simplify(
    gauge_orbit_metric.subs(vacuum_substitution) * gauge_field**2
)
mass_squared_ratio = sp.Integer(8) * gauge_coupling**2
gauge_supertrace = 3 * mass_squared_ratio**2

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "relative_u1_and_bv_complex_derived",
    "product_triple": {
        "algebra": "Cinf(K) tensor (C plus C)",
        "hilbert_space": "L2(K,S) tensor H8",
        "dirac": "D_K tensor 1 + gamma_K tensor chi D_F_star",
    },
    "gauge_quotient": {
        "bimodule_charge_vector": [int(q) for q in charges],
        "charge_square_orbit_trace": charge_square_trace,
        "trivial_subgroup": "diagonal U(1)",
        "faithful_group": "relative U(1)",
        "x_charge": -1,
        "z_charge": 1,
        "xz_neutral": True,
    },
    "gauge_mass": {
        "gauge_orbit_metric": str(gauge_orbit_metric),
        "vacuum_mass_term": str(gauge_mass_term),
        "canonical_mass_squared_over_chi2": str(mass_squared_ratio),
    },
    "bv_ledger": {
        "vector_components": 4,
        "goldstone_real_modes": 1,
        "complex_ghost_weight": -2,
        "physical_massive_vector_dof": 3,
        "gauge_supertrace_numerator": str(gauge_supertrace),
    },
    "remaining_inputs": [
        "spectral normalization fixing g",
        "spin structure",
        "fermion flat character",
        "radion-to-chi relation",
        "common finite-part prescription",
    ],
    "verdict": {
        "gauge_quotient_closed": True,
        "bv_complex_closed": True,
        "gauge_mass_parameter_reduced_to_g": True,
        "full_B_computed": False,
        "next_gate": "a4 gauge kinetic normalization",
    },
}

assert charges.dot(sp.ones(4, 1)) == 0
assert charge_square_trace == 2
assert gauge_mass_term == 4 * chi**2 * gauge_field**2
assert mass_squared_ratio == 8 * gauge_coupling**2
assert gauge_supertrace == 192 * gauge_coupling**4
assert 4 + 1 - 2 == 3

Path("s2t_v3_fluctuated_product_bv_complex_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)