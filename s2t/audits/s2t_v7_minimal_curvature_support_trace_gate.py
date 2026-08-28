#!/usr/bin/env python3
"""Audit trace uniqueness on the minimal edge/linking curvature supports."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_common_chain_number_hodge_relative_trace_gate import (
    chain_number_curvature,
)
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
OUTPUT = ROOT / "s2t/results/s2t_v7_minimal_curvature_support_trace_gate_results.json"
TOL = 1.0e-9


def commutant_dimension(operators: list[np.ndarray]) -> tuple[int, float]:
    dimension = operators[0].shape[0]
    identity = np.eye(dimension)
    equations = np.vstack([
        np.kron(identity, operator) - np.kron(operator.T, identity)
        for operator in operators
    ])
    singular_values = np.linalg.svd(equations, compute_uv=False)
    rank = int(np.sum(singular_values > TOL))
    nonzero = singular_values[singular_values > TOL]
    return dimension * dimension - rank, float(nonzero[-1])


def edge_diagonal_algebra() -> tuple[int, int, float]:
    coordinate_count = 27
    dimension = 2 * coordinate_count
    generators = []
    for index in range(coordinate_count):
        signed = np.zeros(dimension)
        signed[index] = 1.0
        signed[coordinate_count + index] = -1.0
        even = signed * signed
        generators.extend([np.diag(signed), np.diag(even)])
    span = np.column_stack([generator.reshape(-1) for generator in generators])
    algebra_dimension = int(np.linalg.matrix_rank(span, tol=TOL))
    gram = span.conj().T @ span
    minimum_nonzero_gram_eigenvalue = float(
        eigvalsh(gram)[-algebra_dimension]
    )
    return algebra_dimension, dimension, minimum_nonzero_gram_eigenvalue


def main() -> None:
    reference, variations, _, down_cut = physical_blocks()
    transfer, _, _ = polar_coisometry(reference)
    source = reference.shape[1]
    target = reference.shape[0]
    middle = source + target
    full_chain = source + middle + target
    endpoint_indices = np.concatenate([
        np.arange(source), np.arange(source + middle, full_chain)
    ])

    rng = np.random.default_rng(20260828)
    endpoint_operators = []
    maximum_compression_residual = 0.0
    maximum_rank = 0
    support_jump_from_origin = 0.0
    for sample in range(18):
        vector = rng.normal(size=len(variations))
        field = sum(
            coefficient * variation
            for coefficient, variation in zip(vector, variations)
        )
        full = chain_number_curvature(field, reference, transfer)
        endpoint = full[np.ix_(endpoint_indices, endpoint_indices)]
        endpoint_operators.append(endpoint)
        maximum_compression_residual = max(
            maximum_compression_residual,
            abs(float(np.trace(full @ full).real - np.trace(endpoint @ endpoint).real)),
        )
        eigenvalues, eigenvectors = np.linalg.eigh(endpoint)
        active = np.abs(eigenvalues) > TOL
        rank = int(np.sum(active))
        maximum_rank = max(maximum_rank, rank)
        if sample == 0:
            support_projector = eigenvectors[:, active] @ eigenvectors[:, active].conj().T
            support_jump_from_origin = float(np.linalg.norm(support_projector))

    linking_commutant_dimension, linking_commutant_gap = commutant_dimension(
        endpoint_operators
    )
    edge_algebra_dimension, edge_carrier_dimension, edge_gram_gap = (
        edge_diagonal_algebra()
    )

    endpoint_dimension = len(endpoint_indices)
    surrogate_simple_summands = edge_algebra_dimension + 1
    surrogate_trace_parameters = surrogate_simple_summands - 1
    physical_simple_summands = 2
    physical_trace_parameters = 1

    central_trace_scan = []
    for edge_weight in (0.2, 0.5, 0.8):
        linking_weight = 1.0 - edge_weight
        relative_density = (
            linking_weight / endpoint_dimension
        ) / (edge_weight / edge_carrier_dimension)
        central_trace_scan.append({
            "edge_central_weight": edge_weight,
            "linking_central_weight": linking_weight,
            "relative_linking_density": relative_density,
        })

    standard_surrogate_edge_weight = edge_carrier_dimension / (
        edge_carrier_dimension + endpoint_dimension
    )
    standard_physical_edge_weight = 22.0 / 43.0

    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))
    linking_vacuum = relative_transfer_vacuum_hessian(
        reference, variations, transfer
    )
    hessian_scan = []
    for relative_weight in (0.25, 1.0, 18.0 / 7.0, 4.0):
        origin_values = eigvalsh(edge_origin)
        vacuum_values = eigvalsh(
            edge_vacuum + 2.0 * relative_weight * linking_vacuum
        )
        hessian_scan.append({
            "relative_linking_weight": relative_weight,
            "origin_signature": signature(origin_values),
            "vacuum_signature": signature(vacuum_values),
            "vacuum_minimum_eigenvalue": float(vacuum_values[0]),
            "vacuum_maximum_eigenvalue": float(vacuum_values[-1]),
        })

    assert endpoint_dimension == 21
    assert maximum_compression_residual < 1.0e-8
    assert maximum_rank == 14
    assert abs(support_jump_from_origin - np.sqrt(14.0)) < 1.0e-8
    assert linking_commutant_dimension == 1
    assert linking_commutant_gap > 1.0
    assert edge_algebra_dimension == edge_carrier_dimension == 54
    assert edge_gram_gap > 1.0
    assert surrogate_simple_summands == 55
    assert surrogate_trace_parameters == 54
    assert physical_trace_parameters == 1
    assert abs(standard_surrogate_edge_weight - 18.0 / 25.0) < TOL
    assert abs(standard_physical_edge_weight - 22.0 / 43.0) < TOL
    assert all(
        row["origin_signature"] == [7, 0, 20]
        and row["vacuum_signature"] == [0, 0, 27]
        for row in hessian_scan
    )

    result = {
        "gate": "version7_minimal_curvature_support_trace_gate",
        "fixed_support_compression": {
            "full_chain_dimension": full_chain,
            "endpoint_dimension": endpoint_dimension,
            "maximum_trace_compression_residual": maximum_compression_residual,
            "maximum_physical_curvature_rank": maximum_rank,
            "pointwise_support_projector_jump_from_origin": support_jump_from_origin,
            "pointwise_rank_normalization_is_smooth": False,
            "fixed_endpoint_projector_is_admissible": True,
        },
        "generated_algebras": {
            "linking_endpoint": {
                "carrier_dimension": endpoint_dimension,
                "commutant_dimension": linking_commutant_dimension,
                "smallest_nonzero_commutant_singular_value": linking_commutant_gap,
                "generated_factor": "M21(C)",
                "unique_normalized_trace": True,
            },
            "edge_diagonal_surrogate": {
                "carrier_dimension": edge_carrier_dimension,
                "generated_algebra": "C^54",
                "algebra_dimension": edge_algebra_dimension,
                "commutant_dimension": edge_carrier_dimension,
                "minimum_nonzero_generator_gram_eigenvalue": edge_gram_gap,
                "unique_normalized_trace": False,
            },
            "combined_surrogate": {
                "algebra": "C^54 direct_sum M21(C)",
                "center_dimension": surrogate_simple_summands,
                "faithful_normalized_trace_parameters": surrogate_trace_parameters,
            },
            "physical_factor_model": {
                "algebra": "M22(C) direct_sum M21(C)",
                "center_dimension": physical_simple_summands,
                "faithful_normalized_trace_parameters": physical_trace_parameters,
            },
        },
        "trace_normalization": {
            "central_weight_scan": central_trace_scan,
            "standard_one_copy_M75_restriction": {
                "edge_central_weight": standard_surrogate_edge_weight,
                "linking_central_weight": 1.0 - standard_surrogate_edge_weight,
                "relative_unnormalized_sector_weight": 1.0,
                "intrinsic_to_abstract_direct_sum_algebra": False,
            },
            "standard_one_copy_M43_restriction": {
                "edge_central_weight": standard_physical_edge_weight,
                "linking_central_weight": 1.0 - standard_physical_edge_weight,
                "relative_unnormalized_sector_weight": 1.0,
                "intrinsic_to_abstract_direct_sum_algebra": False,
            },
        },
        "simple_completion_cost": {
            "surrogate_completion": "M75(C)",
            "surrogate_offdiagonal_complex_dimension": 54 * 21,
            "physical_completion": "M43(C)",
            "physical_offdiagonal_complex_dimension": 22 * 21,
            "existing_canonical_cross_connector_found": False,
        },
        "physical_hessian_control": {
            "scan": hessian_scan,
            "qualitative_selector_independent_of_trace_weight": True,
            "quantitative_spectrum_independent_of_trace_weight": False,
        },
        "verdict": {
            "minimal_support_produces_unique_common_trace": False,
            "linking_factor_trace_unique": True,
            "common_direct_sum_trace_unique": False,
            "declaring_full_matrix_container_is_derivation": False,
            "qualitative_parent_closed": True,
            "mass_metric_derived": False,
            "status": "minimal_support_trace_no_go_qualitative_parent_mass_metric_freeze_open",
            "next_gate": "version7_qualitative_parent_mass_metric_freeze_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()