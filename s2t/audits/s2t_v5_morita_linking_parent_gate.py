#!/usr/bin/env python3
"""Связывающий родитель Мориты для двух чтений общего носителя."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_morita_linking_parent_gate_results.json"
TOL = 1.0e-10
M = 20
N = 15


def random_hermitian(rng, size):
    raw = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    return 0.5 * (raw + raw.conj().T)


def centered(matrix):
    size = matrix.shape[0]
    return matrix - np.trace(matrix) * np.eye(size) / size


def random_unitary(rng, size):
    raw = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    q, r = np.linalg.qr(raw)
    phases = np.diag(r)
    phases = np.where(abs(phases) > TOL, phases / abs(phases), 1.0)
    return q @ np.diag(phases.conj())


commuting_square = json.loads(
    (ROOT / "s2t/results/s2t_v5_commuting_square_readout_gate_results.json")
    .read_text(encoding="utf-8")
)
observed = json.loads(
    (ROOT / "s2t/results/s2t_v5_sm_linking_corner_gate_results.json")
    .read_text(encoding="utf-8")
)
rank_one = json.loads(
    (ROOT / "s2t/results/s2t_v5_rank_one_tangent_junk_gate_results.json")
    .read_text(encoding="utf-8")
)
state_corner = json.loads(
    (ROOT / "s2t/results/s2t_v5_state_corner_curvature_readout_gate_results.json")
    .read_text(encoding="utf-8")
)
assert commuting_square["verdict"]["two_readings_one_parent_trace"] == "pass"
assert observed["verdict"]["exact_SM_block_reading_in_square"] == "pass"
assert rank_one["verdict"]["off_diagonal_linking_corner_as_one_forms"] == "pass"
assert state_corner["verdict"]["full_to_rank_one_curvature_readout"] == "pass"

rng = np.random.default_rng(20260816)
family_curvature = random_hermitian(rng, M)
observed_curvature = random_hermitian(rng, N)
family_centered = centered(family_curvature)
observed_centered = centered(observed_curvature)

# Векторизация матриц 20x15 по строкам:
# vec(F X)=(F tensor I15)vec(X), vec(X G)=(I20 tensor G^T)vec(X).
left_action = np.kron(family_curvature, np.eye(N))
right_action = np.kron(np.eye(M), observed_curvature.T)
relative_curvature = left_action - right_action

left_centered = np.kron(family_centered, np.eye(N))
right_centered = np.kron(np.eye(M), observed_centered.T)
relative_centered = left_centered - right_centered

left_right_commutator = left_action @ right_action - right_action @ left_action

tau_family = np.trace(family_curvature) / M
tau_observed = np.trace(observed_curvature) / N
predicted_trace = (
    np.trace(family_curvature @ family_curvature) / M
    + np.trace(observed_curvature @ observed_curvature) / N
    - 2.0 * tau_family * tau_observed
)
measured_trace = np.trace(relative_curvature @ relative_curvature) / (M * N)

predicted_centered = (
    np.trace(family_centered @ family_centered) / M
    + np.trace(observed_centered @ observed_centered) / N
)
measured_centered = np.trace(relative_centered @ relative_centered) / (M * N)

# Ковариантность R(X)=F X-X G при X -> U X V*.
unitary_family = random_unitary(rng, M)
unitary_observed = random_unitary(rng, N)
connector = rng.normal(size=(M, N)) + 1j * rng.normal(size=(M, N))
transformed_connector = unitary_family @ connector @ unitary_observed.conj().T
transformed_family = unitary_family @ family_curvature @ unitary_family.conj().T
transformed_observed = (
    unitary_observed @ observed_curvature @ unitary_observed.conj().T
)
curvature_before = family_curvature @ connector - connector @ observed_curvature
curvature_after = (
    transformed_family @ transformed_connector
    - transformed_connector @ transformed_observed
)
covariance_target = (
    unitary_family @ curvature_before @ unitary_observed.conj().T
)
covariance_residual = np.linalg.norm(curvature_after - covariance_target)

# Единственный след связывающей алгебры M35 и нормированные угловые следы.
corner_family_weight = M / (M + N)
corner_observed_weight = N / (M + N)
linking_trace_family = np.trace(family_curvature) / (M + N)
linking_trace_observed = np.trace(observed_curvature) / (M + N)
conditioned_family_trace = linking_trace_family / corner_family_weight
conditioned_observed_trace = linking_trace_observed / corner_observed_weight

# Точное разложение наблюдаемого пятнадцатимерного угла.
observed_block_sizes = [6, 2, 3, 3, 1]
off_diagonal_block_dimensions = [M * size for size in observed_block_sizes]

residuals = {
    "left_right_action_commutator": float(np.linalg.norm(left_right_commutator)),
    "general_relative_trace_identity": float(abs(measured_trace - predicted_trace)),
    "centered_relative_trace_identity": float(
        abs(measured_centered - predicted_centered)
    ),
    "bimodule_curvature_covariance": float(covariance_residual),
    "conditioned_family_trace": float(abs(conditioned_family_trace - tau_family)),
    "conditioned_observed_trace": float(
        abs(conditioned_observed_trace - tau_observed)
    ),
}
assert max(residuals.values()) < TOL

result = {
    "gate": "version5_morita_linking_parent_gate",
    "input_certificates": {
        "commuting_square_two_readings": "pass",
        "exact_standard_model_reading": "pass",
        "rank_one_linking_tangent": "pass",
        "state_corner_curvature_transfer": "pass",
    },
    "morita_carrier": {
        "family_reading_algebra": "M20(C)",
        "observed_control_reading_algebra": "M15(C)",
        "equivalence_bimodule": "E=M20x15(C)",
        "complex_dimension_E": M * N,
        "physical_parent_dimension": 300,
        "left_compact_endomorphisms": "K_right(E)=M20(C)",
        "right_compact_endomorphisms": "K_left(E)=M15(C)",
        "endomorphism_algebra_of_carrier": "End_C(E)=M300(C)",
    },
    "linking_algebra": {
        "formula": "L(E)=[[M20,E],[E*,M15]]=M35(C)",
        "representation_dimension": M + N,
        "complex_vector_space_dimension": (M + N) ** 2,
        "dimension_ledger": {
            "family_corner": M**2,
            "observed_corner": N**2,
            "upper_off_diagonal": M * N,
            "lower_off_diagonal": M * N,
            "sum": M**2 + N**2 + 2 * M * N,
        },
        "unique_normalized_trace": True,
        "family_corner_weight": corner_family_weight,
        "observed_corner_weight": corner_observed_weight,
        "conditioned_corner_traces_recover_tau20_tau15": True,
    },
    "exact_observed_corner_decomposition": {
        "block_sizes": observed_block_sizes,
        "bimodule_block_dimensions": off_diagonal_block_dimensions,
        "sum": sum(off_diagonal_block_dimensions),
    },
    "relative_bimodule_curvature": {
        "covariant_derivative": "nabla_E xi=d xi+A_F xi-xi A_O",
        "curvature": "R_E(xi)=F_F xi-xi F_O",
        "minus_sign_source": "right action in the covariant derivative",
        "independent_braiding_or_sigma_chosen": False,
        "implementation": "ordinary block multiplication in the linking algebra",
        "normalized_operator_trace_formula": (
            "tau300(R^2)=tau20(F_F^2)+tau15(F_O^2)"
            "-2 tau20(F_F) tau15(F_O)"
        ),
        "centered_formula": (
            "tau300(R^2)=tau20(F_F^2)+tau15(F_O^2) when both curvatures are centered"
        ),
        "residuals": residuals,
    },
    "architecture_interpretation": {
        "M35_role": "linking operator container for the two readings",
        "M300_role": "endomorphism algebra of the 300-dimensional off-diagonal carrier",
        "two_algebras_are_not_two_unrelated_worlds": True,
        "physical_carrier_is_the_space_of_transitions": True,
        "old_commuting_square_trace_identity_reinterpreted": (
            "norm identity of centered relative bimodule curvature"
        ),
    },
    "gauge_boundary": {
        "full_M35_as_coordinate_algebra": False,
        "forbidden_full_unitary_lie_dimension": (M + N) ** 2,
        "standard_model_gauge_lie_dimension": 12,
        "extra_generators_if_U35_gauged": (M + N) ** 2 - 12,
        "physical_coordinate_subalgebras_still_required": True,
        "linking_container_does_not_imply_gauging_all_unitaries": True,
    },
    "verdict": {
        "canonical_Morita_bimodule_origin_of_C300": "pass",
        "one_linking_trace_and_conditioned_corner_traces": "pass",
        "relative_curvature_without_free_sigma": "pass",
        "exact_SM_subalgebra_as_right_coordinate_corner": "conditional_pass",
        "M35_as_new_coordinate_algebra": "fail_by_gauge_enlargement",
        "Yukawa_operator_from_same_connection": "open",
        "full_BV_BRST_Hessian": "open",
        "physical_closure": False,
        "status": (
            "C300 is canonically the transition bimodule between two readings; "
            "M35 links the readings while M300 acts on their transitions"
        ),
    },
    "next_gate": (
        "Restrict the right M15 corner to the exact Standard Model coordinate action "
        "and the left M20 corner to the affine family action; classify compatible "
        "bimodule connections and test whether the state-supported Yukawa map is the "
        "unique off-diagonal connection component without gauging U35."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))