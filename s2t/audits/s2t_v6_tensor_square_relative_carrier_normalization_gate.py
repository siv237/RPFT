#!/usr/bin/env python3
"""Audit tensor-square normalization and the thermal reopening of the bridge phase."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def pair_list(dimension: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(dimension) for j in range(i + 1, dimension)]


def compound_two(matrix: np.ndarray) -> np.ndarray:
    pairs = pair_list(matrix.shape[0])
    result = np.zeros((len(pairs), len(pairs)))
    for row, (i, j) in enumerate(pairs):
        for column, (a, b) in enumerate(pairs):
            result[row, column] = matrix[i, a] * matrix[j, b] - matrix[i, b] * matrix[j, a]
    return result


def e2_of_gram(matrix: np.ndarray) -> float:
    gram = matrix.T @ matrix
    return float(0.5 * (np.trace(gram) ** 2 - np.trace(gram @ gram)))


def swap_operator(dimension: int) -> np.ndarray:
    swap = np.zeros((dimension**2, dimension**2))
    for i in range(dimension):
        for j in range(dimension):
            swap[j * dimension + i, i * dimension + j] = 1.0
    return swap


def so3_generators() -> list[np.ndarray]:
    generators = []
    epsilon = np.zeros((3, 3, 3))
    epsilon[0, 1, 2] = epsilon[1, 2, 0] = epsilon[2, 0, 1] = 1.0
    epsilon[0, 2, 1] = epsilon[2, 1, 0] = epsilon[1, 0, 2] = -1.0
    for a in range(3):
        generators.append(-epsilon[a])
    return generators


def state_pieces(axis_weight: float) -> tuple[float, float, float, float]:
    state = np.array([axis_weight, (1.0 - axis_weight) / 2.0, (1.0 - axis_weight) / 2.0])
    second = float(np.sum(state**2))
    third = float(np.sum(state**3))
    bridge = (2.0 / 7.0) * (1.0 - second**2 / third)
    entropy = float(np.sum(state * np.log(state)))
    exterior = 0.5 * (1.0 - second)
    scale = second / third
    return bridge, entropy, exterior, scale


def thermal_free_energy(axis_weight: float, beta: float, exterior_coefficient: float = 2.0) -> float:
    bridge, entropy, exterior, _ = state_pieces(axis_weight)
    return entropy + beta * (bridge + exterior_coefficient * exterior)


def golden_minimum(function, left: float, right: float) -> tuple[float, float]:
    ratio = (np.sqrt(5.0) - 1.0) / 2.0
    x1 = right - ratio * (right - left)
    x2 = left + ratio * (right - left)
    f1, f2 = function(x1), function(x2)
    for _ in range(160):
        if f1 > f2:
            left = x1
            x1, f1 = x2, f2
            x2 = left + ratio * (right - left)
            f2 = function(x2)
        else:
            right = x2
            x2, f2 = x1, f1
            x1 = right - ratio * (right - left)
            f1 = function(x1)
    point = 0.5 * (left + right)
    return point, function(point)


def ordered_minimum(beta: float) -> tuple[float, float]:
    return golden_minimum(lambda axis: thermal_free_energy(axis, beta), 0.55, 1.0 - 1e-11)


def isotropic_energy(beta: float) -> float:
    return -float(np.log(3.0)) + beta * (2.0 / 3.0)


def critical_beta() -> tuple[float, float]:
    left, right = 1.5, 1.6
    for _ in range(80):
        middle = 0.5 * (left + right)
        _, ordered = ordered_minimum(middle)
        if ordered < isotropic_energy(middle):
            right = middle
        else:
            left = middle
    beta = 0.5 * (left + right)
    axis, _ = ordered_minimum(beta)
    return beta, axis


def main() -> None:
    rng = np.random.default_rng(20260819)
    checks = []
    for _ in range(40):
        bridge = rng.normal(size=(3, 3))
        total = float(np.trace(bridge.T @ bridge))
        e2 = e2_of_gram(bridge)
        real_bridge = np.block(
            [[np.zeros((3, 3)), bridge.T], [bridge, np.zeros((3, 3))]]
        )
        exterior_real = compound_two(real_bridge)
        pairs = pair_list(6)
        plus = [index for index, (i, j) in enumerate(pairs) if i < 3 and j < 3]
        minus = [index for index, (i, j) in enumerate(pairs) if i >= 3 and j >= 3]
        mixed = [index for index, (i, j) in enumerate(pairs) if i < 3 <= j]
        same_orientation_norm = float(
            np.linalg.norm(exterior_real[np.ix_(minus, plus)]) ** 2
            + np.linalg.norm(exterior_real[np.ix_(plus, minus)]) ** 2
        )
        mixed_norm = float(np.linalg.norm(exterior_real[np.ix_(mixed, mixed)]) ** 2)

        swap = swap_operator(3)
        identity = np.eye(9)
        projector = 0.5 * (identity - swap)
        tensor_bridge = np.kron(bridge, bridge)
        normalized = float(np.linalg.norm(tensor_bridge @ projector) ** 2)
        raw = float(np.linalg.norm(tensor_bridge @ (identity - swap)) ** 2)
        checks.append(
            {
                "same_orientation_residual": same_orientation_norm - 2.0 * e2,
                "mixed_residual": mixed_norm - total**2,
                "full_exterior_residual": float(np.linalg.norm(exterior_real) ** 2 - (2.0 * e2 + total**2)),
                "normalized_projector_residual": normalized - e2,
                "raw_antisymmetrizer_residual": raw - 4.0 * e2,
            }
        )

    generators = so3_generators()
    vector_casimir = -sum(generator @ generator for generator in generators)
    combined_casimir = np.kron(vector_casimir, np.eye(3)) + np.kron(np.eye(3), vector_casimir)

    beta_transition, coexistence_axis = critical_beta()
    ordered_spectrum = np.array(
        [coexistence_axis, (1.0 - coexistence_axis) / 2.0, (1.0 - coexistence_axis) / 2.0]
    )
    _, _, _, coexistence_scale = state_pieces(coexistence_axis)
    beta_two_axis, beta_two_energy = ordered_minimum(2.0)

    result = {
        "gate": "version6_tensor_square_relative_carrier_normalization_gate",
        "real_pair_exterior_decomposition": {
            "formula": "Lambda2(V+ plus V-)=Lambda2 V+ plus (V+ tensor V-) plus Lambda2 V-",
            "same_orientation_family_term": "2 e2(B^T B)",
            "mixed_orientation_term": "Tr(B^T B)^2",
            "mixed_term_after_state_normalization": 1.0,
            "extra_rank_sensitive_factor": False,
        },
        "exchange_normalization": {
            "orthogonal_antisymmetric_projector": "P_-=(I-swap)/2",
            "projected_norm": "e2(B^T B)",
            "raw_antisymmetrizer": "I-swap=2P_-",
            "raw_norm": "4 e2(B^T B)",
            "raw_factor_is_projection_overcount": True,
        },
        "casimir_clue": {
            "vector_so3_casimir_residual": float(np.linalg.norm(vector_casimir - 2.0 * np.eye(3))),
            "left_right_combined_casimir_residual": float(np.linalg.norm(combined_casimir - 4.0 * np.eye(9))),
            "combined_eigenvalue": 4.0,
            "current_parent_contains_so3_left_right_laplacian": False,
        },
        "thermal_reopening": {
            "free_energy": "Tr(R log R)+beta[S_rad(R)+2e2(R)]",
            "critical_inverse_temperature": beta_transition,
            "coexistence_ordered_spectrum": ordered_spectrum.tolist(),
            "coexistence_optimal_total_singular_weight": coexistence_scale,
            "beta_1_phase": "isotropic",
            "beta_2_ordered_axis_weight": beta_two_axis,
            "beta_2_ordered_free_energy": beta_two_energy,
            "beta_2_isotropic_free_energy": isotropic_energy(2.0),
            "canonical_exterior_term_sufficient_after_cooling": True,
        },
        "project_beta_status": {
            "rho_beta_exists": True,
            "beta_is_fixed_by_project": False,
            "modular_flow_changes_its_own_beta": False,
            "modular_height_acts_on_family_axis": False,
            "cooling_trajectory_derived": False,
        },
        "maximum_residuals": {
            key: max(abs(row[key]) for row in checks)
            for key in checks[0]
        },
        "verdict": {
            "tensor_square_supplies_missing_factor_two": False,
            "raw_coefficient_four_is_canonical_exchange_norm": False,
            "so3_casimir_four_is_algebraically_exact": True,
            "so3_casimir_four_is_parent_derived": False,
            "thermal_phase_transition_with_canonical_term": True,
            "thermal_transition_is_dynamically_derived": False,
            "next_gate": "version6_modular_cooling_projective_transition_gate",
        },
    }

    assert all(value < 1e-9 for value in result["maximum_residuals"].values())
    assert result["casimir_clue"]["vector_so3_casimir_residual"] < 1e-12
    assert result["casimir_clue"]["left_right_combined_casimir_residual"] < 1e-12
    assert 1.54 < beta_transition < 1.55
    assert beta_two_energy < isotropic_energy(2.0)

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_tensor_square_relative_carrier_normalization_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()