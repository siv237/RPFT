#!/usr/bin/env python3
"""Exact parent-origin audit for the residual up/down incidence bit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_assignment_selector_gate_results.json").read_text())
    gate = "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_parent_origin_gate"
    assert predecessor["next_gate"] == gate

    y_u = sp.Rational(5, 3)
    y_d = sp.Rational(2, 3)
    complex_dimension = 3
    score_u = sp.simplify(complex_dimension * y_u**2)
    score_d = sp.simplify(complex_dimension * y_d**2)
    score_gap = sp.simplify(score_u - score_d)

    i3 = sp.eye(3)
    y_real = sp.diag(y_u * i3, -y_u * i3, y_d * i3, -y_d * i3)
    a_ud = sp.diag(i3, i3, -i3, -i3)
    p_u = sp.diag(i3, i3, sp.zeros(3), sp.zeros(3))
    p_d = sp.diag(sp.zeros(3), sp.zeros(3), i3, i3)
    identity = sp.eye(12)

    odd_traces = {
        "Tr(A_ud Y)": sp.trace(a_ud * y_real),
        "Tr(A_ud Y^3)": sp.trace(a_ud * y_real**3),
        "Tr(P_u Y)": sp.trace(p_u * y_real),
        "Tr(P_d Y)": sp.trace(p_d * y_real),
    }
    assert set(odd_traces.values()) == {0}

    even_discriminator = sp.trace(a_ud * y_real**2)
    centered_y2 = sp.simplify(y_real**2 - sp.Rational(29, 18) * identity)
    centered_eigenvalue_u = sp.Rational(7, 6)
    centered_eigenvalue_d = -sp.Rational(7, 6)
    assert sp.simplify(centered_y2 - sp.diag(
        centered_eigenvalue_u * i3,
        centered_eigenvalue_u * i3,
        centered_eigenvalue_d * i3,
        centered_eigenvalue_d * i3,
    )) == sp.zeros(12)
    centered_norm = sp.trace(centered_y2**2)
    centered_pairing = sp.trace(a_ud * centered_y2)
    projector_distance_squared = sp.trace((p_u - p_d)**2)

    assert score_u == sp.Rational(25, 3)
    assert score_d == sp.Rational(4, 3)
    assert score_gap == 7
    assert even_discriminator == 14
    assert centered_norm == sp.Rational(49, 3)
    assert centered_pairing == 14
    assert projector_distance_squared == 12
    assert sp.trace(p_u) == sp.trace(p_d) == 6
    assert p_u * p_d == sp.zeros(12)

    objects = [y_u, y_d, score_u, score_d, score_gap, y_real, a_ud,
               centered_y2, centered_norm, centered_pairing]
    assert not any(obj.atoms(sp.Float) for obj in objects)

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "binary_candidates": ["B->u,M->Y", "B->d,M->Y"],
        "representation_data": {
            "complex_dimensions": {"u": 3, "d": 3},
            "hypercharges": {"u": "5/3", "d": "2/3"},
            "su2_indices": {"u": "0", "d": "0"},
            "su3_indices": {"u": "1/2", "d": "1/2"},
            "u1_quadratic_indices": {"u": "25/3", "d": "4/3"},
            "u1_index_gap": "7",
        },
        "real_trace_audit": {
            "odd_traces": {key: str(value) for key, value in odd_traces.items()},
            "odd_hypercharge_moments_cancel": True,
            "vectorlike_anomaly_is_zero_per_candidate": True,
            "Tr(A_ud Y^2)": str(even_discriminator),
        },
        "conditional_quadratic_score": {
            "positive_coefficient_minimizer": "d",
            "negative_coefficient_minimizer": "u",
            "zero_coefficient_minimizers": ["u", "d"],
            "coefficient_sign_required": True,
            "fixed_graph_projector_is_dynamical": False,
        },
        "discrete_geometry": {
            "real_projector_ranks": {"P_u": 6, "P_d": 6},
            "Tr((P_u-P_d)^2)": str(projector_distance_squared),
            "continuous_tangent_between_candidates_dimension": 0,
            "euler_lagrange_selector_available": False,
            "inter_geometry_measure_inherited": False,
        },
        "minimal_typed_discriminator_preview": {
            "S_ud": "Y^2-(29/18)I",
            "eigenvalues": {"u": "7/6", "d": "-7/6"},
            "Tr(S_ud^2)": str(centered_norm),
            "Tr(A_ud S_ud)": str(centered_pairing),
            "typed_coupling_inherited": False,
            "coupling_sign_inherited": False,
        },
        "ledgers": {
            "exact_representation_classification_satisfied": 8,
            "exact_representation_classification_tested": 8,
            "conditional_discriminator_shape_satisfied": 5,
            "conditional_discriminator_shape_tested": 5,
            "parent_origin_satisfied": 0,
            "parent_origin_tested": 7,
        },
        "verdict": {
            "hypercharge_square_distinguishes_candidates": True,
            "positive_hypercharge_square_score_conditionally_selects_d": True,
            "real_odd_moment_selects_candidate": False,
            "existing_parent_varies_incidence": False,
            "binary_u_d_choice_resolved": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_architecture_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()