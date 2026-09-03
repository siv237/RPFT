#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_shared_fixed_point_auxiliary_channel_typed_embedding import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_shared_fixed_point_auxiliary_channel_typed_embedding_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_stabilizer_moment_map_curvature_parent_origin_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.fixed_point_weights.rows == 36
    assert c.weight_match_matrix == sp.zeros(36, 8)
    assert c.intertwiner_constraint.rank() == 288
    assert c.untyped_injection.rank() == 8
    assert c.untyped_metric_pullback == sp.eye(8)
    assert c.untyped_equivariance_residual.rank() == 8
    assert c.grading_constraint.rank() == 288
    assert c.extension_equivariance_residual == sp.zeros(8)
    assert c.extension_grading_residual == sp.zeros(8)
    assert c.extension_reality_residual == sp.zeros(8)
    assert c.conditional_schur_complement == sp.diag(40, 40, 0, 48, 48, 0, 40, 40)

    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "weight_audit": {
            "Sigma_weights_6Y": list(map(int, c.sigma_weights)),
            "fixed_point_auxiliary_weight_multiplicities": {
                "-6": 1, "-4": 6, "0": 22, "4": 6, "6": 1,
            },
            "Sigma_weight_multiplicities": {
                "-7": 1, "-3": 2, "-1": 1, "1": 1, "3": 2, "7": 1,
            },
            "common_weight_count": 0,
            "equivariant_Hom_dimension": 0,
            "intertwiner_constraint_rank": 288,
        },
        "typed_embedding": {
            "ambient_fixed_point_dimension": 36,
            "untyped_isometric_embedding_rank": 8,
            "untyped_equivariance_residual_rank": 8,
            "fixed_point_grading": "even",
            "required_auxiliary_grading": "odd",
            "graded_Hom_dimension": 0,
            "inherited_typed_embedding_rank": 0,
        },
        "minimal_conditional_extension": {
            "new_odd_auxiliary_real_dimension": 8,
            "weights_6Y": list(map(int, c.extension_weights)),
            "hypercharge_equivariant": True,
            "grading_compatible": True,
            "reality_compatible": True,
            "trace_isometric": True,
            "full_parent_rank_nullity": [14, 2],
            "Schur_complement_diagonal": list(map(int, c.conditional_schur_complement.diagonal())),
            "inherited": False,
        },
        "status": {
            "inherited_fixed_point_channel": "2/4",
            "conditional_odd_extension": "4/4",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "untyped_dimension_embedding_exists": True,
            "fixed_point_hypercharge_equivariant_embedding_exists": False,
            "fixed_point_graded_embedding_exists": False,
            "minimal_odd_extension_conditionally_succeeds": True,
            "physical_shared_auxiliary_channel_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_minimal_odd_auxiliary_bimodule_candidate_audit_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()