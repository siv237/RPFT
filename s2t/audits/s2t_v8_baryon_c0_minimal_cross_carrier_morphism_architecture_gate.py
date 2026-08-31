#!/usr/bin/env python3
"""Exact classification of the minimal c0 cross-carrier morphism."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_minimal_cross_carrier_morphism_architecture_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_typed_internal_map_candidate_audit_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["admitted_count"] == 0
    assert previous["next_gate"] == "version8_baryon_c0_minimal_cross_carrier_morphism_architecture_gate"

    kappa, r, a, z, s = sp.symbols("kappa r a z s", positive=True)
    m = sp.Matrix([[kappa]])
    source_action = sp.Matrix([[1]])
    target_action = sp.Matrix([[1]])
    equivariance_residual = sp.simplify(target_action * m - m * source_action)
    assert equivariance_residual == sp.zeros(1)

    pole_hessian = z + a * kappa * r
    c0 = sp.simplify((pole_hessian - z) / a)
    assert c0 == kappa * r
    orbit_residual = sp.simplify((s * kappa) * (r / s) - kappa * r)
    assert orbit_residual == 0

    r_star = sp.Integer(4)
    witnesses = [sp.simplify(k * r_star) for k in (sp.Integer(1), sp.Rational(1, 4))]
    assert witnesses == [4, 1]
    isometry_equation = sp.simplify((m.T * m)[0, 0])
    assert isometry_equation == kappa**2
    assert sp.solve(sp.Eq(isometry_equation, 1), kappa) == [1]

    exact_objects = [*m, *equivariance_residual, pole_hessian, c0, orbit_residual, *witnesses, isometry_equation]
    assert not any(
        atom.is_Float for obj in exact_objects for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_minimal_cross_carrier_morphism_architecture_gate",
        "representations": {
            "source_line": "L_src=R*u with trivial G action",
            "auxiliary_line": "L_aux=R*e with trivial G action",
            "equivariant_hom_dimension": 1,
        },
        "morphism_family": {
            "definition": "M_kappa(r*u)=kappa*r*e",
            "parameter_space": "R",
            "positive_pole_ray": "kappa>0",
            "unique_from_equivariance": False,
        },
        "cross_parent": {
            "quadratic_block": "phi*(z+a*kappa*r(X))*phi/2",
            "pole_hessian": "z+a*kappa*r_star",
            "c0": "kappa*r_star",
        },
        "normalization_orbit": {
            "action": "u->s*u, r->r/s, kappa->s*kappa",
            "kappa_times_r_invariant": True,
        },
        "positive_witnesses_at_r_star_4": {
            "kappa_1_gives_c0": 4,
            "kappa_1_over_4_gives_c0": 1,
            "same_symmetry_class": True,
        },
        "isometry_selector": {
            "equation": "M_kappa^* M_kappa=I iff kappa^2=1",
            "positive_solution": 1,
            "sufficient_to_fix_normalization": True,
            "derived_from_current_parent": False,
        },
        "verdict": {
            "typed_cross_carrier_architecture_exists": True,
            "normalization_defect_dimension": 1,
            "c0_selected": False,
        },
        "next_gate": "version8_baryon_c0_common_trace_embedding_normalization_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()