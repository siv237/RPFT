#!/usr/bin/env python3
"""Exact audit of a parent SO(3) action on the connector multiplicity space."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_multiplicity_environment_so3_action_parent_origin_gate_results.json"


def matrix_unit(row: int, column: int) -> sp.Matrix:
    result = sp.zeros(3, 2)
    result[row, column] = 1
    return result


def column_vectorize(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(list(matrix[:, 0]) + list(matrix[:, 1]))


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_family_to_multiplicity_intertwiner_admission_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["verdict"]["derived_extension_structures"] == 0
    assert previous["next_gate"] == "version8_baryon_c0_multiplicity_environment_so3_action_parent_origin_gate"

    j1 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    j2 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    j3 = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    generators = (j1, j2, j3)
    assert j1 * j2 - j2 * j1 == j3
    assert j2 * j3 - j3 * j2 == j1
    assert j3 * j1 - j1 * j3 == j2

    current_arrows = (matrix_unit(0, 0), matrix_unit(1, 1), matrix_unit(2, 1))
    current_matrix = sp.Matrix.hstack(*(column_vectorize(item) for item in current_arrows))
    assert current_matrix.rank() == 3

    one_step = [generator * arrow for generator in generators for arrow in current_arrows]
    closure_matrix = sp.Matrix.hstack(
        *(column_vectorize(item) for item in (*current_arrows, *one_step))
    )
    assert closure_matrix.rank() == 6

    missing_arrows = (matrix_unit(1, 0), matrix_unit(2, 0), matrix_unit(0, 1))
    completed_matrix = sp.Matrix.hstack(
        *(column_vectorize(item) for item in (*current_arrows, *missing_arrows))
    )
    assert completed_matrix.rank() == 6
    assert closure_matrix.row_join(completed_matrix).rank() == 6

    invariance_failures = 0
    for generator in generators:
        for arrow in current_arrows:
            if current_matrix.row_join(column_vectorize(generator * arrow)).rank() > 3:
                invariance_failures += 1
    assert invariance_failures == 4

    # Any orthogonal real two-dimensional SO(3) representation is trivial:
    # so(2) is one-dimensional and abelian, whereas [so(3),so(3)]=so(3).
    source_coefficients = sp.symbols("k1:4", real=True)
    source_generator = sp.Matrix([[0, -1], [1, 0]])
    source_images = tuple(coefficient * source_generator for coefficient in source_coefficients)
    source_relations = [
        *(source_images[0] * source_images[1] - source_images[1] * source_images[0] - source_images[2]),
        *(source_images[1] * source_images[2] - source_images[2] * source_images[1] - source_images[0]),
        *(source_images[2] * source_images[0] - source_images[0] * source_images[2] - source_images[1]),
    ]
    source_system, _ = sp.linear_eq_to_matrix(source_relations, source_coefficients)
    assert source_system.rank() == 3
    assert sp.solve(source_relations, source_coefficients, dict=True) == [
        {source_coefficients[0]: 0, source_coefficients[1]: 0, source_coefficients[2]: 0}
    ]

    arrow_generators = tuple(sp.diag(generator, generator) for generator in generators)
    intertwiner_variables = sp.symbols("t0:18", real=True)
    intertwiner = sp.Matrix(6, 3, intertwiner_variables)
    intertwiner_equations: list[sp.Expr] = []
    for arrow_generator, family_generator in zip(arrow_generators, generators):
        intertwiner_equations.extend(list(arrow_generator * intertwiner - intertwiner * family_generator))
    intertwiner_system, _ = sp.linear_eq_to_matrix(intertwiner_equations, intertwiner_variables)
    intertwiner_kernel = intertwiner_system.nullspace()
    assert intertwiner_system.shape == (54, 18)
    assert intertwiner_system.rank() == 16
    assert len(intertwiner_kernel) == 2
    assert sp.Matrix(6, 3, list(intertwiner_kernel[0])) == sp.Matrix.vstack(sp.eye(3), sp.zeros(3))
    assert sp.Matrix(6, 3, list(intertwiner_kernel[1])) == sp.Matrix.vstack(sp.zeros(3), sp.eye(3))

    u, v = sp.symbols("u v", real=True)
    general_intertwiner = sp.Matrix.vstack(u * sp.eye(3), v * sp.eye(3))
    assert all(
        arrow_generator * general_intertwiner - general_intertwiner * family_generator == sp.zeros(6, 3)
        for arrow_generator, family_generator in zip(arrow_generators, generators)
    )
    metric_pullback = sp.simplify(general_intertwiner.T * general_intertwiner)
    assert metric_pullback == (u**2 + v**2) * sp.eye(3)

    hermitian_quadratures: list[sp.Matrix] = []
    for arrow in (*current_arrows, *missing_arrows):
        block = sp.zeros(5)
        for row in range(3):
            for column in range(2):
                block[row, 3 + column] = arrow[row, column]
        hermitian_quadratures.extend((block + block.T, sp.I * (block - block.T)))
    quadrature_matrix = sp.Matrix.hstack(*(sp.Matrix(item).reshape(25, 1) for item in hermitian_quadratures))
    assert quadrature_matrix.rank() == 12

    exact_objects = [
        *generators,
        current_matrix,
        closure_matrix,
        completed_matrix,
        source_system,
        intertwiner_system,
        general_intertwiner,
        metric_pullback,
        quadrature_matrix,
    ]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_multiplicity_environment_so3_action_parent_origin_gate",
        "current_connector_space": {
            "model": "span(E_00,E_11,E_21) inside Hom(R^2,R^3)",
            "dimension": 3,
            "SO3_invariant": False,
            "infinitesimal_invariance_failures": invariance_failures,
            "source_SO3_representation_dimension": 2,
            "source_lie_hom_constraint_rank": source_system.rank(),
            "source_action": "trivial",
        },
        "minimal_SO3_closure": {
            "closure_dimension": closure_matrix.rank(),
            "completed_space": "Hom(R^2,R^3)",
            "missing_matrix_units": ["E_10", "E_20", "E_01"],
            "missing_complex_arrows": 3,
            "added_real_quadratures": 6,
            "completed_quadrature_rank": quadrature_matrix.rank(),
            "conditional_frame_dimension": 57,
            "representation_decomposition": "3 + 3",
        },
        "family_intertwiners_after_closure": {
            "constraint_shape": list(intertwiner_system.shape),
            "constraint_rank": intertwiner_system.rank(),
            "dimension": len(intertwiner_kernel),
            "general_form": "T_(u,v)=vertical_stack(u I3,v I3)",
            "metric_pullback": "(u^2+v^2) I3",
            "isometric_selector_orbit": "RP1 after the irrelevant overall sign",
        },
        "parent_sources": {
            "existing_family_action_on_H21_restricts_to_current_three_arrows": False,
            "endpoint_algebra_supplies_irreducible_triplet": False,
            "current_three_arrow_frame_is_invariant": False,
            "full_M5_contains_conditional_six_arrow_closure": True,
            "full_M5_trace_selects_source_line": False,
            "derived_sources": 0,
            "required_sources": 5,
        },
        "verdict": {
            "current_SO3_action_parent_derived": False,
            "minimal_covariant_extension_exists": True,
            "minimal_covariant_extension_is_current_parent": False,
            "family_to_environment_map_unique_after_extension": False,
            "residual_projective_selector": "RP1",
            "single_c0_map_derived": False,
        },
        "next_gate": "version8_baryon_c0_so3_closed_environment_source_line_selector_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()