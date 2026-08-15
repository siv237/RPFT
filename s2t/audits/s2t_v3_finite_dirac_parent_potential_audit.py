#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

r, s, phase, scale = sp.symbols(
    "r s phase scale", positive=True, real=True
)
u = r**2 + s**2
v = r**2 * s**2 * sp.sin(phase) ** 2
potential = sp.expand(8 * u**2 - 16 * v - 8 * u + 4)

variables = (r, s, phase)
minimum_plus = {
    r: 1 / sp.sqrt(2),
    s: 1 / sp.sqrt(2),
    phase: sp.pi / 2,
}
minimum_minus = {
    r: 1 / sp.sqrt(2),
    s: 1 / sp.sqrt(2),
    phase: -sp.pi / 2,
}
gradient_plus = [
    sp.simplify(sp.diff(potential, variable).subs(minimum_plus))
    for variable in variables
]
hessian_plus = sp.simplify(sp.hessian(potential, variables).subs(minimum_plus))

general_a, general_b = sp.symbols("general_a general_b", positive=True)
general_scale_u = sp.simplify(general_b / (2 * general_a))
physical_modulus = scale / sp.sqrt(2)

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "orbit_direction_selected_scale_and_CP_sign_open",
    "potential": {
        "name": "orbit_trace((D_F^2-I)^2)",
        "expression": str(potential),
        "nonnegative_by_construction": True,
        "zero_condition": "D_F^2=I",
    },
    "global_minima": {
        "abs_x": "1/sqrt(2)",
        "abs_z": "1/sqrt(2)",
        "arg_xz": ["pi/2", "-pi/2"],
        "minimum_value_plus": str(sp.simplify(potential.subs(minimum_plus))),
        "minimum_value_minus": str(sp.simplify(potential.subs(minimum_minus))),
        "gradient_plus": [str(value) for value in gradient_plus],
    },
    "stability": {
        "hessian": str(hessian_plus),
        "eigenvalues": [8, 32, 32],
        "positive_on_orbit_coordinates": True,
    },
    "generic_even_polynomial": {
        "potential": "a*Tr(D^4)-b*Tr(D^2)",
        "selected_u": str(general_scale_u),
        "equal_moduli_selected": True,
        "maximal_CP_magnitude_selected": True,
        "absolute_scale_fixed_without_ratio_b_over_a": False,
    },
    "physical_scale": {
        "dimensionful_potential": "Tr((D_F^2-M^2 I)^2)",
        "selected_edge_modulus": str(physical_modulus),
        "M_fixed_by_finite_algebra": False,
    },
    "CP_gate": {
        "two_conjugate_branches": True,
        "even_real_action_selects_sign": False,
        "orientation_odd_term_required_for_unique_sign": True,
    },
    "verdict": {
        "continuous_direction_orbit_closed": True,
        "scale_gate_closed": False,
        "CP_sign_gate_closed": False,
        "parent_action_passed": False,
        "next_gate": "geometric scale and orientation-odd selector",
    },
}

assert sp.simplify(potential.subs(minimum_plus)) == 0
assert sp.simplify(potential.subs(minimum_minus)) == 0
assert gradient_plus == [0, 0, 0]
assert hessian_plus == sp.diag(32, 32, 8)

Path("s2t_v3_finite_dirac_parent_potential_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)