#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_dirac_seed_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_dirac_seed_candidate_audit_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_generalized_first_order_parent_admission_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.internal_r2_projections == sp.zeros(5, 1)
    assert c.target_projection == c.r2_seed
    assert c.candidate_matrix.rank() == 6
    assert c.pass_vector == sp.zeros(11, 1)
    assert c.inherited_seed_map.rank() == 0

    candidates = [
        "standard_finite_Dirac",
        "standard_Higgs_one_form",
        "admitted_generalized_A2",
        "Callias_M4_tensor_amplifier",
        "H15_incidence_laplacian",
        "Pati_Salam_Sigma_2_2_15",
        "Clifford_mixed_weak_colour_scalar",
        "historical_S0_reality_relaxation",
        "strict_mirror_cycle_completion",
        "explicit_D_R2_insertion",
        "normalized_target_loaded_D_R2",
    ]
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "R2_target": {
            "edges": ["L_L-u_R", "Q_L-e_R"],
            "multiplet": "R2=(3,2)_{7/6}",
            "operator_rank_with_adjoints": 4,
            "support_projector_rank": 4,
        },
        "inherited_operator_projection_audit": {
            "operators": [
                "standard_finite_Dirac",
                "standard_Higgs_one_form",
                "admitted_generalized_A2",
                "Callias_H15_identity_factor",
                "H15_type_laplacian",
            ],
            "R2_projection_ranks": list(map(int, c.internal_r2_projections)),
            "all_zero": True,
        },
        "extension_routes": {
            "Pati_Salam_Sigma": "contains an R2-typed component after explicit algebra enlargement",
            "Clifford_extension": "contains mixed weak-colour scalars but does not select the exact two-edge R2 seed here",
            "S0_reality_relaxation": "historical leptoquark channel is not the current two-edge R2 rectangle",
            "strict_mirror_cycle": "factorizes transport through new vertices and has no elementary R2 block",
        },
        "candidate_audit": {
            "criteria": [
                "exact_R2_two_edge_support",
                "correct_SM_gauge_type",
                "Real_odd_consistency",
                "current_parent_inheritance",
                "no_new_algebra_or_fermions",
                "coefficient_normalization_origin",
            ],
            "candidates": candidates,
            "matrix": [list(map(int, c.candidate_matrix.row(i))) for i in range(c.candidate_matrix.rows)],
            "matrix_rank": 6,
            "scores": list(map(int, c.score_vector)),
            "pass": list(map(int, c.pass_vector)),
            "passing_candidates": 0,
            "coverage": list(map(int, c.coverage)),
        },
        "inheritance": {
            "current_parent_to_R2_coefficient_map_rank": 0,
            "target_loaded_coefficient_hessian_rank": 1,
            "target_loaded_is_derivation": False,
        },
        "status": {
            "conditional_target_architecture": "12/12",
            "inherited_R2_support": "0/5",
            "physical_origin": "0/3",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "R2_seed_found_in_current_parent": False,
            "explicit_D_R2_is_exact_but_target_loaded": True,
            "Pati_Salam_is_the_nearest_structural_extension": True,
            "seed_origin_gate_closed": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_typed_embedding_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()