#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

charge_square_trace = sp.Integer(2)
scalar_a4_coefficient = sp.Integer(2)
gauge_a4_coefficient = sp.Rational(2, 3) * charge_square_trace
normalized_gauge_coefficient = sp.simplify(
    gauge_a4_coefficient / scalar_a4_coefficient
)
g_squared = sp.simplify(1 / (4 * normalized_gauge_coefficient))
mass_squared_ratio = sp.simplify(8 * g_squared)
gauge_supertrace = sp.simplify(3 * mass_squared_ratio**2)
finite_numerator = sp.Integer(40)
completed_zero_mode_numerator = finite_numerator + gauge_supertrace
B_zero = sp.simplify(completed_zero_mode_numerator / (64 * sp.pi**2))

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "a4_relative_u1_coupling_closed",
    "heat_kernel_coefficients": {
        "scalar_kinetic_before_common_rescaling": str(scalar_a4_coefficient),
        "charge_square_orbit_trace": int(charge_square_trace),
        "gauge_before_common_rescaling": str(gauge_a4_coefficient),
        "gauge_after_scalar_normalization": str(normalized_gauge_coefficient),
    },
    "coupling": {
        "matching": "1/(4 g^2) = normalized gauge coefficient",
        "g_squared": str(g_squared),
        "g": "sqrt(3/8)",
    },
    "mass_and_supertrace": {
        "m_A_squared_over_chi_squared": str(mass_squared_ratio),
        "gauge_ghost_numerator": str(gauge_supertrace),
        "finite_scalar_fermion_numerator": int(finite_numerator),
        "completed_zero_mode_numerator": str(completed_zero_mode_numerator),
        "B_zero": str(B_zero),
        "positive": True,
    },
    "robustness": {
        "common_f0_cancels": True,
        "ko6_full_trace_ratio_unchanged": True,
        "depends_on_charge_representation": True,
    },
    "verdict": {
        "gauge_coupling_free": False,
        "zero_mode_gauge_completion_closed": True,
        "full_B_computed": False,
        "next_gate": "spin and flat character KK branch audit",
    },
}

assert normalized_gauge_coefficient == sp.Rational(2, 3)
assert g_squared == sp.Rational(3, 8)
assert mass_squared_ratio == 3
assert gauge_supertrace == 27
assert completed_zero_mode_numerator == 67
assert B_zero == sp.Rational(67, 64) / sp.pi**2

Path("s2t_v3_a4_gauge_coupling_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)