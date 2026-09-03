#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin_gate"
    assert predecessor["next_gate"] == gate and SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.stationary_gradient == sp.zeros(2, 1)
    assert certificate.parent_hessian == sp.ImmutableMatrix([[2, -1], [-1, 1]])
    assert certificate.parent_hessian.rank() == 2
    assert certificate.parent_hessian.det() == 1
    assert certificate.scale_map.rank() == 2
    assert len(certificate.scale_map.nullspace()) == 1
    assert certificate.scale_map * certificate.scale_vector == sp.zeros(2, 1)

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "throughflow_inputs": {
            "cycle_affinity": "F=3*log(2)",
            "entropy_production": "sigma=kappa*log(2)",
            "inputs_inherited": "2/2",
        },
        "conditional_parent": {
            "normalized_variables": [
                "s_flow=sigma/(kappa*log(2))",
                "u_Lambda=Lambda*c^2*F^2/(3*sigma^2)",
            ],
            "functional": "((s_flow-1)^2+(u_Lambda-s_flow)^2)/2",
            "selected_point": "s_flow=u_Lambda=1",
            "hessian": [[2, -1], [-1, 1]],
            "hessian_rank": 2,
            "hessian_determinant": 1,
            "bounded_below": True,
        },
        "curvature_response": {
            "entropy_form": "Lambda_flow=3*sigma^2/(c^2*F^2)",
            "conductance_form": "Lambda_flow=kappa^2/(3*c^2)",
            "zero_flow_limit": "kappa=0 => sigma=0 => Lambda_flow=0",
        },
        "remaining_scale_orbit": {
            "variables": ["kappa", "sigma", "Lambda"],
            "map_rank": 2,
            "map_nullity": 1,
            "scale_vector": [1, 1, 2],
            "transformation": "(kappa,sigma,Lambda)->(a*kappa,a*sigma,a^2*Lambda)",
        },
        "origin_boundary": {
            "inherited_sources": ["cycle_affinity", "entropy_production"],
            "new_uninherited_term": "curvature_response_coupling",
            "inherited_origin": "2/3",
        },
        "status": {
            "architecture": "10/10",
            "conditional_origin": "5/5",
            "throughflow_input_origin": "2/2",
            "curvature_coupling_origin": "0/1",
            "physical_cosmological_origin": "0/1",
            "absolute_scale": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "throughflow_supports_conditional_cosmological_curvature": True,
            "curvature_collapses_when_flow_stops": True,
            "existing_parent_derives_curvature_response_coupling": False,
            "throughflow_parent_derives_absolute_Lambda": False,
        },
        "next_gate": "version10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()