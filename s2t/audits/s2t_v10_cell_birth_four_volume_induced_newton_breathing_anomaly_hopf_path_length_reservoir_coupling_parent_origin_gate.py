#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_path_length_reservoir_coupling_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_path_length_reservoir_coupling_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_common_affinity_temperature_anchor_candidate_audit_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.assignment_scores == sp.Matrix([0, 8])
    assert certificate.conditional_hessian.rank() == 2
    assert certificate.inherited_mixed_block == sp.zeros(2)
    assert certificate.temperature_map.rank() == 2
    assert certificate.temperature_map * certificate.temperature_kernel == sp.zeros(2, 1)

    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "path_length_operator": [[1, 0], [0, 2]],
        "oriented_assignments": {
            "aligned_hot_one_cold_two": {
                "intertwiner": [[1, 0], [0, 1]],
                "defect": [[0, 0], [0, 0]],
                "score": 0,
                "affinities": ["log(2)", "2*log(2)"],
                "affinity_difference": "log(2)",
            },
            "swapped_hot_two_cold_one": {
                "intertwiner": [[0, 1], [1, 0]],
                "defect": [[-2, 0], [0, 2]],
                "score": 8,
                "affinity_difference": "-log(2)",
            },
        },
        "kms_ratios": ["1/2", "1/4"],
        "conditional_parent": {
            "hessian": [[1, 0], [0, 1]],
            "rank": 2,
            "determinant": 1,
            "assignment_unique_given_signed_affinity_difference": True,
        },
        "inherited_parent": {
            "reservoir_path_mixed_block": [[0, 0], [0, 0]],
            "coupling_origin": "0/1",
        },
        "temperature_scale_orbit": {
            "rank_nullity": "2/1",
            "kernel": [-1, -1, 1],
            "physical_temperature_origin": "0/1",
        },
        "status": {
            "conditional_architecture": "4/4",
            "typed_path_assignment_given_coupling": "1/1",
            "inherited_reservoir_path_coupling_origin": "0/1",
            "physical_temperature_origin": "0/1",
            "origin_ledger": "4/6",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "signed_affinity_difference_selects_hot_one_cold_two": True,
            "current_parent_generates_assignment_intertwiner": False,
            "dimensionless_assignment_fixes_physical_temperature": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()