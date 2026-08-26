#!/usr/bin/env python3
"""Classify the minimal mixed Krajewski-cycle completion of charged H15."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_minimal_h15_mixed_connector_admission_gate_results.json"

LEFT = {
    "Q_L": {"colour": "3", "hypercharge": Fraction(1, 6)},
    "L_L": {"colour": "1", "hypercharge": Fraction(-1, 2)},
}
RIGHT = {
    "u_R": {"colour": "3", "hypercharge": Fraction(2, 3)},
    "d_R": {"colour": "3", "hypercharge": Fraction(-1, 3)},
    "e_R": {"colour": "1", "hypercharge": Fraction(-1, 1)},
}
EXISTING = {("Q_L", "u_R"), ("Q_L", "d_R"), ("L_L", "e_R")}
MISSING = set(itertools.product(LEFT, RIGHT)) - EXISTING


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def scalar_for_edge(edge: tuple[str, str]) -> dict:
    left, right = edge
    hypercharge = LEFT[left]["hypercharge"] - RIGHT[right]["hypercharge"]
    if LEFT[left]["colour"] == "1" and RIGHT[right]["colour"] == "3":
        colour = "3bar"
    elif LEFT[left]["colour"] == "3" and RIGHT[right]["colour"] == "1":
        colour = "3"
    else:
        colour = "1+8"
    return {
        "edge": f"{left}->{right}",
        "representation_in_barL_S_R_convention": [
            colour, "2", f"{hypercharge.numerator}/{hypercharge.denominator}"
        ],
    }


def rectangles(edges: set[tuple[str, str]]) -> list[list[str]]:
    found = []
    for right_pair in itertools.combinations(RIGHT, 2):
        if set(itertools.product(LEFT, right_pair)) <= edges:
            found.append(list(right_pair))
    return found


def multiplet(edge: tuple[str, str]) -> str:
    return {
        ("L_L", "u_R"): "R2=(3,2,7/6) up to conjugation",
        ("Q_L", "e_R"): "R2=(3,2,7/6) up to conjugation",
        ("L_L", "d_R"): "R2_tilde=(3,2,1/6) up to conjugation",
    }[edge]


def main() -> None:
    oneform = load_result("s2t_v5_h15_physical_oneform_bimodule_gate_results.json")
    square = load_result("s2t_v4_order_one_krajewski_square_gate_results.json")
    quartic = load_result("s2t_v7_quartic_cross_edge_invariant_admission_gate_results.json")
    assert square["minimum_order_one_cycle_length"] == 4
    assert quartic["verdict"]["raising_polynomial_degree_without_new_connector_can_help"] is False
    assert oneform["charged_edge_multiplicity_space"]["bimodule_endomorphism_algebra"] == "C^3"

    completions: list[dict] = []
    minimum_new_edges = None
    for size in range(len(MISSING) + 1):
        for addition in itertools.combinations(sorted(MISSING), size):
            cycles = rectangles(EXISTING | set(addition))
            if cycles:
                fields = sorted({multiplet(edge) for edge in addition})
                completions.append({
                    "added_edges": [f"{a}->{b}" for a, b in addition],
                    "added_scalar_representations": [scalar_for_edge(edge) for edge in addition],
                    "complex_scalar_multiplets": fields,
                    "number_of_distinct_complex_scalar_multiplets": len(fields),
                    "completed_right_pair": cycles[0],
                })
        if completions:
            minimum_new_edges = size
            break

    one_field = [x for x in completions if x["number_of_distinct_complex_scalar_multiplets"] == 1]
    result = {
        "gate": "version7_minimal_h15_mixed_connector_admission_gate",
        "fixed_fermion_graph": {
            "left_vertices": list(LEFT),
            "right_vertices": list(RIGHT),
            "existing_edges": [f"{a}->{b}" for a, b in sorted(EXISTING)],
            "missing_edges": [f"{a}->{b}" for a, b in sorted(MISSING)],
            "existing_graph_contains_four_cycle": bool(rectangles(EXISTING)),
            "current_edge_endomorphism_algebra": "C^3",
        },
        "order_one_cycle_preclassification": {
            "minimum_cycle_length_from_prior_gate": 4,
            "minimum_number_of_added_edges_on_fixed_vertices": minimum_new_edges,
            "minimal_completions": completions,
            "number_of_minimal_edge_completions": len(completions),
        },
        "scalar_multiplet_minimality": {
            "one_complex_multiplet_completions": one_field,
            "unique_one_complex_multiplet_completion": len(one_field) == 1,
            "candidate": "R2=(3,2,7/6) plus Hermitian conjugate",
            "candidate_edges": ["Q_L->e_R", "L_L->u_R"],
            "second_standard_Higgs_adds_graph_edges": 0,
            "second_standard_Higgs_completes_rectangle": False,
        },
        "typing_boundary": {
            "preserves_fixed_fermion_vertices_H15": True,
            "preserves_current_physical_oneform_bimodule": False,
            "already_present_in_current_finite_Dirac_operator": False,
            "requires_new_coloured_bifundamental_oneform_sector": True,
            "grading_L_to_R_compatible": True,
            "strict_Real_first_order_admission_proved": False,
            "colour_preserving_vacuum_proved": False,
            "family_selector_proved": False,
        },
        "verdict": {
            "connector_admitted_in_unchanged_parent": False,
            "graph_minimal_candidate_identified": True,
            "graph_minimal_candidate": "one complex R2 multiplet completing the u-e rectangle",
            "physical_model_admission": "conditional_open",
            "next_gate": "R2 connector Real, first-order, spectral-action and colour-vacuum admission",
        },
    }
    assert minimum_new_edges == 2
    assert len(completions) == 3
    assert len(one_field) == 1
    assert set(one_field[0]["added_edges"]) == {"L_L->u_R", "Q_L->e_R"}
    assert not result["verdict"]["connector_admitted_in_unchanged_parent"]
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()