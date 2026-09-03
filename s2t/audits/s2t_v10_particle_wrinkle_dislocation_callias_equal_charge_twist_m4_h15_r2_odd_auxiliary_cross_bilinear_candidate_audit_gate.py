#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hubbard_stratonovich_odd_auxiliary_parent_origin_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.cartan_basis.rank() == 2
    assert c.cartan_basis * c.locked_coefficients == c.hypercharge6
    assert c.required_cross_block.rank() == 8
    assert c.inherited_cross_block.rank() == 0
    assert c.cross_hessian.rank() == 16
    assert c.candidate_matrix.shape == (12, 6)
    assert c.candidate_matrix.rank() == 6
    assert c.pass_vector == sp.zeros(12, 1)

    names = [
        "universal_identity_portal",
        "fixed_point_projection",
        "one_sided_target_Q",
        "Delta_moment_map_trilinear",
        "two_independent_Cartan_portals",
        "ordinary_even_spectral_moments",
        "spectral_commutator_D_Y",
        "inherited_mapping_cone_incidence",
        "KO6_first_order_fluctuation",
        "Callias_normal_component",
        "superconnection_mixed_curvature",
        "fermion_loop_triangle",
    ]
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "required_cross_operator": {
            "operator": "Q=6Y=T+B",
            "spectrum": list(map(int, c.hypercharge6)),
            "Cartan_basis_rank": 2,
            "locked_coefficients_T_B": [1, 1],
            "cross_block_rank": 8,
            "full_cross_hessian_rank": 16,
            "full_cross_hessian_inertia_negative_zero_positive": [8, 0, 8],
            "inherited_cross_block_rank": 0,
        },
        "candidate_audit": {
            "criteria": ["typed_A_Sigma_domain", "exact_Q", "gauge_equivariance", "Real_even_scalar", "single_parent_locked_coefficient", "inherited_action"],
            "names": names,
            "matrix": [list(map(int, c.candidate_matrix.row(i))) for i in range(c.candidate_matrix.rows)],
            "rank": 6,
            "scores": list(map(int, c.score_vector)),
            "passes": list(map(int, c.pass_vector)),
            "passing_candidates": 0,
        },
        "best_candidates": [
            {"name": "Delta_moment_map_trilinear", "score": "5/6", "failed": "inherited_action"},
            {"name": "superconnection_mixed_curvature", "score": "5/6", "failed": "inherited_action"},
        ],
        "status": {
            "physical_origin": "5/6",
            "remaining_slot": "inherited common three-field parent",
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
            "cross_operator_unique_in_Cartan_span": True,
            "best_route_identified": True,
            "physical_cross_bilinear_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_moment_map_odd_auxiliary_trilinear_parent_origin_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()