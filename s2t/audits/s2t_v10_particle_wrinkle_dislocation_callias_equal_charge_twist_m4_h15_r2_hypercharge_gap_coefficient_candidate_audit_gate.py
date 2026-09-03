#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_gap_coefficient_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_gap_coefficient_candidate_audit_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_projector_mass_splitting_parent_origin_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.sector_mass_map.rank() == 2
    assert c.diagnostic_masses == sp.ImmutableMatrix(
        [[-1, -1, -1], [49, 9, 1], [-49, -9, -1], [0, 40, 48], [-20, 20, 28], [-40, 0, 8]]
    )
    assert c.strict_sign_pass == sp.ImmutableMatrix([0, 0, 0, 0, 1, 0])
    assert c.interior_coefficients.rank() == 2
    assert c.inherited_coefficient_map.rank() == 0
    assert c.candidate_matrix.rank() == 6
    assert c.pass_vector == sp.zeros(11, 1)

    candidates = [
        "ordinary_one_profile_spectral_moments",
        "universal_quadratic_mass_shift",
        "positive_hypercharge_Casimir_D_term",
        "negative_hypercharge_Casimir",
        "algebraic_boundary_gap_GY",
        "target_loaded_interior_potential",
        "independent_Pati_Salam_adjoint_VEV_pair",
        "Coleman_Weinberg_universal_singlet",
        "fermionic_determinant_susceptibility",
        "dimensional_transmutation_scale_only",
        "connected_breaking_background_spectral_trace",
    ]
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "coefficient_cone": {
            "mass_polynomial": "m^2(Q^2)=a+b*Q^2",
            "strict_conditions": ["b<0", "a+49*b<0", "a+9*b>0"],
            "normalized_parameterization": "(a,b)=(49-r,-1), 0<r<40",
            "not_unique": True,
            "inequivalent_exact_ratios": [10, 30],
            "corresponding_masses": [list(map(int, c.interior_masses.row(i))) for i in range(2)],
        },
        "diagnostic_coefficients": {
            "basis": ["I", "Q^2"],
            "vectors": [list(map(int, c.diagnostic_coefficients.row(i))) for i in range(c.diagnostic_coefficients.rows)],
            "masses_order_R2_Q2_9_Q2_1": [list(map(int, c.diagnostic_masses.row(i))) for i in range(c.diagnostic_masses.rows)],
            "strict_sign_pass": list(map(int, c.strict_sign_pass)),
            "boundary_flags": list(map(int, c.boundary_flags)),
            "interpretation": "G_Y is a boundary selector; an interior tachyonic ratio is additional data",
        },
        "candidate_audit": {
            "criteria": [
                "Q2_resolution",
                "interior_sign_cone",
                "positive_quartic",
                "typed_SM_breaking_background",
                "inherited_carrier",
                "coefficient_locking",
            ],
            "candidates": candidates,
            "matrix": [list(map(int, c.candidate_matrix.row(i))) for i in range(c.candidate_matrix.rows)],
            "matrix_rank": 6,
            "scores": list(map(int, c.score_vector)),
            "pass": list(map(int, c.pass_vector)),
            "passing_candidates": 0,
            "closest_candidate": "connected_breaking_background_spectral_trace",
            "closest_score": "5/6",
            "closest_missing_criterion": "inherited_carrier",
            "coverage": list(map(int, c.coverage)),
        },
        "inheritance": {
            "coefficient_map_rank": 0,
            "coefficient_map_nullity": 3,
            "ratio_selected": False,
            "absolute_scale_selected": False,
        },
        "status": {
            "algebraic_gap": "derived",
            "coefficient_candidates": "0/11",
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
            "sign_cone_is_nonempty": True,
            "sign_cone_selects_unique_ratio": False,
            "current_parent_locks_coefficients": False,
            "physical_gap_coefficient_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_breaking_background_common_carrier_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()