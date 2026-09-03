#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_breaking_background_common_carrier_admission import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_breaking_background_common_carrier_admission_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_gap_coefficient_candidate_audit_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.delta_hypercharge6 == sp.ImmutableMatrix([4, 4, 4, -2, -2, -2, 0, -6])
    assert c.polynomial_neutral_selector == c.neutral_selector
    assert c.neutral_selector.rank() == 1
    assert len(c.delta_hypercharge_generator.nullspace()) == 1
    assert c.stabilizer_constraint * c.unbroken_cartan_ray == sp.zeros(1, 1)
    assert c.sigma_charge_basis * c.unbroken_cartan_ray == c.sigma_hypercharge6
    assert c.joint_spectral_algebra.rank() == 6
    assert c.hypercharge_spectral_algebra.rank() == 6
    assert c.combined_spectral_algebra.rank() == 6
    assert c.inherited_tome10_background_map.rank() == 0

    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "delta_carrier": {
            "representation": "Delta=(2_R,1_L,4_4)",
            "complex_dimension": 8,
            "six_T3R_weights": list(map(int, c.delta_t3r6)),
            "three_B_minus_L_weights": list(map(int, c.delta_bl3)),
            "six_Y_weights": list(map(int, c.delta_hypercharge6)),
            "neutral_direction_count": 1,
            "neutral_selector_formula": "P0=-(Q-4I)(Q+2I)(Q+6I)/48",
            "preserves_SU2L": True,
        },
        "stabilizer": {
            "neutral_weight": [3, -3],
            "constraint": "3*alpha-3*beta=0",
            "kernel_ray": [1, 1],
            "unbroken_generator": "6Y=6T3R+3(B-L)",
            "unique_Cartan_ray": True,
        },
        "sigma_action": {
            "six_T3R": list(map(int, c.sigma_t3r6)),
            "three_B_minus_L": list(map(int, c.sigma_bl3)),
            "six_Y": list(map(int, c.sigma_hypercharge6)),
            "charge_basis_Gram": [[72, 0], [0, 64]],
            "joint_spectral_algebra_rank": 6,
            "hypercharge_spectral_algebra_rank": 6,
            "combined_rank": 6,
            "same_spectral_algebra": True,
        },
        "branch_status": {
            "general_fundamental_Delta_carrier": False,
            "constrained_composite_Delta_carrier": True,
            "minimal_composite_rank_one_vacuum_stable": False,
            "relative_mapping_cone_Delta_plus_C_signature": [43, 9, 0],
            "relative_mapping_cone_status": "conditional_not_embedded_in_current_Tome_X_parent",
            "inherited_Tome_X_background_map_rank": 0,
        },
        "status": {
            "conditional_common_carrier": "admitted",
            "conditional_origin": "3/4",
            "current_physical_origin": "2/4",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "single_scalar_carrier_for_hypercharge_background_exists": True,
            "carrier_is_Delta_not_two_independent_adjoints": True,
            "current_Tome_X_parent_contains_background_state": False,
            "physical_background_origin_closed": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_mapping_cone_common_parent_typed_embedding_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()