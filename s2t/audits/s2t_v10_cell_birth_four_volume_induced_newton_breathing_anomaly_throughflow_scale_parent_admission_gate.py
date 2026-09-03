#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_throughflow_scale_parent_admission import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_throughflow_scale_parent_admission_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_throughflow_scale_parent_admission_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.stationary_gradient == sp.zeros(3, 1)
    assert certificate.parent_hessian.rank() == 3
    assert certificate.parent_hessian.det() == 1
    assert certificate.leading_minors == sp.ImmutableMatrix([2, 3, 1])
    assert certificate.scale_map.rank() == 3
    assert certificate.scale_map * certificate.scale_vector == sp.zeros(3, 1)
    assert certificate.externally_anchored_map.rank() == 4

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "normalized_breathing_model": {
            "cell_four_volume": "v_cell=beta_E^2/(4*alpha^2*m^2)",
            "flow_occupancy": "n_flow>=0",
            "injection_density": "d_in=n_flow*log(2)/v_cell=C_flow*m^2",
            "flow_coefficient": "C_flow=4*alpha^2*n_flow*log(2)/beta_E^2",
            "leading_output_density": "d_out^(0)=epsilon*m^2",
        },
        "leading_balance": {
            "equation": "m^2*(C_flow-epsilon)=0",
            "positive_scale_condition": "epsilon=C_flow",
            "absolute_scale_selected": False,
            "reason": "m^2 cancels identically for m>0",
        },
        "logarithmic_anomaly": {
            "output_density": "d_out=epsilon*m^2*(1+b_A*log(m/mu_spec^2))",
            "stationary_log_ratio": "log(m/mu_spec^2)=(C_flow/epsilon-1)/b_A",
            "relative_scale_selected": True,
            "absolute_scale_selected": False,
        },
        "zero_flow_limit": {
            "n_flow_zero_implies_injection_zero": True,
            "positive_m_has_positive_output": True,
            "balanced_nonnegative_endpoint": "m=0",
            "interpretation": "flow-off collapse is admitted conditionally",
        },
        "common_parent": {
            "variables": ["cell-volume relation", "inflow-output balance", "logarithmic relative scale"],
            "hessian": [[2, -1, 0], [-1, 2, -1], [0, -1, 1]],
            "rank": 3,
            "determinant": 1,
            "leading_principal_minors": [2, 3, 1],
        },
        "scale_orbit": {
            "variables": ["m", "mu_spec^2", "v_cell", "density/Theta"],
            "rank": 3,
            "nullity": 1,
            "kernel": [-1, -1, 2, -2],
            "external_reference_scale_row_rank": 4,
        },
        "status": {
            "inherited_origin": "3/3",
            "architecture": "10/10",
            "conditional_origin": "8/8",
            "physical_origin": "0/3",
            "flow_off_collapse": "1/1 conditional",
            "flow_on_absolute_scale": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "hose_metaphor_has_exact_open_system_model": True,
            "leading_balance_selects_scale": False,
            "log_anomaly_selects_relative_scale": True,
            "absolute_vacuum_scale_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_spectral_coefficient_origin_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()