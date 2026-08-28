#!/usr/bin/env python3
"""Audit the three-node spectral parent of edge coherence."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_edge_coherence_spectral_parent_gate_results.json"


def exterior_maps(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return A_B and C_B=(1/2)d(Lambda^2)_B in orthonormal bases."""
    first = matrix.reshape(6, 1)
    pairs = ((0, 1), (0, 2), (1, 2))
    second = np.zeros((3, 6), dtype=complex)
    for output, (a, b) in enumerate(pairs):
        for row in range(2):
            for column in range(3):
                variation = np.zeros((2, 3), dtype=complex)
                variation[row, column] = 1.0
                second[output, 3 * row + column] = 0.5 * (
                    variation[0, a] * matrix[1, b]
                    + matrix[0, a] * variation[1, b]
                    - variation[0, b] * matrix[1, a]
                    - matrix[0, b] * variation[1, a]
                )
    return first, second


def exterior_square(matrix: np.ndarray) -> np.ndarray:
    return np.array(
        [
            matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0],
            matrix[0, 0] * matrix[1, 2] - matrix[0, 2] * matrix[1, 0],
            matrix[0, 1] * matrix[1, 2] - matrix[0, 2] * matrix[1, 1],
        ],
        dtype=complex,
    ).reshape(3, 1)


def dirac(matrix: np.ndarray) -> np.ndarray:
    first, second = exterior_maps(matrix)
    return np.block(
        [
            [np.zeros((1, 1)), first.conj().T, np.zeros((1, 3))],
            [first, np.zeros((6, 6)), second.conj().T],
            [np.zeros((3, 1)), second, np.zeros((3, 3))],
        ]
    )


def invariants(matrix: np.ndarray) -> tuple[float, float]:
    covariance = matrix @ matrix.conj().T
    return float(np.trace(covariance).real), float(np.linalg.det(covariance).real)


def spectral_action(matrix: np.ndarray, mu: float = 4.5) -> float:
    operator = dirac(matrix)
    trace_two = float(np.trace(operator @ operator).real)
    trace_four = float(np.trace(np.linalg.matrix_power(operator, 4)).real)
    return (4.0 / 9.0) * (trace_four - mu * trace_two + mu**2)


def unpack(coordinates: np.ndarray, real_only: bool = False) -> np.ndarray:
    if real_only:
        return coordinates.reshape(2, 3).astype(complex)
    return (coordinates[0::2] + 1j * coordinates[1::2]).reshape(2, 3)


def finite_difference_hessian(
    coordinates: np.ndarray, *, real_only: bool = False, step: float = 2e-4
) -> np.ndarray:
    dimension = coordinates.size
    hessian = np.zeros((dimension, dimension), dtype=float)
    baseline = spectral_action(unpack(coordinates, real_only))
    for i in range(dimension):
        ei = np.zeros(dimension)
        ei[i] = step
        hessian[i, i] = (
            spectral_action(unpack(coordinates + ei, real_only))
            - 2.0 * baseline
            + spectral_action(unpack(coordinates - ei, real_only))
        ) / step**2
        for j in range(i):
            ej = np.zeros(dimension)
            ej[j] = step
            hessian[i, j] = hessian[j, i] = (
                spectral_action(unpack(coordinates + ei + ej, real_only))
                - spectral_action(unpack(coordinates + ei - ej, real_only))
                - spectral_action(unpack(coordinates - ei + ej, real_only))
                + spectral_action(unpack(coordinates - ei - ej, real_only))
            ) / (4.0 * step**2)
    return hessian


def signature(values: np.ndarray, tolerance: float = 1e-4) -> dict[str, int]:
    return {
        "negative": int(np.sum(values < -tolerance)),
        "zero": int(np.sum(np.abs(values) <= tolerance)),
        "positive": int(np.sum(values > tolerance)),
    }


def main() -> None:
    previous = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v7_edge_coherence_rank_one_condensate_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert previous["parent_status"]["status"] == "conditional_positive_potential_parent_missing"

    rng = np.random.default_rng(20260827)
    residuals = {
        "polarization": [],
        "trace_two": [],
        "trace_four": [],
        "parent_action": [],
        "second_edge_norm": [],
        "second_edge_fourth_trace": [],
    }
    for _ in range(250):
        matrix = rng.normal(size=(2, 3)) + 1j * rng.normal(size=(2, 3))
        first, second = exterior_maps(matrix)
        operator = dirac(matrix)
        total, determinant = invariants(matrix)
        residuals["polarization"].append(
            float(np.linalg.norm(second @ first - exterior_square(matrix)))
        )
        residuals["trace_two"].append(
            abs(float(np.trace(operator @ operator).real) - 3.0 * total)
        )
        residuals["trace_four"].append(
            abs(
                float(np.trace(np.linalg.matrix_power(operator, 4)).real)
                - 2.25 * total**2
                - 3.75 * determinant
            )
        )
        residuals["parent_action"].append(
            abs(spectral_action(matrix) - (total - 3.0) ** 2 - (5.0 / 3.0) * determinant)
        )
        residuals["second_edge_norm"].append(
            abs(float(np.linalg.norm(second) ** 2) - 0.5 * total)
        )
        second_gram = second.conj().T @ second
        residuals["second_edge_fourth_trace"].append(
            abs(
                float(np.trace(second_gram @ second_gram).real)
                - 0.125 * (total**2 - determinant)
            )
        )
    maxima = {name: float(max(values)) for name, values in residuals.items()}
    assert max(maxima.values()) < 2e-10

    grading = np.diag(np.r_[np.ones(1), -np.ones(6), np.ones(3)])
    control = rng.normal(size=(2, 3)) + 1j * rng.normal(size=(2, 3))
    control_operator = dirac(control)
    self_adjoint_residual = float(
        np.linalg.norm(control_operator - control_operator.conj().T)
    )
    grading_residual = float(
        np.linalg.norm(grading @ control_operator + control_operator @ grading)
    )
    assert self_adjoint_residual < 1e-12
    assert grading_residual < 1e-12

    origin = np.zeros(12)
    vacuum = np.zeros(12)
    vacuum[0] = np.sqrt(3.0)
    origin_spectrum = np.linalg.eigvalsh(finite_difference_hessian(origin))
    vacuum_spectrum = np.linalg.eigvalsh(finite_difference_hessian(vacuum))
    origin_signature = signature(origin_spectrum)
    vacuum_signature = signature(vacuum_spectrum)
    assert origin_signature == {"negative": 12, "zero": 0, "positive": 0}
    assert vacuum_signature == {"negative": 0, "zero": 7, "positive": 5}
    assert np.linalg.norm(origin_spectrum + 12.0) < 2e-5
    assert np.linalg.norm(vacuum_spectrum[7:11] - 10.0) < 2e-4
    assert abs(vacuum_spectrum[11] - 24.0) < 2e-4

    real_origin = np.zeros(6)
    real_vacuum = np.zeros(6)
    real_vacuum[0] = np.sqrt(3.0)
    real_origin_spectrum = np.linalg.eigvalsh(
        finite_difference_hessian(real_origin, real_only=True)
    )
    real_vacuum_spectrum = np.linalg.eigvalsh(
        finite_difference_hessian(real_vacuum, real_only=True)
    )
    assert signature(real_origin_spectrum) == {"negative": 6, "zero": 0, "positive": 0}
    assert signature(real_vacuum_spectrum) == {"negative": 0, "zero": 3, "positive": 3}

    result = {
        "gate": "version7_edge_coherence_spectral_parent_gate",
        "carrier": {
            "chain_dimensions": [1, 6, 3],
            "chain": "C -> C^2 tensor (C^3)* -> Lambda^2 C^2 tensor Lambda^2 (C^3)*",
            "grading": ["even", "odd", "even"],
            "dirac_linear_in_B": True,
            "self_adjoint_residual": self_adjoint_residual,
            "odd_grading_residual": grading_residual,
            "real_completion": "conjugate chain; physical half-trace preserves particle trace",
        },
        "identities": {
            "C_B": "(1/2) d(Lambda^2)_B",
            "C_B_A_B": "Lambda^2 B",
            "trace_D2": "3 T",
            "trace_D4": "(9/4) T^2 + (15/4) det(B B*)",
            "second_edge_norm": "T/2",
            "second_edge_fourth_trace": "(T^2-det(B B*))/8",
            "maximum_residuals": maxima,
        },
        "spectral_parent": {
            "mu": 4.5,
            "formula": "(4/9)(Tr D_B^4 - mu Tr D_B^2 + mu^2)",
            "reduced_formula": "(T-3)^2 + (5/3) det(B B*)",
            "relative_determinant_coefficient": 5.0 / 3.0,
            "absolute_scale_role": "mu fixes only the common radial norm T*=2mu/3",
            "zero_set": "rank(B)=1 and T=3",
        },
        "origin": {
            "action": spectral_action(np.zeros((2, 3), dtype=complex)),
            "spectrum": origin_spectrum.tolist(),
            "signature": origin_signature,
        },
        "vacuum": {
            "action": spectral_action(unpack(vacuum)),
            "spectrum": vacuum_spectrum.tolist(),
            "signature": vacuum_signature,
            "analytic_spectrum": {"zero": [0.0, 7], "rank_growth": [10.0, 4], "radial": [24.0, 1]},
        },
        "Real_slice": {
            "origin_spectrum": real_origin_spectrum.tolist(),
            "origin_signature": signature(real_origin_spectrum),
            "vacuum_spectrum": real_vacuum_spectrum.tolist(),
            "vacuum_signature": signature(real_vacuum_spectrum),
        },
        "verdict": {
            "single_full_spectral_polynomial": True,
            "manual_minor_norm_removed": True,
            "relative_radial_wedge_weight_derived": True,
            "rank_one_condensation": True,
            "strict_finite_triple_embedding": False,
            "status": "positive_graded_spectral_parent_strict_algebraic_embedding_open",
            "next_gate": "embed or exclude the 1-6-3 exterior chain as a strict Real finite spectral triple over the admitted physical algebra",
        },
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()