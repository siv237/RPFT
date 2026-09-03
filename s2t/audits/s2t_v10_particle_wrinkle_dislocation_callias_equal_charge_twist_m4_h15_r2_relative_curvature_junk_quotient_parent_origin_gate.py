#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_curvature_junk_quotient_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_curvature_junk_quotient_parent_origin_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_curvature_trace_selector_candidate_audit_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.represented_one_forms.rank() == 2
    assert c.represented_two_forms.rank() == 2
    assert c.degree_two_junk.rank() == 0
    assert c.quotient_basis.rank() == 2
    assert c.relative_projector**2 == c.relative_projector
    assert c.relative_projector.rank() == 1
    assert c.projected_sum == sp.zeros(2, 1)
    assert c.projected_relative == c.relative_vector
    assert c.relative_readout == c.target_generator

    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "standard_two_node_calculus": {
            "node_algebra": "C^2",
            "represented_one_form_rank": 2,
            "represented_one_form_kernel_dimension": 2,
            "represented_two_form_rank": 2,
            "degree_two_junk_rank": 0,
            "degree_two_quotient_rank": 2,
            "sum_class_survives": True,
            "relative_class_survives": True,
            "junk_selects_relative_class": False,
        },
        "graph_hodge_route": {
            "incidence": [[1, -1]],
            "laplacian": [[1, -1], [-1, 1]],
            "relative_projector": [["1/2", "-1/2"], ["-1/2", "1/2"]],
            "projector_rank": 1,
            "projector_inertia_negative_zero_positive": [0, 1, 1],
            "kills_sum": True,
            "preserves_difference": True,
            "relative_readout": "T-(-B)=Q",
            "relative_readout_rank": 8,
        },
        "inheritance": {
            "inherited_Hodge_selector_rank": 0,
            "conditional_Hodge_selector_rank": 1,
            "inherited_auxiliary_edge_rank": 0,
            "conditional_auxiliary_edge_rank": 8,
        },
        "status": {
            "conditional_relative_Hodge_parent": "4/6",
            "physical_origin": "4/6",
            "remaining_slots": ["inherited graph-Hodge selector", "inherited odd auxiliary edge"],
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "standard_junk_quotient_derives_relative_selector": False,
            "canonical_graph_Hodge_projector_exists": True,
            "physical_parent_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_common_parent_admission_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()