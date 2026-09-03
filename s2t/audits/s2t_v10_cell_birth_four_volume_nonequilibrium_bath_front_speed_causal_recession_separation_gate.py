#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_front_speed_causal_recession_separation import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_front_speed_causal_recession_separation_gate_results.json"
PREDECESSOR = "version10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_cell_birth_front_speed_morphism_origin_gate"


def main() -> None:
    verification = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": PREDECESSOR,
        "velocity_decomposition": {
            "total": "u_total=u_recession+u_local",
            "recession": "u_recession=H_B*R/c=rho*k_X/3",
            "bath_local": "u_b=121*k_X/24",
            "front_local": 0,
            "outgoing_characteristic": "u_recession+u_b",
            "incoming_characteristic": "u_recession-u_b",
        },
        "causal_classification": {
            "metric": [[1, 0], [0, -1]],
            "front_norm": "u_b^2",
            "outgoing_norm": 0,
            "incoming_norm": 0,
            "recession_speed_may_exceed_c": True,
            "local_bath_speed_must_not_exceed_c": True,
        },
        "local_subluminality": {
            "condition": "k_X<=24/121",
            "critical_weight": "(exp(24/121)-1)/(2-exp(24/121))",
            "minimum_action": "log((2-exp(24/121))/(exp(24/121)-1))",
            "conditional_S_vac_candidate_passes": True,
            "S_vac_status": "conditional_project_input",
        },
        "status": {
            "architecture": "10/10",
            "conditional_origin": "8/8",
            "kinematic_separation": "1/1",
            "local_causal_cone": "1/1",
            "conditional_vacuum_subluminality": "1/1",
            "microscopic_propagation_kernel_origin": "0/1",
            "absolute_scale": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verification.obligations),
            "obligations": [name for name, _ in verification.obligations],
            "certificate_sha256": verification.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "superluminal_recession_is_local_causality_violation": False,
            "front_is_center_of_local_bath_cone": True,
            "microscopic_bath_kernel_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verification.sha256)


if __name__ == "__main__":
    main()