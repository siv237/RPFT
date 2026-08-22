#!/usr/bin/env python3
"""Нерадиальный спектр эффективного Z6-вихря Q+T+B.

В отличие от полярного амплитудного сокращения этот аудит сохраняет фазу
заряженного поля и обе поперечные компоненты связности. На декартовой
сетке добавляется фоновая калибровка, поэтому переносные моды отделяются
от чистых калибровочных направлений без сингулярного выбора фазы в ядре.
"""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh


ROOT = Path(__file__).resolve().parents[2]
PROFILE_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_defect_profile_gate.py"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_q_tetrahedral_vortex_angular_stability_gate_results.json"


def main() -> None:
    module = runpy.run_path(str(PROFILE_AUDIT))
    solution = module["solve_profile"]()
    A, B, G = module["A"], module["B"], module["G"]
    derivative_a = module["derivative_a"]
    derivative_b = module["derivative_b"]

    def calculate(grid_size: int, box_radius: float = 10.0, eigen_count: int = 10):
        if grid_size % 2:
            raise ValueError("Чётная сетка нужна, чтобы не помещать сингулярную полярную карту в один узел.")
        coordinate = np.linspace(-box_radius, box_radius, grid_size)
        spacing = coordinate[1] - coordinate[0]
        xx, yy = np.meshgrid(coordinate, coordinate)
        radius = np.hypot(xx, yy)
        theta = np.arctan2(yy, xx)
        k, a, b = solution.sol(np.maximum(radius, 1.0e-5))[[0, 2, 4]]

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

            gphi1 = A * (adjoint_x(px1) + adjoint_y(py1))
            gphi2 = A * (adjoint_x(px2) + adjoint_y(py2))
            # Транспонированное действие -A_i J равно +A_i J.
            gphi1 += A * (-ax_i * px2 - ay_i * py2)
            gphi2 += A * (ax_i * px1 + ay_i * py1)

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

            factor = spacing**2
            return factor * pack([gphi1, gphi2, gax, gay, gneutral])

        zero = np.zeros(dimension)
        phi1_i = phi1_background[interior]
        phi2_i = phi2_background[interior]
        gauge_coefficient = A / G

        def gauge_fixing_hessian(vector):
            eta1, eta2, dax, day, _ = unpack(vector, add_background=False)
            eta1_i, eta2_i = eta1[interior], eta2[interior]
            condition = (
                derivative_x(dax) + derivative_y(day)
                + gauge_coefficient * (-phi2_i * eta1_i + phi1_i * eta2_i)
            )
            geta1 = -A * phi2_i * condition
            geta2 = A * phi1_i * condition
            gdax = adjoint_x(G * condition)
            gday = adjoint_y(G * condition)
            gneutral = np.zeros_like(condition)
            return spacing**2 * pack([geta1, geta2, gdax, gday, gneutral])

        base_gradient = energy_gradient(zero)
        finite_difference_step = 2.0e-5

        def hessian_action(vector):
            plus = energy_gradient(finite_difference_step * vector)
            minus = energy_gradient(-finite_difference_step * vector)
            return (plus - minus) / (2.0 * finite_difference_step) + gauge_fixing_hessian(vector)

        metric_weights = np.repeat(
            np.array([A, A, G, G, B]) * spacing**2,
            block_size,
        )
        inverse_sqrt_metric = 1.0 / np.sqrt(metric_weights)

        def normalized_action(vector):
            physical = inverse_sqrt_metric * vector
            return inverse_sqrt_metric * hessian_action(physical)

        operator = LinearOperator((dimension, dimension), matvec=normalized_action, dtype=float)
        eigenvalues, eigenvectors = eigsh(
            operator, k=eigen_count, which="SA", tol=3.0e-6,
            maxiter=1800, return_eigenvectors=True,
        )
        order = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[order]
        eigenvectors = eigenvectors[:, order]

        # Переносные касательные строятся непосредственным дифференцированием
        # гладкого декартова фона и сравниваются с низшим собственным подпространством.
        translation_x = pack([
            -derivative_x(phi1_background), -derivative_x(phi2_background),
            -derivative_x(ax_background), -derivative_x(ay_background), -derivative_x(b),
        ])
        translation_y = pack([
            -derivative_y(phi1_background), -derivative_y(phi2_background),
            -derivative_y(ax_background), -derivative_y(ay_background), -derivative_y(b),
        ])
        translations = []
        for tangent in (translation_x, translation_y):
            normalized = np.sqrt(metric_weights) * tangent
            normalized /= np.linalg.norm(normalized)
            translations.append(normalized)
        low_space = eigenvectors[:, :4]
        overlaps = [float(np.linalg.norm(low_space.T @ tangent) ** 2) for tangent in translations]

        residual_norm = float(np.linalg.norm(base_gradient) / np.sqrt(dimension))
        return {
            "grid_size": grid_size,
            "box_radius": box_radius,
            "spacing": float(spacing),
            "dimension": dimension,
            "background_discrete_gradient_rms": residual_norm,
            "eigenvalues": eigenvalues.tolist(),
            "translation_low_space_overlaps": overlaps,
        }

    grids = [24, 32, 40, 48]
    spectra = {str(grid): calculate(grid) for grid in grids}
    finest = np.array(spectra["48"]["eigenvalues"])
    previous = np.array(spectra["40"]["eigenvalues"])

    # Две низшие моды мягчают при измельчении сетки. Они являются кандидатами
    # на решёточно поднятые переносы, но вычисленный overlap пока недостаточен
    # для строгого отождествления. Отдельно фиксируется устойчивый зазор над ними.
    physical_minimum = float(finest[2])
    longitudinal_wave_numbers = [0.0, 0.25, 0.5, 1.0, 2.0]
    dispersion = {str(kz): physical_minimum + kz * kz for kz in longitudinal_wave_numbers}

    result = {
        "gate": "version6_bosonic_defect_q_tetrahedral_vortex_angular_stability_gate",
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
            "soft_lattice_mode_count": 2,
            "soft_pair_rigorously_identified_as_translations": False,
            "minimum_checked_eigenvalue": float(finest[0]),
            "minimum_hard_sector_eigenvalue": physical_minimum,
            "hard_sector_drift_40_to_48": float(abs(finest[2] - previous[2])),
            "hard_sector_longitudinal_dispersion_samples": dispersion,
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
            "full_vortex_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_q_tetrahedral_vortex_full_hessian_gate",
        },
    }
    assert result["stability"]["negative_mode_count_checked"] == 0
    assert result["stability"]["minimum_checked_eigenvalue"] > 0.5
    assert result["stability"]["minimum_hard_sector_eigenvalue"] > 1.4
    assert result["stability"]["hard_sector_drift_40_to_48"] < 1.0e-3
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()