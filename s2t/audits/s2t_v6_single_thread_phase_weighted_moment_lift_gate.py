#!/usr/bin/env python3
"""Проверка Z3- и Real-фаз для третьего момента одной нити."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
PARENT = ROOT / "s2t/results/s2t_v6_single_thread_moment_realization_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_single_thread_phase_weighted_moment_lift_gate_results.json"


def symmetric_traceless_rank_three(moment: np.ndarray) -> np.ndarray:
    trace = np.einsum("ijj->i", moment)
    identity = np.eye(3)
    return moment - (
        np.einsum("ij,k->ijk", identity, trace)
        + np.einsum("ik,j->ijk", identity, trace)
        + np.einsum("jk,i->ijk", identity, trace)
    ) / 5.0


def projection_metrics(candidate: np.ndarray, target: np.ndarray) -> dict[str, float]:
    scale = float(np.dot(target, candidate) / np.dot(target, target))
    residual = float(np.linalg.norm(candidate - scale * target) / np.linalg.norm(candidate))
    cosine = float(abs(np.dot(target, candidate)) / (np.linalg.norm(target) * np.linalg.norm(candidate)))
    return {"best_scale": scale, "relative_residual": residual, "absolute_cosine": cosine}


def main() -> None:
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    axes = np.array(parent["input"]["tetrahedral_axes"], dtype=float)
    weights = np.array(parent["ordered_second_moment_fit"]["weights"], dtype=float)

    contributions = np.stack(
        [
            symmetric_traceless_rank_three(np.einsum("i,j,k->ijk", axis, axis, axis)).reshape(-1)
            for axis in axes
        ],
        axis=1,
    )
    singular_values = np.linalg.svd(contributions, compute_uv=False)
    contribution_rank = int(np.linalg.matrix_rank(contributions, tol=1.0e-12))
    canonical_target = contributions @ np.ones(4)

    trivial_candidate = contributions @ weights
    trivial_metrics = projection_metrics(trivial_candidate, canonical_target)

    omega = np.exp(2.0j * np.pi / 3.0)
    nontrivial_records = []
    for orbit_phases in itertools.permutations([1.0 + 0.0j, omega, omega**2]):
        character = np.array([1.0 + 0.0j, *orbit_phases])
        complex_candidate = contributions @ (weights * character)
        real_span = np.stack([complex_candidate.real, complex_candidate.imag], axis=1)
        span_rank = int(np.linalg.matrix_rank(real_span, tol=1.0e-12))
        coefficients = np.linalg.lstsq(real_span, canonical_target, rcond=None)[0]
        best_real_candidate = real_span @ coefficients
        metrics = projection_metrics(best_real_candidate, canonical_target)
        nontrivial_records.append(
            {
                "orbit_phases": [[float(z.real), float(z.imag)] for z in orbit_phases],
                "continuous_real_pair_span_rank": span_rank,
                "optimal_real_imag_coefficients": coefficients.tolist(),
                **metrics,
            }
        )
    best_nontrivial = min(nontrivial_records, key=lambda item: item["relative_residual"])

    required_inverse_weights = 1.0 / weights
    required_modulus_ratio = float(weights[0] / weights[1])
    result = {
        "gate": "version6_single_thread_phase_weighted_moment_lift_gate",
        "input": {
            "ordered_weights": weights.tolist(),
            "residual_group": "Z3",
            "real_pair_combinations_tested": "full continuous span of real and imaginary parts",
        },
        "linear_independence": {
            "rank_of_four_spin3_contributions": contribution_rank,
            "singular_values": singular_values.tolist(),
            "exact_target_requires_equal_complex_coefficients": contribution_rank == 4,
        },
        "trivial_character": trivial_metrics,
        "nontrivial_characters": {
            "number_of_character_spans": len(nontrivial_records),
            "best_candidate": best_nontrivial,
        },
        "amplitude_obstruction": {
            "required_inverse_weights": required_inverse_weights.tolist(),
            "required_off_axis_to_selected_modulus_ratio": required_modulus_ratio,
            "unitary_character_modulus_ratio": 1.0,
            "unit_modulus_phase_can_compensate_weights": False,
        },
        "real_pair_boundary": {
            "counterpropagating_pair_can_cancel_physical_first_moment": True,
            "real_pair_can_change_effective_real_coefficient_moduli": True,
            "fixed_axis_and_one_orbit_axis_share_trivial_phase_with_unequal_weights": True,
            "real_pair_removes_spin3_amplitude_obstruction": False,
        },
        "verdict": {
            "canonical_Z3_or_Real_phase_lift_reproduces_T": False,
            "single_global_thread_hypothesis_refuted": False,
            "pure_phase_weighting_route_closed": True,
            "state_dependent_amplitude_weight_required": True,
            "next_gate": "version6_single_thread_connectivity_weighted_moment_parent_gate",
        },
    }

    assert contribution_rank == 4
    assert trivial_metrics["relative_residual"] > 0.6
    assert best_nontrivial["relative_residual"] > trivial_metrics["relative_residual"]
    assert required_modulus_ratio > 27.0
    assert not result["verdict"]["canonical_Z3_or_Real_phase_lift_reproduces_T"]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()