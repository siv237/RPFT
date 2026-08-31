#!/usr/bin/env python3
"""Exact minimal Hamiltonian data for a singlet--triplet central weight."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_weight_minimal_hamiltonian_data_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_trace_weight_parent_origin_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_weight_minimal_hamiltonian_data_gate"

    theta = sp.symbols("theta", real=True)
    p = sp.symbols("p", positive=True)
    q = sp.symbols("q", positive=True)
    beta = sp.symbols("beta", positive=True)
    delta = sp.symbols("Delta", real=True)
    epsilon = sp.symbols("epsilon", real=True)

    p1 = sp.diag(1, 0, 0, 0)
    p3 = sp.diag(0, 1, 1, 1)
    h = epsilon * sp.eye(4) + delta * p3
    theta_definition = beta * delta
    p_theta = sp.simplify(1 / (1 + 3 * sp.exp(-theta)))
    r_theta = sp.exp(-theta)
    rho_theta = p_theta * p1 + (1 - p_theta) * p3 / 3
    assert sp.trace(rho_theta) == 1
    assert sp.simplify(rho_theta[1, 1] / rho_theta[0, 0] - r_theta) == 0

    inverse_theta = sp.log(3 * p / (1 - p))
    assert sp.simplify(p_theta.subs(theta, inverse_theta) - p) == 0
    derivative = sp.simplify(sp.diff(p_theta, theta))
    assert sp.simplify(derivative - p_theta * (1 - p_theta)) == 0

    assert p_theta.subs(theta, 0) == sp.Rational(1, 4)
    assert sp.simplify(p_theta.subs(theta, sp.log(3))) == sp.Rational(1, 2)

    entropy = -p * sp.log(p) - (1 - p) * sp.log((1 - p) / 3)
    free_energy = sp.simplify((1 - p) * theta - entropy)
    free_energy_prime = sp.simplify(sp.diff(free_energy, p))
    free_energy_second = sp.simplify(sp.diff(free_energy, p, 2))
    assert free_energy_prime == -theta + sp.log(p) - sp.log((1 - p) / 3)
    assert sp.simplify(free_energy_second - 1 / (p * (1 - p))) == 0
    assert sp.simplify(free_energy_prime.subs(p, p_theta)) == 0
    equilibrium_free_energy = sp.simplify(free_energy.subs(p, p_theta))
    assert sp.simplify(equilibrium_free_energy + sp.log(1 + 3 * sp.exp(-theta))) == 0

    theta_q = sp.log(3 * q / (1 - q))
    relative_entropy = p * sp.log(p / q) + (1 - p) * sp.log((1 - p) / (1 - q))
    variational_difference = sp.expand_log(
        free_energy.subs(theta, theta_q) - free_energy.subs({p: q, theta: theta_q}),
        force=True,
    )
    assert sp.simplify(sp.expand_log(variational_difference - relative_entropy, force=True)) == 0

    scale = sp.symbols("a", positive=True)
    assert sp.simplify((beta / scale) * (scale * delta) - theta_definition) == 0

    fisher = sp.simplify(derivative)
    assert sp.simplify(fisher.subs(theta, 0) - sp.Rational(3, 16)) == 0
    assert sp.simplify(fisher.subs(theta, sp.log(3)) - sp.Rational(1, 4)) == 0

    exact_objects = [p1, p3, h, rho_theta]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_singlet_triplet_central_weight_minimal_hamiltonian_data_gate",
        "admissible_hamiltonian": {
            "form": "epsilon I4 + Delta P3",
            "spectral_type": "1 + 3",
            "additive_shift_relevant": False,
            "selector_quotient_dimension": 1,
        },
        "minimal_dimensionless_selector": {
            "theta": "beta Delta",
            "weight": "p(theta)=1/(1+3 exp(-theta))",
            "relative_rate": "r(theta)=exp(-theta)",
            "inverse": "theta=log(3p/(1-p))",
            "bijection": "R to (0,1)",
            "derivative": "p(1-p)>0",
        },
        "exact_witnesses": {
            "degenerate_levels": {"theta": 0, "p": "1/4", "relative_rate": 1},
            "equal_sector_weight": {"theta": "log(3)", "p": "1/2", "relative_rate": "1/3"},
        },
        "gibbs_variational_identity": {
            "dimensionless_functional": "Phi_theta(p)=(1-p)theta-S(p)",
            "first_derivative": "log(3p/(1-p))-theta",
            "second_derivative": "1/(p(1-p))>0",
            "minimum": "-log(1+3 exp(-theta))",
            "excess": "D(rho_p || rho_p_theta)",
            "unique_minimizer": True,
        },
        "identifiability": {
            "equilibrium_determines_beta_Delta_only": True,
            "beta_and_Delta_separately_determined": False,
            "scaling_orbit": "(beta,Delta) -> (beta/a,a Delta)",
            "relaxation_rate_determined": False,
        },
        "data_layers": {
            "central_weight": "theta=beta Delta",
            "physical_energy_or_temperature": "one absolute member of {beta,Delta}",
            "relaxation_time": "independent bath spectral scale",
        },
        "verdict": {
            "minimal_selector_data_dimension": 1,
            "minimal_selector_is_theta": True,
            "theta_derived_by_current_parent": False,
            "derived_selector_data": 0,
            "required_selector_data": 1,
            "physical_single_c0_map_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_parent_action_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()