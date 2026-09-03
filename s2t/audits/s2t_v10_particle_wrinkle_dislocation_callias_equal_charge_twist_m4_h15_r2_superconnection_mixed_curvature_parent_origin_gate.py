#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_mixed_curvature_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_mixed_curvature_parent_origin_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_moment_map_odd_auxiliary_trilinear_parent_origin_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.oddness_residual == sp.zeros(16)
    assert c.graded_polarization == c.hypercharge_generator
    assert c.graded_polarization.rank() == 8
    assert c.ordinary_polarization == c.ordinary_generator
    assert c.polarization_defect.rank() == 4
    assert c.inherited_auxiliary_embedding.rank() == 0
    assert c.conditional_auxiliary_embedding.rank() == 8

    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "superconnection": {
            "left_endpoint_moment": "T=6T3_R",
            "right_endpoint_moment": "-B=-3(B-L)",
            "graded_endpoint_difference": "T-(-B)=Q=6Y",
            "ordinary_endpoint_sum": "T+(-B)=T-B",
            "oddness_residual_rank": c.oddness_residual.rank(),
            "Real_self_adjoint": True,
        },
        "curvature_polarization": {
            "graded_diagonal": list(map(int, c.graded_polarization.diagonal())),
            "graded_rank": 8,
            "ordinary_diagonal": list(map(int, c.ordinary_polarization.diagonal())),
            "ordinary_rank": 8,
            "graded_minus_ordinary_diagonal": list(map(int, c.polarization_defect.diagonal())),
            "defect_rank": 4,
            "coefficient_locked_by_half_anticommutator": True,
        },
        "trace_diagnosis": {
            "graded_trace_inertia_negative_zero_positive": [8, 0, 8],
            "ordinary_trace_inertia_negative_zero_positive": [0, 0, 16],
            "exact_Q_uses_indefinite_supertrace": True,
            "positive_Hilbert_Schmidt_trace_gives_Q": False,
        },
        "inheritance": {
            "required_auxiliary_arrow_rank": 8,
            "inherited_auxiliary_arrow_rank": 0,
            "grading_inherited": True,
            "positive_trace_selector_for_mixed_component": "open",
        },
        "status": {
            "conditional_superconnection_origin": "4/6",
            "physical_origin": "4/6",
            "remaining_slots": ["positive full trace or derived quotient", "inherited A_Sigma arrow"],
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "graded_curvature_generates_exact_cross_bilinear": True,
            "coefficient_is_canonical": True,
            "positive_full_trace_generates_exact_cross_bilinear": False,
            "physical_parent_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_curvature_trace_selector_candidate_audit_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()