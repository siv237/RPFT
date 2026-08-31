#!/usr/bin/env python3
"""Exact grading audit of the residual source line in the SO(3)-closed environment."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_so3_closed_environment_source_line_selector_gate_results.json"


def matrix_unit(row: int, column: int) -> sp.Matrix:
    result = sp.zeros(3, 2)
    result[row, column] = 1
    return result


def hs_square(matrix: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.trace(matrix.T.conjugate() * matrix))


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_multiplicity_environment_so3_action_parent_origin_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["verdict"]["residual_projective_selector"] == "RP1"
    assert previous["next_gate"] == "version8_baryon_c0_so3_closed_environment_source_line_selector_gate"

    target_grading = sp.diag(-1, 1, 1)
    source_grading = sp.diag(1, -1)
    current_arrows = (matrix_unit(0, 0), matrix_unit(1, 1), matrix_unit(2, 1))
    missing_arrows = (matrix_unit(1, 0), matrix_unit(2, 0), matrix_unit(0, 1))

    def odd_residual(arrow: sp.Matrix) -> sp.Matrix:
        return target_grading * arrow + arrow * source_grading

    assert all(odd_residual(arrow) == sp.zeros(3, 2) for arrow in current_arrows)
    missing_residual_squares = [hs_square(odd_residual(arrow)) for arrow in missing_arrows]
    assert missing_residual_squares == [4, 4, 4]

    j1 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    j2 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    j3 = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    generators = (j1, j2, j3)
    grading_commutator_squares = [hs_square(target_grading * item - item * target_grading) for item in generators]
    assert grading_commutator_squares == [0, 8, 8]

    u, v = sp.symbols("u v", real=True)
    family_basis = tuple(sp.eye(3)[:, index] for index in range(3))
    family_maps = tuple(sp.Matrix.hstack(u * vector, v * vector) for vector in family_basis)
    oddness_expressions: list[sp.Expr] = []
    for family_map in family_maps:
        oddness_expressions.extend(list(odd_residual(family_map)))
    oddness_system, _ = sp.linear_eq_to_matrix(oddness_expressions, (u, v))
    assert oddness_system.rank() == 2
    assert oddness_system.nullspace() == []

    total_parity_defect = sp.simplify(sum(hs_square(odd_residual(item)) for item in family_maps))
    assert total_parity_defect == 8 * u**2 + 4 * v**2
    assert sp.simplify(total_parity_defect.subs({u: 1, v: 0})) == 8
    assert sp.simplify(total_parity_defect.subs({u: 0, v: 1})) == 4

    odd_projector = lambda arrow: sp.simplify((arrow - target_grading * arrow * source_grading) / 2)
    projected_u = sp.Matrix.hstack(*(odd_projector(item.subs({u: 1, v: 0})).reshape(6, 1) for item in family_maps))
    projected_v = sp.Matrix.hstack(*(odd_projector(item.subs({u: 0, v: 1})).reshape(6, 1) for item in family_maps))
    assert projected_u.rank() == 1
    assert projected_v.rank() == 2

    x = sp.Matrix([[0, 1], [1, 0]])
    y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    h = source_grading
    pauli_casimir = sp.simplify(x**2 + y**2 + h**2)
    assert pauli_casimir == 3 * sp.eye(2)
    trace_state = sp.eye(2) / 2
    assert sp.trace(trace_state * h) == 0
    assert sp.trace(trace_state * sp.diag(1, 0)) == sp.Rational(1, 2)
    assert sp.trace(trace_state * sp.diag(0, 1)) == sp.Rational(1, 2)

    alpha, beta = sp.symbols("alpha beta", real=True)
    candidate_hamiltonian = beta * sp.eye(2) + alpha * h
    assert candidate_hamiltonian.eigenvals() == {alpha + beta: 1, -alpha + beta: 1}

    uniform_minus = -sp.eye(3)
    uniform_plus = sp.eye(3)
    minus_flips = sum(1 for index in range(3) if uniform_minus[index, index] != target_grading[index, index])
    plus_flips = sum(1 for index in range(3) if uniform_plus[index, index] != target_grading[index, index])
    assert (minus_flips, plus_flips) == (2, 1)

    exact_objects = [
        target_grading,
        source_grading,
        *current_arrows,
        *missing_arrows,
        *generators,
        oddness_system,
        total_parity_defect,
        projected_u,
        projected_v,
        pauli_casimir,
        trace_state,
        candidate_hamiltonian,
    ]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_so3_closed_environment_source_line_selector_gate",
        "grading": {
            "target": "diag(-1,+1,+1)",
            "source": "diag(+1,-1)",
            "current_three_arrows_odd": True,
            "missing_arrow_oddness_residual_squares": [int(item) for item in missing_residual_squares],
            "SO3_generator_grading_commutator_squares": [int(item) for item in grading_commutator_squares],
            "standard_SO3_commutes_with_target_grading": False,
        },
        "source_line_family": {
            "intertwiner": "T_(u,v)(z)=[u z, v z]",
            "oddness_constraint_rank": oddness_system.rank(),
            "odd_intertwiner_dimension": 0,
            "total_parity_defect": "8 u^2 + 4 v^2",
            "u_axis_defect": 8,
            "v_axis_defect": 4,
            "odd_projection_rank_u_axis": projected_u.rank(),
            "odd_projection_rank_v_axis": projected_v.rank(),
            "admissible_RP1_points": 0,
        },
        "current_parent_selectors": {
            "source_grading_projectors": "two coordinate lines, no preferred sign",
            "normalized_trace_state": "I2/2",
            "pauli_casimir": "3 I2",
            "depolarizing_stationary_state": "I2/2",
            "real_structure": "preserves both coordinate lines",
            "grading_hamiltonian": "beta I2 + alpha Gamma_src with sign(alpha) unselected",
            "derived_unique_selectors": 0,
            "tested_selectors": 6,
        },
        "conditional_grading_changes": {
            "target_minus_identity_selects_source_column": "s0",
            "target_minus_identity_grade_flips": minus_flips,
            "target_plus_identity_selects_source_column": "a0",
            "target_plus_identity_grade_flips": plus_flips,
            "minimum_edit_is_parent_principle": False,
            "changes_existing_H21_grading": True,
        },
        "verdict": {
            "source_line_selected": False,
            "any_current_RP1_point_is_odd_SO3_intertwiner": False,
            "grading_obstruction_stronger_than_selector_ambiguity": True,
            "single_c0_map_derived": False,
        },
        "next_gate": "version8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()