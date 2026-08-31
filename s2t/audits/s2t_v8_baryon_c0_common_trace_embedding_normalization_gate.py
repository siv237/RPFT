#!/usr/bin/env python3
"""Exact direct-sum common-trace normalization audit for c0."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_common_trace_embedding_normalization_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_minimal_cross_carrier_morphism_architecture_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["verdict"]["normalization_defect_dimension"] == 1
    assert previous["next_gate"] == "version8_baryon_c0_common_trace_embedding_normalization_gate"

    p, q, kappa = sp.symbols("p q kappa", positive=True)
    equation = sp.Eq(q * kappa**2, p)
    positive_solution = sp.solve(equation, kappa)
    assert positive_solution == [sp.sqrt(p / q)]

    witnesses = [
        (sp.Rational(1, 2), sp.Rational(1, 2)),
        (sp.Rational(4, 5), sp.Rational(1, 5)),
    ]
    kappas = [sp.simplify(sp.sqrt(pv / qv)) for pv, qv in witnesses]
    assert kappas == [1, 2]
    assert all(sp.simplify(pv + qv) == 1 for pv, qv in witnesses)
    assert all(pv > 0 and qv > 0 for pv, qv in witnesses)

    center_weight_matrix = sp.Matrix([[p, 0], [0, q]])
    assert center_weight_matrix.rank() == 2
    exact_objects = [equation.lhs, equation.rhs, *kappas, *center_weight_matrix]
    assert not any(
        atom.is_Float for obj in exact_objects for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_common_trace_embedding_normalization_gate",
        "separated_algebra": "A_src direct_sum A_aux",
        "normalized_trace_family": {
            "definition": "tau_pq=p*tau_src+q*tau_aux",
            "conditions": "p>0, q>0, p+q=1",
            "simplex_dimension": 1,
        },
        "line_metrics": {
            "G_src": "p",
            "G_aux": "q",
            "pullback_isometry": "q*kappa^2=p",
            "positive_kappa": "sqrt(p/q)",
        },
        "exact_witnesses": [
            {"p": "1/2", "q": "1/2", "kappa": "1"},
            {"p": "4/5", "q": "1/5", "kappa": "2"},
        ],
        "linking_requirement": {
            "off_diagonal_bimodule_required": True,
            "current_auxiliary_carrier_in_common_simple_block": False,
            "equal_central_weights_derived": False,
        },
        "verdict": {
            "common_trace_exists": True,
            "common_trace_alone_selects_kappa": False,
            "c0_selected": False,
            "direct_sum_common_trace_no_go": True,
        },
        "next_gate": "version8_baryon_c0_linking_algebra_offdiagonal_bridge_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()