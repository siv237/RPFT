#!/usr/bin/env python3
"""Test whether the 27D gauge-closed noise module has one inherited parent Hessian."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh, expm


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_gauge_closed_noise_parent_hessian_gate_results.json"
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
from s2t_v8_noise_isotropy_symmetry_admission_gate import (  # noqa: E402
    lie_orbit_closure,
    orthonormal_map_span,
)


def real_vector(matrix: np.ndarray) -> np.ndarray:
    return np.concatenate([matrix.real.reshape(-1), matrix.imag.reshape(-1)])


def orthonormal_real_span(matrices: list[np.ndarray]) -> np.ndarray:
    columns = np.stack([real_vector(matrix) for matrix in matrices], axis=1)
    left, values, _ = np.linalg.svd(columns, full_matrices=False)
    rank = int(np.sum(values > 1.0e-10 * values[0]))
    return left[:, :rank]


def rounded(values) -> list[float]:
    return [float(f"{value:.12g}") for value in values]


def main() -> None:
    background, variations, labels, down_cut = physical_blocks()
    gauge_labels, gauge_sources, gauge_targets = gauge_components()
    assert background.shape == (10, 11)
    assert len(variations) == 27
    assert len(gauge_labels) == len(gauge_sources) == len(gauge_targets) == 12

    heavy_span = orthonormal_map_span(variations[7:])
    incidence_orbit, incidence_sequence = lie_orbit_closure(
        [background], gauge_sources, gauge_targets
    )
    gauge_closed_transfer = orthonormal_map_span(incidence_orbit + heavy_span)
    assert len(heavy_span) == 10
    assert incidence_sequence == [1, 4, 5, 5]
    assert len(gauge_closed_transfer) == 15

    classical_basis = orthonormal_real_span(variations)
    noise_real_directions = [
        direction
        for operator in gauge_closed_transfer
        for direction in (operator, 1j * operator)
    ]
    noise_basis = orthonormal_real_span(noise_real_directions)
    assert classical_basis.shape[1] == 27
    assert noise_basis.shape[1] == 30

    principal_values = np.linalg.svd(
        classical_basis.T @ noise_basis, compute_uv=False
    )
    intersection_dimension = int(np.sum(np.abs(principal_values - 1.0) < TOL))
    coupled_rank = int(np.sum(principal_values > TOL))
    union_dimension = classical_basis.shape[1] + noise_basis.shape[1] - intersection_dimension
    classical_only_dimension = classical_basis.shape[1] - intersection_dimension
    noise_only_dimension = noise_basis.shape[1] - intersection_dimension
    assert intersection_dimension == coupled_rank == 23
    assert union_dimension == 34
    assert classical_only_dimension == 4
    assert noise_only_dimension == 7

    root_projection_residuals = []
    for index, variation in enumerate(variations[:7]):
        vector = real_vector(variation)
        residual = vector - noise_basis @ (noise_basis.T @ vector)
        root_projection_residuals.append(
            {
                "root_index": index,
                "relative_residual_outside_noise_transfer_space": float(
                    np.linalg.norm(residual) / np.linalg.norm(vector)
                ),
            }
        )

    rng = np.random.default_rng(20260829)
    gauge_leakage_rows = []
    for sample in range(12):
        coefficients = rng.normal(scale=0.7, size=12)
        source_generator = sum(
            (coefficients[i] * gauge_sources[i] for i in range(12)),
            np.zeros_like(gauge_sources[0]),
        )
        target_generator = sum(
            (coefficients[i] * gauge_targets[i] for i in range(12)),
            np.zeros_like(gauge_targets[0]),
        )
        source_unitary = expm(1j * source_generator)
        target_unitary = expm(1j * target_generator)
        maximum = 0.0
        for variation in variations:
            transformed = target_unitary @ variation @ source_unitary.conj().T
            vector = real_vector(transformed)
            residual = vector - classical_basis @ (classical_basis.T @ vector)
            maximum = max(maximum, float(np.linalg.norm(residual)))
        gauge_leakage_rows.append({"sample": sample, "maximum_residual": maximum})
    maximum_classical_slice_leakage = max(
        row["maximum_residual"] for row in gauge_leakage_rows
    )
    assert maximum_classical_slice_leakage > 1.0

    physical_origin, physical_vacuum = physical_hessians(
        background, noise_real_directions
    )
    physical_origin_values = eigvalsh(physical_origin)
    physical_vacuum_values = eigvalsh(physical_vacuum)
    assert signature(physical_origin_values) == [30, 0, 0]
    assert signature(physical_vacuum_values) == [0, 2, 28]

    old_physical_origin, old_physical_vacuum = physical_hessians(
        background, variations
    )
    old_edge_origin, old_edge_vacuum = edge_hessians(down_cut, len(variations))
    old_origin = old_edge_origin + 0.5 * old_physical_origin
    old_vacuum = old_edge_vacuum + 0.5 * old_physical_vacuum
    old_origin_values = eigvalsh(old_origin)
    old_vacuum_values = eigvalsh(old_vacuum)
    assert signature(old_origin_values) == [7, 0, 20]
    assert signature(old_vacuum_values) == [0, 0, 27]

    # The physical relative-Gram term extends to all transfer maps, but the
    # edge selector does not: it was defined on the old 27-real-dimensional
    # slice, which is neither equal to nor contained in the 30D realification
    # of the gauge-closed transfer noise module.  A scalar completion therefore
    # illustrates genuine, not merely coordinate, freedom.
    completion_scan = []
    for mass in (0.0, 0.1, 1.0, 3.0, 4.0, 5.0, 10.0, 100.0):
        origin = 0.5 * physical_origin + mass * np.eye(30)
        vacuum = 0.5 * physical_vacuum + mass * np.eye(30)
        origin_values = eigvalsh(origin)
        vacuum_values = eigvalsh(vacuum)
        completion_scan.append(
            {
                "undetermined_scalar_transfer_mass": mass,
                "origin_signature": signature(origin_values),
                "vacuum_signature": signature(vacuum_values),
                "origin_minimum_eigenvalue": float(origin_values[0]),
                "origin_maximum_eigenvalue": float(origin_values[-1]),
                "vacuum_minimum_eigenvalue": float(vacuum_values[0]),
            }
        )
    assert len({tuple(row["origin_signature"]) for row in completion_scan}) >= 4
    assert completion_scan[0]["vacuum_signature"] == [0, 2, 28]
    assert all(
        row["vacuum_signature"] == [0, 0, 30]
        for row in completion_scan[1:]
    )

    freeze = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v7_qualitative_parent_mass_metric_freeze_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    gauge_anchor = json.loads(
        (
            ROOT / "s2t/results/s2t_v7_common_gauge_f0_anchor_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    prior = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v8_noise_isotropy_symmetry_admission_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert prior["verdict"]["minimal_gauge_closed_noise_dimension"] == 27
    assert not freeze["frozen_boundaries"]["full_spacetime_gauge_closure_obtained"]
    assert not freeze["frozen_boundaries"]["unique_parent_action_derived"]
    assert not gauge_anchor["verdict"]["common_physical_gauge_anchor_admitted"]

    result = {
        "date": "2026-08-29",
        "gate": "version8_gauge_closed_noise_parent_hessian_gate",
        "space_type_audit": {
            "classical_tome7_field_slice_real_dimension": 27,
            "gauge_closed_transfer_noise_complex_dimension": 15,
            "gauge_closed_transfer_noise_realification_dimension": 30,
            "intersection_real_dimension": intersection_dimension,
            "union_real_dimension": union_dimension,
            "classical_only_real_dimension": classical_only_dimension,
            "noise_only_real_dimension": noise_only_dimension,
            "principal_singular_values": rounded(principal_values),
            "root_projection_residuals": root_projection_residuals,
            "spaces_are_equal": False,
            "either_space_contains_the_other": False,
        },
        "classical_slice_gauge_closure": {
            "finite_gauge_samples": gauge_leakage_rows,
            "maximum_residual": maximum_classical_slice_leakage,
            "old_27D_field_slice_is_full_gauge_invariant": False,
        },
        "inherited_parent_hessian": {
            "old_field_origin_signature": signature(old_origin_values),
            "old_field_vacuum_signature": signature(old_vacuum_values),
            "old_field_vacuum_minimum_eigenvalue": float(old_vacuum_values[0]),
            "relative_gram_term_on_30D_noise_origin_signature": signature(
                physical_origin_values
            ),
            "relative_gram_term_on_30D_noise_vacuum_signature": signature(
                physical_vacuum_values
            ),
            "relative_gram_term_vacuum_kernel_dimension": 2,
            "edge_selector_has_canonical_extension_to_noise_space": False,
            "reason": "the edge selector is specified on a non-gauge-closed 27D real field slice, not on the 30D realified transfer-noise module",
        },
        "completion_nonuniqueness": {
            "probe": "H_transfer(lambda)=0.5 H_relative_Gram + lambda I_30",
            "scan": completion_scan,
            "qualitative_origin_signature_depends_on_completion": True,
            "old_seven_mode_selector_recovered_without_new_input": False,
        },
        "gauge_noise_parent_coverage": {
            "gauge_noise_dimension": 12,
            "gauge_noise_role": "endpoint Lie-algebra Lindblad operators on observables",
            "tome7_parent_field_role": "finite transfer map A:C11->C10",
            "common_field_space_identification_exists": False,
            "full_spacetime_gauge_kinetic_trace_obtained": False,
            "common_physical_gauge_anchor_admitted": False,
            "a_27_by_27_parent_hessian_is_well_typed": False,
        },
        "verdict": {
            "old_tome7_hessian_remains_valid_on_old_field_slice": True,
            "gauge_closed_noise_module_inherits_unique_parent_hessian": False,
            "full_27D_noise_parent_hessian_obtained": False,
            "failure_is_instability": False,
            "failure_is_space_type_and_completion_nonuniqueness": True,
            "status": "parent_hessian_type_mismatch_and_gauge_closed_completion_no_go",
            "next_gate": "version8_gauge_closed_field_space_superconnection_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()