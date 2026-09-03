#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_suspension_auxiliary_copy_parent_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_suspension_auxiliary_copy_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_origin_candidate_audit_gate_results.json"
        ).read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.bare_dynamical_injection.rank() == 0
    assert c.thom_differential**2 == sp.zeros(16)
    assert c.thom_differential.rank() == 8
    assert c.thom_boson_injection.rank() == 8
    assert c.relative_boson_image.rank() == 8
    assert c.gaussian_hessian.rank() == 14
    assert c.effective_hessian == sp.diag(40, 40, 0, 48, 48, 0, 40, 40)
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "suspension": {
            "carrier_dimension": 16,
            "edge_rank": c.suspension_edge.rank(),
            "grading_odd": True,
            "gauge_equivariant": True,
            "real_equivariant": True,
            "independent_dynamical_injection_rank": 0,
            "interpretation": "graded stabilization, not yet a field origin",
        },
        "mathai_quillen_completion": {
            "thom_pair_dimension": 16,
            "nilpotent_differential_rank": c.thom_differential.rank(),
            "cohomology_dimension": 0,
            "independent_boson_rank": c.thom_boson_injection.rank(),
            "relative_image_rank": c.relative_boson_image.rank(),
            "section_rank": c.section_operator.rank(),
            "section_jacobian": int(c.fermionic_jacobian),
            "jacobian_field_independent_at_fixed_Q": True,
        },
        "gaussian_elimination": {
            "joint_hessian_rank": c.gaussian_hessian.rank(),
            "joint_hessian_nullity": 16 - c.gaussian_hessian.rank(),
            "schur_complement_diagonal": list(map(int, c.effective_hessian.diagonal())),
            "schur_complement_rank": c.effective_hessian.rank(),
            "schur_complement_inertia": [0, 2, 6],
        },
        "criteria": [
            "exact_type",
            "independent_boson",
            "nilpotent_pair",
            "positive_metric",
            "exact_Q_section",
            "inherited_origin",
            "no_new_on_shell_boson",
        ],
        "status": {
            "bare_suspension": list(map(int, c.bare_status)),
            "bare_score": "3/7",
            "conditional_thom_completion": list(map(int, c.thom_status)),
            "conditional_score": "6/7",
            "remaining_slot": "inherited cohomological differential and full measure",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "bare_suspension_is_physical_auxiliary_origin": False,
            "mathai_quillen_completion_is_exact_conditionally": True,
            "physical_parent_found": False,
            "best_route_sharpened": True,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_thom_multiplet_common_parent_origin_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()