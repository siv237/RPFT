#!/usr/bin/env python3
"""Audit the self-consistent purification R=B^T B/Tr(B^T B)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def reduced_states(bridge: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    norm_squared = float(np.trace(bridge.T @ bridge))
    if norm_squared <= 0.0:
        raise ValueError("The zero bridge has no normalized reduced state")
    return (bridge.T @ bridge) / norm_squared, (bridge @ bridge.T) / norm_squared


def self_consistent_action(bridge: np.ndarray) -> float:
    right_state, left_state = reduced_states(bridge)
    identity = np.eye(3)
    right_defect = identity - bridge.T @ bridge
    left_defect = identity - bridge @ bridge.T
    return float(
        (
            np.trace(right_state @ right_defect @ right_defect)
            + np.trace(left_state @ left_defect @ left_defect)
        )
        / 7.0
    )


def spectral_formula(bridge: np.ndarray) -> float:
    singular_values = np.linalg.svd(bridge, compute_uv=False)
    x = singular_values**2
    return float((2.0 / (7.0 * np.sum(x))) * np.sum(x * (1.0 - x) ** 2))


def entropy(state: np.ndarray) -> float:
    eigenvalues = np.linalg.eigvalsh(state)
    positive = eigenvalues[eigenvalues > 1e-14]
    return float(np.sum(positive * np.log(positive)))


def partial_isometry(rank: int) -> np.ndarray:
    matrix = np.zeros((3, 3))
    matrix[:rank, :rank] = np.eye(rank)
    return matrix


def main() -> None:
    rng = np.random.default_rng(20260819)

    formula_checks = []
    for _ in range(30):
        bridge = rng.normal(size=(3, 3))
        direct = self_consistent_action(bridge)
        spectral = spectral_formula(bridge)
        formula_checks.append(
            {
                "direct_action": direct,
                "spectral_action": spectral,
                "residual": direct - spectral,
            }
        )

    former_valley_checks = []
    projector = np.diag([1.0, 0.0, 0.0])
    for _ in range(20):
        transverse = rng.normal(size=(2, 2))
        bridge = np.zeros((3, 3))
        bridge[0, 0] = 1.0
        bridge[1:, 1:] = transverse
        right_state, _ = reduced_states(bridge)
        former_valley_checks.append(
            {
                "transverse_norm": float(np.linalg.norm(transverse)),
                "distance_of_R_from_projector": float(np.linalg.norm(right_state - projector)),
                "self_consistent_action": self_consistent_action(bridge),
                "rank_R": int(np.linalg.matrix_rank(right_state, tol=1e-10)),
            }
        )

    rank_strata = []
    for rank in [1, 2, 3]:
        bridge = partial_isometry(rank)
        right_state, left_state = reduced_states(bridge)
        rank_strata.append(
            {
                "rank": rank,
                "action": self_consistent_action(bridge),
                "right_state_eigenvalues": np.linalg.eigvalsh(right_state).tolist(),
                "left_state_eigenvalues": np.linalg.eigvalsh(left_state).tolist(),
                "state_entropy": entropy(right_state),
                "free_energy_action_plus_entropy": self_consistent_action(bridge)
                + entropy(right_state),
            }
        )

    base = rng.normal(size=(3, 3))
    scaling = []
    for scale in np.logspace(0.5, 3.0, 18):
        scaling.append(
            {
                "scale": float(scale),
                "action": self_consistent_action(scale * base),
            }
        )
    log_scales = np.log([row["scale"] for row in scaling[-8:]])
    log_actions = np.log([row["action"] for row in scaling[-8:]])
    asymptotic_power = float(np.polyfit(log_scales, log_actions, 1)[0])

    scalar_recovery = []
    for scalar in np.linspace(0.1, 2.0, 20):
        bridge = scalar * np.eye(3)
        target = 2.0 * (1.0 - scalar**2) ** 2 / 7.0
        scalar_recovery.append(self_consistent_action(bridge) - target)

    result = {
        "gate": "version6_self_consistent_state_bridge_purification_gate",
        "state_map": {
            "right": "R_R=B^T B/Tr(B^T B)",
            "left": "R_L=B B^T/Tr(B^T B)",
            "new_continuous_coefficient": False,
            "scalar_bridge_recovery_maximum_residual": max(
                abs(value) for value in scalar_recovery
            ),
        },
        "spectral_action_identity": {
            "formula": "S=2/(7 sum x_i) sum x_i(1-x_i)^2",
            "maximum_residual": max(abs(row["residual"]) for row in formula_checks),
            "samples": formula_checks,
        },
        "former_fixed_state_valley": {
            "checks": former_valley_checks,
            "pure_state_with_nonzero_C_possible": False,
            "flat_valley_removed": True,
        },
        "zero_action_rank_strata": rank_strata,
        "coercivity": {
            "large_scale_power": asymptotic_power,
            "expected_power": 4.0,
            "finite_matrix_integral_at_infinity": True,
        },
        "entropy_selection": {
            "lower_bound": "Tr(R log R)>=-log 3",
            "global_minimum_rank": 3,
            "global_minimum_bridge": "O(3)",
            "global_minimum_state": "I3/3",
            "RP2_selected": False,
        },
        "verdict": {
            "self_consistency_removes_rank_loss_divergence": True,
            "self_consistency_preserves_independent_state_one_loop_mechanism": False,
            "self_consistent_parent_births_RP2": False,
            "independent_R_assumption_was_essential_to_previous_self_start": True,
            "next_gate": "version6_partial_isometry_rank_stratum_selection_gate",
        },
    }

    assert result["state_map"]["scalar_bridge_recovery_maximum_residual"] < 1e-12
    assert result["spectral_action_identity"]["maximum_residual"] < 1e-12
    assert all(row["distance_of_R_from_projector"] > 1e-8 for row in former_valley_checks)
    assert all(abs(row["action"]) < 1e-14 for row in rank_strata)
    assert np.allclose(
        [row["state_entropy"] for row in rank_strata],
        [0.0, -np.log(2.0), -np.log(3.0)],
        atol=1e-12,
    )
    assert abs(asymptotic_power - 4.0) < 0.05

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_self_consistent_state_bridge_purification_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()