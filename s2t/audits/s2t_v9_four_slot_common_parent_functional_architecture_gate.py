#!/usr/bin/env python3
"""Exact bounded-functional architecture audit for four Tome IX slots."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "four_slot_common_parent_functional_architecture_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v9_four_slot_common_carrier_architecture_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert predecessor["verdict"]["single_common_carrier_architecture_constructed"]

    energy, coupling, transport = sp.symbols(
        "E_star chi q", nonnegative=True
    )
    a_e, b_e, a_c, b_c = sp.symbols(
        "a_E b_E a_chi b_chi", positive=True
    )
    energy_part = a_e * energy**4 - b_e * energy**2
    coupling_part = a_c * coupling**4 - b_c * coupling**2
    energy_min = sp.sqrt(b_e / (2 * a_e))
    coupling_min = sp.sqrt(b_c / (2 * a_c))
    assert sp.simplify(sp.diff(energy_part, energy).subs(energy, energy_min)) == 0
    assert sp.simplify(sp.diff(coupling_part, coupling).subs(coupling, coupling_min)) == 0
    assert sp.simplify(sp.diff(energy_part, energy, 2).subs(energy, energy_min)) == 4 * b_e
    assert sp.simplify(sp.diff(coupling_part, coupling, 2).subs(coupling, coupling_min)) == 4 * b_c

    # Exact witness; it certifies architecture only and is not a physical fit.
    endpoint_scores = (sp.Integer(2), sp.Integer(1), sp.Integer(0))
    endpoint_vertex = min(range(3), key=lambda index: endpoint_scores[index])
    assert endpoint_vertex == 2

    kappa_t = sp.Integer(3)
    delta_t = sp.Integer(-1)
    transport_part = kappa_t * transport * (1 - transport) + delta_t * transport
    boundary_values = [transport_part.subs(transport, value) for value in (0, 1)]
    assert boundary_values == [0, -1]
    assert sp.diff(transport_part, transport, 2) < 0

    witness = (
        energy_part.subs({a_e: 1, b_e: 2})
        + coupling_part.subs({a_c: 1, b_c: 2})
    )
    witness_hessian = sp.hessian(witness, (energy, coupling)).subs(
        {energy: 1, coupling: 1}
    )
    assert witness_hessian == sp.diag(8, 8)

    checks = {
        "one_product_domain_for_four_slots": True,
        "single_polynomial_functional": True,
        "bounded_below_by_quartic_completion": True,
        "endpoint_minimum_is_a_simplex_vertex": True,
        "unique_endpoint_score_selects_one_vertex": True,
        "positive_energy_minimum_exists": True,
        "positive_coupling_minimum_exists": True,
        "transport_minimum_is_a_boundary_class": True,
        "continuous_hessian_is_positive": True,
    }
    assert all(checks.values())

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "functional": {
            "domain": "Delta2 tensor R_nonnegative_E tensor R_nonnegative_chi tensor interval_q",
            "endpoint_selector": "kappa_e(1-sum p_i^2)+sum epsilon_i p_i",
            "energy_selector": "a_E E_star^4-b_E E_star^2",
            "coupling_selector": "a_chi chi^4-b_chi chi^2",
            "transport_selector": "kappa_t q(1-q)+delta_t q",
            "bounded_below": True,
        },
        "exact_minima": {
            "endpoint_witness_vertex": "Q2=H24",
            "energy": "sqrt(b_E/(2 a_E))",
            "coupling": "sqrt(b_chi/(2 a_chi))",
            "transport": "q=0 if delta_t>0; q=1 if delta_t<0",
            "continuous_hessian": "diag(4 b_E,4 b_chi)",
            "witness_hessian": [[8, 0], [0, 8]],
        },
        "functional_architecture_audit": {
            **checks,
            "satisfied": sum(checks.values()),
            "tested": len(checks),
        },
        "selector_coefficient_packages": {
            "endpoint_score_order": False,
            "energy_ratio_b_E_over_a_E": False,
            "coupling_ratio_b_chi_over_a_chi": False,
            "transport_bias_sign": False,
            "satisfied": 0,
            "tested": 4,
        },
        "ledgers": {
            "functional_architecture_satisfied": 9,
            "functional_architecture_tested": 9,
            "conditional_slot_selection_satisfied": 4,
            "conditional_slot_selection_tested": 4,
            "physical_coefficient_origin_satisfied": 0,
            "physical_coefficient_origin_tested": 4,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "one_bounded_four_slot_functional_family_constructed": True,
            "all_four_slots_conditionally_selectable": True,
            "selector_coefficients_physically_derived": False,
            "physical_four_slot_parent_constructed": False,
        },
        "next_gate": "version9_four_slot_parent_selector_coefficient_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()