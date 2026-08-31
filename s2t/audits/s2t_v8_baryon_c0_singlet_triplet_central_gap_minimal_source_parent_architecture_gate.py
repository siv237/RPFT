#!/usr/bin/env python3
"""Exact audit of the minimal source-parent architecture for the central gap."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_minimal_source_parent_architecture_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_coefficient_selector_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_minimal_source_parent_architecture_gate"
    assert previous["verdict"]["minimal_missing_parent_structure"] == "odd central source plus even stiffness"

    lam, c0, c1, c2 = sp.symbols("lambda c0 c1 c2", real=True)
    general_quadratic = c0 + c1 * lam + c2 * lam**2
    assert sp.diff(general_quadratic, lam) == c1 + 2 * c2 * lam
    assert sp.diff(general_quadratic, lam, 2) == 2 * c2
    quadratic_minimizer = -c1 / (2 * c2)
    assert sp.simplify(sp.diff(general_quadratic, lam).subs(lam, quadratic_minimizer)) == 0

    m2 = sp.symbols("m2", positive=True)
    j = sp.symbols("j", real=True, nonzero=True)
    source_parent = m2 * lam**2 / 2 - j * lam
    lam_star = j / m2
    assert sp.simplify(sp.diff(source_parent, lam).subs(lam, lam_star)) == 0
    assert sp.diff(source_parent, lam, 2) == m2
    completed_square = m2 * (lam - lam_star) ** 2 / 2 - j**2 / (2 * m2)
    assert sp.simplify(source_parent - completed_square) == 0
    assert sp.simplify(source_parent.subs(lam, lam_star) + j**2 / (2 * m2)) == 0

    identity = sp.eye(4)
    p1 = sp.diag(1, 0, 0, 0)
    p3 = identity - p1
    q = p3 - sp.Rational(3, 4) * identity
    q_norm_sq = sp.trace(q.T * q)
    assert q_norm_sq == sp.Rational(3, 4)
    h0 = lam * q
    operator_parent = (
        m2 * sp.trace(h0.T * h0) / (2 * q_norm_sq)
        - j * sp.trace(q.T * h0) / q_norm_sq
    )
    assert sp.simplify(operator_parent - source_parent) == 0

    grading = sp.diag(-1, 1, 1, 1)
    generators3 = [
        sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]]),
    ]
    generators4 = [sp.diag(0, generator) for generator in generators3]
    assert q * grading == grading * q
    assert all(q * generator == generator * q for generator in generators4)
    assert q == q.conjugate()
    assert p1.rank() == 1 and p3.rank() == 3

    scale = sp.symbols("a", positive=True)
    assert sp.simplify((scale * j) / (scale * m2) - lam_star) == 0
    scaled_curvature = scale * m2
    scaled_on_shell = -scale * j**2 / (2 * m2)
    assert scaled_curvature != m2
    assert scaled_on_shell != -j**2 / (2 * m2)

    witness_1 = {m2: sp.Integer(1), j: sp.Integer(1)}
    witness_2 = {m2: sp.Integer(2), j: sp.Integer(2)}
    assert sp.simplify(lam_star.subs(witness_1)) == 1
    assert sp.simplify(lam_star.subs(witness_2)) == 1
    assert m2.subs(witness_1) == 1 and m2.subs(witness_2) == 2

    kappa, ell = sp.symbols("kappa ell", real=True)
    reconstructed = source_parent.subs({m2: kappa, j: kappa * ell})
    assert sp.simplify(sp.diff(reconstructed, lam).subs(lam, ell)) == 0
    assert sp.diff(reconstructed, lam, 2) == kappa

    exact_objects = [general_quadratic, source_parent, completed_square, q, operator_parent]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_minimal_source_parent_architecture_gate",
        "quadratic_classification": {
            "general_form": "c0+c1 lambda+c2 lambda^2",
            "bounded_and_unique_condition": "c2>0",
            "nonzero_signed_minimum_condition": "c1!=0",
            "minimizer": "-c1/(2 c2)",
            "constant_is_irrelevant": True,
            "linear_only_is_bounded_below": False,
            "even_quadratic_selects_nonzero_sign": False,
            "minimal_nonconstant_monomials": 2,
            "minimal_degree": 2,
        },
        "source_parent": {
            "potential": "m2 lambda^2/2-j lambda",
            "assumptions": ["m2>0", "j!=0"],
            "unique_global_minimum": "lambda*=j/m2",
            "hessian": "m2",
            "on_shell_value": "-j^2/(2 m2)",
            "completed_square": "m2(lambda-j/m2)^2/2-j^2/(2m2)",
        },
        "operator_lift": {
            "central_direction": "Q=P3-3 I4/4",
            "trace_Q2": "3/4",
            "functional": "m2 Tr((h0)^2)/(2 Tr(Q^2))-j Tr(Q h0)/Tr(Q^2)",
            "pullback_on_h0_equals_lambda_Q": "m2 lambda^2/2-j lambda",
            "commutes_with_family_so3": True,
            "commutes_with_grading": True,
            "real_compatible": True,
            "sign_flip_is_required_structural_symmetry": False,
            "rank_P1": 1,
            "rank_P3": 3,
        },
        "identifiability": {
            "parameter_orbit": "(m2,j)->(a m2,a j), a>0",
            "vacuum_lambda_invariant": True,
            "hessian_scales_by_a": True,
            "on_shell_depth_scales_by_a": True,
            "same_vacuum_witnesses": [
                {"m2": 1, "j": 1, "lambda_star": 1, "hessian": 1},
                {"m2": 2, "j": 2, "lambda_star": 1, "hessian": 2},
            ],
            "vacuum_plus_curvature_reconstruction": ["m2=kappa", "j=kappa lambda_star"],
        },
        "architecture_ledger": {
            "bounded_below": True,
            "unique_global_minimum": True,
            "nonzero_minimum_if_j_nonzero": True,
            "signed_minimum": True,
            "operator_lift": True,
            "family_grading_real_compatibility": True,
            "minimal_polynomial_degree": True,
            "satisfied_requirements": 7,
            "tested_requirements": 7,
        },
        "parent_origin_ledger": {
            "stiffness_m2_derived": False,
            "source_j_derived": False,
            "derived_inputs": 0,
            "tested_inputs": 2,
        },
        "verdict": {
            "minimal_architecture_conditionally_admitted": True,
            "physical_gap_derived": False,
            "vacuum_alone_identifies_parent": False,
            "new_data": ["odd central source j", "positive stiffness m2"],
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_source_stiffness_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()