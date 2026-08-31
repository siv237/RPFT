#!/usr/bin/env python3
"""Exact audit of candidate normalizations for the central gap coefficient."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_coefficient_selector_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_parent_action_origin_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_coefficient_selector_gate"
    assert previous["verdict"]["central_gap_direction_conditionally_unique"]

    identity = sp.eye(4)
    p3 = sp.diag(0, 1, 1, 1)
    q = p3 - sp.Rational(3, 4) * identity
    assert sp.trace(q) == 0

    hs_norm_sq = sp.trace(q.T * q)
    op_norm = max(abs(value) for value in q.eigenvals())
    trace_norm = sum(abs(value) * multiplicity for value, multiplicity in q.eigenvals().items())
    counting_variance = hs_norm_sq / 4
    assert hs_norm_sq == sp.Rational(3, 4)
    assert op_norm == sp.Rational(3, 4)
    assert trace_norm == sp.Rational(3, 2)
    assert counting_variance == sp.Rational(3, 16)

    candidates = {
        "projector_gap": sp.Integer(1),
        "grading_or_casimir_gap": sp.Integer(2),
        "HS_unit": 1 / sp.sqrt(hs_norm_sq),
        "operator_unit": 1 / op_norm,
        "trace_norm_unit": 1 / trace_norm,
        "counting_variance_unit": 1 / sp.sqrt(counting_variance),
    }
    expected = {
        "projector_gap": sp.Integer(1),
        "grading_or_casimir_gap": sp.Integer(2),
        "HS_unit": 2 / sp.sqrt(3),
        "operator_unit": sp.Rational(4, 3),
        "trace_norm_unit": sp.Rational(2, 3),
        "counting_variance_unit": 4 / sp.sqrt(3),
    }
    assert all(sp.simplify(candidates[key] - value) == 0 for key, value in expected.items())
    assert len({sp.srepr(sp.simplify(value)) for value in candidates.values()}) == 6

    shift = sp.symbols("b", real=True)
    assert sp.simplify(sp.trace((q + shift * identity) ** 2) - (4 * shift**2 + hs_norm_sq)) == 0

    lam, a, quartic = sp.symbols("lambda a b4", real=True)
    potential = a * lam**2 / 2 + quartic * lam**4 / 4
    derivative = sp.factor(sp.diff(potential, lam))
    hessian = sp.diff(potential, lam, 2)
    assert derivative == lam * (a + quartic * lam**2)
    assert sp.simplify(hessian.subs({a: -1, quartic: 1, lam: 1})) == 2
    assert sp.simplify(hessian.subs({a: -4, quartic: 1, lam: 2})) == 8
    assert sp.simplify(potential.subs({a: -1, quartic: 1, lam: 1}) - potential.subs({a: -1, quartic: 1, lam: -1})) == 0

    beta = sp.symbols("beta", positive=True)
    theta = beta * lam
    p = sp.simplify(1 / (1 + 3 * sp.exp(-theta)))
    assert sp.simplify(p.subs(lam, 0) - sp.Rational(1, 4)) == 0

    exact_objects = [identity, p3, q]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_coefficient_selector_gate",
        "central_direction_invariants": {
            "Q": "P3 - 3 I4/4",
            "trace_Q2": "3/4",
            "operator_norm": "3/4",
            "trace_norm": "3/2",
            "counting_trace_variance": "3/16",
        },
        "normalization_candidates": {
            "projector_gap": 1,
            "grading_or_casimir_gap": 2,
            "HS_unit_gap": "2/sqrt(3)",
            "operator_unit_gap": "4/3",
            "trace_norm_unit_gap": "2/3",
            "counting_variance_unit_gap": "4/sqrt(3)",
            "distinct_values": 6,
        },
        "shift_dependence": {
            "uncentered_HS_norm_squared": "4 b^2 + 3/4",
            "norm_requires_centering_convention": True,
        },
        "even_parent_potential": {
            "potential": "a lambda^2/2 + b4 lambda^4/4",
            "stationarity": "lambda(a+b4 lambda^2)=0",
            "stable_witness_1": {"a": -1, "b4": 1, "minima": ["-1", "1"], "hessian": 2},
            "stable_witness_2": {"a": -4, "b4": 1, "minima": ["-2", "2"], "hessian": 8},
            "magnitude_selected_without_coefficients": False,
            "sign_selected": False,
        },
        "thermal_and_entropy_candidates": {
            "maximum_entropy": "lambda=0 at fixed beta",
            "equal_sector_weight": "beta lambda=log(3)",
            "KMS_observed_ratio": "beta lambda=-log(r)",
            "select_lambda_without_beta_or_target": False,
        },
        "selector_ledger": {
            "projector_normalization": False,
            "grading_normalization": False,
            "Casimir_normalization": False,
            "HS_normalization": False,
            "operator_normalization": False,
            "counting_variance_normalization": False,
            "even_parent_potential": False,
            "entropy_or_KMS_target": False,
            "derived_selectors": 0,
            "tested_selectors": 8,
        },
        "verdict": {
            "coefficient_selected": False,
            "sign_selected": False,
            "normalization_is_coordinate_choice": True,
            "minimal_missing_parent_structure": "odd central source plus even stiffness",
            "theta_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_minimal_source_parent_architecture_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()