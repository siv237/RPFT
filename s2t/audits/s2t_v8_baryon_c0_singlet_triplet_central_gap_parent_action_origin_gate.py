#!/usr/bin/env python3
"""Exact parent-origin audit for the singlet--triplet central gap."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_parent_action_origin_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_weight_minimal_hamiltonian_data_gate_results.json").read_text(encoding="utf-8")
    )
    extension = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate_results.json").read_text(encoding="utf-8")
    )
    family_origin = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_multiplicity_environment_so3_action_parent_origin_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_parent_action_origin_gate"
    assert extension["verdict"]["derived_extension_structures"] == 0
    assert family_origin["parent_sources"]["derived_sources"] == 0

    p1 = sp.diag(1, 0, 0, 0)
    p3 = sp.diag(0, 1, 1, 1)
    identity = sp.eye(4)
    grading = sp.diag(-1, 1, 1, 1)
    q = p3 - sp.Rational(3, 4) * identity

    j1 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    j2 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    j3 = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    generators = tuple(sp.diag(0, item) for item in (j1, j2, j3))
    casimir = -sum((item * item for item in generators), sp.zeros(4))
    assert casimir == 2 * p3

    centered_grading = grading - sp.trace(grading) * identity / 4
    centered_casimir = casimir - sp.trace(casimir) * identity / 4
    assert centered_grading == 2 * q
    assert centered_casimir == 2 * q
    assert sp.trace(q) == 0
    assert all(generator * q == q * generator for generator in generators)

    seed_span = sp.Matrix.hstack(identity.reshape(16, 1), grading.reshape(16, 1), casimir.reshape(16, 1), p3.reshape(16, 1))
    assert seed_span.rank() == 2

    h_singlet_low = p3
    h_triplet_low = p1
    assert all(value >= 0 for value in h_singlet_low.eigenvals())
    assert all(value >= 0 for value in h_triplet_low.eigenvals())
    assert h_singlet_low == q + sp.Rational(3, 4) * identity
    assert h_triplet_low == -q + sp.Rational(1, 4) * identity

    beta = sp.symbols("beta", positive=True)
    p_singlet_low = sp.simplify(1 / (1 + 3 * sp.exp(-beta)))
    p_triplet_low = sp.simplify(sp.exp(-beta) / (sp.exp(-beta) + 3))
    singlet_difference = sp.simplify(p_singlet_low - sp.Rational(1, 4))
    triplet_difference = sp.simplify(p_triplet_low - sp.Rational(1, 4))
    assert sp.simplify(singlet_difference - 3 * (sp.exp(beta) - 1) / (4 * (sp.exp(beta) + 3))) == 0
    assert sp.simplify(triplet_difference + 3 * (sp.exp(beta) - 1) / (4 * (3 * sp.exp(beta) + 1))) == 0

    lam = sp.symbols("lambda", real=True)
    h_general = lam * q
    gap = sp.simplify(h_general[1, 1] - h_general[0, 0])
    assert gap == lam

    a0, a1, a2, a3 = sp.symbols("a0:4", real=True)
    polynomial = a0 * identity + a1 * casimir + a2 * casimir**2 + a3 * casimir**3
    polynomial_gap = sp.simplify(polynomial[1, 1] - polynomial[0, 0])
    assert polynomial_gap == 2 * a1 + 4 * a2 + 8 * a3

    quadratic_even = sp.expand((lam * q) ** 2)
    assert quadratic_even == sp.expand((-lam * q) ** 2)
    assert sp.trace(q**2) == sp.Rational(3, 4)

    exact_objects = [p1, p3, identity, grading, q, *generators, casimir, centered_grading, centered_casimir, seed_span, h_singlet_low, h_triplet_low, h_general, polynomial, quadratic_even]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_parent_action_origin_gate",
        "canonical_central_direction": {
            "Q": "P3 - 3 I4/4",
            "trace": 0,
            "SO3_invariant": True,
            "seed_algebra_dimension": seed_span.rank(),
        },
        "grading_casimir_equivalence": {
            "grading": "diag(-1,+1,+1,+1)",
            "SO3_quadratic_casimir": "2 P3",
            "centered_grading": "2 Q",
            "centered_casimir": "2 Q",
            "same_gap_direction_mod_scalars": True,
        },
        "orientation_witnesses": {
            "singlet_low": {"hamiltonian": "P3", "gap": 1, "positive": True, "weight_relation": "p>1/4 for beta>0"},
            "triplet_low": {"hamiltonian": "P1", "gap": -1, "positive": True, "weight_relation": "p<1/4 for beta>0"},
            "positivity_selects_sign": False,
        },
        "coefficient_freedom": {
            "general_centered_hamiltonian": "lambda Q",
            "gap": "lambda",
            "theta": "beta lambda",
            "polynomial_Casimir_gap": "2 a1 + 4 a2 + 8 a3",
            "quadratic_action_detects_sign": False,
        },
        "architectural_status": {
            "current_parent_contains_family_SO3_action": False,
            "current_parent_contains_new_triplet_state": False,
            "current_parent_contains_covariant_M3_endpoint": False,
            "conditional_gap_shape_available": True,
            "conditional_shape_sources": ["grading", "SO3 Casimir", "central endpoint projector"],
        },
        "parent_origin_ledger": {
            "old_parent_restriction": False,
            "grading_as_energy_term": False,
            "SO3_Casimir_coefficient": False,
            "positivity_orientation": False,
            "even_quadratic_action_sign": False,
            "derived_gap_coefficients": 0,
            "tested_sources": 5,
        },
        "verdict": {
            "central_gap_direction_conditionally_unique": True,
            "central_gap_coefficient_selected": False,
            "central_gap_sign_selected": False,
            "theta_derived_by_current_parent": False,
            "physical_single_c0_map_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_coefficient_selector_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()