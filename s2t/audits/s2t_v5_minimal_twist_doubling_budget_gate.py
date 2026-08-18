#!/usr/bin/env python3
"""Budget and incidence audit for selective one-summand twists."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_minimal_twist_doubling_budget_gate_results.json"

vertices = [
    {"name": "p0", "left": "R0", "right": "R0", "grading": "+"},
    {"name": "p1", "left": "G", "right": "R0", "grading": "-"},
    {"name": "p2", "left": "G", "right": "C2", "grading": "+"},
    {"name": "c0", "left": "R0", "right": "R0", "grading": "-"},
    {"name": "c1", "left": "R0", "right": "G", "grading": "+"},
    {"name": "c2", "left": "C2", "right": "G", "grading": "-"},
]

support = {}
for summand in ("R0", "G", "C2"):
    counts = {"+": 0, "-": 0}
    for vertex in vertices:
        counts[vertex["grading"]] += int(vertex["left"] == summand)
        counts[vertex["grading"]] += int(vertex["right"] == summand)
    support[summand] = counts

assert support == {
    "R0": {"+": 3, "-": 3},
    "G": {"+": 2, "-": 2},
    "C2": {"+": 1, "-": 1},
}

edges = {
    "X": {"source": ("R0", "R0"), "target": ("G", "R0")},
    "Y": {"source": ("G", "R0"), "target": ("G", "C2")},
}

coverage = {}
for summand in ("R0", "G", "C2"):
    touched = []
    for edge_name, edge in edges.items():
        labels = edge["source"] + edge["target"]
        if summand in labels:
            touched.append(edge_name)
    coverage[summand] = sorted(touched)

assert coverage["R0"] == ["X", "Y"]
assert coverage["G"] == ["X", "Y"]
assert coverage["C2"] == ["Y"]

branches = {
    "duplicate_R0": {
        "simple_summands": 4,
        "within_budget": True,
        "graded_support": support["R0"],
        "edges_touched": coverage["R0"],
        "both_arrows": True,
        "extra_continuous_gauge_generators": 0,
        "new_fermion_dimensions_required_at_support_level": 0,
    },
    "duplicate_M3R_G": {
        "simple_summands": 4,
        "within_budget": True,
        "graded_support": support["G"],
        "edges_touched": coverage["G"],
        "both_arrows": True,
        "extra_continuous_gauge_generators": 3,
        "new_fermion_dimensions_required_at_support_level": 0,
    },
    "duplicate_C2": {
        "simple_summands": 4,
        "within_budget": True,
        "graded_support": support["C2"],
        "edges_touched": coverage["C2"],
        "both_arrows": False,
        "extra_continuous_gauge_generators": 1,
        "new_fermion_dimensions_required_at_support_level": 0,
    },
    "full_algebra_doubling": {
        "simple_summands": 6,
        "within_budget": False,
        "both_arrows": True,
        "extra_continuous_gauge_generators": 4,
        "new_fermion_dimensions_required_at_support_level": 0,
    },
}

eligible = [
    name
    for name, data in branches.items()
    if data["within_budget"] and data["both_arrows"]
]
selected = min(
    eligible,
    key=lambda name: branches[name]["extra_continuous_gauge_generators"],
)
assert eligible == ["duplicate_R0", "duplicate_M3R_G"]
assert selected == "duplicate_R0"

result = {
    "date": "2026-08-16",
    "gate": "version5_minimal_twist_doubling_budget_gate",
    "vertices": vertices,
    "graded_label_support": support,
    "edge_incidence": edges,
    "summand_edge_coverage": coverage,
    "frozen_simple_summand_budget": 4,
    "branches": branches,
    "eligible_two_arrow_branches": eligible,
    "selected_branch": selected,
    "selection_scope": "one explicit twisted KO6 representation kill-test",
    "unresolved": [
        "faithful representation of both R0 copies",
        "compatibility with J and gamma",
        "twisted order-zero and first-order conditions",
        "radial quartic cross sign",
        "common kinetic normalization",
    ],
    "verdict": {
        "finite_selective_menu": "pass",
        "full_doubling": "rejected_by_budget",
        "duplicate_C2": "deferred_one_arrow_only",
        "duplicate_M3R_G": "eligible_higher_gauge_cost",
        "duplicate_R0": "selected_next_test",
        "twisted_parent_action": "not_passed",
        "physical_closure": False,
    },
    "next_gate": "version5_real_scalar_flip_twisted_ko6_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))