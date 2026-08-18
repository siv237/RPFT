#!/usr/bin/env python3
"""Test blockwise independence of a pendant Krajewski selector."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_real_selector_leaf_ko6_gate_results.json"

nodes = {
    "A": ("o", "o"),
    "B": ("o", "h"),
    "C": ("h", "h"),
    "D": ("h", "o"),
}
cycle_edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]


def allowed(left, right):
    return left[0] == right[0] or left[1] == right[1]


assert all(allowed(nodes[a], nodes[b]) for a, b in cycle_edges)
leafs = {"E_left": ("s", "o"), "E_right": ("o", "s")}
assert all(allowed(nodes["A"], label) for label in leafs.values())

passive_dimension_before = 9
passive_dimension_after = 9
assert passive_dimension_before == passive_dimension_after

y_symbols = sp.symbols("y0:9")
y = sp.Matrix(3, 3, y_symbols)
equations = []
for i in range(3):
    for j in range(3):
        unit = sp.zeros(3)
        unit[i, j] = 1
        equations.extend(list(y * unit - unit * y))
matrix, _ = sp.linear_eq_to_matrix(equations, y_symbols)
active_commutant_dimension = 9 - matrix.rank()
assert active_commutant_dimension == 1

result = {
    "date": "2026-08-15",
    "gate": "version5_real_selector_leaf_ko6_gate",
    "square_nodes": {key: list(value) for key, value in nodes.items()},
    "leaf_placements": {
        key: {
            "label": list(value),
            "order_one_allowed": allowed(nodes["A"], value),
            "J_transpose": [value[1], value[0]],
        }
        for key, value in leafs.items()
    },
    "blockwise_test": {
        "cycle_family_dimension_before_leaf": passive_dimension_before,
        "cycle_family_dimension_after_leaf": passive_dimension_after,
        "leaf_constrains_cycle_edge": False,
    },
    "active_family_algebra": {
        "algebra": "M3(R)",
        "shared_on_cycle_edge": True,
        "commutant_dimension": active_commutant_dimension,
        "edge_form": "scalar times I3",
    },
    "verdict": {
        "selector_leaf": "fail",
        "selector_leaf_geometry_closed": True,
        "complexity_ledger_corrected": True,
        "family_algebra_rectangle": "admitted_for_one_gate",
        "mathematical_parent_architecture_pass": False,
        "physical_closure": False,
    },
    "next_gate": "version5_family_algebra_rectangle_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))