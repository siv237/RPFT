#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_geometric_scale_beta_trace_anomaly_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_geometric_scale_beta_trace_anomaly_origin_gate_results.json"


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/s2t_v10_quantum_rg_common_carrier_admission_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = "version10_geometric_scale_beta_trace_anomaly_origin_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    q = sp.symbols("q", real=True)
    root = sp.sqrt(sp.Rational(1, 2))
    assert certificate.closed_partition == 1
    assert certificate.quadratic_curvature.is_negative is True
    assert certificate.quartic_curvature.is_positive is True
    assert sp.simplify(sp.diff(certificate.witness_potential, q).subs(q, root)) == 0
    assert sp.simplify(
        sp.diff(certificate.witness_potential, q, 2).subs(q, root)
    ) == sp.Rational(37, 24)

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "closed_sector": {
            "physical_operator": "1+q^2",
            "ghost_operator": "1+q^2",
            "combined_partition": "1",
            "effective_action": "0",
        },
        "physical_influx": {
            "shifted_operator": "1+q^2+J",
            "normalized_partition": "(1+J)*(1+q^2)/(1+q^2+J)",
            "effective_action": "log(1+q^2+J)-log(1+q^2)-log(1+J)",
            "origin_curvature": "-2*J/(1+J)",
            "fourth_variation": "12*J*(J+2)/(J+1)^2",
        },
        "broken_phase_witness": {
            "influx": "9/10",
            "positive_saturation": "q^4/4",
            "symmetric_hessian": "-18/19",
            "stationary_points": ["-1/sqrt(2)", "1/sqrt(2)"],
            "broken_hessian": "37/24",
        },
        "geometric_beta_boundary": {
            "extensive_influx": "J_ext=J0*exp(3*zeta)",
            "extensive_beta": "dJ_ext/dzeta=3*J_ext",
            "intensive_influx": "j_int=exp(-3*zeta)*J_ext=J0",
            "intensive_beta": "dj_int/dzeta=0",
            "quantum_trace_anomaly_derived": False,
        },
        "status": {
            "inflow_symmetry_breaking_architecture": "6/6",
            "intensive_quantum_beta": "0/1",
            "physical_reservoir_and_anomaly_origin": "0/2",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "ghost_cancellation_preserved": True,
            "physical_influx_breaks_flatness": True,
            "stable_broken_witness_exists": True,
            "cell_multiplication_alone_generates_quantum_beta": False,
        },
        "next_gate": "version10_inflow_spectral_self_energy_running_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()