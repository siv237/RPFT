#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_correlation_time_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_correlation_time_parent_origin_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_microscopic_carrier_cutoff_parent_admission_gate",
        "correlation_profiles": {
            "exponential": {"C_of_x": "exp(-x)", "tau_corr_times_omega_UV": "1", "slope_at_zero": "-1"},
            "gaussian": {"C_of_x": "exp(-x^2)", "tau_corr_times_omega_UV": "sqrt(pi)/2", "slope_at_zero": "0"},
            "mixture": {
                "C_of_x": "a exp(-x)+(1-a) exp(-x^2)",
                "tau_corr_times_omega_UV": "a+(1-a)sqrt(pi)/2",
                "slope_at_zero": "-a",
                "free_shape_parameter": True,
            },
        },
        "conditional_exponential_parent": {"minimum": 1, "hessian": [[1]], "determinant": 1},
        "scale_audit": {
            "map": [[int(value) for value in row] for row in certificate.scale_map.tolist()],
            "rank_nullity": "2/2",
            "kernel": [[int(value) for value in row] for row in certificate.scale_kernel.tolist()],
            "after_velocity_anchor": "3/1",
            "after_velocity_and_length_anchors": "4/0",
        },
        "status": {
            "conditional_time_architecture": "8/8",
            "profile_nonuniqueness_witness": "3/3",
            "spectral_shape_origin": "0/1",
            "absolute_correlation_time_origin": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "inverse_cutoff_supplies_a_time_unit": True,
            "cutoff_uniquely_selects_bath_correlation_time": False,
            "spectral_profile_is_required": True,
            "absolute_time_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_spectral_density_memory_scale_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()