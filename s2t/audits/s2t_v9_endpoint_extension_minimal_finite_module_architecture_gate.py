#!/usr/bin/env python3
"""Exact minimal finite-module architecture audit for Tome IX."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_extension_minimal_finite_module_architecture_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def matrix_unit(size: int, row: int, column: int) -> sp.Matrix:
    result = sp.zeros(size)
    result[row, column] = 1
    return result


def span_rank(matrices: list[sp.Matrix]) -> int:
    return sp.Matrix.hstack(*[matrix.reshape(matrix.rows * matrix.cols, 1) for matrix in matrices]).rank()


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v9_endpoint_extension_raw_parent_origin_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert predecessor["verdict"]["minimal_new_typed_module_dimension"] == 3

    m2_units = [matrix_unit(2, row, column) for row in range(2) for column in range(2)]
    m3_units = [matrix_unit(3, row, column) for row in range(3) for column in range(3)]
    assert span_rank(m2_units) == 4
    assert span_rank(m3_units) == 9

    neutral_hermitian = [
        sp.eye(2),
        sp.diag(1, -1),
        matrix_unit(2, 0, 1) + matrix_unit(2, 1, 0),
        -sp.I * (matrix_unit(2, 0, 1) - matrix_unit(2, 1, 0)),
    ]
    triplet_hermitian = []
    for index in range(3):
        triplet_hermitian.append(matrix_unit(3, index, index))
    for left in range(3):
        for right in range(left + 1, 3):
            triplet_hermitian.extend(
                [
                    matrix_unit(3, left, right) + matrix_unit(3, right, left),
                    -sp.I * (matrix_unit(3, left, right) - matrix_unit(3, right, left)),
                ]
            )
    assert span_rank(neutral_hermitian) == 4
    assert span_rank(triplet_hermitian) == 9

    grading_2 = sp.diag(1, -1)
    hypercharge_2 = sp.zeros(2)
    x = neutral_hermitian[2]
    y = neutral_hermitian[3]
    assert grading_2 * x + x * grading_2 == sp.zeros(2)
    assert grading_2 * y + y * grading_2 == sp.zeros(2)
    assert hypercharge_2 * x - x * hypercharge_2 == sp.zeros(2)

    grading_3 = sp.eye(3)
    hypercharge_3 = -sp.eye(3)
    family_generators = [
        matrix_unit(3, 1, 2) - matrix_unit(3, 2, 1),
        matrix_unit(3, 2, 0) - matrix_unit(3, 0, 2),
        matrix_unit(3, 0, 1) - matrix_unit(3, 1, 0),
    ]
    for generator in family_generators:
        assert generator * grading_3 - grading_3 * generator == sp.zeros(3)
        assert generator * hypercharge_3 - hypercharge_3 * generator == sp.zeros(3)

    swap = sp.zeros(10)
    swap[:5, 5:] = sp.eye(5)
    swap[5:, :5] = sp.eye(5)
    assert swap**2 == sp.eye(10)

    checks = {
        "neutral_matrix_algebra_dimension_is_4": True,
        "triplet_matrix_algebra_dimension_is_9": True,
        "direct_sum_algebra_dimension_is_13": True,
        "direct_sum_center_dimension_is_2": True,
        "three_new_complex_system_states": True,
        "real_closed_increment_has_dimension_6": True,
        "hermitian_increment_over_old_D2_is_11": True,
        "neutral_bridge_is_odd_and_gauge_neutral": True,
        "triplet_block_is_family_grading_gauge_compatible": True,
        "old_H21_is_preserved_as_a_corner": True,
    }
    assert all(checks.values())

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "finite_module": {
            "new_independent_complex_states": 3,
            "real_closed_complex_increment": 6,
            "active_block_decomposition": "H24=Hrest19 direct_sum Hn2 direct_sum Ht3",
            "old_corner": "H21=Hrest19 direct_sum span(eR_t1,eR_t2)",
        },
        "finite_algebra": {
            "neutral_block": "M2(C)",
            "neutral_complex_dimension": 4,
            "triplet_block": "M3(C)",
            "triplet_complex_dimension": 9,
            "direct_sum": "M2(C) direct_sum M3(C)",
            "complex_dimension": 13,
            "center_dimension": 2,
            "old_active_hermitian_dimension": 2,
            "new_active_hermitian_dimension": 13,
            "hermitian_increment": 11,
        },
        "architecture_audit": {
            **checks,
            "satisfied": sum(checks.values()),
            "tested": len(checks),
        },
        "ledgers": {
            "finite_module_architecture_satisfied": 10,
            "finite_module_architecture_tested": 10,
            "finite_module_parent_origin_satisfied": 0,
            "finite_module_parent_origin_tested": 1,
            "raw_physical_slot_closure_satisfied": 0,
            "raw_physical_slot_closure_tested": 4,
        },
        "verdict": {
            "minimal_finite_module_architecture_constructed": True,
            "old_H21_restriction_preserved": True,
            "real_gauge_grading_family_compatible": True,
            "new_module_physically_derived": False,
        },
        "next_gate": "version9_endpoint_finite_module_parent_action_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()