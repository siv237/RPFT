#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_mapping_cone_common_parent_typed_embedding import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_mapping_cone_common_parent_typed_embedding_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_breaking_background_common_carrier_admission_gate_results.json").read_text()
    )
    relative_parent = json.loads(
        (ROOT / "s2t/results/s2t_v4_pati_salam_irreducible_relative_cycle_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    assert relative_parent["uneliminated_auxiliary_Hessian"]["total_real_dimension"] == 52
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.delta_injection.rank() == 52
    assert c.sigma_injection.rank() == 8
    assert c.delta_injection.T * c.sigma_injection == sp.zeros(52, 8)
    assert c.inherited_cross_block.rank() == 0
    assert c.inherited_direct_sum_hessian.rank() == 43
    assert len(c.inherited_direct_sum_hessian.nullspace()) == 17
    assert c.conditional_gap_hessian.rank() == 49
    assert len(c.conditional_gap_hessian.nullspace()) == 11
    assert c.inherited_coefficient_map.rank() == 0
    assert c.universal_augmented_map.rank() == 2

    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "reused_parent": relative_parent["gate"],
        "typed_common_carrier": {
            "Delta_plus_auxiliary_real_dimension": 52,
            "Sigma_sector_dimension": 8,
            "total_dimension": 60,
            "Delta_injection_rank": 52,
            "Sigma_injection_rank": 8,
            "orthogonal_injections": True,
            "complete_direct_sum": True,
        },
        "inherited_embedding": {
            "Delta_inertia_negative_zero_positive": [0, 9, 43],
            "common_Hessian_rank": 43,
            "common_Hessian_nullity": 17,
            "common_inertia_negative_zero_positive": [0, 17, 43],
            "Sigma_Hessian_rank": 0,
            "Delta_Sigma_cross_rank": 0,
            "interpretation": "stable Delta background but eight completely flat Sigma sectors",
        },
        "conditional_gap_insertion": {
            "Sigma_gap_spectrum": {"0": 2, "40": 4, "48": 2},
            "common_Hessian_rank": 49,
            "common_Hessian_nullity": 11,
            "common_inertia_negative_zero_positive": [0, 11, 49],
            "status": "typed_but_not_parent_derived",
        },
        "coefficient_origin": {
            "inherited_map_rank": 0,
            "universal_norm_portal_rank": 1,
            "target_gap_coefficients_basis_I_Q2": [49, -1],
            "target_outside_universal_portal_image": True,
            "connected_extension_map_rank": 2,
            "new_mixed_curvature_required": True,
        },
        "status": {
            "typed_direct_sum": "admitted",
            "connected_common_parent": "absent",
            "conditional_status": "3/4",
            "physical_status": "2/4",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "mapping_cone_parent_embeds_as_typed_direct_sum": True,
            "mapping_cone_parent_generates_Sigma_gap": False,
            "mapping_cone_parent_generates_Delta_Sigma_cross_curvature": False,
            "physical_common_parent_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_sigma_mixed_curvature_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()