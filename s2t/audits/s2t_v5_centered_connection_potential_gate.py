#!/usr/bin/env python3
"""Динамический аудит потенциалов центрированной физической связности."""

import json
from pathlib import Path

import numpy as np
from scipy.linalg import null_space
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_centered_connection_potential_gate_results.json"
TOL = 1.0e-8
BLOCK_NAMES = ["Q_L", "L_L", "u_R", "d_R", "e_R"]
BLOCK_SIZES = np.array([6, 2, 3, 3, 1], dtype=float)
WEIGHTS = BLOCK_SIZES / np.sum(BLOCK_SIZES)


classification = json.loads(
    (
        ROOT
        / "s2t/results/s2t_v5_physical_corner_connection_classification_gate_results.json"
    ).read_text(encoding="utf-8")
)
assert classification["verdict"]["minimum_centered_ambiguity_dimension"] == 4
assert not classification["verdict"]["unique_Yukawa_connection"]

# Центрированное пространство: sum_s w_s z_s=0.
centered_basis = null_space(WEIGHTS.reshape(1, -1)).astype(complex)
center_residual = float(np.max(np.abs(WEIGHTS @ centered_basis)))
assert centered_basis.shape == (5, 4)
assert center_residual < TOL


def invariants(real_coordinates):
    """Пять блочных квадратичных инвариантов I_s=w_s |z_s|^2."""
    coordinates = real_coordinates[:4] + 1j * real_coordinates[4:]
    z = centered_basis @ coordinates
    return WEIGHTS * np.abs(z) ** 2


# Все пять I_s остаются линейно независимыми после центрирования.
quadratic_forms = []
for index, weight in enumerate(WEIGHTS):
    projector = np.zeros((5, 5), dtype=complex)
    projector[index, index] = weight
    form = centered_basis.conj().T @ projector @ centered_basis
    quadratic_forms.append(form)
quadratic_form_matrix = np.stack(
    [
        np.concatenate([form.real.reshape(-1), form.imag.reshape(-1)])
        for form in quadratic_forms
    ]
)
quadratic_invariant_rank = int(np.linalg.matrix_rank(quadratic_form_matrix, tol=TOL))

# Квартичные произведения I_s I_t также независимы как функции на общем
# наборе точек центрированного пространства.
rng = np.random.default_rng(20260816)
samples = rng.normal(size=(160, 8))
quadratic_values = np.array([invariants(sample) for sample in samples])
quartic_pairs = [(first, second) for first in range(5) for second in range(first, 5)]
quartic_values = np.array(
    [
        [values[first] * values[second] for first, second in quartic_pairs]
        for values in quadratic_values
    ]
)
quartic_invariant_rank = int(np.linalg.matrix_rank(quartic_values, tol=TOL))

# Даже если запретить блочные коэффициенты и оставить только следовые моменты,
# p1, p1^2 и p2 являются независимыми.
p1 = np.sum(quadratic_values, axis=1)
p2 = np.sum((quadratic_values**2) / WEIGHTS.reshape(1, -1), axis=1)
trace_invariant_matrix = np.column_stack([p1, p1**2, p2])
trace_quartic_rank = int(np.linalg.matrix_rank(trace_invariant_matrix, tol=TOL))


def closure_objective(phases):
    z = np.exp(1j * phases)
    return float(abs(WEIGHTS @ z) ** 2)


# Ищем два различных нулевых минимума наиболее благоприятного
# выравнивающего функционала sum w_s (|z_s|^2-1)^2.
flat_minima = []
for seed in range(64):
    local_rng = np.random.default_rng(seed)
    solution = minimize(
        closure_objective,
        local_rng.uniform(-np.pi, np.pi, 5),
        method="BFGS",
        options={"gtol": 1.0e-12, "maxiter": 5000},
    )
    if solution.fun > 1.0e-16:
        continue
    z = np.exp(1j * (solution.x - solution.x[0]))
    if not flat_minima:
        flat_minima.append(z)
        continue
    overlaps = [
        abs(np.vdot(existing, z)) / (np.linalg.norm(existing) * np.linalg.norm(z))
        for existing in flat_minima
    ]
    if max(overlaps) < 1.0 - 1.0e-4:
        flat_minima.append(z)
    if len(flat_minima) == 2:
        break

assert len(flat_minima) == 2
flat_center_residuals = [float(abs(WEIGHTS @ z)) for z in flat_minima]
flat_potential_values = [
    float(np.sum(WEIGHTS * (np.abs(z) ** 2 - 1.0) ** 2)) for z in flat_minima
]

# Точный гессиан выравнивающего функционала на центрированном пространстве.
# При |z_s|=1 вторая вариация равна
# 8 sum_s w_s Re(conj(z_s) delta z_s)^2.
z0 = flat_minima[0]
real_map = np.block(
    [
        [centered_basis.real, -centered_basis.imag],
        [centered_basis.imag, centered_basis.real],
    ]
)
jacobian = np.zeros((5, 8))
for index, value in enumerate(z0):
    row = np.zeros(10)
    row[index] = value.real
    row[5 + index] = value.imag
    jacobian[index] = row @ real_map
flat_hessian = 8.0 * jacobian.T @ np.diag(WEIGHTS) @ jacobian
flat_hessian_eigenvalues = np.linalg.eigvalsh(flat_hessian)
flat_hessian_nullity = int(np.sum(np.abs(flat_hessian_eigenvalues) < 1.0e-7))

# V=(p1-rho)^2 имеет минимум на сфере в C^4: один радиальный и семь
# касательных вещественных направлений.
test_point = rng.normal(size=8)
test_point /= np.sqrt(np.sum(invariants(test_point)))
epsilon = 1.0e-6


def sphere_potential(point):
    return float((np.sum(invariants(point)) - 1.0) ** 2)


sphere_hessian = np.zeros((8, 8))
origin_value = sphere_potential(test_point)
for first in range(8):
    e_first = np.zeros(8)
    e_first[first] = epsilon
    sphere_hessian[first, first] = (
        sphere_potential(test_point + e_first)
        - 2.0 * origin_value
        + sphere_potential(test_point - e_first)
    ) / epsilon**2
    for second in range(first):
        e_second = np.zeros(8)
        e_second[second] = epsilon
        sphere_hessian[first, second] = sphere_hessian[second, first] = (
            sphere_potential(test_point + e_first + e_second)
            - sphere_potential(test_point + e_first - e_second)
            - sphere_potential(test_point - e_first + e_second)
            + sphere_potential(test_point - e_first - e_second)
        ) / (4.0 * epsilon**2)
sphere_hessian_eigenvalues = np.linalg.eigvalsh(sphere_hessian)
sphere_hessian_nullity = int(np.sum(np.abs(sphere_hessian_eigenvalues) < 1.0e-4))

assert quadratic_invariant_rank == 5
assert quartic_invariant_rank == 15
assert trace_quartic_rank == 3
assert max(flat_center_residuals) < TOL
assert max(flat_potential_values) < TOL
assert flat_hessian_nullity == 3
assert sphere_hessian_nullity == 7

result = {
    "gate": "version5_centered_connection_potential_gate",
    "input_certificate": {
        "centered_connection_complex_dimension": 4,
        "unique_Yukawa_connection_before_dynamics": False,
    },
    "centered_space": {
        "block_names": BLOCK_NAMES,
        "block_sizes": BLOCK_SIZES.astype(int).tolist(),
        "trace_weights": WEIGHTS.tolist(),
        "constraint": "sum_s w_s z_s = 0",
        "complex_dimension": int(centered_basis.shape[1]),
        "real_dimension": int(2 * centered_basis.shape[1]),
        "basis_residual": center_residual,
    },
    "general_even_phase_blind_potential": {
        "independent_quadratic_invariants": quadratic_invariant_rank,
        "independent_quartic_products": quartic_invariant_rank,
        "real_coefficients_through_degree_four": (
            quadratic_invariant_rank + quartic_invariant_rank
        ),
        "form": (
            "V=sum_s m_s I_s + sum_{s<=t} lambda_st I_s I_t, "
            "I_s=w_s |z_s|^2"
        ),
        "coefficients_fixed_by_current_symmetry": False,
    },
    "trace_only_restriction": {
        "independent_invariants_through_degree_four": trace_quartic_rank,
        "basis": ["p1", "p1^2", "p2"],
        "general_form": "a p1+b p1^2+c p2+constant",
        "dimensionless_coefficient_ratios_after_overall_normalization": 2,
        "positive_parent_norm_minimum": "z=0",
    },
    "radial_trace_potential": {
        "functional": "(p1-1)^2",
        "minimum_manifold": "weighted sphere in centered C^4",
        "hessian_eigenvalues": sphere_hessian_eigenvalues.tolist(),
        "hessian_nullity": sphere_hessian_nullity,
        "unique_orbit": False,
    },
    "unitary_flattening_best_case": {
        "functional": "sum_s w_s (|z_s|^2-1)^2",
        "external_unit_scale_required": True,
        "number_of_distinct_certified_minima": len(flat_minima),
        "center_residuals": flat_center_residuals,
        "potential_values": flat_potential_values,
        "representative_phases": [np.angle(z).tolist() for z in flat_minima],
        "hessian_eigenvalues": flat_hessian_eigenvalues.tolist(),
        "hessian_nullity": flat_hessian_nullity,
        "minimum_manifold_real_dimension": flat_hessian_nullity,
        "unique_orbit": False,
    },
    "moment_map_level": {
        "block_center_real_dimension": 5,
        "trace_zero_level_real_dimension": 4,
        "canonical_nonzero_level_from_current_data": False,
        "interpretation": (
            "a nonzero central moment-map level would reintroduce the same "
            "four relative block choices"
        ),
    },
    "verdict": {
        "current_parent_quadratic_norm_selects_nonzero_connection": False,
        "symmetry_fixes_general_quartic_coefficients": False,
        "trace_only_quartic_selects_unique_orbit": False,
        "flattening_selects_unique_orbit": False,
        "unique_Yukawa_connection": False,
        "Yukawa_origin_status": "underdetermined",
        "Morita_carrier_status": "retained as kinematics",
        "physical_closure": False,
    },
    "next_step": (
        "Freeze the origin of the Yukawa connection within the present Morita "
        "parent architecture. Any reopening must add and independently derive "
        "a symmetry, moment-map level, spectral profile, or fermionic principle "
        "that fixes the four relative block directions."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))