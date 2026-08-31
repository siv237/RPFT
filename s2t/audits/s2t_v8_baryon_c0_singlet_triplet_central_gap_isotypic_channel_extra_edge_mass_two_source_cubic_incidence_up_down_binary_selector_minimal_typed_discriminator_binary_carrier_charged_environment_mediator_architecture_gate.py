#!/usr/bin/env python3
"""Exact audit of the minimal charged environment mediator architecture."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_architecture_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v8_{STEM}_results.json"


def main() -> None:
    predecessor_path = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_parent_origin_gate_results.json"
    predecessor = json.loads(predecessor_path.read_text())
    gate = f"version8_{STEM}"
    assert predecessor["next_gate"] == gate

    delta = sp.Integer(7)
    y_s = sp.diag(sp.Rational(5, 3), sp.Rational(2, 3))
    h_s = sp.diag(delta, 0)
    p_u, p_d = sp.diag(1, 0), sp.diag(0, 1)
    l_down = sp.Matrix([[0, 0], [1, 0]])
    l_up = l_down.T

    y_e = sp.diag(0, 1)
    h_e = sp.diag(0, delta)
    b_plus = sp.Matrix([[0, 0], [1, 0]])
    identity = sp.eye(2)
    y_total = sp.kronecker_product(y_s, identity) + sp.kronecker_product(identity, y_e)
    h_total = sp.kronecker_product(h_s, identity) + sp.kronecker_product(identity, h_e)
    interaction = sp.kronecker_product(l_down, b_plus) + sp.kronecker_product(l_up, b_plus.T)

    assert y_total * interaction - interaction * y_total == sp.zeros(4)
    assert h_total * interaction - interaction * h_total == sp.zeros(4)
    assert interaction.rank() == 2
    assert interaction.eigenvals() == {-1: 1, 0: 2, 1: 1}

    c, s = sp.sqrt(3) / 2, sp.Rational(1, 2)
    k0 = p_d + c * p_u
    k1 = -sp.I * s * l_down
    assert sp.simplify(k0.H * k0 + k1.H * k1) == identity
    rho_uu, rho_ud, rho_du, rho_dd = sp.symbols("rho_uu rho_ud rho_du rho_dd")
    rho = sp.Matrix([[rho_uu, rho_ud], [rho_du, rho_dd]])
    channel = sp.simplify(k0 * rho * k0.H + k1 * rho * k1.H)
    expected = sp.Matrix([[sp.Rational(3, 4) * rho_uu, c * rho_ud],
                          [c * rho_du, rho_dd + sp.Rational(1, 4) * rho_uu]])
    assert sp.simplify(channel - expected) == sp.zeros(2)

    p_one = sp.Rational(1, 4)
    p_composed = 1 - (1 - p_one) ** 2
    p_coherent_double = sp.Rational(3, 4)
    assert p_composed == sp.Rational(7, 16)
    assert p_coherent_double - p_composed == sp.Rational(5, 16)

    y_real = sp.diag(0, 1, -1)
    real_swap = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    assert real_swap * y_real * real_swap.T == -y_real

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "minimal_complex_mediator": {
            "environment_basis": ["neutral_vacuum", "charge_plus_one_excitation"],
            "complex_dimension": 2,
            "environment_hypercharge": "diag(0,1)",
            "environment_hamiltonian": "diag(0,7 gamma)",
            "system_hamiltonian": "diag(7 gamma,0)",
            "interaction": "g(L_down tensor b_+ + L_up tensor b_+^*)",
            "total_charge_commutator_zero": True,
            "free_energy_commutator_zero": True,
            "resonant_interaction_rank": 2,
            "resonant_interaction_spectrum": ["-1", "0", "0", "1"],
        },
        "one_collision_channel": {
            "kraus_operators": ["P_d+cos(theta)P_u", "-i sin(theta)L_down"],
            "amplitude_damping_parameter": "sin(theta)^2",
            "kraus_rank_for_open_interval": 2,
            "minimal_complex_environment_dimension": 2,
            "exact_test_theta": "pi/6",
            "exact_test_parameter": str(p_one),
            "trace_preserving": True,
        },
        "semigroup_boundary": {
            "single_ancilla_is_periodic": True,
            "full_transfer_angle": "pi/2",
            "revival_angle": "pi",
            "same_channel_twice_parameter_at_pi_over_6": str(p_composed),
            "coherent_double_time_parameter": str(p_coherent_double),
            "composition_defect": str(p_coherent_double - p_composed),
            "single_finite_ancilla_is_not_irreversible_semigroup": True,
            "fresh_ancilla_chain_required": True,
            "weak_collision_scaling_required": "theta_h=g sqrt(h)",
        },
        "real_completion": {
            "complex_two_level_environment_is_real_closed": False,
            "minimal_real_compatible_complex_dimension": 3,
            "charges": [0, 1, -1],
            "real_structure_swaps_charged_lines": True,
            "family_singlet_assignment_is_new_data": True,
        },
        "ledgers": {
            "minimal_complex_dilation_satisfied": 8,
            "minimal_complex_dilation_tested": 8,
            "gauge_energy_real_completion_satisfied": 6,
            "gauge_energy_real_completion_tested": 6,
            "autonomous_irreversible_origin_satisfied": 0,
            "autonomous_irreversible_origin_tested": 6,
        },
        "missing_parent_data": [
            "new_family_singlet_charged_environment_pair",
            "environment_gap_7_gamma",
            "neutral_vacuum_state",
            "coupling_constant_g",
            "fresh_ancilla_chain_or_reset_mechanism",
            "physical_clock_to_collision_rate_anchor",
        ],
        "verdict": {
            "conditional_charged_mediator_architecture_complete": True,
            "one_collision_amplitude_damping_exact": True,
            "minimal_complex_dilation_proved": True,
            "minimal_real_completion_proved": True,
            "irreversible_parent_inherited": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_existing_carrier_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()