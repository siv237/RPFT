#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin_gate"
    assert predecessor["next_gate"] == gate and SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.stationary_gradient == sp.zeros(3, 1)
    assert certificate.parent_hessian == sp.ImmutableMatrix(
        [[2, -1, 0], [-1, 2, -1], [0, -1, 1]]
    )
    assert certificate.parent_hessian.rank() == 3
    assert certificate.parent_hessian.det() == 1
    assert certificate.leading_minors == sp.ImmutableMatrix([2, 3, 1])
    assert certificate.anchor_scale_map.rank() == 1
    assert len(certificate.anchor_scale_map.nullspace()) == 3
    assert certificate.fully_anchored_map.rank() == 4

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "conditional_stress_bridge": {
            "entropy_rate": "sigma=kappa*log(2)",
            "residence_time": "tau_res=1/kappa",
            "energy_density": "rho_flow=Theta*sigma*tau_res/v_cell=Theta*log(2)/v_cell",
            "einstein_response": "Lambda_E=8*pi*G*rho_flow/c^4",
        },
        "conditional_scale_selection": {
            "flow_curvature": "Lambda_flow=kappa^2/(3*c^2)",
            "matching_condition": "Lambda_E=Lambda_flow",
            "selected_conductance_squared": "kappa^2=24*pi*G*Theta*log(2)/(c^2*v_cell)",
        },
        "common_parent": {
            "variables": ["kappa*tau_res", "Lambda/Lambda_E", "Lambda/Lambda_flow"],
            "functional": "((u_tau-1)^2+(u_E-u_tau)^2+(u_match-u_E)^2)/2",
            "selected_point": "u_tau=u_E=u_match=1",
            "hessian": [[2, -1, 0], [-1, 2, -1], [0, -1, 1]],
            "hessian_rank": 3,
            "hessian_determinant": 1,
            "leading_principal_minors": [2, 3, 1],
        },
        "anchor_rank": {
            "variables": ["kappa", "G", "Theta", "v_cell"],
            "conditional_relation_rank": 1,
            "conditional_relation_nullity": 3,
            "rank_after_independent_G_Theta_v": 4,
        },
        "origin_boundary": {
            "inherited": ["cycle_affinity", "entropy_production", "Einstein_response_form"],
            "open": ["physical_G", "independent_Theta", "absolute_v_cell", "typed_stress_tensor_origin"],
            "inherited_origin": "3/7",
            "physical_anchor_package": "0/4",
        },
        "status": {
            "architecture": "10/10",
            "conditional_Einstein_closure": "5/5",
            "inherited_origin": "3/7",
            "physical_anchor_package": "0/4",
            "absolute_conductance": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "Einstein_response_can_conditionally_select_conductance": True,
            "entropy_rate_alone_is_stress_energy": False,
            "current_project_derives_required_anchor_package": False,
            "absolute_conductance_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_einstein_response_anchor_package_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()