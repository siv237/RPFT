#!/usr/bin/env python3
"""Exact classification of gauge-covariant old-new connector multiplets."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_old_new_gauge_covariant_connector_classification_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_full_noise_trace_frame import full_noise_frame  # noqa: E402
from s2t.proofdsl.examples.version8_gauge_twirl_kraus import _endpoint_gauge_generators  # noqa: E402


def extend_old(matrix: sp.MatrixBase) -> sp.ImmutableMatrix:
    result = sp.zeros(23)
    result[:21, :21] = matrix
    return sp.ImmutableMatrix(result)


def dirac_quadratures(v: sp.MatrixBase) -> tuple[sp.ImmutableMatrix, sp.ImmutableMatrix]:
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
        (ROOT / "s2t/results/s2t_v8_baryon_c0_extended_45_frame_fixed_algebra_and_dynamics_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["commutant"]["full_fixed_algebra_dimension"] == 2
    assert previous["next_gate"] == "version8_baryon_c0_old_new_gauge_covariant_connector_classification_gate"

    generators = tuple(_endpoint_gauge_generators())
    semisimple = generators[:-1]
    hypercharge = generators[-1]
    gamma21 = sp.diag(*([-1] * 11 + [1] * 10))
    gamma_n = sp.diag(1, -1)

    variables = sp.symbols("v0:42")
    generic = sp.Matrix(21, 2, variables)
    equations = []
    for generator in semisimple:
        equations.extend(list(generator * generic))
    equations.extend(list((hypercharge + sp.eye(21)) * generic))
    equations.extend(list(gamma21 * generic + generic * gamma_n))
    system, _ = sp.linear_eq_to_matrix(equations, variables)
    nullspace = system.nullspace()
    assert system.shape == (546, 42)
    assert system.rank() == 39
    assert len(nullspace) == 3

    support = []
    basis = []
    for vector in nullspace:
        matrix = sp.ImmutableMatrix(21, 2, list(vector))
        basis.append(matrix)
        support.append([(i, j) for i in range(21) for j in range(2) if matrix[i, j] != 0])
    assert support == [[(8, 0)], [(17, 1)], [(18, 1)]]

    v = basis[0]
    c1, c2 = dirac_quadratures(v)
    gamma23 = sp.ImmutableMatrix(sp.diag(gamma21, gamma_n))
    assert gamma23 * c1 + c1 * gamma23 == sp.zeros(23)
    assert gamma23 * c2 + c2 * gamma23 == sp.zeros(23)
    assert sp.conjugate(c1) == c1
    assert sp.conjugate(c2) == -c2

    extended_generators = tuple(extend_old(item) for item in generators)
    assert all(generator * c1 - c1 * generator == sp.zeros(23) for generator in extended_generators[:-1])
    assert all(generator * c2 - c2 * generator == sp.zeros(23) for generator in extended_generators[:-1])
    y23 = extended_generators[-1]
    assert sp.I * (y23 * c1 - c1 * y23) == -c2
    assert sp.I * (y23 * c2 - c2 * y23) == c1

    old23 = tuple(extend_old(item) for item in full_noise_frame())
    pauli23 = []
    for sigma in (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    ):
        item = sp.zeros(23); item[21:23, 21:23] = sigma
        pauli23.append(sp.ImmutableMatrix(item))
    frame45 = old23 + tuple(pauli23)
    assert all(sp.trace(item.H * c1) == 0 and sp.trace(item.H * c2) == 0 for item in frame45)
    connector_metric = sp.Matrix(
        [[sp.trace(left.H * right) for right in (c1, c2)] for left in (c1, c2)]
    )
    assert connector_metric == 2 * sp.eye(2)
    connector_flat = sp.Matrix.hstack(sp.Matrix(list(c1)), sp.Matrix(list(c2)))
    assert connector_flat.rank() == 2

    p21 = sp.ImmutableMatrix(sp.diag(*([1] * 21 + [0, 0])))
    pn = sp.ImmutableMatrix(sp.diag(*([0] * 21 + [1, 1])))
    central_basis = (p21 / sp.sqrt(21), pn / sp.sqrt(2))
    central_matrix = sp.Matrix(
        [
            [sp.simplify(sp.trace(left.H * (-lindblad((c1, c2), right)))) for right in central_basis]
            for left in central_basis
        ]
    )
    expected = sp.Matrix(
        [[sp.Rational(2, 21), -sp.sqrt(42) / 21], [-sp.sqrt(42) / 21, 1]]
    )
    assert central_matrix == expected
    assert central_matrix.rank() == 1
    assert central_matrix.nullspace()[0] == sp.Matrix([sp.sqrt(42) / 2, 1])

    alpha, beta = sp.symbols("alpha beta")
    central_observable = alpha * p21 + beta * pn
    central_commutator = central_observable * c1 - c1 * central_observable
    central_bridge = p21 * c1 - c1 * p21
    assert central_commutator == (alpha - beta) * central_bridge
    assert central_bridge != sp.zeros(23)

    exact_objects = [*system, *c1, *c2, *connector_metric, *central_matrix]
    assert not any(atom.is_Float for obj in exact_objects for atom in sp.preorder_traversal(obj))

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_old_new_gauge_covariant_connector_classification_gate",
        "classification": {
            "linear_system_shape": [546, 42],
            "linear_system_rank": 39,
            "complex_solution_dimension": 3,
            "basis_support": support,
            "real_projective_family": "RP^2",
            "charged_singlet_multiplicity": 3,
        },
        "minimal_connector_frame": {
            "real_dimension": 2,
            "odd": True,
            "SU3_SU2_invariant": True,
            "U1_covariant_rotation": ["i[Y,C1]=-C2", "i[Y,C2]=C1"],
            "real_span_closed": True,
            "trace_metric": "2 I2",
            "extended_frame_rank": 47,
        },
        "central_dynamics": {
            "dirichlet_matrix": [["2/21", "-sqrt(42)/21"], ["-sqrt(42)/21", "1"]],
            "dirichlet_rank": 1,
            "old_fixed_dimension": 2,
            "new_fixed_dimension": 1,
            "fixed_algebra": "C I_23",
            "primitive_for_every_positive_rate": True,
        },
        "selector_boundary": {
            "connector_direction_selected": False,
            "positive_rate_selected": False,
            "conditional_c0": 4,
            "physical_c0_derived": False,
        },
        "verdict": {
            "gauge_covariant_old_new_connector_exists": True,
            "minimal_two_quadrature_extension_is_primitive": True,
            "unique_connector_derived": False,
            "parent_selector_required": True,
        },
        "next_gate": "version8_baryon_c0_connector_multiplicity_and_rate_parent_selector_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()