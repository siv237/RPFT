#!/usr/bin/env python3
"""Exact fork audit for the oriented height--Hodge selector."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_nonordinary_architecture_fork_gate_results.json"

x, y = sp.symbols("x y", real=True)
h = sp.diag(-1, 0, 1)
d = sp.Matrix([[0, 0, 0], [x, 0, 0], [0, y, 0]])
D = d + d.T

extracted_d = sp.simplify((D + h * D - D * h) / 2)
assert extracted_d == d

hodge = sp.simplify(d * d.T - d.T * d)
expected_hodge = sp.diag(-x**2, x**2 - y**2, y**2)
assert hodge == expected_hodge

projector = sp.eye(3) - h**2
assert projector == sp.diag(0, 1, 0)
selected_action = sp.simplify(sp.trace(projector * hodge**2))
assert sp.expand(selected_action - (x**2 - y**2) ** 2) == 0

h_reversed = -h
d_reversed = sp.simplify((D + h_reversed * D - D * h_reversed) / 2)
hodge_reversed = sp.simplify(d_reversed * d_reversed.T - d_reversed.T * d_reversed)
reversed_action = sp.simplify(sp.trace((sp.eye(3) - h_reversed**2) * hodge_reversed**2))
assert sp.simplify(reversed_action - selected_action) == 0

a, b, z = sp.symbols("a b z")
selector_polynomial = a + b * z
selector_solution = sp.solve(
    [sp.Eq(selector_polynomial.subs(z, 0), 1), sp.Eq(selector_polynomial.subs(z, 1), 0)],
    [a, b],
    dict=True,
)
assert selector_solution == [{a: 1, b: -1}]

X = sp.Matrix([[1, 2], [0, 1]])
Y = sp.Matrix([[2, 0], [1, 1]])
zero = sp.zeros(2)
d_matrix = zero.row_join(zero).row_join(zero)
d_matrix = d_matrix.col_join(X.row_join(zero).row_join(zero))
d_matrix = d_matrix.col_join(zero.row_join(Y).row_join(zero))
h_matrix = sp.diag(-1, -1, 0, 0, 1, 1)
P_matrix = sp.eye(6) - h_matrix**2
K_matrix = d_matrix * d_matrix.T - d_matrix.T * d_matrix
matrix_action = sp.trace(P_matrix * K_matrix**2)
matrix_target = sp.trace((X * X.T - Y.T * Y) ** 2)
assert sp.simplify(matrix_action - matrix_target) == 0

routes = {
    "ordinary_mapping_cone": {
        "previously_closed": True,
        "exact_target": False,
        "eligible": False,
    },
    "real_or_standard_bv_auxiliary": {
        "previously_closed": True,
        "exact_target": False,
        "eligible": False,
    },
    "imaginary_hs_current_ko6_measure": {
        "previously_closed": True,
        "exact_target": "formal_only",
        "eligible": False,
    },
    "twisted_spectral_calculus": {
        "previously_closed": False,
        "exact_target": False,
        "eligible": True,
        "readiness": 2,
    },
    "derived_or_bv_bfv": {
        "previously_closed": False,
        "exact_target": "abstract_only",
        "eligible": True,
        "readiness": 1,
    },
    "relative_modular": {
        "previously_closed": False,
        "exact_target": False,
        "eligible": True,
        "readiness": 1,
    },
    "oriented_height_hodge": {
        "previously_closed": False,
        "exact_target": True,
        "coefficient_free_selector": True,
        "reuses_existing_ko6_chain": True,
        "eligible": True,
        "readiness": 4,
    },
}

eligible = [name for name, data in routes.items() if data.get("eligible")]
selected = max(eligible, key=lambda name: routes[name].get("readiness", 0))
assert selected == "oriented_height_hodge"

result = {
    "date": "2026-08-15",
    "gate": "version5_nonordinary_architecture_fork_gate",
    "height_hodge_identity": {
        "height": str(h),
        "oriented_differential_extracted": extracted_d == d,
        "hodge_commutator": str(hodge),
        "middle_projector": str(projector),
        "selected_action": str(selected_action),
        "target": str((x**2 - y**2) ** 2),
        "global_height_reversal_invariant": True,
        "unique_affine_selector": {"a": "1", "b": "-1"},
        "matrix_identity_exact": True,
        "matrix_action": str(matrix_action),
    },
    "routes": routes,
    "selected_architecture": selected,
    "selection_scope": "next kill-test only",
    "unresolved": [
        "unique height origin in full KO6 real geometry",
        "particle-conjugate compatibility",
        "common kinetic and curvature trace normalization",
        "classical parent interpretation",
        "full Hessian and exact-one BdG kernel",
    ],
    "verdict": {
        "algebraic_orientation_selector": "pass",
        "parent_architecture": "not_passed",
        "physical_closure": False,
    },
    "next_gate": "version5_oriented_height_hodge_ko6_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))