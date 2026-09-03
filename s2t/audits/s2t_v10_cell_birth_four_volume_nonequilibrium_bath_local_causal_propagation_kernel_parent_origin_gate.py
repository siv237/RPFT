#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_spectral_density_memory_scale_candidate_audit_gate",
        "local_kernel": {
            "graph": "seven-site nearest-neighbour path witness",
            "step_operator": "A_ij=1/2 for |i-j|=1",
            "causal_support_rule": "(A^n)_ij=0 when graph_distance(i,j)>n",
            "checked_steps": [1, 2, 3],
            "causal_defects": 0,
        },
        "geometric_memory": {
            "kernel": "K_n(r)=r^n A^n",
            "hot_r": "1/2",
            "cold_r": "1/4",
            "hot_memory_steps": 2,
            "cold_memory_steps": "4/3",
            "Toeplitz_covariance_determinants": ["9/16", "225/256"],
        },
        "parent": {
            "residuals": ["k1-r", "k2-r*k1", "k3-r*k2"],
            "rank_nullity": "3/1",
            "kernel_tangent_at_r_half": ["1", "1", "3/4", "1"],
            "determinant": 0,
        },
        "scale_audit": {
            "rank_nullity": "2/2",
            "kernel": [[int(value) for value in row] for row in certificate.scale_kernel.tolist()],
            "after_step_time_anchor": "3/1",
            "after_step_time_and_length_anchors": "4/0",
        },
        "status": {
            "conditional_local_causal_architecture": "8/8",
            "causal_support": "3/3",
            "damping_parameter_origin": "0/1",
            "absolute_time_origin": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "locality_derives_a_finite_graph_light_cone": True,
            "locality_derives_geometric_memory_family": True,
            "locality_selects_decay_parameter": False,
            "KMS_ratio_is_typed_as_decay_parameter": False,
            "absolute_memory_time_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()