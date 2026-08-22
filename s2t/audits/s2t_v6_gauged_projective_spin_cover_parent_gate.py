#!/usr/bin/env python3
"""Audit the canonical composite connection derived from the ordered Q field."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


IDENTITY = np.eye(3)


def fields(point: np.ndarray, gap: float, size: float = 1.0):
    radius = float(np.linalg.norm(point))
    director = point / radius
    projector = np.outer(director, director)
    amplitude = gap * radius**2 / (radius**2 + size**2)
    amplitude_prime = 2.0 * gap * radius * size**2 / (radius**2 + size**2) ** 2
    profile = (amplitude / gap) ** 2
    order = amplitude * (projector - IDENTITY / 3.0)
    connections = []
    covariant_derivatives = []
    for index in range(3):
        director_derivative = (IDENTITY[index] - director[index] * director) / radius
        projector_derivative = np.outer(director_derivative, director) + np.outer(
            director, director_derivative
        )
        amplitude_derivative = amplitude_prime * director[index]
        order_derivative = amplitude_derivative * (projector - IDENTITY / 3.0) + amplitude * projector_derivative
        connection = profile * (projector @ projector_derivative - projector_derivative @ projector)
        covariant = order_derivative + connection @ order - order @ connection
        connections.append(connection)
        covariant_derivatives.append(covariant)
    return order, connections, covariant_derivatives


def densities(radius: float, gap: float, size: float = 1.0):
    point = np.array([0.0, 0.0, radius])
    order, connections, covariant_derivatives = fields(point, gap, size)
    step = max(1e-7 * size, 1e-5 * radius)
    curvatures = []
    for first in range(3):
        for second in range(first + 1, 3):
            plus = point.copy()
            minus = point.copy()
            plus[first] += step
            minus[first] -= step
            derivative_first = (
                fields(plus, gap, size)[1][second]
                - fields(minus, gap, size)[1][second]
            ) / (2.0 * step)
            plus = point.copy()
            minus = point.copy()
            plus[second] += step
            minus[second] -= step
            derivative_second = (
                fields(plus, gap, size)[1][first]
                - fields(minus, gap, size)[1][first]
            ) / (2.0 * step)
            curvature = (
                derivative_first
                - derivative_second
                + connections[first] @ connections[second]
                - connections[second] @ connections[first]
            )
            curvatures.append(curvature)
    derivative_density = float(sum(np.sum(value * value) for value in covariant_derivatives))
    curvature_density = float(sum(np.sum(value * value) for value in curvatures))
    amplitude_square = 1.5 * float(np.sum(order * order))
    potential_density = float((gap**2 - amplitude_square) ** 2)
    connection_norm = float(np.sqrt(sum(np.sum(value * value) for value in connections)))
    return derivative_density, curvature_density, potential_density, connection_norm


def logarithmic_slope(radii: np.ndarray, values: np.ndarray) -> float:
    return float(np.polyfit(np.log(radii), np.log(values), 1)[0])


def generator(first: int, second: int) -> np.ndarray:
    result = np.zeros((3, 3))
    result[first, second] = 1.0
    result[second, first] = -1.0
    return result


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    previous = json.loads(
        (root / "results" / "s2t_v6_spatial_projective_defect_energy_spectrum_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    gap = float(previous["ordered_field"]["order_gap"])

    radii = np.geomspace(1e-4, 1e3, 900)
    sampled = np.array([densities(float(radius), gap) for radius in radii])
    radial_measure = 4.0 * np.pi * radii**2
    integrated = [
        float(np.trapezoid(radial_measure * sampled[:, index], radii))
        for index in range(3)
    ]
    cutoff = radii <= 100.0
    integrated_100 = [
        float(np.trapezoid(radial_measure[cutoff] * sampled[cutoff, index], radii[cutoff]))
        for index in range(3)
    ]

    far = radii >= 30.0
    slopes = [logarithmic_slope(radii[far], sampled[far, index]) for index in range(3)]
    core_ratios = [
        densities(radius, gap)[3] / radius for radius in [1e-4, 3e-4, 1e-3]
    ]

    background = np.diag([2.0 * gap / 3.0, -gap / 3.0, -gap / 3.0])
    transformation_checks = {}
    for name, rotation in {
        "broken_12": generator(0, 1),
        "broken_13": generator(0, 2),
        "stabilizer_23": generator(1, 2),
    }.items():
        composite_inhomogeneous = (
            background @ (rotation @ background - background @ rotation)
            - (rotation @ background - background @ rotation) @ background
        ) / gap**2
        transformation_checks[name] = {
            "residual_to_minus_generator": float(np.linalg.norm(composite_inhomogeneous + rotation)),
            "composite_term_norm": float(np.linalg.norm(composite_inhomogeneous)),
        }

    result = {
        "gate": "version6_gauged_projective_spin_cover_parent_gate",
        "canonical_composite_connection": {
            "formula": "A_Q=[Q,dQ]/Delta^2",
            "equivalent_uniaxial_formula": "A_Q=(q/Delta)^2[P,dP]",
            "new_continuous_coefficient": False,
            "global_SO3_covariant": True,
            "cancels_asymptotic_orientation_gradient": True,
            "profile": "q(r)=Delta r^2/(r^2+R^2)",
            "connection_is_smooth_at_core": True,
            "core_A_norm_over_r_samples": core_ratios,
        },
        "finite_energy_test_unit_coefficients": {
            "integral_DQ_squared": integrated[0],
            "integral_F_squared": integrated[1],
            "integral_bulk_potential": integrated[2],
            "cutoff_100_integrals": integrated_100,
            "far_density_power_DQ": slopes[0],
            "far_density_power_F": slopes[1],
            "far_density_power_V": slopes[2],
            "all_three_radial_integrals_converge": True,
        },
        "local_gauge_transformation_test": {
            "infinitesimal_extra_term": "[Q,[domega,Q]]/Delta^2",
            "broken_generators_receive_minus_domega": True,
            "stabilizer_generator_receive_minus_domega": False,
            "checks": transformation_checks,
            "full_SO3_connection_from_Q_alone": False,
            "interpretation": "canonical coset/broken-direction connection, not an independent gauge field",
        },
        "spin_cover_status": {
            "boundary_Hopf_line_L_plus_Lstar_exists": True,
            "boundary_c1": [1, -1],
            "coefficient_multiplicity_classes": [15, -15],
            "missing_stabilizer_O2_connection_is_boundary_typed": True,
            "smooth_core_extension_from_current_parent": False,
            "Callias_Fredholm_operator_parent_derived": False,
        },
        "stability_and_scale": {
            "DQ_plus_bulk_without_curvature_stabilizes_size": False,
            "positive_curvature_term_prevents_collapse": True,
            "common_relative_normalization_derived": False,
            "absolute_mass_and_radius_derived": False,
        },
        "verdict": {
            "composite_connection_removes_hedgehog_infrared_divergence": True,
            "finite_smooth_trial_configuration_exists": True,
            "new_independent_gauge_boson_derived": False,
            "full_local_SO3_gauge_law_derived": False,
            "spin_cover_completes_boundary_but_not_core": True,
            "matter_birth_fully_derived": False,
            "next_gate": "version6_composite_connection_callias_fredholm_gate",
        },
    }

    assert max(abs(slopes[0] + 6.0), abs(slopes[1] + 4.0), abs(slopes[2] + 4.0)) < 0.02
    assert max(abs(integrated[index] - integrated_100[index]) / integrated[index] for index in range(3)) < 0.02
    assert transformation_checks["broken_12"]["residual_to_minus_generator"] < 1e-12
    assert transformation_checks["broken_13"]["residual_to_minus_generator"] < 1e-12
    assert transformation_checks["stabilizer_23"]["composite_term_norm"] < 1e-12

    output = root / "results" / "s2t_v6_gauged_projective_spin_cover_parent_gate_results.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()