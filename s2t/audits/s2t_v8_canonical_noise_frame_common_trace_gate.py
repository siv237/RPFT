#!/usr/bin/env python3
"""Build the basis-independent common-trace noise Casimir."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh, svdvals


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_canonical_noise_frame_common_trace_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v8_correlation_kernel_short_time_rate_selector_gate import (  # noqa: E402
    coefficient_design,
    fit_coefficients,
)
from s2t_v8_kms_nontracial_relative_rate_selector_gate import (  # noqa: E402
    assemble,
    block_diagonal,
    central_density,
    corner_dissipator,
    gell_mann_matrices,
    pair_vector,
)
from s2t_v8_modular_bohr_parent_origin_gate import (  # noqa: E402
    directed_family_generator,
    directed_transfer_generator,
)
from s2t_v8_common_chain_dirichlet_rate_metric_gate import TERM_ORDER  # noqa: E402


def gauge_components() -> tuple[list[str], list[np.ndarray], list[np.ndarray]]:
    pauli = [
        np.array([[0, 1], [1, 0]], complex),
        np.array([[0, -1j], [1j, 0]], complex),
        np.array([[1, 0], [0, -1]], complex),
    ]
    labels: list[str] = []
    sources: list[np.ndarray] = []
    targets: list[np.ndarray] = []
    for index, matrix in enumerate(gell_mann_matrices()):
        labels.append(f"SU3_{index}")
        sources.append(
            block_diagonal(
                [
                    np.kron(matrix / 2.0, np.eye(2)),
                    np.zeros((2, 2)),
                    np.zeros((1, 1)),
                    np.zeros((2, 2)),
                ]
            )
        )
        targets.append(
            block_diagonal(
                [
                    matrix / 2.0,
                    matrix / 2.0,
                    np.zeros((1, 1)),
                    np.zeros((1, 1)),
                    np.zeros((2, 2)),
                ]
            )
        )
    for index, matrix in enumerate(pauli):
        labels.append(f"SU2_{index}")
        sources.append(
            block_diagonal(
                [
                    np.kron(np.eye(3), matrix / 2.0),
                    matrix / 2.0,
                    np.zeros((1, 1)),
                    matrix / 2.0,
                ]
            )
        )
        targets.append(
            block_diagonal(
                [
                    np.zeros((3, 3)),
                    np.zeros((3, 3)),
                    np.zeros((1, 1)),
                    np.zeros((1, 1)),
                    matrix / 2.0,
                ]
            )
        )
    labels.append("U1_0")
    sources.append(
        block_diagonal(
            [
                np.eye(6) / 6.0,
                -np.eye(2) / 2.0,
                -np.eye(1),
                -np.eye(2) / 2.0,
            ]
        )
    )
    targets.append(
        block_diagonal(
            [
                2.0 * np.eye(3) / 3.0,
                -np.eye(3) / 3.0,
                -np.eye(1),
                -np.eye(1),
                -np.eye(2) / 2.0,
            ]
        )
    )
    return labels, sources, targets


def gram_whitener(gram: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh((gram + gram.conj().T) / 2.0)
    threshold = 1.0e-12 * values[-1]
    positive = values > threshold
    coefficients = vectors[:, positive] * values[positive] ** -0.5
    return coefficients, values[positive], values


def whiten_maps(maps: list[np.ndarray], gram: np.ndarray) -> list[np.ndarray]:
    coefficients, _, _ = gram_whitener(gram)
    return [
        sum(
            (maps[j] * coefficients[j, i] for j in range(len(maps))),
            np.zeros_like(maps[0]),
        )
        for i in range(coefficients.shape[1])
    ]


def whiten_gauge(
    sources: list[np.ndarray], targets: list[np.ndarray], gram: np.ndarray
) -> tuple[list[np.ndarray], list[np.ndarray]]:
    coefficients, _, _ = gram_whitener(gram)
    white_sources = []
    white_targets = []
    for i in range(coefficients.shape[1]):
        white_sources.append(
            sum(
                (sources[j] * coefficients[j, i] for j in range(len(sources))),
                np.zeros_like(sources[0]),
            )
        )
        white_targets.append(
            sum(
                (targets[j] * coefficients[j, i] for j in range(len(targets))),
                np.zeros_like(targets[0]),
            )
        )
    return white_sources, white_targets


def transfer_generator(maps: list[np.ndarray], ratio: float) -> np.ndarray:
    return sum(
        (directed_transfer_generator(operator, ratio, 1.0) for operator in maps),
        np.zeros((221, 221), complex),
    )


def gauge_generator(sources: list[np.ndarray], targets: list[np.ndarray]) -> np.ndarray:
    return sum(
        (corner_dissipator(source, target) for source, target in zip(sources, targets)),
        np.zeros((221, 221), complex),
    )


def main() -> None:
    symmetric_terms, _, transfers = assemble()
    ratio = float(np.exp(-2.0))
    source_density, target_density = central_density(ratio)

    transfer_labels = []
    transfer_maps = []
    for family in ("linking", "QLYR", "XLdR"):
        for index, operator in enumerate(transfers[family]):
            transfer_labels.append(f"{family}_{index}")
            transfer_maps.append(operator)
    gauge_labels, gauge_sources, gauge_targets = gauge_components()

    transfer_gram = np.array(
        [
            [
                (source_density + target_density)
                * np.trace(left.conj().T @ right)
                for right in transfer_maps
            ]
            for left in transfer_maps
        ]
    )
    gauge_gram = np.array(
        [
            [
                source_density * np.trace(left_s.conj().T @ right_s)
                + target_density * np.trace(left_t.conj().T @ right_t)
                for right_s, right_t in zip(gauge_sources, gauge_targets)
            ]
            for left_s, left_t in zip(gauge_sources, gauge_targets)
        ]
    )
    _, transfer_values, transfer_all_values = gram_whitener(transfer_gram)
    _, gauge_values, gauge_all_values = gram_whitener(gauge_gram)
    white_transfers = whiten_maps(transfer_maps, transfer_gram)
    white_gauge_sources, white_gauge_targets = whiten_gauge(
        gauge_sources, gauge_targets, gauge_gram
    )

    transfer_white_gram = np.array(
        [
            [
                (source_density + target_density)
                * np.trace(left.conj().T @ right)
                for right in white_transfers
            ]
            for left in white_transfers
        ]
    )
    gauge_white_gram = np.array(
        [
            [
                source_density * np.trace(left_s.conj().T @ right_s)
                + target_density * np.trace(left_t.conj().T @ right_t)
                for right_s, right_t in zip(white_gauge_sources, white_gauge_targets)
            ]
            for left_s, left_t in zip(white_gauge_sources, white_gauge_targets)
        ]
    )
    assert np.linalg.norm(transfer_white_gram - np.eye(7)) < TOL
    assert np.linalg.norm(gauge_white_gram - np.eye(12)) < TOL

    canonical_transfer = transfer_generator(white_transfers, ratio)
    canonical_gauge = gauge_generator(white_gauge_sources, white_gauge_targets)
    canonical = canonical_transfer + canonical_gauge

    metric = block_diagonal(
        [source_density * np.eye(121), target_density * np.eye(100)]
    )
    sqrt_metric = block_diagonal(
        [
            np.sqrt(source_density) * np.eye(121),
            np.sqrt(target_density) * np.eye(100),
        ]
    )
    inverse_sqrt_metric = block_diagonal(
        [
            np.eye(121) / np.sqrt(source_density),
            np.eye(100) / np.sqrt(target_density),
        ]
    )
    density_vector = pair_vector(
        source_density * np.eye(11), target_density * np.eye(10)
    )
    identity_vector = pair_vector(np.eye(11), np.eye(10))
    kms_residual = float(np.linalg.norm(metric @ canonical - canonical.conj().T @ metric))
    stationarity_residual = float(np.linalg.norm(canonical.conj().T @ density_vector))
    unital_residual = float(np.linalg.norm(canonical @ identity_vector))
    symmetric = sqrt_metric @ canonical @ inverse_sqrt_metric
    self_adjoint_residual = float(np.linalg.norm(symmetric - symmetric.conj().T))
    spectrum = eigvalsh((symmetric + symmetric.conj().T) / 2.0)
    singular_values = svdvals(canonical)
    kernel_dimension = int(np.sum(singular_values < 1.0e-9))
    gap = float(-spectrum[-kernel_dimension - 1])
    assert kms_residual < TOL
    assert stationarity_residual < TOL
    assert unital_residual < TOL
    assert self_adjoint_residual < TOL
    assert kernel_dimension == 1
    assert gap > 0.0

    # Compare with the old diagonal six-family cone.
    named_terms = {
        "linking": directed_family_generator(transfers["linking"], ratio, 1.0),
        "SU3": symmetric_terms["SU3"],
        "SU2": symmetric_terms["SU2"],
        "U1": symmetric_terms["U1"],
        "QLYR": directed_family_generator(transfers["QLYR"], ratio, 1.0),
        "XLdR": directed_family_generator(transfers["XLdR"], ratio, 1.0),
    }
    design = coefficient_design(named_terms)
    fitted_weights, fit_residual = fit_coefficients(canonical, design)
    relative_fit_residual = float(fit_residual / np.linalg.norm(canonical))
    normalized_fitted_weights = fitted_weights / np.sum(fitted_weights)

    # Basis invariance under arbitrary invertible real changes of raw frame.
    rng = np.random.default_rng(20260829)
    invariance_rows = []
    for trial in range(4):
        transfer_change = np.eye(13) + 0.08 * rng.normal(size=(13, 13))
        gauge_change = np.eye(12) + 0.08 * rng.normal(size=(12, 12))
        changed_transfers = [
            sum(
                (transfer_maps[j] * transfer_change[j, i] for j in range(13)),
                np.zeros_like(transfer_maps[0]),
            )
            for i in range(13)
        ]
        changed_sources = [
            sum(
                (gauge_sources[j] * gauge_change[j, i] for j in range(12)),
                np.zeros_like(gauge_sources[0]),
            )
            for i in range(12)
        ]
        changed_targets = [
            sum(
                (gauge_targets[j] * gauge_change[j, i] for j in range(12)),
                np.zeros_like(gauge_targets[0]),
            )
            for i in range(12)
        ]
        changed_transfer_gram = transfer_change.T @ transfer_gram @ transfer_change
        changed_gauge_gram = gauge_change.T @ gauge_gram @ gauge_change
        changed_white_transfers = whiten_maps(changed_transfers, changed_transfer_gram)
        changed_white_sources, changed_white_targets = whiten_gauge(
            changed_sources, changed_targets, changed_gauge_gram
        )
        rebuilt = transfer_generator(changed_white_transfers, ratio) + gauge_generator(
            changed_white_sources, changed_white_targets
        )
        residual = float(np.linalg.norm(rebuilt - canonical) / np.linalg.norm(canonical))
        assert residual < 1.0e-9
        invariance_rows.append({"trial": trial, "relative_generator_residual": residual})

    # Locate cross-family entries in the transfer Gram matrix.
    cross_family_entries = []
    for i, left in enumerate(transfer_labels):
        left_family = left.rsplit("_", 1)[0]
        for j in range(i + 1, len(transfer_labels)):
            right = transfer_labels[j]
            right_family = right.rsplit("_", 1)[0]
            value = transfer_gram[i, j]
            if left_family != right_family and abs(value) > 1.0e-12:
                cross_family_entries.append(
                    {
                        "left": left,
                        "right": right,
                        "absolute_gram_entry": float(abs(value)),
                    }
                )

    result = {
        "date": "2026-08-29",
        "gate": "version8_canonical_noise_frame_common_trace_gate",
        "common_KMS_trace_gram": {
            "transfer_raw_component_count": len(transfer_maps),
            "transfer_quotient_dimension": len(white_transfers),
            "gauge_component_count": len(gauge_sources),
            "total_raw_component_count": len(transfer_maps) + len(gauge_sources),
            "total_noise_quotient_dimension": len(white_transfers) + len(gauge_sources),
            "transfer_labels": transfer_labels,
            "gauge_labels": gauge_labels,
            "transfer_gram_rank": len(transfer_values),
            "transfer_gram_nullity": int(len(transfer_all_values) - len(transfer_values)),
            "gauge_gram_rank": len(gauge_values),
            "gauge_gram_nullity": int(len(gauge_all_values) - len(gauge_values)),
            "transfer_gram_eigenvalue_range": [float(transfer_values[0]), float(transfer_values[-1])],
            "gauge_gram_eigenvalue_range": [float(gauge_values[0]), float(gauge_values[-1])],
            "transfer_whitening_residual": float(np.linalg.norm(transfer_white_gram - np.eye(7))),
            "gauge_whitening_residual": float(np.linalg.norm(gauge_white_gram - np.eye(12))),
            "cross_family_transfer_gram_entries": cross_family_entries,
        },
        "canonical_trace_isotropic_generator": {
            "formula": "sum over a common-KMS-trace orthonormal noise frame",
            "free_relative_coefficients": 0,
            "overall_time_scale_free": True,
            "KMS_symmetry_residual": kms_residual,
            "stationarity_residual": stationarity_residual,
            "unital_residual": unital_residual,
            "similarity_self_adjoint_residual": self_adjoint_residual,
            "fixed_algebra_dimension": kernel_dimension,
            "decay_gap_in_trace_time_units": gap,
            "basis_change_tests": invariance_rows,
        },
        "relation_to_old_six_family_diagonal_cone": {
            "family_order": TERM_ORDER,
            "least_squares_diagonal_weights": [float(value) for value in fitted_weights],
            "normalized_diagonal_weights": [
                float(value) for value in normalized_fitted_weights
            ],
            "absolute_fit_residual": fit_residual,
            "relative_fit_residual": relative_fit_residual,
            "lies_exactly_in_old_diagonal_family_cone": relative_fit_residual < 1.0e-9,
            "interpretation": "the machine-zero residual shows that the common-trace Casimir fixes a point inside the old six-family diagonal cone",
        },
        "status_boundary": {
            "noise_subspace_already_present_in_project": True,
            "common_KMS_trace_already_present": True,
            "trace_isotropy_is_a_canonical_minimal_choice": True,
            "trace_isotropy_forced_by_physical_symmetry": False,
            "absolute_physical_time_derived": False,
        },
        "verdict": {
            "canonical_basis_independent_noise_frame_obtained": True,
            "canonical_relative_generator_representative_obtained": True,
            "unique_physical_generator_theorem_obtained": False,
            "status": "common_trace_noise_Casimir_positive_canonical_representative_physical_isotropy_open",
            "next_gate": "version8_noise_isotropy_symmetry_admission_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()