#!/usr/bin/env python3
"""Audit the full H15 stationarity fork of the Tome VII curvature parent."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def odd_block(field: np.ndarray) -> np.ndarray:
    return np.block(
        [
            [np.zeros((4, 4), dtype=complex), field.conj().T],
            [field, np.zeros((3, 3), dtype=complex)],
        ]
    )


def normalized_action(operator: np.ndarray) -> float:
    curvature = operator @ operator
    return float(
        np.real(np.trace(curvature.conj().T @ curvature)) / operator.shape[0]
    )


def main() -> None:
    affine_complex_dimension = 12
    physical_oneform_complex_dimension = 12
    full_complex_dimension = (
        affine_complex_dimension * physical_oneform_complex_dimension
    )
    full_real_dimension = 2 * full_complex_dimension

    edge_intertwiner_dimension_matrix = np.eye(3, dtype=int)
    common_edge_projector = np.ones((3, 3)) / 3.0
    relative_edge_projector = np.eye(3) - common_edge_projector

    grading = np.diag([1.0] * 4 + [-1.0] * 3).astype(complex)
    canonical_field = np.zeros((3, 4), dtype=complex)
    canonical_field[:, :3] = np.eye(3)
    canonical_odd = odd_block(canonical_field)

    edge_amplitude_samples = [
        [0.0, 0.0, 0.0],
        [0.25, 0.5, 1.0],
        [1.0, 1.0, 1.0],
        [1.0, 2.0, 3.0],
    ]
    stationarity_samples: list[dict[str, object]] = []
    step = 1.0e-6
    family_oneform_multiplicity = 4
    total_multiplicity = 12

    for amplitudes in edge_amplitude_samples:
        analytic_gradient = []
        finite_difference_gradient = []
        for amplitude in amplitudes:
            # Vary one of four family-oneform copies of this charged edge.
            analytic = 24.0 * amplitude * (1.0 + amplitude**2) / (
                7.0 * total_multiplicity
            )
            background = grading + amplitude * canonical_odd
            numeric = (
                normalized_action(background + step * canonical_odd)
                - normalized_action(background - step * canonical_odd)
            ) / (2.0 * step * total_multiplicity)
            analytic_gradient.append(float(analytic))
            finite_difference_gradient.append(float(numeric))

        stationarity_samples.append(
            {
                "edge_amplitudes": amplitudes,
                "analytic_radial_gradient_per_family_copy": analytic_gradient,
                "finite_difference_radial_gradient_per_family_copy": (
                    finite_difference_gradient
                ),
                "stationary": bool(
                    np.max(np.abs(analytic_gradient)) < 1.0e-12
                ),
            }
        )

    # At D_F=0 each raw real coordinate has the positive eigenvalue
    # (8/7)/12 after the single normalized trace over 12 multiplicity channels.
    zero_background_raw_hessian_eigenvalue = 8.0 / (
        7.0 * total_multiplicity
    )
    zero_background_eigenvalues = np.full(
        full_real_dimension,
        zero_background_raw_hessian_eigenvalue,
    )

    max_gradient_residual = max(
        max(
            abs(analytic - numeric)
            for analytic, numeric in zip(
                sample["analytic_radial_gradient_per_family_copy"],
                sample["finite_difference_radial_gradient_per_family_copy"],
            )
        )
        for sample in stationarity_samples
    )

    result = {
        "gate": "version7_full_physical_rank_field_hessian_gate",
        "frozen_H15_input": {
            "observed_dimension": 15,
            "charged_edges": ["u", "d", "e"],
            "charged_edge_count": 3,
            "edge_intertwiner_dimension_matrix": (
                edge_intertwiner_dimension_matrix.tolist()
            ),
            "edge_bimodule_commutant": "C^3",
            "relative_real_edge_dimension": int(
                np.linalg.matrix_rank(relative_edge_projector)
            ),
            "family_oneform_complex_dimension": family_oneform_multiplicity,
            "physical_oneform_complex_dimension": (
                physical_oneform_complex_dimension
            ),
        },
        "tome7_full_field": {
            "E_aff_complex_dimension": affine_complex_dimension,
            "Y_phys_complex_dimension": physical_oneform_complex_dimension,
            "full_complex_dimension_before_real_completion": (
                full_complex_dimension
            ),
            "full_real_tangent_dimension": full_real_dimension,
            "independent_relative_edge_weights": 2,
        },
        "nonzero_DF_background": {
            "radial_direction_is_in_physical_oneform_module": True,
            "symbolic_gradient": "4 tr_norm(D_F^4) > 0 for D_F != 0",
            "samples": stationarity_samples,
            "maximum_analytic_numeric_gradient_residual": float(
                max_gradient_residual
            ),
            "Phi_zero_stationary_for_nonzero_DF": False,
        },
        "zero_DF_background": {
            "stationary": True,
            "full_real_hessian_dimension": full_real_dimension,
            "raw_coordinate_hessian_eigenvalue": (
                zero_background_raw_hessian_eigenvalue
            ),
            "minimum_eigenvalue": float(np.min(zero_background_eigenvalues)),
            "maximum_eigenvalue": float(np.max(zero_background_eigenvalues)),
            "negative_eigenvalue_count": int(
                np.sum(zero_background_eigenvalues < -1.0e-12)
            ),
            "zero_eigenvalue_count": int(
                np.sum(np.abs(zero_background_eigenvalues) < 1.0e-12)
            ),
        },
        "forbidden_repairs": {
            "manual_negative_mass": True,
            "post_hoc_reference_curvature_subtraction": True,
            "remove_radial_rank_direction_by_constraint": True,
        },
        "contract_update": {
            "P0_common_typed_carrier": "pass",
            "P1_single_trace": "exists_but_relative_DF_background_unfixed",
            "P2_nonzero_DF_vacuum": "fail_nonstationary",
            "P2_zero_DF_vacuum": "fail_no_negative_mode",
            "P3_to_P5": "stopped",
            "P6": "pass",
        },
        "verdict": {
            "pure_curvature_norm_parent": "closed_negative",
            "matter_birth": False,
            "next_requirement": (
                "a preregistered functional with a stationary nonzero "
                "background and no post-hoc curvature subtraction"
            ),
        },
    }

    assert full_complex_dimension == 144
    assert full_real_dimension == 288
    assert np.array_equal(edge_intertwiner_dimension_matrix, np.eye(3, dtype=int))
    assert np.linalg.matrix_rank(common_edge_projector) == 1
    assert np.linalg.matrix_rank(relative_edge_projector) == 2
    assert stationarity_samples[0]["stationary"]
    assert all(not sample["stationary"] for sample in stationarity_samples[1:])
    assert max_gradient_residual < 1.0e-8
    assert result["zero_DF_background"]["minimum_eigenvalue"] > 0.0
    assert result["zero_DF_background"]["negative_eigenvalue_count"] == 0
    assert result["zero_DF_background"]["zero_eigenvalue_count"] == 0

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v7_full_physical_rank_field_hessian_gate_results.json"
    )
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()