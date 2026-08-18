#!/usr/bin/env python3
"""Symbolic spectral-vacuum audit for the active-family rectangle."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_family_algebra_rectangle_gate_results.json"

y, z = sp.symbols("y z", real=True)
v = sp.Matrix(sp.symbols("v0:3", real=True))
w = sp.Matrix(sp.symbols("w0:3", real=True))
variables = [y, z, *list(v), *list(w)]

M = sp.zeros(4)
for i in range(3):
    M[i, i] = y
    M[i, 3] = w[i]
    M[3, i] = v[i]
M[3, 3] = z

Q = M * M.T
tr_d2 = sp.expand(2 * sp.trace(Q))
tr_d4 = sp.expand(2 * sp.trace(Q * Q))

mu2 = sp.Integer(2)
lam = sp.Integer(1)
potential = sp.expand(-mu2 * tr_d2 + lam * tr_d4)
vacuum = {y: 1, z: 1, **{entry: 0 for entry in list(v) + list(w)}}

gradient = sp.Matrix([sp.diff(potential, variable) for variable in variables])
assert gradient.subs(vacuum) == sp.zeros(8, 1)

hessian = sp.hessian(potential, variables).subs(vacuum)
hessian_eigenvalues = sorted(
    [int(value) for value, multiplicity in hessian.eigenvals().items() for _ in range(multiplicity)]
)
assert hessian_eigenvalues == [0, 0, 0, 16, 16, 16, 16, 48]

t = sp.symbols("t", real=True)
flat_substitution = {
    y: 1,
    z: 1,
    v[0]: t,
    v[1]: 0,
    v[2]: 0,
    w[0]: -t,
    w[1]: 0,
    w[2]: 0,
}
flat_delta = sp.factor(potential.subs(flat_substitution) - potential.subs(vacuum))
assert flat_delta == 4 * t**4

r2 = sp.symbols("r2", positive=True)
square_identity_residual = sp.expand(
    2 * lam * sp.trace((Q - r2 * sp.eye(4)) ** 2)
    - (lam * tr_d4 - 4 * lam * r2 * sp.trace(Q) + 8 * lam * r2**2)
)
assert square_identity_residual == 0

result = {
    "date": "2026-08-15",
    "gate": "version5_family_algebra_rectangle_gate",
    "particle_matrix_dimension": 8,
    "offdiagonal_block": "M=[[y I3,w],[v^T,z]]",
    "trace_D2": str(tr_d2),
    "trace_D4": str(tr_d4),
    "square_completion_identity": True,
    "global_minimum_rank_argument": {
        "upper_left_block": "|y|^2 I3 + w w^T",
        "rank_one_cannot_equal_nonzero_scalar_I3": True,
        "w": 0,
        "v": 0,
        "abs_y_equals_abs_z_equals_r": True,
    },
    "normalized_vacuum": {
        "mu_squared": 2,
        "lambda": 1,
        "y": 1,
        "z": 1,
        "v": [0, 0, 0],
        "w": [0, 0, 0],
    },
    "hessian_eigenvalues": hessian_eigenvalues,
    "flat_direction": {
        "condition": "v=-w",
        "multiplicity": 3,
        "potential_difference": str(flat_delta),
        "condenses": False,
    },
    "verdict": {
        "order_one_rectangle": "pass",
        "family_commutant_scalar": "pass",
        "loop_sensitive_quartic": "pass",
        "nonzero_triplet_vacuum": "fail",
        "family_gauge_breaking": "fail",
        "standard_finite_geometry_budget_route": "closed",
        "mathematical_parent_architecture_pass": False,
        "physical_closure": False,
    },
    "next_gate": "version5_nonordinary_architecture_fork_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))