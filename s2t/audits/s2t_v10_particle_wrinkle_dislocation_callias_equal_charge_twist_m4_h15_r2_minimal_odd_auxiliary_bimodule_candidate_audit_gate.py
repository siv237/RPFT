#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_minimal_odd_auxiliary_bimodule_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_minimal_odd_auxiliary_bimodule_candidate_audit_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_shared_fixed_point_auxiliary_channel_typed_embedding_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert sum(c.minimal_multiplicities) == 8
    assert c.candidate_matrix.shape == (12, 6)
    assert c.candidate_matrix.rank() == 6
    assert c.pass_vector == sp.zeros(12, 1)
    assert c.hubbard_stratonovich_row == sp.ImmutableMatrix([[1, 1, 1, 1, 1, 0]])
    assert c.inherited_embedding.rank() == 0
    assert c.conditional_embedding.rank() == 8
    assert c.conditional_schur_complement == sp.diag(40, 40, 0, 48, 48, 0, 40, 40)

    names = [
        "inherited_fixed_point_C",
        "arbitrary_eight_coordinate_slice",
        "reuse_Sigma",
        "composite_QSigma",
        "Hubbard_Stratonovich_A_Sigma",
        "cotangent_TstarSigma",
        "BV_antifield_Sigma",
        "KO6_charge_conjugate_one_form",
        "Delta_mapping_cone_off_diagonal_arrow",
        "Callias_normal_component",
        "superconnection_suspension",
        "Pati_Salam_adjoint_D_term",
    ]
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "required_module": {
            "real_dimension": 8,
            "weights_6Y": list(map(int, c.required_weights)),
            "weight_multiplicities_order_minus7_minus3_minus1_plus1_plus3_plus7": list(map(int, c.minimal_multiplicities)),
            "grading": "odd",
            "reality_pairs": [[0, 1], [2, 5], [3, 4], [6, 7]],
            "trace_metric": "I8",
            "algebraically_eliminable": True,
        },
        "candidate_audit": {
            "criteria": ["exact_weights", "odd_grading", "Real_closure", "positive_bosonic_metric", "independent_algebraic_elimination", "inherited_parent"],
            "names": names,
            "matrix": [list(map(int, c.candidate_matrix.row(i))) for i in range(c.candidate_matrix.rows)],
            "rank": 6,
            "scores": list(map(int, c.score_vector)),
            "passes": list(map(int, c.pass_vector)),
            "passing_candidates": 0,
        },
        "best_conditional_candidate": {
            "name": "Hubbard_Stratonovich_A_Sigma",
            "score": "5/6",
            "failed_criterion": "inherited_parent",
            "embedding_rank": 8,
            "full_parent_rank_nullity": [14, 2],
            "Schur_complement_diagonal": list(map(int, c.conditional_schur_complement.diagonal())),
        },
        "inheritance": {
            "current_independent_odd_auxiliary_embedding_rank": 0,
            "physical_origin": "3/4",
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
            "minimal_representation_determined": True,
            "conditional_Hubbard_Stratonovich_closure": True,
            "physical_odd_auxiliary_parent_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hubbard_stratonovich_odd_auxiliary_parent_origin_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()