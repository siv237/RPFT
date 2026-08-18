#!/usr/bin/env python3
"""Точное наблюдаемое чтение и проверка юкавской проекции на положительность."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_sm_linking_corner_gate_results.json"
TOL = 1.0e-10

square = json.loads(
    (ROOT / "s2t/results/s2t_v5_commuting_square_readout_gate_results.json")
    .read_text(encoding="utf-8")
)
sm = json.loads(
    (ROOT / "s2t/results/s2t_v4_finite_algebra_menu_gate_results.json")
    .read_text(encoding="utf-8")
)
anchored = json.loads(
    (ROOT / "s2t/results/s2t_v4_state_anchored_bimodule_gate_results.json")
    .read_text(encoding="utf-8")
)
assert square["verdict"]["two_readings_one_parent_trace"] == "pass"
assert sm["selected_baseline"] == ["C", "H", "M3C"]
assert anchored["module_dimension"] == 5


def choi_matrix(linear_map, size):
    result = np.zeros((size * size, size * size), dtype=complex)
    for row in range(size):
        for column in range(size):
            unit = np.zeros((size, size), dtype=complex)
            unit[row, column] = 1.0
            result += np.kron(unit, linear_map(unit))
    return result


# Точное разложение одного поколения без nu_R.
block_sizes = [6, 2, 3, 3, 1]
block_names = ["Q_L", "L_L", "u_R", "d_R", "e_R"]
projectors = []
offset = 0
for size in block_sizes:
    projector = np.zeros((15, 15), dtype=complex)
    projector[offset : offset + size, offset : offset + size] = np.eye(size)
    projectors.append(projector)
    offset += size


def observed_block_expectation(matrix):
    return sum(projector @ matrix @ projector for projector in projectors)


rng = np.random.default_rng(20260816)
raw = rng.normal(size=(15, 15)) + 1j * rng.normal(size=(15, 15))
test = raw + raw.conj().T
observed_residuals = {
    "unital": float(np.linalg.norm(observed_block_expectation(np.eye(15)) - np.eye(15))),
    "idempotent": float(
        np.linalg.norm(
            observed_block_expectation(observed_block_expectation(test))
            - observed_block_expectation(test)
        )
    ),
    "trace_preserving": float(
        abs(np.trace(observed_block_expectation(test)) - np.trace(test))
    ),
    "star_preserving": float(
        np.linalg.norm(
            observed_block_expectation(test.conj().T)
            - observed_block_expectation(test).conj().T
        )
    ),
}
assert max(observed_residuals.values()) < TOL

# Проверка прежней state-anchored проекции Pi_rho.
rho = np.diag([1.0, 0.0, 0.0])
Q = np.eye(3) - rho


def anchored_projection(matrix):
    return matrix - Q @ matrix @ Q


positive_witness = np.ones((3, 3))
anchored_witness = anchored_projection(positive_witness)
anchored_witness_eigenvalues = np.linalg.eigvalsh(anchored_witness)
anchored_choi_eigenvalues = np.linalg.eigvalsh(choi_matrix(anchored_projection, 3))
assert np.min(anchored_witness_eigenvalues) < -0.9
assert np.min(anchored_choi_eigenvalues) < -0.9


def state_algebra_expectation(matrix):
    return rho @ matrix @ rho + np.trace(Q @ matrix @ Q) * Q / 2.0


state_choi_eigenvalues = np.linalg.eigvalsh(choi_matrix(state_algebra_expectation, 3))
state_expectation_residuals = {
    "unital": float(np.linalg.norm(state_algebra_expectation(np.eye(3)) - np.eye(3))),
    "idempotent": float(
        np.linalg.norm(
            state_algebra_expectation(state_algebra_expectation(test[:3, :3]))
            - state_algebra_expectation(test[:3, :3])
        )
    ),
    "trace_preserving": float(
        abs(np.trace(state_algebra_expectation(test[:3, :3])) - np.trace(test[:3, :3]))
    ),
    "minimum_Choi_eigenvalue": float(np.min(state_choi_eigenvalues)),
}
assert min(state_choi_eigenvalues) > -TOL
assert max(abs(value) for key, value in state_expectation_residuals.items() if key != "minimum_Choi_eigenvalue") < TOL

off_diagonal = np.zeros((3, 3), dtype=complex)
off_diagonal[0, 1] = 1.0
off_diagonal[1, 0] = 1.0
off_diagonal_erasure = np.linalg.norm(state_algebra_expectation(off_diagonal))
assert off_diagonal_erasure < TOL

result = {
    "gate": "version5_sm_linking_corner_gate",
    "exact_observed_reading": {
        "coordinate_algebra": "C+H+M3(C)",
        "gauge_lie_algebra_after_unimodularity": "su3+su2+u1",
        "gauge_lie_dimension": 12,
        "particle_bimodule_blocks": dict(zip(block_names, block_sizes)),
        "particle_dimension": sum(block_sizes),
        "block_reading_algebra": "M6+M2+M3+M3+C",
        "trace_preserving_expectation_residuals": observed_residuals,
        "compatible_with_family_factor_expectation": True,
    },
    "state_anchored_projection_reaudit": {
        "formula": "Pi_rho(X)=X-QXQ",
        "idempotent_Hilbert_Schmidt_projection": True,
        "positive_input_witness_eigenvalues": anchored_witness_eigenvalues.tolist(),
        "Choi_eigenvalues": anchored_choi_eigenvalues.tolist(),
        "positive": False,
        "completely_positive": False,
        "conditional_expectation": False,
        "previous_CP_map_wording": "retracted",
        "valid_interpretation": "orthogonal projection onto an off-diagonal operator bimodule",
    },
    "canonical_positive_state_reading": {
        "formula": "E_rho(X)=rho X rho+Tr(QXQ)Q/2",
        "target": "C rho + C Q",
        "target_complex_dimension": 2,
        "Choi_eigenvalues": state_choi_eigenvalues.tolist(),
        "residuals": state_expectation_residuals,
        "off_diagonal_connector_norm_after_reading": float(off_diagonal_erasure),
        "can_generate_Yukawa_mixing": False,
    },
    "architecture_split": {
        "diagonal_state_readings": "conditional expectations in the commuting square",
        "interaction_operators": "off-diagonal Hilbert bimodule corners",
        "appropriate_container": "linking algebra of the two readings",
        "one_map_should_do_both_jobs": False,
    },
    "verdict": {
        "exact_SM_block_reading_in_square": "pass",
        "state_anchored_projection_as_CP_readout": "fail",
        "state_anchored_projection_as_operator_bimodule_selector": "conditional_pass",
        "canonical_positive_expectation_generates_mixing": "fail",
        "linking_algebra_interaction_branch": "open",
        "physical_closure": False,
        "status": "commuting_square_handles_states_while_Yukawa_requires_off_diagonal_linking_corner",
    },
    "next_gate": (
        "Build the minimal linking algebra whose diagonal corners are the family "
        "and exact Standard Model readings and whose off-diagonal corner is the "
        "state-supported Yukawa bimodule; test closure, involution, one-trace "
        "normalization and whether the support condition is forced by the affine projector."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))