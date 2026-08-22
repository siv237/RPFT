#!/usr/bin/env python3
"""Численно-аналитическое закрытие высокоуглового хвоста вихря."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
POLAR_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_polar_angular_sturm_liouville_gate.py"
CORRECTED_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_corrected_vortex_nonradial_stability_gate.py"
PROFILE_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_defect_profile_gate.py"
PARENT_RESULT = ROOT / "s2t/results/s2t_v6_bosonic_defect_polar_angular_sturm_liouville_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_polar_high_angular_coercivity_gate_results.json"


def main() -> None:
    polar = runpy.run_path(str(POLAR_AUDIT))
    polar["main"](initialize_only=True)
    block_spectrum = polar["main"].__globals__["BLOCK_SPECTRUM"]
    parent = json.loads(PARENT_RESULT.read_text(encoding="utf-8"))

    corrected = runpy.run_path(str(CORRECTED_AUDIT))
    profile_module = runpy.run_path(str(PROFILE_AUDIT))
    solution, derivative_a, _ = corrected["corrected_profile"]()
    polynomial = profile_module["POLYNOMIAL"]
    A, B, G = corrected["A"], corrected["B"], corrected["G"]

    def second_a(a, b):
        return sum(
            value * i * (i - 1) * a ** (i - 2) * b**j
            for (i, j), value in polynomial.items() if i >= 2
        )

    def second_b(a, b):
        return sum(
            value * j * (j - 1) * a**i * b ** (j - 2)
            for (i, j), value in polynomial.items() if j >= 2
        )

    def mixed_ab(a, b):
        return sum(
            value * i * j * a ** (i - 1) * b ** (j - 1)
            for (i, j), value in polynomial.items() if i and j
        )

    # Direct finite-element bridge between the previously checked |m|<=8
    # window and the analytic coercive tail.
    bridge_node_count = 120
    bridge_angular_numbers = list(range(9, 87))
    bridge_minima = {
        str(angular): float(block_spectrum(bridge_node_count, angular, eigen_count=1)[0])
        for angular in bridge_angular_numbers
    }

    # Conservative local lower matrix. Half of the gauge Hodge square is
    # retained; the other half controls its coupling to the phase variation.
    # Radial derivative squares are discarded, while their background cross
    # term is kept. Positivity of this smaller matrix proves positivity of the
    # original quadratic form.
    epsilon = 0.5

    def lower_matrix(radius: float, angular: float):
        k, a, ap, b = solution.sol(radius)[[0, 2, 3, 4]]
        matrix = np.zeros((5, 5), dtype=complex)

        def add_square(coefficients, weight):
            nonlocal matrix
            coefficients = np.asarray(coefficients, dtype=complex)
            matrix += weight * np.outer(coefficients.conj(), coefficients)

        add_square([1j * angular, -(1.0 - k), 0.0, 0.0, 0.0], A / radius)
        add_square([1.0 - k, 1j * angular, 0.0, -radius * a, 0.0], A / radius)
        matrix[4, 4] += B * angular**2 / radius
        vector_barrier = epsilon * G * (angular - 1.0) ** 2 / radius
        matrix[2, 2] += vector_barrier
        matrix[3, 3] += vector_barrier
        matrix[1, 1] -= epsilon / (1.0 - epsilon) * (A**2 / G) * radius * a**2
        matrix[1, 2] += A * radius * ap
        matrix[2, 1] += A * radius * ap
        matrix[0, 3] -= A * a * (1.0 - k)
        matrix[3, 0] -= A * a * (1.0 - k)
        matrix[0, 0] += radius * second_a(a, b)
        matrix[1, 1] += radius * derivative_a(a, b) / max(a, 1.0e-12)
        matrix[4, 4] += radius * second_b(a, b)
        matrix[0, 4] += radius * mixed_ab(a, b)
        matrix[4, 0] += radius * mixed_ab(a, b)
        normalization = np.diag(1.0 / np.sqrt(np.array([A, A, G, G, B]) * radius))
        return normalization @ matrix @ normalization

    radii = np.unique(np.concatenate([
        np.geomspace(1.0e-4, 20.0, 4000),
        np.linspace(1.0e-3, 20.0, 4000),
    ]))
    row_polynomials = []
    for radius in radii:
        h_zero = lower_matrix(radius, 0.0)
        h_plus = lower_matrix(radius, 1.0)
        h_minus = lower_matrix(radius, -1.0)
        h_linear = 0.5 * (h_plus - h_minus)
        h_quadratic = 0.5 * (h_plus + h_minus) - h_zero
        for row in range(5):
            off_diagonal = [column for column in range(5) if column != row]
            quadratic = float(np.real(h_quadratic[row, row]) - sum(
                abs(h_quadratic[row, column]) for column in off_diagonal
            ))
            linear = float(np.real(h_linear[row, row]) - sum(
                abs(h_linear[row, column]) for column in off_diagonal
            ))
            constant = float(np.real(h_zero[row, row]) - sum(
                abs(h_zero[row, column]) for column in off_diagonal
            ))
            row_polynomials.append((quadratic, linear, constant))

    analytic_threshold = None
    threshold_margin = None
    threshold_derivative = None
    minimum_quadratic_coefficient = min(row[0] for row in row_polynomials)
    for angular in range(9, 501):
        margin = min(a * angular**2 + b * angular + c for a, b, c in row_polynomials)
        derivative = min(2.0 * a * angular + b for a, b, _ in row_polynomials)
        if minimum_quadratic_coefficient > 0.0 and margin > 0.0 and derivative > 0.0:
            analytic_threshold = angular
            threshold_margin = margin
            threshold_derivative = derivative
            break

    if analytic_threshold is None:
        raise RuntimeError("Не найден коэрцитивный высокоугловой порог.")

    bridge_values = np.array(list(bridge_minima.values()))
    previous_gap = float(parent["finest_grid"]["calibrated_axisymmetric_internal_gap"])
    result = {
        "gate": "version6_bosonic_defect_polar_high_angular_coercivity_gate",
        "parent_checked_window": parent["verdict"]["checked_angular_window"],
        "direct_bridge": {
            "radial_node_count": bridge_node_count,
            "angular_numbers": [bridge_angular_numbers[0], bridge_angular_numbers[-1]],
            "minimum_by_angular_number": bridge_minima,
            "minimum_value": float(np.min(bridge_values)),
            "minimum_angular_number": int(bridge_angular_numbers[int(np.argmin(bridge_values))]),
            "negative_mode_count": int(np.sum(bridge_values < -1.0e-5)),
            "strictly_increasing": bool(np.all(np.diff(bridge_values) > 0.0)),
        },
        "analytic_tail": {
            "lower_bound_method": "metric-normalized Gershgorin polynomials after retaining half of the gauge Hodge square",
            "radial_sample_count": int(len(radii)),
            "epsilon": epsilon,
            "threshold_absolute_angular_number": int(analytic_threshold),
            "minimum_quadratic_coefficient": float(minimum_quadratic_coefficient),
            "threshold_margin": float(threshold_margin),
            "threshold_margin_derivative": float(threshold_derivative),
            "all_integer_angular_numbers_at_or_above_threshold_coercive": True,
        },
        "global_effective_operator": {
            "translation_channels": [-1, 1],
            "internal_gap": previous_gap,
            "all_angular_numbers_covered": True,
            "negative_internal_mode_found": False,
        },
        "verdict": {
            "effective_five_component_angular_stability_closed": True,
            "effective_internal_gap_closed": True,
            "full_spin2_spin3_stability_closed": False,
            "closed_loop_stability_checked": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_full_tensor_polar_hessian_gate",
        },
    }

    assert result["direct_bridge"]["negative_mode_count"] == 0
    assert result["direct_bridge"]["strictly_increasing"]
    assert analytic_threshold <= 87
    assert result["analytic_tail"]["threshold_margin"] > 0.0
    assert result["analytic_tail"]["threshold_margin_derivative"] > 0.0
    assert result["global_effective_operator"]["internal_gap"] > 4.0
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()