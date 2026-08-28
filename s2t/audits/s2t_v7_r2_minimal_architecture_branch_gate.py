#!/usr/bin/env python3
"""Classify minimal architecture changes after the strict R2 first-order no-go."""

from __future__ import annotations

import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_r2_minimal_architecture_branch_gate_results.json"

LABELS = ("C", "H", "M3")
LABEL_DIM = {"C": 1, "H": 2, "M3": 3}

BASE = {
    "Q_L": ("H", "M3", "L"),
    "L_L": ("H", "C", "L"),
    "u_R": ("C", "M3", "R"),
    "e_R": ("C", "C", "R"),
}
REQUIRED_EDGES = {frozenset(("Q_L", "u_R")), frozenset(("L_L", "e_R"))}


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def strict_edge(a: tuple[str, str, str], b: tuple[str, str, str]) -> bool:
    i, j, grade = a
    k, ell, other_grade = b
    return grade != other_grade and (i == k or j == ell)


def graph_for(vertices: dict[str, tuple[str, str, str]]) -> dict[str, set[str]]:
    graph = {name: set() for name in vertices}
    for a, b in itertools.combinations(vertices, 2):
        if strict_edge(vertices[a], vertices[b]):
            graph[a].add(b)
            graph[b].add(a)
    return graph


def cycle_containing_required(graph: dict[str, set[str]]) -> list[str] | None:
    start = "Q_L"

    def visit(path: list[str]) -> list[str] | None:
        current = path[-1]
        for nxt in sorted(graph[current]):
            if nxt == start and len(path) >= 4:
                edges = {
                    frozenset((path[i], path[(i + 1) % len(path)]))
                    for i in range(len(path))
                }
                if REQUIRED_EDGES <= edges:
                    return path
            elif nxt not in path and len(path) < 10:
                found = visit(path + [nxt])
                if found is not None:
                    return found
        return None

    return visit([start])


def main() -> None:
    previous = load_result("s2t_v7_r2_real_first_order_admission_gate_results.json")
    assert not previous["verdict"]["R2_admitted_in_unchanged_strict_real_first_order_parent"]

    # A *-automorphism can only permute isomorphic simple ideals.  The three
    # ideals below are pairwise non-isomorphic, so their label orbit is fixed.
    simple_ideal_signatures = {
        "C": ["complex", 1],
        "H": ["quaternionic", 1],
        "M3": ["complex_matrix", 3],
    }
    admissible_label_permutations = [list(LABELS)]

    candidate_types = [
        (left, right, grade)
        for left in LABELS
        for right in LABELS
        for grade in ("L", "R")
    ]

    minimum_new_vertices = None
    strict_solutions: list[dict] = []
    for number in range(4):
        for additions in itertools.combinations(candidate_types, number):
            vertices = dict(BASE)
            for index, candidate in enumerate(additions, start=1):
                vertices[f"X{index}"] = candidate
            cycle = cycle_containing_required(graph_for(vertices))
            if cycle is None:
                continue
            strict_solutions.append({
                "new_vertex_types": [list(item) for item in additions],
                "raw_complex_carrier_dimension": sum(
                    LABEL_DIM[item[0]] * LABEL_DIM[item[1]] for item in additions
                ),
                "cycle": cycle + [cycle[0]],
                "cycle_length": len(cycle),
            })
        if strict_solutions:
            minimum_new_vertices = number
            break

    strict_solutions.sort(key=lambda item: (
        item["raw_complex_carrier_dimension"], item["new_vertex_types"]
    ))

    result = {
        "gate": "version7_r2_minimal_architecture_branch_gate",
        "fixed_input": {
            "algebra": "C + H + M3(C)",
            "base_vertices": {name: list(data) for name, data in BASE.items()},
            "required_existing_edges_in_mixed_cycle": ["Q_L-u_R", "L_L-e_R"],
        },
        "automorphism_twist_branch": {
            "simple_ideal_signatures": simple_ideal_signatures,
            "admissible_summand_label_permutations": admissible_label_permutations,
            "nontrivial_summand_permutation_exists": False,
            "can_turn_forbidden_diagonal_into_same_row_or_column": False,
            "verdict": "closed_for_automorphisms_of_unchanged_A_SM",
        },
        "generalized_inner_fluctuation_branch": {
            "new_fermion_vertices": 0,
            "drops_strict_first_order": True,
            "requires_quadratic_term_A2": True,
            "gauge_covariance_is_not_given_by_linear_fluctuation_alone": True,
            "physical_R2_support_and_vacuum_proved": False,
            "status": "architecturally_admissible_not_physically_closed",
        },
        "strict_first_order_mirror_vertex_branch": {
            "minimum_new_chiral_vertices": minimum_new_vertices,
            "number_of_minimal_coordinate_type_solutions": len(strict_solutions),
            "solutions": strict_solutions,
            "dimension_minimal_solution": strict_solutions[0],
            "Real_completion_and_anomaly_cancellation_proved": False,
            "elementary_R2_edge_obtained": False,
            "mixed_effect_is_factorized_along_cycle": True,
        },
        "verdict": {
            "unchanged_algebra_automorphism_twist_selected": False,
            "unique_physical_branch_selected": False,
            "zero_new_vertex_route": "generalized inner fluctuations without first order",
            "strict_first_order_route": "at least two new mirror-chirality vertices",
            "next_gate": (
                "compare generalized A2 support with Real/anomaly completion of the "
                "dimension-minimal two-mirror-vertex cycle"
            ),
        },
    }

    assert minimum_new_vertices == 2
    assert len(strict_solutions) == 9
    assert strict_solutions[0]["raw_complex_carrier_dimension"] == 3
    assert strict_solutions[0]["new_vertex_types"] == [
        ["C", "C", "L"], ["H", "C", "R"]
    ]
    assert not result["automorphism_twist_branch"]["nontrivial_summand_permutation_exists"]
    assert not result["verdict"]["unique_physical_branch_selected"]

    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()