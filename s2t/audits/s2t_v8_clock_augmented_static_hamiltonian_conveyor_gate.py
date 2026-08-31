#!/usr/bin/env python3
"""Audit the clock-augmented static history Hamiltonian conveyor gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_clock_augmented_static_hamiltonian_conveyor_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_clock_augmented_static_hamiltonian_conveyor import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    transfer = certificate.transfer_theorem.proposition.data
    execution = certificate.execution_theorem.proposition.data
    locality = certificate.locality_theorem.proposition.data
    boundary = certificate.boundary_theorem.proposition.data
    assert transfer["exact_end_to_end_transfer"] is True
    assert execution["exact_one_shot_execution"] is True
    assert execution["clock_returns_to_initial_state"] is False
    assert locality["volume_independent_fixed_time"] is False
    assert boundary["bounded_strength_fixed_time_thermodynamic_limit"] is False

    registry = verify_all()
    gate = next(item for item in registry["gates"] if item["identifier"] == "version8_clock_augmented_static_hamiltonian_conveyor_gate")
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "finite_history_clock": dict(transfer),
        "dressed_execution": dict(execution),
        "locality_scaling": dict(locality),
        "boundary": dict(boundary),
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