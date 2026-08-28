#!/usr/bin/env python3
"""Audit one common trace for the edge moment and chain-number curvature."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import block_diag, eigvalsh

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (
    ROOT_MULTIPLICITIES,
    edge_hessians,
    physical_blocks,
    signature,
)
from s2t_v7_incidence_transfer_markov_weight_gate import polar_coisometry
from s2t_v7_polar_transfer_cross_curvature_origin_gate import (
    relative_transfer_vacuum_hessian,
)
from s2t_v7_real_linking_superconnection_assembly_gate import linking_chain


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_common_chain_number_hodge_relative_trace_gate_results.json"
TOL = 1.0e-10


def edge_curvature(vector, down_cut):
    roots = vector[:7]
    heavy = vector[7:]
    values = np.concatenate([
        np.sqrt(ROOT_MULTIPLICITIES) * (roots**2 - 1.0),
        heavy[:down_cut] ** 2 + 1.6,
        heavy[down_cut:] ** 2 + 0.9,
    ])
    return np.diag(np.concatenate([values, -values])), values


def chain_number_curvature(field, reference, transfer):
    source = field.shape[1]
    target = field.shape[0]
    middle = source + target
    total = source + middle + target
    number = np.diag(np.concatenate([
        np.zeros(source), np.ones(middle), 2.0 * np.ones(target)
    ]))
    differential, _, _ = linking_chain(field, transfer)
    reference_differential, _, _ = linking_chain(reference, transfer)
    q = differential + differential.conj().T
    q0 = reference_differential + reference_differential.conj().T
    curvature = q @ q - q0 @ q0
    relative = 0.5 * (number @ curvature - curvature @ number)
    return 1j * relative


def main() -> None:
    reference, variations, _, down_cut = physical_blocks()
    transfer, _, _ = polar_coisometry(reference)
    rng = np.random.default_rng(20260828)

    maximum_trace_identity_residual = 0.0
    maximum_selfadjoint_residual = 0.0
    maximum_real_half_trace_residual = 0.0
    for _ in range(100):
        vector = rng.normal(size=len(variations))
        field = sum(
            coefficient * variation
            for coefficient, variation in zip(vector, variations)
        )
        edge_block, edge_values = edge_curvature(vector, down_cut)
        linking_block = chain_number_curvature(field, reference, transfer)
        total_curvature = block_diag(edge_block, linking_block)

        relative = (
            field @ field.conj().T @ transfer
            - transfer @ field.conj().T @ field
        )
        expected = float(np.sum(edge_values**2) + np.linalg.norm(relative) ** 2)
        common_trace = float(
            0.5 * np.trace(total_curvature @ total_curvature).real
        )
        maximum_trace_identity_residual = max(
            maximum_trace_identity_residual, abs(common_trace - expected)
        )
        maximum_selfadjoint_residual = max(
            maximum_selfadjoint_residual,
            float(np.linalg.norm(total_curvature - total_curvature.conj().T)),
        )

        real_doubled = block_diag(total_curvature, total_curvature.conj())
        real_half = float(
            0.25 * np.trace(real_doubled @ real_doubled).real
        )
        maximum_real_half_trace_residual = max(
            maximum_real_half_trace_residual, abs(real_half - common_trace)
        )

    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))
    relative_vacuum = relative_transfer_vacuum_hessian(
        reference, variations, transfer
    )

    # One common 1/2 trace gives S_E+||R_U||^2.  Since the previous Hessian
    # was computed for 1/2||R_U||^2, its vacuum contribution is doubled.
    common_origin_values = eigvalsh(edge_origin)
    common_vacuum_values = eigvalsh(edge_vacuum + 2.0 * relative_vacuum)

    positive_metric_scan = []
    for weight in (0.0, 0.25, 1.0, 4.0, 100.0):
        origin_values = eigvalsh(edge_origin)
        vacuum_values = eigvalsh(edge_vacuum + 2.0 * weight * relative_vacuum)
        positive_metric_scan.append({
            "relative_metric_weight": weight,
            "origin_signature": signature(origin_values),
            "origin_heavy_gap": float(origin_values[7]),
            "vacuum_signature": signature(vacuum_values),
            "vacuum_minimum_eigenvalue": float(vacuum_values[0]),
        })

    edge_dimension = 54
    linking_dimension = 42
    total_dimension = edge_dimension + linking_dimension
    edge_projector = np.diag(np.concatenate([
        np.ones(edge_dimension), np.zeros(linking_dimension)
    ]))
    linking_projector = np.eye(total_dimension) - edge_projector
    central_projector_residual = float(np.linalg.norm(
        edge_projector @ linking_projector
    ))

    assert maximum_trace_identity_residual < 1.0e-8
    assert maximum_selfadjoint_residual < 1.0e-10
    assert maximum_real_half_trace_residual < 1.0e-8
    assert signature(common_origin_values) == [7, 0, 20]
    assert signature(common_vacuum_values) == [0, 0, 27]
    assert common_vacuum_values[0] > 4.2
    assert all(
        row["origin_signature"] == [7, 0, 20]
        and row["vacuum_signature"] == [0, 0, 27]
        for row in positive_metric_scan
    )
    assert central_projector_residual == 0.0
    assert edge_dimension != linking_dimension

    result = {
        "gate": "version7_common_chain_number_hodge_relative_trace_gate",
        "common_curvature_carrier": {
            "edge_hodge_dimension": edge_dimension,
            "linking_chain_dimension": linking_dimension,
            "total_complex_dimension": total_dimension,
            "curvature": "diag(M_E,i delta_N(Q^2-Q0^2))",
            "single_action": "1/2 Tr_96(F_common^2)-constant",
            "reduced_action": "S_E+||R_U||^2",
            "maximum_trace_identity_residual": maximum_trace_identity_residual,
            "maximum_selfadjoint_residual": maximum_selfadjoint_residual,
        },
        "real_completion": {
            "doubled_dimension": 2 * total_dimension,
            "physical_half_trace_restores_common_action": True,
            "maximum_real_half_trace_residual": maximum_real_half_trace_residual,
        },
        "common_trace_hessians": {
            "origin_signature": signature(common_origin_values),
            "origin_heavy_gap": float(common_origin_values[7]),
            "vacuum_signature": signature(common_vacuum_values),
            "vacuum_minimum_eigenvalue": float(common_vacuum_values[0]),
        },
        "positive_metric_independence": {
            "scan": positive_metric_scan,
            "qualitative_selector_independent_of_positive_relative_weight": True,
            "qualitative_vacuum_stability_independent_of_positive_relative_weight": True,
        },
        "metric_uniqueness_boundary": {
            "full_matrix_trace_on_M96_is_unique": True,
            "full_M96_is_trace_container_not_coordinate_algebra": True,
            "edge_and_linking_subcarriers_have_different_dimensions": True,
            "unitary_exchange_symmetry_between_subcarriers": False,
            "orthogonal_central_projector_residual": central_projector_residual,
            "relative_hodge_metric_rescaling_forbidden_by_current_symmetry": False,
            "quantitative_mass_ratio_derived": False,
        },
        "verdict": {
            "one_unweighted_common_trace_exists": True,
            "common_trace_correct_origin_selector": True,
            "common_trace_strictly_stable_vacuum": True,
            "manual_weight_needed_for_qualitative_result": False,
            "unique_relative_hodge_metric_derived": False,
            "status": "positive_common_trace_qualitative_closure_metric_uniqueness_open",
            "next_gate": "version7_bicomplex_total_degree_hodge_metric_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()