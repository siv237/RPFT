#!/usr/bin/env python3
"""Audit the current parent against an RP2 vacuum-manifold control."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def ldg_potential(q: np.ndarray, a: float, b: float, c: float) -> float:
    q2 = float(np.trace(q @ q))
    q3 = float(np.trace(q @ q @ q))
    return a * q2 / 2.0 - b * q3 / 3.0 + c * q2**2 / 4.0


def hessian(point: np.ndarray, basis: list[np.ndarray], function) -> np.ndarray:
    step = 1.0e-4
    result = np.zeros((len(basis), len(basis)))
    for i, bi in enumerate(basis):
        for j, bj in enumerate(basis):
            result[i, j] = (
                function(point + step * bi + step * bj)
                - function(point + step * bi - step * bj)
                - function(point - step * bi + step * bj)
                + function(point - step * bi - step * bj)
            ) / (4.0 * step**2)
    return result


def main() -> None:
    rng = np.random.default_rng(20260819)
    projector_residuals = []
    mixed_spectra = []
    for _ in range(20):
        n = rng.normal(size=3)
        n /= np.linalg.norm(n)
        p = np.outer(n, n)
        projector_residuals.append(float(np.linalg.norm(p @ p - p)))
        x = 2.0 / 3.0
        r = x * p + (1.0 - x) * (np.eye(3) - p) / 2.0
        mixed_spectra.append(np.linalg.eigvalsh(r))

    a, b, c = -1.0, 1.0, 1.0
    s = float((b + np.sqrt(b**2 - 24.0 * a * c)) / (4.0 * c))
    p0 = np.diag([1.0, 0.0, 0.0])
    q0 = s * (p0 - np.eye(3) / 3.0)
    basis = [
        np.diag([1.0, -1.0, 0.0]) / np.sqrt(2.0),
        np.diag([1.0, 1.0, -2.0]) / np.sqrt(6.0),
    ]
    for row, column in ((0, 1), (0, 2), (1, 2)):
        matrix = np.zeros((3, 3))
        matrix[row, column] = matrix[column, row] = 1.0 / np.sqrt(2.0)
        basis.append(matrix)
    eigenvalues = np.linalg.eigvalsh(
        hessian(q0, basis, lambda q: ldg_potential(q, a, b, c))
    )

    heights = np.array(
        [-1.0] * 3 + [0.0] * 3 + [1.0] * 3
        + [1.0] * 3 + [0.0] * 3 + [-1.0] * 3
    )
    ground_multiplicity = int(np.sum(heights == np.min(heights)))

    uniform = np.ones(4) / 2.0
    affine_p1 = np.outer(uniform, uniform)
    affine_residuals = []
    for _ in range(20):
        permutation = np.eye(4)[rng.permutation(4)]
        affine_residuals.append(
            float(np.linalg.norm(permutation @ affine_p1 @ permutation.T - affine_p1))
        )

    result = {
        "gate": "version6_rp2_geometric_phase_derivation_gate",
        "project_audit": {
            "rank_one_projector_is_input_in_relevant_tome5_gates": True,
            "current_parent_derives_RP2_vacuum_manifold": False,
            "affine_P1_orbit_dimension": 0,
            "affine_P1_maximum_permutation_residual": max(affine_residuals),
            "modular_ground_multiplicity": ground_multiplicity,
        },
        "available_state_kinematics": {
            "carrier": "D_R3",
            "pure_state_manifold": "RP2",
            "maximum_projector_residual": max(projector_residuals),
            "uniaxial_mixed_state_spectrum": [float(v) for v in mixed_spectra[0]],
            "uniaxial_mixed_state_orbit": "SO3/O2=RP2",
            "full_purification_required": False,
        },
        "landau_de_gennes_control": {
            "scalar_order": s,
            "hessian_eigenvalues": [float(v) for v in eigenvalues],
            "tangent_zero_modes": int(np.sum(np.abs(eigenvalues) < 1.0e-6)),
            "positive_transverse_modes": int(np.sum(eigenvalues > 1.0e-6)),
        },
        "verdict": {
            "missing_dynamic_bridge": "derive_spectral_splitting_3_to_1_plus_2",
            "missing_physical_bridge": "identify_family_state_as_geometric_order_parameter",
            "next_gate": "version6_real_qutrit_purification_transition_gate",
        },
    }

    assert max(projector_residuals) < 1.0e-12
    assert np.allclose(mixed_spectra[0], [1.0 / 6.0, 1.0 / 6.0, 2.0 / 3.0])
    assert result["landau_de_gennes_control"]["tangent_zero_modes"] == 2
    assert result["landau_de_gennes_control"]["positive_transverse_modes"] == 3
    assert ground_multiplicity == 6
    assert max(affine_residuals) < 1.0e-12

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_rp2_geometric_phase_derivation_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()