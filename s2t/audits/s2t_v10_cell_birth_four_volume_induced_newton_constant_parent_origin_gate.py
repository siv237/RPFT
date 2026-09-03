#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_constant_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_constant_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_einstein_response_anchor_package_candidate_audit_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_induced_newton_constant_parent_origin_gate"
    assert predecessor["next_gate"] == gate and SPEC.identifier == gate
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.stationary_gradient == sp.zeros(3, 1)
    assert certificate.parent_hessian.rank() == 3
    assert certificate.parent_hessian.det() == 1
    assert certificate.leading_minors == sp.ImmutableMatrix([2, 3, 1])
    assert certificate.scale_map.rank() == 3
    assert certificate.scale_map.nullspace() == [sp.Matrix([1, -1, -1, 1])]

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "einstein_normalization": {
            "geometric_Newton_area": "g_N=hbar*G/c^3",
            "coefficient_relation": "16*pi*g_N*B=1",
            "physical_Newton_constant": "G=c^3/(16*pi*hbar*B)",
        },
        "induced_relations": {
            "Einstein_coefficient": "B=beta*m",
            "cell_scale_squared": "q=beta/(2*alpha*m)",
            "geometric_Newton_area": "g_N=1/(16*pi*beta*m)",
            "blind_ratio": "g_N/q=alpha/(8*pi*beta^2)",
        },
        "common_parent": {
            "variables": ["16*pi*g_N*B", "B/(beta*m)", "2*alpha*q*m/beta"],
            "hessian": [[2, -1, 0], [-1, 2, -1], [0, -1, 1]],
            "hessian_rank": 3,
            "hessian_determinant": 1,
            "leading_principal_minors": [2, 3, 1],
        },
        "scale_orbit": {
            "variables": ["g_N", "B", "m", "q"],
            "map_rank": 3,
            "map_nullity": 1,
            "kernel": [1, -1, -1, 1],
            "transformation": "(g_N,B,m,q)->(s^2*g_N,B/s^2,m/s^2,s^2*q)",
        },
        "status": {
            "architecture": "10/10",
            "relative_origin": "6/6",
            "Einstein_normalization": "1/1",
            "blind_Newton_cell_ratio": "1/1",
            "seed_origin": "0/1",
            "coefficient_origin": "0/1",
            "absolute_Newton_constant": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "Einstein_coefficient_defines_Newton_area_relatively": True,
            "Newton_to_cell_area_ratio_is_scale_free": True,
            "induced_coefficient_derives_absolute_G": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_scale_seed_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()