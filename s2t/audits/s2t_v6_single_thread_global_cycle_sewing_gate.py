#!/usr/bin/env python3
"""Перебор локальных сшивок проходов одной глобальной нити."""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
PARENT = ROOT / "s2t/results/s2t_v6_single_thread_connectivity_weighted_moment_parent_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_single_thread_global_cycle_sewing_gate_results.json"


def affine_coisometry() -> np.ndarray:
    return np.array(
        [
            [1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0), 0.0, 0.0],
            [1.0 / np.sqrt(6.0), 1.0 / np.sqrt(6.0), -2.0 / np.sqrt(6.0), 0.0],
            [
                1.0 / np.sqrt(12.0),
                1.0 / np.sqrt(12.0),
                1.0 / np.sqrt(12.0),
                -3.0 / np.sqrt(12.0),
            ],
        ]
    )


def parity(perm: tuple[int, ...]) -> int:
    inversions = sum(
        perm[i] > perm[j]
        for i in range(len(perm))
        for j in range(i + 1, len(perm))
    )
    return 1 if inversions % 2 == 0 else -1


def cycles(perm: tuple[int, ...]) -> list[list[int]]:
    unseen = set(range(len(perm)))
    answer = []
    while unseen:
        start = min(unseen)
        cycle = []
        current = start
        while current in unseen:
            unseen.remove(current)
            cycle.append(current)
            current = perm[current]
        answer.append(cycle)
    return answer


def cycle_type(perm: tuple[int, ...]) -> str:
    return "+".join(str(length) for length in sorted((len(c) for c in cycles(perm)), reverse=True))


def permutation_matrix(perm: tuple[int, ...]) -> np.ndarray:
    matrix = np.zeros((len(perm), len(perm)))
    for source, target in enumerate(perm):
        matrix[target, source] = 1.0
    return matrix


def inverse_permutation(perm: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(perm)
    for source, target in enumerate(perm):
        inverse[target] = source
    return tuple(inverse)


def lifted_permutation(perm: tuple[int, ...], mode: str) -> tuple[int, ...]:
    inverse = inverse_permutation(perm)
    lifted = []
    for orientation in range(2):
        for axis in range(4):
            if mode == "diagonal":
                target_axis, target_orientation = perm[axis], orientation
            elif mode == "Real_flip":
                target_axis, target_orientation = perm[axis], 1 - orientation
            elif mode == "arrow_reversal":
                target_axis = perm[axis] if orientation == 0 else inverse[axis]
                target_orientation = 1 - orientation
            else:
                raise ValueError(mode)
            lifted.append(4 * target_orientation + target_axis)
    return tuple(lifted)


def induced_tetrahedral_map(axes: np.ndarray, perm: tuple[int, ...]) -> np.ndarray:
    return 0.75 * sum(np.outer(axes[perm[a]], axes[a]) for a in range(4))


def main() -> None:
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    weights = np.array(parent["input"]["ordered_weights"], dtype=float)
    coisometry = affine_coisometry()
    axes = coisometry.T
    axes = axes / np.linalg.norm(axes, axis=1, keepdims=True)

    permutations = list(itertools.permutations(range(4)))
    even = [perm for perm in permutations if parity(perm) == 1]
    four_cycles = [perm for perm in permutations if cycle_type(perm) == "4"]
    weight_stabilizer = [
        perm
        for perm in permutations
        if np.linalg.norm(permutation_matrix(perm) @ weights - weights) < 1.0e-12
    ]

    induced_residuals = []
    determinant_parity_residuals = []
    for perm in permutations:
        orthogonal = induced_tetrahedral_map(axes, perm)
        induced_residuals.append(
            max(np.linalg.norm(orthogonal @ axes[a] - axes[perm[a]]) for a in range(4))
        )
        determinant_parity_residuals.append(abs(np.linalg.det(orthogonal) - parity(perm)))

    z3 = (0, 2, 3, 1)
    c4 = (1, 2, 3, 0)
    c4_matrix = permutation_matrix(c4)
    c4_map = induced_tetrahedral_map(axes, c4)

    lift_records = {}
    for mode in ("diagonal", "Real_flip", "arrow_reversal"):
        all_lifts = [lifted_permutation(perm, mode) for perm in permutations]
        proper_lifts = [lifted_permutation(perm, mode) for perm in even]
        lift_records[mode] = {
            "all_S4_lifts": len(all_lifts),
            "all_S4_single_8_cycles": sum(cycle_type(lift) == "8" for lift in all_lifts),
            "proper_A4_lifts": len(proper_lifts),
            "proper_A4_single_8_cycles": sum(cycle_type(lift) == "8" for lift in proper_lifts),
            "C4_lift_cycle_type": cycle_type(lifted_permutation(c4, mode)),
            "Z3_lift_cycle_type": cycle_type(lifted_permutation(z3, mode)),
        }

    result = {
        "gate": "version6_single_thread_global_cycle_sewing_gate",
        "input": {
            "local_pass_labels": 4,
            "ordered_weights": weights.tolist(),
            "microscopic_no_branching_rule": "one incoming label maps to exactly one outgoing label",
            "candidate_rule_class": "permutations of four tetrahedral pass labels and standard Real lifts",
        },
        "S4_enumeration": {
            "permutation_count": len(permutations),
            "cycle_type_counts": dict(sorted(Counter(cycle_type(perm) for perm in permutations).items())),
            "single_four_cycle_count": len(four_cycles),
            "all_single_four_cycles_are_odd": all(parity(perm) == -1 for perm in four_cycles),
            "maximum_tetrahedral_map_residual": float(max(induced_residuals)),
            "maximum_determinant_parity_residual": float(max(determinant_parity_residuals)),
        },
        "proper_tetrahedral_A4": {
            "element_count": len(even),
            "cycle_type_counts": dict(sorted(Counter(cycle_type(perm) for perm in even).items())),
            "single_four_cycle_count": sum(cycle_type(perm) == "4" for perm in even),
            "maximum_orbit_size": max(max(len(c) for c in cycles(perm)) for perm in even),
            "one_step_single_cycle_available": False,
        },
        "ordered_weight_stabilizer": {
            "element_count": len(weight_stabilizer),
            "cycle_type_counts": dict(sorted(Counter(cycle_type(perm) for perm in weight_stabilizer).items())),
            "selected_axis_fixed_by_every_element": all(perm[0] == 0 for perm in weight_stabilizer),
            "single_four_cycle_count": sum(cycle_type(perm) == "4" for perm in weight_stabilizer),
            "maximum_orbit_size": max(max(len(c) for c in cycles(perm)) for perm in weight_stabilizer),
        },
        "canonical_generators": {
            "residual_Z3": {
                "permutation": list(z3),
                "cycle_type": cycle_type(z3),
                "cycles": cycles(z3),
                "parity": parity(z3),
                "preserves_ordered_weights": bool(np.linalg.norm(permutation_matrix(z3) @ weights - weights) < 1.0e-12),
            },
            "order_four_shift": {
                "permutation": list(c4),
                "cycle_type": cycle_type(c4),
                "cycles": cycles(c4),
                "parity": parity(c4),
                "induced_orthogonal_determinant": float(np.linalg.det(c4_map)),
                "belongs_to_SO3_tetrahedral_A4": False,
                "ordered_weight_stationarity_residual": float(np.linalg.norm(c4_matrix @ weights - weights)),
                "can_reproduce_ordered_weights_with_nonuniform_dwell_times": True,
                "project_derives_required_axis_dwell_suspension": False,
            },
        },
        "standard_Real_doubled_lifts": lift_records,
        "coisometry_boundary": {
            "shape": list(coisometry.shape),
            "rank": int(np.linalg.matrix_rank(coisometry)),
            "kernel_dimension": int(coisometry.shape[1] - np.linalg.matrix_rank(coisometry)),
            "is_bijection_of_four_pass_labels": False,
            "can_serve_as_moment_frame": True,
            "can_by_itself_serve_as_no_reconnection_sewing": False,
        },
        "continuity_boundary": {
            "local_in_degree_equals_out_degree_for_every_permutation": True,
            "number_conservation_implies_single_global_cycle": False,
            "project_currently_contains_parent_transition_permutation": False,
            "project_currently_contains_ambient_isotopy_or_excluded_crossing_law": False,
            "topological_vortex_charge_forbids_arbitrary_free_endpoint_in_ordered_bulk": True,
            "topological_vortex_charge_forbids_reconnection_or_loop_shrinkage": False,
        },
        "verdict": {
            "four_pass_local_no_branching_is_mathematically_possible": True,
            "existing_residual_Z3_sews_one_global_cycle": False,
            "proper_tetrahedral_A4_sews_one_global_cycle": False,
            "existing_standard_Real_lifts_sew_one_global_cycle": False,
            "order_four_shift_is_single_cycle": True,
            "order_four_shift_is_already_valid_parent_sewing": False,
            "single_global_thread_hypothesis_refuted": False,
            "single_global_thread_derived_from_current_parent": False,
            "no_reconnection_dynamics_derived": False,
            "next_gate": "version6_single_thread_c4_suspension_parent_gate",
        },
    }

    assert len(permutations) == 24
    assert len(even) == 12
    assert len(four_cycles) == 6
    assert result["S4_enumeration"]["all_single_four_cycles_are_odd"]
    assert result["proper_tetrahedral_A4"]["single_four_cycle_count"] == 0
    assert result["ordered_weight_stabilizer"]["single_four_cycle_count"] == 0
    assert result["canonical_generators"]["residual_Z3"]["cycle_type"] == "3+1"
    assert result["canonical_generators"]["order_four_shift"]["cycle_type"] == "4"
    assert all(record["all_S4_single_8_cycles"] == 0 for record in lift_records.values())
    assert result["S4_enumeration"]["maximum_tetrahedral_map_residual"] < 2.0e-15
    assert result["S4_enumeration"]["maximum_determinant_parity_residual"] < 2.0e-15

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()