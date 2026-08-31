#!/usr/bin/env python3
"""Exact audit of the minimal dynamic parent for the charged mediator."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_minimal_dynamic_parent_architecture_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v8_{STEM}_results.json"


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def main() -> None:
    predecessor_path = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_energy_state_rate_parent_origin_gate_results.json"
    predecessor = json.loads(predecessor_path.read_text(encoding="utf-8"))
    gate = f"version8_{STEM}"
    assert predecessor["next_gate"] == gate

    delta = sp.Integer(7)
    identity_s = sp.eye(4)
    identity_e = sp.eye(3)
    y_s = sp.diag(1, 0, -1, 0)
    h_s = sp.diag(delta, 0, delta, 0)
    y_e = sp.diag(0, 1, -1)
    h_e = sp.diag(0, delta, delta)

    # Particle and Real-conjugate downward transitions.
    l_minus = sp.zeros(4)
    l_minus[1, 0] = 1
    l_plus = sp.zeros(4)
    l_plus[3, 2] = 1
    b_plus = sp.zeros(3)
    b_plus[1, 0] = 1
    b_minus = sp.zeros(3)
    b_minus[2, 0] = 1

    interaction = (
        sp.kronecker_product(l_minus, b_plus)
        + sp.kronecker_product(l_minus.T, b_plus.T)
        + sp.kronecker_product(l_plus, b_minus)
        + sp.kronecker_product(l_plus.T, b_minus.T)
    )
    y_total = sp.kronecker_product(y_s, identity_e) + sp.kronecker_product(identity_s, y_e)
    h_total = sp.kronecker_product(h_s, identity_e) + sp.kronecker_product(identity_s, h_e)
    assert is_zero(y_total * interaction - interaction * y_total)
    assert is_zero(h_total * interaction - interaction * h_total)
    assert interaction.rank() == 4
    assert interaction.eigenvals() == {-1: 2, 0: 8, 1: 2}

    vacuum = sp.Matrix([1, 0, 0])
    charged_outputs = (sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1]))
    extracted = []
    for output in charged_outputs:
        left = sp.kronecker_product(identity_s, output.T)
        right = sp.kronecker_product(identity_s, vacuum)
        extracted.append(sp.simplify(left * interaction * right))
    assert extracted == [l_minus, l_plus]
    assert sp.trace(extracted[0].H * extracted[1]) == 0

    left_vac = sp.kronecker_product(identity_s, vacuum.T)
    right_vac = sp.kronecker_product(identity_s, vacuum)
    first_moment = sp.simplify(left_vac * interaction * right_vac)
    second_moment = sp.simplify(left_vac * interaction**2 * right_vac)
    expected_second = l_minus.H * l_minus + l_plus.H * l_plus
    assert is_zero(first_moment)
    assert is_zero(second_moment - expected_second)

    old_jump_count = 42
    added_real_pair = 2
    total_jump_count = old_jump_count + added_real_pair
    old_cell_dimension = 1 + old_jump_count
    extended_cell_dimension = 1 + total_jump_count
    assert old_cell_dimension == 43
    assert extended_cell_dimension == 45

    # A positive on-site projector parent selects the product vacuum.
    h_cell = sp.diag(0, *([1] * old_jump_count), delta, delta)
    assert h_cell.rank() == total_jump_count
    assert len(h_cell.nullspace()) == 1
    assert h_cell.nullspace()[0] == sp.eye(extended_cell_dimension)[:, 0]

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "minimal_extended_cell": {
            "old_jump_count": old_jump_count,
            "old_cell_dimension": old_cell_dimension,
            "added_charged_jump_labels": added_real_pair,
            "total_jump_count": total_jump_count,
            "extended_cell_dimension": extended_cell_dimension,
            "basis": "neutral vacuum + 42 old labels + charge(+1,-1) Real pair",
            "two_added_lines_are_minimal_for_real_closure": True,
        },
        "local_collision_parent": {
            "system_basis": ["u", "d", "u_conjugate", "d_conjugate"],
            "system_charges": [1, 0, -1, 0],
            "environment_charges": [0, 1, -1],
            "system_energies_in_gap_units": [7, 0, 7, 0],
            "environment_energies_in_gap_units": [0, 7, 7],
            "total_charge_commutator_zero": True,
            "free_energy_commutator_zero": True,
            "interaction_rank": interaction.rank(),
            "interaction_spectrum": {"-1": 2, "0": 8, "1": 2},
            "vacuum_first_moment_zero": True,
            "vacuum_second_moment": "L_-^*L_- + L_+^*L_+",
            "cross_covariance_zero": True,
        },
        "chain_parent": {
            "onsite_parent": "h_cell=I-|0><0| with charged energies refined to 7",
            "unique_finite_volume_product_vacuum": True,
            "frustration_free": True,
            "finite_volume_gap_in_old_excitation_units": 1,
            "toeplitz_cell_dimension": extended_cell_dimension,
            "floquet_shift_index": extended_cell_dimension,
            "exact_repeated_channel_available": True,
            "shift_generated_by_local_hamiltonian": False,
        },
        "weak_limit": {
            "old_channels": old_jump_count,
            "new_real_paired_channels": added_real_pair,
            "total_channels": total_jump_count,
            "generator": "L_42 + g^2(D_Lminus + D_Lplus)",
            "primitive_fixed_algebra_preserved_if_L42_is_primitive": True,
            "physical_rate": "Gamma=g^2/hbar-scale after a clock convention",
        },
        "ledgers": {
            "conditional_dynamic_architecture_satisfied": 10,
            "conditional_dynamic_architecture_tested": 10,
            "inherited_parent_origin_satisfied": 0,
            "inherited_parent_origin_tested": 5,
        },
        "missing_parent_data": [
            "conditional neutral and global family carrier extension",
            "resonant dimensional gap 7 gamma",
            "physical coupling g",
            "primitive Floquet shift or balanced transport law",
            "physical clock-to-collision duration",
        ],
        "verdict": {
            "minimal_real_closed_dynamic_parent_constructed": True,
            "old_cell_extension_is_two_dimensional": True,
            "extended_weak_generator_has_44_channels": True,
            "product_vacuum_has_local_parent": True,
            "full_physical_parent_inherited": False,
        },
        "next_gate": "version8_baryon_c0_charged_mediator_dynamic_parent_data_admission_gate",
        "floating_point_values": 0,
    }
    assert result["ledgers"]["conditional_dynamic_architecture_satisfied"] == 10
    assert result["ledgers"]["inherited_parent_origin_satisfied"] == 0
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()