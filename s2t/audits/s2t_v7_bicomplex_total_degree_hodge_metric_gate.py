#!/usr/bin/env python3
"""Audit whether bicomplex total degree fixes the relative Hodge metric."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (
    edge_hessians,
    physical_blocks,
    signature,
)
from s2t_v7_incidence_transfer_markov_weight_gate import polar_coisometry
from s2t_v7_polar_transfer_cross_curvature_origin_gate import (
    relative_transfer_vacuum_hessian,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_bicomplex_total_degree_hodge_metric_gate_results.json"
TOL = 1.0e-10


def minimal_square_bicomplex(vertical_scale: float):
    """Return a 1-1-1-1 square with anticommuting horizontal/vertical arrows."""
    horizontal = np.zeros((4, 4), dtype=float)
    vertical = np.zeros((4, 4), dtype=float)
    # Basis order: (0,0), (1,0), (0,1), (1,1).
    horizontal[1, 0] = 1.0
    horizontal[3, 2] = 1.0
    vertical[2, 0] = vertical_scale
    vertical[3, 1] = -vertical_scale
    total = horizontal + vertical
    degree = np.diag([0.0, 1.0, 1.0, 2.0])
    return horizontal, vertical, total, degree


def hodge_involution(relative_weight: float, edge_dim: int, linking_dim: int):
    """Build an isometric Hodge involution for every positive sector weight."""
    metric = np.diag(np.concatenate([
        np.ones(edge_dim), relative_weight * np.ones(linking_dim)
    ]))
    inverse_metric = np.diag(1.0 / np.diag(metric))
    zero = np.zeros_like(metric)
    star = np.block([[zero, inverse_metric], [metric, zero]])
    doubled_metric = np.block([[metric, zero], [zero, inverse_metric]])
    return metric, star, doubled_metric


def main() -> None:
    square_scan = []
    for scale in (0.125, 0.5, 1.0, 2.0, 8.0):
        horizontal, vertical, total, degree = minimal_square_bicomplex(scale)
        square_scan.append({
            "vertical_scale": scale,
            "horizontal_nilpotence_residual": float(np.linalg.norm(horizontal @ horizontal)),
            "vertical_nilpotence_residual": float(np.linalg.norm(vertical @ vertical)),
            "anticommutator_residual": float(np.linalg.norm(
                horizontal @ vertical + vertical @ horizontal
            )),
            "total_nilpotence_residual": float(np.linalg.norm(total @ total)),
            "total_degree_residual": float(np.linalg.norm(
                degree @ total - total @ degree - total
            )),
        })

    edge_dim = 54
    linking_dim = 42
    total_dim = edge_dim + linking_dim
    total_degree_two = 2.0 * np.eye(total_dim)
    edge_projector = np.diag(np.concatenate([
        np.ones(edge_dim), np.zeros(linking_dim)
    ]))
    linking_projector = np.eye(total_dim) - edge_projector

    metric_scan = []
    for weight in (0.125, 0.5, 1.0, 2.0, 8.0):
        metric, star, doubled_metric = hodge_involution(
            weight, edge_dim, linking_dim
        )
        metric_scan.append({
            "relative_weight": weight,
            "minimum_metric_eigenvalue": float(eigvalsh(metric)[0]),
            "commutator_with_total_degree": float(np.linalg.norm(
                metric @ total_degree_two - total_degree_two @ metric
            )),
            "commutator_with_edge_projector": float(np.linalg.norm(
                metric @ edge_projector - edge_projector @ metric
            )),
            "hodge_involution_residual": float(np.linalg.norm(
                star @ star - np.eye(2 * total_dim)
            )),
            "hodge_isometry_residual": float(np.linalg.norm(
                star.T @ doubled_metric @ star - doubled_metric
            )),
            "real_compatibility_residual": float(np.linalg.norm(star.imag)),
        })

    # A maximal isometric injection from the 42-dimensional linking carrier
    # into the 54-dimensional edge carrier necessarily leaves a 12-dimensional
    # orthogonal defect.  Hence no unitary Hodge exchange can identify them.
    injection = np.zeros((edge_dim, linking_dim), dtype=float)
    injection[:linking_dim, :] = np.eye(linking_dim)
    source_isometry_residual = float(np.linalg.norm(
        injection.T @ injection - np.eye(linking_dim)
    ))
    support = injection @ injection.T
    defect = np.eye(edge_dim) - support
    defect_rank = int(np.linalg.matrix_rank(defect, tol=TOL))

    reference, variations, _, down_cut = physical_blocks()
    transfer, _, _ = polar_coisometry(reference)
    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))
    linking_vacuum = relative_transfer_vacuum_hessian(
        reference, variations, transfer
    )

    physical_metric_scan = []
    spectra = {}
    for weight in (0.25, 1.0, 4.0):
        origin_values = eigvalsh(edge_origin)
        vacuum_values = eigvalsh(edge_vacuum + 2.0 * weight * linking_vacuum)
        spectra[weight] = vacuum_values
        physical_metric_scan.append({
            "relative_weight": weight,
            "origin_signature": signature(origin_values),
            "vacuum_signature": signature(vacuum_values),
            "vacuum_minimum_eigenvalue": float(vacuum_values[0]),
            "vacuum_maximum_eigenvalue": float(vacuum_values[-1]),
            "vacuum_trace": float(np.sum(vacuum_values)),
        })

    low = spectra[0.25]
    high = spectra[4.0]
    best_global_scale = float(np.dot(low, high) / np.dot(low, low))
    nonhomothetic_spectrum_residual = float(
        np.linalg.norm(best_global_scale * low - high) / np.linalg.norm(high)
    )

    maximum_square_residual = max(
        max(row[key] for key in row if key.endswith("residual"))
        for row in square_scan
    )
    maximum_metric_residual = max(
        max(row[key] for key in row if key.endswith("residual"))
        for row in metric_scan
    )

    assert maximum_square_residual < TOL
    assert maximum_metric_residual < TOL
    assert all(row["minimum_metric_eigenvalue"] > 0.0 for row in metric_scan)
    assert source_isometry_residual < TOL
    assert defect_rank == edge_dim - linking_dim == 12
    assert all(
        row["origin_signature"] == [7, 0, 20]
        and row["vacuum_signature"] == [0, 0, 27]
        for row in physical_metric_scan
    )
    assert nonhomothetic_spectrum_residual > 0.05

    result = {
        "gate": "version7_bicomplex_total_degree_hodge_metric_gate",
        "algebraic_bicomplex_rescaling": {
            "basis_bidegrees": [[0, 0], [1, 0], [0, 1], [1, 1]],
            "scan": square_scan,
            "maximum_residual": maximum_square_residual,
            "vertical_rescaling_preserves_bicomplex_relations": True,
            "total_degree_fixes_relative_scale": False,
        },
        "hodge_metric_family": {
            "edge_dimension": edge_dim,
            "linking_dimension": linking_dim,
            "total_degree_two_dimension": total_dim,
            "scan": metric_scan,
            "maximum_residual": maximum_metric_residual,
            "positive_metrics_compatible_with_degree_real_and_hodge_star": True,
            "unique_relative_metric_derived": False,
        },
        "dimension_defect": {
            "maximal_linking_to_edge_isometry_residual": source_isometry_residual,
            "edge_minus_linking_dimension": edge_dim - linking_dim,
            "orthogonal_defect_rank": defect_rank,
            "unitary_exchange_possible": False,
            "affine_carrier_complex_dimension": 4 * 3,
            "dimension_matches_E_aff": defect_rank == 4 * 3,
            "canonical_affine_identification_derived": False,
        },
        "physical_hessian_family": {
            "scan": physical_metric_scan,
            "best_global_scale_low_to_high": best_global_scale,
            "nonhomothetic_spectrum_residual": nonhomothetic_spectrum_residual,
            "qualitative_signatures_fixed": True,
            "quantitative_spectrum_fixed": False,
        },
        "verdict": {
            "total_degree_closes_metric_uniqueness": False,
            "hodge_involution_closes_metric_uniqueness": False,
            "real_structure_closes_metric_uniqueness": False,
            "qualitative_vacuum_remains_closed": True,
            "mass_ratios_derived": False,
            "twelve_dimensional_completion_clue_found": True,
            "status": "bicomplex_total_degree_metric_no_go_affine_defect_completion_open",
            "next_gate": "version7_affine_defect_bicomplex_completion_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()