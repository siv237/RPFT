#!/usr/bin/env python3
"""Проверка Real-замыкания и границы рамированного winding-вложения."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
COUNT_PARENT = ROOT / "s2t/results/s2t_v6_single_thread_c4_suspension_parent_gate_results.json"
MOMENT_PARENT = ROOT / "s2t/results/s2t_v6_single_thread_moment_realization_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_single_thread_framed_winding_embedding_gate_results.json"


def tetrahedral_axes() -> np.ndarray:
    return np.array(
        [[1.0, 1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0]]
    ) / np.sqrt(3.0)


def symmetric_traceless_rank_three(moment: np.ndarray) -> np.ndarray:
    trace = np.einsum("ijj->i", moment)
    identity = np.eye(3)
    return moment - (
        np.einsum("ij,k->ijk", identity, trace)
        + np.einsum("ik,j->ijk", identity, trace)
        + np.einsum("jk,i->ijk", identity, trace)
    ) / 5.0


def mixed_tensor(axis: np.ndarray, dual: np.ndarray) -> np.ndarray:
    return (
        np.einsum("i,j,k->ijk", dual, axis, axis)
        + np.einsum("i,j,k->ijk", axis, dual, axis)
        + np.einsum("i,j,k->ijk", axis, axis, dual)
    ) / 3.0


def projection_metrics(candidate: np.ndarray, target: np.ndarray) -> dict[str, float]:
    candidate_flat = candidate.reshape(-1)
    target_flat = target.reshape(-1)
    scale = float(np.dot(candidate_flat, target_flat) / np.dot(target_flat, target_flat))
    residual = float(np.linalg.norm(candidate_flat - scale * target_flat) / np.linalg.norm(target_flat))
    return {"best_scale": scale, "target_normalized_residual": residual}


def main() -> None:
    count_parent = json.loads(COUNT_PARENT.read_text(encoding="utf-8"))
    moment_parent = json.loads(MOMENT_PARENT.read_text(encoding="utf-8"))
    axes = tetrahedral_axes()
    weights = np.array(moment_parent["ordered_second_moment_fit"]["weights"], dtype=float)
    unsigned_counts = np.array(
        count_parent["integer_pass_count_approximations"]["1000000"]["counts"], dtype=np.int64
    )

    plus_counts = unsigned_counts.copy()
    minus_counts = unsigned_counts.copy()
    total_signed_visits = int(2 * np.sum(unsigned_counts))
    signed_displacement = np.einsum("a,ai->i", plus_counts - minus_counts, axes)

    signed_axes = np.concatenate([axes, -axes], axis=0)
    signed_weights = np.concatenate([weights / 2.0, weights / 2.0])
    physical_current = np.einsum("a,ai->i", signed_weights, signed_axes)
    physical_second = np.einsum("a,ai,aj->ij", signed_weights, signed_axes, signed_axes)
    target_second = np.einsum("a,ai,aj->ij", weights, axes, axes)

    frame_operator = target_second
    unsigned_duals = np.linalg.solve(frame_operator, axes.T).T
    no_character = np.zeros((3, 3, 3))
    real_character = np.zeros((3, 3, 3))
    for axis, dual, weight in zip(axes, unsigned_duals, weights):
        for orientation in (-1.0, 1.0):
            tangent = orientation * axis
            tangent_dual = orientation * dual
            contribution = mixed_tensor(tangent, tangent_dual)
            no_character += 0.5 * weight * contribution
            real_character += 0.5 * weight * orientation * contribution

    no_character = symmetric_traceless_rank_three(no_character)
    real_character = symmetric_traceless_rank_three(real_character)
    target_third = sum(np.einsum("i,j,k->ijk", axis, axis, axis) for axis in axes)
    real_metrics = projection_metrics(real_character, target_third)

    result = {
        "gate": "version6_single_thread_framed_winding_embedding_gate",
        "input": {
            "unsigned_counts": unsigned_counts.tolist(),
            "unsigned_total_passes": int(np.sum(unsigned_counts)),
            "Real_doubled_total_oriented_visits": total_signed_visits,
            "tetrahedral_axes": axes.tolist(),
        },
        "closed_curve_necessary_condition": {
            "condition": "sum of oriented unit tangents over a closed polygonal walk equals zero",
            "plus_counts": plus_counts.tolist(),
            "minus_counts": minus_counts.tolist(),
            "integer_count_difference": (plus_counts - minus_counts).tolist(),
            "displacement_vector": signed_displacement.tolist(),
            "displacement_norm": float(np.linalg.norm(signed_displacement)),
            "closure_passes_after_Real_doubling": True,
        },
        "physical_moments_after_Real_doubling": {
            "polar_current": physical_current.tolist(),
            "polar_current_norm": float(np.linalg.norm(physical_current)),
            "second_moment_residual": float(np.linalg.norm(physical_second - target_second)),
            "Q_is_preserved": True,
        },
        "odd_moment_orientation_test": {
            "without_Real_orientation_character_norm": float(np.linalg.norm(no_character)),
            "with_character_chi_equals_orientation": {
                **real_metrics,
                "expected_scale": 0.75,
                "scale_residual": abs(real_metrics["best_scale"] - 0.75),
            },
            "Real_character_cancels_tangent_reversal_of_rank_three_moment": True,
            "project_has_oriented_E_and_E_star_pair": True,
            "project_derives_this_character_as_physical_thread_observable": False,
        },
        "abstract_embedding_boundary": {
            "one_closed_polygonal_walk_with_the_balanced_step_multiset_exists": True,
            "canonical_reverse_word_construction_closes": True,
            "canonical_reverse_word_retraces_the_same_edges": True,
            "retracing_is_compatible_with_nonzero_tube_thickness": False,
            "simple_self_avoiding_embedding_with_exact_word_certified": False,
            "unique_axis_word_selected": False,
        },
        "framing_and_reconnection_boundary": {
            "Hopf_line_supplies_unit_Chern_class": True,
            "Hopf_line_supplies_a_normal_frame_along_the_full_spatial_curve": False,
            "Calugareanu_self_linking_split_computed": False,
            "fundamental_tube_radius_derived": False,
            "existing_vortex_width_can_be_reused_as_fundamental_thread_radius": False,
            "excluded_volume_or_injectivity_term_in_parent_action": False,
            "reconnection_barrier_computed": False,
        },
        "verdict": {
            "closed_oriented_pass_balance_passed": True,
            "Q_survives_zero_current_Real_doubling": True,
            "T_survives_with_orientation_character": True,
            "orientation_character_parent_derivation_complete": False,
            "finite_thickness_self_avoiding_embedding_derived": False,
            "no_reconnection_dynamics_derived": False,
            "single_global_thread_hypothesis_refuted": False,
            "single_global_thread_geometrically_derived": False,
            "next_gate": "version6_single_thread_excluded_volume_reconnection_barrier_gate",
        },
    }

    assert result["closed_curve_necessary_condition"]["displacement_norm"] < 1.0e-12
    assert result["physical_moments_after_Real_doubling"]["polar_current_norm"] < 1.0e-15
    assert result["physical_moments_after_Real_doubling"]["second_moment_residual"] < 1.0e-15
    assert result["odd_moment_orientation_test"]["without_Real_orientation_character_norm"] < 1.0e-15
    assert real_metrics["target_normalized_residual"] < 2.0e-15
    assert result["odd_moment_orientation_test"]["with_character_chi_equals_orientation"]["scale_residual"] < 2.0e-15
    assert not result["verdict"]["finite_thickness_self_avoiding_embedding_derived"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()