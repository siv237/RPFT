#!/usr/bin/env python3
"""Audit the quantum Markov semigroup canonically induced by linking incidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh, expm


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_linking_dirichlet_quantum_markov_semigroup_gate_results.json"
TOL = 1.0e-10

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import physical_blocks


def block_generator(incidence: np.ndarray) -> np.ndarray:
    """Matrix of L on M_source direct-sum M_target in column vectorization."""
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
    target_to_source = np.kron(incidence.T, incidence.conj().T)
    source_to_target = np.kron(incidence.conj(), incidence)
    return np.block(
        [[source_diagonal, target_to_source], [source_to_target, target_diagonal]]
    )


def apply_generator(incidence: np.ndarray, source: np.ndarray, target: np.ndarray):
    source_gram = incidence.conj().T @ incidence
    target_gram = incidence @ incidence.conj().T
    source_image = (
        incidence.conj().T @ target @ incidence
        - 0.5 * (source_gram @ source + source @ source_gram)
    )
    target_image = (
        incidence @ source @ incidence.conj().T
        - 0.5 * (target_gram @ target + target @ target_gram)
    )
    return source_image, target_image


incidence, _, _, _ = physical_blocks()
target_dimension, source_dimension = incidence.shape
assert (target_dimension, source_dimension) == (10, 11)

linking_dirac = np.block(
    [
        [np.zeros((source_dimension, source_dimension)), incidence.conj().T],
        [incidence, np.zeros((target_dimension, target_dimension))],
    ]
)
generator = block_generator(incidence)
generator_values = eigvalsh(generator)

identity_vector = np.concatenate(
    [
        np.eye(source_dimension).reshape(-1, order="F"),
        np.eye(target_dimension).reshape(-1, order="F"),
    ]
)
unital_residual = float(np.linalg.norm(generator @ identity_vector))
trace_residual = float(np.linalg.norm(identity_vector.conj() @ generator))
self_adjoint_residual = float(np.linalg.norm(generator - generator.conj().T))
fixed_dimension = int(np.sum(np.abs(generator_values) < TOL))
positive_generator_eigenvalues = int(np.sum(generator_values > TOL))
decay_gap = float(-generator_values[-fixed_dimension - 1])

singular_values = np.linalg.svd(incidence, compute_uv=False)
rounded_singular_values = np.round(singular_values, 10)
unique, multiplicities = np.unique(rounded_singular_values, return_counts=True)
predicted_fixed_dimension = 1 + int(np.sum(multiplicities**2))

assert fixed_dimension == predicted_fixed_dimension == 41
assert positive_generator_eigenvalues == 0
assert unital_residual < 1.0e-12
assert trace_residual < 1.0e-12
assert self_adjoint_residual < 1.0e-12
assert decay_gap > 0.0

# For L=-ad_D^2/2, exp(tL) is a Schur multiplier in the D-eigenbasis by the
# positive Gaussian matrix exp(-t(lambda_i-lambda_j)^2/2).  Positivity of
# this multiplier matrix is the finite complete-positivity certificate.
dirac_values = eigvalsh(linking_dirac)
semigroup_tests = []
for time in (0.1, 1.0, 10.0):
    differences = dirac_values[:, None] - dirac_values[None, :]
    gaussian_multiplier = np.exp(-0.5 * time * differences**2)
    multiplier_minimum = float(eigvalsh(gaussian_multiplier)[0])
    channel = expm(time * generator)
    channel_unital_residual = float(np.linalg.norm(channel @ identity_vector - identity_vector))
    source_target_transfer_norm = float(
        np.linalg.norm(channel[: source_dimension**2, source_dimension**2 :], ord="fro")
    )
    assert multiplier_minimum > -1.0e-9
    assert channel_unital_residual < 1.0e-11
    assert source_target_transfer_norm > 1.0e-3
    semigroup_tests.append(
        {
            "time": time,
            "gaussian_cp_multiplier_minimum_eigenvalue": multiplier_minimum,
            "channel_unital_residual": channel_unital_residual,
            "target_to_source_transfer_frobenius_norm": source_target_transfer_norm,
        }
    )

semigroup_composition_error = float(
    np.linalg.norm(expm(0.4 * generator) @ expm(0.7 * generator) - expm(1.1 * generator))
)
assert semigroup_composition_error < 1.0e-11

# Covariance under independent changes of source and target frames.
rng = np.random.default_rng(20260828)
source_seed = rng.normal(size=(source_dimension, source_dimension)) + 1j * rng.normal(
    size=(source_dimension, source_dimension)
)
target_seed = rng.normal(size=(target_dimension, target_dimension)) + 1j * rng.normal(
    size=(target_dimension, target_dimension)
)
source_unitary, _ = np.linalg.qr(source_seed)
target_unitary, _ = np.linalg.qr(target_seed)
transformed_incidence = target_unitary @ incidence @ source_unitary.conj().T

source_observable = rng.normal(size=(source_dimension, source_dimension)) + 1j * rng.normal(
    size=(source_dimension, source_dimension)
)
target_observable = rng.normal(size=(target_dimension, target_dimension)) + 1j * rng.normal(
    size=(target_dimension, target_dimension)
)
source_observable = source_observable + source_observable.conj().T
target_observable = target_observable + target_observable.conj().T
source_image, target_image = apply_generator(incidence, source_observable, target_observable)
transformed_source_image, transformed_target_image = apply_generator(
    transformed_incidence,
    source_unitary @ source_observable @ source_unitary.conj().T,
    target_unitary @ target_observable @ target_unitary.conj().T,
)
covariance_error = float(
    np.linalg.norm(
        transformed_source_image - source_unitary @ source_image @ source_unitary.conj().T
    )
    + np.linalg.norm(
        transformed_target_image - target_unitary @ target_image @ target_unitary.conj().T
    )
)
assert covariance_error < 1.0e-10

required_sources = {
    "transition_observable_corners": "s2t/gates/version5_transition_primitive_scientific_language_gate.tex",
    "physical_incidence": "s2t/gates/version7_derived_relative_involution_curvature_norm_gate.tex",
    "markov_weight": "s2t/gates/version7_incidence_transfer_markov_weight_gate.tex",
    "full_kernel_reopening": "s2t/gates/version8_full_correlation_kernel_locality_reconstruction_gate.tex",
}
source_presence = {key: (ROOT / value).exists() for key, value in required_sources.items()}
assert all(source_presence.values())

result = {
    "date": "2026-08-28",
    "gate": "version8_linking_dirichlet_quantum_markov_semigroup_gate",
    "source_presence": source_presence,
    "derived_observable_algebra": {
        "algebra": "M_11(C) direct_sum M_10(C)",
        "origin": "endpoint corners E*E and EE* of the physical transition bimodule",
        "commutative_coordinate_algebra": False,
        "assigned_minimal_diagonal_basis": False,
    },
    "linking_data": {
        "incidence_shape": [target_dimension, source_dimension],
        "incidence_rank": int(np.linalg.matrix_rank(incidence, TOL)),
        "linking_dirac_dimension": int(linking_dirac.shape[0]),
        "singular_values": [float(value) for value in singular_values],
    },
    "quantum_markov_generator": {
        "formula": "L(X)=-1/2 [D,[D,X]]",
        "corner_formula": "(A*YA-{A*A,X}/2, AXA*-{AA*,Y}/2)",
        "matrix_dimension": int(generator.shape[0]),
        "self_adjoint_residual": self_adjoint_residual,
        "unital_residual": unital_residual,
        "trace_preserving_residual": trace_residual,
        "positive_eigenvalue_count": positive_generator_eigenvalues,
        "semigroup_composition_error": semigroup_composition_error,
        "basis_covariance_error": covariance_error,
        "tests": semigroup_tests,
    },
    "fixed_algebra": {
        "dimension": fixed_dimension,
        "predicted_from_singular_multiplicities": predicted_fixed_dimension,
        "incidence_kernel_contribution": 1,
        "sixfold_unit_singular_value_contribution": 36,
        "remaining_simple_singular_value_contribution": 4,
        "decay_gap_above_fixed_algebra": decay_gap,
        "unique_stationary_observable": False,
        "primitive_semigroup": False,
    },
    "verdict": {
        "endpoint_observable_algebra_derived": True,
        "coefficient_free_quantum_markov_semigroup_derived": True,
        "nonzero_bidirectional_corner_transfer": True,
        "classical_event_algebra_derived": False,
        "locality_selector_derived": False,
        "physical_parent_action_closed": False,
        "status": "positive_noncommutative_semigroup_fixed_algebra_degeneracy_open",
        "reason": (
            "the linking incidence canonically generates a symmetric unital trace-preserving "
            "quantum Markov semigroup, but its 41-dimensional fixed algebra retains a large "
            "multiplicity and does not select a classical diagonal event algebra"
        ),
    },
    "next_gate": {
        "name": "version8_markov_fixed_algebra_selector_gate",
        "question": (
            "can already-derived gauge, Hodge and affine operators reduce the 41-dimensional "
            "fixed algebra without choosing a maximal abelian subalgebra by hand?"
        ),
    },
}

payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
OUTPUT.write_text(payload, encoding="utf-8")
print(OUTPUT)
print(hashlib.sha256(payload.encode("utf-8")).hexdigest())