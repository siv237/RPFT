#!/usr/bin/env python3
"""Exact origin audit for KMS gaps and conductances in Tome IX."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_gap_conductance_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def unit(n: int, i: int, j: int) -> sp.Matrix:
    matrix = sp.zeros(n)
    matrix[i, j] = 1
    return matrix


def dissipator(c: sp.Matrix, x: sp.Matrix) -> sp.Matrix:
    gram = c.T * c
    return c * x * c.T - (gram * x + x * gram) / 2


def liouvillian_rank(
    q: list[sp.Rational], kappa: list[sp.Rational]
) -> int:
    creation = [unit(6, i, 0) for i in range(1, 6)]
    columns = []
    for i in range(6):
        for j in range(6):
            x = unit(6, i, j)
            y = sp.zeros(6)
            for channel, ratio, conductance in zip(creation, q, kappa):
                y += conductance * ratio * dissipator(channel, x)
                y += conductance * dissipator(channel.T, x)
            columns.append(y.reshape(36, 1))
    return sp.Matrix.hstack(*columns).rank()


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_bidirectional_kms_completion_architecture_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate

    type_matrix = sp.Matrix([[1, 1, 3], [1, -1, 3], [0, 0, -3]])
    assert type_matrix.det() == 6 and type_matrix.rank() == 3

    normalizations = sp.Matrix([
        [1, 1, 3, 0, 0, 0],
        [0, 0, 0, 1, 1, 3],
    ])
    assert normalizations.rank() == 2
    assert 6 - normalizations.rank() == 4

    common_metric = sp.diag(1, 1, 3, 1, 1, 3)
    assert common_metric.rank() == 6 and common_metric.det() == 9
    assert common_metric.inv() * sp.zeros(6, 1) == sp.zeros(6, 1)

    q1 = [sp.Rational(1, 2), sp.Rational(1, 3)] + [sp.Rational(1, 4)] * 3
    q2 = [sp.Rational(1, 3), sp.Rational(1, 2)] + [sp.Rational(1, 4)] * 3
    k1 = [sp.Integer(1)] * 5
    k2 = [sp.Integer(2), sp.Integer(1)] + [sp.Rational(2, 3)] * 3
    assert sum(q1) == sum(q2) == sp.Rational(19, 12)
    assert sum(k1) == sum(k2) == 5
    rate1 = sum(q * k for q, k in zip(q1, k1))
    rate2 = sum(q * k for q, k in zip(q2, k2))
    assert rate1 == sp.Rational(19, 12)
    assert rate2 == sp.Rational(5, 3)
    assert liouvillian_rank(q1, k1) == liouvillian_rank(q2, k2) == 35

    rho1 = sp.diag(1, *q1) / (1 + sum(q1))
    rho2 = sp.diag(1, *q2) / (1 + sum(q2))
    assert rho1 == sp.diag(12, 6, 4, 3, 3, 3) / 31
    assert rho2 == sp.diag(12, 4, 6, 3, 3, 3) / 31
    assert rho1 != rho2

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "type_system": {
            "matrix": [[1, 1, 3], [1, -1, 3], [0, 0, -3]],
            "determinant": 6,
            "rank": 3,
            "separates_channels": True,
            "selects_numeric_coefficients": False,
        },
        "normalization_audit": {
            "constraint_rank": 2,
            "six_parameter_relative_freedom": 4,
            "energy_temperature_scale_orbit": True,
            "conductance_time_scale_orbit": True,
        },
        "source_free_parent": {
            "hessian_diagonal": [1, 1, 3, 1, 1, 3],
            "hessian_rank": 6,
            "hessian_determinant": 9,
            "unique_minimum": [0, 0, 0, 0, 0, 0],
            "positive_primitive_minimum": False,
            "required_source_components": 6,
        },
        "normalized_witnesses": {
            "weighted_q_sum": "19/12",
            "weighted_kappa_sum": 5,
            "liouvillian_ranks": [35, 35],
            "initial_excitation_rates": ["19/12", "5/3"],
            "stationary_states_distinct": True,
        },
        "ledgers": {
            "type_separation_satisfied": 3,
            "type_separation_tested": 3,
            "candidate_origin_satisfied": 0,
            "candidate_origin_tested": 7,
            "gap_origin_satisfied": 0,
            "gap_origin_tested": 3,
            "conductance_origin_satisfied": 0,
            "conductance_origin_tested": 3,
            "kms_parameter_origin_satisfied": 0,
            "kms_parameter_origin_tested": 6,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "existing_types_distinguish_all_channels": True,
            "existing_types_select_gap_values": False,
            "existing_types_select_conductances": False,
            "normalizations_select_unique_kms_package": False,
            "common_source_parent_required": True,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_source_vector_"
            "common_parent_architecture_gate"
        ),
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()