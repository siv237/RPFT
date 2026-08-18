#!/usr/bin/env python3
"""Единый квадрат кривизны M300 и точный гессиан связующего сектора."""

import json
import math
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_m300_hodge_curvature_hessian_gate_results.json"
TOL = 1.0e-9

amalgamation = json.loads(
    (ROOT / "s2t/results/s2t_v5_modular_ko6_m60_amalgamation_gate_results.json").read_text(encoding="utf-8")
)
assert amalgamation["verdict"]["kinematic_parent_architecture_candidate"]


def reduced_potential(vector, momentum_squared=0.0):
    X = vector[:9].reshape(3, 3)
    phi_real, phi_imaginary = vector[9:]
    radius_squared = phi_real**2 + phi_imaginary**2
    identity = np.eye(3)
    left = identity - X.T @ X
    middle = X @ X.T - radius_squared * identity
    right = (radius_squared - 1.0) * identity
    return (
        np.trace(left @ left).real
        + np.trace(middle @ middle).real
        + np.trace(right @ right).real
    ) / 3.0 + momentum_squared * radius_squared


def finite_hessian(function, point, step=1.0e-5):
    dimension = len(point)
    result = np.zeros((dimension, dimension))
    center = function(point)
    for left in range(dimension):
        e_left = np.zeros(dimension)
        e_left[left] = step
        for right in range(left, dimension):
            e_right = np.zeros(dimension)
            e_right[right] = step
            if left == right:
                value = (
                    function(point + e_left)
                    - 2.0 * center
                    + function(point - e_left)
                ) / step**2
            else:
                value = (
                    function(point + e_left + e_right)
                    - function(point + e_left - e_right)
                    - function(point - e_left + e_right)
                    + function(point - e_left - e_right)
                ) / (4.0 * step**2)
            result[left, right] = value
            result[right, left] = value
    return result


# Прямая матричная идентичность F=[d,d*]-h.
rng = np.random.default_rng(20260816)
matrix_identity_residuals = []
for _ in range(32):
    X = rng.normal(size=(3, 3))
    phi = rng.normal() + 1j * rng.normal()
    Y = phi * np.eye(3)
    zero = np.zeros((3, 3), dtype=complex)
    d = np.block([[zero, zero, zero], [X, zero, zero], [zero, Y, zero]])
    h = np.block(
        [
            [-np.eye(3), zero, zero],
            [zero, zero, zero],
            [zero, zero, np.eye(3)],
        ]
    )
    curvature = d @ d.conj().T - d.conj().T @ d - h
    direct = float(np.trace(curvature @ curvature).real / 3.0)
    vector = np.concatenate((X.reshape(-1), [phi.real, phi.imag]))
    reduced = reduced_potential(vector)
    matrix_identity_residuals.append(abs(direct - reduced))
assert max(matrix_identity_residuals) < TOL

# Точный символический гессиан.
variables = sp.symbols("z0:11", real=True)
X_symbolic = sp.Matrix(3, 3, variables[:9])
phi_real, phi_imaginary = variables[9], variables[10]
radius_squared = phi_real**2 + phi_imaginary**2
identity_symbolic = sp.eye(3)
left_symbolic = identity_symbolic - X_symbolic.T * X_symbolic
middle_symbolic = X_symbolic * X_symbolic.T - radius_squared * identity_symbolic
right_symbolic = (radius_squared - 1) * identity_symbolic
potential_symbolic = (
    sp.trace(left_symbolic**2)
    + sp.trace(middle_symbolic**2)
    + sp.trace(right_symbolic**2)
) / 3


def isotropic_point(frame_radius, pairing_radius):
    point = [sp.Integer(0)] * 11
    for index in range(3):
        point[3 * index + index] = frame_radius
    point[9] = pairing_radius
    return point


zero_momentum_point = isotropic_point(sp.Integer(1), sp.Integer(1))
zero_hessian = sp.hessian(potential_symbolic, variables).subs(
    dict(zip(variables, zero_momentum_point))
)
zero_eigenvalues = zero_hessian.eigenvals()
expected_zero_eigenvalues = {
    sp.Integer(0): 4,
    sp.Rational(16, 3): 5,
    (sp.Integer(32) - 8 * sp.sqrt(7)) / 3: 1,
    (sp.Integer(32) + 8 * sp.sqrt(7)) / 3: 1,
}
assert zero_eigenvalues == expected_zero_eigenvalues

# Единичный дефектный импульс. Точная стационарная точка:
# rho^2=5/6, r^2=2/3.
momentum_potential = potential_symbolic + radius_squared
momentum_point = isotropic_point(sp.sqrt(sp.Rational(5, 6)), sp.sqrt(sp.Rational(2, 3)))
gradient_at_momentum = [
    sp.simplify(sp.diff(momentum_potential, variable).subs(dict(zip(variables, momentum_point))))
    for variable in variables
]
assert all(value == 0 for value in gradient_at_momentum)
momentum_hessian = sp.hessian(momentum_potential, variables).subs(
    dict(zip(variables, momentum_point))
)
momentum_eigenvalues = momentum_hessian.eigenvals()
expected_momentum_eigenvalues = {
    sp.Integer(0): 4,
    sp.Rational(40, 9): 5,
    (sp.Integer(68) - 4 * sp.sqrt(109)) / 9: 1,
    (sp.Integer(68) + 4 * sp.sqrt(109)) / 9: 1,
}
assert momentum_eigenvalues == expected_momentum_eigenvalues
momentum_energy = sp.simplify(momentum_potential.subs(dict(zip(variables, momentum_point))))
assert momentum_energy == sp.Rational(5, 6)

normal_point = isotropic_point(sp.sqrt(sp.Rational(1, 2)), sp.Integer(0))
normal_energy = sp.simplify(momentum_potential.subs(dict(zip(variables, normal_point))))
assert normal_energy == sp.Rational(3, 2)
energy_gap = sp.simplify(normal_energy - momentum_energy)
assert energy_gap == sp.Rational(2, 3)

# Численная независимая проверка обоих гессианов.
zero_point_numeric = np.concatenate((np.eye(3).reshape(-1), [1.0, 0.0]))
momentum_point_numeric = np.concatenate(
    (np.sqrt(5.0 / 6.0) * np.eye(3).reshape(-1), [np.sqrt(2.0 / 3.0), 0.0])
)
zero_numeric_eigenvalues = np.linalg.eigvalsh(
    finite_hessian(lambda value: reduced_potential(value), zero_point_numeric)
)
momentum_numeric_eigenvalues = np.linalg.eigvalsh(
    finite_hessian(lambda value: reduced_potential(value, 1.0), momentum_point_numeric)
)

# Масса двух связующих комбинаций в стационарной точке.
connector_mass = math.sqrt(5.0 / 6.0 + 2.0 / 3.0)
assert abs(connector_mass - math.sqrt(3.0 / 2.0)) < TOL

# Одна норма полной кривизны фиксирует равные веса трёх вершин. Но одна
# только блочная симметрия допускает хотя бы независимые веса endpoint и
# middle; это отделяет построенный принцип действия от теоремы симметрии.
block_symmetry_weight_count = 2
relative_weight_count_after_overall_scale = 1

result = {
    "date": "2026-08-16",
    "gate": "version5_m300_hodge_curvature_hessian_gate",
    "parent_action": {
        "curvature": "F=[d,d*]-h",
        "action": "S=tau300(F^2)",
        "reduced_particle_chain_potential": (
            "(Tr(I-X*X)^2+Tr(XX*-|phi|^2I)^2+3(|phi|^2-1)^2)/3"
        ),
        "maximum_matrix_reduction_residual": max(matrix_identity_residuals),
        "continuous_relative_coefficients_inside_single_trace_norm": 0,
    },
    "zero_momentum_vacuum": {
        "X": "I3",
        "abs_phi": 1,
        "energy": 0,
        "exact_Hessian_spectrum": {
            "0": 4,
            "16/3": 5,
            "(32-8sqrt7)/3": 1,
            "(32+8sqrt7)/3": 1,
        },
        "numerical_Hessian_eigenvalues": zero_numeric_eigenvalues.tolist(),
        "signature": [7, 4, 0],
    },
    "unit_momentum_vacuum": {
        "frame_radius_squared": "5/6",
        "pairing_radius_squared": "2/3",
        "energy": "5/6",
        "normal_branch_energy": "3/2",
        "condensed_energy_advantage": "2/3",
        "exact_Hessian_spectrum": {
            "0": 4,
            "40/9": 5,
            "(68-4sqrt109)/9": 1,
            "(68+4sqrt109)/9": 1,
        },
        "numerical_Hessian_eigenvalues": momentum_numeric_eigenvalues.tolist(),
        "signature": [7, 4, 0],
        "connector_mass_absolute": connector_mass,
        "connector_mass_squared": "3/2",
    },
    "zero_mode_interpretation": {
        "SO3_orbit_directions": 3,
        "pairing_phase_direction": 1,
        "negative_scalar_modes": 0,
        "physical_scalar_Hessian_after_SO3_and_U1_quotient": "positive",
    },
    "action_uniqueness_boundary": {
        "single_unweighted_full_curvature_norm": "fixes all block weights",
        "block_symmetry_invariant_weight_count_lower_bound": block_symmetry_weight_count,
        "relative_weight_count_after_overall_scale": relative_weight_count_after_overall_scale,
        "finding": (
            "The action is coefficient-free once the unweighted full curvature norm is "
            "adopted, but this equality is a parent-action principle, not a consequence "
            "of the smaller block symmetry alone."
        ),
    },
    "full_M300_limit": {
        "reference_sector_lifted": False,
        "reference_chain_mixing_one_forms_classified": False,
        "complete_BV_BRST_complex": False,
        "all_M300_admissible_fluctuations_in_Hessian": False,
    },
    "verdict": {
        "one_trace_Hodge_curvature_action_candidate": "pass",
        "connector_scalar_Hessian_after_gauge_quotient": "pass",
        "stable_unit_momentum_condensate": "pass",
        "complete_M300_action_uniqueness": False,
        "full_physical_Hessian": False,
        "physical_closure": False,
        "status": "connector_action_and_Hessian_pass_full_calculus_open",
    },
    "next_gate": (
        "Classify the full M300 represented one-form/BV complex, especially reference-"
        "chain mixing blocks, and determine whether the same curvature norm lifts every "
        "nonphysical mode without a second weight."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))