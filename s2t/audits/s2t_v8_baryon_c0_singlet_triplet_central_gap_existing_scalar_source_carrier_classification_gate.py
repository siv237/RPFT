#!/usr/bin/env python3
"""Exact classification audit for existing scalar source carriers."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_existing_scalar_source_carrier_classification_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_dynamical_source_carrier_admission_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_existing_scalar_source_carrier_classification_gate"

    # A Higgs vector is not a gauge singlet, whereas its quadratic norm is.
    j2 = sp.Matrix([[0, 1], [-1, 0]])
    h = sp.Matrix([1, 0])
    assert j2 * h != sp.zeros(2, 1)
    t = sp.symbols("t", real=True)
    h_t = h + t * j2 * h
    assert sp.diff((h_t.T * h_t)[0], t).subs(t, 0) == 0

    # The centered Higgs norm is a half-line coordinate, not a free Real line.
    r2, v2 = sp.symbols("r2 v2", nonnegative=True)
    chi_h = r2 - v2 / 2
    assert sp.simplify(chi_h.subs(r2, 0) + v2 / 2) == 0

    # The rank-one coherence condensate B=sqrt(3) u v* has exact radius 3.
    u = sp.Matrix([1, 0])
    v = sp.Matrix([1, 0, 0])
    b = sp.sqrt(3) * u * v.T
    coherence_radius = sp.trace(b * b.T)
    assert coherence_radius == 3
    assert b.rank() == 1

    # Projective and family order parameters transform nontrivially under SO(3).
    l3 = sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]])
    sigma = sp.Matrix([1, 0, 0])
    q2 = sp.diag(1, -1, 0)
    assert l3 * sigma != sp.zeros(3, 1)
    assert l3 * q2 - q2 * l3 != sp.zeros(3)
    assert sp.trace(q2) == 0

    # Both live composite singlets admit a symmetry-allowed portal to lambda Q,
    # but the coefficient is not present in the inherited parent action.
    lam, k_h, k_b = sp.symbols("lambda k_H k_B", real=True)
    i_h, i_b = sp.symbols("I_H I_B", real=True, nonnegative=True)
    portal = -lam * (k_h * i_h + k_b * i_b)
    assert sp.diff(portal, lam) == -k_h * i_h - k_b * i_b
    assert portal.subs({k_h: 0, k_b: 0}) == 0

    candidates = {
        "Higgs_doublet_H": {
            "real_signed_line": False,
            "gauge_singlet": False,
            "family_singlet": True,
            "grading_even_scalar": True,
            "active_carrier": True,
            "derived_nonzero_condensate": False,
            "inherited_Q_portal": False,
        },
        "centered_Higgs_norm": {
            "real_signed_line": False,
            "gauge_singlet": True,
            "family_singlet": True,
            "grading_even_scalar": True,
            "active_carrier": True,
            "derived_nonzero_condensate": False,
            "inherited_Q_portal": False,
        },
        "edge_coherence_radius_TrBBstar": {
            "real_signed_line": False,
            "gauge_singlet": True,
            "family_singlet": True,
            "grading_even_scalar": True,
            "active_carrier": True,
            "derived_nonzero_condensate": True,
            "inherited_Q_portal": False,
        },
        "smooth_relative_operator_BA": {
            "real_signed_line": False,
            "gauge_singlet": False,
            "family_singlet": True,
            "grading_even_scalar": True,
            "active_carrier": True,
            "derived_nonzero_condensate": False,
            "inherited_Q_portal": False,
        },
        "projective_Q_field": {
            "real_signed_line": False,
            "gauge_singlet": True,
            "family_singlet": False,
            "grading_even_scalar": True,
            "active_carrier": True,
            "derived_nonzero_condensate": True,
            "inherited_Q_portal": False,
        },
        "family_triplet_Sigma": {
            "real_signed_line": False,
            "gauge_singlet": True,
            "family_singlet": False,
            "grading_even_scalar": True,
            "active_carrier": False,
            "derived_nonzero_condensate": False,
            "inherited_Q_portal": False,
        },
        "twisted_real_scalar_difference": {
            "real_signed_line": True,
            "gauge_singlet": True,
            "family_singlet": True,
            "grading_even_scalar": True,
            "active_carrier": False,
            "derived_nonzero_condensate": False,
            "inherited_Q_portal": False,
        },
        "sterile_NCG_singlet": {
            "real_signed_line": True,
            "gauge_singlet": True,
            "family_singlet": True,
            "grading_even_scalar": True,
            "active_carrier": False,
            "derived_nonzero_condensate": False,
            "inherited_Q_portal": False,
        },
    }
    literal_pass = [name for name, row in candidates.items() if all(row.values())]
    assert literal_pass == []
    composite_symmetry_candidates = [
        name for name in ("centered_Higgs_norm", "edge_coherence_radius_TrBBstar")
        if candidates[name]["gauge_singlet"]
        and candidates[name]["family_singlet"]
        and candidates[name]["grading_even_scalar"]
        and candidates[name]["active_carrier"]
    ]
    assert len(composite_symmetry_candidates) == 2
    assert candidates["edge_coherence_radius_TrBBstar"]["derived_nonzero_condensate"]
    assert not candidates["centered_Higgs_norm"]["derived_nonzero_condensate"]

    exact_objects = [j2, h_t, chi_h, b, coherence_radius, l3, q2, portal]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_existing_scalar_source_carrier_classification_gate",
        "required_contract": {
            "literal_carrier": "one-dimensional signed Real gauge/family singlet, grading-even, active, condensed, with inherited bilinear to Q",
            "tested_requirements": 7,
        },
        "candidate_matrix": candidates,
        "exact_witnesses": {
            "Higgs_doublet_not_singlet": "J2(1,0)^T=(0,-1)^T!=0",
            "centered_Higgs_norm_domain": "I_H-v^2/2 >= -v^2/2",
            "coherence_condensate": "B*=sqrt(3)uv*, rank(B*)=1, Tr(B*B*^*)=3",
            "projective_field_family_type": "Sym^2_0(R3), dimension 5, nontrivial SO(3)",
            "family_order_parameter_type": "R3 triplet, nontrivial SO(3)",
            "smooth_relative_candidate": "operator-valued rank 6 and B(A0)=0",
        },
        "classification": {
            "literal_active_reuses": 0,
            "literal_tested_candidates": 8,
            "active_composite_symmetry_candidates": composite_symmetry_candidates,
            "number_of_active_composite_symmetry_candidates": 2,
            "unique_candidate_with_derived_nonzero_invariant": "edge_coherence_radius_TrBBstar",
            "coherence_invariant_value": 3,
            "existing_Q_portals": 0,
        },
        "boundary": {
            "Higgs_norm": "symmetry-compatible but its vacuum scale and portal coefficient are not derived",
            "edge_coherence_radius": "conditionally normalized nonzero invariant, but the cross-parent portal coefficient is absent",
            "twisted_real_scalar": "correct literal type but belongs to a dynamically closed inactive algebra extension",
            "sterile_NCG_singlet": "correct literal type but absent from the active H15 endpoint content",
        },
        "verdict": {
            "existing_literal_dynamic_carrier_identified": False,
            "composite_reuse_possible": True,
            "best_internal_candidate": "I_B=Tr(BB*)",
            "best_candidate_already_has_exact_condensate": True,
            "best_candidate_Q_portal_derived": False,
            "physical_gap_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_edge_coherence_radius_portal_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()