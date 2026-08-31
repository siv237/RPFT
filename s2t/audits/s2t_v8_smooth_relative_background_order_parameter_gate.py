#!/usr/bin/env python3
"""Test smooth gauge-equivariant replacements for the polar order parameter."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import expm


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_smooth_relative_background_order_parameter_gate_results.json"
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


def reconstruct(coefficients: np.ndarray, frame: list[np.ndarray]) -> np.ndarray:
    return sum(
        (coefficients[index] * frame[index] for index in range(len(frame))),
        np.zeros_like(frame[0]),
    )


def relative_curvature(field: np.ndarray, order: np.ndarray) -> np.ndarray:
    return (
        field @ field.conj().T @ order
        - order @ field.conj().T @ field
    )


def rounded(values) -> list[float]:
    return [float(f"{value:.12g}") for value in values]


def main() -> None:
    background, old_variations, _, _ = physical_blocks()
    _, gauge_sources, gauge_targets = gauge_components()
    heavy_span = orthonormal_map_span(old_variations[7:])
    incidence_orbit, incidence_sequence = lie_orbit_closure(
        [background], gauge_sources, gauge_targets
    )
    transfer_frame = orthonormal_map_span(incidence_orbit + heavy_span)
    transfer_rep, closure_residual, _ = transfer_infinitesimal_representation(
        gauge_sources, gauge_targets, transfer_frame
    )
    equivariant_endomorphism_dimension, commutant_tail = commutant_dimension(
        transfer_rep
    )

    assert background.shape == (10, 11)
    assert len(transfer_frame) == 15
    assert incidence_sequence == [1, 4, 5, 5]
    assert closure_residual < TOL
    assert equivariant_endomorphism_dimension == 13

    quark_source = np.diag([1.0] * 6 + [0.0] * 5)
    quark_target = np.diag([1.0] * 6 + [0.0] * 4)
    gamma_source = 2.0 * quark_source - np.eye(11)
    gamma_target = 2.0 * quark_target - np.eye(10)
    gamma_gauge_commutator = max(
        max(
            float(np.linalg.norm(gamma_source @ item - item @ gamma_source))
            for item in gauge_sources
        ),
        max(
            float(np.linalg.norm(gamma_target @ item - item @ gamma_target))
            for item in gauge_targets
        ),
    )
    assert gamma_gauge_commutator < TOL

    def smooth_order(field: np.ndarray) -> np.ndarray:
        return gamma_target @ field - field @ gamma_source

    order_matrix = np.column_stack(
        [coordinates(smooth_order(item), transfer_frame) for item in transfer_frame]
    )
    order_reconstruction_residual = max(
        float(
            np.linalg.norm(
                smooth_order(item)
                - reconstruct(order_matrix[:, index], transfer_frame)
            )
        )
        for index, item in enumerate(transfer_frame)
    )
    order_commutant_residual = max(
        float(np.linalg.norm(order_matrix @ item - item @ order_matrix))
        for item in transfer_rep
    )
    order_eigenvalues = np.linalg.eigvalsh(
        (order_matrix + order_matrix.conj().T) / 2.0
    )
    order_rank = int(np.linalg.matrix_rank(order_matrix, tol=TOL))
    assert order_reconstruction_residual < TOL
    assert order_commutant_residual < TOL
    assert order_rank == 6
    assert np.linalg.norm(smooth_order(background)) < TOL

    left_gram = background @ background.conj().T
    right_gram = background.conj().T @ background

    def vacuum_linearized_curvature(variation: np.ndarray) -> np.ndarray:
        order = smooth_order(variation)
        return left_gram @ order - order @ right_gram

    real_transfer_frame = transfer_frame + [1j * item for item in transfer_frame]
    vacuum_hessian = np.array(
        [
            [
                2.0
                * np.real(
                    np.vdot(
                        vacuum_linearized_curvature(left),
                        vacuum_linearized_curvature(right),
                    )
                )
                for right in real_transfer_frame
            ]
            for left in real_transfer_frame
        ]
    )
    vacuum_hessian_values = np.linalg.eigvalsh(
        (vacuum_hessian + vacuum_hessian.T) / 2.0
    )
    vacuum_hessian_rank = int(np.sum(vacuum_hessian_values > TOL))
    assert vacuum_hessian_rank == 12
    assert np.min(vacuum_hessian_values) > -TOL

    rng = np.random.default_rng(20260829)
    covariance_residuals = []
    relative_norms = []
    degree_six_residuals = []
    natural_functional_residuals = []
    for _ in range(12):
        coefficients = rng.normal(size=15) + 1j * rng.normal(size=15)
        field = reconstruct(coefficients, transfer_frame)
        order = smooth_order(field)
        curvature = relative_curvature(field, order)
        relative_norms.append(float(np.linalg.norm(curvature)))

        group_coefficients = rng.normal(scale=0.7, size=12)
        unitary_source = expm(
            1j
            * sum(
                (
                    group_coefficients[index] * gauge_sources[index]
                    for index in range(12)
                ),
                np.zeros_like(gauge_sources[0]),
            )
        )
        unitary_target = expm(
            1j
            * sum(
                (
                    group_coefficients[index] * gauge_targets[index]
                    for index in range(12)
                ),
                np.zeros_like(gauge_targets[0]),
            )
        )
        transformed = unitary_target @ field @ unitary_source.conj().T
        transformed_curvature = relative_curvature(
            transformed, smooth_order(transformed)
        )
        covariance_residuals.append(
            float(
                np.linalg.norm(
                    transformed_curvature
                    - unitary_target @ curvature @ unitary_source.conj().T
                )
            )
        )

        scale = 0.37
        scaled_curvature = relative_curvature(
            scale * field, smooth_order(scale * field)
        )
        degree_six_residuals.append(
            abs(
                float(np.linalg.norm(scaled_curvature) ** 2)
                - scale**6 * float(np.linalg.norm(curvature) ** 2)
            )
        )

        natural_orders = [
            field,
            field @ (field.conj().T @ field),
            field @ np.linalg.inv(np.eye(11) + field.conj().T @ field),
        ]
        natural_functional_residuals.append(
            max(
                float(np.linalg.norm(relative_curvature(field, item)))
                for item in natural_orders
            )
        )

    assert min(relative_norms) > 1.0
    assert max(covariance_residuals) < 1.0e-8
    assert max(degree_six_residuals) < TOL
    assert max(natural_functional_residuals) < 1.0e-8

    result = {
        "date": "2026-08-29",
        "gate": "version8_smooth_relative_background_order_parameter_gate",
        "transfer_module": {
            "complex_dimension": 15,
            "incidence_orbit_dimension_sequence": incidence_sequence,
            "equivariant_endomorphism_commutant_dimension": equivariant_endomorphism_dimension,
            "commutant_smallest_singular_values": rounded(commutant_tail),
        },
        "quark_lepton_grading": {
            "source_signature": [6, 5],
            "target_signature": [6, 4],
            "maximum_gauge_commutator_residual": gamma_gauge_commutator,
            "smooth_order_formula": "B(A)=Gamma_t A-A Gamma_s",
            "order_map_rank_complex": order_rank,
            "order_map_kernel_dimension_complex": 15 - order_rank,
            "order_map_eigenvalues": rounded(order_eigenvalues),
            "transfer_module_reconstruction_residual": order_reconstruction_residual,
            "equivariant_commutant_residual": order_commutant_residual,
            "background_order_norm": float(np.linalg.norm(smooth_order(background))),
        },
        "relative_curvature": {
            "formula": "R_B(A)=AA*B(A)-B(A)A*A",
            "random_sample_minimum_norm": min(relative_norms),
            "random_sample_maximum_norm": max(relative_norms),
            "maximum_full_gauge_covariance_residual": max(covariance_residuals),
            "maximum_radial_degree_six_action_residual": max(degree_six_residuals),
            "natural_full_unitary_functional_calculus_maximum_curvature_residual": max(
                natural_functional_residuals
            ),
            "origin_action_degree": 6,
            "origin_gradient_is_zero": True,
            "origin_hessian_is_zero": True,
            "background_action_is_zero": True,
        },
        "vacuum_hessian_on_full_transfer_realification": {
            "real_dimension": 30,
            "rank": vacuum_hessian_rank,
            "nullity": 30 - vacuum_hessian_rank,
            "minimum_eigenvalue": float(vacuum_hessian_values[0]),
            "minimum_positive_eigenvalue": float(
                vacuum_hessian_values[vacuum_hessian_values > TOL][0]
            ),
            "maximum_eigenvalue": float(vacuum_hessian_values[-1]),
            "eigenvalues": rounded(vacuum_hessian_values),
            "is_positive_semidefinite": True,
        },
        "verdict": {
            "smooth_full_gauge_covariant_relative_order_exists": True,
            "polar_discontinuity_is_the_only_possible_route": False,
            "candidate_is_unique_from_gauge_covariance": False,
            "candidate_reproduces_polar_background": False,
            "candidate_drives_origin_rank_transition": False,
            "candidate_can_add_vacuum_stiffness": True,
            "full_parent_action_obtained": False,
            "next_gate": "version8_isotypic_relative_curvature_parent_hessian_gate",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()