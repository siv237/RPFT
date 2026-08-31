#!/usr/bin/env python3
"""Exact audit of the environment correlation left by a one-copy parent."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_common_environment_correlation_origin_gate_results.json"


def kron3(a: sp.Matrix, b: sp.Matrix, d: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(a, b, d)


def main() -> None:
    c = sp.symbols("c", real=True)
    identity = sp.eye(2)
    sigma_x = sp.Matrix([[0, 1], [1, 0]])
    f = sp.Matrix([[1, 0], [0, -1]]) / 2
    copies = [
        kron3(f, identity, identity),
        kron3(identity, f, identity),
        kron3(identity, identity, f),
    ]
    covariance = (1 - c) * sp.eye(3) + c * sp.ones(3, 3)

    def generator(observable: sp.Matrix) -> sp.Matrix:
        value = sp.zeros(8, 8)
        for i in range(3):
            for j in range(3):
                inner = copies[j] * observable - observable * copies[j]
                value -= sp.Rational(1, 2) * covariance[i, j] * (
                    copies[i] * inner - inner * copies[i]
                )
        return sp.simplify(value)

    local = kron3(sigma_x, identity, identity)
    pair = kron3(sigma_x, sigma_x, identity)
    local_residual = sp.simplify(generator(local) - generator(local).subs(c, 0))
    pair_difference = sp.simplify(generator(pair) - generator(pair).subs(c, 0))
    pair_difference_square = sp.factor(sp.trace(pair_difference.H * pair_difference))

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_common_environment_correlation_origin_gate",
        "field": "Q(c)",
        "environment_covariance": {
            "matrix": str(covariance),
            "eigenvalues": ["1-c", "1-c", "1+2*c"],
            "complete_positivity_interval": "-1/2 <= c <= 1",
            "independent_environment_rank": int(covariance.subs(c, 0).rank()),
            "common_environment_rank": int(covariance.subs(c, 1).rank()),
            "anticorrelated_boundary_rank": int(covariance.subs(c, -sp.Rational(1, 2)).rank()),
        },
        "one_particle_restriction": {
            "independent_of_c_exact": local_residual == sp.zeros(8, 8),
            "reason": "only R_11 enters a one-site double commutator and R_11=1",
        },
        "two_particle_observable": {
            "depends_on_c": pair_difference != sp.zeros(8, 8),
            "hilbert_schmidt_square_of_difference": str(pair_difference_square),
        },
        "microscopic_parents": {
            "independent_cells": "R=I_3, c=0",
            "shared_cell": "R=11^T, c=1",
            "both_reduce_to_same_one_copy_parent": True,
            "both_permutation_covariant": True,
            "both_gauge_covariant_when_channel_labels_are_shared": True,
        },
        "status_boundary": {
            "one_copy_parent_selects_c": False,
            "product_composition_selects_c_zero_conditionally": True,
            "shared_environment_axiom_selects_c_one_conditionally": True,
            "existing_parent_action_contains_shared_environment_axiom": False,
            "baryon_collective_noise_derived": False,
            "physical_mass_theorem": False,
        },
        "verdict": {
            "common_environment_origin": "not derived",
            "baryon_sprint_status": "stop_on_exact_nonuniqueness",
            "reopening_condition": "derive an inter-copy environment two-point kernel or a common-bath parent action",
        },
    }

    assert covariance.subs(c, 0) == sp.eye(3)
    assert covariance.subs(c, 1) == sp.ones(3, 3)
    assert local_residual == sp.zeros(8, 8)
    assert pair_difference_square == 8 * c**2
    assert covariance.subs(c, 0).rank() == 3
    assert covariance.subs(c, 1).rank() == 1
    assert covariance.subs(c, -sp.Rational(1, 2)).rank() == 2

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()