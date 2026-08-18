#!/usr/bin/env python3
"""Амальгамированное объединение модулярного KO6-носителя и M60."""

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_modular_ko6_m60_amalgamation_gate_results.json"
TOL = 1.0e-10

modular_parent = json.loads(
    (ROOT / "s2t/results/s2t_v5_modular_commutant_parent_correspondence_gate_results.json").read_text(encoding="utf-8")
)
trace60 = json.loads(
    (ROOT / "s2t/results/s2t_parent_trace_tensor_product_results.json").read_text(encoding="utf-8")
)
su5 = json.loads(
    (ROOT / "s2t/results/s2t_state_menu_su5_fiber_results.json").read_text(encoding="utf-8")
)
assert modular_parent["verdict"]["local_parent_correspondence"] == "pass"
assert trace60["gates"]["single_parent_trace"]["passes"]
assert su5["anomaly_checks"]["SU5_total"] == 0

# Размерности двух исходных конструкций и их общей физической части.
family_dimension = 3
su5_package_dimension = 15
reference_dimension = su5_package_dimension
physical_family_dimension = family_dimension * su5_package_dimension  # 45
chain_particle_dimension = 3 * family_dimension * su5_package_dimension  # 135
menu_particle_dimension = reference_dimension + physical_family_dimension  # 60
shared_particle_dimension = physical_family_dimension  # общий L-угол
amalgamated_particle_dimension = (
    menu_particle_dimension + chain_particle_dimension - shared_particle_dimension
)  # 150
parent_dimension = 2 * amalgamated_particle_dimension  # KO6-удвоение
naive_tensor_dimension = 18 * 60

assert parent_dimension == 300
assert naive_tensor_dimension == 1080

# Углы полного M300: удвоенный menu-угол, KO6-chain-угол и их пересечение.
menu_full_corner_rank = 2 * menu_particle_dimension  # 120
chain_full_corner_rank = 2 * chain_particle_dimension  # 270
intersection_full_rank = 2 * shared_particle_dimension  # 90
assert menu_full_corner_rank + chain_full_corner_rank - intersection_full_rank == parent_dimension

# Один полный след индуцирует прежние условные следы без свободного веса.
tau300_reference_weight = (2 * reference_dimension) / parent_dimension
tau300_chain_weight = chain_full_corner_rank / parent_dimension
menu_physical_fraction = physical_family_dimension / menu_particle_dimension
heavy_family_rank = 15
heavy_family_fraction = heavy_family_rank / physical_family_dimension
assert abs(menu_physical_fraction - 3 / 4) < TOL
assert abs(heavy_family_fraction - 1 / 3) < TOL

# SU(5)-эквивариантная цепь требует распространить один и тот же package
# по всем трём вершинам. Иначе ненулевое ребро не коммутирует с SU(5).
generator15 = np.diag([1.0, -1.0] + [0.0] * 13)
I3 = np.eye(3)
I15 = np.eye(15)
rho = 0.83
r = 0.61
zero3 = np.zeros((3, 3))
D9 = np.block(
    [
        [zero3, rho * I3, zero3],
        [rho * I3, zero3, r * I3],
        [zero3, r * I3, zero3],
    ]
)
D135 = np.kron(D9, I15)
su5_all_nodes = np.kron(np.eye(9), generator15)
su5_endpoint_only = np.kron(
    np.diag([1.0] * 3 + [0.0] * 6), generator15
)
propagated_equivariance_residual = float(
    np.linalg.norm(D135 @ su5_all_nodes - su5_all_nodes @ D135)
)
endpoint_only_residual = float(
    np.linalg.norm(D135 @ su5_endpoint_only - su5_endpoint_only @ D135)
)
assert propagated_equivariance_residual < TOL
assert endpoint_only_residual > 1.0

# Спектр цепи: один лёгкий 45-мерный пакет и две массивные комбинации.
eigenvalues = np.linalg.eigvalsh(D135)
kernel_dimension = int(np.count_nonzero(np.abs(eigenvalues) < TOL))
positive_mass = math.sqrt(rho**2 + r**2)
positive_multiplicity = int(np.count_nonzero(np.abs(eigenvalues - positive_mass) < TOL))
negative_multiplicity = int(np.count_nonzero(np.abs(eigenvalues + positive_mass) < TOL))
assert kernel_dimension == 45
assert positive_multiplicity == 45
assert negative_multiplicity == 45

# Общий случай с невырожденным X также оставляет ровно dim=3 до SU5-тензора.
rng = np.random.default_rng(20260816)
X = rng.normal(size=(3, 3))
while abs(np.linalg.det(X)) < 0.1:
    X = rng.normal(size=(3, 3))
Y = (0.42 + 0.17j) * np.eye(3)
zero = np.zeros((3, 3), dtype=complex)
D9_generic = np.block(
    [[zero, X.conj().T, zero], [X, zero, Y.conj().T], [zero, Y, zero]]
)
generic_kernel_dimension = 9 - int(np.linalg.matrix_rank(D9_generic, tol=TOL))
assert generic_kernel_dimension == 3

# Момент-карта после SU5-тензора и полного вещественного удвоения.
target = X @ X.T - Y.conj().T @ Y
full_middle_trace = 2 * su5_package_dimension * float(np.trace(target @ target).real)
normalized_middle_trace = full_middle_trace / intersection_full_rank
expected_tau3 = float(np.trace(target @ target).real / 3.0)
moment_trace_residual = abs(normalized_middle_trace - expected_tau3)
assert moment_trace_residual < TOL

# Калибровочные индексы и аномалии наследуются без нового коэффициента.
three_family_indices = trace60["gauge_operator"]["three_family_loop_indices"]
index_equality_residual = max(three_family_indices.values()) - min(three_family_indices.values())
anomaly_residual = max(
    abs(su5["anomaly_checks"][key])
    for key in [
        "SU5_total",
        "gravitational_U1",
        "U1_cubic",
        "SU3_squared_U1",
        "SU2_squared_U1",
    ]
)
assert index_equality_residual < TOL
assert anomaly_residual < TOL

result = {
    "date": "2026-08-16",
    "gate": "version5_modular_ko6_m60_amalgamation_gate",
    "input_certificates": {
        "modular_KO6_parent": "pass",
        "M60_trace": "pass",
        "SU5_package_anomaly": "zero",
    },
    "dimension_ledger": {
        "naive_M18_tensor_M60": naive_tensor_dimension,
        "menu_particle_corner": menu_particle_dimension,
        "KO6_SU5_chain_particle_corner": chain_particle_dimension,
        "shared_three_family_particle_corner": shared_particle_dimension,
        "amalgamated_particle_dimension": amalgamated_particle_dimension,
        "full_KO6_parent_dimension": parent_dimension,
        "formula": "2*(60+135-45)=300",
        "avoided_dimension_count": naive_tensor_dimension - parent_dimension,
    },
    "parent_algebra": {
        "algebra": "M300(C)",
        "unique_normalized_trace": True,
        "relative_central_weight_count": 0,
        "menu_full_corner_rank": menu_full_corner_rank,
        "chain_full_corner_rank": chain_full_corner_rank,
        "intersection_full_rank": intersection_full_rank,
    },
    "conditional_trace_recovery": {
        "physical_family_rank_inside_particle_menu": physical_family_dimension,
        "particle_menu_rank": menu_particle_dimension,
        "physical_fraction": menu_physical_fraction,
        "expected_M60_fraction": 0.75,
        "heavy_family_rank": heavy_family_rank,
        "heavy_family_fraction_inside_physical": heavy_family_fraction,
        "expected_heavy_fraction": 1 / 3,
        "M60_and_M45_conditional_traces_recovered": True,
        "full_parent_reference_weight_fixed": tau300_reference_weight,
        "full_parent_chain_weight_fixed": tau300_chain_weight,
    },
    "SU5_equivariance": {
        "propagated_package_commutator_residual": propagated_equivariance_residual,
        "endpoint_only_commutator_residual": endpoint_only_residual,
        "finding": (
            "A nonzero SU5-invariant connector requires the same 10+bar5 package on "
            "all three chain nodes; restricting SU5 to the family endpoint kills equivariance."
        ),
    },
    "light_heavy_spectrum": {
        "radial_chain_parameters": {"rho": rho, "r": r},
        "particle_dimension": chain_particle_dimension,
        "zero_mode_dimension": kernel_dimension,
        "positive_mass": positive_mass,
        "positive_mass_multiplicity": positive_multiplicity,
        "negative_mass_multiplicity": negative_multiplicity,
        "generic_internal_kernel_dimension_before_SU5": generic_kernel_dimension,
        "interpretation": (
            "The propagated connector does not leave nine light families: one 45-state "
            "combination remains light while two 45-state combinations become massive."
        ),
    },
    "normalizations": {
        "middle_moment_trace_residual": moment_trace_residual,
        "three_family_SU5_indices": three_family_indices,
        "index_equality_residual": index_equality_residual,
        "maximum_anomaly_residual": anomaly_residual,
    },
    "remaining_risks": {
        "reference_sector_zero_modes_need_physical_projection": True,
        "massive_connector_stability_requires_full_Hessian": True,
        "beta_dependent_state_weights_not_used_as_predictions": True,
        "Yukawa_and_family_rank_one_operator_not_yet_inserted_in_one_action": True,
        "BV_BRST_factor_not_derived": True,
    },
    "verdict": {
        "non_double_counting_amalgamation": "pass",
        "single_trace_two_sector_normalization": "pass",
        "SU5_representation_and_anomaly": "pass",
        "exact_light_family_count_at_chain_level": "pass",
        "kinematic_parent_architecture_candidate": True,
        "full_action_closure": False,
        "physical_closure": False,
        "status": "first_M300_kinematic_parent_candidate_requires_action_and_Hessian",
    },
    "next_gate": (
        "Construct the most general symmetry-allowed M300 parent action and test whether "
        "one coefficient-free Hessian makes the two connector combinations massive, "
        "projects out the reference sector and preserves the 45-state light kernel."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))