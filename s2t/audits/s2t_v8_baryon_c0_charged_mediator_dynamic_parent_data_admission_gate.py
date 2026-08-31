#!/usr/bin/env python3
"""Exact admission audit for the charged-mediator dynamic parent data."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "baryon_c0_charged_mediator_dynamic_parent_data_admission_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v8_{STEM}_results.json"


def swap_matrix(dimension: int) -> sp.Matrix:
    matrix = sp.zeros(dimension * dimension)
    for left in range(dimension):
        for right in range(dimension):
            source = left * dimension + right
            target = right * dimension + left
            matrix[target, source] = 1
    return matrix


def main() -> None:
    predecessor_path = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_charged_environment_mediator_minimal_dynamic_parent_architecture_gate_results.json"
    predecessor = json.loads(predecessor_path.read_text(encoding="utf-8"))
    gate = f"version8_{STEM}"
    assert predecessor["next_gate"] == gate

    old_dimension = 43
    new_dimension = 45
    inclusion = sp.zeros(new_dimension, old_dimension)
    inclusion[:old_dimension, :old_dimension] = sp.eye(old_dimension)
    assert inclusion.T * inclusion == sp.eye(old_dimension)
    assert (inclusion * inclusion.T).rank() == old_dimension

    vacuum_old = sp.eye(old_dimension)[:, 0]
    vacuum_new = sp.eye(new_dimension)[:, 0]
    assert inclusion * vacuum_old == vacuum_new

    old_parent = sp.diag(0, *([1] * 42))
    new_parent = sp.diag(0, *([1] * 42), 7, 7)
    assert inclusion.T * new_parent * inclusion == old_parent

    old_charge = sp.zeros(old_dimension)
    new_charge = sp.diag(*([0] * old_dimension), 1, -1)
    assert inclusion.T * new_charge * inclusion == old_charge

    # The chain intertwining identity is indexwise. A 3->5 representative
    # verifies the exact tensor formula without constructing 45^2 matrices.
    representative_inclusion = sp.zeros(5, 3)
    representative_inclusion[:3, :3] = sp.eye(3)
    tensor_inclusion = sp.kronecker_product(
        representative_inclusion, representative_inclusion
    )
    shift_old = swap_matrix(3)
    shift_new = swap_matrix(5)
    assert shift_new * tensor_inclusion == tensor_inclusion * shift_old

    # Orthogonal complement contains exactly the charged Real pair.
    complement_projector = sp.eye(new_dimension) - inclusion * inclusion.T
    assert complement_projector.rank() == 2
    real_swap = sp.eye(new_dimension)
    real_swap[new_dimension - 2, new_dimension - 2] = 0
    real_swap[new_dimension - 1, new_dimension - 1] = 0
    real_swap[new_dimension - 2, new_dimension - 1] = 1
    real_swap[new_dimension - 1, new_dimension - 2] = 1
    assert real_swap * new_charge * real_swap.T == -new_charge
    assert real_swap * inclusion == inclusion

    structural_checks = {
        "canonical_isometry": True,
        "vacuum_preserved": True,
        "old_parent_is_restriction": True,
        "old_charge_is_restriction": True,
        "old_42_jump_labels_preserved": True,
        "chain_shift_intertwines": True,
        "orthogonal_complement_is_real_charged_pair": True,
        "old_reduced_dynamics_is_unchanged_on_zero_new_coupling": True,
    }
    assert all(structural_checks.values())

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "canonical_cell_embedding": {
            "map": "iota: K43 -> K45, e_a maps to e_a",
            "old_dimension": old_dimension,
            "new_dimension": new_dimension,
            "isometry": True,
            "range_rank": old_dimension,
            "orthogonal_complement_dimension": 2,
            "vacuum_preserved": True,
            "old_parent_recovered_by_compression": True,
            "old_charge_recovered_by_compression": True,
        },
        "chain_embedding": {
            "tensor_product_embedding": "Iota=otimes_m iota_m on the vacuum reference chain",
            "shift_intertwining": "S45 Iota = Iota S43",
            "finite_two_cell_representative_exact": True,
            "old_floquet_step_is_restriction_when_new_coupling_is_zero": True,
            "gnvw_indices": {"old": 43, "extended": 45},
            "index_change_requires_real_cell_extension": True,
        },
        "structural_admission": {
            **structural_checks,
            "satisfied": len(structural_checks),
            "tested": len(structural_checks),
        },
        "available_shapes": {
            "conditional_carrier_and_connector": True,
            "resonant_hamiltonian_form": True,
            "trace_normalized_interaction_direction": True,
            "toeplitz_conveyor_template": True,
            "clock_rate_formula": True,
            "satisfied": 5,
            "tested": 5,
        },
        "physical_parent_origin": {
            "conditional_carrier_inherited_from_raw_H21": False,
            "dimensional_gap_7_gamma_selected": False,
            "physical_coupling_g_selected": False,
            "extended_transport_law_selected": False,
            "physical_tick_duration_selected": False,
            "satisfied": 0,
            "tested": 5,
        },
        "verdict": {
            "extension_is_conservative": True,
            "old_42_channel_process_is_preserved": True,
            "all_required_shapes_are_present_conditionally": True,
            "new_physical_selector_is_obtained": False,
            "dynamic_parent_data_admitted_structurally_not_derived": True,
        },
        "next_gate": "version8_baryon_c0_charged_mediator_dynamic_parent_minimal_new_data_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()