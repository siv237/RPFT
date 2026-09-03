#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_inflow_spectral_self_energy_running_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "s2t/results/"
    "s2t_v10_inflow_spectral_self_energy_running_parent_origin_gate_results.json"
)


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/"
        "s2t_v10_geometric_scale_beta_trace_anomaly_origin_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = "version10_inflow_spectral_self_energy_running_parent_origin_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    zeta, q = sp.symbols("zeta q", real=True)
    assert certificate.reservoir_operator.det() == 1
    assert certificate.reservoir_operator * certificate.reservoir_propagator == sp.eye(2)
    assert certificate.incoming_projector + certificate.outgoing_projector == sp.eye(2)
    assert sp.diff(certificate.incoming_self_energy, zeta) == certificate.incoming_self_energy
    assert sp.diff(certificate.outgoing_self_energy, zeta) == -certificate.outgoing_self_energy
    assert sp.simplify(certificate.anomaly_density.subs({zeta: 0, q: 1})) == -sp.Rational(1, 6)
    assert sum(certificate.architecture) == 7
    assert sum(certificate.origin_ledger) == 2

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "reciprocal_reservoir": {
            "operator": "diag(exp(-zeta),exp(zeta))",
            "propagator": "diag(exp(zeta),exp(-zeta))",
            "determinant": "1",
            "incoming_projector_rank": 1,
            "outgoing_projector_rank": 1,
        },
        "oriented_self_energy": {
            "incoming": "Sigma_in=exp(zeta)",
            "outgoing": "Sigma_out=exp(-zeta)",
            "reciprocal_product": "Sigma_in*Sigma_out=1",
            "incoming_beta": "dSigma_in/dzeta=Sigma_in",
            "outgoing_beta": "dSigma_out/dzeta=-Sigma_out",
            "symmetric": "Sigma_sym=cosh(zeta)",
            "symmetric_beta_at_origin": "0",
        },
        "trace_response": {
            "action": "log(1+q^2+exp(zeta))-log(1+q^2)-log(1+exp(zeta))",
            "density": "exp(zeta)/(1+q^2+exp(zeta))-exp(zeta)/(1+exp(zeta))",
            "witness_point": {"q": "1", "zeta": "0"},
            "witness_value": "-1/6",
            "intensive_nonzero_witness": True,
        },
        "origin_ledger": {
            "geometric_reciprocal_scaling": 1,
            "growth_orientation": 1,
            "typed_k43_reservoir_embedding": 0,
            "score": "2/3",
        },
        "status": {
            "oriented_spectral_running_architecture": "7/7",
            "intensive_trace_response_witness": "1/1",
            "typed_physical_reservoir_embedding": "0/1",
            "physical_absolute_scale_parent": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "cell_multiplication_replaced_by_local_spectral_running": True,
            "orientation_is_necessary_for_linear_running": True,
            "nonzero_intensive_response_constructed": True,
            "physical_reservoir_origin_derived": False,
            "absolute_scale_derived": False,
        },
        "next_gate": "version10_inflow_spectral_self_energy_k43_typed_embedding_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()