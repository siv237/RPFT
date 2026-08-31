#!/usr/bin/env python3
"""Classify gauge-equivariant maps from the full arrow module to endpoints."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_physical_arrow_endpoint_intertwiner_classification_gate_results.json"

REPS = {
    "Q_L": ("3", 2, Fraction(1, 6)),
    "L_L": ("1", 2, Fraction(-1, 2)),
    "u_R": ("3", 1, Fraction(2, 3)),
    "d_R": ("3", 1, Fraction(-1, 3)),
    "e_R": ("1", 1, Fraction(-1, 1)),
    "X_L": ("1", 1, Fraction(-1, 1)),
    "X_R": ("1", 1, Fraction(-1, 1)),
    "Y_L": ("1", 2, Fraction(-1, 2)),
    "Y_R": ("1", 2, Fraction(-1, 2)),
}

LEFT = {"Q_L", "L_L", "X_L", "Y_L"}


def dual(rep):
    color, weak, hypercharge = rep
    return ({"3": "3bar", "3bar": "3"}.get(color, color), weak, -hypercharge)


def tensor_color(first, second):
    if first == "1":
        return [second]
    if second == "1":
        return [first]
    if {first, second} == {"3", "3bar"}:
        return ["1", "8"]
    if first == second == "3":
        return ["6", "3bar"]
    if first == second == "3bar":
        return ["6bar", "3"]
    raise ValueError((first, second))


def tensor_weak(first, second):
    if first == 1:
        return [second]
    if second == 1:
        return [first]
    if first == second == 2:
        return [1, 3]
    raise ValueError((first, second))


def hom_rep(source, target):
    target_rep = REPS[target]
    source_dual = dual(REPS[source])
    return [
        (color, weak, target_rep[2] + source_dual[2])
        for color in tensor_color(target_rep[0], source_dual[0])
        for weak in tensor_weak(target_rep[1], source_dual[1])
    ]


def endpoint_multiplicities():
    return Counter(REPS.values())


def intertwiner_dimension(arrow_reps, endpoint):
    arrow = Counter(arrow_reps)
    return sum(multiplicity * endpoint.get(rep, 0) for rep, multiplicity in arrow.items())


def main():
    data = json.loads((ROOT / "s2t/results/s2t_v7_rooted_cycle_isotypic_edge_projector_gate_results.json").read_text(encoding="utf-8"))
    ordered = data["edge_space"]["ordered_new_edges"]
    selected = set(data["projector_union"]["selected_support"])
    endpoint = endpoint_multiplicities()

    rows = []
    oriented_all = []
    reverse_all = []
    selected_oriented = []
    selected_reverse = []
    unwanted_oriented = []
    unwanted_reverse = []
    for label in ordered:
        first, second = label.split("--")
        source, target = (first, second) if first in LEFT else (second, first)
        forward = hom_rep(source, target)
        reverse = [dual(rep) for rep in forward]
        is_selected = label in selected
        oriented_all.extend(forward)
        reverse_all.extend(reverse)
        (selected_oriented if is_selected else unwanted_oriented).extend(forward)
        (selected_reverse if is_selected else unwanted_reverse).extend(reverse)
        rows.append({
            "edge": label,
            "orientation": f"{source}->{target}",
            "selected": is_selected,
            "forward_endpoint_intertwiner_dimension": intertwiner_dimension(forward, endpoint),
            "reverse_endpoint_intertwiner_dimension": intertwiner_dimension(reverse, endpoint),
        })

    oriented_dimension = intertwiner_dimension(oriented_all, endpoint)
    real_dimension = intertwiner_dimension(oriented_all + reverse_all, endpoint)
    selected_oriented_dimension = intertwiner_dimension(selected_oriented, endpoint)
    selected_real_dimension = intertwiner_dimension(selected_oriented + selected_reverse, endpoint)
    unwanted_oriented_dimension = intertwiner_dimension(unwanted_oriented, endpoint)
    unwanted_real_dimension = intertwiner_dimension(unwanted_oriented + unwanted_reverse, endpoint)

    selected_nonzero = [row for row in rows if row["selected"] and (
        row["forward_endpoint_intertwiner_dimension"] or row["reverse_endpoint_intertwiner_dimension"]
    )]
    assert oriented_dimension == 10
    assert real_dimension == 14
    assert selected_oriented_dimension == 0
    assert selected_real_dimension == 1
    assert unwanted_oriented_dimension == 10
    assert unwanted_real_dimension == 13
    assert len(selected_nonzero) == 1
    assert selected_nonzero[0]["edge"] == "Q_L--Y_R"
    assert selected_nonzero[0]["reverse_endpoint_intertwiner_dimension"] == 1

    result = {
        "gate": "version8_physical_arrow_endpoint_intertwiner_classification_gate",
        "representation_input": {
            "gauge_group": "SU(3)xSU(2)xU(1) representation labels",
            "endpoint_irrep_multiplicities": {str(key): value for key, value in endpoint.items()},
            "arrow_orientation": "physical left vertex -> physical right vertex",
            "real_completion_adds_reverse_conjugate_arrows": True,
        },
        "edge_classification": rows,
        "intertwiner_dimensions": {
            "oriented_full_arrow_to_endpoint": oriented_dimension,
            "real_doubled_full_arrow_to_endpoint": real_dimension,
            "oriented_selected_hodge_support_to_endpoint": selected_oriented_dimension,
            "real_doubled_selected_hodge_support_to_endpoint": selected_real_dimension,
            "oriented_unwanted_support_to_endpoint": unwanted_oriented_dimension,
            "real_doubled_unwanted_support_to_endpoint": unwanted_real_dimension,
        },
        "unique_selected_channel": {
            "edge": "Q_L--Y_R",
            "orientation": "reverse Real partner Y_R->Q_L",
            "representation_component": "(3,1,2/3)",
            "endpoint_block": "u_R",
            "complex_multiplicity": 1,
            "maximum_operator_rank": 3,
            "full_rank_between_hodge_and_endpoint_carriers": False,
        },
        "verdict": {
            "identity_by_dimension_rejected": True,
            "full_equivariant_connector_unique": False,
            "selected_oriented_connector_exists": False,
            "selected_real_connector_unique_up_to_scale": True,
            "unique_channel_is_full_carrier_isomorphism": False,
            "unique_channel_deserves_lift_test": True,
            "new_tome_admitted": False,
            "status": "unique_rank_three_real_selected_channel_full_connector_open",
            "next_gate": "version8_qlyr_ur_real_connector_lift_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()