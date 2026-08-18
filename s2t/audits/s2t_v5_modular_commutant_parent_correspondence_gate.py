#!/usr/bin/env python3
"""Модулярное соответствие проекторов в полном коммутанте KO6."""

import itertools
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v5_modular_commutant_parent_correspondence_gate_results.json"
)
TOL = 1.0e-10

previous_modular_result = json.loads(
    (ROOT / "s2t/results/s2t_modular_grading_cocycle_results.json").read_text(
        encoding="utf-8"
    )
)
assert previous_modular_result["factor_modular_gate"]["exact_spectrum"] == [
    "1/pi",
    "2/pi",
    "3/pi",
]
assert previous_modular_result["factor_modular_gate"]["derived_minimal_edges"] == [
    [1, 0],
    [2, 1],
]


def block_diag(blocks):
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), dtype=complex)
    offset = 0
    for block in blocks:
        width = block.shape[0]
        result[offset : offset + width, offset : offset + width] = block
        offset += width
    return result


def node_projector(node):
    blocks = []
    for half in range(2):
        for index in range(3):
            blocks.append(np.eye(3) if index == node else np.zeros((3, 3)))
    return block_diag(blocks)


def algebra_representation(matrix_part, scalar_left, scalar_right):
    identity = np.eye(3)
    return block_diag(
        [
            scalar_left * identity,
            matrix_part,
            matrix_part,
            np.conj(scalar_left) * identity,
            np.conj(scalar_left) * identity,
            np.conj(scalar_right) * identity,
        ]
    )


def algebra_basis():
    basis = []
    for row in range(3):
        for column in range(3):
            matrix = np.zeros((3, 3))
            matrix[row, column] = 1.0
            basis.append((matrix, 0.0, 0.0))
    basis.extend(
        [
            (np.zeros((3, 3)), 1.0, 0.0),
            (np.zeros((3, 3)), 0.0, 1.0),
            (np.zeros((3, 3)), 0.0, 1.0j),
        ]
    )
    return basis


def positive_frequency_part(operator, height, frequency=1.0):
    levels = np.real(np.diag(height))
    result = np.zeros_like(operator)
    for row, target_level in enumerate(levels):
        for column, source_level in enumerate(levels):
            if abs((target_level - source_level) - frequency) < TOL:
                result[row, column] = operator[row, column]
    return result


# Три проекторы вершин полного вещественного удвоения.
vertex_projectors = [node_projector(index) for index in range(3)]
identity18 = np.eye(18)
projector_residuals = {
    "sum_to_identity": float(np.linalg.norm(sum(vertex_projectors) - identity18)),
    "idempotence": max(
        float(np.linalg.norm(projector @ projector - projector))
        for projector in vertex_projectors
    ),
    "orthogonality": max(
        float(np.linalg.norm(vertex_projectors[i] @ vertex_projectors[j]))
        for i in range(3)
        for j in range(3)
        if i != j
    ),
}
assert max(projector_residuals.values()) < TOL

# Они лежат в совместном коммутанте левого и противоположного действий.
identity9 = np.eye(9)
zero9 = np.zeros((9, 9))
J_matrix = np.block([[zero9, identity9], [identity9, zero9]])
representations = [algebra_representation(*item) for item in algebra_basis()]
opposites = [J_matrix @ representation.conj() @ J_matrix for representation in representations]
left_commutant_residual = max(
    float(np.linalg.norm(projector @ representation - representation @ projector))
    for projector in vertex_projectors
    for representation in representations
)
right_commutant_residual = max(
    float(np.linalg.norm(projector @ representation - representation @ projector))
    for projector in vertex_projectors
    for representation in opposites
)
assert max(left_commutant_residual, right_commutant_residual) < TOL

# Сохраняющие неориентированный граф A3 изоморфизмы спектральных проекторов
# в проекторы вершин. Средняя вершина обязана перейти в единственную вершину
# степени два; два конца можно только сохранить или обратить.
edges = {frozenset((0, 1)), frozenset((1, 2))}
graph_isomorphisms = []
for permutation in itertools.permutations(range(3)):
    image_edges = {
        frozenset((permutation[left], permutation[right]))
        for left, right in [(0, 1), (1, 2)]
    }
    if image_edges == edges:
        graph_isomorphisms.append(permutation)
assert graph_isomorphisms == [(0, 1, 2), (2, 1, 0)]

particle_levels_by_map = []
for permutation in graph_isomorphisms:
    levels = [None, None, None]
    for spectral_index, vertex_index in enumerate(permutation):
        levels[vertex_index] = (-1, 0, 1)[spectral_index]
    particle_levels_by_map.append(tuple(levels))
assert particle_levels_by_map == [(-1, 0, 1), (1, 0, -1)]

# Выбираем одного представителя; второй даёт общий знак и то же квадратное
# действие. Античастичная половина достраивается вещественной структурой.
h_particle = block_diag([-np.eye(3), np.zeros((3, 3)), np.eye(3)])
h_full = block_diag([h_particle, -h_particle])
gamma_particle = block_diag([np.eye(3), -np.eye(3), np.eye(3)])
gamma_full = block_diag([gamma_particle, -gamma_particle])

J_height_residual = float(
    np.linalg.norm(J_matrix @ h_full.conj() @ J_matrix + h_full)
)
grading_height_residual = float(
    np.linalg.norm(h_full @ gamma_full - gamma_full @ h_full)
)
algebra_height_residual = max(
    float(np.linalg.norm(h_full @ representation - representation @ h_full))
    for representation in representations + opposites
)
assert max(J_height_residual, grading_height_residual, algebra_height_residual) < TOL

# Верное положительное состояние на полной матричной алгебре.
beta = 0.73
rho_unnormalized = np.diag(np.exp(-beta * np.real(np.diag(h_full))))
rho = rho_unnormalized / np.trace(rho_unnormalized)
rho_eigenvalues = np.linalg.eigvalsh(rho)
state_trace_residual = float(abs(np.trace(rho) - 1.0))
state_hermiticity_residual = float(np.linalg.norm(rho - rho.conj().T))
state_minimum_eigenvalue = float(np.min(rho_eigenvalues))
assert state_trace_residual < TOL
assert state_hermiticity_residual < TOL
assert state_minimum_eigenvalue > 0.0

# Полный оператор Дирака и его модулярная положительно-частотная часть.
rng = np.random.default_rng(20260816)
X = rng.normal(size=(3, 3))
phi = 0.37 + 0.19j
Y = phi * np.eye(3)
zero3 = np.zeros((3, 3), dtype=complex)
D_particle = np.block(
    [
        [zero3, X.T, zero3],
        [X, zero3, Y.conj().T],
        [zero3, Y, zero3],
    ]
)
D_full = block_diag([D_particle, D_particle.conj()])
d_plus = positive_frequency_part(D_full, h_full, frequency=1.0)
d_minus = d_plus.conj().T

dirac_selfadjoint_residual = float(np.linalg.norm(D_full - D_full.conj().T))
dirac_grading_residual = float(
    np.linalg.norm(D_full @ gamma_full + gamma_full @ D_full)
)
dirac_reality_residual = float(
    np.linalg.norm(J_matrix @ D_full.conj() @ J_matrix - D_full)
)
order_zero_residual = max(
    float(np.linalg.norm(left @ right - right @ left))
    for left in representations
    for right in opposites
)
first_order_residual = max(
    float(
        np.linalg.norm(
            (D_full @ left - left @ D_full) @ right
            - right @ (D_full @ left - left @ D_full)
        )
    )
    for left in representations
    for right in opposites
)
state_algebra_commutator_residual = max(
    float(np.linalg.norm(rho @ representation - representation @ rho))
    for representation in representations + opposites
)
assert max(
    dirac_selfadjoint_residual,
    dirac_grading_residual,
    dirac_reality_residual,
    order_zero_residual,
    first_order_residual,
    state_algebra_commutator_residual,
) < TOL

dirac_reconstruction_residual = float(np.linalg.norm(D_full - d_plus - d_minus))
frequency_residual = float(
    np.linalg.norm(h_full @ d_plus - d_plus @ h_full - d_plus)
)
J_reversal_residual = float(
    np.linalg.norm(J_matrix @ d_plus.conj() @ J_matrix - d_minus)
)
assert max(dirac_reconstruction_residual, frequency_residual, J_reversal_residual) < TOL

# Прямая проверка K_mod=-log Delta=beta ad_h на всех ненулевых элементах d+.
modular_generator_residuals = []
rho_diagonal = np.real(np.diag(rho))
height_diagonal = np.real(np.diag(h_full))
for row, column in zip(*np.nonzero(np.abs(d_plus) > TOL)):
    k_from_state = -math.log(rho_diagonal[row] / rho_diagonal[column])
    k_from_height = beta * (height_diagonal[row] - height_diagonal[column])
    modular_generator_residuals.append(abs(k_from_state - k_from_height))
assert max(modular_generator_residuals) < TOL

curvature = d_plus @ d_minus - d_minus @ d_plus
particle_middle = curvature[3:6, 3:6]
target = X @ X.T - Y.conj().T @ Y
moment_map_residual = float(np.linalg.norm(particle_middle - target))

middle_projector = vertex_projectors[1]
normalized_parent_trace = float(
    np.trace(middle_projector @ curvature @ curvature).real / 6.0
)
expected_trace = float(np.trace(target @ target).real / 3.0)
trace_normalization_residual = abs(normalized_parent_trace - expected_trace)
assert max(moment_map_residual, trace_normalization_residual) < TOL

# Почему это не противоречит запрету конечного центрального обмена:
# центр полной матричной алгебры одномерен, а проекторы вершин не центральны
# в M18, хотя коммутируют с физически представленной алгеброй.
test_offdiagonal = np.zeros((18, 18), dtype=complex)
test_offdiagonal[3:6, 0:3] = np.eye(3)
vertex_noncentral_witness = float(
    np.linalg.norm(vertex_projectors[0] @ test_offdiagonal - test_offdiagonal @ vertex_projectors[0])
)
assert vertex_noncentral_witness > 1.0

result = {
    "date": "2026-08-16",
    "gate": "version5_modular_commutant_parent_correspondence_gate",
    "parent_algebra": {
        "algebra": "M18(C)",
        "normalized_trace": "tau18=Tr18/18",
        "unique_normalized_trace": True,
        "represented_physical_algebra": "R direct_sum M3(R) direct_sum C",
    },
    "vertex_projector_algebra": {
        "algebra": "C^3 inside the joint commutant of left and opposite actions",
        "ranks": [int(np.linalg.matrix_rank(projector)) for projector in vertex_projectors],
        "projector_residuals": projector_residuals,
        "left_commutant_residual": left_commutant_residual,
        "right_commutant_residual": right_commutant_residual,
    },
    "spectral_projector_correspondence": {
        "source": "C*(L_family) isomorphic to C^3",
        "graph": "A3",
        "graph_preserving_star_isomorphism_count": len(graph_isomorphisms),
        "isomorphisms": [list(item) for item in graph_isomorphisms],
        "induced_particle_heights": [list(item) for item in particle_levels_by_map],
        "one_orbit_up_to_global_reversal": True,
        "vector_phase_choice_needed": False,
    },
    "full_KO6_height": {
        "J_odd_residual": J_height_residual,
        "grading_commutator_residual": grading_height_residual,
        "left_and_opposite_algebra_commutator_residual": algebra_height_residual,
    },
    "full_KO6_Dirac_recheck": {
        "selfadjoint_residual": dirac_selfadjoint_residual,
        "grading_odd_residual": dirac_grading_residual,
        "J_reality_residual": dirac_reality_residual,
        "order_zero_residual": order_zero_residual,
        "first_order_residual": first_order_residual,
    },
    "faithful_modular_state": {
        "beta_test_value": beta,
        "trace_residual": state_trace_residual,
        "hermiticity_residual": state_hermiticity_residual,
        "minimum_eigenvalue": state_minimum_eigenvalue,
        "positive_for_every_beta_greater_than_zero": True,
        "orientation_independent_of_beta_magnitude": True,
        "absolute_state_weights_depend_on_beta": True,
        "left_and_opposite_algebra_commutator_residual": state_algebra_commutator_residual,
    },
    "modular_polarization": {
        "D_equals_d_plus_d_star_residual": dirac_reconstruction_residual,
        "positive_frequency_residual": frequency_residual,
        "J_maps_d_to_d_star_residual": J_reversal_residual,
        "Kmod_equals_beta_ad_h_max_residual": max(modular_generator_residuals),
    },
    "oriented_curvature": {
        "middle_identity": "[d,d*]|G=XX*-Y*Y",
        "moment_map_residual": moment_map_residual,
        "normalized_parent_trace": normalized_parent_trace,
        "expected_tau3_trace": expected_trace,
        "trace_normalization_residual": trace_normalization_residual,
    },
    "relation_to_previous_twist_no_go": {
        "center_of_M18_dimension": 1,
        "vertex_projectors_central_in_M18": False,
        "noncentral_commutator_witness": vertex_noncentral_witness,
        "uses_central_flip": False,
        "finding": (
            "The faithful modular state polarizes noncentral transition blocks; it does "
            "not implement the forbidden exchange of central idempotents."
        ),
    },
    "closure_ledger": {
        "one_parent_algebra_for_modular_state_and_KO6_nodes": True,
        "faithful_positive_state": True,
        "unique_full_matrix_trace": True,
        "orientation_derived_before_X_Y": True,
        "exact_moment_map_square": True,
        "standard_model_representation_in_same_parent": False,
        "M60_family_gauge_trace_integrated_without_double_counting": False,
        "full_parent_action": False,
        "physical_BV_BRST_Hessian": False,
        "two_blind_physical_endpoints": False,
    },
    "verdict": {
        "local_parent_correspondence": "pass",
        "previous_orientation_obstruction": "resolved_by_modular_polarization",
        "complete_tome5_parent_architecture": False,
        "physical_closure": False,
        "status": "first_positive_modular_KO6_parent_subarchitecture",
    },
    "next_gate": (
        "Embed the modular-KO6 correspondence and the existing M60 family-gauge trace "
        "in one representation without duplicating the family triplet or adding a free weight."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))