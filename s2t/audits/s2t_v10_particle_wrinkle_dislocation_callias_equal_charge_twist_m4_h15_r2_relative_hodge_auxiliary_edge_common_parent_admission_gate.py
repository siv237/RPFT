#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_common_parent_admission import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_common_parent_admission_gate_results.json"


def main():
    predecessor = json.loads((ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_curvature_junk_quotient_parent_origin_gate_results.json").read_text())
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.weight_match_matrix == sp.zeros(36, 8)
    assert c.intertwiner_constraint.rank() == 288
    assert c.hodge_projector**2 == c.hodge_projector
    assert c.hodge_projector.rank() == 8
    assert c.gauge_hodge_commutator == sp.zeros(16)
    assert c.reality_hodge_commutator == sp.zeros(16)
    assert c.conditional_auxiliary_injection.rank() == 8

    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "inherited_weight_obstruction": {
            "fixed_point_dimension": 36,
            "required_auxiliary_weights": list(map(int, c.sigma_weights)),
            "weight_match_rank": 0,
            "intertwiner_constraint_rank_nullity": [288, 0],
            "minimum_extension_dimension": 8,
        },
        "conditional_common_carrier": {
            "carrier": "Sigma tensor C^2",
            "real_dimension": 16,
            "gauge_generator_rank": 16,
            "odd_edge_operator_rank": 16,
            "oriented_incidence_rank": 8,
            "hodge_projector_rank": 8,
            "hodge_projector_inertia_negative_zero_positive": [0, 8, 8],
            "gauge_equivariant": True,
            "Real_compatible": True,
            "exact_Q_readout": True,
        },
        "status": {
            "inherited_admission": "3/6",
            "conditional_admission": "6/6",
            "physical_common_parent": False,
        },
        "proofdsl": {
            "status": "lcf-checked", "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256, "floating_point_values": 0,
        },
        "verdict": {
            "minimal_conditional_carrier_admitted": True,
            "existing_fixed_point_sector_supplies_auxiliary_copy": False,
            "physical_parent_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_origin_candidate_audit_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()