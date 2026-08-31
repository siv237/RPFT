#!/usr/bin/env python3
"""Construct the minimal covariant one-step dilation of the cross-arrow channel."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_minimal_covariant_stinespring_carrier_gate_results.json"
TOL = 1.0e-10

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import physical_blocks  # noqa: E402


def block_diagonal(blocks: list[np.ndarray]) -> np.ndarray:
    dimension = sum(block.shape[0] for block in blocks)
    result = np.zeros((dimension, dimension), dtype=complex)
    offset = 0
    for block in blocks:
        size = block.shape[0]
        result[offset : offset + size, offset : offset + size] = block
        offset += size
    return result


def random_special_unitary(
    dimension: int, rng: np.random.Generator
) -> np.ndarray:
    seed = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    unitary, _ = np.linalg.qr(seed)
    determinant = np.linalg.det(unitary)
    return unitary / determinant ** (1.0 / dimension)


def gauge_frame(rng: np.random.Generator) -> np.ndarray:
    color = random_special_unitary(3, rng)
    weak = random_special_unitary(2, rng)
    angle = float(rng.uniform(-np.pi, np.pi))

    def phase(charge: float) -> complex:
        return np.exp(1j * charge * angle)

    source = block_diagonal(
        [
            phase(1.0 / 6.0) * np.kron(color, weak),
            phase(-1.0 / 2.0) * weak,
            phase(-1.0) * np.eye(1),
            phase(-1.0 / 2.0) * weak,
        ]
    )
    target = block_diagonal(
        [
            phase(2.0 / 3.0) * color,
            phase(-1.0 / 3.0) * color,
            phase(-1.0) * np.eye(1),
            phase(-1.0) * np.eye(1),
            phase(-1.0 / 2.0) * weak,
        ]
    )
    return block_diagonal([source, target])


def positive_square_root(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(matrix)
    assert values[0] > -TOL
    values = np.maximum(values, 0.0)
    return vectors @ np.diag(np.sqrt(values)) @ vectors.conj().T


def channel(kraus: list[np.ndarray], observable: np.ndarray) -> np.ndarray:
    return sum(operator.conj().T @ observable @ operator for operator in kraus)


def offdiagonal_norm(matrix: np.ndarray) -> float:
    return float(
        np.linalg.norm(matrix[:11, 11:]) + np.linalg.norm(matrix[11:, :11])
    )


def rounded(values) -> list[float]:
    return [float(f"{value:.12g}") for value in values]


def main() -> None:
    _, variations, labels, _ = physical_blocks()
    heavy_variations = variations[7:]
    cross_indices = [
        index
        for index, label in enumerate(labels)
        if label.startswith(("QLYR", "XLdR"))
    ]
    assert len(cross_indices) == 12

    jumps = []
    for index in cross_indices:
        incidence = heavy_variations[index]
        incidence = incidence / np.linalg.norm(incidence, ord="fro")
        jumps.append(
            np.block(
                [
                    [np.zeros((11, 11), complex), incidence.conj().T],
                    [incidence, np.zeros((10, 10), complex)],
                ]
            )
        )

    real_gram = np.array(
        [[np.real(np.vdot(first, second)) for second in jumps] for first in jumps]
    )
    assert np.linalg.norm(real_gram - 2.0 * np.eye(12)) < TOL
    jump_sum = sum(jump @ jump for jump in jumps)
    jump_sum_values = np.linalg.eigvalsh(jump_sum)
    maximum_step = float(1.0 / jump_sum_values[-1])
    assert abs(maximum_step - 1.0 / 6.0) < TOL

    benchmark_step = 1.0 / 12.0
    no_jump = positive_square_root(
        np.eye(21) - benchmark_step * jump_sum
    )
    kraus = [no_jump] + [np.sqrt(benchmark_step) * jump for jump in jumps]
    unital_residual = float(
        np.linalg.norm(sum(item.conj().T @ item for item in kraus) - np.eye(21))
    )
    trace_residual = float(
        np.linalg.norm(sum(item @ item.conj().T for item in kraus) - np.eye(21))
    )
    kraus_vectors = np.column_stack(
        [item.reshape(-1, order="F") for item in kraus]
    )
    kraus_rank = int(np.linalg.matrix_rank(kraus_vectors, TOL))
    jump_rank = int(
        np.linalg.matrix_rank(
            np.column_stack(
                [item.reshape(-1, order="F") for item in jumps]
            ),
            TOL,
        )
    )
    assert unital_residual < TOL
    assert trace_residual < TOL
    assert jump_rank == 12 and kraus_rank == 13

    rng = np.random.default_rng(20260828)
    source_seed = rng.normal(size=(11, 11)) + 1j * rng.normal(size=(11, 11))
    target_seed = rng.normal(size=(10, 10)) + 1j * rng.normal(size=(10, 10))
    observable = block_diagonal(
        [source_seed + source_seed.conj().T, target_seed + target_seed.conj().T]
    )
    endpoint_preservation_residual = offdiagonal_norm(channel(kraus, observable))
    assert endpoint_preservation_residual < TOL

    normalized_jump_basis = [jump / np.sqrt(2.0) for jump in jumps]
    orthogonality_residuals = []
    reconstruction_residuals = []
    channel_covariance_residuals = []
    invariant_jump_sum_residuals = []
    for _ in range(12):
        frame = gauge_frame(rng)
        transformed = [
            frame @ basis @ frame.conj().T for basis in normalized_jump_basis
        ]
        environment = np.array(
            [
                [np.real(np.vdot(basis, item)) for item in transformed]
                for basis in normalized_jump_basis
            ]
        )
        orthogonality_residuals.append(
            float(np.linalg.norm(environment.T @ environment - np.eye(12)))
        )
        reconstruction_residuals.append(
            max(
                float(
                    np.linalg.norm(
                        transformed[column]
                        - sum(
                            environment[row, column] * normalized_jump_basis[row]
                            for row in range(12)
                        )
                    )
                )
                for column in range(12)
            )
        )
        invariant_jump_sum_residuals.append(
            float(np.linalg.norm(frame @ jump_sum @ frame.conj().T - jump_sum))
        )
        left = channel(kraus, frame @ observable @ frame.conj().T)
        right = frame @ channel(kraus, observable) @ frame.conj().T
        channel_covariance_residuals.append(float(np.linalg.norm(left - right)))

    assert max(orthogonality_residuals) < TOL
    assert max(reconstruction_residuals) < TOL
    assert max(invariant_jump_sum_residuals) < TOL
    assert max(channel_covariance_residuals) < TOL

    # The derivative of the one-step channel at p=0 is the desired
    # Lindblad generator.  The finite-p family itself is not a semigroup.
    def kraus_at(step: float) -> list[np.ndarray]:
        return [positive_square_root(np.eye(21) - step * jump_sum)] + [
            np.sqrt(step) * jump for jump in jumps
        ]

    generator_action = sum(jump @ observable @ jump for jump in jumps) - 0.5 * (
        jump_sum @ observable + observable @ jump_sum
    )
    derivative_step = 1.0e-7
    derivative = (
        channel(kraus_at(derivative_step), observable) - observable
    ) / derivative_step
    generator_derivative_residual = float(np.linalg.norm(derivative - generator_action))
    assert generator_derivative_residual < 1.0e-4

    first_step, second_step = 0.02, 0.03
    composed = channel(
        kraus_at(first_step), channel(kraus_at(second_step), observable)
    )
    added = channel(kraus_at(first_step + second_step), observable)
    one_step_semigroup_residual = float(np.linalg.norm(composed - added))
    assert one_step_semigroup_residual > 1.0e-4

    step_scan = []
    for step in (0.0, 1.0e-6, 0.01, benchmark_step, maximum_step):
        if step == 0.0:
            rank = 1
            residual = 0.0
        else:
            operators = kraus_at(step)
            rank = int(
                np.linalg.matrix_rank(
                    np.column_stack(
                        [item.reshape(-1, order="F") for item in operators]
                    ),
                    TOL,
                )
            )
            residual = float(
                np.linalg.norm(
                    sum(item.conj().T @ item for item in operators) - np.eye(21)
                )
            )
        step_scan.append(
            {
                "step_probability": step,
                "kraus_rank": rank,
                "unital_residual": residual,
            }
        )

    previous = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v8_cross_arrow_covariance_origin_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert previous["verdict"]["internal_parent_selects_cross_covariance_axis"]

    result = {
        "date": "2026-08-28",
        "gate": "version8_minimal_covariant_stinespring_carrier_gate",
        "cross_jump_space": {
            "system_dimension": 21,
            "real_jump_dimension": 12,
            "jump_operator_linear_rank": jump_rank,
            "jump_gram_residual_from_2I": float(
                np.linalg.norm(real_gram - 2.0 * np.eye(12))
            ),
            "sum_Da_squared_spectrum": rounded(jump_sum_values),
        },
        "one_step_channel": {
            "formula": "K0=sqrt(I-p sum Da^2), Ka=sqrt(p) Da",
            "allowed_step_interval": [0.0, maximum_step],
            "benchmark_step": benchmark_step,
            "unital_residual": unital_residual,
            "trace_preserving_residual": trace_residual,
            "endpoint_block_preservation_residual": endpoint_preservation_residual,
            "kraus_rank_at_positive_interior_step": kraus_rank,
            "minimal_environment_dimension": kraus_rank,
            "environment_decomposition": "C vacuum direct_sum complexification of E_cross(real dimension 12)",
            "environment_complex_dimension": kraus_rank,
            "step_scan": step_scan,
        },
        "gauge_covariant_environment": {
            "random_gauge_tests": 12,
            "maximum_environment_orthogonality_residual": max(
                orthogonality_residuals
            ),
            "maximum_jump_reconstruction_residual": max(
                reconstruction_residuals
            ),
            "maximum_jump_sum_invariance_residual": max(
                invariant_jump_sum_residuals
            ),
            "maximum_channel_covariance_residual": max(
                channel_covariance_residuals
            ),
            "environment_representation_is_existing_cross_arrow_representation": True,
            "environment_jump_space_is_complexification_not_new_physical_fields": True,
        },
        "continuous_time_test": {
            "generator_derivative_residual_at_1e_minus_7": generator_derivative_residual,
            "one_step_composition_residual_for_0_02_plus_0_03": one_step_semigroup_residual,
            "canonical_one_step_family_is_exact_semigroup": False,
            "continuous_noise_or_repeated_fresh_ancilla_rule_derived": False,
        },
        "verdict": {
            "finite_covariant_stinespring_carrier_exists": True,
            "minimal_environment_uses_existing_cross_arrow_space": True,
            "new_physical_particle_required_for_one_step_channel": False,
            "step_probability_or_rate_derived": False,
            "autonomous_continuous_time_dilation_derived": False,
            "status": "minimal_one_step_dilation_positive_continuous_noise_time_open",
            "next_gate": "version8_intrinsic_noise_clock_dilation_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()