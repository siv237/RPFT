#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_k43_reciprocal_spectral_operator_growth_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "s2t/results/"
    "s2t_v10_k43_reciprocal_spectral_operator_growth_parent_origin_gate_results.json"
)


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/"
        "s2t_v10_inflow_spectral_self_energy_k43_typed_embedding_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = "version10_k43_reciprocal_spectral_operator_growth_parent_origin_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    zeta = sp.symbols("zeta", real=True)
    assert sp.trace(certificate.growth_grading) == 0
    assert certificate.growth_grading**2 == certificate.support_projector
    assert certificate.growth_grading.rank() == 2
    assert certificate.orientation_scores == sp.ImmutableMatrix([2, -2])
    assert certificate.flow_residual == sp.zeros(43)
    assert certificate.spectral_operator.subs(zeta, 0) == sp.eye(43)
    assert certificate.spectral_operator.det() == 1
    assert certificate.jet_gradient == sp.zeros(4, 1)
    assert certificate.jet_hessian.rank() == 4
    assert certificate.jet_hessian.det() == 1
    assert sum(certificate.architecture) == 9
    assert sum(certificate.spectral_origin) == 4
    assert sum(certificate.physical_origin) == 0

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "growth_grading": {
            "definition": "Q_X=P_0-P_Y",
            "trace": 0,
            "rank": 2,
            "square": "P_0+P_Y",
            "spectrum": {"-1": 1, "0": 41, "1": 1},
            "reciprocal_constraint_nullity": 1,
            "orientation_scores": [2, -2],
        },
        "path_parent": {
            "functional": "1/2||K(0)-I43||_HS^2+1/2 integral ||K'-{Q_X,K}/2||_HS^2 dzeta",
            "bounded_below": True,
            "zero_equations": ["K(0)=I43", "K'={Q_X,K}/2"],
            "unique_zero_path": "K_X(zeta)=exp(zeta Q_X)",
            "closed_form": "I43+(exp(-zeta)-1)P_Y+(exp(zeta)-1)P_0",
            "determinant": "1",
        },
        "local_jet_audit": {
            "variables": ["r_Y", "r_0", "v_Y", "v_0"],
            "stationary_point": [1, 1, -1, 1],
            "minimum": 0,
            "hessian_rank": 4,
            "hessian_determinant": 1,
        },
        "selected_spectral_response": {
            "compression": "diag(exp(-zeta),exp(zeta))",
            "incoming_self_energy": "exp(zeta)",
            "incoming_beta": "Sigma_Y",
        },
        "status": {
            "growth_parent_architecture": "9/9",
            "structural_spectral_law_origin": "4/4",
            "normalized_cell_birth_measure": "0/1",
            "physical_time_energy_calibration": "0/1",
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
            "reciprocal_curve_inserted_as_target": False,
            "reciprocal_curve_selected_by_parent": True,
            "dimensionless_spectral_running_derived": True,
            "cell_birth_probability_derived": False,
            "physical_second_or_energy_derived": False,
        },
        "next_gate": "version10_cell_birth_normalized_transition_measure_growth_rate_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()