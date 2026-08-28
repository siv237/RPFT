#!/usr/bin/env python3
"""Audit the rank-one edge-coherence condensate potential."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_edge_coherence_rank_one_condensate_gate_results.json"


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def wedge_norm_squared(matrix: np.ndarray) -> float:
    total = 0.0
    for i in range(2):
        for a in range(3):
            for j in range(2):
                for b in range(3):
                    total += abs(matrix[i, a] * matrix[j, b] - matrix[i, b] * matrix[j, a]) ** 2
    return float(total)


def action(matrix: np.ndarray) -> float:
    covariance = matrix @ matrix.conj().T
    radial = float(np.trace(covariance).real - 3.0)
    return radial**2 + wedge_norm_squared(matrix)


def unpack(coordinates: np.ndarray, real_only: bool = False) -> np.ndarray:
    if real_only:
        return coordinates.reshape(2, 3).astype(complex)
    complex_coordinates = coordinates[0::2] + 1j * coordinates[1::2]
    return complex_coordinates.reshape(2, 3)


def finite_difference_hessian(
    coordinates: np.ndarray, *, real_only: bool = False, step: float = 2e-4
) -> np.ndarray:
    dimension = coordinates.size
    hessian = np.zeros((dimension, dimension), dtype=float)
    baseline = action(unpack(coordinates, real_only=real_only))
    for i in range(dimension):
        shift_i = np.zeros(dimension)
        shift_i[i] = step
        hessian[i, i] = (
            action(unpack(coordinates + shift_i, real_only=real_only))
            - 2.0 * baseline
            + action(unpack(coordinates - shift_i, real_only=real_only))
        ) / step**2
        for j in range(i):
            shift_j = np.zeros(dimension)
            shift_j[j] = step
            hessian[i, j] = hessian[j, i] = (
                action(unpack(coordinates + shift_i + shift_j, real_only=real_only))
                - action(unpack(coordinates + shift_i - shift_j, real_only=real_only))
                - action(unpack(coordinates - shift_i + shift_j, real_only=real_only))
                + action(unpack(coordinates - shift_i - shift_j, real_only=real_only))
            ) / (4.0 * step**2)
    return hessian


def classify_spectrum(values: np.ndarray, tolerance: float = 1e-4) -> dict:
    return {
        "negative": int(np.sum(values < -tolerance)),
        "zero": int(np.sum(np.abs(values) <= tolerance)),
        "positive": int(np.sum(values > tolerance)),
    }


def main() -> None:
    previous = load_result("s2t_v7_universal_incidence_parent_admissibility_gate_results.json")
    assert previous["verdict"]["status"] == "closed_as_internal_universal_incidence_parent"

    rng = np.random.default_rng(20260827)
    wedge_residuals = []
    for _ in range(200):
        matrix = rng.normal(size=(2, 3)) + 1j * rng.normal(size=(2, 3))
        covariance = matrix @ matrix.conj().T
        wedge_residuals.append(
            abs(wedge_norm_squared(matrix) - 4.0 * np.linalg.det(covariance).real)
        )
    maximum_wedge_residual = float(max(wedge_residuals))
    assert maximum_wedge_residual < 1e-10

    origin_coordinates = np.zeros(12)
    vacuum_coordinates = np.zeros(12)
    vacuum_coordinates[0] = np.sqrt(3.0)
    origin_hessian = finite_difference_hessian(origin_coordinates)
    vacuum_hessian = finite_difference_hessian(vacuum_coordinates)
    origin_spectrum = np.linalg.eigvalsh(origin_hessian)
    vacuum_spectrum = np.linalg.eigvalsh(vacuum_hessian)
    origin_signature = classify_spectrum(origin_spectrum)
    vacuum_signature = classify_spectrum(vacuum_spectrum)
    assert origin_signature == {"negative": 12, "zero": 0, "positive": 0}
    assert vacuum_signature == {"negative": 0, "zero": 7, "positive": 5}
    assert np.linalg.norm(origin_spectrum + 12.0) < 1e-5
    assert np.linalg.norm(vacuum_spectrum[-5:] - 24.0) < 1e-4

    vacuum = unpack(vacuum_coordinates)
    covariance = vacuum @ vacuum.conj().T
    copy_state = covariance / np.trace(covariance)
    height = 2.0 * copy_state - np.eye(2)
    assert np.linalg.matrix_rank(vacuum) == 1
    assert abs(np.trace(covariance).real - 3.0) < 1e-12
    assert np.linalg.norm(copy_state @ copy_state - copy_state) < 1e-12
    assert np.linalg.norm(height @ height - np.eye(2)) < 1e-12
    assert action(vacuum) < 1e-24

    # Sample the full singular-value zero set and verify induced purity.
    minimum_samples = []
    for _ in range(50):
        left = rng.normal(size=2) + 1j * rng.normal(size=2)
        right = rng.normal(size=3) + 1j * rng.normal(size=3)
        left /= np.linalg.norm(left)
        right /= np.linalg.norm(right)
        matrix = np.sqrt(3.0) * np.outer(left, right.conj())
        left_state = matrix @ matrix.conj().T / 3.0
        right_state = matrix.conj().T @ matrix / 3.0
        minimum_samples.append(
            {
                "action": action(matrix),
                "rank": int(np.linalg.matrix_rank(matrix, tol=1e-10)),
                "left_purity": float(np.trace(left_state @ left_state).real),
                "right_purity": float(np.trace(right_state @ right_state).real),
            }
        )
    assert max(row["action"] for row in minimum_samples) < 1e-20
    assert all(row["rank"] == 1 for row in minimum_samples)
    assert max(abs(row["left_purity"] - 1.0) for row in minimum_samples) < 1e-12
    assert max(abs(row["right_purity"] - 1.0) for row in minimum_samples) < 1e-12

    # Real slice: six real coordinates and a three-dimensional minimum orbit.
    real_origin = np.zeros(6)
    real_vacuum = np.zeros(6)
    real_vacuum[0] = np.sqrt(3.0)
    real_origin_spectrum = np.linalg.eigvalsh(
        finite_difference_hessian(real_origin, real_only=True)
    )
    real_vacuum_spectrum = np.linalg.eigvalsh(
        finite_difference_hessian(real_vacuum, real_only=True)
    )
    real_origin_signature = classify_spectrum(real_origin_spectrum)
    real_vacuum_signature = classify_spectrum(real_vacuum_spectrum)
    assert real_origin_signature == {"negative": 6, "zero": 0, "positive": 0}
    assert real_vacuum_signature == {"negative": 0, "zero": 3, "positive": 3}

    result = {
        "gate": "version7_edge_coherence_rank_one_condensate_gate",
        "field": {
            "space": "M_2x3(C)",
            "complex_dimension": 6,
            "real_dimension": 12,
            "copy_dimension": 2,
            "common_channel_dimension": 3,
        },
        "action": {
            "formula": "(Tr(B B*) - 3)^2 + ||W(B)||_F^2",
            "wedge_formula": "W_ia,jb = B_ia B_jb - B_ib B_ja",
            "wedge_identity": "||W||^2 = 4 det(B B*)",
            "maximum_random_wedge_identity_residual": maximum_wedge_residual,
            "nonnegative": True,
            "zero_set": "rank(B)=1 and Tr(B B*)=3",
        },
        "origin": {
            "action": action(np.zeros((2, 3), dtype=complex)),
            "stationary": True,
            "analytic_hessian_eigenvalue": -12.0,
            "numeric_spectrum": origin_spectrum.tolist(),
            "signature": origin_signature,
        },
        "vacuum": {
            "representative": vacuum.real.tolist(),
            "action": action(vacuum),
            "rank": int(np.linalg.matrix_rank(vacuum)),
            "frobenius_norm_squared": float(np.trace(covariance).real),
            "complex_vacuum_manifold_real_dimension": 7,
            "analytic_positive_hessian_eigenvalue": 24.0,
            "numeric_spectrum": vacuum_spectrum.tolist(),
            "signature": vacuum_signature,
            "copy_state_purity": float(np.trace(copy_state @ copy_state).real),
            "height_involution_residual": float(np.linalg.norm(height @ height - np.eye(2))),
            "random_minimum_samples": minimum_samples,
        },
        "Real_slice": {
            "field_real_dimension": 6,
            "vacuum_manifold_real_dimension": 3,
            "origin_spectrum": real_origin_spectrum.tolist(),
            "origin_signature": real_origin_signature,
            "vacuum_spectrum": real_vacuum_spectrum.tolist(),
            "vacuum_signature": real_vacuum_signature,
        },
        "parent_status": {
            "radial_and_wedge_terms_combined_in_one_existing_curvature": False,
            "relative_metric_between_scalar_and_wedge_channels_derived": False,
            "copy_axis_inserted_by_hand": False,
            "potential_level_rank_one_condensation": True,
            "status": "conditional_positive_potential_parent_missing",
            "next_gate": "construct or exclude a single Real graded exterior-square parent whose one curvature norm produces both the radial and wedge terms with fixed normalization",
        },
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()