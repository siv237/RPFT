#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_sigma_mixed_curvature_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_sigma_mixed_curvature_candidate_audit_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_mapping_cone_common_parent_typed_embedding_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.curvature_basis.rank() == 3
    assert c.target_coefficients == sp.ImmutableMatrix([40, -1, -2])
    assert c.target_gap == sp.ImmutableMatrix([40, 40, 0, 48, 48, 0, 40, 40])
    assert sp.ImmutableMatrix.hstack(c.even_subbasis, c.target_gap).rank() == 3
    assert sp.ImmutableMatrix.hstack(c.mixed_subbasis, c.target_gap).rank() == 3
    assert c.inherited_curvature_map.rank() == 0
    assert c.candidate_matrix.rank() == 6
    assert c.pass_vector == sp.zeros(11, 1)

    candidates = [
        "inherited_Delta_mapping_cone_direct_sum",
        "universal_norm_portal",
        "four_colour_B2_moment_map_portal",
        "isolated_mixed_TB_portal",
        "independently_weighted_B2_and_TB_portals",
        "single_Delta_stabilizer_moment_map_curvature",
        "target_loaded_GY_potential",
        "composite_Y_phi_Sigma4_at_phi_zero",
        "Delta_determinant_selector",
        "factorized_product_heat_kernel_trace",
        "Callias_M4_cross_channel",
    ]
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "exact_decomposition": {
            "identity": "T^2=9I on Sigma",
            "formula": "G_Y=49I-(T+B)^2=40I-B^2-2TB",
            "basis": ["I", "B^2", "TB"],
            "basis_rank": 3,
            "coefficients": list(map(int, c.target_coefficients)),
            "gap_diagonal": list(map(int, c.target_gap)),
            "gap_rank": 6,
            "gap_nullity": 2,
            "B2_without_TB_sufficient": False,
            "TB_without_B2_sufficient": False,
        },
        "candidate_audit": {
            "criteria": [
                "Sigma_coupling",
                "B2_channel",
                "TB_channel",
                "locked_one_to_two_ratio",
                "inherited_common_parent",
                "correct_target_gap_sign",
            ],
            "candidates": candidates,
            "matrix": [list(map(int, c.candidate_matrix.row(i))) for i in range(c.candidate_matrix.rows)],
            "matrix_rank": 6,
            "scores": list(map(int, c.score_vector)),
            "pass": list(map(int, c.pass_vector)),
            "passing_candidates": 0,
            "closest_candidate": "single_Delta_stabilizer_moment_map_curvature",
            "closest_score": "5/6",
            "closest_missing_criterion": "inherited_common_parent",
            "coverage": list(map(int, c.coverage)),
        },
        "inheritance": {
            "current_curvature_coefficient_map_rank": 0,
            "new_connected_curvature_required": True,
            "independent_portal_weights_not_accepted": True,
        },
        "status": {
            "algebraic_mixed_curvature_target": "derived",
            "candidate_passes": "0/11",
            "physical_origin": "2/4",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "exact_mixed_curvature_signature_known": True,
            "current_parent_generates_required_mixed_curvature": False,
            "physical_mixed_curvature_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_stabilizer_moment_map_curvature_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()