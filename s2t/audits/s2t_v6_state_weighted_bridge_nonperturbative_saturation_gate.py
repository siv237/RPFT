#!/usr/bin/env python3
"""Audit the rank-one flat valley of the full state-weighted bridge integral."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def action(bridge: np.ndarray, state: np.ndarray) -> float:
    identity = np.eye(3)
    left = identity - bridge.T @ bridge
    right = identity - bridge @ bridge.T
    return float((np.trace(state @ left @ left) + np.trace(state @ right @ right)) / 7.0)


def numerical_hessian(bridge: np.ndarray, state: np.ndarray, step: float = 1e-4) -> np.ndarray:
    basis = []
    for row in range(3):
        for column in range(3):
            matrix = np.zeros((3, 3))
            matrix[row, column] = 1.0
            basis.append(matrix)
    hessian = np.zeros((9, 9))
    for i, first in enumerate(basis):
        for j, second in enumerate(basis):
            hessian[i, j] = (
                action(bridge + step * first + step * second, state)
                - action(bridge + step * first - step * second, state)
                - action(bridge - step * first + step * second, state)
                + action(bridge - step * first - step * second, state)
            ) / (4.0 * step**2)
    return (hessian + hessian.T) / 2.0


def main() -> None:
    projector = np.diag([1.0, 0.0, 0.0])
    rng = np.random.default_rng(20260819)
    flat_valley_residuals = []
    for _ in range(30):
        transverse = rng.normal(size=(2, 2)) * rng.uniform(0.1, 20.0)
        bridge = np.zeros((3, 3))
        bridge[0, 0] = 1.0
        bridge[1:, 1:] = transverse
        flat_valley_residuals.append(abs(action(bridge, projector)))

    scales = np.array([2.0, 3.0, 5.0, 8.0, 13.0, 21.0])
    spectra = []
    growing_mode_geometric_means = []
    for scale in scales:
        bridge = np.diag([1.0, scale, scale])
        eigenvalues = np.linalg.eigvalsh(numerical_hessian(bridge, projector))
        positive = eigenvalues[eigenvalues > 1e-6]
        spectra.append([float(value) for value in eigenvalues])
        growing = positive[-4:]
        growing_mode_geometric_means.append(float(np.exp(np.mean(np.log(growing)))))

    slope = float(
        np.polyfit(np.log(scales[-4:]), np.log(growing_mode_geometric_means[-4:]), 1)[0]
    )
    gaussian_volume_power = -4.0
    transverse_matrix_radial_power = 3.0
    residual_radial_power = gaussian_volume_power + transverse_matrix_radial_power

    result = {
        "gate": "version6_state_weighted_bridge_nonperturbative_saturation_gate",
        "rank_one_flat_valley": {
            "state": "diag(1,0,0)",
            "bridge_family": "diag(1,C), C in M2(R)",
            "valley_dimension": 4,
            "maximum_action_residual": max(flat_valley_residuals),
        },
        "transverse_power_counting": {
            "scales": [float(value) for value in scales],
            "hessian_spectra": spectra,
            "large_positive_mode_geometric_means": growing_mode_geometric_means,
            "fitted_growing_eigenvalue_power": slope,
            "expected_growing_eigenvalue_power": 2.0,
            "gaussian_transverse_volume_power": gaussian_volume_power,
            "M2_radial_measure_power": transverse_matrix_radial_power,
            "residual_radial_integrand_power": residual_radial_power,
            "residual_integral": "integral dt/t",
            "flat_measure_partition_at_rank_one": "logarithmically_divergent",
        },
        "world_crystal_retrospective": {
            "early_project_big_bang_as_crystallization": True,
            "leech_lattice_literal_model_retained": False,
            "light_thread_literal_model_retained": False,
            "operator_order_parameter_RP2_retained": True,
            "defects_as_misaligned_domains_retained": True,
            "literal_spacetime_lattice_derived": False,
        },
        "verdict": {
            "one_loop_instability_survives_as_rank_loss_tendency": True,
            "flat_measure_nonperturbative_saturation": False,
            "finite_RP2_vacuum_proved": False,
            "missing_datum": "derived rank-loss barrier from polar/BV measure",
            "next_gate": "version6_polar_bv_rank_loss_barrier_gate",
        },
    }

    assert max(flat_valley_residuals) < 1e-12
    assert all(sum(abs(value) < 1e-6 for value in spectrum) == 4 for spectrum in spectra)
    assert abs(slope - 2.0) < 0.15
    assert residual_radial_power == -1.0

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_state_weighted_bridge_nonperturbative_saturation_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()