#!/usr/bin/env python3
"""Audit the metastability and kinetic regimes of the projective transition."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def entropy(axis: float) -> float:
    transverse = 0.5 * (1.0 - axis)
    return float(axis * np.log(axis) + 2.0 * transverse * np.log(transverse))


def energy(axis: float) -> float:
    second = 0.5 * (3.0 * axis**2 - 2.0 * axis + 1.0)
    third = 0.25 * (3.0 * axis**3 + 3.0 * axis**2 - 3.0 * axis + 1.0)
    radial = (2.0 / 7.0) * (1.0 - second**2 / third)
    exterior = 1.0 - second
    return float(radial + exterior)


def entropy_prime(axis: float) -> float:
    return float(np.log(2.0 * axis / (1.0 - axis)))


def entropy_second(axis: float) -> float:
    return float(1.0 / axis + 1.0 / (1.0 - axis))


def energy_derivatives(axis: float) -> tuple[float, float]:
    second = 0.5 * (3.0 * axis**2 - 2.0 * axis + 1.0)
    second_prime = 3.0 * axis - 1.0
    second_second = 3.0
    third = 0.25 * (3.0 * axis**3 + 3.0 * axis**2 - 3.0 * axis + 1.0)
    third_prime = 0.25 * (9.0 * axis**2 + 6.0 * axis - 3.0)
    third_second = 0.25 * (18.0 * axis + 6.0)

    quotient_prime = (
        2.0 * second * second_prime / third
        - second**2 * third_prime / third**2
    )
    quotient_second = (
        2.0 * (second_prime**2 + second * second_second) / third
        - 4.0 * second * second_prime * third_prime / third**2
        - second**2 * third_second / third**2
        + 2.0 * second**2 * third_prime**2 / third**3
    )
    first = -(2.0 / 7.0) * quotient_prime - second_prime
    second_derivative = -(2.0 / 7.0) * quotient_second - second_second
    return float(first), float(second_derivative)


def free_energy(axis: float, beta: float) -> float:
    return entropy(axis) + beta * energy(axis)


def stationary_beta(axis: float) -> float:
    energy_prime, _ = energy_derivatives(axis)
    return float(-entropy_prime(axis) / energy_prime)


def golden_minimum(function, left: float, right: float) -> tuple[float, float]:
    ratio = (np.sqrt(5.0) - 1.0) / 2.0
    x1 = right - ratio * (right - left)
    x2 = left + ratio * (right - left)
    f1, f2 = function(x1), function(x2)
    for _ in range(180):
        if f1 > f2:
            left = x1
            x1, f1 = x2, f2
            x2 = left + ratio * (right - left)
            f2 = function(x2)
        else:
            right = x2
            x2, f2 = x1, f1
            x1 = right - ratio * (right - left)
            f1 = function(x1)
    point = 0.5 * (left + right)
    return point, float(function(point))


def bisect_root(function, left: float, right: float) -> float:
    f_left = function(left)
    f_right = function(right)
    assert f_left * f_right < 0.0
    for _ in range(180):
        middle = 0.5 * (left + right)
        f_middle = function(middle)
        if f_left * f_middle <= 0.0:
            right = middle
            f_right = f_middle
        else:
            left = middle
            f_left = f_middle
    return 0.5 * (left + right)


def isotropic_free_energy(beta: float) -> float:
    return float(-np.log(3.0) + (2.0 / 3.0) * beta)


def main() -> None:
    ordered_spinodal_axis = bisect_root(
        lambda axis: entropy_second(axis)
        + stationary_beta(axis) * energy_derivatives(axis)[1],
        0.70,
        0.82,
    )
    ordered_spinodal_beta = stationary_beta(ordered_spinodal_axis)

    coexistence_axis = bisect_root(
        lambda axis: free_energy(axis, stationary_beta(axis))
        - isotropic_free_energy(stationary_beta(axis)),
        ordered_spinodal_axis + 1e-8,
        0.97,
    )
    coexistence_beta = stationary_beta(coexistence_axis)
    coexistence_saddle_axis = bisect_root(
        lambda axis: stationary_beta(axis) - coexistence_beta,
        0.40,
        ordered_spinodal_axis - 1e-8,
    )
    coexistence_barrier = (
        free_energy(coexistence_saddle_axis, coexistence_beta)
        - isotropic_free_energy(coexistence_beta)
    )

    beta_two_saddle_axis = bisect_root(
        lambda axis: stationary_beta(axis) - 2.0,
        0.40,
        ordered_spinodal_axis - 1e-8,
    )
    beta_two_ordered_axis = bisect_root(
        lambda axis: stationary_beta(axis) - 2.0,
        ordered_spinodal_axis + 1e-8,
        0.995,
    )
    beta_two_barrier = (
        free_energy(beta_two_saddle_axis, 2.0) - isotropic_free_energy(2.0)
    )

    isotropic_spinodal_beta = 21.0 / 2.0
    isotropic_curvature_residual = (
        entropy_second(1.0 / 3.0)
        + isotropic_spinodal_beta * energy_derivatives(1.0 / 3.0)[1]
    )

    result = {
        "gate": "version6_modular_cooling_projective_transition_gate",
        "free_energy_landscape": {
            "uniaxial_family": "R(a)=diag(a,(1-a)/2,(1-a)/2)",
            "free_energy": "S(a)+beta E(a)",
            "ordered_branch_birth_inverse_temperature": ordered_spinodal_beta,
            "ordered_branch_birth_axis_weight": ordered_spinodal_axis,
            "coexistence_inverse_temperature": coexistence_beta,
            "coexistence_ordered_axis_weight": coexistence_axis,
            "coexistence_saddle_axis_weight": coexistence_saddle_axis,
            "coexistence_barrier_density": coexistence_barrier,
            "isotropic_spinodal_inverse_temperature": isotropic_spinodal_beta,
            "isotropic_spinodal_exact": "21/2",
            "isotropic_curvature": "9/2-3 beta/7",
        },
        "metastability_windows": {
            "beta_below_ordered_spinodal": "only isotropic minimum",
            "ordered_spinodal_to_coexistence": "ordered phase metastable",
            "coexistence_to_isotropic_spinodal": "isotropic phase metastable; nucleation required",
            "beta_above_isotropic_spinodal": "isotropic phase linearly unstable; spinodal roll-down allowed",
        },
        "beta_two_example": {
            "saddle_axis_weight": beta_two_saddle_axis,
            "ordered_axis_weight": beta_two_ordered_axis,
            "barrier_density_above_isotropic": beta_two_barrier,
        },
        "kinetic_classification": {
            "natural_order_parameter_dynamics": "nonconserved Model A / Allen-Cahn type",
            "standard_kibble_zurek_directly_applicable": False,
            "first_order_route": "Langer nucleation for shallow supercooling; spinodal decomposition for deep quench",
            "thin_wall_critical_radius": "2 sigma / Delta f",
            "thin_wall_barrier": "16 pi sigma^3 / (3 Delta f^2)",
            "defect_origin": "independent RP2 axes selected by distinct bubbles or unstable domains",
        },
        "missing_parent_data": {
            "cooling_law_beta_of_internal_time": False,
            "mobility_or_relaxation_coefficient": False,
            "noise_kernel": False,
            "interface_tension_normalization": False,
            "defect_density_prediction": False,
        },
        "maximum_residuals": {
            "ordered_spinodal_stationarity": abs(
                entropy_prime(ordered_spinodal_axis)
                + ordered_spinodal_beta * energy_derivatives(ordered_spinodal_axis)[0]
            ),
            "ordered_spinodal_curvature": abs(
                entropy_second(ordered_spinodal_axis)
                + ordered_spinodal_beta * energy_derivatives(ordered_spinodal_axis)[1]
            ),
            "coexistence_free_energy": abs(
                free_energy(coexistence_axis, coexistence_beta)
                - isotropic_free_energy(coexistence_beta)
            ),
            "isotropic_spinodal_curvature": abs(isotropic_curvature_residual),
        },
        "verdict": {
            "static_transition_kinetics_classified": True,
            "long_metastable_isotropic_window_exists": True,
            "explosive_spinodal_crystallization_is_conditionally_possible": True,
            "internal_cooling_trigger_derived": False,
            "matter_birth_fully_derived": False,
            "next_gate": "version6_internal_entropy_transfer_cooling_gate",
        },
    }

    assert 1.341 < ordered_spinodal_beta < 1.343
    assert 1.542 < coexistence_beta < 1.543
    assert abs(isotropic_spinodal_beta - 10.5) < 1e-15
    assert all(value < 2e-8 for value in result["maximum_residuals"].values())

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_modular_cooling_projective_transition_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()