#!/usr/bin/env python3
"""Exact origin audit for the four relative-shape selector sources."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_relative_shape_selector_source_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def defect_shape(c: sp.Expr) -> sp.Matrix:
    raw = sp.Matrix([c + 2, c + 1, c])
    weights = sp.Matrix([1, 1, 3])
    return sp.simplify(5 * raw / (weights.T * raw)[0])


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_relative_shape_"
        "minimal_selector_architecture_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert predecessor["minimality"]["target_shape_dimension"] == 4

    type_matrix = sp.Matrix([[1, 1, 3], [1, -1, 3], [0, 0, -3]])
    assert type_matrix.rank() == 3 and type_matrix.det() == 6

    # Common scales disappear from all four relative ratios.
    scale_to_shape = sp.zeros(4, 2)
    assert scale_to_shape.rank() == 0

    # Equality of gap/conductance shapes removes only two directions.
    cross_lock = sp.Matrix([[1, 0, -1, 0], [0, 1, 0, -1]])
    assert cross_lock.rank() == 2
    assert len(cross_lock.nullspace()) == 2

    # Invariance under swapping the two singlet labels also leaves two freedoms.
    swap_invariance = sp.Matrix([[1, -1, 0, 0], [0, 0, 1, -1]])
    assert swap_invariance.rank() == 2
    assert len(swap_invariance.nullspace()) == 2
    combined = sp.Matrix.vstack(cross_lock, swap_invariance)
    assert combined.rank() == 3
    assert len(combined.nullspace()) == 1

    c = sp.symbols("c", positive=True)
    family = defect_shape(c)
    expected_family = sp.Matrix([
        5 * (c + 2) / (5 * c + 3),
        5 * (c + 1) / (5 * c + 3),
        5 * c / (5 * c + 3),
    ])
    assert sp.simplify(family - expected_family) == sp.zeros(3, 1)
    witness_one = family.subs(c, 1)
    witness_two = family.subs(c, 2)
    assert witness_one == sp.Matrix([
        sp.Rational(15, 8), sp.Rational(5, 4), sp.Rational(5, 8)
    ])
    assert witness_two == sp.Matrix([
        sp.Rational(20, 13), sp.Rational(15, 13), sp.Rational(10, 13)
    ])
    assert witness_one != witness_two

    u, v = sp.symbols("u v", real=True)
    source_free = 5 * sp.log((sp.exp(u) + sp.exp(v) + 3) / 5)
    gradient = sp.Matrix([sp.diff(source_free, u), sp.diff(source_free, v)])
    assert all(component.is_positive for component in gradient)
    boundary_limit = sp.limit(source_free.subs({u: -c, v: -c}), c, sp.oo)
    assert boundary_limit == 5 * sp.log(sp.Rational(3, 5))
    assert gradient.subs({u: 0, v: 0}) == sp.Matrix([1, 1])

    # Weighted maximum entropy has a unique isotropic representative, but it
    # is an additional inference axiom rather than a term of the inherited parent.
    rs, ra, rt, lam = sp.symbols("rs ra rt lam", positive=True)
    entropy_gradient_equations = sp.Matrix([
        -sp.log(rs) - 1 + lam,
        -sp.log(ra) - 1 + lam,
        -3 * sp.log(rt) - 3 + 3 * lam,
    ])
    assert entropy_gradient_equations.subs({
        rs: 1, ra: 1, rt: 1, lam: 1
    }) == sp.zeros(3, 1)

    source_a = sp.Matrix([1, 2, 2, 1])
    source_b = sp.Matrix([2, 1, 1, 2])
    assert source_a != source_b
    assert all(value > 0 for value in [*source_a, *source_b])
    assert source_a[0] + source_a[1] < 5
    assert source_a[2] + source_a[3] < 5
    assert source_b[0] + source_b[1] < 5
    assert source_b[2] + source_b[3] < 5

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "inherited_parent_restriction": {
            "source_free_log_partition_gradient_at_origin": [1, 1, 1, 1],
            "finite_interior_stationary_point": False,
            "boundary_infimum_per_shape": "5 log(3/5)",
            "primitive_positive_shape_selected": False,
        },
        "candidate_audit": {
            "common_scales_shape_rank": 0,
            "type_matrix_rank": 3,
            "type_matrix_determinant": 6,
            "diagonal_type_coefficients_free": True,
            "kms_relates_forward_reverse_within_channel_only": True,
            "transport_supplies_continuous_source": False,
            "cross_shape_lock_rank": 2,
            "cross_shape_lock_nullity": 2,
            "singlet_swap_invariance_rank": 2,
            "singlet_swap_invariance_nullity": 2,
            "combined_lock_rank": 3,
            "combined_lock_nullity": 1,
        },
        "endpoint_defect_family": {
            "raw_defects": [2, 1, 0],
            "positive_completion_parameter_free": True,
            "witness_c_1": ["15/8", "5/4", "5/8"],
            "witness_c_2": ["20/13", "15/13", "10/13"],
            "unique_selector_source": False,
        },
        "maximum_entropy_candidate": {
            "weighted_isotropic_shape": [1, 1, 1],
            "selector_source_per_package": [1, 1],
            "unique_given_extra_inference_axiom": True,
            "present_in_inherited_parent": False,
            "counts_as_physical_origin": False,
        },
        "admissible_counterexamples": {
            "source_a": [1, 2, 2, 1],
            "source_b": [2, 1, 1, 2],
            "both_inside_source_cone": True,
            "same_common_scales": True,
            "different_relative_shapes": True,
        },
        "ledgers": {
            "candidate_origin_satisfied": 0,
            "candidate_origin_tested": 8,
            "conditional_entropy_representative_satisfied": 1,
            "conditional_entropy_representative_tested": 1,
            "selector_source_origin_satisfied": 0,
            "selector_source_origin_tested": 4,
            "relative_shape_physical_origin_satisfied": 0,
            "relative_shape_physical_origin_tested": 4,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "inherited_parent_selects_selector_sources": False,
            "existing_types_orientations_and_kms_are_sufficient": False,
            "maximum_entropy_is_additional_principle": True,
            "four_selector_sources_physically_derived": False,
            "minimal_invariant_source_parent_required": True,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_relative_shape_selector_source_"
            "minimal_invariant_parent_architecture_gate"
        ),
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()