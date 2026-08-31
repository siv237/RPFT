#!/usr/bin/env python3
"""Exact parent-origin audit for the central-gap source and stiffness."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_source_stiffness_parent_origin_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_minimal_source_parent_architecture_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_source_stiffness_parent_origin_gate"
    assert previous["verdict"]["minimal_architecture_conditionally_admitted"]

    gap_origin = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_parent_action_origin_gate_results.json").read_text(encoding="utf-8")
    )
    assert not gap_origin["architectural_status"]["current_parent_contains_new_triplet_state"]
    assert not gap_origin["architectural_status"]["current_parent_contains_covariant_M3_endpoint"]
    assert not gap_origin["architectural_status"]["current_parent_contains_family_SO3_action"]

    identity = sp.eye(4)
    p1 = sp.diag(1, 0, 0, 0)
    p3 = identity - p1
    q = p3 - sp.Rational(3, 4) * identity
    gamma = sp.diag(-1, 1, 1, 1)
    gamma0 = gamma - sp.trace(gamma) * identity / 4
    casimir = 2 * p3
    casimir0 = casimir - sp.trace(casimir) * identity / 4
    assert gamma0 == 2 * q
    assert casimir0 == 2 * q
    assert sp.trace(q) == 0
    assert sp.trace(q.T * q) == sp.Rational(3, 4)

    lam, eps = sp.symbols("lambda epsilon", real=True)
    h = eps * identity + lam * q
    first_derivatives = {}
    second_derivatives = {}
    for degree in range(1, 7):
        moment = sp.expand(sp.trace(h**degree))
        first = sp.simplify(sp.diff(moment, lam).subs(lam, 0))
        second = sp.simplify(sp.diff(moment, lam, 2).subs(lam, 0))
        assert first == 0
        expected_second = sp.Rational(3, 4) * degree * (degree - 1) * eps ** (degree - 2) if degree >= 2 else 0
        assert sp.simplify(second - expected_second) == 0
        first_derivatives[str(degree)] = str(first)
        second_derivatives[str(degree)] = str(second)

    coefficients = sp.symbols("a1:7", real=True)
    spectral_polynomial = sum(coefficients[n - 1] * sp.trace(h**n) for n in range(1, 7))
    assert sp.simplify(sp.diff(spectral_polynomial, lam).subs(lam, 0)) == 0
    origin_curvature = sp.simplify(sp.diff(spectral_polynomial, lam, 2).subs({lam: 0, eps: 0}))
    assert origin_curvature == sp.Rational(3, 2) * coefficients[1]

    h0 = lam * q
    ordinary_linear = sp.trace(h0)
    grading_linear = sp.expand(sp.trace(gamma0 * h0))
    casimir_linear = sp.expand(sp.trace(casimir0 * h0))
    assert ordinary_linear == 0
    assert grading_linear == sp.Rational(3, 2) * lam
    assert casimir_linear == grading_linear

    a2, g = sp.symbols("a2 g", real=True)
    conditional_parent = a2 * sp.trace(h0**2) - g * sp.trace(gamma0 * h0)
    conditional_pullback = sp.expand(conditional_parent)
    assert conditional_pullback == sp.Rational(3, 4) * a2 * lam**2 - sp.Rational(3, 2) * g * lam
    m2_from_a2 = sp.Rational(3, 2) * a2
    j_from_g = sp.Rational(3, 2) * g

    witness_1 = {a2: sp.Rational(2, 3), g: sp.Rational(2, 3)}
    witness_2 = {a2: sp.Rational(4, 3), g: sp.Rational(4, 3)}
    assert m2_from_a2.subs(witness_1) == 1 and j_from_g.subs(witness_1) == 1
    assert m2_from_a2.subs(witness_2) == 2 and j_from_g.subs(witness_2) == 2

    exact_objects = [q, gamma0, casimir0, spectral_polynomial, conditional_pullback]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_source_stiffness_parent_origin_gate",
        "current_parent_restriction": {
            "contains_new_triplet_state": False,
            "contains_covariant_M3_endpoint": False,
            "contains_family_SO3_action": False,
            "central_source_j": 0,
            "central_stiffness_m2": 0,
        },
        "unmarked_trace_audit": {
            "background": "epsilon I4",
            "direction": "Q=P3-3 I4/4",
            "trace_Q": 0,
            "tested_moment_degrees": [1, 2, 3, 4, 5, 6],
            "first_derivatives_at_lambda_zero": first_derivatives,
            "all_linear_terms_zero": True,
            "second_derivatives_at_lambda_zero": second_derivatives,
            "origin_curvature_for_sum_a_n_Tr_h_n": "3 a2/2",
            "stiffness_coefficient_selected": False,
        },
        "marked_trace_audit": {
            "centered_grading": "2 Q",
            "centered_casimir": "2 Q",
            "grading_linear_response": "3 lambda/2",
            "casimir_linear_response": "3 lambda/2",
            "independent_source_directions": 1,
            "marks_belong_to_current_parent": False,
            "insertion_coefficient_selected": False,
        },
        "conditional_implementation": {
            "functional": "a2 Tr(h0^2)-g Tr(Gamma0 h0)",
            "pullback": "3 a2 lambda^2/4-3 g lambda/2",
            "m2": "3 a2/2",
            "j": "3 g/2",
            "source_shape_realized": True,
            "stiffness_shape_realized": True,
            "shape_ledger": "2/2",
            "same_vacuum_witnesses": [
                {"a2": "2/3", "g": "2/3", "m2": 1, "j": 1, "lambda_star": 1},
                {"a2": "4/3", "g": "4/3", "m2": 2, "j": 2, "lambda_star": 1},
            ],
        },
        "typed_obstructions": {
            "KMS_selects_action_coefficients": False,
            "noise_42_hessian_has_canonical_pullback_to_new_central_line": False,
            "scalar_background_creates_source": False,
            "nonzero_Q_background_would_be_circular": True,
        },
        "parent_origin_ledger": {
            "old_parent_restriction": False,
            "unmarked_linear_trace": False,
            "scalar_background_spectral_trace": False,
            "quadratic_trace_fixed_coefficient": False,
            "grading_marked_trace": False,
            "casimir_marked_trace": False,
            "KMS_or_target": False,
            "noise_hessian_pullback": False,
            "derived_channels": 0,
            "tested_channels": 8,
        },
        "verdict": {
            "source_and_stiffness_shapes_conditionally_available": True,
            "source_j_derived_by_current_parent": False,
            "stiffness_m2_derived_by_current_parent": False,
            "current_parent_realizes_minimal_architecture": False,
            "minimal_next_structure": "dynamical Real scalar source carrier with a derived nonzero expectation",
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_dynamical_source_carrier_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()