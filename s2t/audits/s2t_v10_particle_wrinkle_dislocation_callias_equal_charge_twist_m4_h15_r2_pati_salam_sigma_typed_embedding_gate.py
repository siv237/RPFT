#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_typed_embedding import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_typed_embedding_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_dirac_seed_candidate_audit_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert sum(c.sector_dimensions) == 60
    assert c.target_selector.rank() == 2
    assert c.complement_selector.rank() == 6
    assert c.su2r_selector_defect.rank() == 4
    assert c.augmented_laplacian.rank() == 4
    assert len(c.augmented_laplacian.nullspace()) == 1
    assert c.inherited_sigma_map.rank() == 0

    sectors = [
        "(8,2)_{1/2}",
        "(8,2)_{-1/2}",
        "(3,2)_{7/6}=R2",
        "(3,2)_{1/6}=tilde_R2",
        "(bar3,2)_{-1/6}=tilde_R2_conjugate",
        "(bar3,2)_{-7/6}=R2_conjugate",
        "(1,2)_{1/2}",
        "(1,2)_{-1/2}",
    ]
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "Pati_Salam_parent": {
            "group": "SU(2)_R x SU(2)_L x SU(4)",
            "multiplet": "Sigma=(2_R,2_L,15_4)",
            "complex_dimension": 60,
            "hypercharge_rule": "Y=T3_R+(B-L)/2",
            "SU4_branching": "15 -> 8_0 + 3_{4/3} + bar3_{-4/3} + 1_0",
        },
        "SM_branching": {
            "sectors": sectors,
            "dimensions": list(map(int, c.sector_dimensions)),
            "six_hypercharges": list(map(int, c.hypercharge6)),
            "dimension_sum": 60,
            "R2_plus_conjugate_dimension": 12,
            "companion_dimension": 48,
        },
        "R2_embedding": {
            "target_sector_indices": [2, 5],
            "selector_rank": 2,
            "SM_hypercharge_commutator_rank": 0,
            "SM_colour_commutator_rank": 0,
            "SU2R_selector_defect_rank": 4,
            "H15_edge_count": 2,
            "H15_augmented_incidence_rank": 4,
            "H15_augmented_laplacian_rank": 4,
            "H15_kernel_dimension": 1,
            "mixed_cycle_dimension": 1,
        },
        "companion_content": {
            "sector_count": 6,
            "contains_tilde_R2_pair": True,
            "contains_colour_octet_doublet_pair": True,
            "contains_Higgs_like_doublet_pair": True,
            "R2_only_subspace_is_full_PS_invariant": False,
        },
        "inheritance": {
            "current_parent_to_Sigma_R2_map_rank": 0,
            "Pati_Salam_algebra_is_current_parent": False,
            "R2_selector_origin": False,
        },
        "status": {
            "conditional_typed_embedding": "14/14",
            "R2_component_present": True,
            "R2_component_canonically_isolated": False,
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
            "Sigma_contains_exact_R2_type": True,
            "R2_edges_connect_H15": True,
            "R2_only_selector_preserves_full_Pati_Salam": False,
            "typed_embedding_is_inherited": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_component_selector_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()