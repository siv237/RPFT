#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_common_carrier_admission import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_common_carrier_admission_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_candidate_audit_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.reservoir_projector.rank() == 2
    assert certificate.path_projector.rank() == 2
    assert certificate.intertwiner.T * certificate.intertwiner == certificate.path_projector
    assert certificate.intertwiner * certificate.intertwiner.T == certificate.reservoir_projector
    assert certificate.algebra_basis.rank() == 16
    assert certificate.commutant_constraint.rank() == 15
    assert certificate.conditional_hessian.rank() == 4

    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "common_carrier": {
            "space": "C2_reservoir_direct_sum_C2_path",
            "complex_dimension": 4,
            "minimal_dimension": 4,
            "sector_projector_ranks": [2, 2],
            "generated_algebra": "M4(C)",
            "generated_algebra_dimension": 16,
            "commutant_dimension": 1,
        },
        "intertwiner": {
            "type": "rank_two_partial_isometry_path_to_reservoir",
            "initial_projector": "P_path",
            "final_projector": "P_reservoir",
            "nilpotent": True,
            "orientation_preserving": True,
            "real_sign_phase_choices": 4,
        },
        "conditional_parent": {
            "mixed_block_rank": 2,
            "hessian_rank": 4,
            "hessian_determinant": "9/16",
            "hessian_spectrum": {"1/2": 2, "3/2": 2},
        },
        "status": {
            "conditional_architecture": "12/12",
            "inherited_sector_data": "4/4",
            "common_carrier_and_cross_generator_origin": "0/2",
            "intertwiner_phase_origin": "0/1",
            "coupling_coefficient_origin": "0/1",
            "physical_temperature_origin": "0/1",
            "strict_physical_origin": "0/4",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "minimal_common_carrier_exists": True,
            "cross_intertwiner_is_architecturally_admissible": True,
            "current_parent_generates_M4_cross_operator": False,
            "common_carrier_selects_intertwiner_phase": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_m4_cross_generator_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()