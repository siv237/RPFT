#!/usr/bin/env python3
"""Ранг-один угловое чтение уже выведенной семейной кривизны."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_state_corner_curvature_readout_gate_results.json"
TOL = 1.0e-10


def choi_matrix(linear_map, size):
    result = np.zeros((size * size, size * size), dtype=complex)
    for row in range(size):
        for column in range(size):
            unit = np.zeros((size, size), dtype=complex)
            unit[row, column] = 1.0
            result += np.kron(unit, linear_map(unit))
    return result


rank_one = json.loads(
    (ROOT / "s2t/results/s2t_v5_rank_one_tangent_junk_gate_results.json")
    .read_text(encoding="utf-8")
)
square = json.loads(
    (ROOT / "s2t/results/s2t_v5_commuting_square_readout_gate_results.json")
    .read_text(encoding="utf-8")
)
sm = json.loads(
    (ROOT / "s2t/results/s2t_v5_sm_linking_corner_gate_results.json")
    .read_text(encoding="utf-8")
)
measure = json.loads(
    (ROOT / "s2t/results/s2t_multi_trace_measure_hypothesis_results.json")
    .read_text(encoding="utf-8")
)
parent_trace = json.loads(
    (ROOT / "s2t/results/s2t_parent_trace_tensor_product_results.json")
    .read_text(encoding="utf-8")
)

assert rank_one["structural_result"]["degree_two_quotient"] == "C rho"
assert square["verdict"]["two_readings_one_parent_trace"] == "pass"
assert sm["verdict"]["exact_SM_block_reading_in_square"] == "pass"
assert measure["gates"]["one_parent_trace_with_projectors"]["passes"]
assert parent_trace["joint_consistency"]["relative_trace_parameter_count"] == 0

rho = np.diag([1.0, 0.0, 0.0]).astype(complex)
identity3 = np.eye(3, dtype=complex)
identity15 = np.eye(15, dtype=complex)
parent_projector = np.kron(rho, identity15)


def corner_compression(matrix):
    return rho @ matrix @ rho


corner_choi_eigenvalues = np.linalg.eigvalsh(choi_matrix(corner_compression, 3))
assert np.min(corner_choi_eigenvalues) > -TOL
assert np.linalg.norm(corner_compression(identity3) - rho) < TOL


def parent_corner_compression(matrix):
    return parent_projector @ matrix @ parent_projector


def family_partial_trace(matrix):
    result = np.zeros((3, 3), dtype=complex)
    for row in range(3):
        for column in range(3):
            block = matrix[row * 15 : (row + 1) * 15, column * 15 : (column + 1) * 15]
            result[row, column] = np.trace(block) / 15.0
    return result


block_sizes = [6, 2, 3, 3, 1]
observed_projectors = []
offset = 0
for size in block_sizes:
    projector = np.zeros((15, 15), dtype=complex)
    projector[offset : offset + size, offset : offset + size] = np.eye(size)
    observed_projectors.append(projector)
    offset += size


def observed_block_expectation(matrix):
    return sum(projector @ matrix @ projector for projector in observed_projectors)


def parent_observed_block_expectation(matrix):
    result = np.zeros_like(matrix)
    for projector in observed_projectors:
        lifted = np.kron(identity3, projector)
        result += lifted @ matrix @ lifted
    return result


def conditioned_observed_reading(matrix):
    compressed = parent_corner_compression(matrix)
    return compressed[:15, :15]


rng = np.random.default_rng(20260816)
raw = rng.normal(size=(45, 45)) + 1j * rng.normal(size=(45, 45))
test = raw + raw.conj().T

commutation_residuals = {
    "corner_with_family_partial_trace": float(
        np.linalg.norm(
            corner_compression(family_partial_trace(test))
            - family_partial_trace(parent_corner_compression(test))
        )
    ),
    "corner_with_exact_SM_block_reading": float(
        np.linalg.norm(
            parent_corner_compression(parent_observed_block_expectation(test))
            - parent_observed_block_expectation(parent_corner_compression(test))
        )
    ),
    "conditioned_observed_with_SM_block_reading": float(
        np.linalg.norm(
            conditioned_observed_reading(parent_observed_block_expectation(test))
            - observed_block_expectation(conditioned_observed_reading(test))
        )
    ),
}
assert max(commutation_residuals.values()) < TOL

samples = []
for radial, phi in [(1.0, 1.0), (np.sqrt(5.0 / 6.0), np.sqrt(2.0 / 3.0)), (0.73, 0.41 + 0.27j)]:
    moment = float(radial**2 - abs(phi) ** 2)
    full_curvature = moment * identity3
    corner_curvature = corner_compression(full_curvature)
    lifted_full = np.kron(full_curvature, identity15)
    lifted_corner = parent_corner_compression(lifted_full)

    family_normalized_norm = float(np.trace(full_curvature.conj().T @ full_curvature).real / 3.0)
    corner_normalized_norm = float(
        np.trace(corner_curvature.conj().T @ corner_curvature).real / np.trace(rho).real
    )
    parent_loop_norm = float(
        np.trace(lifted_corner.conj().T @ lifted_corner).real / 45.0
    )
    parent_conditioned_norm = float(
        np.trace(lifted_corner.conj().T @ lifted_corner).real
        / np.trace(parent_projector).real
    )

    assert np.linalg.norm(corner_curvature - moment * rho) < TOL
    assert abs(family_normalized_norm - moment**2) < TOL
    assert abs(corner_normalized_norm - moment**2) < TOL
    assert abs(parent_conditioned_norm - moment**2) < TOL
    assert abs(parent_loop_norm - moment**2 / 3.0) < TOL

    samples.append(
        {
            "radial": float(radial),
            "phi": [float(np.real(phi)), float(np.imag(phi))],
            "moment": moment,
            "family_normalized_curvature_norm": family_normalized_norm,
            "corner_normalized_curvature_norm": corner_normalized_norm,
            "parent_loop_curvature_norm": parent_loop_norm,
            "parent_conditioned_curvature_norm": parent_conditioned_norm,
        }
    )

# Базисная ковариантность компрессии.
raw_unitary = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
unitary, _ = np.linalg.qr(raw_unitary)
rotated_rho = unitary @ rho @ unitary.conj().T
matrix = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
rotated_compression = rotated_rho @ (unitary @ matrix @ unitary.conj().T) @ rotated_rho
covariance_residual = float(
    np.linalg.norm(rotated_compression - unitary @ corner_compression(matrix) @ unitary.conj().T)
)
assert covariance_residual < TOL

result = {
    "gate": "version5_state_corner_curvature_readout_gate",
    "input_ledger": {
        "modular_or_Hodge_moment_curvature": "already derived before this gate",
        "equivariant_middle_curvature": "mu I3 with mu=radial^2-|Phi|^2",
        "rank_one_degree_two_quotient": "C rho",
        "exact_observed_block": "6+2+3+3+1=15",
        "measure_rule": "one parent trace with observable-type reductions",
    },
    "corner_map": {
        "formula": "C_rho(A)=rho A rho",
        "global_unital": False,
        "corner_unital": True,
        "idempotent": True,
        "completely_positive": True,
        "Choi_eigenvalues": corner_choi_eigenvalues.tolist(),
        "basis_covariance_residual": covariance_residual,
        "range": "C rho for rank-one rho",
    },
    "parent_corner": {
        "space": "C3_family tensor C15_observed",
        "parent_dimension": 45,
        "projector": "rho tensor I15",
        "projector_rank": int(np.linalg.matrix_rank(parent_projector)),
        "rank_fraction": float(np.trace(parent_projector).real / 45.0),
        "relative_trace_parameter_count": 0,
    },
    "commuting_readouts": commutation_residuals,
    "curvature_samples": samples,
    "interpretation": {
        "family_loop_reading": "tau3((mu I3)^2)=mu^2",
        "state_corner_reading": "Tr_rho((mu rho)^2)/Tr(rho)=mu^2",
        "parent_loop_reading": "tau45((rho tensor I15)(mu^2 I45))=mu^2/3",
        "fixed_multiplicity_factor": "rank(rho)/3=1/3",
        "normalization_switch": False,
        "different_observable_types": True,
        "full_curvature_reconstructed_from_corner": False,
    },
    "verdict": {
        "full_to_rank_one_curvature_readout": "pass",
        "normalized_curvature_norm_preserved": "pass",
        "one_parent_trace_no_free_weight": "pass",
        "compatibility_with_exact_SM_block_reading": "pass",
        "rank_one_quotient_as_controlled_readout": "pass",
        "new_origin_of_full_moment_map": "not_claimed",
        "off_diagonal_Yukawa_dynamics": "open",
        "two_sided_bimodule_connection_needed_for_scalar_transfer": False,
        "two_sided_bimodule_connection_needed_for_interaction_dynamics": True,
        "physical_closure": False,
        "status": (
            "the one-dimensional quotient is the correct normalized state-corner "
            "readout of the already derived equivariant family curvature"
        ),
    },
    "next_gate": (
        "Construct the two-sided connection only on the off-diagonal interaction "
        "bimodule, keeping curvature transfer fixed by the state-corner square; test "
        "Leibniz rules, KO6, exact SM covariance and the Yukawa Hessian."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))