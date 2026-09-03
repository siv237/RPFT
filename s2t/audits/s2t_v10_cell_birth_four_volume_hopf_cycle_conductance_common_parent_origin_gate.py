#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_hopf_cycle_conductance_common_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_hopf_cycle_conductance_common_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_hopf_cycle_k43_kms_product_embedding_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_hopf_cycle_conductance_common_parent_origin_gate"
    assert predecessor["next_gate"] == gate and SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.stationary_gradient == sp.zeros(2, 1)
    assert certificate.parent_hessian == sp.ImmutableMatrix([[2, -1], [-1, 1]])
    assert certificate.parent_hessian.rank() == 2
    assert certificate.parent_hessian.det() == 1
    assert certificate.scale_constraint_map.rank() == 2
    assert certificate.scale_constraint_map.nullspace() == [sp.ones(3, 1)]

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "common_parent": {
            "variables": ["Gamma_B/Omega", "kappa/Omega"],
            "functional": "((r_B-k_X)^2+(r_kappa-r_B)^2)/2",
            "selected_point": "r_B=r_kappa=k_X",
            "hessian": [[2, -1], [-1, 1]],
            "hessian_rank": 2,
            "hessian_determinant": 1,
            "bounded_below": True,
        },
        "selected_relations": {
            "growth_coupling": "k_X=log((1+2*x)/(1+x))=3*Delta_zeta",
            "conductance": "kappa=Gamma_B=k_X*Omega",
            "edge_current_clock_ratio": "J_edge/Omega=Delta_zeta",
            "entropy_clock_ratio": "sigma/Omega=3*Delta_zeta*log(2)",
        },
        "remaining_scale_orbit": {
            "transformation": "(kappa,Gamma_B,Omega)->c*(kappa,Gamma_B,Omega), t->t/c",
            "constraint_map_rank": 2,
            "constraint_map_nullity": 1,
            "kernel": [1, 1, 1],
            "absolute_conductance_derived": False,
            "absolute_clock_derived": False,
        },
        "status": {
            "architecture": "10/10",
            "relative_origin": "6/6",
            "common_parent_origin": "1/1",
            "blind_dimensionless_relations": "2/2",
            "absolute_conductance": "0/1",
            "absolute_clock": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "common_parent_selects_conductance_relative_to_clock": True,
            "cycle_conductance_is_identified_with_cell_birth_rate": True,
            "edge_current_matches_geometric_growth_per_clock": True,
            "common_parent_selects_absolute_conductance": False,
        },
        "next_gate": "version10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()