#!/usr/bin/env python3
"""Audit the polar incidence transfer behind the apparent 11/21 weight."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigh, eigvalsh

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_common_irreducible_trace_multiplicity_gate import (
    split_physical_hessians,
)
from s2t_v7_derived_relative_involution_curvature_norm_gate import (
    edge_hessians,
    physical_blocks,
    physical_hessians,
    signature,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_incidence_transfer_markov_weight_gate_results.json"
TOL = 1.0e-10


def polar_coisometry(reference: np.ndarray):
    gram = reference.conj().T @ reference
    values, vectors = eigh(gram)
    inverse_square_root = vectors @ np.diag([
        0.0 if value < TOL else value ** -0.5 for value in values
    ]) @ vectors.conj().T
    transfer = reference @ inverse_square_root
    support = transfer.conj().T @ transfer
    defect = np.eye(reference.shape[1]) - support
    return transfer, support, defect


def quotient_hessians(reference, variations, transfer):
    left_reference = reference.conj().T @ reference
    right_reference = reference @ reference.conj().T
    zero_curvature = -(transfer @ left_reference @ transfer.conj().T
                       + right_reference) / 2.0

    origin = np.zeros((len(variations), len(variations)))
    vacuum = np.zeros_like(origin)
    for i, first in enumerate(variations):
        left_linear_i = reference.conj().T @ first + first.conj().T @ reference
        right_linear_i = reference @ first.conj().T + first @ reference.conj().T
        transfer_linear_i = (
            transfer @ left_linear_i @ transfer.conj().T + right_linear_i
        ) / 2.0
        for j, second in enumerate(variations):
            left_linear_j = (reference.conj().T @ second
                             + second.conj().T @ reference)
            right_linear_j = (reference @ second.conj().T
                              + second @ reference.conj().T)
            transfer_linear_j = (
                transfer @ left_linear_j @ transfer.conj().T + right_linear_j
            ) / 2.0
            vacuum[i, j] = np.real(np.vdot(
                transfer_linear_i, transfer_linear_j
            ))

            left_quadratic = (
                first.conj().T @ second + second.conj().T @ first
            ) / 2.0
            right_quadratic = (
                first @ second.conj().T + second @ first.conj().T
            ) / 2.0
            transfer_quadratic = (
                transfer @ left_quadratic @ transfer.conj().T
                + right_quadratic
            ) / 2.0
            origin[i, j] = 2.0 * np.real(np.vdot(
                zero_curvature, transfer_quadratic
            ))
    return origin, vacuum


def main() -> None:
    reference, variations, heavy_labels, down_cut = physical_blocks()
    root_labels = ["QLuR", "QLdR", "LLeR", "LLYR", "XLXR", "XLeR", "YLYR"]
    labels = root_labels + heavy_labels
    transfer, support, defect = polar_coisometry(reference)

    assert reference.shape == (10, 11)
    assert np.linalg.matrix_rank(reference, TOL) == 10
    assert np.linalg.matrix_rank(support, TOL) == 10
    assert np.linalg.matrix_rank(defect, TOL) == 1
    coisometry_residual = float(np.linalg.norm(
        transfer @ transfer.conj().T - np.eye(10)
    ))
    support_residual = float(np.linalg.norm(support @ support - support))

    physical_origin, physical_vacuum = physical_hessians(reference, variations)
    quotient_origin, quotient_vacuum = quotient_hessians(
        reference, variations, transfer
    )
    origin_half_residual = float(np.linalg.norm(
        quotient_origin - physical_origin / 2.0
    ))

    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))
    quotient_origin_values = eigvalsh(edge_origin + quotient_origin)
    quotient_vacuum_values = eigvalsh(edge_vacuum + quotient_vacuum)

    # The trace-preserving expectation onto the tied M10 corner duplicates
    # the averaged curvature in both matched corners.  The rank-one defect
    # has no linear or quadratic contribution at the origin, so its origin
    # Hessian is exactly twice the one-corner quotient Hessian.
    expectation_origin = 2.0 * quotient_origin
    expectation_origin_values = eigvalsh(edge_origin + expectation_origin)

    left_origin, right_origin = split_physical_hessians(reference, variations)
    source_values, source_vectors = eigh(edge_origin + left_origin)
    negative_indices = np.where(source_values < -TOL)[0]
    unwanted = set(heavy_labels)
    extra_modes = []
    for index in negative_indices:
        weights = abs(source_vectors[:, index]) ** 2
        dominant = int(np.argmax(weights))
        if labels[dominant] in unwanted:
            extra_modes.append({
                "eigenvalue": float(source_values[index]),
                "dominant_label": labels[dominant],
                "dominant_weight": float(weights[dominant]),
            })
    assert any(item["dominant_label"] == "LLXR_w1_im" for item in extra_modes)

    # The quotient channel T(X,Y)=(UXU*+Y)/2 is unital and completely
    # positive as a convex sum of two completely positive maps.  Positivity
    # is also checked numerically on deterministic random positive inputs.
    rng = np.random.default_rng(20260828)
    positivity_minimum = float("inf")
    for _ in range(100):
        source_seed = rng.normal(size=(11, 11)) + 1j * rng.normal(size=(11, 11))
        target_seed = rng.normal(size=(10, 10)) + 1j * rng.normal(size=(10, 10))
        source_positive = source_seed.conj().T @ source_seed
        target_positive = target_seed.conj().T @ target_seed
        image = (transfer @ source_positive @ transfer.conj().T
                 + target_positive) / 2.0
        positivity_minimum = min(
            positivity_minimum, float(eigvalsh(image)[0])
        )
    unital_residual = float(np.linalg.norm(
        (transfer @ np.eye(11) @ transfer.conj().T + np.eye(10)) / 2.0
        - np.eye(10)
    ))

    assert coisometry_residual < 1.0e-12
    assert support_residual < 1.0e-12
    assert origin_half_residual < 1.0e-12
    assert signature(quotient_origin_values) == [7, 0, 20]
    assert signature(quotient_vacuum_values) == [0, 0, 27]
    assert signature(expectation_origin_values) == [21, 0, 6]
    assert positivity_minimum > -1.0e-10
    assert unital_residual < 1.0e-12

    result = {
        "gate": "version7_incidence_transfer_markov_weight_gate",
        "polar_transfer": {
            "reference_shape": list(reference.shape),
            "reference_rank": 10,
            "matched_source_support_rank": 10,
            "source_defect_rank": 1,
            "decomposition": "21 = 10 matched source + 10 target + 1 index defect",
            "coisometry_residual": coisometry_residual,
            "support_projector_residual": support_residual,
        },
        "source_corner_reinterpretation": {
            "signature": signature(source_values),
            "unwanted_negative_modes": extra_modes,
            "meaning": "source-only curvature forgets target endpoint data",
        },
        "one_corner_quotient_channel": {
            "formula": "T(X,Y)=(U X U* + Y)/2",
            "unital_residual": unital_residual,
            "random_positive_input_minimum_eigenvalue": positivity_minimum,
            "origin_half_full_hessian_residual": origin_half_residual,
            "origin_signature": signature(quotient_origin_values),
            "origin_heavy_gap": float(quotient_origin_values[7]),
            "vacuum_signature": signature(quotient_vacuum_values),
            "vacuum_minimum_eigenvalue": float(quotient_vacuum_values[0]),
            "local_selector_pass": True,
        },
        "trace_preserving_expectation": {
            "matched_corner_is_duplicated": True,
            "origin_hessian_equals_twice_quotient_hessian": True,
            "origin_signature": signature(expectation_origin_values),
            "origin_heavy_gap": float(expectation_origin_values[7]),
            "local_selector_pass": False,
        },
        "verdict": {
            "eleven_over_twenty_one_is_fundamental_weight": False,
            "canonical_polar_quotient_derives_local_half_weight": True,
            "full_trace_preserving_expectation_derives_half_weight": False,
            "physical_reduced_quotient_is_derived": False,
            "status": "local_ucp_quotient_pass_full_expectation_no_go",
            "next_gate": "version7_index_defect_reduced_linking_quotient_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()