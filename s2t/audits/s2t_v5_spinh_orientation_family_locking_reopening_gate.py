#!/usr/bin/env python3
"""Аудит Spin^h-связывания ориентационного и семейного дублетов."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_spinh_orientation_family_locking_reopening_gate_results.json"


def commutator(a, b):
    return a @ b - b @ a


def matrix_rank(a, tol=1e-10):
    return int(np.linalg.matrix_rank(a, tol=tol))


sigma = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]
eye2 = np.eye(2, dtype=complex)
eye4 = np.eye(4, dtype=complex)

# Коммутант полного фундаментального SU(2)-действия на C2.
# X = a0 I + ax sigma_x + ay sigma_y + az sigma_z.
commutant_constraints = []
for generator in sigma:
    for basis in [eye2] + sigma:
        commutant_constraints.append(commutator(basis, generator).reshape(-1))

# Столбцы соответствуют коэффициентам общего X в базисе {I,sigma_i}.
constraint_matrix = np.stack(commutant_constraints, axis=0).reshape(3, 4, 4)
constraint_matrix = np.concatenate(constraint_matrix, axis=0).T
commutant_dimension = 4 - matrix_rank(constraint_matrix)
assert commutant_dimension == 1

# На C2 не существует второго нетривиального commuting su(2).
# В минимальном тензорном представлении C2_spin tensor C2_family оно есть.
spin_generators_c4 = [np.kron(s / 2, eye2) for s in sigma]
family_generators_c4 = [np.kron(eye2, s / 2) for s in sigma]
cross_commutator_norms = [
    float(np.linalg.norm(commutator(a, b)))
    for a in spin_generators_c4
    for b in family_generators_c4
]
assert all(np.isclose(value, 0) for value in cross_commutator_norms)

spin_center_c4 = np.kron(-eye2, eye2)
family_center_c4 = np.kron(eye2, -eye2)
diagonal_center_c4 = spin_center_c4 @ family_center_c4
assert np.allclose(diagonal_center_c4, eye4)
assert not np.allclose(spin_center_c4, eye4)
assert not np.allclose(family_center_c4, eye4)

# Размерностный бюджет текущего локального переноса.
morita_internal_dimension = 300
current_walk_dimension = 2 * morita_internal_dimension
minimal_spinh_walk_dimension = 2 * 2 * morita_internal_dimension
assert current_walk_dimension == 600
assert minimal_spinh_walk_dimension == 1200

# Если новый внутренний дублет назначается всем H15-каналам, сохраняется
# нечётное число хиральных SU(2)-дублетов.
universal_family_doublets = 15
assert universal_family_doublets % 2 == 1

result = {
    "gate": "version5_spinh_orientation_family_locking_reopening_gate",
    "mathematical_definition": {
        "group": "Spin^h(n)=(Spin(n) x SU(2))/diagonal_Z2",
        "descent_condition": "the pair (-1,-1) must act trivially",
        "canonical_auxiliary_bundle": "SO(3)",
        "topological_condition": "w2(Q)=w2(TM)",
    },
    "single_orientation_doublet_test": {
        "carrier": "C2_orientation",
        "commutant_dimension_of_fundamental_SU2": commutant_dimension,
        "second_nontrivial_commuting_SU2_exists": False,
        "can_host_independent_spin_and_family_actions": False,
        "reason": "the fundamental SU(2) action on C2 is irreducible and its commutant is scalar",
    },
    "minimal_valid_product_representation": {
        "carrier": "C2_spin tensor C2_family",
        "complex_dimension": 4,
        "all_cross_commutator_norms": cross_commutator_norms,
        "spin_center_action": "-I4",
        "family_center_action": "-I4",
        "diagonal_center_action": "+I4",
        "descends_to_Spinh": True,
    },
    "state_and_trace_budget": {
        "Morita_internal_dimension": morita_internal_dimension,
        "current_orientation_walk_dimension": current_walk_dimension,
        "minimal_Spinh_walk_dimension": minimal_spinh_walk_dimension,
        "extra_internal_doublet_required": True,
        "contained_in_H15_M35": False,
        "existing_M35_trace_normalizes_it": False,
    },
    "topology_audit": {
        "current_carrier_has_spin_structures": True,
        "Spinh_needed_to_repair_tangent_spin_obstruction": False,
        "projective_order_parameter_alone_specifies_auxiliary_SO3_bundle": False,
        "required_equality_w2_Q_equals_w2_TM_derived": False,
    },
    "anomaly_audit": {
        "universal_H15_half_isospin_doublets": universal_family_doublets,
        "odd_doublet_obstruction_removed_by_relabeling_as_Spinh": False,
        "fresh_bordism_and_global_anomaly_audit_required": True,
    },
    "verdict": {
        "existing_orientation_C2_is_a_hidden_Spinh_completion": False,
        "Spinh_is_a_precise_language_for_a_new_architecture": True,
        "reopening_without_new_module": False,
        "status": "fail_single_doublet_locking",
        "version5_route": "remains_closed",
        "possible_new_version": "requires an explicit independent C2_family, an extended trace, a derived SO3 bundle, and anomaly cancellation",
    },
    "next_gate": None,
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))