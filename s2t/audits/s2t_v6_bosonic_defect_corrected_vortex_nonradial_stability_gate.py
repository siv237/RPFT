#!/usr/bin/env python3
"""Нерадиальный спектр вихря после единой условной нормировки Q/T."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp
from scipy.sparse.linalg import LinearOperator, eigsh


ROOT = Path(__file__).resolve().parents[2]
PROFILE_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_defect_profile_gate.py"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_corrected_vortex_nonradial_stability_gate_results.json"

A = 128.0 / 243.0
B = 160.0 / 243.0
G = 2.0 / 27.0


def corrected_profile():
    old = runpy.run_path(str(PROFILE_AUDIT))
    polynomial = old["POLYNOMIAL"]

    def potential(a, b):
        return sum(c * a**i * b**j for (i, j), c in polynomial.items())

    def derivative_a(a, b):
        return sum(c * i * a ** (i - 1) * b**j for (i, j), c in polynomial.items() if i)

    def derivative_b(a, b):
        return sum(c * j * a**i * b ** (j - 1) for (i, j), c in polynomial.items() if j)

    derivative_a.potential = potential

    def equations(radius, value):
        k, kp, a, ap, b, bp = value
        return np.vstack([
            kp,
            kp / radius - (A / G) * a**2 * (1.0 - k),
            ap,
            -ap / radius + (1.0 - k) ** 2 * a / radius**2 + derivative_a(a, b) / A,
            bp,
            -bp / radius + derivative_b(a, b) / B,
        ])

    def boundary(left, right):
        return np.array([left[0], left[2], left[5], right[0] - 1.0, right[2] - 1.0, right[4] - 1.0])

    radius = np.linspace(1.0e-5, 20.0, 700)
    k = radius**2 / (1.0 + radius**2)
    a = np.tanh(2.0 * radius)
    b = 1.0 + 0.1 * np.exp(-radius**2)
    initial = np.vstack([
        k, np.gradient(k, radius),
        a, np.gradient(a, radius),
        b, np.gradient(b, radius),
    ])
    solution = solve_bvp(equations, boundary, radius, initial, tol=2.0e-7, max_nodes=50000)
    if solution.status != 0:
        raise RuntimeError(solution.message)
    return solution, derivative_a, derivative_b


def calculate(
    solution, derivative_a, derivative_b, grid_size: int,
    box_radius: float = 10.0, eigen_count: int = 10,
    gauge_sign: float = 1.0, return_state: bool = False,
):
    coordinate = np.linspace(-box_radius, box_radius, grid_size)
    spacing = coordinate[1] - coordinate[0]
    xx, yy = np.meshgrid(coordinate, coordinate)
    radius = np.hypot(xx, yy)
    theta = np.arctan2(yy, xx)
    k, a, b = solution.sol(np.maximum(radius, 1.0e-5))[[0, 2, 4]]
    center = radius < 1.0e-12
    k[center] = 0.0
    a[center] = 0.0

    phi1_background = a * np.cos(theta)
    phi2_background = a * np.sin(theta)
    inverse_radius_squared = 1.0 / np.maximum(radius**2, 1.0e-12)
    ax_background = -k * yy * inverse_radius_squared
    ay_background = k * xx * inverse_radius_squared
    background = [phi1_background, phi2_background, ax_background, ay_background, b]

    interior = (slice(1, -1), slice(1, -1))
    interior_size = grid_size - 2
    block_size = interior_size * interior_size
    dimension = 5 * block_size

    def derivative_x(field):
        return (field[1:-1, 2:] - field[1:-1, 1:-1]) / spacing

    def derivative_y(field):
        return (field[2:, 1:-1] - field[1:-1, 1:-1]) / spacing

    def adjoint_x(field):
        result = np.zeros((grid_size, grid_size))
        result[1:-1, 2:] += field / spacing
        result[1:-1, 1:-1] -= field / spacing
        return result[interior]

    def adjoint_y(field):
        result = np.zeros((grid_size, grid_size))
        result[2:, 1:-1] += field / spacing
        result[1:-1, 1:-1] -= field / spacing
        return result[interior]

    def unpack(vector, add_background: bool):
        fields = []
        for field_index in range(5):
            values = vector[field_index * block_size:(field_index + 1) * block_size].reshape(interior_size, interior_size)
            full = background[field_index].copy() if add_background else np.zeros_like(background[field_index])
            full[interior] += values
            fields.append(full)
        return fields

    def pack(fields):
        return np.concatenate([np.asarray(field).reshape(-1) for field in fields])

    def energy_gradient(vector):
        phi1, phi2, ax, ay, neutral = unpack(vector, add_background=True)
        phi1_i, phi2_i = phi1[interior], phi2[interior]
        ax_i, ay_i = ax[interior], ay[interior]

        jphi1, jphi2 = -phi2_i, phi1_i
        px1 = derivative_x(phi1) - ax_i * jphi1
        px2 = derivative_x(phi2) - ax_i * jphi2
        py1 = derivative_y(phi1) - ay_i * jphi1
        py2 = derivative_y(phi2) - ay_i * jphi2

        gphi1 = A * (adjoint_x(px1) + adjoint_y(py1) - ax_i * px2 - ay_i * py2)
        gphi2 = A * (adjoint_x(px2) + adjoint_y(py2) + ax_i * px1 + ay_i * py1)
        gax = -A * (jphi1 * px1 + jphi2 * px2)
        gay = -A * (jphi1 * py1 + jphi2 * py2)
        curvature = derivative_x(ay) - derivative_y(ax)
        gax -= adjoint_y(G * curvature)
        gay += adjoint_x(G * curvature)
        gneutral = B * (adjoint_x(derivative_x(neutral)) + adjoint_y(derivative_y(neutral)))

        amplitude = np.sqrt(phi1_i**2 + phi2_i**2)
        safe_amplitude = np.maximum(amplitude, 1.0e-12)
        va = derivative_a(amplitude, neutral[interior])
        vb = derivative_b(amplitude, neutral[interior])
        gphi1 += va * phi1_i / safe_amplitude
        gphi2 += va * phi2_i / safe_amplitude
        gneutral += vb
        return spacing**2 * pack([gphi1, gphi2, gax, gay, gneutral])

    def physical_energy(vector):
        phi1, phi2, ax, ay, neutral = unpack(vector, add_background=True)
        phi1_i, phi2_i = phi1[interior], phi2[interior]
        ax_i, ay_i = ax[interior], ay[interior]
        jphi1, jphi2 = -phi2_i, phi1_i
        px1 = derivative_x(phi1) - ax_i * jphi1
        px2 = derivative_x(phi2) - ax_i * jphi2
        py1 = derivative_y(phi1) - ay_i * jphi1
        py2 = derivative_y(phi2) - ay_i * jphi2
        curvature = derivative_x(ay) - derivative_y(ax)
        neutral_x = derivative_x(neutral)
        neutral_y = derivative_y(neutral)
        amplitude = np.sqrt(phi1_i**2 + phi2_i**2)
        density = (
            0.5 * A * (px1**2 + px2**2 + py1**2 + py2**2)
            + 0.5 * B * (neutral_x**2 + neutral_y**2)
            + 0.5 * G * curvature**2
            + derivative_a.potential(amplitude, neutral[interior])
        )
        return float(spacing**2 * np.sum(density))

    zero = np.zeros(dimension)
    phi1_i, phi2_i = phi1_background[interior], phi2_background[interior]
    gauge_coefficient = A / G

    def gauge_fixing_hessian(vector):
        eta1, eta2, dax, day, _ = unpack(vector, add_background=False)
        condition = (
            derivative_x(dax) + derivative_y(day)
            + gauge_sign * gauge_coefficient
            * (-phi2_i * eta1[interior] + phi1_i * eta2[interior])
        )
        return spacing**2 * pack([
            -gauge_sign * A * phi2_i * condition,
            gauge_sign * A * phi1_i * condition,
            adjoint_x(G * condition),
            adjoint_y(G * condition),
            np.zeros_like(condition),
        ])

    base_gradient = energy_gradient(zero)
    finite_difference_step = 2.0e-5

    def hessian_action(vector):
        plus = energy_gradient(finite_difference_step * vector)
        minus = energy_gradient(-finite_difference_step * vector)
        return (plus - minus) / (2.0 * finite_difference_step) + gauge_fixing_hessian(vector)

    metric_weights = np.repeat(np.array([A, A, G, G, B]) * spacing**2, block_size)
    inverse_sqrt_metric = 1.0 / np.sqrt(metric_weights)

    def normalized_action(vector):
        physical = inverse_sqrt_metric * vector
        return inverse_sqrt_metric * hessian_action(physical)

    operator = LinearOperator((dimension, dimension), matvec=normalized_action, dtype=float)
    eigenvalues, eigenvectors = eigsh(
        operator, k=eigen_count, which="SA", tol=3.0e-6,
        maxiter=3000, ncv=max(32, 4 * eigen_count + 1),
        return_eigenvectors=True,
    )
    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    translation_x = pack([
        -derivative_x(phi1_background), -derivative_x(phi2_background),
        -derivative_x(ax_background), -derivative_x(ay_background), -derivative_x(b),
    ])
    translation_y = pack([
        -derivative_y(phi1_background), -derivative_y(phi2_background),
        -derivative_y(ax_background), -derivative_y(ay_background), -derivative_y(b),
    ])
    naive_overlaps = []
    for tangent in (translation_x, translation_y):
        normalized = np.sqrt(metric_weights) * tangent
        normalized /= np.linalg.norm(normalized)
        naive_overlaps.append(float(np.linalg.norm(eigenvectors[:, :4].T @ normalized) ** 2))

    # Перенос, дополненный калибровочным преобразованием с параметром A_j:
    # delta_j phi=-D_j phi, delta_j A_i=-partial_j A_i+partial_i A_j.
    # На точном решении он удовлетворяет фоновой калибровке по уравнению
    # связности и является правильной геометрической нулевой модой.
    jphi1_background = -phi2_background[interior]
    jphi2_background = phi1_background[interior]
    covariant_x_phi1 = derivative_x(phi1_background) - ax_background[interior] * jphi1_background
    covariant_x_phi2 = derivative_x(phi2_background) - ax_background[interior] * jphi2_background
    covariant_y_phi1 = derivative_y(phi1_background) - ay_background[interior] * jphi1_background
    covariant_y_phi2 = derivative_y(phi2_background) - ay_background[interior] * jphi2_background
    curvature_background = derivative_x(ay_background) - derivative_y(ax_background)
    covariant_translation_x = pack([
        -gauge_sign * covariant_x_phi1, -gauge_sign * covariant_x_phi2,
        np.zeros_like(curvature_background), -curvature_background, -derivative_x(b),
    ])
    covariant_translation_y = pack([
        -gauge_sign * covariant_y_phi1, -gauge_sign * covariant_y_phi2,
        curvature_background, np.zeros_like(curvature_background), -derivative_y(b),
    ])
    covariant_overlaps_four = []
    covariant_overlaps_eight = []
    covariant_rayleigh = []
    for tangent in (covariant_translation_x, covariant_translation_y):
        normalized = np.sqrt(metric_weights) * tangent
        normalized /= np.linalg.norm(normalized)
        covariant_overlaps_four.append(float(np.linalg.norm(eigenvectors[:, :4].T @ normalized) ** 2))
        covariant_overlaps_eight.append(float(np.linalg.norm(eigenvectors[:, :8].T @ normalized) ** 2))
        covariant_rayleigh.append(float(
            np.dot(tangent, hessian_action(tangent)) / np.dot(tangent, metric_weights * tangent)
        ))

    mode_block_weights = []
    for mode in range(eigenvectors.shape[1]):
        vector = eigenvectors[:, mode]
        mode_block_weights.append({
            "charged_scalar": float(np.dot(vector[:2 * block_size], vector[:2 * block_size])),
            "gauge_field": float(np.dot(vector[2 * block_size:4 * block_size], vector[2 * block_size:4 * block_size])),
            "neutral_scalar": float(np.dot(vector[4 * block_size:], vector[4 * block_size:])),
        })

    result = {
        "grid_size": grid_size,
        "gauge_sign": gauge_sign,
        "box_radius": box_radius,
        "spacing": float(spacing),
        "dimension": dimension,
        "background_discrete_gradient_rms": float(np.linalg.norm(base_gradient) / np.sqrt(dimension)),
        "eigenvalues": eigenvalues.tolist(),
        "naive_translation_first_four_overlaps": naive_overlaps,
        "covariant_translation_first_four_overlaps": covariant_overlaps_four,
        "covariant_translation_first_eight_overlaps": covariant_overlaps_eight,
        "covariant_translation_rayleigh_quotients": covariant_rayleigh,
        "mode_block_weights": mode_block_weights,
    }
    if return_state:
        result["_state"] = {
            "background_vector": zero,
            "physical_energy": physical_energy,
            "physical_gradient": energy_gradient,
            "base_gradient": base_gradient,
            "gauge_fixing_action": gauge_fixing_hessian,
            "metric_weights": metric_weights,
            "inverse_sqrt_metric": inverse_sqrt_metric,
            "normalized_eigenvectors": eigenvectors,
            "hessian_action": hessian_action,
            "unpack_fields": lambda vector: unpack(vector, add_background=True),
            "coordinate": coordinate,
            "spacing": spacing,
            "interior_slice": interior,
        }
    return result


def main() -> None:
    solution, derivative_a, derivative_b = corrected_profile()
    grids = [24, 32, 40, 48, 56]
    spectra = {
        str(grid): calculate(solution, derivative_a, derivative_b, grid, eigen_count=8)
        for grid in grids
    }
    finest = np.array(spectra["56"]["eigenvalues"])
    previous = np.array(spectra["48"]["eigenvalues"])
    third_mode_ratio = float(finest[2] / previous[2])
    dispersion = {str(kz): float(finest[0] + kz * kz) for kz in [0.0, 0.25, 0.5, 1.0, 2.0]}

    result = {
        "gate": "version6_bosonic_defect_corrected_vortex_nonradial_stability_gate",
        "corrected_normalization": {"A": A, "B": B, "G": G, "A_over_G": A / G},
        "operator": {
            "sector": "effective charged amplitude + neutral amplitude + two transverse gauge components",
            "coordinate_system": "Cartesian",
            "gauge_fixing": "background gauge div(delta A)+(A/G)(J phi0).delta phi=0",
            "finite_difference_hessian_step": 2.0e-5,
            "spectra": spectra,
        },
        "stability": {
            "finest_eigenvalues": finest.tolist(),
            "negative_mode_count_checked": int(np.sum(finest < -2.0e-2)),
            "near_zero_mode_count_at_finest_grid": int(np.sum(np.abs(finest) < 3.0e-2)),
            "soft_modes_rigorously_identified": False,
            "minimum_checked_eigenvalue": float(finest[0]),
            "minimum_drift_48_to_56": float(abs(finest[0] - previous[0])),
            "third_mode_ratio_56_over_48": third_mode_ratio,
            "longitudinal_dispersion_samples_for_lowest_finite_grid_mode": dispersion,
            "positive_gap_converged": False,
        },
        "boundary": {
            "effective_abelian_subsystem_checked": True,
            "translation_zero_modes_rigorously_resolved": False,
            "all_spin2_components_checked": False,
            "all_spin3_components_checked": False,
            "full_nonabelian_gauge_fixed_hessian_checked": False,
            "closed_loop_stability_checked": False,
            "hopf_identification_checked": False,
            "absolute_scale_derived": False,
        },
        "verdict": {
            "negative_mode_found_in_checked_effective_sector": bool(np.any(finest < -2.0e-2)),
            "checked_effective_sector_is_numerically_nonnegative": bool(np.all(finest >= -2.0e-2)),
            "nonradial_stability_certificate_passes": False,
            "reason": "more than two modes collapse toward zero under grid refinement",
            "full_vortex_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_corrected_vortex_covariant_zero_mode_resolution_gate",
        },
    }
    assert result["stability"]["negative_mode_count_checked"] == 0
    assert result["stability"]["near_zero_mode_count_at_finest_grid"] >= 6
    assert result["stability"]["third_mode_ratio_56_over_48"] < 0.2
    assert not result["verdict"]["nonradial_stability_certificate_passes"]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()