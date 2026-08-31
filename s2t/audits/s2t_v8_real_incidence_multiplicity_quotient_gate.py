#!/usr/bin/env python3
"""Test whether Real orientation doubling selects the 4+4 incidence copy."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import expm


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_real_incidence_multiplicity_quotient_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (  # noqa: E402
    physical_blocks,
)
from s2t_v8_canonical_noise_frame_common_trace_gate import (  # noqa: E402
    gauge_components,
)
from s2t_v8_gauge_closed_field_space_superconnection_gate import (  # noqa: E402
    transfer_infinitesimal_representation,
)
from s2t_v8_noise_isotropy_symmetry_admission_gate import (  # noqa: E402
    commutant_dimension,
    lie_orbit_closure,
    orthonormal_map_span,
)


def coordinates(matrix: np.ndarray, frame: list[np.ndarray]) -> np.ndarray:
    return np.array([np.trace(item.conj().T @ matrix) for item in frame])


def spectral_projector(matrix: np.ndarray, value: float) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    selected = np.abs(eigenvalues - value) < 1.0e-8
    return eigenvectors[:, selected] @ eigenvectors[:, selected].conj().T


def commutant_basis(matrices: list[np.ndarray]) -> list[np.ndarray]:
    dimension = matrices[0].shape[0]
    identity = np.eye(dimension)
    constraints = np.vstack(
        [
            np.kron(matrix.T, identity) - np.kron(identity, matrix)
            for matrix in matrices
        ]
    )
    _, singular_values, right = np.linalg.svd(constraints, full_matrices=True)
    threshold = max(TOL, 1.0e-10 * singular_values[0])
    rank = int(np.sum(singular_values > threshold))
    null_vectors = right.conj().T[:, rank:]
    return [
        null_vectors[:, index].reshape((dimension, dimension), order="F")
        for index in range(null_vectors.shape[1])
    ]


def main() -> None:
    background, variations, _, _ = physical_blocks()
    _, gauge_sources, gauge_targets = gauge_components()
    incidence_orbit, _ = lie_orbit_closure(
        [background], gauge_sources, gauge_targets
    )
    incidence_frame = orthonormal_map_span(incidence_orbit)
    transfer_frame = orthonormal_map_span(
        incidence_frame + orthonormal_map_span(variations[7:])
    )
    transfer_rep, closure_residual, _ = transfer_infinitesimal_representation(
        gauge_sources, gauge_targets, transfer_frame
    )
    assert len(incidence_frame) == 5
    assert len(transfer_frame) == 15
    assert closure_residual < TOL

    incidence_coordinates = np.column_stack(
        [coordinates(item, transfer_frame) for item in incidence_frame]
    )
    incidence_projector = incidence_coordinates @ incidence_coordinates.conj().T
    gauge_casimir = sum(
        (matrix.conj().T @ matrix for matrix in transfer_rep),
        np.zeros((15, 15), complex),
    )
    gamma_source = np.diag([1.0] * 6 + [-1.0] * 5)
    gamma_target = np.diag([1.0] * 6 + [-1.0] * 4)
    sector_order = np.column_stack(
        [
            coordinates(gamma_target @ item - item @ gamma_source, transfer_frame)
            for item in transfer_frame
        ]
    )

    degenerate_projector = (
        spectral_projector(gauge_casimir, 1.0)
        @ spectral_projector(sector_order, 0.0)
    )
    eigenvalues, eigenvectors = np.linalg.eigh(
        (degenerate_projector + degenerate_projector.conj().T) / 2.0
    )
    degenerate_frame = eigenvectors[:, eigenvalues > 0.5]
    assert degenerate_frame.shape == (15, 8)

    restricted_rep = [
        degenerate_frame.conj().T @ matrix @ degenerate_frame
        for matrix in transfer_rep
    ]
    restricted_incidence = (
        degenerate_frame.conj().T
        @ incidence_projector
        @ degenerate_frame
    )
    restricted_commutant_dimension, commutant_tail = commutant_dimension(
        restricted_rep
    )
    assert int(np.linalg.matrix_rank(restricted_incidence, tol=TOL)) == 4
    assert restricted_commutant_dimension == 10
    assert max(
        float(np.linalg.norm(restricted_incidence @ matrix - matrix @ restricted_incidence))
        for matrix in restricted_rep
    ) < TOL

    basis = commutant_basis(restricted_rep)
    assert len(basis) == restricted_commutant_dimension
    rng = np.random.default_rng(20260829)
    hermitian = sum(
        (rng.normal() * item for item in basis),
        np.zeros((8, 8), complex),
    )
    hermitian = (hermitian + hermitian.conj().T) / 2.0
    complement = np.eye(8) - restricted_incidence
    mixing = (
        complement @ hermitian @ restricted_incidence
        + restricted_incidence @ hermitian @ complement
    )
    mixing_norm = float(np.linalg.norm(mixing))
    assert mixing_norm > 0.1
    mixing /= mixing_norm
    mixing_gauge_residual = max(
        float(np.linalg.norm(mixing @ matrix - matrix @ mixing))
        for matrix in restricted_rep
    )
    assert mixing_gauge_residual < TOL

    exchange = np.block(
        [
            [np.zeros((8, 8)), np.eye(8)],
            [np.eye(8), np.zeros((8, 8))],
        ]
    )
    rotation_rows = []
    for theta in (0.0, 0.2, 0.5, 1.0, 1.5):
        unitary = expm(1j * theta * mixing)
        projector = (
            unitary @ restricted_incidence @ unitary.conj().T
        )
        doubled_projector = np.block(
            [
                [projector, np.zeros((8, 8))],
                [np.zeros((8, 8)), projector.conj()],
            ]
        )
        rotation_rows.append(
            {
                "theta": theta,
                "projector_complex_rank": int(
                    np.linalg.matrix_rank(projector, tol=TOL)
                ),
                "distance_from_incidence_projector": float(
                    np.linalg.norm(projector - restricted_incidence)
                ),
                "incidence_overlap": float(
                    np.trace(restricted_incidence @ projector).real
                ),
                "maximum_gauge_commutator_residual": max(
                    float(np.linalg.norm(projector @ matrix - matrix @ projector))
                    for matrix in restricted_rep
                ),
                "real_exchange_compatibility_residual": float(
                    np.linalg.norm(
                        exchange @ doubled_projector.conj() @ exchange
                        - doubled_projector
                    )
                ),
                "real_fixed_projector_rank": 2
                * int(np.linalg.matrix_rank(projector, tol=TOL)),
            }
        )
    assert max(row["maximum_gauge_commutator_residual"] for row in rotation_rows) < TOL
    assert max(row["real_exchange_compatibility_residual"] for row in rotation_rows) < TOL
    assert rotation_rows[-1]["distance_from_incidence_projector"] > 1.0

    random_operator = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    doubled_operator = np.block(
        [
            [random_operator, np.zeros((8, 8))],
            [np.zeros((8, 8)), random_operator.conj()],
        ]
    )
    half_trace = 0.5 * np.trace(doubled_operator.conj().T @ doubled_operator).real
    oriented_trace = np.trace(random_operator.conj().T @ random_operator).real
    half_trace_residual = float(abs(half_trace - oriented_trace))
    assert half_trace_residual < TOL

    result = {
        "date": "2026-08-29",
        "gate": "version8_real_incidence_multiplicity_quotient_gate",
        "orientation_type": {
            "oriented_transfer_shape": [10, 11],
            "real_partner_shape": [11, 10],
            "real_maps_oriented_half_to_opposite_half": True,
            "real_is_internal_endomorphism_of_oriented_half": False,
            "oriented_transfer_complex_dimension": 15,
            "real_doubled_transfer_complex_dimension": 30,
            "real_fixed_selfadjoint_dimension_real": 30,
            "real_doubling_reduces_physical_real_dimension": False,
        },
        "degenerate_four_plus_four_block": {
            "complex_dimension": 8,
            "incidence_complex_rank": 4,
            "heavy_complex_rank": 4,
            "restricted_gauge_commutant_dimension_complex": restricted_commutant_dimension,
            "commutant_smallest_singular_values": [
                float(value) for value in commutant_tail
            ],
            "gauge_commuting_copy_mixing_exists": True,
            "mixing_generator_norm_before_normalization": mixing_norm,
            "mixing_generator_gauge_residual": mixing_gauge_residual,
        },
        "real_compatible_projector_orbit": {
            "rows": rotation_rows,
            "all_projectors_have_complex_rank_four": True,
            "all_projectors_are_gauge_invariant": True,
            "all_doubled_projectors_are_real_compatible": True,
            "real_fixed_rank_for_each_projector": 8,
            "projector_is_unique": False,
        },
        "real_half_trace": {
            "identity": "0.5 Tr_doubled diag(X,conj X)^*diag(X,conj X)=Tr X*X",
            "residual": half_trace_residual,
            "weights_incidence_and_heavy_uniformly": True,
            "derives_incidence_heavy_mass_ratio": False,
        },
        "verdict": {
            "real_orientation_doubling_splits_four_plus_four": False,
            "real_fixed_quotient_selects_incidence_copy": False,
            "real_half_trace_selects_incidence_copy": False,
            "real_structure_alone_derives_edge_hodge_metric": False,
            "full_parent_action_obtained": False,
            "next_gate": "version8_bimodule_multiplicity_separator_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()