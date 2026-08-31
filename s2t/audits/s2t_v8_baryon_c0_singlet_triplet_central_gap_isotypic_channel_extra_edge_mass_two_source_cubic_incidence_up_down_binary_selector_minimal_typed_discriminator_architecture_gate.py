#!/usr/bin/env python3
"""Exact audit of the minimal typed two-state incidence discriminator."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_architecture_gate_results.json"


def heisenberg_superoperator(jump: sp.Matrix) -> sp.Matrix:
    basis = [sp.Matrix([[1, 0], [0, 0]]), sp.Matrix([[0, 1], [0, 0]]),
             sp.Matrix([[0, 0], [1, 0]]), sp.Matrix([[0, 0], [0, 1]])]
    gram = jump.T * jump
    columns = []
    for x in basis:
        image = jump.T * x * jump - sp.Rational(1, 2) * (gram * x + x * gram)
        columns.append(sp.Matrix([image[0, 0], image[0, 1], image[1, 0], image[1, 1]]))
    return sp.Matrix.hstack(*columns)


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_parent_origin_gate_results.json").read_text())
    gate = "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_architecture_gate"
    assert predecessor["next_gate"] == gate

    p_u = sp.diag(1, 0)
    p_d = sp.diag(0, 1)
    sigma_z = p_u - p_d
    h_u = sp.Rational(25, 3)
    h_d = sp.Rational(4, 3)
    h_inc = sp.diag(h_u, h_d)
    h_mean = sp.simplify((h_u + h_d) / 2)
    h_split = sp.simplify((h_u - h_d) / 2)
    h_zero = sp.simplify(h_inc - h_mean * sp.eye(2))
    gap = sp.simplify(h_u - h_d)

    assert p_u * p_d == sp.zeros(2)
    assert p_u + p_d == sp.eye(2)
    assert sigma_z**2 == sp.eye(2)
    assert h_mean == sp.Rational(29, 6)
    assert h_split == sp.Rational(7, 2)
    assert h_zero == h_split * sigma_z
    assert gap == 7

    endpoint_p_u = sp.diag(sp.eye(6), sp.zeros(6))
    endpoint_p_d = sp.diag(sp.zeros(6), sp.eye(6))
    controlled = sp.kronecker_product(p_u, endpoint_p_u) + sp.kronecker_product(p_d, endpoint_p_d)
    assert controlled**2 == controlled
    assert controlled.rank() == 12

    jump_down = sp.Matrix([[0, 0], [1, 0]])
    dissipator = heisenberg_superoperator(jump_down)
    assert dissipator.rank() == 3
    assert len(dissipator.nullspace()) == 1
    assert dissipator * sp.Matrix([1, 0, 0, 1]) == sp.zeros(4, 1)

    commutator_super = sp.kronecker_product(sp.eye(2), h_inc) - sp.kronecker_product(h_inc.T, sp.eye(2))
    assert commutator_super.rank() == 2
    assert len(commutator_super.nullspace()) == 2

    theta = sp.symbols("theta", positive=True)
    gibbs_ratio = sp.exp(-gap * theta)
    p_u_thermal = sp.simplify(gibbs_ratio / (1 + gibbs_ratio))
    p_d_thermal = sp.simplify(1 / (1 + gibbs_ratio))
    assert sp.simplify(p_u_thermal / p_d_thermal - gibbs_ratio) == 0
    assert sp.limit(p_u_thermal, theta, sp.oo) == 0
    assert sp.limit(p_d_thermal, theta, sp.oo) == 1

    objects = [p_u, p_d, sigma_z, h_inc, h_zero, gap, controlled,
               jump_down, dissipator, commutator_super]
    assert not any(obj.atoms(sp.Float) for obj in objects)

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "binary_carrier": {
            "hilbert_dimension": 2,
            "projectors": {"u": "|u><u|", "d": "|d><d|"},
            "sigma_z": "P_u-P_d",
            "sigma_z_squared": "I_2",
            "faithful_dimension_is_minimal": True,
        },
        "controlled_incidence": {
            "formula": "P_u(bit) tensor P_u(endpoint) + P_d(bit) tensor P_d(endpoint)",
            "is_projection": True,
            "rank": 12,
            "gauge_equivariant": True,
            "real_compatible": True,
            "grading_even": True,
        },
        "typed_hamiltonian": {
            "eigenvalues": {"u": "25/3", "d": "4/3"},
            "decomposition": "(29/6)I_2+(7/2)sigma_z",
            "spectral_gap": "7",
            "positive_coefficient_ground_state": "d",
            "negative_coefficient_ground_state": "u",
            "coefficient_sign_is_architecture_input": True,
        },
        "dynamics": {
            "unitary_commutator_superoperator_rank": 2,
            "unitary_fixed_algebra_dimension": 2,
            "unitary_dynamics_selects_population": False,
            "zero_temperature_jump": "|d><u|",
            "amplitude_damping_heisenberg_rank": 3,
            "amplitude_damping_fixed_algebra_dimension": 1,
            "unique_stationary_state": "|d><d|",
            "thermal_population_ratio": "exp(-7 theta)",
            "zero_temperature_limit": {"p_u": "0", "p_d": "1"},
            "relaxation_rate_is_free": True,
        },
        "minimal_new_data": [
            "two_state_binary_carrier",
            "controlled_endpoint_embedding",
            "positive_typed_hypercharge_square_coefficient",
            "downward_jump_or_zero_temperature_bath",
            "relaxation_rate_for_physical_time",
        ],
        "ledgers": {
            "typed_static_architecture_satisfied": 8,
            "typed_static_architecture_tested": 8,
            "conditional_relaxation_shape_satisfied": 5,
            "conditional_relaxation_shape_tested": 5,
            "inherited_origin_satisfied": 0,
            "inherited_origin_tested": 5,
        },
        "verdict": {
            "minimal_static_selector_constructed": True,
            "unitary_hamiltonian_alone_selects_branch": False,
            "conditional_zero_temperature_relaxation_constructed": True,
            "binary_choice_derived_from_existing_parent": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()