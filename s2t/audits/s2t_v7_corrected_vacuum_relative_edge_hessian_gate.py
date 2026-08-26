#!/usr/bin/env python3
"""Full 72-real-dimensional Hessian of the corrected three-edge vacuum."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


V = np.array(
    [
        [1 / np.sqrt(2), -1 / np.sqrt(2), 0.0, 0.0],
        [1 / np.sqrt(6), 1 / np.sqrt(6), -2 / np.sqrt(6), 0.0],
        [1 / np.sqrt(12), 1 / np.sqrt(12), 1 / np.sqrt(12), -3 / np.sqrt(12)],
    ],
    dtype=complex,
)
P3 = V.conj().T @ V


def edge_operators() -> list[np.ndarray]:
    u = np.zeros((7, 8), dtype=complex)
    d = np.zeros((7, 8), dtype=complex)
    e = np.zeros((7, 8), dtype=complex)
    u[0:3, 0:3] = np.eye(3)
    d[3:6, 3:6] = np.eye(3)
    e[6, 7] = 1.0
    return [u, d, e]


EDGES = edge_operators()
MULTIPLICITIES = np.array([3.0, 3.0, 1.0])
P_LEFT = np.kron(P3, np.eye(8))


def unpack(vector: np.ndarray) -> np.ndarray:
    complex_coordinates = vector[:36] + 1j * vector[36:]
    return complex_coordinates.reshape(3, 3, 4)


def lifted_operator(vector: np.ndarray) -> np.ndarray:
    fields = unpack(vector)
    return sum(np.kron(fields[index], EDGES[index]) for index in range(3))


def action(vector: np.ndarray) -> float:
    z = lifted_operator(vector)
    return float(
        (
            np.linalg.norm(P_LEFT - z.conj().T @ z, "fro") ** 2
            + np.linalg.norm(z @ z.conj().T - np.eye(21), "fro") ** 2
        )
        / 45.0
    )


def reduced_action(vector: np.ndarray) -> float:
    fields = unpack(vector)
    value = 3.0
    for multiplicity, field in zip(MULTIPLICITIES, fields):
        value += multiplicity * (
            np.linalg.norm(field.conj().T @ field - P3, "fro") ** 2
            + np.linalg.norm(field @ field.conj().T - np.eye(3), "fro") ** 2
        )
    return float(value / 45.0)


def finite_difference_hessian(point: np.ndarray, epsilon: float = 2.0e-4) -> np.ndarray:
    dimension = point.size
    hessian = np.zeros((dimension, dimension))
    center = action(point)
    for i in range(dimension):
        direction = np.zeros(dimension)
        direction[i] = epsilon
        hessian[i, i] = (action(point + direction) - 2.0 * center + action(point - direction)) / epsilon**2
    for i in range(dimension):
        for j in range(i + 1, dimension):
            first = np.zeros(dimension)
            second = np.zeros(dimension)
            first[i] = epsilon
            second[j] = epsilon
            value = (
                action(point + first + second)
                - action(point + first - second)
                - action(point - first + second)
                + action(point - first - second)
            ) / (4.0 * epsilon**2)
            hessian[i, j] = value
            hessian[j, i] = value
    return hessian


def cluster(values: np.ndarray, tolerance: float = 2.0e-5) -> list[dict[str, float | int]]:
    groups: list[list[float]] = []
    for value in sorted(values.tolist()):
        if not groups or abs(value - np.mean(groups[-1])) > tolerance:
            groups.append([value])
        else:
            groups[-1].append(value)
    return [
        {"value": float(np.mean(group)), "multiplicity": len(group)} for group in groups
    ]


def random_unitary(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    q, r = np.linalg.qr(raw)
    phases = np.diag(r)
    return q @ np.diag(np.conj(phases) / np.abs(phases))


def main() -> None:
    fields = np.stack([V, V, V])
    flat = fields.reshape(-1)
    point = np.concatenate([flat.real, flat.imag])

    rng = np.random.default_rng(20260826)
    reduction_residuals = []
    for _ in range(32):
        test = rng.normal(size=72)
        reduction_residuals.append(abs(action(test) - reduced_action(test)))

    hessian = finite_difference_hessian(point)
    raw_eigenvalues = np.linalg.eigvalsh(hessian)

    coordinate_weights = np.repeat(MULTIPLICITIES, 12)
    metric_diagonal = np.concatenate([coordinate_weights, coordinate_weights])
    inverse_sqrt_metric = np.diag(1.0 / np.sqrt(metric_diagonal))
    generalized_hessian = inverse_sqrt_metric @ hessian @ inverse_sqrt_metric
    generalized_eigenvalues = np.linalg.eigvalsh(generalized_hessian)

    unitary_actions = []
    for _ in range(24):
        rotated = np.stack([random_unitary(rng) @ V for _ in range(3)])
        rotated_flat = rotated.reshape(-1)
        rotated_point = np.concatenate([rotated_flat.real, rotated_flat.imag])
        unitary_actions.append(action(rotated_point))

    cross_block_norms = []
    edge_coordinate_blocks = [
        list(range(12 * edge, 12 * (edge + 1)))
        + list(range(36 + 12 * edge, 36 + 12 * (edge + 1)))
        for edge in range(3)
    ]
    for first in range(3):
        for second in range(first + 1, 3):
            cross_block_norms.append(
                float(np.linalg.norm(hessian[np.ix_(edge_coordinate_blocks[first], edge_coordinate_blocks[second])]))
            )

    negative = int(np.sum(generalized_eigenvalues < -1.0e-5))
    zero = int(np.sum(np.abs(generalized_eigenvalues) <= 1.0e-5))
    positive = int(np.sum(generalized_eigenvalues > 1.0e-5))

    result = {
        "gate": "version7_corrected_vacuum_relative_edge_hessian_gate",
        "corrected_field": {
            "complex_dimension": 36,
            "real_dimension": 72,
            "edge_multiplicities": {"u": 3, "d": 3, "e": 1},
        },
        "block_reduction": {
            "maximum_full_reduced_action_residual": max(reduction_residuals),
            "maximum_mixed_edge_hessian_block_norm": max(cross_block_norms),
        },
        "vacuum": {
            "action": action(point),
            "manifold": "U(3)_u x U(3)_d x U(3)_e",
            "real_dimension": 27,
            "maximum_random_unitary_action_residual": max(abs(value - 1.0 / 15.0) for value in unitary_actions),
        },
        "raw_coordinate_hessian": {
            "clusters": cluster(raw_eigenvalues),
            "minimum_eigenvalue": float(np.min(raw_eigenvalues)),
            "maximum_eigenvalue": float(np.max(raw_eigenvalues)),
        },
        "trace_metric_generalized_hessian": {
            "clusters": cluster(generalized_eigenvalues),
            "negative_count": negative,
            "zero_count": zero,
            "positive_count": positive,
            "minimum_eigenvalue": float(np.min(generalized_eigenvalues)),
            "maximum_eigenvalue": float(np.max(generalized_eigenvalues)),
        },
        "relative_moduli": {
            "after_common_U3_quotient": 18,
            "after_common_O3_quotient_in_real_limit": 6,
            "mixing_selected": False,
        },
        "contract_update": {
            "transverse_endpoint_stability": "pass",
            "isolated_endpoint": "fail_continuous_moduli",
            "relative_edge_alignment": "not_selected",
            "CKM_PMNS_prediction": "not_obtained",
            "next_gate": "degree_two_cross_edge_curvature and junk quotient",
        },
    }

    assert max(reduction_residuals) < 1.0e-10
    assert negative == 0
    assert zero == 27
    assert positive == 45
    assert max(cross_block_norms) < 1.0e-6
    assert result["vacuum"]["maximum_random_unitary_action_residual"] < 1.0e-12

    output = Path(__file__).resolve().parents[1] / "results" / "s2t_v7_corrected_vacuum_relative_edge_hessian_gate_results.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()