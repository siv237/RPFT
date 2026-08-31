#!/usr/bin/env python3
"""Exact Kraus-rank obstruction between the full frame and one c0 map."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_full_multiplicity_frame_single_map_compatibility_gate_results.json"


def connector(row: int, column: int) -> sp.ImmutableMatrix:
    value = sp.zeros(21, 2)
    value[row, column] = 1
    return sp.ImmutableMatrix(value)


def quadratures(v: sp.MatrixBase) -> tuple[sp.ImmutableMatrix, sp.ImmutableMatrix]:
    c1 = sp.zeros(23); c1[:21, 21:23] = v; c1[21:23, :21] = v.H
    c2 = sp.zeros(23); c2[:21, 21:23] = sp.I * v; c2[21:23, :21] = -sp.I * v.H
    return sp.ImmutableMatrix(c1), sp.ImmutableMatrix(c2)


def lindblad(jumps: tuple[sp.ImmutableMatrix, ...], observable: sp.MatrixBase) -> sp.ImmutableMatrix:
    result = sp.zeros(23)
    for jump in jumps:
        square = jump * jump
        result += jump * observable * jump - sp.Rational(1, 2) * (
            square * observable + observable * square
        )
    return sp.ImmutableMatrix(result)


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_extended_endpoint_bimodule_weight_origin_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["full_hom_closure"]["new_real_quadratures"] == 6
    assert previous["next_gate"] == "version8_baryon_c0_full_multiplicity_frame_single_map_compatibility_gate"

    maps = tuple(connector(row, column) for row, column in ((8, 0), (17, 1), (18, 1)))
    vectorized = sp.Matrix.hstack(*[sp.Matrix(list(item)) for item in maps])
    assert vectorized.rank() == 3

    c_full = sp.eye(3)
    z = sp.Matrix([1, 2, 3])
    c_single = z * z.T
    assert c_full.rank() == 3
    assert c_single.rank() == 1

    choi_full = vectorized * c_full * vectorized.H
    choi_single = vectorized * c_single * vectorized.H
    assert choi_full.rank() == 3
    assert choi_single.rank() == 1

    full_jumps = tuple(jump for item in maps for jump in quadratures(item))
    single_jumps = quadratures(maps[0])
    p21 = sp.ImmutableMatrix(sp.diag(*([1] * 21 + [0, 0])))
    pn = sp.ImmutableMatrix(sp.diag(*([0] * 21 + [1, 1])))
    central_basis = (p21 / sp.sqrt(21), pn / sp.sqrt(2))

    def central_matrix(jumps: tuple[sp.ImmutableMatrix, ...]) -> sp.Matrix:
        return sp.Matrix(
            [
                [sp.simplify(sp.trace(left.H * (-lindblad(jumps, right)))) for right in central_basis]
                for left in central_basis
            ]
        )

    d0 = sp.Matrix([[sp.Rational(2, 21), -sp.sqrt(42) / 21], [-sp.sqrt(42) / 21, 1]])
    assert central_matrix(single_jumps) == d0
    assert central_matrix(full_jumps) == 3 * d0

    p_er = sp.zeros(23); p_er[17, 17] = 1
    p_er = sp.ImmutableMatrix(p_er)
    p_a = sp.zeros(23); p_a[22, 22] = 1
    p_a = sp.ImmutableMatrix(p_a)
    assert lindblad(single_jumps, p_er) == sp.zeros(23)
    assert lindblad(full_jumps, p_er) == 2 * (p_a - p_er)

    gamma_full, gamma_single = sp.symbols("gamma_full gamma_single", positive=True)
    assert sp.simplify((3 * gamma_full * d0 - gamma_single * d0).subs(gamma_single, 3 * gamma_full)) == sp.zeros(2)

    exact_objects = [*vectorized, *choi_full, *choi_single, *d0]
    assert not any(atom.is_Float for obj in exact_objects for atom in sp.preorder_traversal(obj))

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_full_multiplicity_frame_single_map_compatibility_gate",
        "kossakowski": {
            "full_covariance": "I3",
            "full_rank": 3,
            "single_covariance": "z z*",
            "single_rank": 1,
            "rank_preserved_by_kraus_isometries": True,
        },
        "choi_stinespring": {
            "connector_vectorization_rank": 3,
            "full_choi_rank": 3,
            "single_choi_rank": 1,
            "full_minimal_environment_dimension": 3,
            "single_minimal_environment_dimension": 1,
        },
        "central_restriction": {
            "single_coordinate_matrix": [["2/21", "-sqrt(42)/21"], ["-sqrt(42)/21", "1"]],
            "full_matrix_factor": 3,
            "central_equivalence_rate_relation": "gamma_single=3 gamma_full",
            "central_test_distinguishes_processes": False,
        },
        "operator_witness": {
            "observable": "P_eR",
            "full_action": "2(P_a-P_eR)",
            "single_V0_action": "0",
            "full_and_single_generators_equal": False,
        },
        "selector_boundary": {
            "rank_one_reduction_requires_environment_pure_state": True,
            "environment_direction_space": "CP^2; RP^2 on Real slice",
            "pure_state_selected": False,
            "single_c0_map_derived": False,
        },
        "verdict": {
            "central_compatibility_after_rate_rescaling": True,
            "operator_level_compatibility": False,
            "kraus_minimality_no_go": True,
            "environment_selector_required": True,
        },
        "next_gate": "version8_baryon_c0_multiplicity_environment_pure_state_selector_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()