#!/usr/bin/env python3
"""Exact four-slot origin audit for the two Tome IX KMS source covectors."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_source_covector_four_slot_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_source_vector_"
        "common_parent_architecture_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate

    weight = sp.diag(1, 1, 3)
    multiplicity = sp.Matrix([1, 1, 3])
    shape_basis = sp.Matrix([
        [1, 0],
        [0, 1],
        [-sp.Rational(1, 3), -sp.Rational(1, 3)],
    ])
    assert (multiplicity.T * shape_basis) == sp.zeros(1, 2)
    assert shape_basis.rank() == 2

    # log(E_*), log(chi) -> log(E_*), log(chi^2 E_*/hbar)
    scale_jacobian = sp.Matrix([[1, 0], [1, 2]])
    assert scale_jacobian.rank() == 2
    assert scale_jacobian.det() == 2

    e, chi, a, b, c, d = sp.symbols(
        "e chi a b c d", positive=True
    )
    gap_shape = sp.Matrix([a, b, (5 - a - b) / 3])
    conductance_shape = sp.Matrix([c, d, (5 - c - d) / 3])
    gamma = chi**2 * e
    physical_package = sp.Matrix.vstack(
        e * gap_shape,
        gamma * conductance_shape,
    )
    variables = sp.Matrix([e, chi, a, b, c, d])
    full_jacobian = physical_package.jacobian(variables)
    witness = {e: 1, chi: 1, a: 1, b: 1, c: 1, d: 1}
    witness_jacobian = full_jacobian.subs(witness)
    assert witness_jacobian.rank() == 6
    assert witness_jacobian.det() == sp.Rational(50, 9)

    scale_columns = witness_jacobian[:, :2]
    shape_columns = witness_jacobian[:, 2:]
    assert scale_columns.rank() == 2
    assert shape_columns.rank() == 4
    assert witness_jacobian.rank() - scale_columns.rank() == 4

    identity = sp.eye(3)
    reverse = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    assert identity.T * weight * identity == weight
    assert reverse.T * weight * reverse == weight
    assert identity.det() == 1 and reverse.det() == -1
    assert (reverse * shape_basis).rank() == 2

    gap_shape_a = sp.Matrix([1, 1, 1])
    gap_shape_b = sp.Matrix([2, 1, sp.Rational(2, 3)])
    conductance_shape_a = sp.Matrix([1, 1, 1])
    conductance_shape_b = sp.Matrix([1, 2, sp.Rational(2, 3)])
    for vector in [
        gap_shape_a,
        gap_shape_b,
        conductance_shape_a,
        conductance_shape_b,
    ]:
        assert (multiplicity.T * vector)[0] == 5
        assert all(value > 0 for value in vector)
    assert gap_shape_a != gap_shape_b
    assert conductance_shape_a != conductance_shape_b

    j_theta_a = weight * gap_shape_a
    j_theta_b = weight * gap_shape_b
    j_kappa_a = weight * conductance_shape_a
    j_kappa_b = weight * conductance_shape_b
    assert j_theta_a != j_theta_b and j_kappa_a != j_kappa_b

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "four_slot_scale_map": {
            "gap_scale": "E_*",
            "conductance_scale": "chi^2 E_*/hbar",
            "log_jacobian": [[1, 0], [1, 2]],
            "rank": 2,
            "determinant": 2,
            "common_scales_linked": True,
        },
        "type_shape_decomposition": {
            "multiplicity_weights": [1, 1, 3],
            "shape_dimension_per_covector": 2,
            "total_relative_shape_dimension": 4,
            "endpoint_types_label_channels": True,
            "endpoint_types_select_relative_values": False,
        },
        "transport_audit": {
            "orientations_tested": ["identity", "neutral_swap"],
            "metric_preserved": True,
            "shape_rank_preserved": 2,
            "relative_values_selected": False,
        },
        "jacobian_audit": {
            "full_parameter_rank": 6,
            "full_parameter_determinant_at_unit_witness": "50/9",
            "four_slot_continuous_rank": 2,
            "relative_shape_rank": 4,
            "unselected_relative_dimension": 4,
        },
        "normalized_witnesses": {
            "gap_shapes": [[1, 1, 1], [2, 1, "2/3"]],
            "conductance_shapes": [[1, 1, 1], [1, 2, "2/3"]],
            "weighted_normalization": 5,
            "same_common_scales": True,
            "distinct_source_covectors": True,
        },
        "ledgers": {
            "common_scale_links_satisfied": 2,
            "common_scale_links_tested": 2,
            "channel_type_labels_satisfied": 3,
            "channel_type_labels_tested": 3,
            "relative_ratio_origin_satisfied": 0,
            "relative_ratio_origin_tested": 4,
            "source_covector_origin_satisfied": 0,
            "source_covector_origin_tested": 2,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "four_slots_fix_both_common_scales": True,
            "endpoint_types_fix_channel_form": True,
            "transport_can_orient_type_coordinates": True,
            "four_relative_ratios_remain_free": True,
            "source_covectors_physically_derived": False,
            "minimal_four_coordinate_selector_required": True,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_relative_shape_"
            "minimal_selector_architecture_gate"
        ),
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()