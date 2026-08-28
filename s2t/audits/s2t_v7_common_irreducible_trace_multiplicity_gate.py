#!/usr/bin/env python3
"""Audit trace multiplicities and the tempting 11/21 relative weight."""

from __future__ import annotations

from fractions import Fraction
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


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_common_irreducible_trace_multiplicity_gate_results.json"


def split_physical_hessians(reference: np.ndarray, variations: list[np.ndarray]):
    left_reference = reference.conj().T @ reference
    right_reference = reference @ reference.conj().T

    def quadratic(first, second):
        return (
            (first.conj().T @ second + second.conj().T @ first) / 2.0,
            (first @ second.conj().T + second @ first.conj().T) / 2.0,
        )

    left_origin = np.array([
        [-2.0 * np.real(np.vdot(left_reference, quadratic(first, second)[0]))
         for second in variations]
        for first in variations
    ])
    right_origin = np.array([
        [-2.0 * np.real(np.vdot(right_reference, quadratic(first, second)[1]))
         for second in variations]
        for first in variations
    ])
    return left_origin, right_origin


def row(name, beta, edge_origin, physical_origin):
    values = eigvalsh(edge_origin + float(beta) * physical_origin)
    return {
        "name": name,
        "beta": str(beta),
        "inside_window": float(beta) < 8.0 / 15.0,
        "signature": signature(values),
        "heavy_gap": float(values[7]),
    }


def main() -> None:
    reference, variations, labels, down_cut = physical_blocks()
    left_origin, right_origin = split_physical_hessians(reference, variations)
    physical_origin = left_origin + right_origin
    edge_origin, _ = edge_hessians(down_cut, len(variations))

    candidates = [
        row("single_full_trace", Fraction(1, 1), edge_origin, physical_origin),
        row("separately_normalized_22_and_21_corners", Fraction(22, 21),
            edge_origin, physical_origin),
        row("inverse_total_dimension_fraction", Fraction(21, 22),
            edge_origin, physical_origin),
        row("inverse_active_rank_fraction", Fraction(20, 22),
            edge_origin, physical_origin),
        row("tempting_source_fraction", Fraction(11, 21),
            edge_origin, physical_origin),
        row("tempting_target_fraction", Fraction(10, 21),
            edge_origin, physical_origin),
    ]
    assert candidates[0]["signature"] == [21, 0, 6]
    assert candidates[4]["signature"] == [7, 0, 20]
    assert candidates[5]["signature"] == [7, 0, 20]

    # Inserting the rank-11 or rank-10 corner projector into the trace does
    # not multiply the full two-sided curvature by its rank fraction.  It
    # selects one Gram end.  Both genuine corner insertions fail.
    source_values = eigvalsh(edge_origin + left_origin)
    target_values = eigvalsh(edge_origin + right_origin)
    assert signature(source_values) == [8, 0, 19]
    assert signature(target_values) == [17, 0, 10]

    left_gram = reference.conj().T @ reference
    right_gram = reference @ reference.conj().T
    physical_spectrum = np.sort(np.concatenate([
        eigvalsh(left_gram), eigvalsh(right_gram), np.zeros(1)
    ]))
    edge_reference_spectrum = np.ones(22)
    physical_rank = int(np.sum(physical_spectrum > 1.0e-10))
    spectral_mismatch = float(np.linalg.norm(
        edge_reference_spectrum - physical_spectrum
    ))
    assert physical_rank == 20
    assert abs(spectral_mismatch - 4.0) < 1.0e-10

    # Normalized traces erase a uniform representation multiplicity:
    # Tr_{nk}(X tensor I_k)/(nk)=Tr_n(X)/n.
    normalized_multiplicity_examples = []
    rng = np.random.default_rng(20260828)
    for dimension, multiplicity in ((3, 2), (5, 4), (11, 3)):
        matrix = rng.normal(size=(dimension, dimension))
        lifted = np.kron(matrix, np.eye(multiplicity))
        residual = abs(
            np.trace(lifted) / (dimension * multiplicity)
            - np.trace(matrix) / dimension
        )
        assert residual < 1.0e-12
        normalized_multiplicity_examples.append({
            "dimension": dimension,
            "multiplicity": multiplicity,
            "residual": float(residual),
        })

    result = {
        "gate": "version7_common_irreducible_trace_multiplicity_gate",
        "carrier_dimensions": {
            "edge_hodge_two_ended_dimension": 22,
            "physical_incidence_dimension": 21,
            "physical_source_target_dimensions": [11, 10],
            "edge_reference_rank": 22,
            "physical_gram_rank": physical_rank,
            "edge_physical_padded_spectral_mismatch": spectral_mismatch,
        },
        "simple_factor_trace": {
            "unique_normalized_trace": True,
            "uniform_representation_multiplicity_cancels": True,
            "examples": normalized_multiplicity_examples,
            "one_copy_each_gives_beta": "1",
        },
        "candidate_ratios": candidates,
        "corner_projector_test": {
            "trace_of_source_projector": "11/21",
            "trace_of_target_projector": "10/21",
            "scalar_multiplication_by_11_over_21_would_pass": True,
            "scalar_multiplication_heavy_gap": candidates[4]["heavy_gap"],
            "actual_source_corner_insertion_signature": signature(source_values),
            "actual_target_corner_insertion_signature": signature(target_values),
            "corner_insertion_equals_global_sector_rescaling": False,
        },
        "algebraic_fork": {
            "block_diagonal_algebra": "M22(C) direct_sum M21(C)",
            "block_diagonal_center_dimension": 2,
            "free_relative_trace_weights_after_normalization": 1,
            "simple_completion": "M43(C)",
            "simple_completion_offdiagonal_complex_dimension": 22 * 21,
            "simple_completion_adds_connectors": True,
        },
        "verdict": {
            "common_existing_trace_derives_allowed_beta": False,
            "dimension_resonance_11_over_21_numerically_passes": True,
            "dimension_resonance_is_currently_one_trace_operation": False,
            "rank_spectral_pairing_available": False,
            "status": "simple_trace_multiplicity_no_go_incidence_transfer_weight_open",
            "next_gate": "version7_incidence_transfer_markov_weight_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()