#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hubbard_stratonovich_odd_auxiliary_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hubbard_stratonovich_odd_auxiliary_parent_origin_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_minimal_odd_auxiliary_bimodule_candidate_audit_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.shift_matrix.det() == 1
    assert c.hs_parent_hessian.rank() == 14
    assert len(c.hs_parent_hessian.nullspace()) == 2
    assert c.hs_schur_complement == c.target_gap
    assert c.inherited_parent_hessian.rank() == 16
    assert c.inherited_cross_block.rank() == 0
    assert c.required_cross_block.rank() == 8
    assert c.new_operator_increment.rank() == 16
    assert c.rank_ledger == sp.ImmutableMatrix([16, 14])

    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "formal_Hubbard_Stratonovich_identity": {
            "potential": "1/2 Sigma^T 49I Sigma + A^T Q Sigma + 1/2 A^T A",
            "completed_square": "1/2 ||A+Q Sigma||^2 + 1/2 Sigma^T(49I-Q^2)Sigma",
            "stationary_solution": "A*=-Q Sigma",
            "stationary_map_rank": 8,
            "shift_determinant": 1,
            "Gaussian_metric_determinant": 1,
            "full_rank_nullity": [14, 2],
            "Schur_complement_diagonal": list(map(int, c.hs_schur_complement.diagonal())),
        },
        "origin_audit": {
            "inherited_parent": "diag(49I,I)",
            "inherited_parent_rank_nullity": [16, 0],
            "inherited_cross_block_rank": 0,
            "inherited_Schur_complement": "49I",
            "required_cross_block": "Q",
            "required_cross_block_rank": 8,
            "operator_increment_rank": 16,
            "operator_increment_inertia_negative_zero_positive": [8, 0, 8],
            "rank_mismatch_blocks_invertible_field_redefinition": True,
        },
        "interpretation": {
            "exact_linearization_of_existing_target_gap": True,
            "derivation_of_missing_Q_squared_term": False,
            "field_independent_Gaussian_normalization": True,
            "new_mixed_operator_required": True,
        },
        "status": {
            "formal_identity": "4/4",
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
            "Hubbard_Stratonovich_rewrite_exact": True,
            "Hubbard_Stratonovich_is_physical_origin": False,
            "inherited_and_target_parents_congruent": False,
            "physical_parent_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()