#!/usr/bin/env python3
"""Audit the local clocked-QMS continuum and time-scale boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_local_observable_clocked_qms_limit_and_time_anchor_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_local_observable_clocked_qms_limit_and_time_anchor import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    error = dict(certificate.error_theorem.proposition.data)
    joint = dict(certificate.joint_limit_theorem.proposition.data)
    reduced = dict(certificate.reduced_limit_theorem.proposition.data)
    time_boundary = dict(certificate.time_boundary_theorem.proposition.data)

    assert error["total_reduced_error"] == "epsilon_(n,d) <= C_u/n + n A exp(-c d)"
    assert joint["continuous_dimensionless_qms_recovered"] is True
    assert joint["dimension_growth"] == "O(log n)"
    assert reduced["fresh_ancilla_reset_external"] is False
    assert time_boundary["autonomous_dimensionless_time_recovered"] is True
    assert time_boundary["absolute_second_selected"] is False

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"]
        == "version8_local_observable_clocked_qms_limit_and_time_anchor_gate"
    )
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "error_decomposition": error,
        "joint_limit": joint,
        "reduced_observable_limit": reduced,
        "time_scale_boundary": time_boundary,
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