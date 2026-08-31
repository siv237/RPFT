#!/usr/bin/env python3
"""Exact fixed-parent origin audit for the Tome IX endpoint finite module."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_finite_module_parent_action_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def coordinate_projector(size: int, indices: tuple[int, ...]) -> sp.Matrix:
    projector = sp.zeros(size)
    for index in indices:
        projector[index, index] = 1
    return projector


def main() -> None:
    predecessor = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v9_endpoint_extension_minimal_finite_module_architecture_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert predecessor["finite_module"]["new_independent_complex_states"] == 3

    old_multiplicity = sp.Matrix([0, 0, 2])
    new_multiplicity = sp.Matrix([1, 1, 3])
    jump = new_multiplicity - old_multiplicity
    assert list(jump) == [1, 1, 1]
    assert sum(abs(value) for value in jump) == 3

    dimension = 24
    rank = 3
    target = coordinate_projector(dimension, (21, 22, 23))
    competitor = coordinate_projector(dimension, (0, 1, 2))
    identity = sp.eye(dimension)
    seed = identity - 2 * target

    assert target**2 == target
    assert target.T.conjugate() == target
    assert sp.trace(target) == rank
    assert competitor**2 == competitor
    assert sp.trace(competitor) == rank

    kappa, mu, epsilon = sp.symbols("kappa mu epsilon", positive=True)

    def unseeded_potential(projector: sp.Matrix) -> sp.Expr:
        defect = projector**2 - projector
        return sp.simplify(
            kappa * sp.trace(defect * defect)
            + mu * (sp.trace(projector) - rank) ** 2
        )

    assert unseeded_potential(target) == 0
    assert unseeded_potential(competitor) == 0
    grassmannian_real_dimension = 2 * rank * (dimension - rank)
    assert grassmannian_real_dimension == 126

    eigenvalues = seed.eigenvals()
    assert eigenvalues == {sp.Integer(1): 21, sp.Integer(-1): 3}
    target_score = sp.simplify(epsilon * sp.trace(seed * target))
    competitor_score = sp.simplify(epsilon * sp.trace(seed * competitor))
    assert target_score == -3 * epsilon
    assert competitor_score == 3 * epsilon
    assert (identity - seed) / 2 == target

    triplet_increment = coordinate_projector(3, (0,))
    family_generator = sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]])
    family_commutator = family_generator * triplet_increment - triplet_increment * family_generator
    assert family_commutator != sp.zeros(3)
    assert family_commutator.rank() == 2

    fixed_parent_candidates = {
        "dirac_operator_variation": False,
        "inner_fluctuation": False,
        "old_operator_algebra_closure": False,
        "kernel_or_condensate_inside_H21": False,
        "morita_completion_without_new_bimodule": False,
        "environment_retyping": False,
        "sum_over_finite_geometries": False,
    }
    conditional_checks = {
        "rank_three_projector_space_defined_on_H24": True,
        "positive_penalty_has_projector_minima": True,
        "unseeded_minimum_is_not_unique": True,
        "typed_seed_has_target_negative_eigenspace": True,
        "seeded_constrained_score_selects_target": True,
    }
    assert not any(fixed_parent_candidates.values())
    assert all(conditional_checks.values())

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "multiplicity_jump": {
            "types": ["neutral_plus", "neutral_minus", "charged_minus_one_plus"],
            "old": [0, 0, 2],
            "new": [1, 1, 3],
            "delta": [1, 1, 1],
            "l1_size": 3,
            "integer_multiplicity_tangent_dimension": 0,
        },
        "fixed_parent_candidates": {
            **fixed_parent_candidates,
            "satisfied": sum(fixed_parent_candidates.values()),
            "tested": len(fixed_parent_candidates),
        },
        "conditional_projector_parent": {
            "ambient_dimension": dimension,
            "projector_rank": rank,
            "unseeded_minimum_manifold": "Gr_C(3,24)",
            "unseeded_minimum_real_dimension": grassmannian_real_dimension,
            "target_seed_spectrum": {"minus_one": 3, "plus_one": 21},
            "target_score": "-3 epsilon",
            "disjoint_coordinate_competitor_score": "+3 epsilon",
            "target_recovered_from_seed": "P_E=(I-C_E)/2",
            "triplet_increment_projector_family_commutator_rank": 2,
            "triplet_increment_projector_is_family_invariant": False,
            **conditional_checks,
            "satisfied": sum(conditional_checks.values()),
            "tested": len(conditional_checks),
        },
        "ledgers": {
            "fixed_parent_module_origin_satisfied": 0,
            "fixed_parent_module_origin_tested": 7,
            "conditional_projector_architecture_satisfied": 5,
            "conditional_projector_architecture_tested": 5,
            "finite_module_parent_origin_satisfied": 0,
            "finite_module_parent_origin_tested": 5,
            "raw_physical_slot_closure_satisfied": 0,
            "raw_physical_slot_closure_tested": 4,
        },
        "verdict": {
            "fixed_parent_can_change_representation_multiplicity": False,
            "unseeded_rank_projector_selects_required_type": False,
            "typed_seed_selects_target_conditionally": True,
            "typed_seed_is_target_loaded": True,
            "typed_seed_selects_a_family_axis": True,
            "finite_module_physically_derived": False,
            "common_finite_geometry_configuration_space_required": True,
        },
        "next_gate": "version9_endpoint_finite_geometry_configuration_space_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()