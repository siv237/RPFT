#!/usr/bin/env python3
"""Моментная реализация Q и T локальными проходами одной нити."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
THERMAL_RESULT = ROOT / "s2t/results/s2t_v6_tensor_square_relative_carrier_normalization_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_single_thread_moment_realization_gate_results.json"


def tetrahedral_axes() -> np.ndarray:
    return np.array(
        [[1.0, 1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0]]
    ) / np.sqrt(3.0)


def symmetric_traceless_rank_three(moment: np.ndarray) -> np.ndarray:
    trace = np.einsum("ijj->i", moment)
    identity = np.eye(3)
    trace_part = (
        np.einsum("ij,k->ijk", identity, trace)
        + np.einsum("ik,j->ijk", identity, trace)
        + np.einsum("jk,i->ijk", identity, trace)
    ) / 5.0
    return moment - trace_part


def main() -> None:
    thermal = json.loads(THERMAL_RESULT.read_text(encoding="utf-8"))["thermal_reopening"]
    ordered_spectrum = np.array(thermal["coexistence_ordered_spectrum"], dtype=float)
    longitudinal, transverse = ordered_spectrum[0], ordered_spectrum[1]
    axes = tetrahedral_axes()
    director = axes[0]
    projector = np.outer(director, director)
    target_second_moment = longitudinal * projector + transverse * (np.eye(3) - projector)

    selected_weight = float((9.0 * longitudinal - 1.0) / 8.0)
    other_weight = float((1.0 - selected_weight) / 3.0)
    ordered_weights = np.array([selected_weight, other_weight, other_weight, other_weight])
    first_moment = np.einsum("a,ai->i", ordered_weights, axes)
    second_moment = np.einsum("a,ai,aj->ij", ordered_weights, axes, axes)
    raw_third_moment = np.einsum("a,ai,aj,ak->ijk", ordered_weights, axes, axes, axes)
    third_moment = symmetric_traceless_rank_three(raw_third_moment)

    canonical_third_moment = np.einsum("ai,aj,ak->ijk", axes, axes, axes)
    best_scale = float(
        np.sum(third_moment * canonical_third_moment)
        / np.sum(canonical_third_moment * canonical_third_moment)
    )
    third_residual = float(
        np.linalg.norm(third_moment - best_scale * canonical_third_moment)
        / np.linalg.norm(third_moment)
    )
    third_cosine = float(
        np.sum(third_moment * canonical_third_moment)
        / (np.linalg.norm(third_moment) * np.linalg.norm(canonical_third_moment))
    )

    conservation_matrix = np.vstack([np.ones(4), axes.T])
    balanced_weights = np.linalg.solve(conservation_matrix, np.array([1.0, 0.0, 0.0, 0.0]))
    balanced_first_moment = np.einsum("a,ai->i", balanced_weights, axes)
    balanced_second_moment = np.einsum("a,ai,aj->ij", balanced_weights, axes, axes)
    balanced_q = balanced_second_moment - np.eye(3) / 3.0
    balanced_third_moment = np.einsum("a,ai,aj,ak->ijk", balanced_weights, axes, axes, axes)

    paired_axes = np.concatenate([axes, -axes], axis=0)
    paired_weights = np.full(8, 1.0 / 8.0)
    paired_first_moment = np.einsum("a,ai->i", paired_weights, paired_axes)
    paired_third_moment = np.einsum(
        "a,ai,aj,ak->ijk", paired_weights, paired_axes, paired_axes, paired_axes
    )

    result = {
        "gate": "version6_single_thread_moment_realization_gate",
        "input": {
            "ordered_spectrum": ordered_spectrum.tolist(),
            "tetrahedral_axes": axes.tolist(),
            "same_nonnegative_local_pass_distribution_assumed": True,
        },
        "ordered_second_moment_fit": {
            "weights": ordered_weights.tolist(),
            "weights_nonnegative": bool(np.all(ordered_weights >= 0.0)),
            "sum_weights": float(np.sum(ordered_weights)),
            "second_moment_residual": float(np.linalg.norm(second_moment - target_second_moment)),
            "polar_first_moment": first_moment.tolist(),
            "polar_first_moment_norm": float(np.linalg.norm(first_moment)),
            "third_moment_best_scale_to_canonical_T": best_scale,
            "third_moment_cosine_to_canonical_T": third_cosine,
            "third_moment_relative_residual_after_best_scale": third_residual,
        },
        "zero_polar_current_solution": {
            "constraint_matrix_rank": int(np.linalg.matrix_rank(conservation_matrix)),
            "unique_weights": balanced_weights.tolist(),
            "first_moment_norm": float(np.linalg.norm(balanced_first_moment)),
            "quadrupole_norm": float(np.linalg.norm(balanced_q)),
            "third_moment_norm": float(np.linalg.norm(balanced_third_moment)),
            "ordered_Q_reproduced": False,
            "canonical_T_reproduced_up_to_factor": True,
        },
        "head_tail_real_pair": {
            "first_moment_norm": float(np.linalg.norm(paired_first_moment)),
            "third_moment_norm": float(np.linalg.norm(paired_third_moment)),
            "canonical_T_reproduced": False,
        },
        "verdict": {
            "raw_common_distribution_realizes_Q_T_and_zero_current": False,
            "single_global_thread_hypothesis_refuted": False,
            "Q_and_T_require_distinct_weightings_or_observables": True,
            "minimal_refinement": "phase- or connectivity-weighted third moment on the same thread",
            "next_gate": "version6_single_thread_phase_weighted_moment_lift_gate",
        },
    }

    assert result["ordered_second_moment_fit"]["second_moment_residual"] < 1.0e-14
    assert result["ordered_second_moment_fit"]["polar_first_moment_norm"] > 0.8
    assert result["zero_polar_current_solution"]["quadrupole_norm"] < 1.0e-14
    assert result["zero_polar_current_solution"]["third_moment_norm"] > 0.4
    assert result["head_tail_real_pair"]["third_moment_norm"] < 1.0e-14
    assert result["ordered_second_moment_fit"]["third_moment_relative_residual_after_best_scale"] > 0.6
    assert not result["verdict"]["raw_common_distribution_realizes_Q_T_and_zero_current"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()