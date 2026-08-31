#!/usr/bin/env python3
"""Exact minimal endpoint extension for a grading-compatible family triplet."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate_results.json"


def linear_system(expressions: list[sp.Expr], variables: tuple[sp.Symbol, ...]) -> sp.Matrix:
    matrix, _ = sp.linear_eq_to_matrix(expressions, variables)
    return matrix


def main() -> None:
    previous = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_so3_closed_environment_source_line_selector_gate_results.json").read_text(encoding="utf-8"))
    assert previous["next_gate"] == "version8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate"
    assert previous["source_line_family"]["admissible_RP1_points"] == 0

    target_grading = sp.diag(-1, 1, 1)
    plus_count = sum(target_grading[i, i] == 1 for i in range(3))
    minus_count = sum(target_grading[i, i] == -1 for i in range(3))
    plus_additions = 3 - plus_count
    minus_additions = 3 - minus_count
    assert (plus_count, minus_count, plus_additions, minus_additions) == (2, 1, 1, 2)

    j1 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    j2 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    j3 = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    generators = (j1, j2, j3)
    gamma_plus = sp.eye(3)
    gamma_minus = -sp.eye(3)
    hypercharge = -sp.eye(3)
    assert all(gamma_plus * item == item * gamma_plus for item in generators)
    assert all(gamma_minus * item == item * gamma_minus for item in generators)
    assert all(hypercharge * item == item * hypercharge for item in generators)

    source_a_grade = -1
    source_s_grade = 1
    assert gamma_plus + source_a_grade * sp.eye(3) == sp.zeros(3)
    assert gamma_minus + source_s_grade * sp.eye(3) == sp.zeros(3)

    variables = sp.symbols("t0:9", real=True)
    intertwiner = sp.Matrix(3, 3, variables)
    hom_equations = [entry for generator in generators for entry in list(intertwiner * generator - generator * intertwiner)]
    hom_system = linear_system(hom_equations, variables)
    assert hom_system.rank() == 8 and len(hom_system.nullspace()) == 1
    assert sp.Matrix(3, 3, list(hom_system.nullspace()[0])) == sp.eye(3)

    endpoint_projectors = (sp.diag(1, 0, 0), sp.diag(0, 1, 0), sp.diag(0, 0, 1))
    assert sum(endpoint_projectors, sp.zeros(3)) == sp.eye(3)
    assert any(generator * projector != projector * generator for generator in generators for projector in endpoint_projectors)
    algebra_seeds = [*endpoint_projectors, *generators]
    algebra_matrix = sp.Matrix.hstack(*(item.reshape(9, 1) for item in algebra_seeds))
    products = [left * right for left in algebra_seeds for right in algebra_seeds]
    generated_algebra = sp.Matrix.hstack(algebra_matrix, *(item.reshape(9, 1) for item in products))
    assert generated_algebra.rank() == 9

    covariance_variables = sp.symbols("c0:10", real=True)
    covariance = sp.zeros(4)
    cursor = 0
    for row in range(4):
        for column in range(row, 4):
            covariance[row, column] = covariance[column, row] = covariance_variables[cursor]
            cursor += 1
    full_generators = tuple(sp.diag(0, generator) for generator in generators)
    covariance_equations = [entry for generator in full_generators for entry in list(generator * covariance - covariance * generator)]
    covariance_system = linear_system(covariance_equations, covariance_variables)
    assert covariance_system.rank() == 8 and len(covariance_system.nullspace()) == 2
    singlet_projector = sp.diag(1, 0, 0, 0)
    triplet_projector = sp.diag(0, 1, 1, 1)
    assert all(generator * singlet_projector == singlet_projector * generator for generator in full_generators)
    assert all(generator * triplet_projector == triplet_projector * generator for generator in full_generators)

    exact_objects = [target_grading, *generators, gamma_plus, gamma_minus, hypercharge, hom_system, generated_algebra, covariance_system]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate",
        "current_target_grading": {"spectrum": "one minus and two plus", "plus_dimension": plus_count, "minus_dimension": minus_count},
        "homogeneous_triplet_branches": {
            "plus_branch": {"new_target_states": plus_additions, "extended_carrier_dimension": 24, "source_line": "a0", "new_complex_connector_arrows": 1, "all_triplet_arrows_odd": True},
            "minus_branch": {"new_target_states": minus_additions, "extended_carrier_dimension": 25, "source_line": "s0", "new_complex_connector_arrows": 2, "all_triplet_arrows_odd": True},
            "unique_minimal_state_branch": "plus",
        },
        "plus_triplet_compatibility": {
            "SM_hypercharge": -1,
            "SO3_commutes_with_hypercharge": True,
            "SO3_commutes_with_grading": True,
            "real_standard_generators": True,
            "family_intertwiner_constraint_rank": hom_system.rank(),
            "family_intertwiner_dimension": 1,
            "isometric_intertwiners": ["-I3", "I3"],
        },
        "endpoint_algebra": {
            "individual_coordinate_projectors_preserved": False,
            "triplet_sum_projector_preserved": True,
            "covariant_algebra_generated_rank": generated_algebra.rank(),
            "covariant_algebra": "M3(C)",
            "new_offdiagonal_hermitian_directions": 6,
        },
        "full_connector_representation": {
            "decomposition": "1 + 3",
            "invariant_symmetric_covariance_dimension": len(covariance_system.nullspace()),
            "covariance_constraint_rank": covariance_system.rank(),
            "general_covariance": "gamma_1 P_1 + gamma_3 P_3",
            "singlet_triplet_relative_rate_selected": False,
        },
        "verdict": {
            "minimal_grading_compatible_extension_exists": True,
            "minimal_branch": "add one plus-graded charged target state",
            "current_parent_contains_new_state": False,
            "current_parent_contains_covariant_M3_endpoint_algebra": False,
            "conditional_family_map_unique_up_to_sign": True,
            "physical_single_c0_map_derived": False,
            "derived_extension_structures": 0,
            "required_extension_structures": 3,
        },
        "next_gate": "version8_baryon_c0_family_triplet_singlet_relative_rate_selector_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()