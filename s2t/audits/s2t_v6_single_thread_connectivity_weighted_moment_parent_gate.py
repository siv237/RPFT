#!/usr/bin/env python3
"""Аудит канонического двойственного каркаса для моментов одной нити."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
MOMENT_PARENT = ROOT / "s2t/results/s2t_v6_single_thread_moment_realization_gate_results.json"
PHASE_PARENT = ROOT / "s2t/results/s2t_v6_single_thread_phase_weighted_moment_lift_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_single_thread_connectivity_weighted_moment_parent_gate_results.json"


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


def symmetric_traceless_rank_three(moment: np.ndarray) -> np.ndarray:
    trace = np.einsum("ijj->i", moment)
    identity = np.eye(3)
    return moment - (
        np.einsum("ij,k->ijk", identity, trace)
        + np.einsum("ik,j->ijk", identity, trace)
        + np.einsum("jk,i->ijk", identity, trace)
    ) / 5.0


def mixed_primal_dual_moment(axes: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    frame_operator = np.einsum("a,ai,aj->ij", weights, axes, axes)
    dual_axes = np.linalg.solve(frame_operator, axes.T).T
    moment = np.zeros((3, 3, 3))
    for weight, axis, dual in zip(weights, axes, dual_axes):
        moment += weight * (
            np.einsum("i,j,k->ijk", dual, axis, axis)
            + np.einsum("i,j,k->ijk", axis, dual, axis)
            + np.einsum("i,j,k->ijk", axis, axis, dual)
        ) / 3.0
    return frame_operator, symmetric_traceless_rank_three(moment)


def target_and_metrics(axes: np.ndarray, candidate: np.ndarray) -> tuple[np.ndarray, dict[str, float]]:
    target = sum(np.einsum("i,j,k->ijk", axis, axis, axis) for axis in axes)
    target_flat = target.reshape(-1)
    candidate_flat = candidate.reshape(-1)
    scale = float(np.dot(target_flat, candidate_flat) / np.dot(target_flat, target_flat))
    residual = float(np.linalg.norm(candidate_flat - scale * target_flat) / np.linalg.norm(target_flat))
    cosine = float(
        np.dot(target_flat, candidate_flat)
        / (np.linalg.norm(target_flat) * np.linalg.norm(candidate_flat))
    )
    return target, {
        "best_scale": scale,
        "target_normalized_residual": residual,
        "cosine": cosine,
    }


def exact_c3_identity_certificate() -> dict[str, object]:
    p = sp.symbols("p", positive=True)
    q = (1 - p) / 3
    root3 = sp.sqrt(3)
    axes = [
        sp.Matrix(v) / root3
        for v in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    ]
    weights = [p, q, q, q]
    frame = sum((weight * axis * axis.T for weight, axis in zip(weights, axes)), sp.zeros(3))
    duals = [frame.inv() * axis for axis in axes]

    moment = sp.MutableDenseNDimArray.zeros(3, 3, 3)
    target = sp.MutableDenseNDimArray.zeros(3, 3, 3)
    for weight, axis, dual in zip(weights, axes, duals):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    moment[i, j, k] += weight * (
                        dual[i] * axis[j] * axis[k]
                        + axis[i] * dual[j] * axis[k]
                        + axis[i] * axis[j] * dual[k]
                    ) / 3
                    target[i, j, k] += axis[i] * axis[j] * axis[k]

    trace = [sum(moment[i, j, j] for j in range(3)) for i in range(3)]
    differences = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                stf = moment[i, j, k] - (
                    int(i == j) * trace[k]
                    + int(i == k) * trace[j]
                    + int(j == k) * trace[i]
                ) / 5
                differences.append(sp.simplify(stf - sp.Rational(3, 4) * target[i, j, k]))
    return {
        "symbolic_parameter": "p with q=(1-p)/3",
        "exact_scale": "3/4",
        "number_of_tensor_components": len(differences),
        "all_component_differences_are_zero": all(value == 0 for value in differences),
        "distinct_simplified_differences": sorted({str(value) for value in differences}),
    }


def main() -> None:
    moment_parent = json.loads(MOMENT_PARENT.read_text(encoding="utf-8"))
    phase_parent = json.loads(PHASE_PARENT.read_text(encoding="utf-8"))
    weights = np.array(moment_parent["ordered_second_moment_fit"]["weights"], dtype=float)

    coisometry = affine_coisometry()
    columns = coisometry.T
    axes = columns / np.linalg.norm(columns, axis=1, keepdims=True)
    gram = axes @ axes.T
    p3 = np.eye(4) - np.ones((4, 4)) / 4.0

    frame_operator, dual_candidate = mixed_primal_dual_moment(axes, weights)
    _, working_metrics = target_and_metrics(axes, dual_candidate)
    frame_eigenvalues = np.linalg.eigvalsh(frame_operator)

    rng = np.random.default_rng(20260821)
    scan_records = []
    for sample_weights in rng.dirichlet(np.ones(4), size=256):
        sample_frame, sample_candidate = mixed_primal_dual_moment(axes, sample_weights)
        _, sample_metrics = target_and_metrics(axes, sample_candidate)
        scan_records.append(
            (
                sample_metrics["target_normalized_residual"],
                abs(sample_metrics["best_scale"] - 0.75),
                float(np.linalg.eigvalsh(sample_frame)[0]),
            )
        )
    scan = np.array(scan_records)

    c3_scan_records = []
    for p in np.linspace(1.0e-4, 0.9999, 1001):
        q = (1.0 - p) / 3.0
        sample_weights = np.array([p, q, q, q])
        _, sample_candidate = mixed_primal_dual_moment(axes, sample_weights)
        _, sample_metrics = target_and_metrics(axes, sample_candidate)
        c3_scan_records.append(
            (
                sample_metrics["target_normalized_residual"],
                abs(sample_metrics["best_scale"] - 0.75),
            )
        )
    c3_scan = np.array(c3_scan_records)
    exact_certificate = exact_c3_identity_certificate()

    result = {
        "gate": "version6_single_thread_connectivity_weighted_moment_parent_gate",
        "input": {
            "ordered_weights": weights.tolist(),
            "affine_parent": "canonical 4-to-3 coisometry from version6_existing_multiplicity_resonant_sink_gate",
            "observable": "STF sum_a w_a Sym((R^-1 n_a) tensor n_a tensor n_a)",
        },
        "affine_tetrahedral_frame": {
            "coisometry_rank": int(np.linalg.matrix_rank(coisometry)),
            "V_Vstar_identity_residual": float(np.linalg.norm(coisometry @ coisometry.T - np.eye(3))),
            "Vstar_V_P3_residual": float(np.linalg.norm(coisometry.T @ coisometry - p3)),
            "normalized_column_gram": gram.tolist(),
            "regular_tetrahedron_gram_residual": float(
                np.linalg.norm(gram - (4.0 * np.eye(4) - np.ones((4, 4))) / 3.0)
            ),
        },
        "working_ordered_state": {
            "frame_operator": frame_operator.tolist(),
            "frame_eigenvalues": frame_eigenvalues.tolist(),
            "frame_condition_number": float(frame_eigenvalues[-1] / frame_eigenvalues[0]),
            **working_metrics,
            "expected_exact_scale": 0.75,
            "scale_residual": abs(working_metrics["best_scale"] - 0.75),
            "previous_naive_moment_residual": phase_parent["trivial_character"]["relative_residual"],
            "previous_best_nontrivial_phase_residual": phase_parent["nontrivial_characters"]["best_candidate"]["relative_residual"],
        },
        "positive_weight_robustness": {
            "random_dirichlet_samples": int(scan.shape[0]),
            "maximum_target_normalized_residual": float(np.max(scan[:, 0])),
            "maximum_scale_residual_from_three_quarters": float(np.max(scan[:, 1])),
            "minimum_sampled_frame_eigenvalue": float(np.min(scan[:, 2])),
            "C3_weight_samples": int(c3_scan.shape[0]),
            "C3_maximum_target_normalized_residual": float(np.max(c3_scan[:, 0])),
            "C3_maximum_scale_residual_from_three_quarters": float(np.max(c3_scan[:, 1])),
        },
        "exact_C3_identity": exact_certificate,
        "interpretation_boundary": {
            "R_inverse_role": "canonical dual frame and reconstruction map",
            "R_inverse_used_as_energy_weight": False,
            "new_relative_parameter_added": False,
            "inverse_exists_for_strictly_positive_four_pass_weights": True,
            "dual_frame_diverges_at_rank_loss_boundary": True,
            "local_pass_moment_identity_proves_one_global_cycle": False,
        },
        "verdict": {
            "affine_coisometry_is_tetrahedral_frame": True,
            "canonical_dual_mixed_moment_reproduces_T": True,
            "local_Q_T_moment_bridge_passed": True,
            "single_global_thread_hypothesis_refuted": False,
            "global_single_cycle_sewing_derived": False,
            "matter_birth_fully_derived": False,
            "next_gate": "version6_single_thread_global_cycle_sewing_gate",
        },
    }

    assert result["affine_tetrahedral_frame"]["regular_tetrahedron_gram_residual"] < 2.0e-15
    assert working_metrics["target_normalized_residual"] < 2.0e-15
    assert result["working_ordered_state"]["scale_residual"] < 2.0e-15
    assert result["positive_weight_robustness"]["maximum_target_normalized_residual"] < 2.0e-14
    assert result["positive_weight_robustness"]["C3_maximum_target_normalized_residual"] < 1.0e-12
    assert result["exact_C3_identity"]["all_component_differences_are_zero"]
    assert result["verdict"]["local_Q_T_moment_bridge_passed"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()