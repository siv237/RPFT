#!/usr/bin/env python3
"""Exact full-graph embedding audit for the aligned isotypic parent."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_full_graph_aligned_parent_embedding_gate_results.json"


def bm_action(b: sp.Matrix, m: sp.Matrix) -> sp.Expr:
    gram_b = b * b.T
    gram_m = m * m.T
    alignment = m * b.T
    return sp.expand(
        (sp.trace(gram_b) - 3) ** 2
        + 4 * gram_b.det()
        + sp.trace((gram_m - sp.eye(2)) ** 2)
        + sp.trace(alignment * alignment.T)
    )


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_vectorlike_mass_edge_selector_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_full_graph_aligned_parent_embedding_gate"
    extension = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_minimal_isotypic_channel_extension_gate_results.json").read_text(encoding="utf-8")
    )

    full_new_edges = set(extension["minimal_vectorlike_completion"]["new_strict_edges"])
    selected_sparse_edges = set(extension["minimal_vectorlike_completion"]["selected_new_edges"])
    b_new_edges = {"L_L--Z_R", "Y_L--Z_R"}
    m_new_edges = {"X_L--Z_R", "X_R--Z_L", "Z_L--Z_R", "Z_L--e_R"}
    carrier_covered_edges = b_new_edges | m_new_edges
    omitted_edges = full_new_edges - carrier_covered_edges
    present_but_sparse_unwanted = carrier_covered_edges - selected_sparse_edges

    assert len(full_new_edges) == 9
    assert len(carrier_covered_edges) == 6
    assert omitted_edges == {"Y_R--Z_L", "Z_L--d_R", "Z_L--u_R"}
    assert present_but_sparse_unwanted == {"X_L--Z_R", "X_R--Z_L", "Z_L--e_R"}
    assert len(previous["orbit_and_edge_selector"]["omitted_allowed_complex_edges"]) == 6

    b_variables = sp.symbols("b0:6", real=True)
    m_variables = sp.symbols("m0:6", real=True)
    z_variables = sp.symbols("z0:6", real=True)
    mu_y, mu_u, mu_d = sp.symbols("mu_y mu_u mu_d", positive=True)
    b = sp.Matrix(2, 3, b_variables)
    m = sp.Matrix(2, 3, m_variables)
    z_pairs = ((z_variables[0], z_variables[1]), (z_variables[2], z_variables[3]), (z_variables[4], z_variables[5]))
    masses = (mu_y, mu_u, mu_d)
    stabilizer = sum(mu * (x**2 + y**2) for mu, (x, y) in zip(masses, z_pairs))
    full_action = bm_action(b, m) + stabilizer

    substitutions = {variable: 0 for variable in (*b_variables, *m_variables, *z_variables)}
    substitutions[b_variables[0]] = sp.sqrt(3)
    substitutions[m_variables[1]] = 1
    substitutions[m_variables[5]] = 1
    normalized_substitutions = substitutions | {mu_y: 1, mu_u: 1, mu_d: 1}
    assert sp.simplify(full_action.subs(normalized_substitutions)) == 0

    hessian = sp.simplify(
        sp.hessian(full_action, (*b_variables, *m_variables, *z_variables)).subs(normalized_substitutions)
    )
    eigenvalues = hessian.eigenvals()
    assert hessian.rank() == 14
    assert eigenvalues == {
        sp.Integer(0): 4,
        sp.Integer(2): 6,
        sp.Integer(8): 5,
        sp.Integer(24): 1,
        sp.Integer(26): 2,
    }

    mass_hessian = sp.diag(2 * mu_y, 2 * mu_y, 2 * mu_u, 2 * mu_u, 2 * mu_d, 2 * mu_d)
    assert mass_hessian.det() == 64 * mu_y**2 * mu_u**2 * mu_d**2

    # The three omitted fields have inequivalent endpoint/gauge signatures,
    # so covariance leaves a three-dimensional positive mass cone.
    omitted_type_signatures = {
        "Y_R--Z_L": "weak-doublet channel",
        "Z_L--u_R": "up-type coloured channel",
        "Z_L--d_R": "down-type coloured channel",
    }
    assert len(set(omitted_type_signatures.values())) == 3

    exact_objects = [b, m, full_action, stabilizer, hessian, mass_hessian, mu_y, mu_u, mu_d]
    assert not any(obj.atoms(sp.Float) for obj in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_full_graph_aligned_parent_embedding_gate",
        "carrier_correction": {
            "full_new_strict_edges": sorted(full_new_edges),
            "new_edges_already_in_B": sorted(b_new_edges),
            "new_edges_already_in_M": sorted(m_new_edges),
            "new_edges_covered_by_B_plus_M": len(carrier_covered_edges),
            "present_but_outside_sparse_target": sorted(present_but_sparse_unwanted),
            "truly_omitted_complex_edges": sorted(omitted_edges),
            "truly_omitted_count": len(omitted_edges),
            "predecessor_reported_omitted_count": len(previous["orbit_and_edge_selector"]["omitted_allowed_complex_edges"]),
            "predecessor_flat_mode_count_superseded": True,
            "correct_flat_real_modes_before_stabilization": 2 * len(omitted_edges),
        },
        "conditional_full_graph_parent": {
            "potential": "S_BM + mu_y |z_Y|^2 + mu_u |z_u|^2 + mu_d |z_d|^2",
            "positive_mass_cone_dimension": 3,
            "projective_relative_mass_dimension": 2,
            "overall_mass_scale_free": True,
            "omitted_type_signatures": omitted_type_signatures,
            "zero_vacuum_preserved": True,
            "all_nine_new_edges_in_field_carrier": True,
        },
        "normalized_real_slice_hessian": {
            "variables": 18,
            "rank": hessian.rank(),
            "nullity": 18 - hessian.rank(),
            "eigenvalue_multiplicities": {str(key): value for key, value in sorted(eigenvalues.items(), key=lambda item: item[0])},
            "signature": {"negative": 0, "zero": 4, "positive": 14},
            "extra_mass_block_determinant": "64 mu_y^2 mu_u^2 mu_d^2",
        },
        "ledgers": {
            "carrier_embedding_satisfied": 7,
            "carrier_embedding_tested": 7,
            "coordinate_sparse_selector_satisfied": 0,
            "coordinate_sparse_selector_tested": 3,
            "mass_parent_origin_satisfied": 0,
            "mass_parent_origin_tested": 4,
            "new_parent_inputs": [
                "three positive stabilizing masses",
                "two independent relative mass ratios",
                "one overall mass scale",
                "spectral/superconnection origin of the stabilizer",
            ],
        },
        "verdict": {
            "predecessor_six_omitted_edge_count_exact": False,
            "correct_omitted_edge_count": 3,
            "conditional_full_graph_embedding_exists": True,
            "all_non_orbit_real_flat_modes_lifted_when_masses_positive": True,
            "coordinate_sparse_edge_menu_selected": False,
            "stabilizing_mass_coefficients_derived": False,
            "portal_parent_origin_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()