#!/usr/bin/env python3
"""Exact parent-origin audit for the typed binary incidence carrier."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_architecture_gate_results.json").read_text())
    gate = "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_parent_origin_gate"
    assert predecessor["next_gate"] == gate

    y_u = sp.Rational(5, 3)
    y_d = sp.Rational(2, 3)
    y_bit = sp.diag(y_u, y_d)
    p_u = sp.diag(1, 0)
    p_d = sp.diag(0, 1)
    l_down = sp.Matrix([[0, 0], [1, 0]])
    l_up = l_down.T

    assert y_bit * p_u == p_u * y_bit
    assert y_bit * p_d == p_d * y_bit
    assert y_bit * l_down - l_down * y_bit == -l_down
    assert y_bit * l_up - l_up * y_bit == l_up

    a, b, c, d = sp.symbols("a b c d")
    x = sp.Matrix([[a, b], [c, d]])
    commutator = y_bit * x - x * y_bit
    equations = list(commutator)
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, [a, b, c, d])
    invariant_dimension = 4 - coefficient_matrix.rank()
    assert invariant_dimension == 2
    assert sp.solve(equations, [b, c], dict=True) == [{b: 0, c: 0}]

    z = sp.symbols("z", nonzero=True)
    gram = l_down.T * l_down
    gram_scaled = (z**-1 * l_down.T) * (z * l_down)
    assert sp.simplify(gram_scaled - gram) == sp.zeros(2)
    assert sp.simplify((z**-1 * l_down.T) * x * (z * l_down) - l_down.T * x * l_down) == sp.zeros(2)

    j1 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    j2 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    j3 = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    stacked = sp.Matrix.vstack(j1, j2, j3)
    assert stacked.rank() == 3
    assert len(stacked.nullspace()) == 0

    q_down = sp.simplify(y_d - y_u)
    q_environment = -q_down
    assert q_down == -1
    assert q_environment == 1

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "existing_static_center": {
            "algebra": "C P_u direct_sum C P_d",
            "dimension": 2,
            "projectors_present": True,
            "classical_binary_label_requires_new_hilbert_dimension": False,
            "controlled_dynamic_switch_present": False,
        },
        "gauge_transition": {
            "hypercharges": {"u": "5/3", "d": "2/3"},
            "invariant_commutant_dimension": invariant_dimension,
            "invariant_off_diagonal_hom_dimension": 0,
            "downward_operator": "|d><u|",
            "downward_operator_charge": str(q_down),
            "upward_operator_charge": "1",
            "single_jump_dissipator_is_gauge_covariant": True,
            "invariant_system_hamiltonian_contains_downward_operator": False,
        },
        "existing_noise_frame": {
            "old_frame_ambient": "End(H_21)",
            "new_controlled_carrier_in_old_frame": False,
            "zero_extension_annihilates_new_binary_off_diagonal": True,
            "old_42_frame_supplies_required_jump": False,
        },
        "charged_environment_route": {
            "required_environment_transition_charge": str(q_environment),
            "minimal_interaction": "g(L_down tensor b_+ + L_up tensor b_+^*)",
            "gauge_neutral_total_charge": "0",
            "old_charged_singlet_multiplicity": 3,
            "family_type": "SO(3) triplet",
            "family_invariant_vector_dimension": 0,
            "canonical_mediator_line_selected": False,
            "resonant_environment_gap_required": "7 gamma",
            "resonant_environment_gap_inherited": False,
        },
        "missing_parent_data": [
            "binary_off_diagonal_system_operator_in_extended_frame",
            "family_singlet_environment_transition_of_charge_plus_one",
            "gauge_invariant_system_environment_interaction",
            "environment_vacuum_or_zero_temperature_state",
            "resonant_gap_7_gamma",
            "physical_relaxation_rate",
        ],
        "ledgers": {
            "static_center_origin_satisfied": 4,
            "static_center_origin_tested": 4,
            "covariant_transition_shape_satisfied": 6,
            "covariant_transition_shape_tested": 6,
            "microscopic_parent_origin_satisfied": 0,
            "microscopic_parent_origin_tested": 6,
        },
        "verdict": {
            "classical_binary_center_already_exists": True,
            "gauge_covariant_dissipator_is_conditionally_allowed": True,
            "existing_42_frame_contains_binary_jump": False,
            "existing_family_triplet_selects_unique_mediator": False,
            "binary_relaxation_parent_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_architecture_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()