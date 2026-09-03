#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_clock_energy_common_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "s2t/results/"
    "s2t_v10_cell_birth_clock_energy_common_parent_origin_gate_results.json"
)


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/"
        "s2t_v10_cell_birth_normalized_transition_measure_growth_rate_origin_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = "version10_cell_birth_clock_energy_common_parent_origin_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    x = sp.symbols("x", positive=True)
    expected_coupling = sp.log((1 + 2 * x) / (1 + x))
    assert certificate.bare_hamiltonian.eigenvals() == {0: 1, 1: 2, 2: 1}
    assert certificate.bare_hamiltonian * certificate.exchange_generator == (
        certificate.exchange_generator * certificate.bare_hamiltonian
    )
    assert certificate.exchange_generator.rank() == 2
    assert certificate.exchange_generator.eigenvals() == {-1: 1, 0: 2, 1: 1}
    assert certificate.growth_coupling == expected_coupling
    assert certificate.growth_coupling.is_positive is True
    assert certificate.stationary_gradient == sp.zeros(2, 1)
    assert certificate.parent_hessian == sp.ImmutableMatrix([[2, -1], [-1, 1]])
    assert certificate.parent_hessian.rank() == 2
    assert certificate.parent_hessian.det() == 1
    assert certificate.scale_orbit_map.nullspace() == [sp.Matrix([-1, 1])]
    assert sum(certificate.architecture) == 9
    assert sum(certificate.relative_origin) == 3

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "birth_clock_carrier": {
            "dimension": 4,
            "bare_hamiltonian": "N_B tensor I + I tensor N_C",
            "bare_spectrum": {"0": 1, "1": 2, "2": 1},
            "resonant_pair": ["|N,1_C>", "|N+1,0_C>"],
            "exchange_rank": 2,
            "exchange_spectrum": {"-1": 1, "0": 2, "1": 1},
            "energy_commutator": "[H_0,G_B]=0",
        },
        "normalized_growth_input": {
            "x": "exp(-S_vac)",
            "growth_coupling": "k_X=log((1+2*x)/(1+x))=3*Delta_zeta",
            "positive_for_x": "x>0",
        },
        "common_parent": {
            "variables": ["u=chi^2", "rho=Gamma_B/Omega"],
            "functional": "P_BC=((u-k_X)^2+(rho-u)^2)/2",
            "unique_zero": "u=rho=k_X",
            "hessian": [[2, -1], [-1, 1]],
            "hessian_rank": 2,
            "hessian_determinant": 1,
            "hessian_spectrum": ["(3-sqrt(5))/2", "(3+sqrt(5))/2"],
        },
        "relative_physical_calibration": {
            "clock_frequency": "Omega=E_C/hbar",
            "birth_rate": "Gamma_B=k_X*E_C/hbar",
            "growth_rate": "H_B=Gamma_B/3=Delta_zeta*E_C/hbar",
            "relative_growth": "H_B/Omega=Delta_zeta",
        },
        "absolute_scale_boundary": {
            "scale_orbit": "(E_C,t)->(c*E_C,t/c)",
            "scale_orbit_nullity": 1,
            "proposed_target": "h_vac=x/sqrt(8*pi)",
            "required_clock_frequency": (
                "Omega_req=3*x/(sqrt(8*pi)*log((1+2*x)/(1+x)))"
            ),
            "clock_energy_selected": False,
            "absolute_growth_rate_selected": False,
        },
        "status": {
            "common_parent_architecture": "9/9",
            "relative_origin": "3/3",
            "clock_energy_and_absolute_growth": "0/2",
            "physical_cosmological_constant": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "common_relative_parent_constructed": True,
            "energy_conserving_birth_clock_exchange_constructed": True,
            "clock_blind_growth_ratio_derived": True,
            "physical_clock_energy_derived": False,
            "absolute_cosmological_rate_derived": False,
        },
        "next_gate": (
            "version10_cell_birth_clock_energy_geometric_anchor_candidate_audit_gate"
        ),
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()