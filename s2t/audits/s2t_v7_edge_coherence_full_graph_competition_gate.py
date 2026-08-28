#!/usr/bin/env python3
"""Audit the coherence vacuum against the full eleven-edge extension."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v7_edge_coherence_full_graph_competition_gate_results.json"
)


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def edge_name(first: str, second: str) -> str:
    return "--".join(sorted((first, second)))


def field_from_real(vector: np.ndarray) -> np.ndarray:
    complex_entries = vector[:6] + 1j * vector[6:12]
    return complex_entries.reshape(2, 3)


def coherence_action(field: np.ndarray) -> float:
    gram = field @ field.conj().T
    total = float(np.trace(gram).real)
    determinant = float(np.linalg.det(gram).real)
    return (total - 3.0) ** 2 + (5.0 / 3.0) * determinant


def extended_action(vector: np.ndarray) -> float:
    # The final twelve real coordinates are the six complex new edges outside
    # the coherence biclique.  The admitted D_B action contains none of them.
    return coherence_action(field_from_real(vector[:12]))


def numerical_hessian(function, point: np.ndarray, step: float = 2.0e-4) -> np.ndarray:
    size = point.size
    result = np.zeros((size, size))
    origin = function(point)
    for i in range(size):
        ei = np.zeros(size)
        ei[i] = step
        result[i, i] = (function(point + ei) - 2.0 * origin + function(point - ei)) / step**2
        for j in range(i + 1, size):
            ej = np.zeros(size)
            ej[j] = step
            value = (
                function(point + ei + ej)
                - function(point + ei - ej)
                - function(point - ei + ej)
                + function(point - ei - ej)
            ) / (4.0 * step**2)
            result[i, j] = value
            result[j, i] = value
    return result


def support_mask(rows: tuple[int, ...], columns: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        int(row in rows and column in columns)
        for row in range(2)
        for column in range(3)
    )


def main() -> None:
    previous = load_result(
        "s2t_v7_edge_coherence_field_space_superconnection_gate_results.json"
    )
    graph = load_result("s2t_v7_four_vertex_vectorlike_selector_gate_results.json")
    assert previous["verdict"]["status"] == (
        "positive_auxiliary_field_space_superconnection_carrier"
    )

    baseline = set(graph["carrier"]["baseline_edges"])
    new_allowed = set(graph["carrier"]["new_allowed_edges"])
    selected_new = set(graph["carrier"]["desired_cycle_plus_vector_masses"])
    unwanted_new = set(graph["carrier"]["allowed_but_unselected_edges"])

    coherence_edges = {
        edge_name(left, right)
        for left in ("L_L", "Y_L")
        for right in ("e_R", "X_R", "Y_R")
    }
    baseline_inside = coherence_edges & baseline
    new_inside = coherence_edges & new_allowed
    selected_inside = coherence_edges & selected_new
    unwanted_inside = coherence_edges & unwanted_new
    new_outside = new_allowed - coherence_edges
    selected_outside = selected_new - coherence_edges
    unwanted_outside = unwanted_new - coherence_edges

    assert len(coherence_edges) == 6
    assert baseline_inside == {edge_name("L_L", "e_R")}
    assert selected_inside == {
        edge_name("L_L", "Y_R"),
        edge_name("Y_L", "Y_R"),
    }
    assert unwanted_inside == {
        edge_name("L_L", "X_R"),
        edge_name("Y_L", "e_R"),
        edge_name("Y_L", "X_R"),
    }
    assert len(new_inside) == 5
    assert len(new_outside) == 6
    assert len(selected_outside) == 4
    assert len(unwanted_outside) == 2

    # Row order L_L,Y_L; column order e_R,X_R,Y_R.  The desired restriction
    # keeps the old L-e edge and the selected L-Y and Y-Y edges.
    target_mask = (1, 0, 1, 0, 0, 1)
    rank_one_supports = {
        support_mask(rows, columns)
        for row_count in (1, 2)
        for rows in itertools.combinations(range(2), row_count)
        for column_count in (1, 2, 3)
        for columns in itertools.combinations(range(3), column_count)
    }
    assert len(rank_one_supports) == 21
    assert target_mask not in rank_one_supports

    desired_positions = {0, 2, 5}
    unwanted_positions = {1, 3, 4}
    supports_containing_all_desired = [
        mask
        for mask in rank_one_supports
        if all(mask[index] for index in desired_positions)
    ]
    assert supports_containing_all_desired
    minimum_unwanted = min(
        sum(mask[index] for index in unwanted_positions)
        for mask in supports_containing_all_desired
    )
    assert minimum_unwanted == 1
    forced_unwanted_positions = {
        index
        for index in unwanted_positions
        if all(mask[index] for mask in supports_containing_all_desired)
    }
    assert forced_unwanted_positions == {3}  # Y_L--e_R

    target_representative = np.array(
        [[1.0, 0.0, 1.0], [0.0, 0.0, 1.0]], dtype=complex
    )
    target_rank = int(np.linalg.matrix_rank(target_representative))
    target_minor_e_y = float(
        np.linalg.det(target_representative[:, [0, 2]]).real
    )
    target_energy = coherence_action(target_representative)
    assert target_rank == 2
    assert target_minor_e_y == 1.0
    assert abs(target_energy - 5.0 / 3.0) < 1.0e-12

    # On the target-support stratum B=[[a,0,b],[0,0,c]], put
    # x=|a|^2, y=|b|^2, z=|c|^2.  S=(x+y+z-3)^2+(5/3)xz.
    # The y equation gives r=x+y+z-3=0; the x equation then forces z=0.
    # Thus there is no stationary point with all three required amplitudes
    # nonzero.
    stationary_in_open_target_stratum = False

    point = np.zeros(24)
    point[0] = np.sqrt(3.0)
    hessian = numerical_hessian(extended_action, point)
    eigenvalues = np.linalg.eigvalsh(hessian)
    zero_count = int(np.sum(np.abs(eigenvalues) < 2.0e-5))
    positive_count = int(np.sum(eigenvalues > 2.0e-5))
    negative_count = int(np.sum(eigenvalues < -2.0e-5))
    assert (negative_count, zero_count, positive_count) == (0, 19, 5)
    outside_block = hessian[12:, 12:]
    outside_coupling = hessian[:12, 12:]
    assert np.max(np.abs(outside_block)) < 1.0e-10
    assert np.max(np.abs(outside_coupling)) < 1.0e-10

    result = {
        "gate": "version7_edge_coherence_full_graph_competition_gate",
        "full_graph": {
            "baseline_edges": sorted(baseline),
            "new_allowed_edges": sorted(new_allowed),
            "selected_new_edges": sorted(selected_new),
            "unwanted_new_edges": sorted(unwanted_new),
        },
        "coherence_biclique_placement": {
            "vertices": {
                "rows": ["L_L", "Y_L"],
                "columns": ["e_R", "X_R", "Y_R"],
            },
            "all_edges": sorted(coherence_edges),
            "baseline_inside": sorted(baseline_inside),
            "selected_new_inside": sorted(selected_inside),
            "unwanted_new_inside": sorted(unwanted_inside),
            "new_outside": sorted(new_outside),
            "selected_new_outside": sorted(selected_outside),
            "unwanted_new_outside": sorted(unwanted_outside),
        },
        "support_obstruction": {
            "row_order": ["L_L", "Y_L"],
            "column_order": ["e_R", "X_R", "Y_R"],
            "target_mask": list(target_mask),
            "rank_one_rectangular_support_count": len(rank_one_supports),
            "target_is_rank_one_support": False,
            "target_representative_rank": target_rank,
            "target_eY_minor": target_minor_e_y,
            "target_representative_energy_at_unit_amplitudes": target_energy,
            "minimum_unwanted_edges_if_all_three_desired_inside_edges_survive": minimum_unwanted,
            "forced_unwanted_edge": edge_name("Y_L", "e_R"),
            "stationary_point_with_all_target_inside_amplitudes_nonzero": stationary_in_open_target_stratum,
        },
        "spectator_test": {
            "new_complex_edges_outside_coherence_block": len(new_outside),
            "one_generation_real_flat_directions": 2 * len(new_outside),
            "three_generation_real_flat_directions": 18 * len(new_outside),
            "selected_new_complex_edges_left_flat": len(selected_outside),
            "unwanted_new_complex_edges_left_flat": len(unwanted_outside),
            "extended_hessian_signature": {
                "negative": negative_count,
                "zero": zero_count,
                "positive": positive_count,
            },
            "maximum_outside_hessian_entry": float(np.max(np.abs(outside_block))),
            "maximum_mixed_hessian_entry": float(np.max(np.abs(outside_coupling))),
        },
        "verdict": {
            "status": "closed_as_selector_of_target_six_edge_extension",
            "auxiliary_superconnection_carrier_preserved": True,
            "rank_one_coherence_mechanism_preserved": True,
            "target_edge_menu_selected": False,
            "reason": "the target support inside the coherence biclique has rank two, while the potential selects rank one; six new outside edges are spectators",
            "next_gate": "construct and preregister a full-quiver cycle-curvature parent whose variables include all eleven new edges and whose vacuum support is the selected six-edge cycle rather than a rank-one biclique",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()