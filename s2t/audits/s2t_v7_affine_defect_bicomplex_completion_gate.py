#!/usr/bin/env python3
"""Audit whether the apparent 12-dimensional carrier defect is affine."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import block_diag

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_affine_physical_module_canonical_lift_gate import (
    PERMUTATIONS,
    TRIPLET_REPS,
    eaff_invariant_projector,
)
from s2t_v7_common_chain_number_hodge_relative_trace_gate import (
    chain_number_curvature,
)
from s2t_v7_derived_relative_involution_curvature_norm_gate import physical_blocks
from s2t_v7_incidence_transfer_markov_weight_gate import polar_coisometry


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_affine_defect_bicomplex_completion_gate_results.json"
TOL = 1.0e-10


def cycle_type(permutation: tuple[int, ...]) -> tuple[int, ...]:
    seen = set()
    lengths = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            current = permutation[current]
            length += 1
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def eaff_representations() -> list[np.ndarray]:
    representations = []
    for permutation_matrix, triplet in zip(PERMUTATIONS, TRIPLET_REPS):
        matrix = np.zeros((12, 12), dtype=float)
        for column in range(12):
            field = np.zeros((3, 4), dtype=float)
            field.flat[column] = 1.0
            matrix[:, column] = (
                triplet @ field @ permutation_matrix.T
            ).ravel()
        representations.append(matrix)
    return representations


def main() -> None:
    reference, variations, _, _ = physical_blocks()
    transfer, _, _ = polar_coisometry(reference)
    source = reference.shape[1]
    target = reference.shape[0]
    middle = source + target
    chain_dimension = source + middle + target
    endpoint_indices = np.concatenate([
        np.arange(source), np.arange(source + middle, chain_dimension)
    ])

    rng = np.random.default_rng(20260828)
    maximum_middle_block_residual = 0.0
    maximum_compression_trace_residual = 0.0
    maximum_padding_trace_residual = 0.0
    maximum_full_rank = 0
    maximum_compressed_rank = 0
    padding_dimensions = set()
    for _ in range(100):
        vector = rng.normal(size=len(variations))
        field = sum(
            coefficient * variation
            for coefficient, variation in zip(vector, variations)
        )
        curvature = chain_number_curvature(field, reference, transfer)
        middle_slice = slice(source, source + middle)
        maximum_middle_block_residual = max(
            maximum_middle_block_residual,
            float(np.linalg.norm(curvature[middle_slice, :])),
            float(np.linalg.norm(curvature[:, middle_slice])),
        )
        compressed = curvature[np.ix_(endpoint_indices, endpoint_indices)]
        full_trace = float(0.5 * np.trace(curvature @ curvature).real)
        compressed_trace = float(0.5 * np.trace(compressed @ compressed).real)
        maximum_compression_trace_residual = max(
            maximum_compression_trace_residual,
            abs(full_trace - compressed_trace),
        )
        maximum_full_rank = max(
            maximum_full_rank, int(np.linalg.matrix_rank(curvature, tol=TOL))
        )
        maximum_compressed_rank = max(
            maximum_compressed_rank,
            int(np.linalg.matrix_rank(compressed, tol=TOL)),
        )
        for padding in (0, 12, 37):
            padded = block_diag(curvature, np.zeros((padding, padding)))
            padded_trace = float(0.5 * np.trace(padded @ padded).real)
            maximum_padding_trace_residual = max(
                maximum_padding_trace_residual, abs(padded_trace - full_trace)
            )
            padding_dimensions.add(int(padded.shape[0]))

    representations = eaff_representations()
    invariant_projector = eaff_invariant_projector()
    invariant_rank = int(np.linalg.matrix_rank(invariant_projector, tol=TOL))

    character_table = {
        "trivial": {(1, 1, 1, 1): 1, (2, 1, 1): 1, (2, 2): 1, (3, 1): 1, (4,): 1},
        "sign": {(1, 1, 1, 1): 1, (2, 1, 1): -1, (2, 2): 1, (3, 1): 1, (4,): -1},
        "standard_3": {(1, 1, 1, 1): 3, (2, 1, 1): 1, (2, 2): -1, (3, 1): 0, (4,): -1},
        "standard_3_sign": {(1, 1, 1, 1): 3, (2, 1, 1): -1, (2, 2): -1, (3, 1): 0, (4,): 1},
        "irreducible_2": {(1, 1, 1, 1): 2, (2, 1, 1): 0, (2, 2): 2, (3, 1): -1, (4,): 0},
    }
    decomposition = {}
    for name, characters in character_table.items():
        multiplicity = 0.0
        for permutation, representation in zip(PERMUTATIONS, representations):
            permutation_tuple = tuple(np.argmax(permutation, axis=0).tolist())
            multiplicity += (
                np.trace(representation).real
                * characters[cycle_type(permutation_tuple)]
            )
        decomposition[name] = int(round(multiplicity / len(representations)))

    maximum_trivial_target_intertwiner_rank = 0
    maximum_intertwiner_residual = 0.0
    for _ in range(50):
        raw_map = rng.normal(size=(12, 12))
        equivariant_map = sum(raw_map @ representation for representation in representations)
        equivariant_map /= len(representations)
        maximum_trivial_target_intertwiner_rank = max(
            maximum_trivial_target_intertwiner_rank,
            int(np.linalg.matrix_rank(equivariant_map, tol=TOL)),
        )
        maximum_intertwiner_residual = max(
            maximum_intertwiner_residual,
            max(float(np.linalg.norm(equivariant_map @ representation - equivariant_map))
                for representation in representations),
        )

    edge_curvature_dimension = 54
    apparent_chain_dimension = chain_dimension
    minimal_endpoint_carrier_dimension = len(endpoint_indices)
    apparent_difference = edge_curvature_dimension - apparent_chain_dimension
    support_difference = edge_curvature_dimension - minimal_endpoint_carrier_dimension
    grassmannian_real_dimension = 2 * apparent_chain_dimension * apparent_difference

    assert chain_dimension == 42
    assert middle == 21
    assert minimal_endpoint_carrier_dimension == 21
    assert maximum_middle_block_residual < TOL
    assert maximum_compression_trace_residual < TOL
    assert maximum_padding_trace_residual < TOL
    assert maximum_full_rank == maximum_compressed_rank == 14
    assert sorted(padding_dimensions) == [42, 54, 79]
    assert invariant_rank == 1
    assert decomposition == {
        "trivial": 1,
        "sign": 0,
        "standard_3": 2,
        "standard_3_sign": 1,
        "irreducible_2": 1,
    }
    assert maximum_trivial_target_intertwiner_rank == 1
    assert maximum_intertwiner_residual < TOL
    assert apparent_difference == 12
    assert support_difference == 33

    result = {
        "gate": "version7_affine_defect_bicomplex_completion_gate",
        "linking_curvature_support": {
            "full_chain_dimension": chain_dimension,
            "source_dimension": source,
            "middle_dimension": middle,
            "target_dimension": target,
            "middle_block_identically_zero": True,
            "maximum_middle_block_residual": maximum_middle_block_residual,
            "minimal_endpoint_carrier_dimension": minimal_endpoint_carrier_dimension,
            "maximum_full_curvature_rank": maximum_full_rank,
            "maximum_compressed_curvature_rank": maximum_compressed_rank,
            "maximum_trace_compression_residual": maximum_compression_trace_residual,
        },
        "zero_padding_noninvariance": {
            "tested_ambient_dimensions": sorted(padding_dimensions),
            "maximum_trace_residual": maximum_padding_trace_residual,
            "action_unchanged_by_zero_padding": True,
            "edge_minus_full_chain_dimension": apparent_difference,
            "edge_minus_minimal_support_dimension": support_difference,
            "twelve_dimensional_difference_is_carrier_invariant": False,
        },
        "affine_representation": {
            "complex_dimension": 12,
            "S4_irreducible_multiplicities": decomposition,
            "invariant_subspace_dimension": invariant_rank,
            "maximum_rank_of_map_to_undefined_or_trivial_defect_action": (
                maximum_trivial_target_intertwiner_rank
            ),
            "maximum_intertwiner_residual": maximum_intertwiner_residual,
            "equivariant_isomorphism_from_dimension_alone": False,
        },
        "arbitrary_embedding_cost": {
            "complex_grassmannian": "Gr(42,54)",
            "real_dimension": grassmannian_real_dimension,
            "defect_subspace_canonical_without_extra_symmetry": False,
        },
        "verdict": {
            "affine_defect_completion_derived": False,
            "dimension_match_12_is_zero_padding_artifact": True,
            "E_aff_identification_rejected": True,
            "qualitative_common_action_affected": False,
            "mass_ratios_derived": False,
            "status": "affine_defect_completion_no_go_minimal_curvature_support_open",
            "next_gate": "version7_minimal_curvature_support_trace_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()