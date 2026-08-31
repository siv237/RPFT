#!/usr/bin/env python3
"""Assemble the gauge-closed field-space superconnection candidate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import expm


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_gauge_closed_field_space_superconnection_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (  # noqa: E402
    physical_blocks,
)
from s2t_v7_incidence_transfer_markov_weight_gate import (  # noqa: E402
    polar_coisometry,
)
from s2t_v8_canonical_noise_frame_common_trace_gate import (  # noqa: E402
    gauge_components,
    whiten_gauge,
)
from s2t_v8_kms_nontracial_relative_rate_selector_gate import (  # noqa: E402
    central_density,
)
from s2t_v8_noise_isotropy_symmetry_admission_gate import (  # noqa: E402
    lie_orbit_closure,
    orthonormal_map_span,
)


def gauge_gram(
    sources: list[np.ndarray],
    targets: list[np.ndarray],
    source_density: float,
    target_density: float,
) -> np.ndarray:
    return np.array(
        [
            [
                source_density * np.trace(left_s.conj().T @ right_s)
                + target_density * np.trace(left_t.conj().T @ right_t)
                for right_s, right_t in zip(sources, targets)
            ]
            for left_s, left_t in zip(sources, targets)
        ]
    )


def transfer_infinitesimal_representation(
    actors_source: list[np.ndarray],
    actors_target: list[np.ndarray],
    frame: list[np.ndarray],
) -> tuple[list[np.ndarray], float, float]:
    representations = []
    closure_residual = 0.0
    antihermiticity_residual = 0.0
    for source, target in zip(actors_source, actors_target):
        matrix = np.zeros((len(frame), len(frame)), complex)
        for column, operator in enumerate(frame):
            transformed = 1j * (target @ operator - operator @ source)
            coefficients = np.array(
                [np.trace(item.conj().T @ transformed) for item in frame]
            )
            matrix[:, column] = coefficients
            reconstructed = sum(
                (coefficients[i] * frame[i] for i in range(len(frame))),
                np.zeros_like(operator),
            )
            closure_residual = max(
                closure_residual,
                float(np.linalg.norm(transformed - reconstructed)),
            )
        antihermiticity_residual = max(
            antihermiticity_residual,
            float(np.linalg.norm(matrix + matrix.conj().T)),
        )
        representations.append(matrix)
    return representations, closure_residual, antihermiticity_residual


def adjoint_infinitesimal_representation(
    actors_source: list[np.ndarray],
    actors_target: list[np.ndarray],
    frame_source: list[np.ndarray],
    frame_target: list[np.ndarray],
    source_density: float,
    target_density: float,
) -> tuple[list[np.ndarray], float, float, float]:
    representations = []
    closure_residual = 0.0
    antihermiticity_residual = 0.0
    imaginary_coefficient_residual = 0.0
    for actor_source, actor_target in zip(actors_source, actors_target):
        matrix = np.zeros((len(frame_source), len(frame_source)), complex)
        for column, (source, target) in enumerate(
            zip(frame_source, frame_target)
        ):
            transformed_source = 1j * (
                actor_source @ source - source @ actor_source
            )
            transformed_target = 1j * (
                actor_target @ target - target @ actor_target
            )
            coefficients = np.array(
                [
                    source_density
                    * np.trace(item_s.conj().T @ transformed_source)
                    + target_density
                    * np.trace(item_t.conj().T @ transformed_target)
                    for item_s, item_t in zip(frame_source, frame_target)
                ]
            )
            matrix[:, column] = coefficients
            reconstructed_source = sum(
                (
                    coefficients[i] * frame_source[i]
                    for i in range(len(frame_source))
                ),
                np.zeros_like(source),
            )
            reconstructed_target = sum(
                (
                    coefficients[i] * frame_target[i]
                    for i in range(len(frame_target))
                ),
                np.zeros_like(target),
            )
            closure_residual = max(
                closure_residual,
                float(np.linalg.norm(transformed_source - reconstructed_source)),
                float(np.linalg.norm(transformed_target - reconstructed_target)),
            )
        antihermiticity_residual = max(
            antihermiticity_residual,
            float(np.linalg.norm(matrix + matrix.conj().T)),
        )
        imaginary_coefficient_residual = max(
            imaginary_coefficient_residual,
            float(np.max(np.abs(matrix.imag))),
        )
        representations.append(matrix)
    return (
        representations,
        closure_residual,
        antihermiticity_residual,
        imaginary_coefficient_residual,
    )


def partial_polar(matrix: np.ndarray, tolerance: float = 1.0e-12) -> np.ndarray:
    left, values, right = np.linalg.svd(matrix, full_matrices=False)
    if values.size == 0 or values[0] == 0.0:
        return np.zeros_like(matrix)
    rank = int(np.sum(values > tolerance * values[0]))
    if rank == 0:
        return np.zeros_like(matrix)
    return left[:, :rank] @ right[:rank, :]


def relative_curvature(field: np.ndarray, polar: np.ndarray) -> np.ndarray:
    return field @ field.conj().T @ polar - polar @ field.conj().T @ field


def rounded(values) -> list[float]:
    return [float(f"{value:.12g}") for value in values]


def main() -> None:
    background, variations, _, _ = physical_blocks()
    labels, raw_sources, raw_targets = gauge_components()
    ratio = float(np.exp(-2.0))
    source_density, target_density = central_density(ratio)
    white_sources, white_targets = whiten_gauge(
        raw_sources,
        raw_targets,
        gauge_gram(
            raw_sources,
            raw_targets,
            source_density,
            target_density,
        ),
    )

    heavy_span = orthonormal_map_span(variations[7:])
    incidence_orbit, incidence_sequence = lie_orbit_closure(
        [background], raw_sources, raw_targets
    )
    transfer_frame = orthonormal_map_span(incidence_orbit + heavy_span)
    assert len(transfer_frame) == 15
    assert len(white_sources) == len(white_targets) == 12
    assert incidence_sequence == [1, 4, 5, 5]

    transfer_rep, transfer_closure, transfer_antihermitian = (
        transfer_infinitesimal_representation(
            raw_sources, raw_targets, transfer_frame
        )
    )
    (
        gauge_rep,
        gauge_closure,
        gauge_antihermitian,
        gauge_reality,
    ) = adjoint_infinitesimal_representation(
        raw_sources,
        raw_targets,
        white_sources,
        white_targets,
        source_density,
        target_density,
    )
    assert transfer_closure < TOL
    assert transfer_antihermitian < TOL
    assert gauge_closure < TOL
    assert gauge_antihermitian < TOL
    assert gauge_reality < TOL

    polar, _, defect = polar_coisometry(background)
    defect_dimension = int(np.linalg.matrix_rank(defect, tol=TOL))
    assert defect_dimension == 1
    assert np.linalg.norm(polar @ polar.conj().T - np.eye(10)) < TOL

    rng = np.random.default_rng(20260829)
    covariance_rows = []
    fixed_polar_defects = []
    moving_polar_residuals = []
    polar_equivariance_residuals = []
    for sample in range(12):
        field_coefficients = rng.normal(size=15) + 1j * rng.normal(size=15)
        field = sum(
            (field_coefficients[i] * transfer_frame[i] for i in range(15)),
            np.zeros_like(transfer_frame[0]),
        )
        connection_coefficients = rng.normal(scale=0.4, size=(3, 12))
        connections_source = [
            sum(
                (
                    connection_coefficients[mu, i] * raw_sources[i]
                    for i in range(12)
                ),
                np.zeros_like(raw_sources[0]),
            )
            for mu in range(3)
        ]
        connections_target = [
            sum(
                (
                    connection_coefficients[mu, i] * raw_targets[i]
                    for i in range(12)
                ),
                np.zeros_like(raw_targets[0]),
            )
            for mu in range(3)
        ]
        group_coefficients = rng.normal(scale=0.7, size=12)
        unitary_source = expm(
            1j
            * sum(
                (group_coefficients[i] * raw_sources[i] for i in range(12)),
                np.zeros_like(raw_sources[0]),
            )
        )
        unitary_target = expm(
            1j
            * sum(
                (group_coefficients[i] * raw_targets[i] for i in range(12)),
                np.zeros_like(raw_targets[0]),
            )
        )
        transformed_field = unitary_target @ field @ unitary_source.conj().T
        transformed_sources = [
            unitary_source @ item @ unitary_source.conj().T
            for item in connections_source
        ]
        transformed_targets = [
            unitary_target @ item @ unitary_target.conj().T
            for item in connections_target
        ]

        derivative_residual = 0.0
        for mu in range(3):
            derivative = (
                connections_target[mu] @ field
                - field @ connections_source[mu]
            )
            transformed_derivative = (
                transformed_targets[mu] @ transformed_field
                - transformed_field @ transformed_sources[mu]
            )
            derivative_residual = max(
                derivative_residual,
                float(
                    np.linalg.norm(
                        transformed_derivative
                        - unitary_target @ derivative @ unitary_source.conj().T
                    )
                ),
            )

        source_curvature = 1j * (
            connections_source[0] @ connections_source[1]
            - connections_source[1] @ connections_source[0]
        )
        target_curvature = 1j * (
            connections_target[0] @ connections_target[1]
            - connections_target[1] @ connections_target[0]
        )
        transformed_source_curvature = 1j * (
            transformed_sources[0] @ transformed_sources[1]
            - transformed_sources[1] @ transformed_sources[0]
        )
        transformed_target_curvature = 1j * (
            transformed_targets[0] @ transformed_targets[1]
            - transformed_targets[1] @ transformed_targets[0]
        )
        gauge_curvature_residual = max(
            float(
                np.linalg.norm(
                    transformed_source_curvature
                    - unitary_source
                    @ source_curvature
                    @ unitary_source.conj().T
                )
            ),
            float(
                np.linalg.norm(
                    transformed_target_curvature
                    - unitary_target
                    @ target_curvature
                    @ unitary_target.conj().T
                )
            ),
        )
        gram_residual = max(
            float(
                np.linalg.norm(
                    transformed_field.conj().T @ transformed_field
                    - unitary_source
                    @ (field.conj().T @ field)
                    @ unitary_source.conj().T
                )
            ),
            float(
                np.linalg.norm(
                    transformed_field @ transformed_field.conj().T
                    - unitary_target
                    @ (field @ field.conj().T)
                    @ unitary_target.conj().T
                )
            ),
        )
        covariance_rows.append(
            {
                "sample": sample,
                "induced_connection_residual": derivative_residual,
                "endpoint_curvature_residual": gauge_curvature_residual,
                "gram_curvature_residual": gram_residual,
            }
        )

        base_relative = relative_curvature(field, polar)
        fixed_relative = relative_curvature(transformed_field, polar)
        expected_relative = (
            unitary_target @ base_relative @ unitary_source.conj().T
        )
        fixed_polar_defects.append(
            float(np.linalg.norm(fixed_relative - expected_relative))
        )

        transformed_polar = unitary_target @ polar @ unitary_source.conj().T
        moving_relative = relative_curvature(
            transformed_field, transformed_polar
        )
        moving_polar_residuals.append(
            float(np.linalg.norm(moving_relative - expected_relative))
        )

        transformed_background = (
            unitary_target @ background @ unitary_source.conj().T
        )
        polar_from_transformed_background = partial_polar(transformed_background)
        polar_equivariance_residuals.append(
            float(
                np.linalg.norm(
                    polar_from_transformed_background - transformed_polar
                )
            )
        )

    assert max(
        max(
            row["induced_connection_residual"],
            row["endpoint_curvature_residual"],
            row["gram_curvature_residual"],
        )
        for row in covariance_rows
    ) < TOL
    assert min(fixed_polar_defects) > 1.0
    assert max(moving_polar_residuals) < TOL
    assert max(polar_equivariance_residuals) < TOL

    radial_polar_rows = []
    for scale in (1.0, 1.0e-1, 1.0e-3, 1.0e-6, 0.0):
        radial = partial_polar(scale * background)
        radial_polar_rows.append(
            {
                "scale": scale,
                "rank": int(np.linalg.matrix_rank(scale * background)),
                "polar_norm": float(np.linalg.norm(radial)),
                "distance_from_nonzero_polar": float(np.linalg.norm(radial - polar)),
            }
        )
    assert max(
        row["distance_from_nonzero_polar"] for row in radial_polar_rows[:-1]
    ) < TOL
    assert abs(radial_polar_rows[-1]["distance_from_nonzero_polar"] - np.sqrt(10.0)) < TOL

    field_metric = np.eye(27)
    total_representations = [
        np.block(
            [
                [transfer_rep[i], np.zeros((15, 12), complex)],
                [np.zeros((12, 15), complex), gauge_rep[i]],
            ]
        )
        for i in range(12)
    ]
    total_antihermiticity = max(
        float(np.linalg.norm(matrix.conj().T @ field_metric + field_metric @ matrix))
        for matrix in total_representations
    )
    assert total_antihermiticity < TOL

    previous = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v8_gauge_closed_noise_parent_hessian_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    field_precedent = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v7_edge_coherence_field_space_superconnection_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    full_square = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v7_real_linking_superconnection_assembly_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert not previous["verdict"]["full_27D_noise_parent_hessian_obtained"]
    assert field_precedent["verdict"]["new_independent_gauge_field_required"] is False
    assert full_square["verdict"]["ordinary_full_selfadjoint_curvature_is_parent"] is False

    result = {
        "date": "2026-08-29",
        "gate": "version8_gauge_closed_field_space_superconnection_gate",
        "field_space": {
            "endpoint_source_rank": 11,
            "endpoint_target_rank": 10,
            "physical_gauge_algebra_dimension": 12,
            "transfer_complex_dimension": 15,
            "transfer_real_dimension": 30,
            "gauge_connection_real_dimension_per_spacetime_one_form": 12,
            "finite_internal_field_real_dimension": 42,
            "new_gauge_generators_added": 0,
            "new_endpoint_fermion_states_added": 0,
            "incidence_orbit_dimension_sequence": incidence_sequence,
        },
        "infinitesimal_covariance": {
            "transfer_representation_closure_residual": transfer_closure,
            "transfer_representation_antihermiticity_residual": transfer_antihermitian,
            "gauge_adjoint_closure_residual": gauge_closure,
            "gauge_adjoint_antihermiticity_residual": gauge_antihermitian,
            "gauge_adjoint_real_coefficient_residual": gauge_reality,
            "total_field_representation_antihermiticity_residual": total_antihermiticity,
            "transfer_generator_ranks": [
                int(np.linalg.matrix_rank(item, tol=TOL)) for item in transfer_rep
            ],
            "gauge_adjoint_generator_ranks": [
                int(np.linalg.matrix_rank(item, tol=TOL)) for item in gauge_rep
            ],
        },
        "superconnection_curvature_covariance": {
            "formula": "A_super=diag(nabla_s,nabla_t)+offdiag(A,A*)",
            "finite_samples": covariance_rows,
            "maximum_induced_connection_residual": max(
                row["induced_connection_residual"] for row in covariance_rows
            ),
            "maximum_endpoint_curvature_residual": max(
                row["endpoint_curvature_residual"] for row in covariance_rows
            ),
            "maximum_gram_curvature_residual": max(
                row["gram_curvature_residual"] for row in covariance_rows
            ),
            "standard_curvature_contains_gauge_kinetic_transfer_kinetic_and_gram_blocks": True,
            "standard_curvature_alone_contains_derived_edge_hodge_selector": False,
        },
        "polar_relative_curvature_fork": {
            "polar_is_coisometry": True,
            "polar_cokernel_dimension": defect_dimension,
            "fixed_polar_minimum_full_gauge_covariance_defect": min(fixed_polar_defects),
            "fixed_polar_maximum_full_gauge_covariance_defect": max(fixed_polar_defects),
            "moving_polar_maximum_covariance_residual": max(moving_polar_residuals),
            "polar_equivariance_from_transformed_background_residual": max(
                polar_equivariance_residuals
            ),
            "fixed_polar_is_only_stabilizer_covariant": True,
            "moving_polar_is_full_gauge_covariant": True,
            "moving_polar_is_independent_new_field": False,
            "moving_polar_is_derived_from_background_on_constant_rank_stratum": True,
            "radial_rank_drop_scan": radial_polar_rows,
            "polar_jump_at_zero": float(np.sqrt(10.0)),
            "derived_polar_is_continuous_through_zero": False,
        },
        "parent_action_boundary": {
            "gauge_closed_field_bundle_kinematically_assembled": True,
            "one_standard_superconnection_curvature_available": True,
            "ordinary_full_square_is_valid_selector": False,
            "edge_hodge_selector_derived_on_full_field_bundle": False,
            "smooth_full_gauge_relative_curvature_through_origin": False,
            "full_BV_gauge_fixed_hessian_ready": False,
        },
        "verdict": {
            "field_space_type_mismatch_repaired": True,
            "full_parent_action_obtained": False,
            "positive_result": "15 complex transfer fields and 12 real gauge connections form one closed associated field bundle with covariant standard curvature",
            "remaining_obstruction": "the polar relative curvature is either fixed and only stabilizer-covariant or moving and discontinuous at the rank-zero origin; the edge-Hodge selector is not a standard full-curvature block",
            "status": "gauge_closed_field_space_pass_smooth_relative_parent_no_go",
            "next_gate": "version8_smooth_relative_background_order_parameter_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()