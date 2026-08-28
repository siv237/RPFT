#!/usr/bin/env python3
"""Audit ordinary junk and the chain-number relative degree-two quotient."""

from __future__ import annotations

import hashlib
from itertools import product
import json
from pathlib import Path
import sys

import numpy as np

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
from s2t_v7_real_linking_superconnection_assembly_gate import linking_chain


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_linking_chain_degree_two_curvature_quotient_gate_results.json"
TOL = 1.0e-9


def orthonormal_span(columns: np.ndarray) -> np.ndarray:
    left, values, _ = np.linalg.svd(columns, full_matrices=False)
    return left[:, values > TOL]


def node_projectors(sizes):
    offsets = np.cumsum([0] + list(sizes))
    total = offsets[-1]
    projectors = []
    for index, size in enumerate(sizes):
        item = np.zeros((total, total), dtype=complex)
        item[offsets[index]:offsets[index + 1],
             offsets[index]:offsets[index + 1]] = np.eye(size)
        projectors.append(item)
    return offsets, projectors


def ordinary_junk_audit(field, transfer):
    differential, _, _ = linking_chain(field, transfer)
    dirac = differential + differential.conj().T
    sizes = (field.shape[1], field.shape[1] + field.shape[0], field.shape[0])
    offsets, projectors = node_projectors(sizes)

    def commutator(left, right):
        return left @ right - right @ left

    represented_one = []
    differentials_of_one = []
    for first, second in product(range(3), repeat=2):
        represented_one.append(
            projectors[first] @ commutator(dirac, projectors[second])
        )
        differentials_of_one.append(
            commutator(dirac, projectors[first])
            @ commutator(dirac, projectors[second])
        )
    one_matrix = np.stack([item.reshape(-1) for item in represented_one], axis=1)
    _, one_values, one_right = np.linalg.svd(one_matrix, full_matrices=True)
    one_rank = int(np.sum(one_values > TOL))
    one_kernel = one_right[one_rank:].conj().T

    junk_columns = []
    for kernel_index in range(one_kernel.shape[1]):
        junk = sum(
            one_kernel[generator, kernel_index] * differentials_of_one[generator]
            for generator in range(len(differentials_of_one))
        )
        junk_columns.append(junk.reshape(-1))
    junk_matrix = np.stack(junk_columns, axis=1)
    junk_basis = orthonormal_span(junk_matrix)

    represented_two = []
    for first, second, third in product(range(3), repeat=3):
        represented_two.append(
            projectors[first]
            @ commutator(dirac, projectors[second])
            @ commutator(dirac, projectors[third])
        )
    two_matrix = np.stack([item.reshape(-1) for item in represented_two], axis=1)
    two_basis = orthonormal_span(two_matrix)

    curvature = dirac @ dirac
    endpoint = np.zeros_like(curvature)
    endpoint[offsets[2]:offsets[3], offsets[0]:offsets[1]] = (
        curvature[offsets[2]:offsets[3], offsets[0]:offsets[1]]
    )
    endpoint[offsets[0]:offsets[1], offsets[2]:offsets[3]] = (
        curvature[offsets[0]:offsets[1], offsets[2]:offsets[3]]
    )
    endpoint_vector = endpoint.reshape(-1)
    endpoint_outside_junk = float(np.linalg.norm(
        endpoint_vector - junk_basis @ (junk_basis.conj().T @ endpoint_vector)
    ))
    endpoint_outside_two = float(np.linalg.norm(
        endpoint_vector - two_basis @ (two_basis.conj().T @ endpoint_vector)
    ))
    junk_outside_two = float(np.linalg.norm(
        junk_basis - two_basis @ (two_basis.conj().T @ junk_basis)
    ))
    return {
        "one_form_rank": one_rank,
        "one_form_kernel_dimension": int(one_kernel.shape[1]),
        "represented_two_form_rank": int(two_basis.shape[1]),
        "degree_two_junk_rank": int(junk_basis.shape[1]),
        "degree_two_quotient_rank": int(two_basis.shape[1] - junk_basis.shape[1]),
        "endpoint_norm": float(np.linalg.norm(endpoint_vector)),
        "endpoint_residual_outside_two_forms": endpoint_outside_two,
        "endpoint_residual_outside_junk": endpoint_outside_junk,
        "junk_residual_outside_two_forms": junk_outside_two,
    }


def random_unitary(size, rng):
    seed = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    q, r = np.linalg.qr(seed)
    phases = np.diag(r)
    phases = np.where(abs(phases) > 1.0e-14, phases / abs(phases), 1.0)
    return q @ np.diag(phases.conj())


def main() -> None:
    reference, variations, _, down_cut = physical_blocks()
    transfer, _, _ = polar_coisometry(reference)
    source = reference.shape[1]
    target = reference.shape[0]
    middle = source + target
    total = source + middle + target
    offsets = np.cumsum([0, source, middle, target])

    rng = np.random.default_rng(20260828)
    junk_controls = []
    maximum_junk_endpoint_residual = 0.0
    maximum_junk_containment_residual = 0.0
    maximum_number_endpoint_residual = 0.0
    maximum_number_norm_residual = 0.0
    maximum_covariance_residual = 0.0
    maximum_reversal_norm_residual = 0.0

    number = np.diag(np.concatenate([
        np.zeros(source), np.ones(middle), 2.0 * np.ones(target)
    ]))
    reversed_number = 2.0 * np.eye(total) - number

    for _ in range(20):
        field = (rng.normal(size=reference.shape)
                 + 1j * rng.normal(size=reference.shape))
        control = ordinary_junk_audit(field, transfer)
        junk_controls.append(control)
        maximum_junk_endpoint_residual = max(
            maximum_junk_endpoint_residual,
            control["endpoint_residual_outside_junk"],
        )
        maximum_junk_containment_residual = max(
            maximum_junk_containment_residual,
            control["junk_residual_outside_two_forms"],
        )

        differential, _, _ = linking_chain(field, transfer)
        curvature = (differential + differential.conj().T) @ (
            differential + differential.conj().T
        )
        relative = 0.5 * (number @ curvature - curvature @ number)
        endpoint = np.zeros_like(curvature)
        endpoint[offsets[2]:offsets[3], offsets[0]:offsets[1]] = (
            curvature[offsets[2]:offsets[3], offsets[0]:offsets[1]]
        )
        endpoint[offsets[0]:offsets[1], offsets[2]:offsets[3]] = (
            curvature[offsets[0]:offsets[1], offsets[2]:offsets[3]]
        )
        signed_endpoint = 0.5 * (number @ endpoint - endpoint @ number)
        maximum_number_endpoint_residual = max(
            maximum_number_endpoint_residual,
            float(np.linalg.norm(relative - signed_endpoint)),
        )
        maximum_number_norm_residual = max(
            maximum_number_norm_residual,
            abs(np.linalg.norm(relative) ** 2 - np.linalg.norm(endpoint) ** 2),
        )

        gauges = [random_unitary(size, rng) for size in (source, middle, target)]
        gauge = np.zeros((total, total), dtype=complex)
        for index, item in enumerate(gauges):
            gauge[offsets[index]:offsets[index + 1],
                  offsets[index]:offsets[index + 1]] = item
        transformed = gauge @ curvature @ gauge.conj().T
        transformed_relative = 0.5 * (
            number @ transformed - transformed @ number
        )
        maximum_covariance_residual = max(
            maximum_covariance_residual,
            float(np.linalg.norm(
                transformed_relative - gauge @ relative @ gauge.conj().T
            )),
        )

        reversed_relative = 0.5 * (
            reversed_number @ curvature - curvature @ reversed_number
        )
        maximum_reversal_norm_residual = max(
            maximum_reversal_norm_residual,
            abs(np.linalg.norm(reversed_relative) - np.linalg.norm(relative)),
        )

    stable_rank_rows = {
        (item["one_form_rank"], item["represented_two_form_rank"],
         item["degree_two_junk_rank"], item["degree_two_quotient_rank"])
        for item in junk_controls
    }

    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))
    relative_vacuum = relative_transfer_vacuum_hessian(
        reference, variations, transfer
    )
    origin_values = np.linalg.eigvalsh(edge_origin)
    vacuum_values = np.linalg.eigvalsh(edge_vacuum + relative_vacuum)

    assert stable_rank_rows == {(4, 6, 2, 4)}
    assert maximum_junk_endpoint_residual < 1.0e-10
    assert maximum_junk_containment_residual < 1.0e-10
    assert maximum_number_endpoint_residual < 1.0e-10
    assert maximum_number_norm_residual < 1.0e-8
    assert maximum_covariance_residual < 1.0e-10
    assert maximum_reversal_norm_residual < 1.0e-10
    assert signature(origin_values) == [7, 0, 20]
    assert signature(vacuum_values) == [0, 0, 27]

    result = {
        "gate": "version7_linking_chain_degree_two_curvature_quotient_gate",
        "ordinary_connes_calculus": {
            "node_algebra": "C^3 acting by scalars on H0,H1,H2",
            "chain_dimensions": [source, middle, target],
            "random_controls": len(junk_controls),
            "stable_ranks": {
                "represented_one_forms": 4,
                "represented_two_forms": 6,
                "degree_two_junk": 2,
                "degree_two_quotient": 4,
            },
            "maximum_endpoint_residual_outside_junk": maximum_junk_endpoint_residual,
            "maximum_junk_residual_outside_two_forms": maximum_junk_containment_residual,
            "endpoint_length_two_class_survives": False,
            "ordinary_junk_quotient_pass": False,
        },
        "chain_number_relative_derivation": {
            "number_operator": "N=diag(0*I11,1*I21,2*I10)",
            "definition": "delta_N(F)=1/2[N,F]",
            "adjacent_degree_spacing": 1,
            "endpoint_degree_gap": 2,
            "unique_up_to_additive_constant_and_orientation": True,
            "kills_diagonal_backtracking_blocks": True,
            "retains_exactly_endpoint_blocks": True,
            "maximum_endpoint_projection_residual": maximum_number_endpoint_residual,
            "maximum_endpoint_norm_residual": maximum_number_norm_residual,
            "maximum_block_gauge_covariance_residual": maximum_covariance_residual,
            "maximum_orientation_reversal_norm_residual": maximum_reversal_norm_residual,
            "continuous_weight_added": False,
        },
        "relative_hodge_action": {
            "formula": "S_E+1/4||delta_N(Q^2-Q0^2)||^2 = S_E+1/2||R_U||^2",
            "origin_signature": signature(origin_values),
            "origin_heavy_gap": float(origin_values[7]),
            "vacuum_signature": signature(vacuum_values),
            "vacuum_minimum_eigenvalue": float(vacuum_values[0]),
            "bounded_below": True,
        },
        "status_boundary": {
            "ordinary_connes_two_form_interpretation": False,
            "relative_mapping_cone_interpretation": True,
            "relative_observable_selected_by_chain_degree": True,
            "single_common_hodge_trace_with_edge_moment_derived": False,
        },
        "verdict": {
            "standard_junk_route": "failed_endpoint_is_junk",
            "canonical_chain_number_relative_quotient": "passed",
            "manual_endpoint_projector_needed": False,
            "correct_origin_selector": True,
            "strictly_stable_vacuum": True,
            "status": "ordinary_junk_no_go_chain_number_mapping_cone_pass_common_hodge_trace_open",
            "next_gate": "version7_common_chain_number_hodge_relative_trace_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()