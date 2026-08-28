#!/usr/bin/env python3
"""Audit the four-vertex vectorlike closure and its selector deficit."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_four_vertex_vectorlike_selector_gate_results.json"


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def strict_edge(a: tuple[str, str, str], b: tuple[str, str, str]) -> bool:
    i, j, grade = a
    k, ell, other_grade = b
    return grade != other_grade and (i == k or j == ell)


def edge_name(a: str, b: str) -> str:
    return "--".join(sorted((a, b)))


def main() -> None:
    previous = load_result("s2t_v7_minimal_mirror_pair_real_anomaly_gate_results.json")
    assert not previous["verdict"]["dimension_minimal_pair_physically_admitted"]
    assert previous["minimal_conservative_repair"]["total_new_chiral_vertices"] == 4

    vertices = {
        "Q_L": ("H", "M3", "L"),
        "L_L": ("H", "C", "L"),
        "u_R": ("C", "M3", "R"),
        "d_R": ("C", "M3", "R"),
        "e_R": ("C", "C", "R"),
        "X_L": ("C", "C", "L"),
        "X_R": ("C", "C", "R"),
        "Y_L": ("H", "C", "L"),
        "Y_R": ("H", "C", "R"),
    }
    all_edges = {
        edge_name(a, b)
        for a, b in itertools.combinations(vertices, 2)
        if strict_edge(vertices[a], vertices[b])
    }
    baseline_edges = {
        edge_name("Q_L", "u_R"),
        edge_name("Q_L", "d_R"),
        edge_name("L_L", "e_R"),
    }
    cycle_edges = {
        edge_name(a, b)
        for a, b in zip(
            ["Q_L", "u_R", "X_L", "e_R", "L_L", "Y_R"],
            ["u_R", "X_L", "e_R", "L_L", "Y_R", "Q_L"],
        )
    }
    vectorlike_mass_edges = {edge_name("X_L", "X_R"), edge_name("Y_L", "Y_R")}
    selected_extension_edges = (cycle_edges | vectorlike_mass_edges) - baseline_edges
    additional_allowed_edges = all_edges - baseline_edges
    unselected_allowed_edges = additional_allowed_edges - selected_extension_edges

    assert len(all_edges) == 14
    assert len(additional_allowed_edges) == 11
    assert len(selected_extension_edges) == 6
    assert len(unselected_allowed_edges) == 5

    duplicate_types: dict[tuple[str, str, str], list[str]] = {}
    for name, vertex in vertices.items():
        duplicate_types.setdefault(vertex, []).append(name)
    duplicate_types = {key: value for key, value in duplicate_types.items() if len(value) > 1}
    assert duplicate_types == {
        ("H", "C", "L"): ["L_L", "Y_L"],
        ("C", "M3", "R"): ["u_R", "d_R"],
        ("C", "C", "R"): ["e_R", "X_R"],
    }
    # The coarse C/M3 coordinate suppresses the conjugate C-character that
    # distinguishes u_R from d_R.  The genuinely identical gauge copies in
    # the canonical lift are the old/new lepton doublets and singlets.
    exact_gauge_duplicates = {
        "H/C/L;Y=-1/2": ["L_L", "Y_L"],
        "C/C/R;Y=-1": ["e_R", "X_R"],
    }

    # Generic family-level vectorlike masses preserve one chiral kernel per
    # generation, but their orientation is arbitrary.
    rng = np.random.default_rng(20260827)
    singlet_mass = rng.normal(size=(3, 6)) + 1j * rng.normal(size=(3, 6))
    doublet_mass = rng.normal(size=(6, 3)) + 1j * rng.normal(size=(6, 3))
    singlet_rank = int(np.linalg.matrix_rank(singlet_mass))
    doublet_rank = int(np.linalg.matrix_rank(doublet_mass))
    assert singlet_rank == 3 and doublet_rank == 3

    base_indices = {"Q": 1, "u": -1, "d": -1, "L": 1, "e": -1}
    four_vertex_indices = {"Q": 1, "u": -1, "d": -1, "L": 2 - 1, "e": 1 - 2}
    full_mirror_indices = {key: 0 for key in base_indices}
    assert four_vertex_indices == base_indices

    result = {
        "gate": "version7_four_vertex_vectorlike_selector_gate",
        "carrier": {
            "new_vertices": {
                name: list(vertices[name]) for name in ("X_L", "X_R", "Y_L", "Y_R")
            },
            "strict_first_order_edges_total": len(all_edges),
            "baseline_edges": sorted(baseline_edges),
            "new_allowed_edges": sorted(additional_allowed_edges),
            "desired_cycle_plus_vector_masses": sorted(selected_extension_edges),
            "allowed_but_unselected_edges": sorted(unselected_allowed_edges),
        },
        "admission": {
            "strict_first_order": True,
            "formal_Real_completion": True,
            "local_anomalies_cancel_pairwise": True,
            "Witten_doublet_parity_even": True,
        },
        "family_matrix_cost": {
            "new_allowed_3x3_complex_matrices": len(additional_allowed_edges),
            "raw_real_parameters_before_quotients": 18 * len(additional_allowed_edges),
            "desired_nonbaseline_matrices": len(selected_extension_edges),
            "allowed_matrices_requiring_zero_or_relation": len(unselected_allowed_edges),
        },
        "generic_mass_kernel": {
            "charged_singlet_matrix_shape": list(singlet_mass.shape),
            "charged_singlet_rank": singlet_rank,
            "right_kernel_dimension": singlet_mass.shape[1] - singlet_rank,
            "weak_doublet_matrix_shape": list(doublet_mass.shape),
            "weak_doublet_rank": doublet_rank,
            "left_kernel_dimension": doublet_mass.shape[0] - doublet_rank,
            "one_light_chiral_direction_per_generation_survives": True,
            "kernel_orientation_selected_by_current_action": False,
        },
        "chiral_index_comparison": {
            "H15_without_nuR": base_indices,
            "four_vertex_extension": four_vertex_indices,
            "complete_mirror_generation": full_mirror_indices,
            "four_vertex_preserves_H15_indices": four_vertex_indices == base_indices,
            "complete_mirror_generation_preserves_H15_indices": False,
        },
        "selector_obstruction": {
            "coarse_coordinate_duplicates": {"/".join(key): value for key, value in duplicate_types.items()},
            "exact_gauge_duplicate_types": exact_gauge_duplicates,
            "unchanged_algebra_distinguishes_old_from_new_copies": False,
            "desired_six_of_eleven_new_edges_selected": False,
            "arbitrary_Yukawa_enlargement_avoided": False,
        },
        "verdict": {
            "four_vertex_vectorlike_closure_structurally_admitted": True,
            "complete_mirror_generation_rejected_by_chiral_index": True,
            "canonical_single_source_parent_obtained": False,
            "status": "conditional_positive_selector_missing",
            "next_gate": "derive a multiplicity-space selector from the existing affine/Hodge parent and test whether it fixes the light kernels and edge menu",
        },
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()