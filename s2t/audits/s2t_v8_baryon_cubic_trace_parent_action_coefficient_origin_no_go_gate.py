#!/usr/bin/env python3
"""Exact no-go audit for the coefficient of the cubic trace carrier."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_cubic_trace_parent_action_coefficient_origin_no_go_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_full_noise_trace_frame import (  # noqa: E402
    full_noise_frame,
)


def main() -> None:
    alpha, beta = sp.symbols("alpha beta", positive=True)
    lambda_3, t = sp.symbols("lambda_3 t", real=True)
    frame = list(full_noise_frame())
    identity = sp.eye(21)
    centered = [
        sp.ImmutableMatrix(item - sp.trace(item) * identity / 21) for item in frame
    ]

    # The first transfer direction and the eleventh gauge direction give a
    # particularly small rational ray with a nonzero cubic trace.
    ray = sp.ImmutableMatrix(centered[0] + centered[40])
    q2 = sp.expand(sp.trace(ray**2))
    q3 = sp.expand(sp.trace(ray**3))
    q4 = sp.expand(sp.trace(ray**4))
    action = sp.expand(alpha * q2 * t**2 + lambda_3 * q3 * t**3 + beta * q4 * t**4)
    first = sp.diff(action, t)
    second = sp.diff(action, t, 2)
    third_at_zero = sp.diff(action, t, 3).subs(t, 0)
    quadratic_third_at_zero = sp.diff(alpha * q2 * t**2, t, 3).subs(t, 0)
    stationary_lambda_at_one = sp.solve(sp.Eq(first.subs(t, 1), 0), lambda_3)[0]
    stationary_hessian_at_one = sp.factor(
        second.subs({t: 1, lambda_3: stationary_lambda_at_one})
    )
    dimensionless_ratio = sp.factor(lambda_3**2 / (alpha * beta))

    assert (q2, q3, q4) == (38, -3, 134)
    assert action == 38 * alpha * t**2 - 3 * lambda_3 * t**3 + 134 * beta * t**4
    assert quadratic_third_at_zero == 0
    assert third_at_zero == -18 * lambda_3
    assert stationary_lambda_at_one == (76 * alpha + 536 * beta) / 9
    assert sp.expand(stationary_hessian_at_one) == -76 * alpha + 536 * beta
    assert sp.simplify(
        stationary_hessian_at_one / 536 - (beta - 19 * alpha / 134)
    ) == 0

    exact_objects = [
        q2,
        q3,
        q4,
        action,
        first,
        second,
        third_at_zero,
        stationary_lambda_at_one,
        stationary_hessian_at_one,
        dimensionless_ratio,
    ]
    assert not any(
        atom.is_Float
        for obj in exact_objects
        for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_cubic_trace_parent_action_coefficient_origin_no_go_gate",
        "field": "Q(alpha,beta,lambda_3,t)",
        "exact_ray": {
            "definition": "A=Fhat_0+Fhat_40",
            "Tr_A2": str(q2),
            "Tr_A3": str(q3),
            "Tr_A4": str(q4),
        },
        "ray_action": {
            "definition": "alpha Tr(A^2)t^2 + lambda_3 Tr(A^3)t^3 + beta Tr(A^4)t^4",
            "polynomial": str(action),
            "quadratic_parent_third_derivative_at_zero": str(quadratic_third_at_zero),
            "full_third_derivative_at_zero": str(third_at_zero),
        },
        "boundedness": {
            "pure_nonzero_cubic_bounded_below": False,
            "positive_quartic_bounded_below_for_every_lambda_3": True,
            "boundedness_selects_lambda_3": False,
        },
        "stationary_unit_ray": {
            "lambda_3": str(stationary_lambda_at_one),
            "hessian_after_stationarity": str(stationary_hessian_at_one),
            "positive_hessian_condition": "beta > 19*alpha/134",
            "unique_without_alpha_beta": False,
        },
        "normalization": {
            "dimensionless_shape_ratio": str(dimensionless_ratio),
            "fixed_by_trace_metric": False,
        },
        "verdict": {
            "current_quadratic_parent_generates_cubic_coefficient": False,
            "boundedness_fixes_coefficient": False,
            "stationarity_fixes_absolute_coefficient": False,
            "cubic_carrier_remains_admissible": True,
            "resume_condition": "full spacetime supercurvature projection onto W3 with common normalization",
            "next_gate": "spacetime_supercurvature_cubic_projection_admission",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()