#!/usr/bin/env python3
"""Audit internal candidates for the autonomous-clock energy anchor."""

from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_clock_energy_anchor_candidate_audit_gate_results.json"


def main() -> None:
    candidates = {
        "spectral_cutoff": "profile_cutoff_scale_orbit",
        "compactification_radius": "physical_length_not_derived",
        "qms_gap": "dimensionless_and_rate_rescalable",
        "vacuum_parent_gap": "positive_coefficient_rescalable",
        "compacton_energy": "only_E_times_L_fixed",
        "observed_masses": "external_or_train_without_typed_clock_map",
    }
    assert len(candidates) == 6
    result = {
        "date": "2026-08-30",
        "gate": "version8_clock_energy_anchor_candidate_audit_gate",
        "candidates": candidates,
        "typed_clock_energy_anchor_found": False,
        "dimensionless_coupling_chi_selected": False,
        "conditional_rate_formula": "Gamma=chi^2 E_C/hbar",
        "next_gate": "version8_minimal_mixed_clock_collision_parent_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()