#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_cell_birth_front_speed_morphism_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_cell_birth_front_speed_morphism_origin_gate_results.json"
PREDECESSOR = "version10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_vacuum_growth_common_parent_origin_gate"


def main() -> None:
    verification = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": PREDECESSOR,
        "kinematics": {
            "bath_group_speed_over_c": "121*k_X/24",
            "local_growth_speed_over_c": "k_X/3",
            "front_speed_over_c": "rho*k_X/3",
            "front_to_bath_speed": "8*rho/121",
            "rho": "R/ell_cell",
        },
        "crossing": {
            "rho_star": "121/8",
            "bath_reach_over_cell_length": "121/8",
            "history_transfer": "8*rho_0*exp(zeta)/121",
            "global_identity": False,
            "single_shell_identity": True,
        },
        "linear_audit": {
            "scale_rank_nullity": "2/2",
            "scale_kernels": [[1, 0], [1, 0], [0, 1], [1, 1]],
            "radius_anchored_rank_nullity": "3/1",
            "parent_rank_nullity": "2/1",
            "anchored_parent_rank": 3,
            "anchored_parent_determinant": 1,
        },
        "status": {
            "architecture": "10/10",
            "conditional_origin": "8/8",
            "typed_front_morphism": "1/1",
            "universal_speed_identity": "0/1",
            "microscopic_causal_identity": "0/1",
            "absolute_scale": "0/1",
        },
        "verdict": {
            "radius_dependent_morphism_exists": True,
            "bath_speed_equals_front_speed_for_all_history": False,
            "front_speed_is_automatically_a_signal_speed": False,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verification.obligations),
            "obligations": [name for name, _ in verification.obligations],
            "certificate_sha256": verification.sha256,
            "floating_point_values": 0,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_front_speed_causal_recession_separation_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verification.sha256)


if __name__ == "__main__":
    main()