#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_output_density_morphism_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_output_density_morphism_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_spectral_coefficient_origin_candidate_audit_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_output_density_morphism_origin_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.sign_admissibility == sp.ImmutableMatrix([0, 1])
    assert certificate.stationary_gradient == sp.zeros(3, 1)
    assert certificate.parent_hessian.rank() == 3
    assert certificate.parent_hessian.det() == 1
    assert certificate.leading_minors == sp.ImmutableMatrix([2, 3, 1])
    assert certificate.scale_map.rank() == 3
    assert certificate.scale_map * certificate.scale_vector == sp.zeros(3, 1)
    assert certificate.externally_anchored_map.rank() == 4

    result = {
        "date": "2026-09-02",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "oriented_trace_response": {
            "x_definition": "x=exp(zeta)>0",
            "response": "A=-x*q^2/((1+x)*(1+q^2+x))",
            "output_fraction": "R_out=-A=x*q^2/((1+x)*(1+q^2+x))",
            "range": "0<R_out<1 for x>0 and q>0",
            "canonical_witness": "R_out(1,1)=1/6",
        },
        "sign_selection": {
            "candidates": ["A", "-A"],
            "positivity_admissibility": [0, 1],
            "selected_map": "R_out=-A",
            "selection_character": "conditional positivity selection",
        },
        "density_morphism": {
            "cell_four_volume": "v_cell=beta_E^2/(4*alpha^2*m^2)",
            "output_density": "d_out=R_out/v_cell=epsilon_K43*m^2",
            "effective_coefficient": "epsilon_K43=4*alpha^2*R_out/beta_E^2",
            "canonical_witness_coefficient": "epsilon_K43=2*alpha^2/(3*beta_E^2)",
        },
        "throughflow_balance": {
            "inflow_density": "d_in=n_flow*log(2)/v_cell",
            "residual": "d_in-d_out=4*alpha^2*m^2*(n_flow*log(2)-R_out)/beta_E^2",
            "dimensionless_stationarity": "n_flow*log(2)=R_out",
            "absolute_scale_selected": False,
        },
        "common_parent": {
            "variables": ["trace-response sign", "per-cell to density morphism", "inflow-output balance"],
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
            "inherited_origin": "4/4",
            "architecture": "10/10",
            "conditional_origin": "8/8",
            "positive_output_morphism": "1/1 conditional",
            "physical_channel_identity": "0/1",
            "physical_coefficient_and_scale_origin": "0/2",
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
            "positive_subunit_K43_output_map_exists": True,
            "leading_epsilon_conditionally_constructed": True,
            "map_is_derived_physical_open_system_flux": False,
            "absolute_breathing_scale_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()