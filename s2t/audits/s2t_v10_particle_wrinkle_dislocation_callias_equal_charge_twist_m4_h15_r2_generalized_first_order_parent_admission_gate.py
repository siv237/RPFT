#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_generalized_first_order_parent_admission import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_generalized_first_order_parent_admission_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_quark_lepton_connector_candidate_audit_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.admitted_a2 == sp.zeros(5)
    assert c.r2_a2 == 4 * c.r2_seed
    assert c.seeded_a2_coefficient == c.r2_seed
    assert c.existing_laplacian.rank() == 3
    assert len(c.existing_laplacian.nullspace()) == 2
    assert c.augmented_laplacian.rank() == 4
    assert len(c.augmented_laplacian.nullspace()) == 1
    assert c.inherited_r2_seed == sp.zeros(2, 1)

    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "generalized_inner_fluctuation": {
            "formula": "D_A=D+A1+A1_opposite+A2",
            "quadratic_term": "A2=sum_j hat(a_j)[A1,hat(b_j)]",
            "left_unitary_diagonal": list(map(int, c.left_unitary.diagonal())),
            "right_unitary_diagonal": list(map(int, c.right_unitary.diagonal())),
            "total_unitary_diagonal": list(map(int, c.total_unitary.diagonal())),
            "exact_gauge_covariance": True,
        },
        "admitted_SM_seed": {
            "support": ["Q_L-u_R", "Q_L-d_R", "L_L-e_R"],
            "Dirac_rank": 4,
            "A1_rank": int(c.admitted_a1.rank()),
            "A1_opposite_rank": int(c.admitted_opposite_a1.rank()),
            "A2_rank": int(c.admitted_a2.rank()),
            "A2_zero": True,
            "H15_laplacian_rank": 3,
            "H15_kernel_dimension": 2,
            "uniform_ray_selected": False,
        },
        "R2_positive_control": {
            "support": ["L_L-u_R", "Q_L-e_R"],
            "seed_operator_rank": 4,
            "double_commutator_rank": 4,
            "A1_equals": "-2 D_R2",
            "A1_opposite_equals": "-2 D_R2",
            "A2_equals": "4 D_R2",
            "A2_support_equals_seed_support": True,
            "augmented_laplacian_rank": 4,
            "augmented_kernel_dimension": 1,
        },
        "inheritance": {
            "R2_seed_coefficients": [0, 0],
            "R2_seed_rank": 0,
            "generalized_fluctuation_creates_absent_support": False,
            "family_or_Callias_tensor_amplification_changes_support": False,
        },
        "status": {
            "conditional_generalized_architecture": "12/12",
            "inherited_R2_seed": "0/2",
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
            "generalized_first_order_formalism_is_consistent": True,
            "current_SM_parent_generates_R2": False,
            "nonzero_A2_requires_inserted_R2_seed": True,
            "generalized_R2_parent_admitted_as_derivation": False,
            "reason": "inner fluctuations preserve the block support of the finite Dirac seed",
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_dirac_seed_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()