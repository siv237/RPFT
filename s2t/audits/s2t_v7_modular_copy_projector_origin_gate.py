#!/usr/bin/env python3
"""Audit the graph-derived modular parity selector for duplicate copies."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_modular_copy_projector_origin_gate_results.json"


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def canonical_edge(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def main() -> None:
    previous = load_result("s2t_v7_affine_hodge_copy_selector_no_go_gate_results.json")
    assert previous["verdict"]["status"] == "closed_as_copy_selector"

    vertices = ["Q_L", "L_L", "u_R", "d_R", "e_R", "X_L", "X_R", "Y_L", "Y_R"]
    baseline_edges = [("L_L", "e_R"), ("Q_L", "d_R"), ("Q_L", "u_R")]
    new_edges = [
        ("L_L", "X_R"),
        ("L_L", "Y_R"),
        ("Q_L", "Y_R"),
        ("X_L", "X_R"),
        ("X_L", "Y_R"),
        ("X_L", "d_R"),
        ("X_L", "e_R"),
        ("X_L", "u_R"),
        ("X_R", "Y_L"),
        ("Y_L", "Y_R"),
        ("Y_L", "e_R"),
    ]
    edges = {canonical_edge(*edge) for edge in baseline_edges + new_edges}
    index = {vertex: position for position, vertex in enumerate(vertices)}
    adjacency = np.zeros((len(vertices), len(vertices)), dtype=float)
    for left, right in edges:
        i, j = index[left], index[right]
        adjacency[i, j] = adjacency[j, i] = 1.0

    neighbours = {
        vertex: sorted(
            other for other in vertices if canonical_edge(vertex, other) in edges
        )
        for vertex in vertices
    }
    twin_pairs = [("L_L", "Y_L"), ("e_R", "X_R")]
    assert all(neighbours[left] == neighbours[right] for left, right in twin_pairs)

    swaps = []
    compressed_data = {}
    adjacency_squared = adjacency @ adjacency
    for left, right in twin_pairs:
        permutation = np.eye(len(vertices), dtype=float)
        i, j = index[left], index[right]
        permutation[i, i] = permutation[j, j] = 0.0
        permutation[i, j] = permutation[j, i] = 1.0
        assert np.linalg.norm(adjacency @ permutation - permutation @ adjacency) < 1e-12
        swaps.append(permutation)

        compressed = adjacency_squared[np.ix_([i, j], [i, j])]
        exchange = compressed / 3.0 - np.eye(2)
        plus = (np.eye(2) + exchange) / 2.0
        minus = (np.eye(2) - exchange) / 2.0
        assert np.linalg.norm(compressed - 3.0 * np.ones((2, 2))) < 1e-12
        assert np.linalg.norm(exchange @ exchange - np.eye(2)) < 1e-12
        assert np.linalg.norm(plus @ plus - plus) < 1e-12
        assert np.linalg.norm(minus @ minus - minus) < 1e-12
        compressed_data[f"{left}/{right}"] = {
            "compressed_A2": compressed.tolist(),
            "derived_exchange": exchange.tolist(),
            "plus_projector": plus.tolist(),
            "minus_projector": minus.tolist(),
            "exchange_square_residual": float(np.linalg.norm(exchange @ exchange - np.eye(2))),
        }

    # Determine the edge orbits under the two independent twin swaps.
    generators = [
        {"L_L": "Y_L", "Y_L": "L_L"},
        {"e_R": "X_R", "X_R": "e_R"},
    ]

    def act(edge: tuple[str, str], generator: dict[str, str]) -> tuple[str, str]:
        left, right = edge
        return canonical_edge(generator.get(left, left), generator.get(right, right))

    unseen = set(edges)
    edge_orbits: list[list[tuple[str, str]]] = []
    while unseen:
        orbit = {next(iter(unseen))}
        changed = True
        while changed:
            changed = False
            for edge in tuple(orbit):
                for generator in generators:
                    image = act(edge, generator)
                    if image not in orbit:
                        orbit.add(image)
                        changed = True
        assert orbit <= edges
        edge_orbits.append(sorted(orbit))
        unseen -= orbit
    edge_orbits.sort(key=lambda orbit: (-len(orbit), orbit))
    assert len(edge_orbits) == 9

    selected_edges = {
        canonical_edge(*edge)
        for edge in baseline_edges
        + [
            ("L_L", "Y_R"),
            ("Q_L", "Y_R"),
            ("X_L", "X_R"),
            ("X_L", "e_R"),
            ("X_L", "u_R"),
            ("Y_L", "Y_R"),
        ]
    }
    selected_invariant = True
    selected_symmetric_differences = {}
    for generator in generators:
        image = {act(edge, generator) for edge in selected_edges}
        difference = sorted(selected_edges.symmetric_difference(image))
        selected_symmetric_differences[str(generator)] = [list(edge) for edge in difference]
        selected_invariant = selected_invariant and not difference
    assert not selected_invariant

    # Modular lifting of the formerly flat Hodge orbit.
    identity3 = np.eye(3, dtype=float)
    exchange = np.array([[0.0, 1.0], [1.0, 0.0]])
    beta = 1.0
    height = np.kron(exchange, identity3)
    eigenvalues, eigenvectors = np.linalg.eigh(height)
    modular_state = eigenvectors @ np.diag(np.exp(-beta * eigenvalues)) @ eigenvectors.T
    modular_state /= np.trace(modular_state)

    samples = []
    for theta in np.linspace(-np.pi / 2.0, np.pi / 2.0, 129):
        mass = np.hstack((np.cos(theta) * identity3, np.sin(theta) * identity3))
        gram = mass.T @ mass
        hodge_residual = float(np.linalg.norm(mass @ mass.T - identity3, "fro") ** 2)
        weighted_moment = float(np.trace(modular_state @ (gram @ gram)).real)
        samples.append(
            {
                "theta": float(theta),
                "hodge_action": hodge_residual,
                "weighted_moment": weighted_moment,
            }
        )

    minimum_sample = min(samples, key=lambda row: row["weighted_moment"])
    maximum_sample = max(samples, key=lambda row: row["weighted_moment"])
    expected_minimum = 1.0 / (1.0 + np.exp(2.0 * beta))
    expected_maximum = np.exp(2.0 * beta) / (1.0 + np.exp(2.0 * beta))
    expected_gap = np.tanh(beta)
    assert abs(minimum_sample["theta"] - np.pi / 4.0) < 1e-12
    assert abs(minimum_sample["weighted_moment"] - expected_minimum) < 1e-12
    assert abs(maximum_sample["weighted_moment"] - expected_maximum) < 1e-12
    assert max(row["hodge_action"] for row in samples) < 1e-24

    step = 1e-4

    def weighted_moment(theta: float) -> float:
        mass = np.hstack((np.cos(theta) * identity3, np.sin(theta) * identity3))
        gram = mass.T @ mass
        return float(np.trace(modular_state @ (gram @ gram)).real)

    modular_hessian = (
        weighted_moment(np.pi / 4.0 + step)
        - 2.0 * weighted_moment(np.pi / 4.0)
        + weighted_moment(np.pi / 4.0 - step)
    ) / step**2
    assert abs(modular_hessian - 2.0 * np.tanh(beta)) < 1e-7

    result = {
        "gate": "version7_modular_copy_projector_origin_gate",
        "maximal_first_order_graph": {
            "vertex_count": len(vertices),
            "edge_count": len(edges),
            "adjacency_rank": int(np.linalg.matrix_rank(adjacency)),
            "adjacency_nullity": len(vertices) - int(np.linalg.matrix_rank(adjacency)),
            "physical_duplicate_twin_pairs": [list(pair) for pair in twin_pairs],
            "neighbourhoods": neighbours,
            "independent_twin_swap_group": "S2 x S2",
            "edge_orbit_count": len(edge_orbits),
            "edge_orbits": [[list(edge) for edge in orbit] for orbit in edge_orbits],
        },
        "derived_copy_operator": compressed_data,
        "modular_selector": {
            "beta": beta,
            "sample_count": len(samples),
            "maximum_unweighted_Hodge_action": max(row["hodge_action"] for row in samples),
            "minimum": minimum_sample,
            "maximum": maximum_sample,
            "analytic_minimum": expected_minimum,
            "analytic_maximum": expected_maximum,
            "analytic_gap": expected_gap,
            "finite_difference_hessian_at_minimum": modular_hessian,
            "analytic_hessian_at_minimum": 2.0 * np.tanh(beta),
            "selected_heavy_copy_parity": "even",
            "selected_light_kernel_parity": "odd",
        },
        "old_six_edge_pattern": {
            "invariant_under_twin_swaps": selected_invariant,
            "symmetric_differences": selected_symmetric_differences,
            "recovered_by_parity_selector": False,
        },
        "architectural_status": {
            "operator_derived_from_binary_maximal_incidence": True,
            "operator_derived_from_existing_physical_DF": False,
            "binary_unit_incidence_parent_previously_derived": False,
            "continuous_copy_U2_lifted": True,
            "old_new_vertex_label_selected": False,
            "status": "conditional_positive_parity_selector",
            "next_gate": "test whether maximal binary first-order incidence is an admissible universal parent on the full represented carrier without inserting unit edge maps by hand",
        },
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()