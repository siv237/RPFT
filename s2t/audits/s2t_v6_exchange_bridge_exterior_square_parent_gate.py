#!/usr/bin/env python3
"""Audit whether the exchange-bridge parent derives the exterior-square term."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


PAIRS = [(0, 1), (0, 2), (1, 2)]


def compound_two(matrix: np.ndarray) -> np.ndarray:
    result = np.zeros((3, 3))
    for row, (i, j) in enumerate(PAIRS):
        for column, (a, b) in enumerate(PAIRS):
            result[row, column] = matrix[i, a] * matrix[j, b] - matrix[i, b] * matrix[j, a]
    return result


def exterior_invariant(matrix: np.ndarray) -> float:
    gram = matrix.T @ matrix
    return float(0.5 * (np.trace(gram) ** 2 - np.trace(gram @ gram)))


def polarized_edge(matrix: np.ndarray) -> np.ndarray:
    edge = np.zeros((9, 9))
    for column in range(9):
        variation = np.zeros((3, 3))
        variation.reshape(-1)[column] = 1.0
        polarized = 0.5 * (
            compound_two(matrix + variation)
            - compound_two(matrix)
            - compound_two(variation)
        )
        edge[:, column] = polarized.reshape(-1)
    return edge


def relative_chain(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    first = matrix.reshape(9, 1)
    second = polarized_edge(matrix)
    operator = np.zeros((19, 19))
    operator[0:1, 1:10] = first.T
    operator[1:10, 0:1] = first
    operator[1:10, 10:19] = second.T
    operator[10:19, 1:10] = second
    curvature = operator @ operator
    fixed = curvature.copy()
    fixed[0:1, 10:19] = 0.0
    fixed[10:19, 0:1] = 0.0
    return operator, curvature, fixed


def raw_direct_crossed_norm(matrix: np.ndarray) -> float:
    direct = np.einsum("ia,jb->iajb", matrix, matrix)
    crossed = np.einsum("ib,ja->iajb", matrix, matrix)
    return float(np.sum((direct - crossed) ** 2))


def bridge_radial_minimum(state_spectrum: np.ndarray) -> tuple[float, float]:
    second = float(np.sum(state_spectrum**2))
    third = float(np.sum(state_spectrum**3))
    scale = second / third
    minimum = (2.0 / 7.0) * (1.0 - second**2 / third)
    return scale, minimum


def uniaxial_spectrum(axis_weight: float) -> np.ndarray:
    return np.array([axis_weight, (1.0 - axis_weight) / 2.0, (1.0 - axis_weight) / 2.0])


def effective_free_energy(axis_weight: float, exterior_coefficient: float) -> float:
    spectrum = uniaxial_spectrum(axis_weight)
    _, bridge_minimum = bridge_radial_minimum(spectrum)
    entropy = float(np.sum(spectrum * np.log(spectrum)))
    e2 = 0.5 * (1.0 - float(np.sum(spectrum**2)))
    return bridge_minimum + entropy + exterior_coefficient * e2


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


def ordered_minimum(exterior_coefficient: float) -> tuple[float, float]:
    return golden_minimum(
        lambda axis: effective_free_energy(axis, exterior_coefficient),
        0.55,
        1.0 - 1e-11,
    )


def isotropic_energy(exterior_coefficient: float) -> float:
    return -float(np.log(3.0)) + exterior_coefficient / 3.0


def transition_threshold() -> tuple[float, float]:
    left, right = 3.0, 3.1
    for _ in range(80):
        middle = 0.5 * (left + right)
        _, ordered = ordered_minimum(middle)
        if ordered < isotropic_energy(middle):
            right = middle
        else:
            left = middle
    coefficient = 0.5 * (left + right)
    axis, _ = ordered_minimum(coefficient)
    return coefficient, axis


def main() -> None:
    rng = np.random.default_rng(20260819)
    checks = []
    for _ in range(40):
        bridge = rng.normal(size=(3, 3))
        first = bridge.reshape(9, 1)
        second = polarized_edge(bridge)
        compound = compound_two(bridge)
        operator, curvature, fixed = relative_chain(bridge)
        quotient = curvature - fixed
        invariant = exterior_invariant(bridge)
        gram = bridge.T @ bridge
        two_node = np.block(
            [[np.zeros((3, 3)), bridge.T], [bridge, np.zeros((3, 3))]]
        )
        checks.append(
            {
                "polarization_residual": float(np.linalg.norm(second @ first - compound.reshape(9, 1))),
                "compound_norm_residual": float(np.linalg.norm(compound) ** 2 - invariant),
                "relative_action_residual": float(np.linalg.norm(quotient) ** 2 - 2.0 * invariant),
                "raw_tensor_residual": raw_direct_crossed_norm(bridge) - 4.0 * invariant,
                "two_node_trace_four_residual": float(
                    np.trace(np.linalg.matrix_power(two_node, 4)) - 2.0 * np.trace(gram @ gram)
                ),
                "self_adjoint_residual": float(np.linalg.norm(operator - operator.T)),
            }
        )

    critical_coefficient, critical_axis = transition_threshold()
    canonical_coefficient = 2.0
    raw_coefficient = 4.0
    raw_axis, raw_energy = ordered_minimum(raw_coefficient)
    raw_spectrum = uniaxial_spectrum(raw_axis)
    raw_scale, raw_bridge_energy = bridge_radial_minimum(raw_spectrum)

    result = {
        "gate": "version6_exchange_bridge_exterior_square_parent_gate",
        "ordinary_two_node_superconnection": {
            "trace_phi_four": "2 Tr((B^T B)^2)",
            "contains_trace_squared": False,
            "contains_exterior_invariant": False,
        },
        "minimal_exterior_chain": {
            "nodes": ["R", "R3 tensor R3", "Lambda2(R3) tensor Lambda2(R3)"],
            "dimensions": [1, 9, 9],
            "polarized_two_step_path": "Lambda2(B)",
            "path_norm": "e2(B^T B)",
            "relative_endpoint_action": "2 e2(B^T B)",
            "normalized_exterior_coefficient": canonical_coefficient,
            "equivalent_purity_coefficient": canonical_coefficient / 2.0,
            "new_carrier_required": True,
        },
        "full_self_consistent_phase_test": {
            "free_energy": "min_T S_sc(T,R)+Tr(R log R)+m e2(R)",
            "transition_exterior_coefficient": critical_coefficient,
            "transition_equivalent_purity_coefficient": critical_coefficient / 2.0,
            "coexistence_axis_weight": critical_axis,
            "canonical_chain_passes_transition": canonical_coefficient > critical_coefficient,
            "raw_direct_crossed_passes_transition": raw_coefficient > critical_coefficient,
            "raw_ordered_state_spectrum": raw_spectrum.tolist(),
            "raw_optimal_total_singular_weight": raw_scale,
            "raw_bridge_action_at_minimum": raw_bridge_energy,
            "raw_ordered_free_energy": raw_energy,
            "raw_isotropic_free_energy": isotropic_energy(raw_coefficient),
        },
        "normalization_audit": {
            "normalized_exterior_basis": "||Lambda2 B||^2=e2",
            "self_adjoint_endpoint_pair": "2 e2",
            "raw_direct_minus_crossed_tensor": "4 e2",
            "extra_factor_needed_over_minimal_chain": 2.0,
            "available_from_KO6_doubling_after_half_trace": False,
            "available_from_one_irreducible_copy": False,
        },
        "maximum_residuals": {
            key: max(abs(row[key]) for row in checks)
            for key in checks[0]
        },
        "verdict": {
            "current_two_node_parent_derives_exterior_square": False,
            "canonical_functorial_exterior_extension_exists": True,
            "canonical_extension_is_dynamically_sufficient": False,
            "raw_tensor_channel_is_dynamically_sufficient": True,
            "raw_tensor_channel_is_already_parent_derived": False,
            "next_gate": "version6_tensor_square_relative_carrier_normalization_gate",
        },
    }

    assert all(value < 1e-9 for value in result["maximum_residuals"].values())
    assert 3.02 < critical_coefficient < 3.04
    assert canonical_coefficient < critical_coefficient < raw_coefficient
    assert raw_energy < isotropic_energy(raw_coefficient)
    assert np.all(raw_spectrum > 0.0)

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_exchange_bridge_exterior_square_parent_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()