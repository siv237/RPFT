#!/usr/bin/env python3
"""Test internal Gaussian, harmonic and heat-kernel origins of cross covariance."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_cross_arrow_covariance_origin_gate_results.json"
TOL = 1.0e-10

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (  # noqa: E402
    edge_hessians,
    physical_blocks,
)
from s2t_v7_incidence_transfer_markov_weight_gate import polar_coisometry  # noqa: E402
from s2t_v7_polar_transfer_cross_curvature_origin_gate import (  # noqa: E402
    relative_transfer_vacuum_hessian,
)


def spectral_function(matrix: np.ndarray, function) -> np.ndarray:
    values, vectors = np.linalg.eigh(matrix)
    return vectors @ np.diag(function(values)) @ vectors.T


def rounded_matrix(matrix: np.ndarray) -> list[list[float]]:
    return [[float(f"{value:.12g}") for value in row] for row in matrix]


def normalized(matrix: np.ndarray) -> np.ndarray:
    return matrix / np.trace(matrix)


def axis_angle(matrix: np.ndarray) -> float:
    """Principal-axis angle for a symmetric 2x2 covariance."""
    return float(
        0.5
        * np.arctan2(
            2.0 * matrix[0, 1], matrix[0, 0] - matrix[1, 1]
        )
    )


def main() -> None:
    reference, variations, heavy_labels, down_cut = physical_blocks()
    transfer, _, _ = polar_coisometry(reference)
    _, edge_vacuum = edge_hessians(down_cut, len(variations))
    linking_vacuum = relative_transfer_vacuum_hessian(
        reference, variations, transfer
    )

    pairs = []
    for color in range(3):
        for component in ("re", "im"):
            q_index = 7 + heavy_labels.index(f"QLYR_c{color}_{component}")
            x_index = 7 + heavy_labels.index(f"XLdR_c{color}_{component}")
            pairs.append((q_index, x_index))
    cross_indices = np.array([index for pair in pairs for index in pair])
    other_indices = np.setdiff1d(np.arange(27), cross_indices)

    permutation_block = linking_vacuum[np.ix_(cross_indices, cross_indices)]
    linking_pair = permutation_block[:2, :2]
    repeated_pair = np.kron(np.eye(6), linking_pair)
    repetition_residual = float(np.linalg.norm(permutation_block - repeated_pair))
    cross_other_residual = float(
        np.linalg.norm(linking_vacuum[np.ix_(cross_indices, other_indices)])
    )
    linking_pair_values = np.linalg.eigvalsh(linking_pair)
    linking_stiff_axis = axis_angle(linking_pair)
    covariance_soft_axis = linking_stiff_axis + np.pi / 2.0

    assert repetition_residual < TOL
    assert cross_other_residual < TOL
    assert linking_pair_values[0] > 0.0

    eta_scan = []
    positive_axis_angles = []
    for eta in (0.0, 1.0e-6, 0.25, 1.0, 4.0, 1.0e3, 1.0e6):
        hessian = edge_vacuum + 2.0 * eta * linking_vacuum
        pair_hessian = hessian[np.ix_(pairs[0], pairs[0])]
        classical_pair = np.linalg.inv(pair_hessian)
        quantum_pair = 0.5 * spectral_function(pair_hessian, lambda x: x ** -0.5)
        classical_shape = normalized(classical_pair)
        quantum_shape = normalized(quantum_pair)
        if eta > 0.0:
            positive_axis_angles.extend(
                [axis_angle(classical_shape), axis_angle(quantum_shape)]
            )
        eta_scan.append(
            {
                "relative_metric_weight_eta": eta,
                "pair_hessian": rounded_matrix(pair_hessian),
                "classical_normalized_pair_covariance": rounded_matrix(
                    classical_shape
                ),
                "quantum_normalized_pair_covariance": rounded_matrix(
                    quantum_shape
                ),
                "classical_pair_anisotropy_ratio": float(
                    np.linalg.eigvalsh(classical_shape)[-1]
                    / np.linalg.eigvalsh(classical_shape)[0]
                ),
                "quantum_pair_anisotropy_ratio": float(
                    np.linalg.eigvalsh(quantum_shape)[-1]
                    / np.linalg.eigvalsh(quantum_shape)[0]
                ),
            }
        )

    assert max(
        abs(angle - covariance_soft_axis) for angle in positive_axis_angles
    ) < 1.0e-8
    assert eta_scan[0]["classical_pair_anisotropy_ratio"] == 1.0
    assert eta_scan[-1]["classical_pair_anisotropy_ratio"] > 4.0

    benchmark_eta = 1.0
    benchmark_hessian = edge_vacuum + 2.0 * benchmark_eta * linking_vacuum
    benchmark_cross = benchmark_hessian[np.ix_(cross_indices, cross_indices)]
    bridge_coefficient = 7.0 / 36.0

    classical_scale_scan = []
    for action_scale in (0.1, 1.0, 10.0):
        covariance = np.linalg.inv(action_scale * benchmark_cross)
        classical_scale_scan.append(
            {
                "overall_action_scale": action_scale,
                "cross_covariance_trace": float(np.trace(covariance)),
                "central_decay_rate": float(
                    bridge_coefficient * np.trace(covariance)
                ),
            }
        )
    assert abs(
        classical_scale_scan[0]["central_decay_rate"]
        / classical_scale_scan[1]["central_decay_rate"]
        - 10.0
    ) < TOL

    quantum_scale_scan = []
    base_quantum = 0.5 * spectral_function(benchmark_cross, lambda x: x ** -0.5)
    for hbar_over_sqrt_z in (0.1, 1.0, 10.0):
        covariance = hbar_over_sqrt_z * base_quantum
        quantum_scale_scan.append(
            {
                "hbar_over_sqrt_kinetic_scale": hbar_over_sqrt_z,
                "cross_covariance_trace": float(np.trace(covariance)),
                "central_decay_rate": float(
                    bridge_coefficient * np.trace(covariance)
                ),
            }
        )

    heat_time_scan = []
    for correlation_time in (0.01, 0.1, 1.0, 10.0):
        covariance = spectral_function(
            benchmark_cross, lambda x: np.exp(-correlation_time * x)
        )
        heat_time_scan.append(
            {
                "correlation_time": correlation_time,
                "cross_covariance_trace": float(np.trace(covariance)),
                "central_decay_rate": float(
                    bridge_coefficient * np.trace(covariance)
                ),
            }
        )
    assert heat_time_scan[0]["central_decay_rate"] > heat_time_scan[-1][
        "central_decay_rate"
    ]

    previous = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v8_kraus_bridge_parent_action_hessian_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    tome7 = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v7_qualitative_parent_mass_metric_freeze_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert previous["verdict"]["environment_or_quantum_covariance_required"]
    assert not tome7["frozen_boundaries"]["unique_mass_metric_derived"]

    result = {
        "date": "2026-08-28",
        "gate": "version8_cross_arrow_covariance_origin_gate",
        "polar_linking_cross_structure": {
            "ordered_pair": ["QLYR", "XLdR"],
            "number_of_identical_real_pairs": 6,
            "linking_pair_matrix": rounded_matrix(linking_pair),
            "linking_pair_eigenvalues": [
                float(value) for value in linking_pair_values
            ],
            "stiff_principal_axis_angle_radians": linking_stiff_axis,
            "covariance_soft_axis_angle_radians": covariance_soft_axis,
            "covariance_soft_axis_angle_degrees": float(
                np.degrees(covariance_soft_axis)
            ),
            "six_pair_repetition_residual": repetition_residual,
            "coupling_to_other_15_real_directions_norm": cross_other_residual,
            "common_axis_for_all_positive_eta": True,
        },
        "relative_metric_scan": eta_scan,
        "candidate_covariance_rules_at_eta_one": {
            "classical_gaussian": {
                "formula": "C=(a H_eta)^-1",
                "scale_scan": classical_scale_scan,
                "overall_action_scale_derived": False,
            },
            "harmonic_ground_state": {
                "formula": "C=(hbar/(2 sqrt(Z))) H_eta^-1/2 for scalar kinetic Z",
                "scale_scan": quantum_scale_scan,
                "kinetic_scale_and_hbar_ratio_derived": False,
            },
            "heat_kernel": {
                "formula": "C_tau=exp(-tau H_eta)",
                "time_scan": heat_time_scan,
                "correlation_time_derived": False,
            },
        },
        "invariant_information": {
            "cross_subspace_selected": True,
            "six_repeated_Q_X_pairs_selected": True,
            "relative_Q_X_principal_axis_selected_when_eta_positive": True,
            "axis_angle_depends_on_eta": False,
            "anisotropy_strength_depends_on_eta": True,
            "overall_covariance_scale_depends_on_measure": True,
        },
        "verdict": {
            "internal_parent_selects_cross_covariance_axis": True,
            "unique_normalized_covariance_shape_derived": False,
            "unique_nonzero_covariance_scale_derived": False,
            "unique_kraus_rate_derived": False,
            "reason": "the polar linking block fixes a repeated QLYR-XLdR axis, but eta fixes anisotropy while action, kinetic or heat normalization fixes magnitude",
            "status": "covariance_axis_positive_shape_and_rate_no_go",
            "next_gate": "version8_minimal_covariant_stinespring_carrier_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()