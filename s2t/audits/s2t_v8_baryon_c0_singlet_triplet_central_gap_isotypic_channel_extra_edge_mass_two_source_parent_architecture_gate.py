#!/usr/bin/env python3
"""Exact audit of the minimal two-source parent for the extra edge gaps."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_parent_architecture_gate_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_hamiltonian_parent_action_origin_gate_results.json").read_text())
    gate = "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_parent_architecture_gate"
    assert predecessor["next_gate"] == gate

    py = sp.diag(*([1] * 4 + [0] * 12))
    pu = sp.diag(*([0] * 4 + [1] * 6 + [0] * 6))
    pd = sp.diag(*([0] * 10 + [1] * 6))
    A, B = pu - pd, pu + pd - 3 * py
    assert sp.trace(A) == sp.trace(B) == sp.trace(A * B) == 0
    assert sp.trace(A * A) == 12 and sp.trace(B * B) == 48

    a, b, j_a, j_b = sp.symbols("a b j_A j_B", real=True)
    h = a * A + b * B
    potential = sp.trace(h * h) / 2 - j_a * a - j_b * b
    hessian = sp.hessian(potential, (a, b))
    assert hessian == sp.diag(12, 48)
    stationary = sp.solve([sp.diff(potential, a), sp.diff(potential, b)], (a, b))
    assert stationary == {a: j_a / 12, b: j_b / 48}
    completed = 6 * (a - j_a / 12) ** 2 + 24 * (b - j_b / 48) ** 2 - j_a ** 2 / 24 - j_b ** 2 / 96
    assert sp.expand(potential - completed) == 0

    gaps = sp.Matrix([a + 4 * b, -a + 4 * b]).subs(stationary)
    source_to_gap = sp.Matrix([[sp.Rational(1, 12), sp.Rational(1, 12)], [-sp.Rational(1, 12), sp.Rational(1, 12)]])
    assert gaps == source_to_gap * sp.Matrix([j_a, j_b])
    assert source_to_gap.det() == sp.Rational(1, 72) and source_to_gap.rank() == 2
    d_u, d_d = sp.symbols("Delta_u Delta_d", real=True)
    inverse = source_to_gap.inv() * sp.Matrix([d_u, d_d])
    assert inverse == sp.Matrix([6 * d_u - 6 * d_d, 6 * d_u + 6 * d_d])
    assert inverse.subs({d_u: 1, d_d: 2}) == sp.Matrix([-6, 18])
    delta = sp.symbols("delta", real=True)
    assert inverse.subs({d_u: delta, d_d: delta}) == sp.Matrix([0, 12 * delta])
    assert inverse.subs({d_u: 0, d_d: 0}) == sp.zeros(2, 1)

    one_source_rank_bound = 1
    general_stiffness_parameter_count = 3
    objects = [py, pu, pd, A, B, h, potential, hessian, completed, gaps, source_to_gap, inverse]
    assert not any(obj.atoms(sp.Float) for obj in objects)

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "inherited_trace_stiffness": {
            "basis": ["A=P_u-P_d", "B=P_u+P_d-3P_Y"],
            "gram_matrix": [[12, 0], [0, 48]],
            "potential": "6a^2+24b^2-j_A a-j_B b",
            "hessian": [[12, 0], [0, 48]],
            "positive_definite": True,
            "new_stiffness_parameters": 0,
            "general_symmetric_stiffness_parameters_avoided": general_stiffness_parameter_count,
        },
        "unique_minimum": {
            "a_star": "j_A/12",
            "b_star": "j_B/48",
            "minimum_value": "-j_A^2/24-j_B^2/96",
        },
        "source_gap_bijection": {
            "matrix": [["1/12", "1/12"], ["-1/12", "1/12"]],
            "determinant": "1/72",
            "rank": 2,
            "inverse": ["j_A=6(Delta_u-Delta_d)", "j_B=6(Delta_u+Delta_d)"],
        },
        "witnesses": {
            "zero_gaps_source": [0, 0],
            "equal_gaps_source": [0, "12 delta"],
            "gaps_1_2_source": [-6, 18],
        },
        "minimality": {
            "gap_plane_dimension": 2,
            "one_real_source_rank_bound": one_source_rank_bound,
            "minimal_real_source_count": 2,
            "source_data_decomposition": ["one magnitude", "one projective direction"],
        },
        "compatibility": {
            "central": True,
            "real": True,
            "grading_even": True,
            "gauge_invariant_linear_functional": True,
            "physical_beta_scale_fixed": False,
        },
        "ledgers": {
            "architecture_satisfied": 9,
            "architecture_tested": 9,
            "source_origin_satisfied": 0,
            "source_origin_tested": 2,
        },
        "verdict": {
            "two_source_parent_strictly_convex": True,
            "arbitrary_gap_pair_realized": True,
            "two_sources_necessary_and_sufficient": True,
            "source_coefficients_derived": False,
            "gap_pair_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_existing_scalar_carrier_classification_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()