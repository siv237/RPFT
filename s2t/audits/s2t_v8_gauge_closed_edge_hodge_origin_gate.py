#!/usr/bin/env python3
"""Test whether canonical gauge/chain data derive the full edge-Hodge masses."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_gauge_closed_edge_hodge_origin_gate_results.json"
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
from s2t_v8_kms_nontracial_relative_rate_selector_gate import (  # noqa: E402
    central_density,
)
from s2t_v8_noise_isotropy_symmetry_admission_gate import (  # noqa: E402
    commutant_dimension,
    lie_orbit_closure,
    orthonormal_map_span,
)


def rounded(values) -> list[float]:
    return [float(f"{value:.12g}") for value in values]


def coordinates(matrix: np.ndarray, frame: list[np.ndarray]) -> np.ndarray:
    return np.array([np.trace(item.conj().T @ matrix) for item in frame])


def spectral_projector(matrix: np.ndarray, value: float) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    selected = np.abs(eigenvalues - value) < 1.0e-8
    return eigenvectors[:, selected] @ eigenvectors[:, selected].conj().T


def subset_real_indices(complex_ranks: list[int]) -> list[int]:
    values = set()
    for choices in itertools.product((0, 1), repeat=len(complex_ranks)):
        values.add(2 * sum(rank * choice for rank, choice in zip(complex_ranks, choices)))
    return sorted(values)


def main() -> None:
    background, variations, _, _ = physical_blocks()
    _, gauge_sources, gauge_targets = gauge_components()
    incidence_orbit, incidence_sequence = lie_orbit_closure(
        [background], gauge_sources, gauge_targets
    )
    incidence_frame = orthonormal_map_span(incidence_orbit)
    heavy_frame = orthonormal_map_span(variations[7:])
    transfer_frame = orthonormal_map_span(incidence_frame + heavy_frame)
    transfer_rep, closure_residual, _ = transfer_infinitesimal_representation(
        gauge_sources, gauge_targets, transfer_frame
    )
    assert incidence_sequence == [1, 4, 5, 5]
    assert len(incidence_frame) == 5
    assert len(transfer_frame) == 15
    assert closure_residual < TOL

    gauge_casimir = sum(
        (matrix.conj().T @ matrix for matrix in transfer_rep),
        np.zeros((15, 15), complex),
    )
    casimir_values = np.linalg.eigvalsh(gauge_casimir)
    expected_casimir = np.array([0.0] + [1.0] * 8 + [16.0 / 9.0] * 6)
    assert np.linalg.norm(casimir_values - expected_casimir) < TOL

    gamma_source = np.diag([1.0] * 6 + [-1.0] * 5)
    gamma_target = np.diag([1.0] * 6 + [-1.0] * 4)
    sector_order = np.column_stack(
        [
            coordinates(gamma_target @ item - item @ gamma_source, transfer_frame)
            for item in transfer_frame
        ]
    )
    order_values = np.linalg.eigvalsh(
        (sector_order + sector_order.conj().T) / 2.0
    )
    assert np.linalg.norm(
        order_values - np.array([-2.0] * 3 + [0.0] * 9 + [2.0] * 3)
    ) < TOL
    assert np.linalg.norm(gauge_casimir @ sector_order - sector_order @ gauge_casimir) < TOL

    incidence_coordinates = np.column_stack(
        [coordinates(item, transfer_frame) for item in incidence_frame]
    )
    incidence_projector = incidence_coordinates @ incidence_coordinates.conj().T
    assert int(np.linalg.matrix_rank(incidence_projector, tol=TOL)) == 5

    joint_rows = []
    joint_projectors = []
    for casimir_value in (0.0, 1.0, 16.0 / 9.0):
        casimir_projector = spectral_projector(gauge_casimir, casimir_value)
        for order_value in (-2.0, 0.0, 2.0):
            order_projector = spectral_projector(sector_order, order_value)
            joint = casimir_projector @ order_projector
            rank = int(round(float(np.trace(joint).real)))
            if rank == 0:
                continue
            overlap = float(np.trace(incidence_projector @ joint).real)
            joint_rows.append(
                {
                    "gauge_casimir": casimir_value,
                    "sector_order": order_value,
                    "complex_rank": rank,
                    "incidence_overlap_rank": int(round(overlap)),
                }
            )
            joint_projectors.append(joint)
    assert [row["complex_rank"] for row in joint_rows] == [1, 8, 3, 3]
    assert [row["incidence_overlap_rank"] for row in joint_rows] == [1, 4, 0, 0]

    best_incidence_approximation = sum(
        (
            float(np.trace(projector @ incidence_projector).real)
            / float(np.trace(projector).real)
            * projector
            for projector in joint_projectors
        ),
        np.zeros((15, 15), complex),
    )
    incidence_hilbert_schmidt_residual = float(
        np.linalg.norm(incidence_projector - best_incidence_approximation)
    )
    incidence_operator_residual = float(
        np.linalg.norm(incidence_projector - best_incidence_approximation, 2)
    )
    incidence_relative_residual = incidence_hilbert_schmidt_residual / float(
        np.linalg.norm(incidence_projector)
    )
    assert abs(incidence_hilbert_schmidt_residual - np.sqrt(2.0)) < TOL
    assert abs(incidence_operator_residual - 0.5) < TOL

    representative_incidence_mass = 4.0
    representative_heavy_mass = 3.6
    representative_mass = (
        representative_incidence_mass * incidence_projector
        + representative_heavy_mass * (np.eye(15) - incidence_projector)
    )
    best_mass_approximation = sum(
        (
            float(np.trace(projector @ representative_mass).real)
            / float(np.trace(projector).real)
            * projector
            for projector in joint_projectors
        ),
        np.zeros((15, 15), complex),
    )
    representative_mass_residual = float(
        np.linalg.norm(representative_mass - best_mass_approximation)
    )
    assert abs(representative_mass_residual - 0.4 * np.sqrt(2.0)) < TOL

    base_commutant_dimension, _ = commutant_dimension(transfer_rep)
    enriched_commutant_dimension, _ = commutant_dimension(
        transfer_rep + [gauge_casimir, sector_order, 2.0 * np.eye(15)]
    )
    assert base_commutant_dimension == enriched_commutant_dimension == 13

    signed_joint_ranks = [row["complex_rank"] for row in joint_rows]
    even_joint_ranks = [1, 8, 6]
    signed_possible_real_indices = subset_real_indices(signed_joint_ranks)
    even_possible_real_indices = subset_real_indices(even_joint_ranks)
    assert 10 not in signed_possible_real_indices
    assert 10 not in even_possible_real_indices

    common_trace_rows = []
    for ratio in (1.0, float(np.exp(-2.0)), 22.0 / 21.0, 21.0 / 22.0):
        source_density, target_density = central_density(ratio)
        gram = (source_density + target_density) * np.eye(15)
        values = np.linalg.eigvalsh(gram)
        common_trace_rows.append(
            {
                "target_to_source_density_ratio": ratio,
                "transfer_gram_eigenvalue": float(values[0]),
                "condition_number": float(values[-1] / values[0]),
                "incidence_to_heavy_weight_ratio": 1.0,
            }
        )
    assert max(abs(row["condition_number"] - 1.0) for row in common_trace_rows) < TOL

    previous = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v8_isotypic_relative_curvature_parent_hessian_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert previous["gauge_invariant_incidence_heavy_completion"][
        "origin_signature_depends_on_mass_completion"
    ]

    result = {
        "date": "2026-08-29",
        "gate": "version8_gauge_closed_edge_hodge_origin_gate",
        "canonical_operator_algebra": {
            "transfer_complex_dimension": 15,
            "gauge_casimir_spectrum": rounded(casimir_values),
            "sector_order_spectrum": rounded(order_values),
            "chain_bohr_degree_on_all_transfers": 2,
            "joint_spectral_blocks": joint_rows,
            "base_gauge_commutant_dimension": base_commutant_dimension,
            "commutant_dimension_after_casimir_sector_order_and_degree": enriched_commutant_dimension,
        },
        "incidence_projector_reconstruction": {
            "incidence_complex_rank": 5,
            "best_joint_function_hilbert_schmidt_residual": incidence_hilbert_schmidt_residual,
            "best_joint_function_operator_norm_residual": incidence_operator_residual,
            "best_joint_function_relative_hilbert_schmidt_residual": incidence_relative_residual,
            "unresolved_degenerate_block_complex_rank": 8,
            "incidence_rank_inside_degenerate_block": 4,
            "heavy_rank_inside_degenerate_block": 4,
            "incidence_projector_is_function_of_casimir_order_and_degree": False,
        },
        "representative_two_mass_metric": {
            "incidence_mass": representative_incidence_mass,
            "heavy_mass": representative_heavy_mass,
            "best_canonical_operator_algebra_residual": representative_mass_residual,
            "best_degenerate_block_scalar_mass": 3.8,
            "exact_two_mass_metric_reconstructed": False,
        },
        "common_kms_trace": {
            "rows": common_trace_rows,
            "transfer_metric_is_scalar_for_every_endpoint_density_ratio": True,
            "derives_incidence_heavy_ratio": False,
        },
        "morse_index_constraint": {
            "signed_joint_block_complex_ranks": signed_joint_ranks,
            "possible_real_indices_from_signed_joint_spectral_selectors": signed_possible_real_indices,
            "even_joint_block_complex_ranks": even_joint_ranks,
            "possible_real_indices_from_even_joint_spectral_selectors": even_possible_real_indices,
            "ten_real_incidence_index_available": False,
        },
        "verdict": {
            "gauge_casimir_derives_two_edge_hodge_masses": False,
            "chain_degree_derives_two_edge_hodge_masses": False,
            "quark_lepton_grading_derives_two_edge_hodge_masses": False,
            "common_kms_trace_derives_two_edge_hodge_masses": False,
            "four_plus_four_multiplicity_ambiguity_remains": True,
            "using_incidence_projector_at_origin_without_new_selector_is_circular": True,
            "unique_gauge_closed_edge_hodge_origin_obtained": False,
            "full_parent_action_obtained": False,
            "next_gate": "version8_real_incidence_multiplicity_quotient_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()