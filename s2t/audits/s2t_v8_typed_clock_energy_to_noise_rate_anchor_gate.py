#!/usr/bin/env python3
"""Audit the typed clock-energy to full-noise-rate bridge."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_typed_clock_energy_to_noise_rate_anchor_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_typed_clock_energy_to_noise_rate_anchor import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    identity = dict(certificate.rate_identity_theorem.proposition.data)
    calibration = dict(certificate.relative_calibration_theorem.proposition.data)
    freedom = dict(certificate.underdetermination_theorem.proposition.data)
    boundary = dict(certificate.anchor_no_go_theorem.proposition.data)
    assert identity["relative_rate"] == "Gamma/Omega=chi^2"
    assert calibration["relative_calibration_obtained_conditionally"] is True
    assert freedom["current_parent_selects_chi"] is False
    assert boundary["clock_energy_E_C_derived"] is False
    assert boundary["absolute_rate_Gamma_derived"] is False

    registry = verify_all()
    gate = next(item for item in registry["gates"] if item["identifier"] == "version8_typed_clock_energy_to_noise_rate_anchor_gate")
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "typed_rate_identity": identity,
        "relative_calibration": calibration,
        "coupling_freedom": freedom,
        "anchor_boundary": boundary,
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