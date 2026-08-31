#!/usr/bin/env python3
"""Typed exact audit of existing candidates for the baryon spectral scale."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_spectral_scale_anchor_candidate_audit_gate_results.json"
INPUTS = [
    ROOT / "s2t/results/s2t_v8_clock_energy_anchor_candidate_audit_gate_results.json",
    ROOT / "s2t/results/s2t_v8_full_noise_physical_time_scale_no_go_gate_results.json",
    ROOT / "s2t/results/s2t_v8_full_field_a4_dirac_lift_origin_gate_results.json",
    ROOT / "s2t/results/s2t_v8_gauge_invariant_vacuum_hessian_reconstruction_gate_results.json",
]

def main() -> None:
    data = [json.loads(p.read_text(encoding="utf-8")) for p in INPUTS]
    assert data[0]["typed_clock_energy_anchor_found"] is False
    assert data[1]["verdict"]["absolute_second_is_fixed"] is False
    assert data[2]["verdict"]["external_metric_scale_selected"] is False
    assert data[3]["verdict"]["unconditional_physical_B_derived"] is False
    candidates = {
        "base_dirac_scale": (-2, False, True, False),
        "clock_energy_squared": (-2, False, False, False),
        "noise_rate_squared": (-2, False, False, False),
        "vacuum_hessian_gap": (0, True, False, False),
        "cutoff_or_inverse_radius_squared": (-2, False, False, False),
        "observed_baryon_mass_squared": (-2, False, True, True),
    }
    # tuple = (length weight, internally selected, typed map to kernel, breaks orbit)
    passes = {k: (v[0] == -2 and v[1] and v[2] and v[3]) for k, v in candidates.items()}
    assert sum(passes.values()) == 0
    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_spectral_scale_anchor_candidate_audit_gate",
        "target": {"quantity": "mass_sq", "length_scaling_weight": -2},
        "contract": ["correct_weight", "internally_selected", "typed_kernel_map", "breaks_scale_orbit"],
        "candidates": {
            k: {"length_weight": v[0], "internally_selected": v[1], "typed_kernel_map": v[2], "breaks_scale_orbit": v[3], "passes": passes[k]}
            for k, v in candidates.items()
        },
        "passing_candidates": 0,
        "input_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in INPUTS},
        "verdict": {"internal_spectral_scale_anchor_found": False, "observed_mass_is_target_loaded": True, "new_typed_base_scale_selector_required": True},
        "next_gate": "version8_baryon_spectral_scale_anchor_minimal_new_data_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())

if __name__ == "__main__": main()