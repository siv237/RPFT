#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_output_density_morphism_origin_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.completeness == sp.eye(2)
    assert certificate.stationary_state == certificate.kms_state
    assert certificate.fluxes == sp.ImmutableMatrix([sp.Rational(1, 18), sp.Rational(1, 18)])
    assert certificate.net_flux == 0
    assert certificate.excited_output[0, 0] == sp.Rational(1, 6)
    assert certificate.parent_hessian.rank() == 3
    assert certificate.scale_map.rank() == 3

    result = {
        "date": "2026-09-02",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "canonical_KMS_channel": {
            "downward_probability": "p_down=1/6",
            "upward_probability": "p_up=1/12",
            "KMS_ratio": "p_up/p_down=1/2=exp(-log(2))",
            "Kraus_complete": True,
            "completely_positive_trace_preserving": True,
            "population_transition": [["11/12", "1/6"], ["1/12", "5/6"]],
        },
        "equilibrium": {
            "Gibbs_state": "diag(2/3,1/3)",
            "stationary": True,
            "downward_flux": "1/18",
            "upward_flux": "1/18",
            "net_flux": "0",
        },
        "spectral_match": {
            "excited_state_loss": "1/6",
            "matches_R_out_witness": True,
            "population_contraction_eigenvalue": "3/4",
        },
        "zero_temperature_boundary": {
            "upward_probability": "0",
            "downward_probability": "1/6",
            "stationary_state": "vacuum diag(1,0)",
            "faithful_finite_KMS_state": False,
        },
        "status": {
            "architecture": "10/10",
            "conditional_origin": "8/8",
            "canonical_CPTP_KMS_channel": "1/1",
            "sustained_stationary_throughflow": "0/1",
            "nonequilibrium_drive_and_bath_origin": "0/2",
            "absolute_scale": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "canonical_KMS_channel_exists": True,
            "one_sixth_loss_is_channel_realizable": True,
            "finite_KMS_detailed_balance_supports_net_outflow": False,
            "nonequilibrium_reservoir_required": True,
            "absolute_breathing_scale_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_nonequilibrium_two_reservoir_output_current_parent_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()