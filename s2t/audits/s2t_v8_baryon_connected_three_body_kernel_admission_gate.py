#!/usr/bin/env python3
"""Exact admission audit for a connected three-body baryon kernel."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v8_baryon_connected_three_body_kernel_admission_gate_results.json"
)


def main() -> None:
    theta, epsilon, u, kappa_3 = sp.symbols(
        "theta epsilon u kappa_3", real=True
    )
    configurations = list(itertools.product((-1, 1), repeat=3))
    parity = sp.Matrix([x1 * x2 * x3 for x1, x2, x3 in configurations])
    uniform = sp.ones(8, 1) / 8
    probability = uniform + theta * parity / 8

    pairs = ((0, 1), (0, 2), (1, 2))
    pair_outcomes = list(itertools.product((-1, 1), repeat=2))
    marginal_rows = []
    for i, j in pairs:
        for outcome in pair_outcomes:
            marginal_rows.append(
                [
                    sp.Integer(int((x[i], x[j]) == outcome))
                    for x in configurations
                ]
            )
    marginal_map = sp.Matrix(marginal_rows)
    pair_marginals = sp.simplify(marginal_map * probability)

    first_moments = [
        sp.factor(sum(x[i] * probability[n] for n, x in enumerate(configurations)))
        for i in range(3)
    ]
    second_moments = {
        f"{i + 1}{j + 1}": sp.factor(
            sum(
                x[i] * x[j] * probability[n]
                for n, x in enumerate(configurations)
            )
        )
        for i, j in pairs
    }
    third_moment = sp.factor(
        sum(x[0] * x[1] * x[2] * probability[n] for n, x in enumerate(configurations))
    )

    # Exact parity test for the star-shaped repeated-interaction carrier.
    y = sp.symbols("y0:4", real=True)
    star = sp.zeros(5)
    for a, value in enumerate(y, start=1):
        star[0, a] = value
        star[a, 0] = value
    environment_parity = sp.diag(1, -1, -1, -1, -1)
    parity_anticommutator = sp.simplify(
        environment_parity * star * environment_parity + star
    )
    vacuum_second_moment = sp.expand((star**2)[0, 0])
    vacuum_third_moment = sp.expand((star**3)[0, 0])

    # Put h=epsilon^2 and n=u/epsilon^2.  The second cumulant survives,
    # whereas a bounded third cumulant is suppressed by one power of epsilon.
    accumulated_second_order = sp.cancel((u / epsilon**2) * epsilon**2)
    accumulated_third_order = sp.cancel(
        (u / epsilon**2) * epsilon**3 * kappa_3
    )

    assert sp.factor(sum(probability)) == 1
    assert marginal_map.rank() == 7
    assert len(marginal_map.nullspace()) == 1
    assert marginal_map * parity == sp.zeros(12, 1)
    assert pair_marginals == sp.ones(12, 1) / 4
    assert first_moments == [0, 0, 0]
    assert set(second_moments.values()) == {sp.Integer(0)}
    assert third_moment == theta
    assert parity_anticommutator == sp.zeros(5)
    assert vacuum_second_moment == sum(value**2 for value in y)
    assert vacuum_third_moment == 0
    assert accumulated_second_order == u
    assert accumulated_third_order == epsilon * kappa_3 * u

    exact_objects = (
        list(probability)
        + list(marginal_map)
        + list(pair_marginals)
        + list(star)
        + list(environment_parity)
        + [accumulated_second_order, accumulated_third_order]
    )
    assert not any(
        atom.is_Float
        for obj in exact_objects
        for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_connected_three_body_kernel_admission_gate",
        "field": "Q(theta,epsilon,u,kappa_3)",
        "three_bit_family": {
            "probability": "(1 + theta*x1*x2*x3)/8",
            "positivity_interval": "-1 <= theta <= 1",
            "normalization": "1",
            "first_moments": [str(value) for value in first_moments],
            "second_moments": {
                key: str(value) for key, value in second_moments.items()
            },
            "connected_third_moment": str(third_moment),
        },
        "marginal_map": {
            "shape": list(marginal_map.shape),
            "rank": marginal_map.rank(),
            "kernel_dimension": len(marginal_map.nullspace()),
            "kernel_generator": [str(value) for value in parity],
            "all_pair_marginals": [str(value) for value in pair_marginals],
        },
        "star_collision_parent": {
            "environment_dimension": "43 in the full model",
            "parity_identity": "Pi*H_int*Pi = -H_int",
            "vacuum_second_moment_surrogate": str(vacuum_second_moment),
            "vacuum_third_moment": str(vacuum_third_moment),
            "all_vacuum_odd_moments": "zero by parity",
        },
        "weak_collision_scaling": {
            "h": "epsilon^2",
            "n": "u/epsilon^2",
            "accumulated_second_order": str(accumulated_second_order),
            "accumulated_bounded_third_order": str(accumulated_third_order),
            "third_order_limit_epsilon_to_zero": "0",
        },
        "verdict": {
            "one_and_two_body_data_determine_three_body_kernel": False,
            "current_star_parent_selects_connected_third_cumulant": False,
            "current_gksl_limit_retains_bounded_third_cumulant": False,
            "new_operator_required": "connected three-body or six-point kernel",
            "next_gate": "three_body_kernel_parent_origin_or_no_go",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()