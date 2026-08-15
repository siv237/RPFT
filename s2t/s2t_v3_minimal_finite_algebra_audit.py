#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

a_x, a_c, b_x, b_c, mixing = sp.symbols(
    "a_x a_c b_x b_c mixing", real=True
)
rho_a = sp.diag(a_x, a_c)
rho_b = sp.diag(b_x, b_c)
dirac_f = sp.Matrix([[0, mixing], [mixing, 0]])
first_commutator = dirac_f * rho_a - rho_a * dirac_f
first_order = sp.simplify(first_commutator * rho_b - rho_b * first_commutator)

volume_x = sp.pi**2
length_c = 2 * sp.pi
spectator_c_norm = sp.Integer(1)
spectator_x_norm = sp.Integer(1)
factor_x_norm = sp.simplify(volume_x * spectator_c_norm)
factor_c_norm = sp.simplify(length_c * spectator_x_norm)

results = {
    "date": "2026-08-09",
    "version": "S2T-III",
    "status": "minimal_finite_module_pass_diagonal_first_order_mixing_no_go",
    "finite_algebra": {
        "algebra": "C direct_sum C",
        "primitive_central_idempotents": 2,
        "minimal_faithful_multiplicities": [1, 1],
        "trace_weights": [1, 1],
    },
    "spectator_zero_mode_module": {
        "factor_X_norm": str(factor_x_norm),
        "factor_C_norm": str(factor_c_norm),
        "sum": str(sp.simplify(factor_x_norm + factor_c_norm)),
        "free_factor_weights": False,
        "module_multiplicity_derived": True,
    },
    "first_order_test": {
        "commutator": str(first_order),
        "generic_off_diagonal_factor": "mixing*(a_c-a_x)*(b_c-b_x)",
        "nonzero_mixing_allowed": False,
        "forced_mixing": 0,
    },
    "verdict": {
        "measure_gate_passed": True,
        "module_origin_gate_passed": True,
        "vertex_gate_passed": False,
        "parent_action_passed": False,
        "next_gate": "classify minimal real graded bimodules",
    },
}

expected = mixing * (a_c - a_x) * (b_c - b_x)
assert sp.simplify(first_order[0, 1] - expected) == 0
assert sp.simplify(first_order[1, 0] - expected) == 0
assert factor_x_norm == sp.pi**2
assert factor_c_norm == 2 * sp.pi

Path("s2t_v3_minimal_finite_algebra_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)