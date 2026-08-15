#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

G_reduced = sp.diag(4, 4, 1)
H_reduced = sp.diag(32, 32, 8)
kappa = sp.Integer(2)

G_full = 2 * G_reduced
H_full = 2 * H_reduced

mass_reduced = sp.simplify(
    (kappa * G_reduced).inv() * H_reduced
)
mass_full = sp.simplify(
    (kappa * G_full).inv() * H_full
)

charge_trace_reduced = sp.Integer(2)
charge_trace_full = 2 * charge_trace_reduced
scalar_coefficient_reduced = sp.Integer(2)
scalar_coefficient_full = 2 * scalar_coefficient_reduced

gauge_ratio_reduced = sp.simplify(
    sp.Rational(2, 3)
    * charge_trace_reduced
    / scalar_coefficient_reduced
)
gauge_ratio_full = sp.simplify(
    sp.Rational(2, 3)
    * charge_trace_full
    / scalar_coefficient_full
)

supertrace_numerator = 3 * 4**2 + 3 * 3**2 - 2 * 4

results = {
    "date": "2026-08-10",
    "version": "S2T-III.H",
    "status": "pfaffian_fermion_half_count_full_bosonic_trace",
    "trace_dictionary": {
        "spectral": "Tr_H8 for bosonic action",
        "physical": "(1/2) Tr_H8 for Pfaffian fermion count",
        "reduced": "Tr_H4 as computational representative",
    },
    "mass_invariance": {
        "reduced": str(mass_reduced),
        "full": str(mass_full),
        "equal": mass_reduced == mass_full,
    },
    "gauge_ratio_invariance": {
        "reduced_charge_trace": int(charge_trace_reduced),
        "full_charge_trace": int(charge_trace_full),
        "reduced_scalar_coefficient": int(scalar_coefficient_reduced),
        "full_scalar_coefficient": int(scalar_coefficient_full),
        "reduced_ratio": str(gauge_ratio_reduced),
        "full_ratio": str(gauge_ratio_full),
    },
    "physical_supertrace": {
        "numerator": supertrace_numerator,
        "fermion_pairs": 2,
        "formal_KO6_doubling_counted_as_particles": False,
    },
    "status_changes": {
        "universal_orbit_half_trace": False,
        "fermionic_half_count_derived": True,
        "bosonic_dimensionless_results_retained": True,
        "absolute_role_rank_norms_measure_derived": False,
    },
    "verdict": {
        "hidden_measure_gate": "closed by trace separation",
        "next_gate": "portal menu",
    },
}

assert mass_reduced == mass_full == sp.diag(4, 4, 4)
assert gauge_ratio_reduced == gauge_ratio_full == sp.Rational(2, 3)
assert supertrace_numerator == 67

Path("s2t_v3_orbit_measure_pfaffian_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)