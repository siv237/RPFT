#!/usr/bin/env python3
"""Reduce the linking Markov fixed algebra by already-derived gauge data."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_markov_fixed_algebra_selector_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import physical_blocks


def block_generator(incidence: np.ndarray) -> np.ndarray:
    target_dimension, source_dimension = incidence.shape
    source_gram = incidence.conj().T @ incidence
    target_gram = incidence @ incidence.conj().T
    source_diagonal = (
        -0.5 * np.kron(np.eye(source_dimension), source_gram)
        -0.5 * np.kron(source_gram.T, np.eye(source_dimension))
    )
    target_diagonal = (
        -0.5 * np.kron(np.eye(target_dimension), target_gram)
        -0.5 * np.kron(target_gram.T, np.eye(target_dimension))
    )
    return np.block(
        [
            [source_diagonal, np.kron(incidence.T, incidence.conj().T)],
            [np.kron(incidence.conj(), incidence), target_diagonal],
        ]
    )


def block_diagonal(blocks):
    dimension = sum(block.shape[0] for block in blocks)
    matrix = np.zeros((dimension, dimension), dtype=complex)
    offset = 0
    for block in blocks:
        size = block.shape[0]
        matrix[offset : offset + size, offset : offset + size] = block
        offset += size
    return matrix


def dissipator(operator):
    dimension = operator.shape[0]
    square = operator @ operator
    return (
        np.kron(operator.T, operator)
        - 0.5 * np.kron(np.eye(dimension), square)
        - 0.5 * np.kron(square.T, np.eye(dimension))
    )


def gell_mann_matrices():
    matrices = []

    def matrix(entries):
        result = np.zeros((3, 3), dtype=complex)
        for row, column, value in entries:
            result[row, column] = value
        return result

    matrices.extend(
        [
            matrix(((0, 1, 1), (1, 0, 1))),
            matrix(((0, 1, -1j), (1, 0, 1j))),
            matrix(((0, 0, 1), (1, 1, -1))),
            matrix(((0, 2, 1), (2, 0, 1))),
            matrix(((0, 2, -1j), (2, 0, 1j))),
            matrix(((1, 2, 1), (2, 1, 1))),
            matrix(((1, 2, -1j), (2, 1, 1j))),
            np.diag([1.0, 1.0, -2.0]) / np.sqrt(3.0),
        ]
    )
    return matrices


pauli = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]

source_su3 = []
target_su3 = []
for matrix in gell_mann_matrices():
    source_su3.append(
        block_diagonal(
            [
                np.kron(matrix / 2.0, np.eye(2)),
                np.zeros((2, 2)),
                np.zeros((1, 1)),
                np.zeros((2, 2)),
            ]
        )
    )
    target_su3.append(
        block_diagonal(
            [
                matrix / 2.0,
                matrix / 2.0,
                np.zeros((1, 1)),
                np.zeros((1, 1)),
                np.zeros((2, 2)),
            ]
        )
    )

source_su2 = []
target_su2 = []
for matrix in pauli:
    source_su2.append(
        block_diagonal(
            [
                np.kron(np.eye(3), matrix / 2.0),
                matrix / 2.0,
                np.zeros((1, 1)),
                matrix / 2.0,
            ]
        )
    )
    target_su2.append(
        block_diagonal(
            [
                np.zeros((3, 3)),
                np.zeros((3, 3)),
                np.zeros((1, 1)),
                np.zeros((1, 1)),
                matrix / 2.0,
            ]
        )
    )

source_hypercharge = block_diagonal(
    [
        np.eye(6) / 6.0,
        -np.eye(2) / 2.0,
        -np.eye(1),
        -np.eye(2) / 2.0,
    ]
)
target_hypercharge = block_diagonal(
    [
        2.0 * np.eye(3) / 3.0,
        -np.eye(3) / 3.0,
        -np.eye(1),
        -np.eye(1),
        -np.eye(2) / 2.0,
    ]
)


def corner_dissipator(source_operator, target_operator):
    source_size = source_operator.shape[0] ** 2
    target_size = target_operator.shape[0] ** 2
    return np.block(
        [
            [dissipator(source_operator), np.zeros((source_size, target_size))],
            [np.zeros((target_size, source_size)), dissipator(target_operator)],
        ]
    )


incidence, _, _, _ = physical_blocks()
base_generator = block_generator(incidence)
su3_generator = sum(
    (corner_dissipator(source, target) for source, target in zip(source_su3, target_su3)),
    np.zeros_like(base_generator),
)
su2_generator = sum(
    (corner_dissipator(source, target) for source, target in zip(source_su2, target_su2)),
    np.zeros_like(base_generator),
)
hypercharge_generator = corner_dissipator(source_hypercharge, target_hypercharge)


def kernel_dimension(matrix):
    values = eigvalsh(matrix)
    return int(np.sum(np.abs(values) < TOL)), values


named_reductions = {}
variants = {
    "linking_only": base_generator,
    "linking_plus_hypercharge": base_generator + hypercharge_generator,
    "linking_plus_su2": base_generator + su2_generator,
    "linking_plus_su3": base_generator + su3_generator,
    "linking_plus_su3_plus_hypercharge": base_generator + su3_generator + hypercharge_generator,
    "linking_plus_full_gauge": base_generator + su3_generator + su2_generator + hypercharge_generator,
}
for name, matrix in variants.items():
    dimension, values = kernel_dimension(matrix)
    named_reductions[name] = {
        "fixed_dimension": dimension,
        "positive_eigenvalue_count": int(np.sum(values > TOL)),
        "decay_gap": float(-values[-dimension - 1]),
    }
    assert np.sum(values > TOL) == 0

assert {key: value["fixed_dimension"] for key, value in named_reductions.items()} == {
    "linking_only": 41,
    "linking_plus_hypercharge": 21,
    "linking_plus_su2": 10,
    "linking_plus_su3": 9,
    "linking_plus_su3_plus_hypercharge": 5,
    "linking_plus_full_gauge": 2,
}

source_dimension = 11
target_dimension = 10
quark_source = np.diag([1.0] * 6 + [0.0] * 5)
quark_target = np.diag([1.0] * 6 + [0.0] * 4)
lepton_source = np.eye(source_dimension) - quark_source
lepton_target = np.eye(target_dimension) - quark_target


def pair_vector(source, target):
    return np.concatenate(
        [source.reshape(-1, order="F"), target.reshape(-1, order="F")]
    )


full_generator = variants["linking_plus_full_gauge"]
quark_vector = pair_vector(quark_source, quark_target)
lepton_vector = pair_vector(lepton_source, lepton_target)
quark_fixed_residual = float(np.linalg.norm(full_generator @ quark_vector))
lepton_fixed_residual = float(np.linalg.norm(full_generator @ lepton_vector))
orthogonality = float(abs(np.vdot(quark_vector, lepton_vector)))
assert quark_fixed_residual < 1.0e-12
assert lepton_fixed_residual < 1.0e-12
assert orthogonality < 1.0e-12
assert int(np.trace(quark_source) + np.trace(quark_target)) == 12
assert int(np.trace(lepton_source) + np.trace(lepton_target)) == 9

# The kernel depends only on which positive Dirichlet summands are present,
# not on their relative positive weights.
rng = np.random.default_rng(20260828)
weight_scan = []
for _ in range(64):
    weights = 10.0 ** rng.uniform(-4.0, 4.0, size=4)
    candidate = (
        weights[0] * base_generator
        + weights[1] * su3_generator
        + weights[2] * su2_generator
        + weights[3] * hypercharge_generator
    )
    dimension, values = kernel_dimension(candidate)
    assert dimension == 2
    assert np.sum(values > 1.0e-7) == 0
    weight_scan.append(
        {
            "weights_linking_su3_su2_u1": [float(value) for value in weights],
            "fixed_dimension": dimension,
            "decay_gap": float(-values[-dimension - 1]),
        }
    )

# Endpoint grading is scalar on each corner and its double commutator
# vanishes identically on the endpoint observable algebra.
endpoint_grading_source = np.eye(source_dimension)
endpoint_grading_target = -np.eye(target_dimension)
grading_generator = corner_dissipator(endpoint_grading_source, endpoint_grading_target)
grading_generator_norm = float(np.linalg.norm(grading_generator))
assert grading_generator_norm == 0.0

required_sources = {
    "linking_semigroup": "s2t/gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex",
    "gauge_carrier": "s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex",
    "physical_incidence": "s2t/gates/version7_derived_relative_involution_curvature_norm_gate.tex",
    "universal_incidence_no_go": "s2t/gates/version7_universal_incidence_parent_admissibility_gate.tex",
}
source_presence = {key: (ROOT / value).exists() for key, value in required_sources.items()}
assert all(source_presence.values())

result = {
    "date": "2026-08-28",
    "gate": "version8_markov_fixed_algebra_selector_gate",
    "source_presence": source_presence,
    "gauge_representations": {
        "source_order": "QL(6), LL(2), XL(1), YL(2)",
        "target_order": "uR(3), dR(3), eR(1), XR(1), YR(2)",
        "su3_generators": 8,
        "su2_generators": 3,
        "u1_generators": 1,
    },
    "fixed_algebra_reduction": named_reductions,
    "final_fixed_algebra": {
        "algebra": "C P_quark direct_sum C P_lepton_vectorlike",
        "dimension": 2,
        "quark_projector_rank": 12,
        "lepton_vectorlike_projector_rank": 9,
        "quark_fixed_residual": quark_fixed_residual,
        "lepton_vectorlike_fixed_residual": lepton_fixed_residual,
        "projector_orthogonality": orthogonality,
        "incidence_cross_component_blocks": 0,
    },
    "robustness": {
        "positive_weight_samples": len(weight_scan),
        "weight_range": "1e-4 through 1e4 independently for linking, SU3, SU2, U1",
        "fixed_dimension_always_two": True,
        "samples": weight_scan,
        "endpoint_grading_generator_norm": grading_generator_norm,
        "affine_factor_action_on_endpoint_internal_space": "identity, hence no further reduction",
    },
    "verdict": {
        "full_gauge_data_reduce_fixed_algebra": True,
        "canonical_commutative_sector_algebra_derived": True,
        "sector_algebra_dimension": 2,
        "minimal_state_event_algebra_derived": False,
        "unified_primitive_semigroup_derived": False,
        "quark_lepton_connector_present": False,
        "status": "canonical_two_sector_event_algebra_and_disconnection_witness",
        "reason": (
            "the joint commutant of linking incidence and the complete gauge representation "
            "is exactly C^2, selecting colored and colorless connected components while "
            "proving that the present transition graph contains no operator between them"
        ),
    },
    "next_gate": {
        "name": "version8_two_sector_kernel_self_consistency_gate",
        "question": (
            "can the full correlation kernel dynamically generate a color-preserving composite "
            "bridge between the two central sectors, or is C^2 a strict superselection boundary?"
        ),
    },
}

payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
OUTPUT.write_text(payload, encoding="utf-8")
print(OUTPUT)
print(hashlib.sha256(payload.encode("utf-8")).hexdigest())