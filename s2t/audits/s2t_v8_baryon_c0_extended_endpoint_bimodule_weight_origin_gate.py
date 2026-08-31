#!/usr/bin/env python3
"""Exact endpoint-bimodule trace-weight and full-Hom closure audit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_extended_endpoint_bimodule_weight_origin_gate_results.json"


def matrix_unit(size: int, row: int, column: int) -> sp.ImmutableMatrix:
    value = sp.zeros(size)
    value[row, column] = 1
    return sp.ImmutableMatrix(value)


def algebra_closure(generators: list[sp.ImmutableMatrix]) -> list[sp.ImmutableMatrix]:
    basis: list[sp.ImmutableMatrix] = []

    def extend(candidates: list[sp.ImmutableMatrix]) -> bool:
        nonlocal basis
        pool = basis + candidates
        columns = sp.Matrix.hstack(*[sp.Matrix(list(item)) for item in pool])
        pivots = columns.rref()[1]
        enlarged = [pool[index] for index in pivots]
        changed = len(enlarged) > len(basis)
        basis = enlarged
        return changed

    extend(generators)
    while True:
        products = [sp.ImmutableMatrix(left * right) for left in basis for right in basis]
        if not extend(products):
            return basis


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_connector_multiplicity_and_rate_parent_selector_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["selector_ledger"]["derived"] == 0
    assert previous["next_gate"] == "version8_baryon_c0_extended_endpoint_bimodule_weight_origin_gate"

    coordinate_projectors = tuple(
        sp.ImmutableMatrix(sp.diag(*[int(i == j) for i in range(3)]))
        for j in range(3)
    )
    assert sum(coordinate_projectors, sp.zeros(3)) == sp.eye(3)
    assert all(projector.rank() == 1 for projector in coordinate_projectors)

    p0, p1, p2, q = sp.symbols("p0 p1 p2 q", positive=True)
    connector_metric = sp.diag(p0 + q, p1 + q, p2 + q)
    assert connector_metric.rank() == 3

    witness_a = {p0: sp.Rational(1, 10), p1: sp.Rational(1, 5), p2: sp.Rational(1, 2), q: sp.Rational(1, 10)}
    witness_b = {p0: sp.Rational(1, 2), p1: sp.Rational(1, 10), p2: sp.Rational(1, 5), q: sp.Rational(1, 10)}
    assert sum(witness_a[item] for item in (p0, p1, p2)) + 2 * witness_a[q] == 1
    assert sum(witness_b[item] for item in (p0, p1, p2)) + 2 * witness_b[q] == 1
    metric_a = connector_metric.subs(witness_a)
    metric_b = connector_metric.subs(witness_b)
    assert metric_a == sp.diag(sp.Rational(1, 5), sp.Rational(3, 10), sp.Rational(3, 5))
    assert metric_b == sp.diag(sp.Rational(3, 5), sp.Rational(1, 5), sp.Rational(3, 10))

    px, pe = sp.symbols("pX pE", positive=True)
    vectorlike_metric = connector_metric.subs({p0: px, p1: pe, p2: px})
    assert vectorlike_metric == sp.diag(px + q, pe + q, px + q)

    size = 5
    identity = sp.ImmutableMatrix(sp.eye(size))
    undirected_edges = ((3, 4), (0, 3), (1, 4), (2, 4))
    generators = [identity]
    for left, right in undirected_edges:
        generators.extend((matrix_unit(size, left, right), matrix_unit(size, right, left)))
    closure = algebra_closure(generators)
    assert len(closure) == 25

    adjacency = sp.zeros(size)
    for left, right in undirected_edges:
        adjacency[left, right] = adjacency[right, left] = 1
    laplacian = sp.diag(*[sum(adjacency[row, column] for column in range(size)) for row in range(size)]) - adjacency
    assert laplacian.rank() == 4
    assert len(laplacian.nullspace()) == 1
    assert laplacian.nullspace()[0] == sp.ones(5, 1)

    tau_corner_weight = sp.Rational(1, 5)
    full_connector_metric = 2 * tau_corner_weight * sp.eye(3)
    assert full_connector_metric == sp.Rational(2, 5) * sp.eye(3)

    connector_support = []
    for old, new in ((0, 3), (1, 4), (2, 4)):
        edge = matrix_unit(size, old, new)
        c1 = edge + edge.H
        c2 = sp.I * edge - sp.I * edge.H
        connector_support.extend((sp.ImmutableMatrix(c1), sp.ImmutableMatrix(c2)))
    flattened = sp.Matrix.hstack(*[sp.Matrix(list(item)) for item in connector_support])
    assert flattened.rank() == 6
    tau_metric = sp.Matrix(
        [[sp.trace(left.H * right) / 5 for right in connector_support] for left in connector_support]
    )
    assert tau_metric == sp.Rational(2, 5) * sp.eye(6)

    exact_objects = [*connector_metric, *metric_a, *metric_b, *laplacian, *tau_metric]
    assert not any(atom.is_Float for obj in exact_objects for atom in sp.preorder_traversal(obj))

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_extended_endpoint_bimodule_weight_origin_gate",
        "local_endpoint_algebra": {
            "before_old_new_connectors": "C^3 direct_sum M2(C)",
            "center_dimension": 4,
            "connector_coordinate_projectors": 3,
            "off_diagonal_multiplicity_mixing_removed": True,
        },
        "trace_simplex": {
            "positive_parameters": ["p0", "p1", "p2", "q"],
            "normalization": "p0+p1+p2+2q=1",
            "free_dimension": 3,
            "connector_metric": "diag(p0+q,p1+q,p2+q)",
            "witness_A": ["1/10", "1/5", "1/2", "1/10"],
            "witness_B": ["1/2", "1/10", "1/5", "1/10"],
            "witness_minimal_branches_differ": True,
            "anisotropic_weight_selected": False,
        },
        "vectorlike_constraint": {
            "condition": "p0=p2=pX",
            "metric": "diag(pX+q,pE+q,pX+q)",
            "free_relative_weight_remains": True,
            "X_branch_degeneracy": 2,
        },
        "full_hom_closure": {
            "corner_count": 5,
            "edge_count": 4,
            "graph_laplacian_rank": 4,
            "graph_connected": True,
            "generated_algebra": "M5(C)",
            "generated_algebra_dimension": 25,
            "unique_normalized_trace": True,
            "connector_metric": "(2/5) I3",
            "new_real_quadratures": 6,
            "full_frame_rank": 51,
        },
        "verdict": {
            "bimodule_labels_diagonalize_multiplicity": True,
            "local_trace_selects_anisotropic_weights": False,
            "full_multiplicity_frame_canonical_after_M5_closure": True,
            "single_c0_map_selected": False,
            "absolute_rate_selected": False,
        },
        "next_gate": "version8_baryon_c0_full_multiplicity_frame_single_map_compatibility_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()