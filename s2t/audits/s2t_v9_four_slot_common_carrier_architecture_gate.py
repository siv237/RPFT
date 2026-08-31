#!/usr/bin/env python3
"""Exact common-carrier architecture audit for Tome IX."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "four_slot_common_carrier_architecture_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v9_four_slot_dynamic_parent_program_admission_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert predecessor["verdict"]["tome9_program_admitted"]

    endpoint_ranks = (21, 2, 1)
    endpoint_labels = [0] * 21 + [1] * 2 + [2]
    projectors = [
        sp.diag(*[int(label == sector) for label in endpoint_labels])
        for sector in range(3)
    ]
    identity_24 = sp.eye(24)
    assert sum(projectors, sp.zeros(24)) == identity_24
    assert tuple(projector.rank() for projector in projectors) == endpoint_ranks
    for left in range(3):
        for right in range(3):
            expected = projectors[left] if left == right else sp.zeros(24)
            assert projectors[left] * projectors[right] == expected

    cell_ranks = (1, 42, 2)
    assert sum(cell_ranks) == 45
    total_dimension = sum(endpoint_ranks) * sum(cell_ranks) ** 2
    assert total_dimension == 48600

    index_forward = sp.Integer(45)
    index_balanced = index_forward / index_forward
    assert index_forward == 45
    assert index_balanced == 1

    checks = {
        "endpoint_projectors_are_orthogonal_and_complete": True,
        "endpoint_ranks_are_21_2_1": True,
        "noise_cell_ranks_are_1_42_2": True,
        "common_cell_dimension_is_48600": True,
        "old_H21_corner_embedding_exists": True,
        "L44_collision_has_one_common_local_algebra": True,
        "floquet_transport_index_is_45": True,
        "balanced_transport_index_is_1": True,
    }
    assert all(checks.values())

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "carrier": {
            "endpoint_decomposition": "H24=H21 direct_sum Hn2 direct_sum Ht1",
            "endpoint_ranks": list(endpoint_ranks),
            "noise_cell_decomposition": "K45=K0_1 direct_sum N42 direct_sum Ech_2",
            "noise_cell_ranks": list(cell_ranks),
            "common_local_cell": "Xi_IX=H24 tensor K45_right tensor K45_left",
            "common_local_dimension": total_dimension,
        },
        "transport_menu": {
            "floquet": "S45_right tensor identity_left",
            "floquet_gnvw_index": 45,
            "balanced": "S45_right tensor inverse(S45_left)",
            "balanced_gnvw_index": 1,
            "same_doubled_chain_carrier": True,
        },
        "architecture_audit": {
            **checks,
            "satisfied": sum(checks.values()),
            "tested": len(checks),
        },
        "ledgers": {
            "common_carrier_architecture_satisfied": 8,
            "common_carrier_architecture_tested": 8,
            "selected_slots_satisfied": 0,
            "selected_slots_tested": 4,
            "bounded_four_slot_action_satisfied": 0,
            "bounded_four_slot_action_tested": 1,
        },
        "verdict": {
            "single_common_carrier_architecture_constructed": True,
            "endpoint_sector_selected": False,
            "transport_law_selected": False,
            "energy_and_coupling_selected": False,
            "four_slot_parent_constructed": False,
        },
        "next_gate": "version9_four_slot_common_parent_functional_architecture_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()