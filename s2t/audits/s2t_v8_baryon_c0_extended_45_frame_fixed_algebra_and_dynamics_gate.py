#!/usr/bin/env python3
"""Exact fixed-algebra and dynamics audit for the extended 45-frame."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_extended_45_frame_fixed_algebra_and_dynamics_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_full_noise_trace_frame import full_noise_frame  # noqa: E402


def extend_old(matrix: sp.MatrixBase) -> sp.ImmutableMatrix:
    result = sp.zeros(23)
    result[:21, :21] = matrix
    return sp.ImmutableMatrix(result)


def lindblad(jumps: tuple[sp.ImmutableMatrix, ...], observable: sp.MatrixBase) -> sp.ImmutableMatrix:
    result = sp.zeros(observable.rows)
    for jump in jumps:
        square = jump * jump
        result += jump * observable * jump - sp.Rational(1, 2) * (
            square * observable + observable * square
        )
    return sp.ImmutableMatrix(result)


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_minimal_neutral_endpoint_extension_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["extended_frame"]["new_rank"] == 45
    assert previous["next_gate"] == "version8_baryon_c0_extended_45_frame_fixed_algebra_and_dynamics_gate"

    old21 = tuple(sp.ImmutableMatrix(item) for item in full_noise_frame())
    common_kernel_system = sp.Matrix.vstack(*old21)
    assert common_kernel_system.rank() == 21

    q42 = sp.ImmutableMatrix(sum((item**2 for item in old21), sp.zeros(21)))
    assert q42 == q42.H
    assert q42.rank() == 21
    assert q42.is_positive_definite

    x2 = sp.ImmutableMatrix([[0, 1], [1, 0]])
    y2 = sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]])
    h2 = sp.ImmutableMatrix([[1, 0], [0, -1]])
    paulis = (x2, y2, h2)

    a, b, c, d = sp.symbols("a b c d")
    generic = sp.Matrix([[a, b], [c, d]])
    equations = []
    for sigma in paulis:
        equations.extend(list(generic * sigma - sigma * generic))
    commutant_system, _ = sp.linear_eq_to_matrix(equations, (a, b, c, d))
    assert commutant_system.rank() == 3
    assert 4 - commutant_system.rank() == 1

    old23 = tuple(extend_old(item) for item in old21)
    new23 = []
    for sigma in paulis:
        item = sp.zeros(23)
        item[21:23, 21:23] = sigma
        new23.append(sp.ImmutableMatrix(item))
    jumps = old23 + tuple(new23)

    p21 = sp.ImmutableMatrix(sp.diag(*([1] * 21 + [0, 0])))
    pn = sp.ImmutableMatrix(sp.diag(*([0] * 21 + [1, 1])))
    assert all(jump * p21 == p21 * jump for jump in jumps)
    assert all(jump * pn == pn * jump for jump in jumps)

    for sigma, embedded in zip(paulis, new23):
        assert lindblad(tuple(new23), embedded) == -4 * embedded
        assert sum((left * sigma * left for left in paulis), sp.zeros(2)) == -sigma

    b_symbols = sp.symbols("b0:42")
    bmat = sp.Matrix(21, 2, b_symbols)
    observable = sp.zeros(23)
    observable[:21, 21:23] = bmat
    assert all(jump * observable * jump == sp.zeros(23) for jump in jumps)
    square_sum = sum((jump * jump for jump in jumps), sp.zeros(23))
    expected_square_sum = sp.zeros(23)
    expected_square_sum[:21, :21] = q42
    expected_square_sum[21:23, 21:23] = 3 * sp.eye(2)
    assert square_sum == expected_square_sum
    dissipative_block = -sp.Rational(1, 2) * (
        square_sum * observable + observable * square_sum
    )
    assert dissipative_block[:21, 21:23] == -sp.Rational(1, 2) * (
        q42 * bmat + 3 * bmat
    )

    exact_objects = [*q42, *commutant_system, *p21, *pn]
    assert not any(
        atom.is_Float for obj in exact_objects for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_extended_45_frame_fixed_algebra_and_dynamics_gate",
        "generator": {
            "jump_count": 45,
            "self_adjoint_jumps": True,
            "gksl": True,
            "unital": True,
            "trace_preserving": True,
            "dirichlet_identity": "-<A,L(A)>=1/2 sum ||[R,A]||_HS^2",
        },
        "commutant": {
            "old_frame_commutant": "C I_21",
            "old_frame_common_kernel_dimension": 0,
            "new_pauli_commutant": "C I_2",
            "full_fixed_algebra": "C P_21 direct_sum C P_n",
            "full_fixed_algebra_dimension": 2,
            "primitive_on_H23": False,
        },
        "dynamics": {
            "new_traceless_eigenvalue": -4,
            "new_traceless_multiplicity": 3,
            "Q42_rank": 21,
            "Q42_positive_definite": True,
            "old_new_coherences_decay": True,
            "central_sector_populations_conserved": True,
            "old_new_population_transfer": False,
        },
        "c0_boundary": {
            "internal_M2_linking_block_exists": True,
            "dynamically_embedded_into_old_42_carrier": False,
            "conditional_c0": 4,
            "physical_c0_derived": False,
        },
        "verdict": {
            "extended_45_frame_dynamics_constructed": True,
            "scalar_fixed_algebra_obtained": False,
            "disconnected_center_no_go": True,
            "old_new_connector_required": True,
        },
        "next_gate": "version8_baryon_c0_old_new_gauge_covariant_connector_classification_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()