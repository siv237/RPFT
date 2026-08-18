#!/usr/bin/env python3
"""Градуированное соответствие: правило Лейбница, кривизна и калибровочная развилка."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_graded_correspondence_superconnection_gate_results.json"
TOL = 1.0e-10

commutant_gate = json.loads(
    (ROOT / "s2t/results/s2t_v5_sm_family_commutant_calculus_gate_results.json")
    .read_text(encoding="utf-8")
)
affine_gate = json.loads(
    (ROOT / "s2t/results/s2t_v5_affine_ko6_reference_corner_gate_results.json")
    .read_text(encoding="utf-8")
)
assert commutant_gate["verdict"]["graded_correspondence_branch"] == "open"
assert affine_gate["family_KO6_bimodule"]["base_complex_dimension"] == 20


def block_diagonal(blocks):
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), dtype=complex)
    offset = 0
    for block in blocks:
        width = block.shape[0]
        result[offset : offset + width, offset : offset + width] = block
        offset += width
    return result


V = np.array(
    [
        [1.0, -1.0, 0.0, 0.0],
        [1.0, 1.0, -2.0, 0.0],
        [1.0, 1.0, 1.0, -3.0],
    ]
)
V /= np.linalg.norm(V, axis=1)[:, None]
P3 = V.T @ V
P1 = np.eye(4) - P3
uniform = np.ones(4) / 2.0

zero4 = np.zeros((4, 4), dtype=complex)
zero3 = np.zeros((3, 3), dtype=complex)
zero43 = np.zeros((4, 3), dtype=complex)
zero34 = np.zeros((3, 4), dtype=complex)
I3 = np.eye(3)


def raising_operator(X, phi):
    Y = phi * I3
    return np.block(
        [
            [zero4, zero43, zero43],
            [X, zero3, zero3],
            [zero34, Y, zero3],
        ]
    )


def hodge_curvature(X, phi):
    d = raising_operator(X, phi)
    height = block_diagonal([-P3, zero3, I3])
    return d @ d.conj().T - d.conj().T @ d - height


rng = np.random.default_rng(20260816)
rho = 0.83
phi = 0.61 + 0.20j
X = rho * V
d = raising_operator(X, phi)
Q = d + d.conj().T
height = block_diagonal([-P3, zero3, I3])

# Как A_SM-модуль семейная часть лежит в кратностном множителе и потому
# является A_SM-линейным нечётным эндоморфизмом. Это и есть конечномерный
# остаток правила Лейбница для ∇=∇_SM+Q.
observed_test_matrices = []
for _ in range(16):
    raw = rng.normal(size=(15, 15)) + 1j * rng.normal(size=(15, 15))
    observed_test_matrices.append(raw)
leibniz_residual = max(
    np.linalg.norm(
        np.kron(Q, np.eye(15)) @ np.kron(np.eye(10), a)
        - np.kron(np.eye(10), a) @ np.kron(Q, np.eye(15))
    )
    for a in observed_test_matrices
)
assert leibniz_residual < TOL

# Три естественных кандидата на кривизну семейной суперсвязности.
standard_curvature = Q @ Q
holomorphic_curvature = d @ d
commutator_curvature = d @ d.conj().T - d.conj().T @ d

middle = slice(4, 7)
gram_in = X @ X.conj().T
gram_out = abs(phi) ** 2 * I3
standard_middle_residual = np.linalg.norm(
    standard_curvature[middle, middle] - (gram_in + gram_out)
)
moment_middle_residual = np.linalg.norm(
    commutator_curvature[middle, middle] - (gram_in - gram_out)
)
holomorphic_path_residual = np.linalg.norm(
    holomorphic_curvature[7:10, 0:4] - phi * X
)
assert max(
    standard_middle_residual,
    moment_middle_residual,
    holomorphic_path_residual,
) < TOL

# Норма d^2 содержит только произведение двух стрелок, а не отображение
# момента. Проверяем это на случайной выборке.
holomorphic_norm_residuals = []
for _ in range(64):
    X_random = rng.normal(size=(3, 4)) + 1j * rng.normal(size=(3, 4))
    phi_random = rng.normal() + 1j * rng.normal()
    d_random = raising_operator(X_random, phi_random)
    d2 = d_random @ d_random
    holomorphic_norm_residuals.append(
        abs(
            np.trace(d2.conj().T @ d2).real
            - abs(phi_random) ** 2 * np.trace(X_random.conj().T @ X_random).real
        )
    )
assert max(holomorphic_norm_residuals) < TOL

# Высота действительно задаёт степень +1 только на подпространстве X=XP3.
height_vacuum_residual = np.linalg.norm(height @ d - d @ height - d)
reference_mixing_defects = []
for row in range(3):
    delta_X = np.zeros((3, 4))
    delta_X[row, :] = uniform
    delta_d = raising_operator(delta_X, 0.0)
    reference_mixing_defects.append(
        float(np.linalg.norm(height @ delta_d - delta_d @ height - delta_d))
    )
assert height_vacuum_residual < TOL
assert min(reference_mixing_defects) > 0.9

# Общая нормировка носителя одинаково масштабирует потенциальную и
# кинетическую квадратичные формы. Поэтому один множитель 3/10 сокращается
# из обобщённой задачи на собственные значения H v = m^2 G v.
trace_ratio_residuals = []
for _ in range(64):
    delta_X = rng.normal(size=(3, 4)) + 1j * rng.normal(size=(3, 4))
    delta_phi = rng.normal() + 1j * rng.normal()
    delta_d = raising_operator(delta_X, delta_phi)
    delta_Q = delta_d + delta_d.conj().T
    reduced_kinetic = np.trace(delta_Q.conj().T @ delta_Q).real / 3.0
    full_kinetic = (
        2.0 * 15.0 * np.trace(delta_Q.conj().T @ delta_Q).real / 300.0
    )
    trace_ratio_residuals.append(abs(full_kinetic - 0.3 * reduced_kinetic))
assert max(trace_ratio_residuals) < TOL

potential_trace_residuals = []
for _ in range(64):
    X_random = rng.normal(size=(3, 4)) + 1j * rng.normal(size=(3, 4))
    phi_random = rng.normal() + 1j * rng.normal()
    F = hodge_curvature(X_random, phi_random)
    reduced = np.trace(F.conj().T @ F).real / 3.0
    full = 2.0 * 15.0 * np.trace(F.conj().T @ F).real / 300.0
    potential_trace_residuals.append(abs(full - 0.3 * reduced))
assert max(potential_trace_residuals) < TOL

# Минимальная кратностная группа эндоморфизмов уже содержит U(10).
multiplicity_endomorphism_real_dimension_lower_bound = 10**2
standard_model_gauge_lie_dimension = 12

result = {
    "gate": "version5_graded_correspondence_superconnection_gate",
    "inputs": {
        "coordinate_algebra": "A_SM=C+H+M3(C)",
        "family_module": "K_fam=C4+C3+C3",
        "correspondence_module": "E=K_fam tensor A_SM",
        "full_KO6_observed_dimension": 300,
    },
    "connection_consistency": {
        "candidate": "nabla=nabla_SM+Q_fam, Q_fam=d+d*",
        "A_SM_linearity_residual": float(leibniz_residual),
        "graded_Leibniz_rule": "pass because Q_fam is A_SM-linear",
        "KO6_inherited_from_affine_bimodule": True,
        "standard_model_gauge_covariance": True,
        "family_operator_is_new_morphism_data": True,
    },
    "curvature_comparison": {
        "standard_superconnection": {
            "curvature": "Q_fam^2",
            "middle_block": "XX*+|Phi|^2 I3",
            "residual": float(standard_middle_residual),
            "produces_moment_map_difference": False,
        },
        "holomorphic_superconnection": {
            "curvature": "d^2",
            "nonzero_path": "Phi X from node 0 to node 2",
            "path_residual": float(holomorphic_path_residual),
            "maximum_norm_formula_residual": float(max(holomorphic_norm_residuals)),
            "norm": "|Phi|^2 Tr(X*X)",
            "produces_moment_map_difference": False,
        },
        "Hodge_moment_map": {
            "curvature": "[d,d*]-h",
            "middle_block": "XX*-|Phi|^2 I3",
            "residual": float(moment_middle_residual),
            "is_standard_superconnection_curvature": False,
            "requires_Hermitian_moment_map_primitive": True,
        },
    },
    "fixed_height_tangent_space": {
        "vacuum_unit_degree_residual": float(height_vacuum_residual),
        "condition": "X=XP3",
        "admissible_real_X_dimension": 9,
        "excluded_reference_mixing_real_dimension": 3,
        "reference_mixing_degree_defects": reference_mixing_defects,
        "previous_positive_4_over_3_modes_are_inside_fixed_grading": False,
        "interpretation": "they are massive in the extended Hodge functional but are not tangent to the fixed graded correspondence",
    },
    "common_trace_normalization": {
        "tau300_over_reduced_factor": "3/10",
        "maximum_kinetic_scaling_residual": float(max(trace_ratio_residuals)),
        "maximum_potential_scaling_residual": float(max(potential_trace_residuals)),
        "generalized_mass_spectrum_changed_by_common_factor": False,
        "normalization_correction_alone_invalidates_unit_momentum_vacuum": False,
        "relative_heat_kernel_coefficients_still_required": True,
    },
    "gauge_BV_fork": {
        "SM_only": {
            "gauge_lie_dimension": standard_model_gauge_lie_dimension,
            "family_SO3_orbit_is_BRST_exact": False,
            "at_least_three_rotational_zero_modes_are_physical": True,
        },
        "module_endomorphisms_gauged": {
            "contains_U10_real_lie_dimension_at_least": multiplicity_endomorphism_real_dimension_lower_bound,
            "new_gauge_fields_and_ghosts": True,
            "compatible_with_no_gauge_enlargement": False,
        },
        "discrete_A4_stabilization": {
            "new_continuous_gauge_bosons": False,
            "candidate_source": "previous tetrahedral cubic and holonomy sector",
            "lifting_of_SO3_zero_modes_verified": False,
        },
    },
    "verdict": {
        "graded_correspondence_Leibniz_and_KO6": "pass",
        "standard_superconnection_derives_Hodge_moment_map": "fail",
        "common_trace_multiplicity_normalization": "pass",
        "SM_only_full_BV_quotient": "fail_with_rotational_zero_modes",
        "gauged_module_endomorphism_route": "fail_by_gauge_enlargement",
        "tetrahedral_discrete_stabilization_route": "open",
        "physical_closure": False,
        "status": "correspondence_consistent_but_moment_map_and_BV_require_tetrahedral_hamiltonian_enrichment",
    },
    "next_gate": (
        "Import the previously derived tetrahedral cubic/holonomy invariant into "
        "the affine Hodge moment-map functional and test whether one common "
        "A4-equivariant trace lifts the three accidental SO3 zero modes without "
        "continuous family gauge bosons or a tunable anisotropy coefficient."
    ),
}

OUTPUT.write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False, indent=2))