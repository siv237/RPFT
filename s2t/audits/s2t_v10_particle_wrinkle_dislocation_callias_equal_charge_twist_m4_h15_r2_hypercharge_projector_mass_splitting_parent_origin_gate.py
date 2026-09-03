#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_projector_mass_splitting_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_projector_mass_splitting_parent_origin_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_component_selector_candidate_audit_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.gap_operator == sp.diag(40, 40, 0, 48, 48, 0, 40, 40)
    assert c.gap_operator.rank() == 6
    assert len(c.gap_operator.nullspace()) == 2
    assert c.gap_operator * c.target_selector == sp.zeros(8)
    assert c.su2r_defect.rank() == 4
    assert c.witness_hessian == sp.diag(20, 20, -20, 28, 28, -20, 20, 20)
    assert c.witness_hessian.det() == 50176000000
    assert c.inherited_gap_hessian.rank() == 0
    assert c.coefficient_origin == sp.zeros(2, 1)

    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "hypercharge_gap": {
            "operator": "G_Y=49I-(6Y)^2",
            "diagonal": list(map(int, c.gap_operator.diagonal())),
            "eigenvalue_multiplicities": {"0": 2, "40": 4, "48": 2},
            "rank": 6,
            "nullity": 2,
            "kernel": ["R2", "R2_conjugate"],
            "positive_semidefinite": True,
            "Real_compatible": True,
            "SU2R_commutator_rank": 4,
        },
        "quadratic_family": {
            "Hessian": "H(mu2,kappa)=kappa*G_Y-mu2*I",
            "R2_mass_squared": "-mu2",
            "Q2_9_companion_mass_squared": "40*kappa-mu2",
            "Q2_1_companion_mass_squared": "48*kappa-mu2",
            "R2_only_instability_conditions": ["kappa>0", "mu2>0", "mu2/kappa<40"],
            "quartic_stabilization_still_required": True,
        },
        "exact_witness": {
            "kappa": 1,
            "mu2": 20,
            "ratio_mu2_over_kappa": 20,
            "diagonal": list(map(int, c.witness_hessian.diagonal())),
            "signature_negative_zero_positive": [2, 0, 6],
            "determinant": 50176000000,
            "status": "conditional_only",
        },
        "inheritance": {
            "inherited_gap_Hessian_rank": 0,
            "coefficient_origin_map": [0, 0],
            "kappa_derived": False,
            "mu2_over_kappa_derived": False,
            "absolute_mass_scale_derived": False,
        },
        "status": {
            "algebraic_gap_operator": "derived",
            "conditional_mass_splitting_architecture": "14/14",
            "dynamical_mass_parent": "absent",
            "physical_origin": "1/3",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "conditional_R2_only_tachyonic_window_exists": True,
            "current_parent_generates_hypercharge_gap": False,
            "tachyonic_ratio_selected": False,
            "absolute_scale_selected": False,
            "physical_mass_splitting_parent_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_gap_coefficient_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()