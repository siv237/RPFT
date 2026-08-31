#!/usr/bin/env python3
"""Audit the vacuum parent and the information-flow obstruction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_vacuum_chain_parent_state_and_local_hamiltonian_origin_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_vacuum_chain_parent_state_and_local_hamiltonian_origin import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    parent = certificate.parent_theorem.proposition.data
    no_go = certificate.local_hamiltonian_no_go_theorem.proposition.data
    assert certificate.cell_dimension == 43
    assert certificate.excitation_dimension == 42
    assert parent["finite_volume_ground_dimension"] == 1
    assert parent["finite_volume_gap"] == 1
    assert certificate.shift_index_theorem.proposition.data["multiplicative_index"] == 43
    assert certificate.global_index_theorem.proposition.data[
        "global_step_multiplicative_index"
    ] == 43
    assert no_go["exact_local_hamiltonian_generator_exists"] is False

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"]
        == "version8_vacuum_chain_parent_state_and_local_hamiltonian_origin_gate"
    )
    assert len(gate["obligations"]) == 4
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "vacuum_parent": {
            "local_term": "h_m=I-|0><0|_m",
            "cell_dimension": 43,
            "excitation_dimension": 42,
            "commuting_projectors": True,
            "frustration_free": True,
            "finite_volume_ground_dimension": 1,
            "finite_volume_gap": 1,
            "product_vacuum_parent_derived": True,
        },
        "information_flow": {
            "shift_multiplicative_gnvw_index": 43,
            "localized_collision_index": 1,
            "global_floquet_step_index": 43,
            "local_hamiltonian_path_index": 1,
            "index_mismatch": "43 != 1",
        },
        "verdict": {
            "preloaded_vacuum_has_local_parent": True,
            "exact_shift_has_local_hamiltonian_origin": False,
            "time_independent_local_hamiltonian_origin": False,
            "even_time_dependent_lieb_robinson_origin": False,
            "strong_self_generated_reservoir": False,
            "current_floquet_construction_remains_valid": True,
            "next_gate": "version8_index_balanced_ancilla_conveyor_gate",
        },
        "literature": {
            "gnvw": "arXiv:0910.3675",
            "alpu_converse_lieb_robinson": "arXiv:2012.00741",
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