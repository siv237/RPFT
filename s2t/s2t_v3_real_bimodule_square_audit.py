#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

labels = [(1, 1), (1, 2), (2, 1), (2, 2)]
allowed_edges = []
for index, source in enumerate(labels):
    for target in labels[index + 1 :]:
        if source[0] == target[0] or source[1] == target[1]:
            allowed_edges.append((source, target))

expected_edges = [
    ((1, 1), (1, 2)),
    ((1, 1), (2, 1)),
    ((1, 2), (2, 2)),
    ((2, 1), (2, 2)),
]

x_real, x_imag, z_real, z_imag = sp.symbols(
    "x_real x_imag z_real z_imag", real=True
)
x = x_real + sp.I * x_imag
z = z_real + sp.I * z_imag
B = sp.Matrix([[x, sp.conjugate(x)], [sp.conjugate(z), z]])
D = sp.zeros(4)
D[:2, 2:] = B
D[2:, :2] = sp.conjugate(B.T)

grading = sp.diag(1, 1, -1, -1)
swap_negative = sp.Matrix(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ]
)

determinant_B = sp.simplify(B.det())
odd_test = sp.simplify(grading * D + D * grading)
reality_test = sp.simplify(D - swap_negative * sp.conjugate(D) * swap_negative)
J_gamma_commutator = sp.simplify(
    swap_negative * grading - grading * swap_negative
)

results = {
    "date": "2026-08-09",
    "version": "S2T-III",
    "status": "first_order_vertex_pass_KO6_doubling_and_parameter_orbit_open",
    "bimodule_classification": {
        "sectors": [str(label) for label in labels],
        "allowed_edges": [[str(a), str(b)] for a, b in allowed_edges],
        "minimal_J_stable_sector_count": 4,
        "direct_diagonal_edge_allowed": False,
    },
    "odd_operator": {
        "B": str(B),
        "determinant": str(determinant_B),
        "free_complex_parameters": 2,
        "full_rank_condition": "Im(x*z) != 0",
        "odd_grading_test": str(odd_test),
        "reality_test": str(reality_test),
    },
    "KO_gate": {
        "J_gamma_relation_on_square": "commute",
        "KO6_requires_anticommute": True,
        "undoubled_KO6_passed": False,
        "minimal_particle_antiparticle_dimension": 8,
        "physical_half_trace_derived": False,
    },
    "verdict": {
        "first_order_vertex_exists": True,
        "parameter_free_vertex": False,
        "parent_action_passed": False,
        "next_gate": "automorphism orbit and KO6 half-trace",
    },
}

assert allowed_edges == expected_edges
assert odd_test == sp.zeros(4)
assert reality_test == sp.zeros(4)
assert J_gamma_commutator == sp.zeros(4)
assert sp.simplify(
    determinant_B - 2 * sp.I * sp.im(x * z)
) == 0

Path("s2t_v3_real_bimodule_square_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)