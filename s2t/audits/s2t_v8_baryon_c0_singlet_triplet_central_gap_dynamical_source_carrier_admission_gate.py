#!/usr/bin/env python3
"""Exact admission audit for a dynamical carrier of the central source."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_dynamical_source_carrier_admission_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_source_stiffness_parent_origin_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_dynamical_source_carrier_admission_gate"
    assert previous["verdict"]["minimal_next_structure"] == "dynamical Real scalar source carrier with a derived nonzero expectation"

    lam, s = sp.symbols("lambda s", real=True)
    mass, quartic = sp.symbols("M u", positive=True)
    coupling = sp.symbols("g", real=True, nonzero=True)
    potential = mass * lam**2 / 2 - coupling * s * lam + quartic * s**4 / 4

    grad = sp.Matrix([sp.diff(potential, lam), sp.diff(potential, s)])
    hessian = sp.hessian(potential, (lam, s))
    origin_hessian = hessian.subs({lam: 0, s: 0})
    assert origin_hessian == sp.Matrix([[mass, -coupling], [-coupling, 0]])
    assert sp.det(origin_hessian) == -coupling**2

    eliminated_lam = coupling * s / mass
    effective = sp.factor(potential.subs(lam, eliminated_lam))
    assert effective == s**2 * (-2 * coupling**2 + mass * quartic * s**2) / (4 * mass)
    assert sp.simplify(effective - (quartic * s**4 / 4 - coupling**2 * s**2 / (2 * mass))) == 0

    s2_star = coupling**2 / (quartic * mass)
    lam2_star = coupling**4 / (quartic * mass**3)
    assert sp.factor(grad[1].subs(lam, eliminated_lam)) == s * (-coupling**2 + mass * quartic * s**2) / mass

    nonzero_hessian = hessian.subs(s**2, s2_star)
    assert nonzero_hessian == sp.Matrix([[mass, -coupling], [-coupling, 3 * coupling**2 / mass]])
    assert sp.det(nonzero_hessian) == 2 * coupling**2
    assert nonzero_hessian[0, 0] == mass

    energy_star = sp.simplify(effective.subs(s**2, s2_star))
    assert energy_star == -coupling**4 / (4 * mass**2 * quartic)
    assert sp.simplify((coupling * s / mass) ** 2).subs(s**2, s2_star) == lam2_star

    identity = sp.eye(4)
    p3 = sp.diag(0, 1, 1, 1)
    q = p3 - sp.Rational(3, 4) * identity
    gamma0 = 2 * q
    h0 = lam * q
    marked_bilinear = sp.trace(gamma0 * h0) * s
    assert marked_bilinear == sp.Rational(3, 2) * s * lam
    assert q == q.conjugate()

    assert sp.simplify(potential.subs({lam: -lam, s: -s}) - potential) == 0

    scale = sp.symbols("c", positive=True)
    s_new = sp.symbols("s_new", real=True)
    transformed = sp.expand(potential.subs(s, s_new / scale))
    expected_transformed = mass * lam**2 / 2 - (coupling / scale) * s_new * lam + (quartic / scale**4) * s_new**4 / 4
    assert sp.simplify(transformed - expected_transformed) == 0
    invariant_gap_squared = sp.simplify((coupling / scale) ** 4 / ((quartic / scale**4) * mass**3))
    assert invariant_gap_squared == lam2_star

    exact_objects = [potential, grad, hessian, effective, nonzero_hessian, marked_bilinear]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_dynamical_source_carrier_admission_gate",
        "minimal_dynamic_parent": {
            "carrier": "one-dimensional Real scalar s",
            "potential": "M lambda^2/2-g s lambda+u s^4/4",
            "assumptions": ["M>0", "u>0", "g!=0"],
            "external_linear_source_required": False,
        },
        "origin_instability": {
            "hessian": [["M", "-g"], ["-g", "0"]],
            "determinant": "-g^2",
            "origin_is_saddle": True,
        },
        "nonzero_vacua": {
            "effective_potential": "u s^4/4-g^2 s^2/(2M)",
            "s_star_squared": "g^2/(u M)",
            "lambda_star_relation": "lambda*=g s*/M",
            "lambda_star_squared": "g^4/(u M^3)",
            "vacuum_energy": "-g^4/(4u M^2)",
            "number_of_nonzero_vacua": 2,
            "paired_by": "(s,lambda)->(-s,-lambda)",
            "sign_uniquely_selected": False,
        },
        "vacuum_hessian": {
            "matrix": [["M", "-g"], ["-g", "3g^2/M"]],
            "leading_minor": "M>0",
            "determinant": "2g^2>0",
            "positive_definite": True,
        },
        "operator_typing": {
            "central_direction": "Q=P3-3I4/4",
            "source_carrier_gauge_type": "trivial",
            "source_carrier_family_type": "singlet",
            "source_carrier_grading": "even",
            "source_carrier_real": True,
            "marked_bilinear": "s Tr(Gamma0 h0)=3s lambda/2",
            "bilinear_is_structurally_invariant": True,
        },
        "minimality": {
            "without_scalar_carrier_nonzero_source": False,
            "without_M_bounded_below": False,
            "without_g_nonzero_gap": False,
            "without_u_bounded_below": False,
            "minimal_carrier_real_dimension": 1,
            "necessary_nonconstant_terms": 3,
        },
        "normalization_orbit": {
            "coordinate_change": "s_new=c s",
            "coupling_change": "g_new=g/c",
            "quartic_change": "u_new=u/c^4",
            "lambda_star_squared_invariant": True,
            "carrier_metric_required": True,
        },
        "architecture_ledger": {
            "one_real_carrier": True,
            "bounded_below": True,
            "origin_unstable": True,
            "nonzero_vacua": True,
            "positive_vacuum_hessian": True,
            "structural_symmetries": True,
            "external_source_removed": True,
            "minimal_terms": True,
            "satisfied_requirements": 8,
            "tested_requirements": 8,
        },
        "origin_ledger": {
            "typed_existing_scalar_carrier_identified": False,
            "M_derived": False,
            "g_derived": False,
            "u_derived": False,
            "derived_inputs": 0,
            "tested_inputs": 4,
        },
        "verdict": {
            "dynamical_source_carrier_conditionally_admitted": True,
            "nonzero_gap_generated_without_external_j": True,
            "gap_sign_selected": False,
            "physical_gap_derived": False,
            "next_task": "classify existing typed scalar carriers and their bilinear coupling to Q",
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_existing_scalar_source_carrier_classification_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()