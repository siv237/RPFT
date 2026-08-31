#!/usr/bin/env python3
"""Test whether one common curvature derives the remaining Gram weight."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import block_diag, eigvalsh, svd


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_bimodule_common_curvature_relative_weight_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (  # noqa: E402
    physical_blocks,
    physical_hessians,
    signature,
)
from s2t_v8_bimodule_multiplicity_separator_gate import (  # noqa: E402
    close_under_blocks,
    endpoint_projectors,
    realification,
)
from s2t_v8_canonical_noise_frame_common_trace_gate import (  # noqa: E402
    gauge_components,
)
from s2t_v8_noise_isotropy_symmetry_admission_gate import (  # noqa: E402
    lie_orbit_closure,
    orthonormal_map_span,
)


def transfer_frame() -> tuple[np.ndarray, list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    background, variations, _, _ = physical_blocks()
    _, gauge_sources, gauge_targets = gauge_components()
    projectors = endpoint_projectors()
    incidence_orbit, sequence = lie_orbit_closure(
        [background], gauge_sources, gauge_targets
    )
    assert sequence == [1, 4, 5, 5]
    incidence = close_under_blocks(
        orthonormal_map_span(incidence_orbit), projectors
    )
    heavy = close_under_blocks(
        orthonormal_map_span(variations[7:]), projectors
    )
    frame = incidence + heavy
    frame_gram = np.array(
        [
            [np.trace(left.conj().T @ right) for right in frame]
            for left in frame
        ]
    )
    assert np.linalg.norm(frame_gram - np.eye(20)) < TOL
    assert len(incidence) == 10 and len(heavy) == 10 and len(frame) == 20
    return background, frame, gauge_sources, gauge_targets


def representation_matrices(
    frame: list[np.ndarray],
    gauge_sources: list[np.ndarray],
    gauge_targets: list[np.ndarray],
) -> tuple[list[np.ndarray], list[np.ndarray], float]:
    transfer = []
    endpoint = []
    residual = 0.0
    for source, target in zip(gauge_sources, gauge_targets):
        matrix = np.zeros((20, 20), complex)
        for column, item in enumerate(frame):
            transformed = 1j * (target @ item - item @ source)
            coefficients = np.array(
                [np.trace(basis.conj().T @ transformed) for basis in frame]
            )
            matrix[:, column] = coefficients
            reconstructed = sum(
                (
                    coefficients[index] * frame[index]
                    for index in range(len(frame))
                ),
                np.zeros_like(item),
            )
            residual = max(residual, float(np.linalg.norm(transformed - reconstructed)))
        transfer.append(matrix)
        endpoint.append(1j * block_diag(target, source))
    return transfer, endpoint, residual


def intertwiner_audit(
    transfer: list[np.ndarray], endpoint: list[np.ndarray]
) -> dict[str, object]:
    constraints = np.vstack(
        [
            np.kron(np.eye(21), left)
            - np.kron(right.T, np.eye(20))
            for left, right in zip(transfer, endpoint)
        ]
    )
    _, values, right_vectors = svd(constraints, full_matrices=False)
    rank = int(np.sum(values > TOL))
    nullity = 20 * 21 - rank
    null_basis = right_vectors[rank:].conj().T
    intertwiners = [
        null_basis[:, index].reshape((20, 21), order="F")
        for index in range(nullity)
    ]
    common_coimage_values = np.linalg.svd(
        np.vstack(intertwiners), compute_uv=False
    )
    common_coimage_rank = int(np.sum(common_coimage_values > TOL))
    deterministic = sum(
        ((index + 1.0) * item for index, item in enumerate(intertwiners)),
        np.zeros((20, 21), complex),
    )
    deterministic_values = np.linalg.svd(deterministic, compute_uv=False)
    deterministic_rank = int(np.sum(deterministic_values > TOL))
    assert nullity == 13
    assert common_coimage_rank == 9
    assert deterministic_rank == 9
    return {
        "constraint_shape": list(constraints.shape),
        "intertwiner_complex_dimension": nullity,
        "common_endpoint_coimage_rank": common_coimage_rank,
        "common_endpoint_kernel_dimension": 21 - common_coimage_rank,
        "deterministic_generic_rank": deterministic_rank,
        "largest_rank_is_strictly_below_twenty": True,
        "smallest_constraint_singular_values": [
            float(value) for value in values[-16:]
        ],
        "deterministic_nonzero_singular_values": [
            float(value) for value in deterministic_values[:deterministic_rank]
        ],
    }


def common_trace_audit() -> dict[str, object]:
    rng = np.random.default_rng(20260829)
    edge_moment = rng.normal(size=20)
    trial = rng.normal(size=(10, 11)) + 1j * rng.normal(size=(10, 11))
    reference = rng.normal(size=(10, 11)) + 1j * rng.normal(size=(10, 11))
    gram_source = trial.conj().T @ trial - reference.conj().T @ reference
    gram_target = trial @ trial.conj().T - reference @ reference.conj().T
    edge_curvature = block_diag(np.diag(edge_moment), -np.diag(edge_moment))
    gram_curvature = block_diag(gram_target, gram_source)
    edge_action = float(np.sum(edge_moment**2))
    gram_action = float(
        0.5
        * (
            np.vdot(gram_source, gram_source).real
            + np.vdot(gram_target, gram_target).real
        )
    )
    rows = []
    for beta in (0.25, 0.5, 1.0, 2.0, 4.0):
        common = block_diag(edge_curvature, np.sqrt(beta) * gram_curvature)
        action = float(0.5 * np.trace(common.conj().T @ common).real)
        expected = edge_action + beta * gram_action
        real_completed = block_diag(common, common.conj())
        real_half_action = float(
            0.25 * np.trace(real_completed.conj().T @ real_completed).real
        )
        rows.append(
            {
                "beta": beta,
                "common_trace_action": action,
                "expected_action": expected,
                "real_half_trace_action": real_half_action,
                "residual": abs(action - expected),
                "real_completion_residual": abs(real_half_action - expected),
                "required_gram_curvature_rescaling": float(np.sqrt(beta)),
            }
        )
    assert max(row["residual"] for row in rows) < 1.0e-8
    assert max(row["real_completion_residual"] for row in rows) < 1.0e-8

    common_dimension = edge_curvature.shape[0] + gram_curvature.shape[0]
    edge_projector = block_diag(np.eye(40), np.zeros((21, 21)))
    gram_projector = np.eye(common_dimension) - edge_projector
    central_rows = []
    for eta in (0.25, 0.5, 1.0, 2.0, 4.0):
        metric = edge_projector + eta * gram_projector
        central_rows.append(
            {
                "eta": eta,
                "minimum_metric_eigenvalue": float(eigvalsh(metric)[0]),
                "edge_projector_commutator": float(
                    np.linalg.norm(metric @ edge_projector - edge_projector @ metric)
                ),
                "gram_projector_commutator": float(
                    np.linalg.norm(metric @ gram_projector - gram_projector @ metric)
                ),
            }
        )
    return {
        "edge_real_curvature_dimension": 40,
        "endpoint_gram_curvature_dimension": 21,
        "common_curvature_dimension": common_dimension,
        "rows": rows,
        "unweighted_common_trace_beta": 1.0,
        "beta_half_requires_inserted_rescaling": "Omega_Gram/sqrt(2)",
        "real_half_trace_changes_relative_weight": False,
        "central_metric_family": central_rows,
        "central_projectors_remain_independent": True,
    }


def hessian_audit(
    background: np.ndarray, frame: list[np.ndarray]
) -> dict[str, object]:
    real_frame = realification(frame)
    gram_origin, gram_vacuum = physical_hessians(background, real_frame)
    incidence = np.diag([1.0] * 20 + [0.0] * 20)
    edge_origin = -4.0 * incidence + 4.0 * (np.eye(40) - incidence)
    edge_vacuum = 8.0 * incidence + 4.0 * (np.eye(40) - incidence)
    rows = []
    for beta in (0.5, 2.0 / 3.0, 1.0):
        origin_values = eigvalsh(edge_origin + beta * gram_origin)
        vacuum_values = eigvalsh(edge_vacuum + beta * gram_vacuum)
        rows.append(
            {
                "beta": beta,
                "origin_signature": signature(origin_values),
                "vacuum_signature_without_isotypic_positive_term": signature(
                    vacuum_values
                ),
                "origin_minimum_eigenvalue": float(origin_values[0]),
            }
        )
    assert rows[0]["origin_signature"] == [20, 0, 20]
    assert rows[1]["origin_signature"] == [20, 12, 8]
    assert rows[2]["origin_signature"] == [38, 0, 2]
    return {
        "rows": rows,
        "beta_half_passes_origin_selector": True,
        "unweighted_beta_one_passes_origin_selector": False,
        "critical_beta": 2.0 / 3.0,
    }


def main() -> None:
    background, frame, gauge_sources, gauge_targets = transfer_frame()
    transfer, endpoint, covariance_residual = representation_matrices(
        frame, gauge_sources, gauge_targets
    )
    assert covariance_residual < TOL
    intertwiners = intertwiner_audit(transfer, endpoint)
    common_trace = common_trace_audit()
    hessian = hessian_audit(background, frame)

    result = {
        "date": "2026-08-29",
        "gate": "version8_bimodule_common_curvature_relative_weight_gate",
        "carrier": {
            "transfer_complex_dimension": 20,
            "endpoint_complex_dimension": 21,
            "transfer_representation_covariance_residual": covariance_residual,
        },
        "covariant_connector_test": intertwiners,
        "common_curvature_trace": common_trace,
        "hessian_test": hessian,
        "verdict": {
            "one_unweighted_common_trace_derives_beta_one": True,
            "beta_one_is_physical_selector_failure": True,
            "beta_half_is_stable_representative": True,
            "beta_half_derived": False,
            "real_half_trace_derives_beta_half": False,
            "full_rank_covariant_endpoint_transfer_connector_exists": False,
            "central_metric_family_removed": False,
            "full_parent_action_obtained": False,
            "next_gate": "version8_nonlinear_incidence_boundary_connector_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()