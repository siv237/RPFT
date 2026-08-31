#!/usr/bin/env python3
"""Audit the exact two-chain index-balanced ancilla conveyor."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_index_balanced_ancilla_conveyor_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_index_balanced_ancilla_conveyor import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.cell_dimension == 43
    assert certificate.total_index == 1
    circuit = certificate.swap_circuit_theorem.proposition.data
    assert circuit["circuit_depth"] == 2
    assert circuit["exact_counterpropagating_shifts"] is True
    recovery = certificate.recovery_theorem.proposition.data
    assert recovery["active_chain_supplies_fresh_vacuum"] is True
    assert recovery["valid_steps"] == "all finite n >= 0"
    boundary = certificate.autonomy_boundary_theorem.proposition.data
    assert boundary["exact_piecewise_local_hamiltonian"] is True
    assert boundary["single_static_local_hamiltonian_derived"] is False

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"] == "version8_index_balanced_ancilla_conveyor_gate"
    )
    assert len(gate["obligations"]) == 5
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "carrier": {
            "active_chain_cell_dimension": 43,
            "spectator_chain_cell_dimension": 43,
            "active_shift_index": 43,
            "spectator_shift_index": "1/43",
            "total_gnvw_index": 1,
        },
        "swap_circuit": {
            "depth": 2,
            "layer_0": "product_m SWAP(A_m,B_m)",
            "layer_1": "product_m SWAP(B_m,A_(m+1))",
            "active_result": "A_m(final)=A_(m-1)(initial)",
            "spectator_result": "B_m(final)=B_(m+1)(initial)",
            "nearest_neighbour": True,
            "gauge_covariant": True,
            "real_covariant": True,
        },
        "hamiltonian": {
            "local_term": "(pi/2)(I-SWAP)",
            "two_piece_local_generation": True,
            "single_static_local_generation": False,
            "absolute_stage_duration_derived": False,
        },
        "recovery": {
            "fresh_active_vacuum_each_step": True,
            "spectator_couples_to_system": False,
            "reduced_iteration": "Phi_h^n for all finite n>=0",
            "residual": "0",
        },
        "verdict": {
            "gnvw_obstruction_removed": True,
            "exact_local_floquet_conveyor": True,
            "single_time_independent_hamiltonian": False,
            "strong_stationary_autonomy": False,
            "next_gate": "version8_static_local_hamiltonian_embedding_or_no_go_gate",
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()