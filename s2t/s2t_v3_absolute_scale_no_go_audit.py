#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

scale, radius, mass = sp.symbols("scale radius mass", positive=True)
dimension, form_degree = sp.symbols(
    "dimension form_degree", integer=True, nonnegative=True
)
A, B = sp.symbols("A B", positive=True)

scaled_radius = scale * radius
scaled_mass = mass / scale
dimensionless_product = sp.simplify(scaled_radius * scaled_mass)
p_form_norm_exponent = dimension - 2 * form_degree

radion_potential = A * radius + B / radius
radion_stationary = sp.solve(
    sp.Eq(sp.diff(radion_potential, radius), 0), radius
)[0]
radion_hessian = sp.simplify(
    sp.diff(radion_potential, radius, 2).subs(radius, radion_stationary)
)

results = {
    "date": "2026-08-10",
    "version": "S2T-III",
    "status": "absolute_scale_no_go_dimensionless_program_open",
    "homothety": {
        "metric": "g -> lambda^2 g",
        "length": "L -> lambda L",
        "volume_d": "Vol_d -> lambda^d Vol_d",
        "laplacian": "Delta -> lambda^-2 Delta",
        "dirac": "D -> lambda^-1 D",
        "p_form_norm_squared_exponent": str(p_form_norm_exponent),
    },
    "dimensionless_invariant": {
        "scaled_MR": str(dimensionless_product),
        "equals_original_MR": bool(dimensionless_product == mass * radius),
        "absolute_M_fixed": False,
        "absolute_R_fixed": False,
    },
    "spectral_action": {
        "functional": "Tr f(D/Lambda)",
        "D_and_Lambda_common_rescaling_invariant": True,
        "Lambda_dynamically_derived": False,
    },
    "two_term_radion_example": {
        "potential": "A*R+B/R",
        "stationary_radius": str(radion_stationary),
        "hessian_at_stationary": str(radion_hessian),
        "depends_on_coefficient_ratio": True,
        "R_equals_one_requires_A_equals_B": True,
    },
    "verdict": {
        "topology_fixes_absolute_scale": False,
        "normalized_geometry_fixes_absolute_scale": False,
        "dimensionless_predictions_allowed": True,
        "absolute_mass_predictions_allowed": False,
        "next_gate": "dilaton-radion action or dimensionless blind protocol",
    },
}

assert dimensionless_product == mass * radius
assert radion_stationary == sp.sqrt(B) / sp.sqrt(A)
assert radion_hessian > 0

Path("s2t_v3_absolute_scale_no_go_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)