#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_curvature_trace_selector_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_curvature_trace_selector_candidate_audit_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_mixed_curvature_parent_origin_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.endpoint_channel_map.rank() == 2
    assert c.endpoint_channel_map * c.unique_trace_weights == c.target_generator
    assert c.unique_trace_weights == sp.ImmutableMatrix([1, -1])
    assert c.relative_projector**2 == c.relative_projector
    assert c.relative_projector.rank() == 1
    assert c.inherited_relative_selector.rank() == 0
    assert c.candidate_matrix.shape == (12, 6)
    assert c.candidate_matrix.rank() == 6
    assert c.pass_vector == sp.zeros(12, 1)

    names = [
        "ordinary_Hilbert_Schmidt_trace",
        "raw_supertrace",
        "positive_left_chiral_trace",
        "positive_right_chiral_trace",
        "absolute_grading_trace",
        "Krein_fundamental_symmetry",
        "represented_junk_quotient",
        "length_two_relative_curvature_block",
        "conditional_expectation_relative_block",
        "BRST_exact_diagonal_cancellation",
        "Pauli_Villars_trace_difference",
        "target_loaded_endpoint_projector",
    ]
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "endpoint_weight_no_go": {
            "channel_map_rank": 2,
            "channel_gram": [[72, 0], [0, 64]],
            "unique_exact_weights": [1, -1],
            "ordinary_positive_weights": [1, 1],
            "exact_weight_inertia_negative_zero_positive": [1, 0, 1],
            "positive_endpoint_trace_can_produce_Q": False,
        },
        "relative_block_route": {
            "projector": [["1/2", "-1/2"], ["-1/2", "1/2"]],
            "projector_rank": 1,
            "projector_idempotent": True,
            "projected_norm_inertia_negative_zero_positive": [0, 1, 1],
            "inherited_selector_rank": 0,
        },
        "candidate_audit": {
            "criteria": ["exact_Q", "positive_full_action", "gauge_Real", "canonical_normalization", "local_degree_compatible", "inherited_selector"],
            "names": names,
            "matrix": [list(map(int, c.candidate_matrix.row(i))) for i in range(12)],
            "rank": 6,
            "scores": list(map(int, c.score_vector)),
            "passes": list(map(int, c.pass_vector)),
            "passing_candidates": 0,
        },
        "best_candidates": [
            {"name": "ordinary_Hilbert_Schmidt_trace", "score": "5/6", "failed": "exact_Q"},
            {"name": "raw_supertrace", "score": "5/6", "failed": "positive_full_action"},
            {"name": "represented_junk_quotient", "score": "5/6", "failed": "inherited_selector"},
            {"name": "length_two_relative_curvature_block", "score": "5/6", "failed": "inherited_selector"},
        ],
        "status": {
            "best_positive_exact_route": "5/6",
            "remaining_slot": "derive relative curvature quotient from current represented calculus",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "candidate_passes_all_criteria": False,
            "positive_endpoint_trace_no_go": True,
            "positive_relative_block_route_exists_conditionally": True,
            "physical_trace_selector_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_curvature_junk_quotient_parent_origin_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()