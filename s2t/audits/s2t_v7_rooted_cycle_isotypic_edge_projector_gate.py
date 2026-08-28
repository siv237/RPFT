#!/usr/bin/env python3
"""Audit the union of rooted-cycle and isotypic projectors on new edges."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v7_rooted_cycle_isotypic_edge_projector_gate_results.json"
)


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def edge(first: str, second: str) -> str:
    return "--".join(sorted((first, second)))


def diagonal_projector(edge_order: list[str], support: set[str]) -> np.ndarray:
    return np.diag([float(item in support) for item in edge_order])


def signature(matrix: np.ndarray, tolerance: float = 1.0e-12) -> dict[str, int]:
    eigenvalues = np.linalg.eigvalsh(matrix)
    return {
        "negative": int(np.sum(eigenvalues < -tolerance)),
        "zero": int(np.sum(np.abs(eigenvalues) <= tolerance)),
        "positive": int(np.sum(eigenvalues > tolerance)),
    }


def main() -> None:
    graph = load_result("s2t_v7_four_vertex_vectorlike_selector_gate_results.json")
    rooted = load_result(
        "s2t_v7_baseline_rooted_primitive_cycle_admission_gate_results.json"
    )
    assert rooted["verdict"]["status"] == (
        "positive_relative_cycle_observable_not_full_parent"
    )

    carrier = graph["carrier"]
    edge_order = sorted(carrier["new_allowed_edges"])
    selected = set(carrier["desired_cycle_plus_vector_masses"])
    unwanted = set(carrier["allowed_but_unselected_edges"])
    assert len(edge_order) == 11 and len(selected) == 6 and len(unwanted) == 5

    rooted_cycle_edges = set(rooted["baseline_rooted_selector"]["new_cycle_edges"])
    assert len(rooted_cycle_edges) == 4

    # Gauge representation, without chirality.  Equality means that an edge
    # is an isotypic left-right mass block; no old/new label is used.
    gauge_types = {
        "Q_L": ("3", "2", "1/6"),
        "L_L": ("1", "2", "-1/2"),
        "u_R": ("3", "1", "2/3"),
        "d_R": ("3", "1", "-1/3"),
        "e_R": ("1", "1", "-1"),
        "X_L": ("1", "1", "-1"),
        "X_R": ("1", "1", "-1"),
        "Y_L": ("1", "2", "-1/2"),
        "Y_R": ("1", "2", "-1/2"),
    }
    isotypic_edges = set()
    for item in edge_order:
        first, second = item.split("--")
        if gauge_types[first] == gauge_types[second]:
            isotypic_edges.add(item)

    expected_isotypic = {
        edge("L_L", "Y_R"),
        edge("Y_L", "Y_R"),
        edge("X_L", "e_R"),
        edge("X_L", "X_R"),
    }
    assert isotypic_edges == expected_isotypic

    p_cycle = diagonal_projector(edge_order, rooted_cycle_edges)
    p_iso = diagonal_projector(edge_order, isotypic_edges)
    p_intersection = p_cycle @ p_iso
    p_selected = p_cycle + p_iso - p_intersection
    identity = np.eye(len(edge_order))
    p_unwanted = identity - p_selected
    grading = identity - 2.0 * p_selected

    selected_by_union = {
        item for index, item in enumerate(edge_order) if p_selected[index, index] > 0.5
    }
    unwanted_by_complement = set(edge_order) - selected_by_union
    assert selected_by_union == selected
    assert unwanted_by_complement == unwanted

    for projector in (p_cycle, p_iso, p_intersection, p_selected, p_unwanted):
        assert np.max(np.abs(projector @ projector - projector)) < 1.0e-12
        assert np.max(np.abs(projector.conj().T - projector)) < 1.0e-12
    assert np.max(np.abs(p_cycle @ p_iso - p_iso @ p_cycle)) < 1.0e-12
    assert np.max(np.abs(grading @ grading - identity)) < 1.0e-12

    complex_signature = signature(grading)
    real_hessian = 2.0 * np.kron(grading, np.eye(2))
    real_signature = signature(real_hessian)
    family_real_hessian = np.kron(real_hessian, np.eye(9))
    family_signature = signature(family_real_hessian)
    assert complex_signature == {"negative": 6, "zero": 0, "positive": 5}
    assert real_signature == {"negative": 12, "zero": 0, "positive": 10}
    assert family_signature == {"negative": 108, "zero": 0, "positive": 90}

    cycle_only_false_negatives = selected - rooted_cycle_edges
    iso_only_false_negatives = selected - isotypic_edges
    assert cycle_only_false_negatives == {
        edge("X_L", "X_R"),
        edge("Y_L", "Y_R"),
    }
    assert iso_only_false_negatives == {
        edge("Q_L", "Y_R"),
        edge("X_L", "u_R"),
    }
    assert not (rooted_cycle_edges - selected)
    assert not (isotypic_edges - selected)

    result = {
        "gate": "version7_rooted_cycle_isotypic_edge_projector_gate",
        "edge_space": {
            "ordered_new_edges": edge_order,
            "complex_dimension": len(edge_order),
            "real_dimension_per_generation": 2 * len(edge_order),
            "real_dimension_for_3x3_family_blocks": 18 * len(edge_order),
        },
        "rooted_cycle_projector": {
            "support": sorted(rooted_cycle_edges),
            "rank": int(np.trace(p_cycle)),
            "false_positive_edges": sorted(rooted_cycle_edges - selected),
            "missed_selected_edges": sorted(cycle_only_false_negatives),
        },
        "isotypic_projector": {
            "definition": "opposite-chirality edge endpoints carry the same (SU3,SU2,Y) gauge representation",
            "support": sorted(isotypic_edges),
            "rank": int(np.trace(p_iso)),
            "false_positive_edges": sorted(isotypic_edges - selected),
            "missed_selected_edges": sorted(iso_only_false_negatives),
            "uses_old_new_copy_labels": False,
        },
        "projector_union": {
            "formula": "P_sel=P_cycle+P_iso-P_cycle*P_iso",
            "intersection_rank": int(np.trace(p_intersection)),
            "selected_rank": int(np.trace(p_selected)),
            "complement_rank": int(np.trace(p_unwanted)),
            "selected_support": sorted(selected_by_union),
            "complement_support": sorted(unwanted_by_complement),
            "equals_desired_six_edge_menu": selected_by_union == selected,
            "commuting_orthogonal_projectors": True,
            "free_relative_weight": False,
        },
        "edge_grading": {
            "formula": "Gamma_E=I-2*P_sel",
            "involution_residual": float(np.max(np.abs(grading @ grading - identity))),
            "complex_signature": complex_signature,
            "one_generation_real_hessian_signature": real_signature,
            "three_generation_family_hessian_signature": family_signature,
            "negative_edges": sorted(selected_by_union),
            "positive_edges": sorted(unwanted_by_complement),
        },
        "covariance": {
            "acts_by_complete_gauge_covariant_edge_blocks": True,
            "orientation_reversal_assigns_same_sign_to_Real_pair": True,
            "depends_on_pre_extension_H15_support": True,
            "depends_on_observed_old_new_basis": False,
        },
        "remaining_parent_gap": {
            "quadratic_relative_signs_fixed": True,
            "overall_mass_scale_fixed": False,
            "quartic_stabilization_fixed": False,
            "nonzero_vacuum_with_all_six_selected_edges_proved": False,
            "real_superconnection_or_spectral_trace_origin_proved": False,
        },
        "verdict": {
            "status": "positive_canonical_edge_grading_parent_origin_open",
            "exact_six_of_eleven_selector_obtained": True,
            "unwanted_edges_have_positive_quadratic_sign": True,
            "selected_edges_have_negative_quadratic_sign": True,
            "complete_dynamical_parent_obtained": False,
            "next_gate": "derive Gamma_E as the degree-zero part of one Real field-space superconnection and test the quartic vacuum and full Hessian without an independent stabilization weight",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()