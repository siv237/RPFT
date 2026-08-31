#!/usr/bin/env python3
"""Exact parent-origin audit for the three extra-edge mass coefficients."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_parent_origin_gate_results.json"


def edge_block(dimension: int, x: sp.Symbol, y: sp.Symbol) -> sp.Matrix:
    identity = sp.eye(dimension)
    zero = sp.zeros(dimension)
    z = x + sp.I * y
    return zero.row_join(z * identity).col_join(sp.conjugate(z) * identity.row_join(zero))


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_full_graph_aligned_parent_embedding_gate_results.json").read_text(encoding="utf-8")
    )
    gate = "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_parent_origin_gate"
    assert predecessor["next_gate"] == gate

    # Order: weak Y edge, up-colour edge, down-colour edge.
    names = ("Z_L--Y_R", "Z_L--u_R", "Z_L--d_R")
    dimensions = sp.Matrix([2, 3, 3])
    hypercharges = (sp.Rational(1, 2), sp.Rational(5, 3), sp.Rational(2, 3))
    su2_indices = (sp.Rational(1, 2), 0, 0)
    su3_indices = (0, sp.Rational(1, 2), sp.Rational(1, 2))
    u1_indices = tuple(d * y**2 for d, y in zip(dimensions, hypercharges))
    gauge_index_matrix = sp.Matrix([u1_indices, su2_indices, su3_indices])
    assert gauge_index_matrix == sp.Matrix([
        [sp.Rational(1, 2), sp.Rational(25, 3), sp.Rational(4, 3)],
        [sp.Rational(1, 2), 0, 0],
        [0, sp.Rational(1, 2), sp.Rational(1, 2)],
    ])
    assert gauge_index_matrix.det() == -sp.Rational(7, 4)
    assert gauge_index_matrix.rank() == 3

    variables = sp.symbols("xY yY xu yu xd yd", real=True)
    blocks = [edge_block(d, *variables[2 * i: 2 * i + 2]) for i, d in enumerate(dimensions)]
    physical_half_trace_terms = [sp.expand(sp.trace(block**2) / 2) for block in blocks]
    expected_terms = [
        dimensions[i] * (variables[2 * i] ** 2 + variables[2 * i + 1] ** 2)
        for i in range(3)
    ]
    assert all(sp.simplify(left - right) == 0 for left, right in zip(physical_half_trace_terms, expected_terms))

    p_y, p_u, p_d = sp.symbols("p_Y p_u p_d", positive=True)
    central_weights = sp.Matrix([p_y, p_u, p_d])
    mass_vector = sp.diag(*dimensions) * central_weights
    assert mass_vector == sp.Matrix([2 * p_y, 3 * p_u, 3 * p_d])
    unweighted_mass_vector = mass_vector.subs({p_y: 1, p_u: 1, p_d: 1})
    alternative_mass_vector = mass_vector.subs({p_y: 1, p_u: 2, p_d: 1})
    assert unweighted_mass_vector == sp.Matrix([2, 3, 3])
    assert alternative_mass_vector == sp.Matrix([2, 6, 3])
    assert unweighted_mass_vector.cross(alternative_mass_vector) != sp.zeros(3, 1)

    # Gauge indices span all three edge coefficients, hence impose no relation.
    sector_coefficients_for_unweighted_ratio = gauge_index_matrix.T.LUsolve(unweighted_mass_vector)
    assert sector_coefficients_for_unweighted_ratio == sp.Matrix([0, 4, 6])

    representation_signatures = {
        names[0]: "(1,2)_{1/2}",
        names[1]: "(3,1)_{5/3}",
        names[2]: "(3,1)_{2/3}",
    }
    assert len(set(representation_signatures.values())) == 3

    exact_objects = [
        dimensions,
        gauge_index_matrix,
        *blocks,
        *physical_half_trace_terms,
        mass_vector,
        unweighted_mass_vector,
        alternative_mass_vector,
        sector_coefficients_for_unweighted_ratio,
    ]
    assert not any(obj.atoms(sp.Float) for obj in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "extra_edge_representations": {
            "ordered_edges": names,
            "signatures": representation_signatures,
            "complex_dimensions": [int(value) for value in dimensions],
            "pairwise_equivariant_intertwiners": 0,
        },
        "common_trace_candidate": {
            "block_operator": "F_e=[[0,z_e I_d],[conj(z_e) I_d,0]]",
            "physical_half_trace": "(1/2) Tr(F_e^2)=d_e |z_e|^2",
            "unweighted_mass_coefficients": [int(value) for value in unweighted_mass_vector],
            "unweighted_ratio": "2:3:3",
            "positive_shape_generated": True,
            "real_half_trace_changes_ratio": False,
        },
        "central_trace_family": {
            "center_dimension": 3,
            "positive_weights": [str(value) for value in central_weights],
            "mass_vector": [str(value) for value in mass_vector],
            "projective_relative_dimension": 2,
            "equal_weight_witness": [int(value) for value in unweighted_mass_vector],
            "unequal_weight_witness": [int(value) for value in alternative_mass_vector],
            "ratio_unique": False,
            "canonical_simple_factor_connector_present": False,
        },
        "gauge_index_test": {
            "rows": ["U(1)", "SU(2)", "SU(3)"],
            "matrix": [[str(value) for value in gauge_index_matrix.row(i)] for i in range(3)],
            "determinant": str(gauge_index_matrix.det()),
            "rank": gauge_index_matrix.rank(),
            "sector_coefficients_for_unweighted_ratio": [str(value) for value in sector_coefficients_for_unweighted_ratio],
            "mass_relation_selected": False,
        },
        "ledgers": {
            "quadratic_trace_shape_satisfied": 5,
            "quadratic_trace_shape_tested": 5,
            "relative_mass_parent_origin_satisfied": 0,
            "relative_mass_parent_origin_tested": 5,
            "absolute_mass_scale_origin_satisfied": 0,
            "absolute_mass_scale_origin_tested": 2,
        },
        "verdict": {
            "one_superconnection_can_generate_all_three_positive_norms": True,
            "unweighted_trace_produces_dimension_ratio": True,
            "unweighted_trace_is_internally_selected": False,
            "central_trace_simplex_survives": True,
            "gauge_indices_remove_central_freedom": False,
            "relative_masses_derived": False,
            "absolute_mass_scale_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_trace_simplex_selector_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()