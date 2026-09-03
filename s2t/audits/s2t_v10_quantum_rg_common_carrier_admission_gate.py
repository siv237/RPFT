#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_quantum_rg_common_carrier_admission import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_quantum_rg_common_carrier_admission_gate_results.json"


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/s2t_v9_final_conclusion_and_tome10_program_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = "version10_quantum_rg_common_carrier_admission_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    action = sp.symbols("S_vac", real=True)
    assert sp.simplify(
        certificate.cosmological_curvature
        - sp.Rational(3, 8) * sp.exp(-2 * action) / sp.pi
    ) == 0
    assert certificate.atlas_contrast * certificate.masses == sp.zeros(2, 1)
    assert certificate.carrier_incidence.rank() == 3
    assert sum(certificate.architecture) == 7
    assert sum(certificate.physical_origin) == 0

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "common_carrier": {
            "history": "ell2(N0)",
            "cell_conveyor_dimension": 43,
            "endpoint_kms_dimension": 6,
            "local_field_layer": "F_loc",
            "incidence_rank": 3,
            "incidence_determinant": 2,
        },
        "geometric_growth": {
            "cell_count": "N(tau)=N0*exp(3*h_vac*tau)",
            "scale_factor": "a(tau)=exp(h_vac*tau)=(N/N0)^(1/3)",
            "growth_amplitude": "h_vac=exp(-S_vac)/sqrt(8*pi)",
            "relative_rate_identity": "a'/a=N'/(3N)=h_vac",
            "cosmological_identity": "Lambda_growth=3*h_vac^2=3*exp(-2*S_vac)/(8*pi)",
        },
        "quantum_rg_coordinate": {
            "coordinate": "zeta=log(a)=log(N/N0)/3",
            "beta_definition": "beta_i=dg_i/dzeta",
            "nonzero_beta_derived": False,
        },
        "spectral_atlas": {
            "factorization": "D(zeta)=E_cell(zeta)*D_hat(g(zeta))",
            "ratio_rank": 2,
            "common_scale_preserves_ratios": True,
        },
        "branches": {
            "fixed_cell_addition": "v_cell and E_cell fixed while N grows",
            "codilation": "E_cell=E0/a and a*E_cell=E0",
            "codilation_breaks_scale_orbit": False,
        },
        "status": {
            "architecture_score": "7/7",
            "physical_origin_score": "0/3",
            "growth_law_derived": False,
            "physical_tick_derived": False,
            "local_energy_scale_derived": False,
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "tome10_opened": True,
            "geometric_growth_carrier_admitted": True,
            "static_scale_substitution_used": False,
            "cosmological_constant_physically_derived": False,
        },
        "next_gate": "version10_geometric_scale_beta_trace_anomaly_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()