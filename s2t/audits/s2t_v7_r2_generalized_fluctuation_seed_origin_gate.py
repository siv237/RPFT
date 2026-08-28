#!/usr/bin/env python3
"""Test whether the admitted H15 seed can generate a nonzero generalized A2."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_r2_generalized_fluctuation_seed_origin_gate_results.json"
NODES = ("Q_L", "L_L", "u_R", "d_R", "e_R")
COORDS = {
    "Q_L": ("H", "M3"), "L_L": ("H", "C"),
    "u_R": ("C", "M3"), "d_R": ("C", "M3"), "e_R": ("C", "C"),
}
SUMMANDS = ("C", "H", "M3")
ADMITTED_EDGES = (("Q_L", "u_R"), ("Q_L", "d_R"), ("L_L", "e_R"))
R2_EDGES = (("L_L", "u_R"), ("Q_L", "e_R"))


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def edge_operator(edges, weights) -> np.ndarray:
    index = {name: i for i, name in enumerate(NODES)}
    result = np.zeros((len(NODES), len(NODES)), dtype=np.complex128)
    for (source, target), weight in zip(edges, weights, strict=True):
        i, j = index[source], index[target]
        result[i, j], result[j, i] = weight, np.conjugate(weight)
    return result


def central_action(coordinate: int, summand: str) -> np.ndarray:
    return np.diag([
        1.0 if COORDS[node][coordinate] == summand else 0.0 for node in NODES
    ]).astype(np.complex128)


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def first_order_residuals(d: np.ndarray) -> list[float]:
    return [
        float(np.linalg.norm(commutator(
            commutator(d, central_action(0, left)),
            central_action(1, right),
        )))
        for left in SUMMANDS for right in SUMMANDS
    ]


def generalized_unitary_terms(d: np.ndarray) -> dict:
    phases = {"C": np.exp(0.37j), "H": -1.0 + 0.0j, "M3": np.exp(0.91j)}
    left = np.diag([phases[COORDS[node][0]] for node in NODES])
    right = np.diag([phases[COORDS[node][1]] for node in NODES])
    total = left @ right
    transformed = total @ d @ total.conj().T
    a1 = left @ d @ left.conj().T - d
    a1_opposite = right @ d @ right.conj().T - d
    a2 = transformed - d - a1 - a1_opposite
    return {
        "A1_norm": float(np.linalg.norm(a1)),
        "A1_opposite_norm": float(np.linalg.norm(a1_opposite)),
        "A2_norm": float(np.linalg.norm(a2)),
        "full_gauge_covariance_residual": float(np.linalg.norm(
            transformed - (d + a1 + a1_opposite + a2)
        )),
    }


def main() -> None:
    lift = load_result("s2t_v7_affine_physical_module_canonical_lift_gate_results.json")
    first_order = load_result("s2t_v7_r2_real_first_order_admission_gate_results.json")
    branch = load_result("s2t_v7_r2_minimal_architecture_branch_gate_results.json")
    assert lift["corrected_carrier"]["formula"] == "E_aff tensor Lambda_ch"
    assert all(x["strict_first_order_pass"] for x in first_order["existing_yukawa_edges"])
    assert branch["generalized_inner_fluctuation_branch"]["requires_quadratic_term_A2"]

    admitted = edge_operator(ADMITTED_EDGES, (1.0 + 0.2j, -0.7 + 0.4j, 0.6 - 0.3j))
    forbidden = edge_operator(R2_EDGES, (0.9 + 0.1j, -0.5 + 0.8j))
    admitted_residuals = first_order_residuals(admitted)
    forbidden_residuals = first_order_residuals(forbidden)
    admitted_terms = generalized_unitary_terms(admitted)
    forbidden_terms = generalized_unitary_terms(forbidden)

    scan = []
    reference = forbidden_terms["A2_norm"]
    for scale in (0.25, 0.5, 1.0, 2.0):
        terms = generalized_unitary_terms(admitted + scale * forbidden)
        scan.append({
            "forbidden_seed_scale": scale,
            "A2_norm": terms["A2_norm"],
            "linearity_residual": abs(terms["A2_norm"] - scale * reference),
        })

    result = {
        "gate": "version7_r2_generalized_fluctuation_seed_origin_gate",
        "scope": {
            "finite_vertices": list(NODES),
            "admitted_edge_support": [f"{a}->{b}" for a, b in ADMITTED_EDGES],
            "positive_control_R2_support": [f"{a}->{b}" for a, b in R2_EDGES],
            "family_lift": "central algebra actions tensor identity on E_aff",
        },
        "first_order_source_tensor": {
            "admitted_seed_maximum_residual": max(admitted_residuals),
            "forbidden_R2_seed_maximum_residual": max(forbidden_residuals),
            "admitted_seed_double_commutators_all_zero": max(admitted_residuals) < 1e-13,
            "forbidden_seed_has_nonzero_double_commutator": max(forbidden_residuals) > 1e-6,
        },
        "single_unitary_generalized_fluctuation": {
            "admitted_seed": admitted_terms,
            "forbidden_R2_positive_control": forbidden_terms,
            "forbidden_seed_scale_scan": scan,
        },
        "analytic_extension": {
            "any_linear_combination_on_u_d_e_edges_has_A2_zero": True,
            "tensoring_family_multiplicity_can_change_this": False,
            "reason": "double commutator vanishes before the family tensor factor",
        },
        "verdict": {
            "nonzero_A2_generated_from_current_admitted_parent": False,
            "nonzero_A2_requires_first_order_violating_seed": True,
            "R2_obtained_without_inserting_new_sector": False,
            "zero_new_vertex_generalized_route_as_derivation": "closed_circular",
            "generalized_route_as_explicit_new_model": "still_possible",
            "next_gate": "Real and anomaly completion of the minimal two-mirror-vertex strict cycle",
        },
    }
    assert max(admitted_residuals) < 1e-13
    assert max(forbidden_residuals) > 1e-6
    assert admitted_terms["A2_norm"] < 1e-13
    assert forbidden_terms["A2_norm"] > 1e-6
    assert max(x["linearity_residual"] for x in scan) < 1e-13
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()