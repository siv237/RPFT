#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_component_selector_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_component_selector_candidate_audit_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_typed_embedding_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.polynomial_selector == c.target_selector
    assert c.affine_evaluation.rank() == 2
    assert c.affine_augmented.rank() == 3
    assert c.quadratic_evaluation.rank() == 3
    assert c.su2r_defect.rank() == 4
    assert c.target_mass_hessian.rank() == 6
    assert len(c.target_mass_hessian.nullspace()) == 2
    assert c.candidate_matrix.rank() == 6
    assert c.pass_vector == sp.zeros(11, 1)

    candidates = [
        "identity",
        "hypercharge_sign",
        "affine_polynomial_in_Y2",
        "minimal_quadratic_polynomial_in_Y2",
        "T3R_weight_selector",
        "B_minus_L_triplet_selector",
        "colour_Casimir_selector",
        "adjoint_VEV_mass_splitting",
        "inherited_spectral_Hessian",
        "Callias_uniform_amplifier",
        "target_loaded_complement_penalty",
    ]
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "hypercharge_selector": {
            "operator": "Q=6Y",
            "squared_spectral_values": [1, 9, 49],
            "formula": "P_R2=((Q^2-I)(Q^2-9I))/1920",
            "diagonal": list(map(int, c.polynomial_selector.diagonal())),
            "rank": 2,
            "nullity": 6,
            "affine_Y2_selector_exists": False,
            "minimal_degree_in_Y2": 2,
            "quadratic_coefficients_basis_1_x_x2": ["9/1920", "-10/1920", "1/1920"],
        },
        "symmetry": {
            "SM_hypercharge_commutator_rank": 0,
            "Real_conjugation_commutator_rank": 0,
            "SU2R_commutator_rank": 4,
            "interpretation": "canonical only after Pati-Salam breaking to the Standard Model",
        },
        "ideal_mass_split": {
            "Hessian": "2(I-P_R2)",
            "rank": 6,
            "nullity": 2,
            "lifted_companion_sectors": 6,
            "light_sectors": ["R2", "R2_conjugate"],
            "inherited_Hessian_rank": 0,
        },
        "candidate_audit": {
            "criteria": [
                "exact_R2_selector",
                "SM_invariance",
                "Real_compatibility",
                "inherited_data",
                "dynamical_mass_splitting",
                "coefficient_origin",
            ],
            "candidates": candidates,
            "matrix": [list(map(int, c.candidate_matrix.row(i))) for i in range(c.candidate_matrix.rows)],
            "matrix_rank": 6,
            "scores": list(map(int, c.score_vector)),
            "pass": list(map(int, c.pass_vector)),
            "passing_candidates": 0,
            "coverage": list(map(int, c.coverage)),
        },
        "status": {
            "algebraic_R2_selector": "derived",
            "conditional_selector_architecture": "14/14",
            "dynamical_selector_parent": "absent",
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
            "canonical_SM_R2_projector_found": True,
            "projector_is_full_Pati_Salam_invariant": False,
            "current_parent_generates_required_mass_split": False,
            "physical_component_selector_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_projector_mass_splitting_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()