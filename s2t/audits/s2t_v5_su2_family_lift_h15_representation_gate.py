#!/usr/bin/env python3
"""Представительный аудит семейного SU(2)_F-подъёма на H15/M35."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_su2_family_lift_h15_representation_gate_results.json"


def commutator(a, b):
    return a @ b - b @ a


def norm(a):
    return float(np.linalg.norm(a))


def diagonal_center(weights):
    return np.diag(np.exp(-2j * np.pi * np.asarray(weights, dtype=float)))


# Центральный элемент -1 in SU(2) является поворотом на 2 pi.
center_spin_one = diagonal_center([1, 0, -1])
center_spin_half = diagonal_center([0.5, -0.5])
assert np.allclose(center_spin_one, np.eye(3))
assert np.allclose(center_spin_half, -np.eye(2))

# Существующая семейная цепь на частичной половине: 1 + 3 + 3 + 3 = 10.
center_family_particle = np.eye(10, dtype=complex)
center_family_ko6 = np.eye(20, dtype=complex)
center_light_packet = np.eye(45, dtype=complex)
center_full_parent = np.eye(300, dtype=complex)

# Попытка использовать KO6-удвоение как фундаментальный дублет SU(2).
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
eye10 = np.eye(10, dtype=complex)
gamma_ko6 = np.kron(sigma_z, eye10)
ko6_generators = {
    "sigma_x": np.kron(sigma_x, eye10),
    "sigma_y": np.kron(sigma_y, eye10),
    "sigma_z": np.kron(sigma_z, eye10),
}
ko6_commutator_norms = {
    name: norm(commutator(generator, gamma_ko6))
    for name, generator in ko6_generators.items()
}
assert ko6_commutator_norms["sigma_x"] > 0
assert ko6_commutator_norms["sigma_y"] > 0
assert np.isclose(ko6_commutator_norms["sigma_z"], 0)

# Замена триплета поколений на 2+1 сохраняет размерность, но меняет
# центральное действие и разрушает исходное неприводимое SO(3)-чтение.
center_two_plus_one = np.diag([-1, -1, 1]).astype(complex)
assert not np.allclose(center_two_plus_one, np.eye(3))
assert not np.allclose(center_two_plus_one, -np.eye(3))

# Слабый SU(2)_L действует двойственно только на 8 левых состояниях H15:
# три цветных Q_L-дублета и один L_L-дублет. Семь правых синглетов
# получают тривиальный центральный знак.
weak_center_h15 = np.diag([-1] * 8 + [1] * 7).astype(complex)
assert np.linalg.matrix_rank(weak_center_h15 - np.eye(15)) == 8
assert np.linalg.matrix_rank(weak_center_h15 + np.eye(15)) == 7

# Если 2+1 трактовать как хиральный калибровочный SU(2)_F, каждый из 15
# Weyl-каналов H15 несёт один семейный дублет: число дублетов нечётно.
physical_weyl_doublets_if_two_plus_one = 15
assert physical_weyl_doublets_if_two_plus_one % 2 == 1

result = {
    "gate": "version5_su2_family_lift_h15_representation_gate",
    "current_module_ledger": {
        "H15_dimension": 15,
        "light_family_packet_dimension": 45,
        "particle_family_chain_dimension": 10,
        "KO6_family_chain_dimension": 20,
        "full_parent_dimension": 300,
        "linking_algebra": "M35 with corners M20 and M15",
        "existing_family_SO3_decomposition": "1+3+3+3 on the particle family chain",
    },
    "center_action": {
        "spin_one_triplet": "plus_identity",
        "spin_half_doublet": "minus_identity",
        "particle_family_chain": "plus_identity_on_10",
        "KO6_family_chain": "plus_identity_on_20",
        "light_packet": "plus_identity_on_45",
        "full_parent": "plus_identity_on_300",
        "nontrivial_spinor_sign_present_in_current_family_module": False,
    },
    "KO6_double_as_family_spinor_test": {
        "commutator_norms_with_grading": ko6_commutator_norms,
        "full_SU2_preserves_grading": False,
        "maximal_continuous_subgroup_visible_on_copy_factor": "diagonal U(1)",
        "particle_conjugate_mixing_required_for_sigma_x_sigma_y": True,
    },
    "weak_SU2_reuse_test": {
        "minus_center_eigenspace_dimension": 8,
        "plus_center_eigenspace_dimension": 7,
        "uniform_family_spinor_sign": False,
        "preserves_existing_SM_assignment_if_identified_with_SU2F": False,
    },
    "family_two_plus_one_test": {
        "central_spectrum": [-1, -1, 1],
        "same_as_existing_spin_one_triplet": False,
        "irreducible_family_triplet_preserved": False,
        "physical_Weyl_doublet_count": physical_weyl_doublets_if_two_plus_one,
        "odd_doublet_global_anomaly": True,
    },
    "orientation_doublet_test": {
        "dimension": 2,
        "origin": "auxiliary counterpropagating factor added after E=M20x15",
        "contained_in_H15_or_M35": False,
        "can_carry_spin_half_kinematically": True,
        "identification_with_family_SU2_is_current_architecture_pass": False,
        "reason": "it requires an external associated module or a new Spin^h-type locking of propagation and family transport",
    },
    "trace_and_state_budget": {
        "existing_M35_trace_normalizes_external_orientation_doublet": False,
        "new_half_integer_associated_module_requires_trace_rederivation": True,
        "new_fermion_states_allowed_by_gate": False,
    },
    "verdict": {
        "adjoint_SO3_family_transport_reproduced": True,
        "nontrivial_central_spinor_sign_on_current_H15_M35": False,
        "all_gate_conditions_simultaneously_satisfied": False,
        "status": "fail_representation_obstruction",
        "main_route_in_current_version": "closed_before_monopole_dynamics",
        "reopening_condition": "a separately declared new version with an external half-integer associated module or Spin^h-type locking, followed by fresh KO6, anomaly, trace, and phenomenology audits",
    },
    "next_gate": None,
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))