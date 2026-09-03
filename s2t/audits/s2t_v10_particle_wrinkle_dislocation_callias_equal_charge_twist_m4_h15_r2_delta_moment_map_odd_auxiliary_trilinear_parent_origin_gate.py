#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_moment_map_odd_auxiliary_trilinear_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_moment_map_odd_auxiliary_trilinear_parent_origin_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.invariant_metric_basis.rank() == 3
    assert c.normalization_constraint.rank() == 2
    assert len(c.normalization_constraint.nullspace()) == 1
    assert c.inherited_cross_block.rank() == 0
    assert c.half_cross_block == sp.Rational(1, 2) * c.hypercharge_generator
    assert c.target_cross_block == c.hypercharge_generator
    assert c.target_trace_metric.rank() == 8
    assert len(c.target_trace_metric.nullspace()) == 8

    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "moment_map_trilinear": {
            "operator": "Q=6Y",
            "spectrum": list(map(int, c.hypercharge6)),
            "operator_rank": 8,
            "canonical_direct_sum_cross_rank": 0,
            "target_cross_rank": 8,
        },
        "multiplicity_metric": {
            "general_normalized_form": "K(kappa)=[[1,kappa],[kappa,1]]",
            "symmetric_invariant_basis_rank": 3,
            "unit_diagonal_constraint_rank": 2,
            "unit_diagonal_constraint_nullity": 1,
            "free_parameter": "kappa",
            "inherited_kappa": 0,
            "target_kappa": 1,
            "half_mixing_diagonal_form": [3, 1],
            "target_diagonal_form": [4, 0],
        },
        "independence_diagnosis": {
            "inherited_trace_metric_rank_nullity": [16, 0],
            "half_mixed_trace_metric_rank_nullity": [16, 0],
            "target_trace_metric_rank_nullity": [8, 8],
            "unit_mixing_identifies_one_field_copy": True,
            "antisymmetric_mixing_is_quadratically_silent": True,
        },
        "status": {
            "conditional_target_loaded_parent": "3/5",
            "physical_inherited_parent": "3/5",
            "remaining_slots": ["coefficient_origin", "inherited_nonzero_cross_block"],
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "Delta_moment_map_fixes_Q_direction": True,
            "orthogonal_direct_sum_generates_cross_bilinear": False,
            "nondegenerate_normalized_metric_fixes_unit_cross_coefficient": False,
            "physical_parent_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_mixed_curvature_parent_origin_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()