#!/usr/bin/env python3
"""Audit the bounded-strength autonomous-clock thermodynamic boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_bounded_strength_autonomous_clock_thermodynamic_limit_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_bounded_strength_autonomous_clock_thermodynamic_limit import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    finite_volume = dict(certificate.finite_volume_theorem.proposition.data)
    resource = dict(certificate.resource_schedule_theorem.proposition.data)
    global_boundary = dict(certificate.global_boundary_theorem.proposition.data)
    local_limit = dict(certificate.local_limit_theorem.proposition.data)

    assert finite_volume["finite_volume_arbitrary_accuracy"] is True
    assert finite_volume["exact_finite_clock_control_derived"] is False
    assert resource["dimension_independent_of_volume"] is False
    assert global_boundary["universal_autonomous_clock_no_go"] is False
    assert local_limit["local_thermodynamic_approximation_admitted"] is True
    assert local_limit["absolute_tick_duration_derived"] is False

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"]
        == "version8_bounded_strength_autonomous_clock_thermodynamic_limit_gate"
    )
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "finite_volume": finite_volume,
        "resource_schedule": resource,
        "global_boundary": global_boundary,
        "local_observable_limit": local_limit,
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