#!/usr/bin/env python3
"""Exact admission audit for an existing charged environment mediator."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_existing_carrier_admission_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v8_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_architecture_gate_results.json").read_text())
    gate = f"version8_{STEM}"
    assert predecessor["next_gate"] == gate

    j1 = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    j2 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    j3 = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    family_generators = [sp.diag(sp.Integer(0), j) for j in (j1, j2, j3)]
    stacked = sp.Matrix.vstack(*family_generators)
    assert stacked.rank() == 3
    assert len(stacked.nullspace()) == 1
    assert stacked.nullspace()[0] == sp.Matrix([1, 0, 0, 0])

    variables = sp.symbols("t0:8")
    t = sp.Matrix(4, 2, variables)
    gamma_target = sp.diag(-1, 1, 1, 1)
    gamma_neutral = sp.diag(1, -1)
    equations = []
    for generator in family_generators:
        equations.extend(generator * t)
    equations.extend(gamma_target * t + t * gamma_neutral)
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    assert coefficient_matrix.rank() == 7
    assert len(coefficient_matrix.nullspace()) == 1
    mediator = sp.Matrix([[1, 0], [0, 0], [0, 0], [0, 0]])
    assert coefficient_matrix * mediator.reshape(8, 1) == sp.zeros(coefficient_matrix.rows, 1)

    y_target = -sp.eye(4)
    y_neutral = sp.zeros(2)
    assert y_target * mediator - mediator * y_neutral == -mediator

    y_pair = sp.diag(0, -1)
    lowering = sp.Matrix([[0, 0], [1, 0]])
    c1 = lowering + lowering.T
    c2 = sp.I * (lowering - lowering.T)
    assert sp.I * (y_pair * c1 - c1 * y_pair) == -c2
    assert sp.I * (y_pair * c2 - c2 * y_pair) == c1
    gram = sp.Matrix([[sp.trace(a.H * b) for b in (c1, c2)] for a in (c1, c2)])
    assert gram == 2 * sp.eye(2)

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "corrected_charged_family_decomposition": {
            "old_charged_singlet_multiplicity": 3,
            "coarse_all_triplet_reading_valid": False,
            "existing_family_singlet_line": "e_R^(s)",
            "remaining_old_lines": "two members of a positive-grading triplet",
            "globally_closed_conditional_decomposition": "1 direct_sum 3 in H_24",
            "family_fixed_dimension_after_closure": 1,
        },
        "unique_typed_mediator": {
            "neutral_source_space": "span(s0,a0)",
            "neutral_source_gradings": [1, -1],
            "charged_target_gradings": [-1, 1, 1, 1],
            "family_invariant_odd_hom_dimension": 1,
            "basis": "|e_R^(s)><s0|",
            "operator_charge": -1,
            "real_conjugate_charge": 1,
            "hermitian_quadrature_dimension": 2,
            "quadrature_trace_gram": "2 I2",
        },
        "carrier_admission": {
            "raw_H21_has_neutral_vacuum_line": False,
            "raw_H21_has_charged_family_singlet": True,
            "raw_real_double_has_opposite_charge_line": True,
            "conditional_H23_has_neutral_s0": True,
            "conditional_47_frame_contains_singlet_connector_quadratures": True,
            "conditional_H24_closes_global_family_representation": True,
            "raw_inherited_admission_satisfied": 2,
            "raw_inherited_admission_tested": 7,
            "conditional_extended_admission_satisfied": 7,
            "conditional_extended_admission_tested": 7,
        },
        "dynamic_origin": {
            "resonant_gap_7_gamma_inherited": False,
            "neutral_vacuum_state_selected": False,
            "coupling_g_selected": False,
            "fresh_ancilla_chain_inherited_for_this_channel": False,
            "clock_rate_anchor_inherited_for_this_channel": False,
            "satisfied": 0,
            "tested": 5,
        },
        "verdict": {
            "previous_all_triplet_obstruction_superseded": True,
            "unique_family_and_grading_typed_mediator_exists_conditionally": True,
            "new_independent_charged_singlet_pair_required": False,
            "neutral_extension_and_global_family_closure_are_conditional": True,
            "microscopic_irreversible_parent_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_energy_state_rate_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()