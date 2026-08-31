#!/usr/bin/env python3
"""Exact bidirectional KMS completion audit for the Tome IX creation frame."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_bidirectional_kms_completion_architecture_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def unit(n: int, i: int, j: int) -> sp.Matrix:
    matrix = sp.zeros(n)
    matrix[i, j] = 1
    return matrix


def dissipator(c: sp.Matrix, x: sp.Matrix) -> sp.Matrix:
    gram = c.T * c
    return c * x * c.T - (gram * x + x * gram) / 2


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_finite_geometry_creation_operator_parent_origin_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate

    q = [sp.Rational(1, 2), sp.Rational(1, 3)] + [sp.Rational(1, 4)] * 3
    weights = [sp.Integer(1), *q]
    rho = sp.diag(*weights) / sum(weights)
    assert rho == sp.diag(12, 6, 4, 3, 3, 3) / 31
    assert rho.det() == sp.Rational(7776, 887503681)

    creation = [unit(6, i, 0) for i in range(1, 6)]
    columns = []
    for i in range(6):
        for j in range(6):
            x = unit(6, i, j)
            y = sp.zeros(6)
            for channel, ratio in zip(creation, q):
                y += ratio * dissipator(channel, x)
                y += dissipator(channel.T, x)
            columns.append(y.reshape(36, 1))
    superoperator = sp.Matrix.hstack(*columns)
    assert superoperator.rank() == 35
    assert 36 - superoperator.rank() == 1
    assert superoperator * rho.reshape(36, 1) == sp.zeros(36, 1)

    matrix_units = [unit(6, i, j) for i in range(6) for j in range(6)]
    generated = [sp.eye(6), *creation, *(c.T for c in creation)]
    changed = True
    while changed:
        old_rank = sp.Matrix.hstack(*(x.reshape(36, 1) for x in generated)).rank()
        products = [a * b for a in generated for b in generated]
        basis = []
        for candidate in [*generated, *products]:
            trial = [*basis, candidate]
            rank = sp.Matrix.hstack(*(x.reshape(36, 1) for x in trial)).rank()
            if rank > len(basis):
                basis.append(candidate)
            if len(basis) == 36:
                break
        generated = basis
        changed = len(generated) > old_rank
    assert len(generated) == len(matrix_units) == 36

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "exact_witness": {
            "boltzmann_ratios": ["1/2", "1/3", "1/4"],
            "conductances": [1, 1, 1],
            "stationary_state_diagonal": ["12/31", "6/31", "4/31", "3/31", "3/31", "3/31"],
            "stationary_state_determinant": "7776/887503681",
            "new_endpoint_population": "13/31",
        },
        "bidirectional_qms": {
            "channel_pairs": 5,
            "generated_algebra_dimension": 36,
            "jump_commutant_dimension": 1,
            "liouvillian_rank": 35,
            "stationary_operator_space_dimension": 1,
            "primitive": True,
            "faithful_stationary_state": True,
        },
        "ledgers": {
            "architecture_satisfied": 10,
            "architecture_tested": 10,
            "primitive_closure_satisfied": 1,
            "primitive_closure_tested": 1,
            "kms_parameter_origin_satisfied": 0,
            "kms_parameter_origin_tested": 6,
            "physical_endpoint_selection_satisfied": 0,
            "physical_endpoint_selection_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "reverse_jumps_restore_primitive_closure": True,
            "kms_fixes_forward_reverse_ratios": True,
            "kms_selects_three_gaps": False,
            "kms_selects_three_conductances": False,
            "common_parent_still_required": True,
        },
        "next_gate": "version9_endpoint_creation_kms_gap_conductance_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()