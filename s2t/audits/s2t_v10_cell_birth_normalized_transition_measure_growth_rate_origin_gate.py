#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_normalized_transition_measure_growth_rate_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "s2t/results/"
    "s2t_v10_cell_birth_normalized_transition_measure_growth_rate_origin_gate_results.json"
)


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/"
        "s2t_v10_k43_reciprocal_spectral_operator_growth_parent_origin_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = "version10_cell_birth_normalized_transition_measure_growth_rate_origin_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    x = sp.symbols("x", positive=True)
    assert sp.simplify(sum(certificate.probabilities)) == 1
    assert (certificate.transition_matrix * sp.ones(2, 1)).applyfunc(sp.simplify) == sp.ones(2, 1)
    assert certificate.mean_multiplier == (1 + 2 * x) / (1 + x)
    assert sp.diff(certificate.step_growth, x).subs(x, 0) == sp.Rational(1, 3)
    assert certificate.slope_gap.is_positive is True
    assert certificate.clock_orbit_map.rank() == 1
    assert certificate.clock_orbit_map.nullspace() == [sp.Matrix([-1, 1])]
    assert sum(certificate.architecture) == 8
    assert sum(certificate.origin_ledger) == 2

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "binary_birth_measure": {
            "vacuum_weight": "1",
            "birth_weight": "x=exp(-S_vac)",
            "no_birth_probability": "1/(1+x)",
            "birth_probability": "x/(1+x)",
            "probability_sum": "1",
            "odds_ratio": "x",
            "row_stochastic": True,
        },
        "dimensionless_growth": {
            "mean_cell_multiplier": "(1+2*x)/(1+x)",
            "mean_history": "E[N_n]=N0*((1+2*x)/(1+x))^n",
            "zeta_per_step": "log((1+2*x)/(1+x))/3",
            "weak_weight_slope": "1/3",
        },
        "vacuum_amplitude_boundary": {
            "proposed_amplitude": "x/sqrt(8*pi)",
            "proposed_weak_weight_slope": "1/sqrt(8*pi)",
            "slope_gap": "1/3-1/sqrt(8*pi)>0",
            "normalization_derives_proposed_prefactor": False,
        },
        "continuous_clock_boundary": {
            "total_rate": "r_N=gamma*N",
            "waiting_density": "r_N*exp(-r_N*t)",
            "normalization": "1",
            "mean_waiting_time": "1/r_N",
            "scale_orbit": "(gamma,t)->(c*gamma,t/c)",
            "scale_orbit_nullity": 1,
            "physical_gamma_derived": False,
        },
        "status": {
            "minimal_measure_architecture": "8/8",
            "origin_ledger": "2/4",
            "normalized_transition_measure": "1/1 conditional on weights",
            "proposed_vacuum_growth_rate_origin": "0/1",
            "physical_clock_rate": "0/1",
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
            "normalized_birth_measure_constructed": True,
            "dimensionless_mean_growth_constructed": True,
            "normalization_alone_derives_h_vac": False,
            "physical_time_unit_derived": False,
            "cosmological_constant_physically_derived": False,
        },
        "next_gate": "version10_cell_birth_clock_energy_common_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()