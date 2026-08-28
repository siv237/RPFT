#!/usr/bin/env python3
"""Audit strict bimodule admission of the 1-6-3 coherence chain."""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_edge_coherence_bimodule_admission_gate_results.json"

SIMPLE_DIMENSIONS = {"C": 1, "H": 2, "M3": 3}


def module_dimension(coordinates: tuple[str, str]) -> int:
    return SIMPLE_DIMENSIONS[coordinates[0]] * SIMPLE_DIMENSIONS[coordinates[1]]


def first_order_allowed(
    source: tuple[str, str], target: tuple[str, str]
) -> bool:
    return source[0] == target[0] or source[1] == target[1]


def central_idempotent_residuals(
    source: tuple[str, str], target: tuple[str, str]
) -> list[int]:
    labels = tuple(SIMPLE_DIMENSIONS)
    residuals = []
    for left_test, right_test in product(labels, repeat=2):
        left = int(source[0] == left_test) - int(target[0] == left_test)
        right = int(source[1] == right_test) - int(target[1] == right_test)
        residuals.append(left * right)
    return residuals


def main() -> None:
    previous = json.loads(
        (
            ROOT / "s2t/results/s2t_v7_edge_coherence_spectral_parent_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert previous["verdict"]["status"] == (
        "positive_graded_spectral_parent_strict_algebraic_embedding_open"
    )

    irreducibles = [
        (left, right)
        for left, right in product(SIMPLE_DIMENSIONS, repeat=2)
    ]
    by_dimension = {
        dimension: [
            coordinates
            for coordinates in irreducibles
            if module_dimension(coordinates) == dimension
        ]
        for dimension in (1, 3, 6)
    }
    strict_irreducible_chains = []
    for first, middle, last in product(
        by_dimension[1], by_dimension[6], by_dimension[3]
    ):
        if first_order_allowed(first, middle) and first_order_allowed(middle, last):
            strict_irreducible_chains.append((first, middle, last))
    assert by_dimension[1] == [("C", "C")]
    assert set(by_dimension[6]) == {("H", "M3"), ("M3", "H")}
    assert strict_irreducible_chains == []

    vertices = {
        "Q_L": {"coordinates": ("H", "M3"), "chirality": "L", "dimension": 6},
        "L_L": {"coordinates": ("H", "C"), "chirality": "L", "dimension": 2},
        "u_R": {"coordinates": ("C", "M3"), "chirality": "R", "dimension": 3},
        "d_R": {"coordinates": ("C", "M3"), "chirality": "R", "dimension": 3},
        "e_R": {"coordinates": ("C", "C"), "chirality": "R", "dimension": 1},
        "X_L": {"coordinates": ("C", "C"), "chirality": "L", "dimension": 1},
        "X_R": {"coordinates": ("C", "C"), "chirality": "R", "dimension": 1},
        "Y_L": {"coordinates": ("H", "C"), "chirality": "L", "dimension": 2},
        "Y_R": {"coordinates": ("H", "C"), "chirality": "R", "dimension": 2},
    }
    physical_candidates = []
    for first_name, middle_name, last_name in product(vertices, repeat=3):
        first = vertices[first_name]
        middle = vertices[middle_name]
        last = vertices[last_name]
        if (first["dimension"], middle["dimension"], last["dimension"]) != (1, 6, 3):
            continue
        if not (
            first["chirality"] == last["chirality"]
            and first["chirality"] != middle["chirality"]
        ):
            continue
        edge_one = first_order_allowed(first["coordinates"], middle["coordinates"])
        edge_two = first_order_allowed(middle["coordinates"], last["coordinates"])
        physical_candidates.append(
            {
                "vertices": [first_name, middle_name, last_name],
                "first_edge_allowed": edge_one,
                "second_edge_allowed": edge_two,
                "full_chain_allowed": edge_one and edge_two,
                "first_edge_max_central_residual": max(
                    abs(x)
                    for x in central_idempotent_residuals(
                        first["coordinates"], middle["coordinates"]
                    )
                ),
                "second_edge_max_central_residual": max(
                    abs(x)
                    for x in central_idempotent_residuals(
                        middle["coordinates"], last["coordinates"]
                    )
                ),
            }
        )
    assert len(physical_candidates) == 4
    assert all(not row["first_edge_allowed"] for row in physical_candidates)
    assert all(row["second_edge_allowed"] for row in physical_candidates)
    assert all(not row["full_chain_allowed"] for row in physical_candidates)

    # The conjugate orientation swaps both coordinates and gives the same result.
    conjugate_candidates = []
    for row in physical_candidates:
        names = row["vertices"]
        coordinates = [
            tuple(reversed(vertices[name]["coordinates"])) for name in names
        ]
        conjugate_candidates.append(
            {
                "vertices": [f"{name}^c" for name in names],
                "first_edge_allowed": first_order_allowed(
                    coordinates[0], coordinates[1]
                ),
                "second_edge_allowed": first_order_allowed(
                    coordinates[1], coordinates[2]
                ),
            }
        )
    assert all(not row["first_edge_allowed"] for row in conjugate_candidates)
    assert all(row["second_edge_allowed"] for row in conjugate_candidates)

    # A reducible same-column chain is algebraically possible, but absent at
    # the required multiplicities in the admitted physical carrier.
    reducible_chain = {
        "H0": {"type": ("C", "C", "R"), "multiplicity": 1, "dimension": 1},
        "H1": {"type": ("H", "C", "L"), "multiplicity": 3, "dimension": 6},
        "H2": {"type": ("C", "C", "R"), "multiplicity": 3, "dimension": 3},
    }
    available = {
        ("H", "C", "L"): 2,
        ("C", "C", "R"): 2,
    }
    required = {
        ("H", "C", "L"): 3,
        ("C", "C", "R"): 4,
    }
    deficits = {
        "/".join(key): required[key] - available.get(key, 0) for key in required
    }
    assert deficits == {"H/C/L": 1, "C/C/R": 2}
    assert first_order_allowed(("C", "C"), ("H", "C"))
    assert first_order_allowed(("H", "C"), ("C", "C"))

    result = {
        "gate": "version7_edge_coherence_bimodule_admission_gate",
        "algebra": {
            "simple_summands": ["C", "H", "M3(C)"],
            "complex_irrep_dimensions": SIMPLE_DIMENSIONS,
            "first_order_edge_rule": "same left coordinate or same right coordinate",
        },
        "irreducible_dimension_test": {
            "dimension_1_modules": by_dimension[1],
            "dimension_6_modules": by_dimension[6],
            "dimension_3_modules": by_dimension[3],
            "strict_1_6_3_chains": strict_irreducible_chains,
            "reason": "the unique 1D C-C module shares no coordinate with either 6D H-M3 or M3-H module",
        },
        "admitted_carrier_test": {
            "vertices": vertices,
            "candidate_chains": physical_candidates,
            "candidate_count": len(physical_candidates),
            "admitted_chain_count": sum(
                row["full_chain_allowed"] for row in physical_candidates
            ),
            "conjugate_candidates": conjugate_candidates,
            "Real_completion_repairs_first_edge": False,
        },
        "reducible_same_column_alternative": {
            "chain": reducible_chain,
            "first_order": True,
            "required_multiplicities": {
                "/".join(key): value for key, value in required.items()
            },
            "available_multiplicities": {
                "/".join(key): value for key, value in available.items()
            },
            "deficits": deficits,
            "new_physical_chiral_vertices_before_anomaly_completion": 3,
            "simplest_vectorlike_completion_adds_mirror_vertices": 3,
            "exterior_edge_relation_forced_by_first_order": False,
        },
        "interpretation": {
            "six_dimensional_middle_space_in_spectral_parent": "space of edge amplitudes V tensor W*, not an existing irreducible fermion bimodule",
            "three_dimensional_endpoint": "exterior composite Lambda^2 V tensor Lambda^2 W*, not an existing endpoint node",
            "graded_spectral_parent_remains_valid_as_field_space_complex": True,
            "strict_physical_finite_triple_embedding_on_unchanged_carrier": False,
        },
        "verdict": {
            "status": "closed_on_unchanged_physical_bimodule_carrier",
            "spectral_trace_identity_preserved": True,
            "physical_embedding_preserved": False,
            "next_gate": "test whether the 1-6-3 chain can be an auxiliary BRST/BV or mapping-cone field-space complex without adding physical fermion vertices",
        },
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()