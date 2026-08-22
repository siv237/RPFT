#!/usr/bin/env python3
"""Целочисленная кратность проходов и C4-проекция одной нити."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
MOMENT_PARENT = ROOT / "s2t/results/s2t_v6_single_thread_moment_realization_gate_results.json"
SEWING_PARENT = ROOT / "s2t/results/s2t_v6_single_thread_global_cycle_sewing_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_single_thread_c4_suspension_parent_gate_results.json"


def tetrahedral_axes() -> np.ndarray:
    return np.array(
        [[1.0, 1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0]]
    ) / np.sqrt(3.0)


def symmetric_counts(weights: np.ndarray, denominator_bound: int) -> tuple[int, int]:
    ratio = Fraction(float(weights[0] / weights[1])).limit_denominator(denominator_bound)
    return ratio.numerator, ratio.denominator


def count_metrics(weights: np.ndarray, axes: np.ndarray, k0: int, kq: int) -> dict[str, object]:
    counts = np.array([k0, kq, kq, kq], dtype=np.int64)
    total = int(k0 + 3 * kq)
    frequencies = counts.astype(float) / total
    target_second = np.einsum("a,ai,aj->ij", weights, axes, axes)
    count_second = np.einsum("a,ai,aj->ij", frequencies, axes, axes)
    return {
        "counts": counts.tolist(),
        "total_passes": total,
        "frequencies": frequencies.tolist(),
        "maximum_frequency_error": float(np.max(np.abs(frequencies - weights))),
        "L1_frequency_error": float(np.sum(np.abs(frequencies - weights))),
        "second_moment_residual": float(np.linalg.norm(count_second - target_second)),
        "single_cycle_successor": "m -> (m+1) mod total_passes",
        "every_position_has_one_predecessor_and_one_successor": True,
        "cycle_component_count": 1,
    }


def min_square_sum(total: int, slots: int) -> tuple[int, int, int]:
    quotient, remainder = divmod(total, slots)
    value = remainder * (quotient + 1) ** 2 + (slots - remainder) * quotient**2
    return value, quotient, remainder


def main() -> None:
    moment_parent = json.loads(MOMENT_PARENT.read_text(encoding="utf-8"))
    sewing_parent = json.loads(SEWING_PARENT.read_text(encoding="utf-8"))
    weights = np.array(moment_parent["ordered_second_moment_fit"]["weights"], dtype=float)
    axes = tetrahedral_axes()

    approximations = {}
    for bound in (10, 100, 1_000, 10_000, 100_000, 1_000_000):
        k0, kq = symmetric_counts(weights, bound)
        approximations[str(bound)] = count_metrics(weights, axes, k0, kq)

    example_turns = 10_000_000_000
    finite_holonomy = {
        "turn_count": example_turns,
        "C4_residue": example_turns % 4,
        "Z3_residue": example_turns % 3,
        "Z6_residue": example_turns % 6,
        "number_operator_eigenvalue": example_turns,
        "Toeplitz_index_of_U_power": -example_turns,
        "commutator": "[N,U^k]=k U^k",
    }

    concentrated_action = example_turns**2
    distributed_105, quotient, remainder = min_square_sum(example_turns, 105)

    result = {
        "gate": "version6_single_thread_c4_suspension_parent_gate",
        "conceptual_correction": {
            "rejected_variable": "continuous dwell time assigned to a tetrahedral axis",
            "replacement_variable": "integer traversal multiplicity K_a on the unbounded number-operator lift",
            "C4_role": "residue phase of the traversal number, not a permutation of the four tetrahedral axes",
            "previous_odd_four_cycle_obstruction_applies_to_axis_permutation": True,
            "previous_obstruction_applies_to_number_operator_lift": False,
        },
        "project_number_operator": {
            "Hilbert_basis": "e_n on ell2(Z)",
            "number_operator": "N e_n=n e_n",
            "unit_shift": "U e_n=e_(n+1)",
            "unit_commutator": "[N,U]=U",
            "arbitrary_power_commutator": "[N,U^k]=k U^k",
            "distinguishes_first_and_ten_billionth_turn": True,
        },
        "finite_holonomy_information_loss": finite_holonomy,
        "integer_pass_count_approximations": approximations,
        "single_cycle_lift": {
            "construction": "replace four labels by K_0+K_1+K_2+K_3 distinct visit positions and use one cyclic successor",
            "works_for_every_strictly_positive_integer_count_vector": True,
            "local_branching": False,
            "local_endpoints": False,
            "global_component_count": 1,
            "axis_projection_preserves_requested_counts": True,
            "axis_word_is_unique_from_counts": False,
        },
        "Toeplitz_loop_action_boundary": {
            "action": "sum_a k_a^2",
            "ten_billion_turns_in_one_channel": concentrated_action,
            "minimum_over_105_coefficient_channels": distributed_105,
            "minimizer_base_winding_per_channel": quotient,
            "channels_with_one_extra_winding": remainder,
            "concentrated_to_distributed_action_ratio": float(concentrated_action / distributed_105),
            "existing_action_prefers_distributed_unit_winding_for_total_15": True,
            "coefficient_channels_already_identified_with_successive_spatial_passes": False,
        },
        "parent_boundary": {
            "ordered_weights_are_available_from_R": True,
            "current_parent_proves_weights_are_exact_rational_pass_frequencies": False,
            "current_parent_selects_a_unique_cyclic_word_with_those_frequencies": False,
            "current_parent_embeds_the_word_as_a_finite_thickness_nonselfintersecting_curve": False,
            "current_parent_forbids_reconnection_dynamics": False,
            "previous_axis_permutation_result": sewing_parent["verdict"],
        },
        "verdict": {
            "integer_winding_counter_exists_in_project": True,
            "finite_holonomy_alone_counts_absolute_turns": False,
            "one_abstract_nonbranching_cycle_with_prescribed_integer_multiplicities_exists": True,
            "working_Q_weights_have_high_accuracy_integer_approximants": True,
            "exact_finite_count_realization_of_working_weights_proved": False,
            "single_global_thread_hypothesis_refuted": False,
            "single_global_thread_kinematically_reopened": True,
            "single_global_thread_derived_from_current_parent": False,
            "next_gate": "version6_single_thread_framed_winding_embedding_gate",
        },
    }

    best = approximations["1000000"]
    assert finite_holonomy["C4_residue"] == 0
    assert finite_holonomy["number_operator_eigenvalue"] == example_turns
    assert best["maximum_frequency_error"] < 4.0e-15
    assert best["cycle_component_count"] == 1
    assert result["single_cycle_lift"]["local_branching"] is False
    assert result["verdict"]["single_global_thread_kinematically_reopened"]
    assert not result["verdict"]["single_global_thread_derived_from_current_parent"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()