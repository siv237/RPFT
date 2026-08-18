#!/usr/bin/env python3
"""Bound and enumerate the Version V finite-geometry graph search."""

import json
from math import comb
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_finite_geometry_complexity_bound_gate_results.json"

graphs_by_n = {}
for n in (3, 4, 5):
    graphs = [
        graph
        for graph in nx.graph_atlas_g()
        if len(graph) == n and nx.is_connected(graph) and nx.is_bipartite(graph)
    ]
    graphs_by_n[n] = [
        {
            "vertices": n,
            "edges": graph.number_of_edges(),
            "degree_sequence": sorted(dict(graph.degree()).values(), reverse=True),
            "cycle_rank": graph.number_of_edges() - n + 1,
            "graph6": nx.to_graph6_bytes(graph, header=False).strip().decode(),
        }
        for graph in graphs
    ]

assert [len(graphs_by_n[n]) for n in (3, 4, 5)] == [1, 3, 5]
survivors = [g for g in graphs_by_n[5] if g["cycle_rank"] == 1]
assert len(survivors) == 1
assert survivors[0]["degree_sequence"] == [3, 2, 2, 2, 1]

raw_algebra_multisets = sum(comb(12 + s - 1, s) for s in range(1, 6))
assert raw_algebra_multisets == 6187

result = {
    "date": "2026-08-15",
    "gate": "version5_finite_geometry_complexity_bound_gate",
    "budget": {
        "max_summands": 5,
        "matrix_size_max": 4,
        "max_particle_nodes": 5,
        "max_edges": 6,
        "max_hilbert_dimension": 64,
        "max_cycle_rank": 1,
        "raw_algebra_multisets": raw_algebra_multisets,
    },
    "graph_counts": {str(n): len(graphs_by_n[n]) for n in (3, 4, 5)},
    "graphs": {str(n): graphs_by_n[n] for n in (3, 4, 5)},
    "provisional_survivor": {
        **survivors[0],
        "name": "K_2,3 minus one edge; C4 with pendant leaf",
    },
    "selector_algebra_menu": ["M3(R)", "M3(C)"],
    "verdict": {
        "finite_budget": True,
        "graph_enumeration": True,
        "unique_graph_only_survivor": True,
        "selector_function": "open_until_blockwise_first_order_test",
        "finite_geometry_exists": False,
        "physical_closure": False,
    },
    "next_gate": "version5_real_selector_leaf_ko6_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))