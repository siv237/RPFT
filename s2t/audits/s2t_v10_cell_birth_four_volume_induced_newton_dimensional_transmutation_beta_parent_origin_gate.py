#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_scale_seed_candidate_audit_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.landau_log_ratio == 32 * sp.pi**2 / 3
    assert certificate.seed_log_ratio == 64 * sp.pi**2 / 3
    assert certificate.stationary_gradient == sp.zeros(3, 1)
    assert certificate.parent_hessian.rank() == 3
    assert certificate.parent_hessian.det() == 1
    assert certificate.leading_minors == sp.ImmutableMatrix([2, 3, 1])
    assert certificate.scale_map.rank() == 2
    assert certificate.scale_map * certificate.scale_vector == sp.zeros(2, 1)
    assert certificate.externally_anchored_map.rank() == 3

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "inherited_RG_data": {
            "one_loop_beta_coefficient": "b=2",
            "matching_condition": "g^2(mu_spec)=3/8",
            "landau_log_ratio": "log(Lambda_L/mu_spec)=32*pi^2/3",
            "inverse_area_log_ratio": "log(m_DT/mu_spec^2)=64*pi^2/3",
            "physical_character": "ultraviolet_Landau_scale_not_infrared_mass_gap",
        },
        "planck_self_consistency": {
            "condition": "m*g_N=1",
            "einstein_relation": "16*pi*beta_E*m*g_N=1",
            "selected_dimensionless_coefficient": "beta_E=1/(16*pi)",
            "selected_absolute_Newton_constant": False,
        },
        "common_parent": {
            "variables": ["m/(mu_spec^2*exp(64*pi^2/3))", "m*g_N", "16*pi*beta_E*m*g_N"],
            "hessian": [[2, -1, 0], [-1, 2, -1], [0, -1, 1]],
            "rank": 3,
            "determinant": 1,
            "leading_principal_minors": [2, 3, 1],
        },
        "scale_orbit": {
            "variables": ["m", "mu_spec^2", "g_N"],
            "rank": 2,
            "nullity": 1,
            "kernel": [1, 1, -1],
            "external_Newton_area_row_rank": 3,
        },
        "provenance": {
            "historical_RG_data": "2/2",
            "typed_transfer_to_current_carrier": "0/2",
            "Planck_identification_parent_origin": "0/1",
            "RG_boundary_scale_origin": "0/1",
        },
        "status": {
            "architecture": "10/10",
            "conditional_origin": "7/7",
            "physical_origin": "0/4",
            "dimensionless_beta_E_selection": "1/1 conditional",
            "absolute_scale_seed": "0/1",
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
            "inherited_RG_ratio_is_exact": True,
            "positive_beta_generates_IR_Newton_scale": False,
            "Planck_self_consistency_selects_beta_E": True,
            "combined_parent_derives_absolute_G": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_throughflow_scale_parent_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()