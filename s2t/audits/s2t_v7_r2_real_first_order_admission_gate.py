#!/usr/bin/env python3
"""Audit strict Real/first-order admission of the graph-minimal R2 connector."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_r2_real_first_order_admission_gate_results.json"

# Coarse bimodule coordinates for A_SM = C + H + M3(C).
# Complex-conjugate C representations do not affect the summand-label
# obstruction tested here.
VERTICES = {
    "Q_L": ("H", "M3"),
    "L_L": ("H", "C"),
    "u_R": ("C", "M3"),
    "d_R": ("C", "M3"),
    "e_R": ("C", "C"),
}

EXISTING = [("Q_L", "u_R"), ("Q_L", "d_R"), ("L_L", "e_R")]
MISSING = [("L_L", "u_R"), ("L_L", "d_R"), ("Q_L", "e_R")]
R2_EDGES = [("L_L", "u_R"), ("Q_L", "e_R")]


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def central_idempotent_residual(source: str, target: str) -> int:
    """Maximum exact double-commutator coefficient on central idempotents."""
    i, j = VERTICES[source]
    k, ell = VERTICES[target]
    return int(i != k and j != ell)


def edge_record(edge: tuple[str, str]) -> dict:
    source, target = edge
    i, j = VERTICES[source]
    k, ell = VERTICES[target]
    residual = central_idempotent_residual(source, target)
    return {
        "edge": f"{source}->{target}",
        "source_bimodule": [i, j],
        "target_bimodule": [k, ell],
        "same_left_coordinate": i == k,
        "same_right_coordinate": j == ell,
        "maximum_central_idempotent_double_commutator_residual": residual,
        "strict_first_order_pass": residual == 0,
    }


def conjugate_record(edge: tuple[str, str]) -> dict:
    source, target = edge
    i, j = VERTICES[source]
    k, ell = VERTICES[target]
    # J exchanges a bimodule (i,j) with its opposite (j,i).
    residual = int(j != ell and i != k)
    return {
        "edge": f"J({source}->{target})J^-1",
        "source_opposite_bimodule": [j, i],
        "target_opposite_bimodule": [ell, k],
        "maximum_central_idempotent_double_commutator_residual": residual,
        "strict_first_order_pass": residual == 0,
    }


def main() -> None:
    previous = load_result("s2t_v7_minimal_h15_mixed_connector_admission_gate_results.json")
    assert previous["scalar_multiplet_minimality"]["unique_one_complex_multiplet_completion"]
    assert set(previous["scalar_multiplet_minimality"]["candidate_edges"]) == {
        "Q_L->e_R", "L_L->u_R"
    }

    existing_records = [edge_record(edge) for edge in EXISTING]
    missing_records = [edge_record(edge) for edge in MISSING]
    r2_records = [edge_record(edge) for edge in R2_EDGES]
    r2_conjugates = [conjugate_record(edge) for edge in R2_EDGES]

    result = {
        "gate": "version7_r2_real_first_order_admission_gate",
        "algebra": "A_SM = C + H + M3(C)",
        "first_order_edge_criterion": {
            "edge": "D_(ij,kl): H_(ij) -> H_(kl)",
            "double_commutator_coefficient": "(a_i-a_k) D_(ij,kl) (b_j-b_l)",
            "pass_iff": "i=k or j=l",
            "test_basis": "central summand idempotents",
        },
        "standard_bimodule_coordinates": {
            name: list(coords) for name, coords in VERTICES.items()
        },
        "existing_yukawa_edges": existing_records,
        "all_missing_fixed_vertex_edges": missing_records,
        "graph_minimal_R2_candidate": {
            "edges": r2_records,
            "J_conjugate_edges": r2_conjugates,
            "all_edges_fail_strict_first_order": all(
                not item["strict_first_order_pass"] for item in r2_records + r2_conjugates
            ),
            "Real_completion_repairs_obstruction": False,
        },
        "S0_reality_boundary": {
            "strict_S0_preserves_particle_antiparticle_separation": True,
            "historical_leptoquark_channel_requires_dropping_S0": True,
            "historical_channel_identical_to_two_edge_R2_rectangle": False,
        },
        "verdict": {
            "R2_admitted_in_unchanged_strict_real_first_order_parent": False,
            "any_missing_edge_admitted_on_fixed_vertices": any(
                item["strict_first_order_pass"] for item in missing_records
            ),
            "spectral_action_and_colour_vacuum_stage_reached": False,
            "reason": "both bimodule coordinates change on every missing edge",
            "next_gate": (
                "classify the minimal algebra/representation or twisted/generalized-first-order "
                "extension that turns an R2 path into allowed same-row/same-column edges"
            ),
        },
    }

    assert all(item["strict_first_order_pass"] for item in existing_records)
    assert all(not item["strict_first_order_pass"] for item in missing_records)
    assert result["graph_minimal_R2_candidate"]["all_edges_fail_strict_first_order"]
    assert not result["verdict"]["R2_admitted_in_unchanged_strict_real_first_order_parent"]
    assert not result["verdict"]["spectral_action_and_colour_vacuum_stage_reached"]

    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()