#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_thom_multiplet_common_parent_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_thom_multiplet_common_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_suspension_auxiliary_copy_parent_origin_gate_results.json"
        ).read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.oriented_edge**2 == sp.zeros(16)
    assert c.oriented_edge.rank() == 8
    assert c.thom_differential**2 == sp.zeros(32)
    assert c.thom_differential.rank() == 16
    assert c.inherited_field_injection.rank() == 8
    assert c.conditional_bosonic_injection.rank() == 16
    assert c.inherited_odd_injection.rank() == 0
    assert c.normalized_measure_ratio == 1
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "carrier_origin": {
            "suspension_swap_from_hodge": True,
            "oriented_edge_rank": c.oriented_edge.rank(),
            "oriented_edge_nilpotent": True,
            "carrier_differential_derived_conditionally": True,
        },
        "full_thom_quartet": {
            "fields": ["Sigma_boson", "psi_Sigma_odd", "chi_Sigma_odd", "H_Sigma_boson"],
            "real_dimension": 32,
            "differential_rank": c.thom_differential.rank(),
            "cohomology_dimension": 0,
            "gauge_equivariant": True,
            "real_equivariant": True,
            "field_parity_odd": True,
        },
        "measure": {
            "bosonic_hessian_rank": c.bosonic_hessian.rank(),
            "bosonic_hessian_inertia": [0, 0, 16],
            "bosonic_determinant": int(c.bosonic_determinant),
            "fermionic_determinant": int(c.fermionic_determinant),
            "bosonic_equals_fermionic_square": True,
            "normalized_determinant_ratio": int(c.normalized_measure_ratio),
        },
        "inherited_field_ledger": {
            "required_real_directions": 32,
            "inherited_physical_Sigma_rank": c.inherited_field_injection.rank(),
            "conditional_bosonic_rank": c.conditional_bosonic_injection.rank(),
            "inherited_odd_rank": c.inherited_odd_injection.rank(),
            "missing_odd_directions": 16,
        },
        "criteria": [
            "exact_Q_section",
            "carrier_differential",
            "full_quartet",
            "odd_statistics",
            "positive_measure",
            "determinant_cancellation",
            "inherited_origin",
            "zero_on_shell_cohomology",
        ],
        "status": {
            "conditional": list(map(int, c.conditional_status)),
            "conditional_score": "7/8",
            "inherited": list(map(int, c.inherited_status)),
            "inherited_score": "3/8",
            "remaining_slot": "origin of the two odd Thom fields and their Berezin measure",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "oriented_hodge_edge_derives_carrier_differential": True,
            "full_mathai_quillen_parent_exists_conditionally": True,
            "current_parent_contains_required_odd_fields": False,
            "physical_parent_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_odd_pair_statistics_candidate_audit_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()