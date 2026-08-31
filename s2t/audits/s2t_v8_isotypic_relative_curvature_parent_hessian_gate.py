#!/usr/bin/env python3
"""Combine the smooth isotypic curvature with old and gauge-closed Hessians."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_isotypic_relative_curvature_parent_hessian_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (  # noqa: E402
    edge_hessians,
    physical_blocks,
    physical_hessians,
    signature,
)
from s2t_v8_canonical_noise_frame_common_trace_gate import (  # noqa: E402
    gauge_components,
)
from s2t_v8_gauge_closed_field_space_superconnection_gate import (  # noqa: E402
    transfer_infinitesimal_representation,
)
from s2t_v8_noise_isotropy_symmetry_admission_gate import (  # noqa: E402
    lie_orbit_closure,
    orthonormal_map_span,
)


def rounded(values) -> list[float]:
    return [float(f"{value:.12g}") for value in values]


def realification(frame: list[np.ndarray]) -> list[np.ndarray]:
    return [direction for item in frame for direction in (item, 1j * item)]


def real_representation(matrix: np.ndarray) -> np.ndarray:
    dimension = matrix.shape[0]
    result = np.zeros((2 * dimension, 2 * dimension))
    for column in range(dimension):
        for phase, real_column in ((1.0, 2 * column), (1j, 2 * column + 1)):
            transformed = phase * matrix[:, column]
            for row in range(dimension):
                result[2 * row, real_column] = transformed[row].real
                result[2 * row + 1, real_column] = transformed[row].imag
    return result


def main() -> None:
    background, old_variations, _, down_cut = physical_blocks()
    _, gauge_sources, gauge_targets = gauge_components()

    incidence_orbit, incidence_sequence = lie_orbit_closure(
        [background], gauge_sources, gauge_targets
    )
    incidence_frame = orthonormal_map_span(incidence_orbit)
    heavy_frame = orthonormal_map_span(old_variations[7:])
    transfer_frame = orthonormal_map_span(incidence_frame + heavy_frame)
    transfer_real = realification(transfer_frame)
    incidence_real = realification(incidence_frame)

    assert incidence_sequence == [1, 4, 5, 5]
    assert len(incidence_frame) == 5
    assert len(heavy_frame) == 10
    assert len(transfer_frame) == 15
    assert len(transfer_real) == 30

    gamma_source = np.diag([1.0] * 6 + [-1.0] * 5)
    gamma_target = np.diag([1.0] * 6 + [-1.0] * 4)

    def order(field: np.ndarray) -> np.ndarray:
        return gamma_target @ field - field @ gamma_source

    left_gram = background @ background.conj().T
    right_gram = background.conj().T @ background

    def linearized_relative(variation: np.ndarray) -> np.ndarray:
        value = order(variation)
        return left_gram @ value - value @ right_gram

    def isotypic_hessian(directions: list[np.ndarray]) -> np.ndarray:
        return np.array(
            [
                [
                    2.0
                    * np.real(
                        np.vdot(
                            linearized_relative(left),
                            linearized_relative(right),
                        )
                    )
                    for right in directions
                ]
                for left in directions
            ]
        )

    old_physical_origin, old_physical_vacuum = physical_hessians(
        background, old_variations
    )
    old_edge_origin, old_edge_vacuum = edge_hessians(
        down_cut, len(old_variations)
    )
    old_origin = old_edge_origin + 0.5 * old_physical_origin
    old_vacuum = old_edge_vacuum + 0.5 * old_physical_vacuum
    old_isotypic = isotypic_hessian(old_variations)
    assert signature(eigvalsh(old_origin)) == [7, 0, 20]
    assert int(np.linalg.matrix_rank(old_isotypic, tol=TOL)) == 12

    old_weight_scan = []
    for weight in (0.0, 1.0e-6, 1.0e-2, 1.0e-1, 1.0, 4.0, 100.0, 1.0e6):
        origin_values = eigvalsh(old_origin)
        vacuum_values = eigvalsh(old_vacuum + weight * old_isotypic)
        old_weight_scan.append(
            {
                "isotypic_weight": weight,
                "origin_signature": signature(origin_values),
                "vacuum_signature": signature(vacuum_values),
                "vacuum_minimum_eigenvalue": float(vacuum_values[0]),
                "vacuum_maximum_eigenvalue": float(vacuum_values[-1]),
            }
        )
    assert all(row["origin_signature"] == [7, 0, 20] for row in old_weight_scan)
    assert all(row["vacuum_signature"] == [0, 0, 27] for row in old_weight_scan)

    full_physical_origin, full_physical_vacuum = physical_hessians(
        background, transfer_real
    )
    full_isotypic = isotypic_hessian(transfer_real)
    assert signature(eigvalsh(full_physical_origin)) == [30, 0, 0]
    assert signature(eigvalsh(full_physical_vacuum)) == [0, 2, 28]
    assert int(np.linalg.matrix_rank(full_isotypic, tol=TOL)) == 12

    vacuum_values, vacuum_vectors = np.linalg.eigh(
        (full_physical_vacuum + full_physical_vacuum.T) / 2.0
    )
    gram_kernel = vacuum_vectors[:, np.abs(vacuum_values) <= TOL]
    isotypic_on_gram_kernel = eigvalsh(
        (gram_kernel.T @ full_isotypic @ gram_kernel)
    )
    assert len(isotypic_on_gram_kernel) == 2
    assert np.max(np.abs(isotypic_on_gram_kernel)) < TOL

    incidence_projector = np.array(
        [
            [
                sum(
                    np.real(np.vdot(direction, left))
                    * np.real(np.vdot(direction, right))
                    for direction in incidence_real
                )
                for right in transfer_real
            ]
            for left in transfer_real
        ]
    )
    assert np.linalg.norm(incidence_projector.T - incidence_projector) < TOL
    assert np.linalg.norm(incidence_projector @ incidence_projector - incidence_projector) < TOL
    assert int(np.linalg.matrix_rank(incidence_projector, tol=TOL)) == 10

    transfer_rep, _, _ = transfer_infinitesimal_representation(
        gauge_sources, gauge_targets, transfer_frame
    )
    real_transfer_rep = [real_representation(item) for item in transfer_rep]
    projector_covariance_residual = max(
        float(np.linalg.norm(incidence_projector @ item - item @ incidence_projector))
        for item in real_transfer_rep
    )
    assert projector_covariance_residual < TOL

    complex_structure = np.kron(np.eye(15), np.array([[0.0, -1.0], [1.0, 0.0]]))
    assert np.linalg.norm(incidence_projector @ complex_structure - complex_structure @ incidence_projector) < TOL

    completion_scan = []
    for incidence_mass, heavy_mass in (
        (0.0, 0.0),
        (1.0, 0.1),
        (2.0, 1.0),
        (3.0, 2.0),
        (4.0, 3.6),
        (5.0, 5.0),
        (10.0, 0.1),
        (0.1, 10.0),
    ):
        edge_origin = (
            -incidence_mass * incidence_projector
            + heavy_mass * (np.eye(30) - incidence_projector)
        )
        edge_vacuum = (
            2.0 * incidence_mass * incidence_projector
            + heavy_mass * (np.eye(30) - incidence_projector)
        )
        origin_values = eigvalsh(edge_origin + 0.5 * full_physical_origin)
        vacuum_values = eigvalsh(edge_vacuum + 0.5 * full_physical_vacuum + full_isotypic)
        completion_scan.append(
            {
                "incidence_mass": incidence_mass,
                "heavy_mass": heavy_mass,
                "origin_signature": signature(origin_values),
                "vacuum_signature": signature(vacuum_values),
                "origin_minimum_eigenvalue": float(origin_values[0]),
                "origin_maximum_eigenvalue": float(origin_values[-1]),
                "vacuum_minimum_eigenvalue": float(vacuum_values[0]),
            }
        )
    representative = next(
        row
        for row in completion_scan
        if row["incidence_mass"] == 4.0 and row["heavy_mass"] == 3.6
    )
    assert representative["origin_signature"] == [10, 0, 20]
    assert representative["vacuum_signature"] == [0, 0, 30]
    assert len({tuple(row["origin_signature"]) for row in completion_scan}) >= 3

    result = {
        "date": "2026-08-29",
        "gate": "version8_isotypic_relative_curvature_parent_hessian_gate",
        "old_tome7_slice": {
            "real_dimension": 27,
            "isotypic_vacuum_hessian_rank": int(
                np.linalg.matrix_rank(old_isotypic, tol=TOL)
            ),
            "nonnegative_weight_scan": old_weight_scan,
            "seven_mode_origin_signature_preserved_for_all_tested_weights": True,
            "strict_vacuum_stability_preserved_for_all_tested_weights": True,
        },
        "full_gauge_closed_transfer": {
            "complex_dimension": 15,
            "real_dimension": 30,
            "incidence_complex_dimension": 5,
            "incidence_real_dimension": 10,
            "heavy_complex_dimension": 10,
            "heavy_real_dimension": 20,
            "incidence_projector_rank": int(
                np.linalg.matrix_rank(incidence_projector, tol=TOL)
            ),
            "incidence_projector_gauge_commutator_residual": projector_covariance_residual,
            "relative_gram_origin_signature": signature(
                eigvalsh(full_physical_origin)
            ),
            "relative_gram_vacuum_signature": signature(
                eigvalsh(full_physical_vacuum)
            ),
            "isotypic_vacuum_hessian_rank": int(
                np.linalg.matrix_rank(full_isotypic, tol=TOL)
            ),
            "isotypic_hessian_on_two_dimensional_gram_kernel": rounded(
                isotypic_on_gram_kernel
            ),
            "isotypic_term_lifts_gram_vacuum_kernel": False,
        },
        "gauge_invariant_incidence_heavy_completion": {
            "origin_formula": "-m_I P_I + m_H(1-P_I) + 0.5 H_Gram_origin",
            "vacuum_formula": "2m_I P_I + m_H(1-P_I) + 0.5 H_Gram_vacuum + H_B",
            "scan": completion_scan,
            "representative_masses": {"incidence": 4.0, "heavy": 3.6},
            "representative_origin_signature": representative["origin_signature"],
            "representative_vacuum_signature": representative["vacuum_signature"],
            "representative_vacuum_gap": representative[
                "vacuum_minimum_eigenvalue"
            ],
            "qualitative_full_transfer_transition_exists": True,
            "mass_weights_are_uniquely_derived": False,
            "origin_signature_depends_on_mass_completion": True,
        },
        "complex_structure_constraint": {
            "incidence_projector_commutes_with_complex_structure": True,
            "incidence_launch_real_multiplicity": 10,
            "complex_hermitian_morse_indices_are_even": True,
            "exact_seven_real_mode_index_survives_full_complex_closure": False,
        },
        "verdict": {
            "smooth_isotypic_term_is_compatible_with_tome7_transition": True,
            "smooth_isotypic_term_closes_full_parent_alone": False,
            "minimal_gauge_closed_incidence_launch_has_ten_real_modes": True,
            "a_qualitative_10_to_20_full_transfer_transition_exists": True,
            "unique_gauge_closed_edge_hodge_mass_metric_obtained": False,
            "full_parent_action_obtained": False,
            "next_gate": "version8_gauge_closed_edge_hodge_origin_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()