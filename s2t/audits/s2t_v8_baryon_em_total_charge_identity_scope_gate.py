#!/usr/bin/env python3
"""Exact scope audit for the baryon total-charge electromagnetic identity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_em_total_charge_identity_scope_gate_results.json"


def main() -> None:
    x = sp.symbols("x", positive=True)
    mu, lam = sp.symbols("mu lam", real=True)
    up = sp.Rational(2, 3)
    down = -sp.Rational(1, 3)

    triples = []
    identity_exact = True
    for bits in range(8):
        charges = [down if (bits >> place) & 1 else up for place in range(3)]
        total = sum(charges)
        self_part = sum(charge**2 for charge in charges)
        pair_part = sum(
            charges[i] * charges[j]
            for i in range(3)
            for j in range(3)
            if i != j
        )
        identity_exact &= sp.expand(self_part + pair_part - total**2) == 0
        triples.append(
            {
                "down_count": sum(1 for charge in charges if charge == down),
                "total_charge": str(total),
                "self": str(self_part),
                "ordered_pair": str(pair_part),
                "total_square": str(total**2),
            }
        )

    by_down_count = {}
    for item in triples:
        by_down_count[item["down_count"]] = item

    equations = []
    for item in by_down_count.values():
        equations.append(
            sp.Eq(
                mu * sp.sympify(item["self"]) + lam * sp.sympify(item["ordered_pair"]),
                sp.sympify(item["total_square"]),
            )
        )
    coefficient_solution = sp.solve(equations, (mu, lam), dict=True)

    proton = by_down_count[1]
    neutron = by_down_count[2]
    proton_energy = sp.factor(mu * sp.sympify(proton["self"]) + lam * sp.sympify(proton["ordered_pair"]))
    neutron_energy = sp.factor(mu * sp.sympify(neutron["self"]) + lam * sp.sympify(neutron["ordered_pair"]))
    neutron_minus_proton = sp.factor(neutron_energy - proton_energy)

    a = 1 / (11 + 10 * x)
    b = x / (11 + 10 * x)
    trace_norm = sp.factor(sp.Rational(14, 3) * (a + b))
    expected_trace_norm = sp.factor(14 * (1 + x) / (3 * (11 + 10 * x)))

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_em_total_charge_identity_scope_gate",
        "field": "Q(x,mu,lambda), x=exp(-2)",
        "charge_operator": {
            "up": "2/3",
            "down": "-1/3",
            "identity_A_plus_C_equals_Q_total_squared_exact_on_216_states": identity_exact,
            "epsilon_sector_by_down_count": by_down_count,
            "total_square_pattern": ["4", "1", "0", "1"],
        },
        "common_trace_normalization": {
            "source_charge_square_trace": "14/3",
            "target_charge_square_trace": "14/3",
            "T": str(trace_norm),
            "closed_form_identity_exact": sp.simplify(trace_norm - expected_trace_norm) == 0,
            "absolute_energy_scale_derived": False,
        },
        "general_permutation_invariant_electrostatic_form": {
            "energy": "mu*A+lambda*C",
            "collapse_to_total_charge_square_solution": [
                {str(key): str(value) for key, value in solution.items()}
                for solution in coefficient_solution
            ],
            "unique_collapse_requires_mu_lambda_one": coefficient_solution == [{lam: 1, mu: 1}],
            "spatial_pair_coefficients_derived": False,
            "dipole_and_magnetic_terms_derived_zero": False,
        },
        "neutron_proton_sign": {
            "proton_energy": str(proton_energy),
            "neutron_energy": str(neutron_energy),
            "neutron_minus_proton": str(neutron_minus_proton),
            "negative_for_mu_lambda_positive": True,
            "parameter_free_sign_from_charge_identity_alone": False,
        },
        "status_boundary": {
            "algebraic_charge_identity": True,
            "pointlike_equal_kernel_model_lemma": True,
            "canonical_electromagnetic_hamiltonian_derived": False,
            "spatial_electromagnetic_kernel_derived": False,
            "magnetic_hyperfine_terms_included": False,
            "physical_mass_theorem": False,
        },
        "verdict": {
            "accept_total_charge_identity": True,
            "reject_identity_as_universal_em_energy_theorem": True,
            "sign_status": "conditional_on_positive_self_and_pair_coefficients_and_absent_extra_terms",
            "next_gate": "version8_baryon_em_spatial_kernel_origin_gate",
        },
    }

    assert identity_exact
    assert coefficient_solution == [{lam: 1, mu: 1}]
    assert sp.simplify(neutron_minus_proton + (mu + 2 * lam) / 3) == 0
    assert sp.simplify(trace_norm - expected_trace_norm) == 0
    assert [by_down_count[n]["total_square"] for n in range(4)] == ["4", "1", "0", "1"]

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()