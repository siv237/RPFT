#!/usr/bin/env python3
"""Audit the absolute-time scale orbit of the full collision model."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_full_noise_physical_time_scale_no_go_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_full_noise_physical_time_scale import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    data = certificate.physical_time_no_go_theorem.proposition.data
    assert data["absolute_seconds_selected"] is False
    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"] == "version8_full_noise_physical_time_scale_no_go_gate"
    )
    assert len(gate["obligations"]) == 6
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "exact_scale_orbit": {
            "interaction": "H_int -> g H_int",
            "generator": "L_42 -> g^2 L_42",
            "time_compensation": "t_phys -> t_phys/g^2",
            "invariant": "g^2 t_phys",
            "residual": "0",
        },
        "calibration": {
            "generic_unit": "t_* = hbar/E_*",
            "hbar_alone_is_sufficient": False,
            "independent_energy_or_rate_anchor_required": True,
            "collision_schedule_required": True,
            "existing_dimensionless_trace_normalization_is_physical_clock": False,
        },
        "verdict": {
            "dimensionless_flow_is_fixed": True,
            "absolute_second_is_fixed": False,
            "older_mass_or_cutoff_may_be_imported_without_typed_bridge": False,
            "next_gate": "typed_energy_rate_anchor_to_full_noise_generator_gate",
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