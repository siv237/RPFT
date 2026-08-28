#!/usr/bin/env python3
"""Audit a baseline-rooted primitive six-cycle on the full Version VII graph."""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v7_baseline_rooted_primitive_cycle_admission_gate_results.json"
)


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def edge(first: str, second: str) -> tuple[str, str]:
    return tuple(sorted((first, second)))


def edge_text(item: tuple[str, str]) -> str:
    return "--".join(item)


def canonical_cycle(cycle: tuple[str, ...]) -> tuple[str, ...]:
    variants = []
    for oriented in (cycle, tuple(reversed(cycle))):
        variants.extend(
            oriented[index:] + oriented[:index] for index in range(len(oriented))
        )
    return min(variants)


def simple_cycles(
    vertices: tuple[str, ...], adjacency: dict[str, set[str]]
) -> set[tuple[str, ...]]:
    result: set[tuple[str, ...]] = set()

    def search(start: str, current: str, path: tuple[str, ...]) -> None:
        for nxt in adjacency[current]:
            if nxt == start and len(path) >= 3:
                result.add(canonical_cycle(path))
            elif nxt not in path and nxt >= start:
                search(start, nxt, path + (nxt,))

    for start in vertices:
        search(start, start, (start,))
    return result


def closed_walk_monomials(
    vertices: tuple[str, ...],
    adjacency: dict[str, set[str]],
    edge_indices: dict[tuple[str, str], int],
    length: int,
    nonbacktracking: bool,
) -> Counter[tuple[int, ...]]:
    result: Counter[tuple[int, ...]] = Counter()

    def search(path: tuple[str, ...]) -> None:
        if len(path) == length:
            if path[0] not in adjacency[path[-1]]:
                return
            closed = path + (path[0],)
            if nonbacktracking:
                # Include the two cyclic boundary conditions as well as all
                # interior transitions.
                for index in range(length):
                    if closed[(index + 2) % length] == closed[index]:
                        return
            powers = [0] * len(edge_indices)
            for first, second in zip(closed, closed[1:]):
                powers[edge_indices[edge(first, second)]] += 1
            result[tuple(powers)] += 1
            return
        for nxt in adjacency[path[-1]]:
            search(path + (nxt,))

    for start in vertices:
        search((start,))
    return result


def type_preserving_automorphisms(
    vertices: tuple[str, ...],
    types: dict[str, tuple[str, ...]],
    edges: set[tuple[str, str]],
) -> list[dict[str, str]]:
    classes: dict[tuple[str, ...], list[str]] = {}
    for vertex in vertices:
        classes.setdefault(types[vertex], []).append(vertex)
    permutations = [list(itertools.permutations(group)) for group in classes.values()]
    groups = list(classes.values())
    result = []
    for choices in itertools.product(*permutations):
        mapping = {
            old: new
            for group, image in zip(groups, choices)
            for old, new in zip(group, image)
        }
        mapped_edges = {edge(mapping[first], mapping[second]) for first, second in edges}
        if mapped_edges == edges:
            result.append(mapping)
    return result


def main() -> None:
    graph = load_result("s2t_v7_four_vertex_vectorlike_selector_gate_results.json")
    previous = load_result(
        "s2t_v7_edge_coherence_full_graph_competition_gate_results.json"
    )
    assert previous["verdict"]["status"] == (
        "closed_as_selector_of_target_six_edge_extension"
    )

    carrier = graph["carrier"]
    baseline = {edge(*item.split("--")) for item in carrier["baseline_edges"]}
    new_allowed = {
        edge(*item.split("--")) for item in carrier["new_allowed_edges"]
    }
    selected_new = {
        edge(*item.split("--"))
        for item in carrier["desired_cycle_plus_vector_masses"]
    }
    unwanted_new = {
        edge(*item.split("--"))
        for item in carrier["allowed_but_unselected_edges"]
    }
    all_edges = baseline | new_allowed
    vertices = tuple(sorted({vertex for item in all_edges for vertex in item}))
    adjacency = {vertex: set() for vertex in vertices}
    for first, second in all_edges:
        adjacency[first].add(second)
        adjacency[second].add(first)

    cycles = simple_cycles(vertices, adjacency)
    cycle_counts = {
        length: sum(len(cycle) == length for cycle in cycles)
        for length in (4, 6, 8)
    }
    chordless_counts = {}
    for length in (4, 6, 8):
        count = 0
        for cycle in cycles:
            if len(cycle) != length:
                continue
            cycle_edges = {
                edge(cycle[index], cycle[(index + 1) % length])
                for index in range(length)
            }
            induced_edges = {
                item for item in all_edges if item[0] in cycle and item[1] in cycle
            }
            count += cycle_edges == induced_edges
        chordless_counts[length] = count

    target_cycle = ("Q_L", "u_R", "X_L", "e_R", "L_L", "Y_R")
    target_cycle_edges = {
        edge(target_cycle[index], target_cycle[(index + 1) % 6])
        for index in range(6)
    }
    root_edges = {edge("Q_L", "u_R"), edge("L_L", "e_R")}
    target_new_cycle_edges = target_cycle_edges - baseline
    vector_mass_edges = selected_new - target_new_cycle_edges
    target_chords = {
        item
        for item in all_edges - target_cycle_edges
        if item[0] in target_cycle and item[1] in target_cycle
    }
    assert target_chords == {edge("X_L", "Y_R")}
    assert vector_mass_edges == {edge("X_L", "X_R"), edge("Y_L", "Y_R")}

    length_six_cycles = {cycle for cycle in cycles if len(cycle) == 6}
    rooted_cycles = []
    for cycle in length_six_cycles:
        cycle_edges = {
            edge(cycle[index], cycle[(index + 1) % 6]) for index in range(6)
        }
        if root_edges <= cycle_edges:
            rooted_cycles.append(cycle)
    assert len(rooted_cycles) == 1
    assert canonical_cycle(target_cycle) == rooted_cycles[0]

    ordered_edges = tuple(sorted(all_edges))
    edge_indices = {item: index for index, item in enumerate(ordered_edges)}
    ordinary = closed_walk_monomials(
        vertices, adjacency, edge_indices, length=6, nonbacktracking=False
    )
    nonbacktracking = closed_walk_monomials(
        vertices, adjacency, edge_indices, length=6, nonbacktracking=True
    )
    squarefree_ordinary = {
        monomial: coefficient
        for monomial, coefficient in ordinary.items()
        if max(monomial) == 1
    }
    assert len(ordinary) == 305
    assert len(squarefree_ordinary) == 14
    assert set(squarefree_ordinary.values()) == {12}
    assert len(nonbacktracking) == 14
    assert set(nonbacktracking.values()) == {12}
    assert all(max(monomial) == 1 for monomial in nonbacktracking)

    root_indices = [edge_indices[item] for item in sorted(root_edges)]
    rooted_monomials = {
        monomial: coefficient
        for monomial, coefficient in nonbacktracking.items()
        if all(monomial[index] for index in root_indices)
    }
    assert len(rooted_monomials) == 1
    rooted_monomial, rooted_coefficient = next(iter(rooted_monomials.items()))
    rooted_support = {
        ordered_edges[index] for index, power in enumerate(rooted_monomial) if power
    }
    assert rooted_support == target_cycle_edges
    assert rooted_coefficient == 12

    # Exact gauge types include hypercharge.  Only the old/new lepton copies
    # remain equal.  The unmarked full graph has their S2 x S2 symmetry.
    types = {
        "Q_L": ("H", "M3", "L", "1/6"),
        "L_L": ("H", "C", "L", "-1/2"),
        "u_R": ("C", "M3", "R", "2/3"),
        "d_R": ("C", "M3", "R", "-1/3"),
        "e_R": ("C", "C", "R", "-1"),
        "X_L": ("C", "C", "L", "-1"),
        "X_R": ("C", "C", "R", "-1"),
        "Y_L": ("H", "C", "L", "-1/2"),
        "Y_R": ("H", "C", "R", "-1/2"),
    }
    automorphisms = type_preserving_automorphisms(vertices, types, all_edges)
    baseline_stabilizer = [
        mapping
        for mapping in automorphisms
        if {edge(mapping[a], mapping[b]) for a, b in baseline} == baseline
    ]
    assert len(automorphisms) == 4
    assert len(baseline_stabilizer) == 1

    # After the two baseline edge amplitudes are treated as a fixed nonzero
    # background, the rooted cycle word is quartic in new edge fields.  It
    # therefore has zero quadratic Hessian at the origin and cannot launch
    # the extension by itself.
    rooted_new_field_degree = sum(
        rooted_monomial[edge_indices[item]] for item in new_allowed
    )
    assert rooted_new_field_degree == 4

    result = {
        "gate": "version7_baseline_rooted_primitive_cycle_admission_gate",
        "full_graph": {
            "vertices": list(vertices),
            "undirected_edges": [edge_text(item) for item in ordered_edges],
            "vertex_count": len(vertices),
            "edge_count": len(ordered_edges),
            "simple_cycle_counts": {str(key): value for key, value in cycle_counts.items()},
            "chordless_cycle_counts": {
                str(key): value for key, value in chordless_counts.items()
            },
        },
        "ordinary_sixth_trace": {
            "distinct_monomials": len(ordinary),
            "squarefree_simple_cycle_monomials": len(squarefree_ordinary),
            "simple_cycle_coefficient_set": sorted(set(squarefree_ordinary.values())),
            "target_is_unique_by_unrooted_coefficient": False,
        },
        "nonbacktracking_sixth_trace": {
            "distinct_monomials": len(nonbacktracking),
            "all_monomials_are_simple_six_cycles": True,
            "coefficient_set": sorted(set(nonbacktracking.values())),
            "target_is_unique_before_rooting": False,
        },
        "baseline_rooted_selector": {
            "root_edges": [edge_text(item) for item in sorted(root_edges)],
            "rooted_primitive_six_cycles": len(rooted_cycles),
            "unique_cycle": list(rooted_cycles[0]),
            "unique_cycle_edges": [edge_text(item) for item in sorted(rooted_support)],
            "rooted_trace_coefficient": rooted_coefficient,
            "contains_unwanted_new_edge": bool(rooted_support & unwanted_new),
            "new_cycle_edges": [
                edge_text(item) for item in sorted(target_new_cycle_edges)
            ],
            "desired_vector_mass_edges_not_in_cycle": [
                edge_text(item) for item in sorted(vector_mass_edges)
            ],
            "target_chord": [edge_text(item) for item in sorted(target_chords)],
        },
        "canonicity_test": {
            "type_preserving_full_graph_automorphisms": len(automorphisms),
            "expected_unmarked_twin_group_order": 4,
            "type_and_baseline_support_preserving_automorphisms": len(
                baseline_stabilizer
            ),
            "baseline_support_breaks_old_new_twin_symmetry": True,
            "selector_is_absolute_from_full_graph_alone": False,
            "selector_is_canonical_relative_to_fixed_H15_background": True,
        },
        "dynamical_gap": {
            "degree_in_new_fields_after_fixing_nonzero_baseline": rooted_new_field_degree,
            "quadratic_hessian_at_zero_new_fields": "zero",
            "launches_extension_from_zero": False,
            "selects_two_vectorlike_mass_edges": False,
            "suppresses_all_other_allowed_edges": False,
        },
        "verdict": {
            "status": "positive_relative_cycle_observable_not_full_parent",
            "primitive_target_cycle_isolated": True,
            "isolation_requires_only_pre_extension_H15_support": True,
            "complete_six_edge_repair_selected": False,
            "single_source_dynamics_obtained": False,
            "next_gate": "test whether the rooted primitive-cycle response canonically induces a quadratic edge projector that launches the four cycle edges, generates the two vectorlike masses, and gaps the five unwanted edges without free coefficients",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()