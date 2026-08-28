#!/usr/bin/env python3
"""Audit a three-term linking superconnection for the polar relative curvature."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh
from scipy.optimize import brentq

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
OUTPUT = ROOT / "s2t/results/s2t_v7_real_linking_superconnection_assembly_gate_results.json"
TOL = 1.0e-10


def linking_chain(field: np.ndarray, transfer: np.ndarray):
    """Return d, B0, B1 on H_s -> H_s+H_t -> H_t."""
    target, source = field.shape
    middle = source + target
    total = source + middle + target
    first = np.vstack([field.conj().T @ transfer, field])
    second = np.hstack([field, -transfer @ field.conj().T])
    differential = np.zeros((total, total), dtype=complex)
    differential[source:source + middle, :source] = first
    differential[source + middle:, source:source + middle] = second
    return differential, first, second


def full_curvature_hessians(reference, variations, transfer):
    d0, _, _ = linking_chain(reference, transfer)
    q0 = d0 + d0.conj().T
    curvature0 = q0 @ q0
    generators = []
    for item in variations:
        differential, _, _ = linking_chain(item, transfer)
        generators.append(differential + differential.conj().T)

    size = len(generators)
    origin = np.zeros((size, size))
    vacuum_linear = []
    for first in generators:
        vacuum_linear.append(q0 @ first + first @ q0)
    vacuum = np.array([
        [np.real(np.vdot(first, second)) for second in vacuum_linear]
        for first in vacuum_linear
    ])
    for i, first in enumerate(generators):
        for j, second in enumerate(generators):
            quadratic = (first @ second + second @ first) / 2.0
            origin[i, j] = -2.0 * np.real(np.vdot(curvature0, quadratic))
    return origin, vacuum


def rounded(values):
    return [float(f"{value:.12g}") for value in values]


def main() -> None:
    reference, variations, _, down_cut = physical_blocks()
    transfer, _, defect = polar_coisometry(reference)
    source = reference.shape[1]
    target = reference.shape[0]
    middle = source + target

    rng = np.random.default_rng(20260828)
    factorization_residual = 0.0
    square_block_residual = 0.0
    oddness_residual = 0.0
    even_square_residual = 0.0
    grading = np.diag(np.concatenate([
        np.ones(source), -np.ones(middle), np.ones(target)
    ]))
    for _ in range(100):
        field = (rng.normal(size=reference.shape)
                 + 1j * rng.normal(size=reference.shape))
        differential, first, second = linking_chain(field, transfer)
        relative = (field @ field.conj().T @ transfer
                    - transfer @ field.conj().T @ field)
        factorization_residual = max(
            factorization_residual,
            float(np.linalg.norm(second @ first - relative)),
        )
        square = differential @ differential
        square_block_residual = max(
            square_block_residual,
            float(np.linalg.norm(square[source + middle:, :source] - relative)),
        )
        oddness_residual = max(
            oddness_residual,
            float(np.linalg.norm(grading @ differential
                                 + differential @ grading)),
        )
        even_square_residual = max(
            even_square_residual,
            float(np.linalg.norm(grading @ square - square @ grading)),
        )

    reference_d, reference_first, reference_second = linking_chain(
        reference, transfer
    )
    reference_nilpotency_residual = float(np.linalg.norm(
        reference_second @ reference_first
    ))
    zero_differential = linking_chain(np.zeros_like(reference), transfer)[0]
    zero_nilpotency_residual = float(np.linalg.norm(
        zero_differential @ zero_differential
    ))

    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))
    full_origin, full_vacuum = full_curvature_hessians(
        reference, variations, transfer
    )
    relative_vacuum = relative_transfer_vacuum_hessian(
        reference, variations, transfer
    )

    degree_two_origin_values = eigvalsh(edge_origin)
    degree_two_vacuum_values = eigvalsh(edge_vacuum + relative_vacuum)
    full_origin_values = eigvalsh(edge_origin + full_origin)
    full_vacuum_values = eigvalsh(edge_vacuum + full_vacuum)

    def heavy_minimum(scale: float) -> float:
        return float(eigvalsh(edge_origin + scale * full_origin)[7])

    critical_scale = brentq(heavy_minimum, 0.0, 0.125)
    normalization_tests = []
    for name, scale in (
        ("full_half_trace", 1.0),
        ("real_half_of_full_trace", 0.5),
        ("offdiagonal_orientation_quarter", 0.25),
        ("double_deduplication_eighth", 0.125),
        ("first_passing_sixteenth", 0.0625),
    ):
        values = eigvalsh(edge_origin + scale * full_origin)
        normalization_tests.append({
            "name": name,
            "scale": scale,
            "signature": signature(values),
            "heavy_gap": float(values[7]),
            "passes": signature(values) == [7, 0, 20],
        })

    # The full self-adjoint square contains diagonal blocks in addition to
    # the desired length-two block d^2.  Projecting to Hom(H0,H2) recovers
    # precisely R_U, but this is a chain-degree projection still requiring a
    # represented calculus or quotient.
    d2 = reference_d @ reference_d
    degree_two_projected = np.zeros_like(d2)
    degree_two_projected[source + middle:, :source] = (
        d2[source + middle:, :source]
    )
    reference_q = reference_d + reference_d.conj().T
    unwanted_full_square_residual = float(np.linalg.norm(
        reference_q @ reference_q
        - degree_two_projected - degree_two_projected.conj().T
    ))

    assert factorization_residual < 1.0e-12
    assert square_block_residual < 1.0e-12
    assert oddness_residual < 1.0e-12
    assert even_square_residual < 1.0e-12
    assert reference_nilpotency_residual < 1.0e-12
    assert zero_nilpotency_residual == 0.0
    assert signature(degree_two_origin_values) == [7, 0, 20]
    assert signature(degree_two_vacuum_values) == [0, 0, 27]
    assert signature(full_origin_values) == [27, 0, 0]
    assert signature(full_vacuum_values) == [0, 0, 27]
    assert abs(critical_scale - 1.0 / 15.0) < 1.0e-10
    assert normalization_tests[3]["signature"] == [21, 0, 6]
    assert normalization_tests[4]["signature"] == [7, 0, 20]
    assert unwanted_full_square_residual > 1.0
    assert np.linalg.matrix_rank(full_vacuum, TOL) == 27
    assert np.linalg.matrix_rank(defect, TOL) == 1

    result = {
        "gate": "version7_real_linking_superconnection_assembly_gate",
        "three_term_linking_chain": {
            "dimensions": [source, middle, target],
            "total_complex_dimension": source + middle + target,
            "B0": "column(A*U,A)",
            "B1": "row(A,-UA*)",
            "d_is_odd": True,
            "d_square_is_even": True,
            "maximum_oddness_residual": oddness_residual,
            "maximum_even_square_residual": even_square_residual,
        },
        "relative_curvature_factorization": {
            "identity": "B1 B0 = AA*U-UA*A = R_U",
            "maximum_factorization_residual": factorization_residual,
            "maximum_d_square_block_residual": square_block_residual,
            "reference_nilpotency_residual": reference_nilpotency_residual,
            "zero_nilpotency_residual": zero_nilpotency_residual,
            "positive_factorization": True,
        },
        "degree_two_curvature_block": {
            "projection": "Hom(H0,H2) block of d^2",
            "origin_signature_with_edge_hodge": signature(
                degree_two_origin_values
            ),
            "origin_heavy_gap": float(degree_two_origin_values[7]),
            "vacuum_signature_with_edge_hodge": signature(
                degree_two_vacuum_values
            ),
            "vacuum_minimum_eigenvalue": float(
                degree_two_vacuum_values[0]
            ),
            "represented_degree_projection_derived": False,
        },
        "full_selfadjoint_curvature": {
            "operator": "Q=d+d*",
            "curvature": "Q^2-Q0^2",
            "contains_diagonal_gram_blocks": True,
            "unwanted_square_block_norm": unwanted_full_square_residual,
            "origin_signature": signature(full_origin_values),
            "origin_heavy_gap": float(full_origin_values[7]),
            "origin_eigenvalues": rounded(full_origin_values),
            "vacuum_signature": signature(full_vacuum_values),
            "vacuum_minimum_eigenvalue": float(full_vacuum_values[0]),
            "vacuum_hessian_rank": int(np.linalg.matrix_rank(
                full_vacuum, TOL
            )),
        },
        "normalization_test": {
            "exact_allowed_full_curvature_window": "0 <= alpha < 1/15",
            "critical_scale": critical_scale,
            "standard_orientation_and_real_factors": normalization_tests,
            "canonical_standard_factor_passes": False,
        },
        "verdict": {
            "relative_curvature_is_square_of_three_term_differential": True,
            "ordinary_full_selfadjoint_curvature_is_parent": False,
            "ordinary_full_square_restores_forbidden_gram_channels": True,
            "degree_two_block_local_parent_survives": True,
            "degree_two_projection_is_yet_derived": False,
            "status": "positive_three_term_factorization_full_curvature_no_go_degree_two_quotient_open",
            "next_gate": "version7_linking_chain_degree_two_curvature_quotient_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()