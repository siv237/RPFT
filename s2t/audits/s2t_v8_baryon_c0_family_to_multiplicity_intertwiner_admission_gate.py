#!/usr/bin/env python3
"""Exact representation-theoretic audit of the family-to-multiplicity map."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_family_to_multiplicity_intertwiner_admission_gate_results.json"


def linear_system(expressions: list[sp.Expr], variables: tuple[sp.Symbol, ...]) -> sp.Matrix:
    matrix, _ = sp.linear_eq_to_matrix(expressions, variables)
    return matrix


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_multiplicity_environment_hamiltonian_parent_origin_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["verdict"]["derived_parent_origins"] == 0
    assert previous["next_gate"] == "version8_baryon_c0_family_to_multiplicity_intertwiner_admission_gate"

    j1 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    j2 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    j3 = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    generators = (j1, j2, j3)
    variables = sp.symbols("t0:9", real=True)
    generic = sp.Matrix(3, 3, variables)

    current_equations: list[sp.Expr] = []
    for generator in generators:
        current_equations.extend(list(generic * generator))
    current_system = linear_system(current_equations, variables)
    assert current_system.shape == (27, 9)
    assert current_system.rank() == 9
    assert current_system.nullspace() == []

    rotation = sp.diag(1, -1, -1)
    cycle = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    assert rotation**2 == sp.eye(3)
    assert cycle**3 == sp.eye(3)
    assert (rotation * cycle) ** 3 == sp.eye(3)
    a4_equations = list(generic * rotation - generic) + list(generic * cycle - generic)
    a4_system = linear_system(a4_equations, variables)
    assert a4_system.shape == (18, 9)
    assert a4_system.rank() == 9
    assert a4_system.nullspace() == []

    promoted_equations: list[sp.Expr] = []
    for generator in generators:
        promoted_equations.extend(list(generic * generator - generator * generic))
    promoted_system = linear_system(promoted_equations, variables)
    promoted_kernel = promoted_system.nullspace()
    assert promoted_system.rank() == 8
    assert len(promoted_kernel) == 1
    assert sp.Matrix(3, 3, list(promoted_kernel[0])) == sp.eye(3)

    kappa = sp.symbols("kappa", real=True)
    intertwiner = kappa * sp.eye(3)
    isometry_residual = sp.simplify(intertwiner.T * intertwiner - sp.eye(3))
    assert sp.solve(list(isometry_residual), kappa) == [(-1,), (1,)]

    endpoint_projectors = tuple(
        sp.diag(*[1 if i == j else 0 for i in range(3)]) for j in range(3)
    )
    diagonal_variables = sp.diag(*sp.symbols("d0:3", real=True))
    assert all(diagonal_variables * item - item * diagonal_variables == sp.zeros(3) for item in endpoint_projectors)
    assert any(generator * endpoint_projectors[0] - endpoint_projectors[0] * generator != sp.zeros(3) for generator in generators)

    r4 = sp.Matrix(
        [
            [sp.Rational(27, 2), -2, sp.Rational(3, 2)],
            [-2, sp.Rational(35, 2), sp.Rational(-5, 2)],
            [sp.Rational(3, 2), sp.Rational(-5, 2), 17],
        ]
    )
    assert sp.simplify(intertwiner * r4 * intertwiner.T - kappa**2 * r4) == sp.zeros(3)

    exact_objects = [*generators, current_system, rotation, cycle, a4_system, promoted_system, intertwiner, r4]
    assert not any(obj.atoms(sp.Float) for obj in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_family_to_multiplicity_intertwiner_admission_gate",
        "current_types": {
            "family": "standard 3 of SO(3)_fam",
            "multiplicity_environment": "three trivial real lines",
            "SO3_constraint_shape": [27, 9],
            "SO3_constraint_rank": 9,
            "SO3_intertwiner_dimension": 0,
        },
        "tetrahedral_residual": {
            "generators": ["diag(1,-1,-1)", "cyclic permutation C3"],
            "relations": ["R^2=I", "C^3=I", "(RC)^3=I"],
            "constraint_shape": [18, 9],
            "constraint_rank": 9,
            "A4_intertwiner_dimension": 0,
        },
        "endpoint_compatibility": {
            "coordinate_projector_commutant": "diagonal algebra D3",
            "orthogonal_part": "diag(+-1,+-1,+-1)",
            "connected_SO3_action_preserving_each_projector": "trivial",
            "standard_action_preserves_endpoint_projectors": False,
        },
        "conditional_extension": {
            "promoted_target_type": "standard 3 of SO(3)",
            "commutant_constraint_rank": 8,
            "intertwiner_dimension": 1,
            "intertwiner_line": "R I3",
            "isometric_solutions": ["-I3", "I3"],
            "transported_R4_plus": "R4_plus",
            "endpoint_algebra_extension_required": True,
        },
        "verdict": {
            "nonzero_current_intertwiner_exists": False,
            "forgetful_M3_map_is_typed": False,
            "conditional_extension_exists": True,
            "new_family_action_on_environment_required": True,
            "new_covariant_endpoint_lift_required": True,
            "derived_extension_structures": 0,
            "required_extension_structures": 2,
            "single_c0_map_derived": False,
        },
        "next_gate": "version8_baryon_c0_multiplicity_environment_so3_action_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()