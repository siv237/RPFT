#!/usr/bin/env python3
"""Exact parent-origin audit for the edge-coherence radius portal."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_edge_coherence_radius_portal_parent_origin_gate_results.json"


def wedge_representation(generator: sp.Matrix) -> sp.Matrix:
    pairs = ((0, 1), (0, 2), (1, 2))
    result = sp.zeros(3)
    for column, (i, j) in enumerate(pairs):
        for a in range(3):
            coefficient = generator[a, i]
            if coefficient:
                if a == j:
                    continue
                pair = tuple(sorted((a, j)))
                sign = 1 if a < j else -1
                result[pairs.index(pair), column] += sign * coefficient
        for a in range(3):
            coefficient = generator[a, j]
            if coefficient:
                if i == a:
                    continue
                pair = tuple(sorted((i, a)))
                sign = 1 if i < a else -1
                result[pairs.index(pair), column] += sign * coefficient
    return result


def commutant_dimension(generators: list[sp.Matrix]) -> int:
    variables = sp.symbols("z0:9")
    z = sp.Matrix(3, 3, variables)
    equations = []
    for generator in generators:
        equations.extend(list(z * generator - generator * z))
    matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    return 9 - matrix.rank()


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_existing_scalar_source_carrier_classification_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_edge_coherence_radius_portal_parent_origin_gate"
    assert previous["classification"]["coherence_invariant_value"] == 3

    entries = sp.symbols("b0:6", real=True)
    b = sp.Matrix(2, 3, entries)
    a_b = sp.Matrix(6, 1, entries)
    pairs = ((0, 1), (0, 2), (1, 2))
    c_b = sp.zeros(3, 6)
    for output, (i, j) in enumerate(pairs):
        for row in range(2):
            for column in range(3):
                variation = sp.zeros(2, 3)
                variation[row, column] = 1
                c_b[output, 3 * row + column] = sp.Rational(1, 2) * (
                    variation[0, i] * b[1, j]
                    + b[0, i] * variation[1, j]
                    - variation[0, j] * b[1, i]
                    - b[0, j] * variation[1, i]
                )

    d_b = sp.zeros(10)
    d_b[0, 1:7] = a_b.T
    d_b[1:7, 0] = a_b
    d_b[1:7, 7:10] = c_b.T
    d_b[7:10, 1:7] = c_b
    radius = sum(entry**2 for entry in entries)
    determinant = (b * b.T).det()

    middle_weight = sp.symbols("q", real=True)
    q_general = sp.diag(
        sp.Rational(-3, 4),
        *([middle_weight] * 6),
        *([sp.Rational(1, 4)] * 3),
    )
    assert sp.trace(q_general) == 6 * middle_weight
    assert sp.solve(sp.Eq(sp.trace(q_general), 0), middle_weight) == [0]
    q_hat = q_general.subs(middle_weight, 0)
    assert sp.trace(q_hat) == 0
    assert sp.simplify(sp.trace(q_hat * d_b**2) + sp.Rational(5, 8) * radius) == 0

    lam = sp.symbols("lambda", real=True)
    total = d_b + lam * q_hat
    trace_two = sp.factor(sp.trace(total**2))
    trace_three = sp.factor(sp.trace(total**3))
    trace_four = sp.factor(sp.trace(total**4))
    assert sp.simplify(trace_two - 3 * radius - sp.Rational(3, 4) * lam**2) == 0
    assert sp.simplify(trace_three + sp.Rational(3, 8) * lam * (lam**2 + 5 * radius)) == 0
    expected_four = (
        sp.Rational(9, 4) * radius**2
        + sp.Rational(15, 4) * determinant
        + sp.Rational(19, 8) * lam**2 * radius
        + sp.Rational(21, 64) * lam**4
    )
    assert sp.simplify(trace_four - expected_four) == 0
    assert sp.diff(trace_two, lam).subs(lam, 0) == 0
    assert sp.diff(trace_four, lam).subs(lam, 0) == 0

    cubic_coefficient = sp.symbols("c3", real=True)
    cubic_parent = sp.expand(cubic_coefficient * trace_three)
    portal_coefficient = sp.Rational(15, 8) * cubic_coefficient
    self_cubic_coefficient = sp.Rational(3, 8) * cubic_coefficient
    assert sp.expand(cubic_parent + portal_coefficient * lam * radius + self_cubic_coefficient * lam**3) == 0
    assert portal_coefficient / self_cubic_coefficient == 5
    assert (-portal_coefficient * lam * radius).subs(radius, 3) == -sp.Rational(45, 8) * cubic_coefficient * lam

    # The coherence three-corner is 1+2 under the physical channel block group.
    matrix_units = []
    for i, j in ((0, 0), (0, 1), (1, 0), (1, 1), (2, 2)):
        unit = sp.zeros(3)
        unit[i, j] = 1
        matrix_units.append(unit)
    wedge_generators = [wedge_representation(unit) for unit in matrix_units]
    channel_commutant = commutant_dimension(wedge_generators)
    assert channel_commutant == 2

    l12 = sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]])
    l13 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    l23 = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]])
    family_commutant = commutant_dimension([l12, l13, l23])
    assert family_commutant == 1
    assert channel_commutant != family_commutant

    exact_objects = [d_b, q_hat, trace_two, trace_three, trace_four, cubic_parent]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_edge_coherence_radius_portal_parent_origin_gate",
        "common_algebraic_carrier": {
            "coherence_chain_dimensions": [1, 6, 3],
            "central_corner_dimensions": [1, 3],
            "general_extension": "diag(-3/4,q I6,(1/4)I3)",
            "tracelessness_equation": "6q=0",
            "unique_middle_weight": 0,
            "Qhat": "diag(-3/4,0_6,(1/4)I3)",
        },
        "exact_moments": {
            "T": "Tr(BB*)",
            "d": "det(BB*)",
            "Tr_Qhat_D2": "-5T/8",
            "Tr_X2": "3T+3lambda^2/4",
            "Tr_X3": "-15lambda T/8-3lambda^3/8",
            "Tr_X4": "9T^2/4+15d/4+19lambda^2 T/8+21lambda^4/64",
            "X": "D_B+lambda Qhat",
        },
        "portal_shape": {
            "conditional_parent_term": "c3 Tr(X^3)",
            "portal": "-(15c3/8) lambda T",
            "lambda_self_cubic": "-(3c3/8)lambda^3",
            "fixed_portal_to_self_cubic_ratio": 5,
            "source_at_T_equals_3": "j_eff=45c3/8",
            "even_moments_generate_linear_portal": False,
            "Real_half_trace_would_cancel_cubic_shape": False,
        },
        "typing_obstruction": {
            "coherence_three_corner": "Lambda^2(C2+C1)=C1+C2 under U(2)_{eX} x U(1)_Y",
            "coherence_corner_commutant_dimension": channel_commutant,
            "central_family_corner": "irreducible standard SO(3) triplet",
            "family_triplet_commutant_dimension": family_commutant,
            "canonical_typed_identification_exists": False,
            "dimension_match_is_sufficient": False,
        },
        "ledgers": {
            "algebraic_shape_satisfied": 4,
            "algebraic_shape_tested": 4,
            "parent_origin_satisfied": 0,
            "parent_origin_tested": 2,
            "missing_parent_inputs": ["typed corner intertwiner", "nonzero cubic parent coefficient c3"],
        },
        "verdict": {
            "portal_shape_exists": True,
            "portal_generated_by_inherited_even_spectral_parent": False,
            "coherence_corner_is_current_family_triplet": False,
            "portal_parent_origin_derived": False,
            "physical_gap_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_coherence_even_corner_family_triplet_intertwiner_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()