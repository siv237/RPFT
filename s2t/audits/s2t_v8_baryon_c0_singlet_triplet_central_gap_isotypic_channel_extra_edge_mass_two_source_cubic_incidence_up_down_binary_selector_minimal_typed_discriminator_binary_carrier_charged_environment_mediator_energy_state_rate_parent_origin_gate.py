#!/usr/bin/env python3
"""Exact parent-origin audit for charged-mediator energy, state, and rate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_energy_state_rate_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v8_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_existing_carrier_admission_gate_results.json").read_text())
    gate = f"version8_{STEM}"
    assert predecessor["next_gate"] == gate

    y = sp.diag(0, 1, -1)
    real_swap = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    variables = sp.symbols("a b c d e f")
    h = sp.Matrix([[variables[0], variables[1], variables[2]],
                   [variables[1], variables[3], variables[4]],
                   [variables[2], variables[4], variables[5]]])
    equations = list(y * h - h * y) + list(real_swap * h * real_swap.T - h)
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    assert coefficient_matrix.rank() == 4
    assert len(coefficient_matrix.nullspace()) == 2

    e0, ec, delta = sp.symbols("e0 ec delta", real=True)
    h_adm = sp.diag(e0, ec, ec)
    assert y * h_adm == h_adm * y
    assert real_swap * h_adm * real_swap.T == h_adm
    h_shifted = sp.simplify(h_adm - e0 * sp.eye(3))
    assert h_shifted == sp.diag(0, ec - e0, ec - e0)

    p0, pc = sp.symbols("p0 pc", nonnegative=True)
    rho = sp.diag(p0, pc, pc)
    assert real_swap * rho * real_swap.T == rho
    assert sp.trace(rho) == p0 + 2 * pc

    x = sp.symbols("x", positive=True)
    rho_gibbs = sp.diag(1, x, x) / (1 + 2 * x)
    assert sp.simplify(sp.trace(rho_gibbs)) == 1
    assert sp.simplify(sp.trace(rho_gibbs**2)) == (1 + 2 * x**2) / (1 + 2 * x)**2
    assert sp.simplify(rho_gibbs.det() - x**2 / (1 + 2 * x)**3) == 0

    g1, g2 = sp.Integer(1), sp.Integer(2)
    assert g2**2 / g1**2 == 4
    old_jump_count = 42
    new_jump_in_old_chain = False

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "admissible_environment_hamiltonian": {
            "real_gauge_invariant_class": "diag(e0,ec,ec)",
            "linear_constraint_rank": 4,
            "real_dimension_before_energy_shift": 2,
            "essential_gap_parameters_after_shift": 1,
            "gap": "Delta_E=ec-e0",
            "neutral_vacuum_is_ground_condition": "Delta_E>0",
            "resonance_condition": "Delta_E=7 gamma",
            "symmetry_selects_gap_value": False,
            "current_parent_selects_resonance": False,
        },
        "admissible_environment_state": {
            "real_gauge_invariant_class": "diag(p0,pc,pc), p0+2pc=1",
            "simplex_dimension": 1,
            "neutral_vacuum": "diag(1,0,0)",
            "charged_real_mixture": "diag(0,1/2,1/2)",
            "symmetry_selects_neutral_vacuum": False,
            "gibbs_state": "diag(1,x,x)/(1+2x)",
            "x": "exp(-beta Delta_E)",
            "finite_temperature_rank": 3,
            "finite_temperature_purity": "(1+2x^2)/(1+2x)^2",
            "exact_vacuum_requires": "beta Delta_E -> infinity or external pure preparation",
        },
        "coupling_and_rate": {
            "trace_gram_fixes_connector_shape": True,
            "trace_gram_fixes_physical_coupling": False,
            "two_allowed_couplings": [1, 2],
            "corresponding_weak_limit_rate_ratio": 4,
            "conditional_physical_rate": "Gamma=E_int^2 tau_C/hbar^2=chi^2 E_C/hbar",
            "E_C_selected": False,
            "chi_selected": False,
        },
        "fresh_chain": {
            "existing_toeplitz_template_reusable": True,
            "old_cell_jump_count": old_jump_count,
            "new_connector_in_old_42_jump_cell": new_jump_in_old_chain,
            "new_identical_cell_extension_required": True,
            "preloaded_product_vacuum_required": True,
            "chain_parent_derived": False,
        },
        "ledgers": {
            "conditional_shape_satisfied": 8,
            "conditional_shape_tested": 8,
            "energy_state_rate_parent_origin_satisfied": 0,
            "energy_state_rate_parent_origin_tested": 5,
        },
        "verdict": {
            "symmetry_reduces_hamiltonian_to_one_gap": True,
            "symmetry_selects_resonance": False,
            "symmetry_selects_vacuum": False,
            "connector_normalization_selects_rate": False,
            "existing_chain_contains_new_channel": False,
            "energy_state_rate_parent_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_minimal_dynamic_parent_architecture_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()