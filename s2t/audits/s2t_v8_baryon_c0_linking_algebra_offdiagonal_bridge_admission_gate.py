#!/usr/bin/env python3
"""Exact minimal M2 linking-bridge admission audit for c0."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_linking_algebra_offdiagonal_bridge_admission_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_common_trace_embedding_normalization_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["verdict"]["direct_sum_common_trace_no_go"]
    assert previous["next_gate"] == "version8_baryon_c0_linking_algebra_offdiagonal_bridge_admission_gate"

    ps = sp.Matrix([[1, 0], [0, 0]])
    pa = sp.Matrix([[0, 0], [0, 1]])
    e = sp.Matrix([[0, 1], [0, 0]])
    assert e * e.T == ps
    assert e.T * e == pa
    assert ps * e == e == e * pa

    basis = [ps, pa, e, e.T]
    flattened = sp.Matrix.hstack(*[x.reshape(4, 1) for x in basis])
    assert flattened.rank() == 4
    assert sp.trace(ps) / 2 == sp.Rational(1, 2)
    assert sp.trace(pa) / 2 == sp.Rational(1, 2)

    kappa = sp.symbols("kappa", positive=True)
    isometry = sp.Eq(sp.Rational(1, 2) * kappa**2, sp.Rational(1, 2))
    assert sp.solve(isometry, kappa) == [1]

    h = sp.symbols("h", positive=True)
    eh = h * e
    assert eh * eh.T == h**2 * ps
    assert eh.T * eh == h**2 * pa
    assert sp.solve(sp.Eq(h**2, 1), h) == [1]

    r_star = sp.Integer(4)
    c0 = sp.simplify(r_star * sp.Integer(1))
    assert c0 == 4
    exact_objects = [*ps, *pa, *e, *flattened, isometry.lhs, isometry.rhs, *eh, c0]
    assert not any(
        atom.is_Float for obj in exact_objects for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_linking_algebra_offdiagonal_bridge_admission_gate",
        "minimal_linking_block": {
            "algebra": "M2(C)",
            "source_corner": "P_s=diag(1,0)",
            "auxiliary_corner": "P_a=diag(0,1)",
            "bridge": "E_12",
            "generated_vector_space_rank": 4,
            "center_dimension": 1,
        },
        "imprimitivity": {
            "E_E_star": "P_s",
            "E_star_E": "P_a",
            "scaled_bridge_requires_h_squared": "1",
            "positive_h": 1,
        },
        "trace_normalization": {
            "unique_normalized_matrix_trace": True,
            "source_corner_weight": "1/2",
            "auxiliary_corner_weight": "1/2",
            "positive_isometric_kappa": 1,
        },
        "conditional_c0": {
            "source_invariant_r_star": 4,
            "c0": 4,
            "derived_in_existing_42_carrier": False,
        },
        "verdict": {
            "minimal_linking_architecture_admitted": True,
            "central_trace_weight_freedom_removed": True,
            "existing_bridge_origin_open": True,
            "physical_c0_derived": False,
        },
        "next_gate": "version8_baryon_c0_existing_42_carrier_linking_bridge_classification_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()