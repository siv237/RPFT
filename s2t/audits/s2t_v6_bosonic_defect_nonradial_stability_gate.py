#!/usr/bin/env python3
"""Audit the five-component, nonradial Hessian of the composite Q defect."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp
from scipy.linalg import eigh


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_nonradial_stability_gate_results.json"
GAP = 0.8682499004685158
BETA = 1.5426695408602842
IDENTITY = np.eye(3)


def commutator(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return left @ right - right @ left


def traceless_basis() -> np.ndarray:
    basis = []
    basis.append(np.diag([2.0, -1.0, -1.0]) / np.sqrt(6.0))
    basis.append(np.diag([0.0, 1.0, -1.0]) / np.sqrt(2.0))
    for first, second in [(0, 1), (0, 2), (1, 2)]:
        value = np.zeros((3, 3))
        value[first, second] = value[second, first] = 1.0 / np.sqrt(2.0)
        basis.append(value)
    return np.array(basis)


TENSOR_BASIS = traceless_basis()


def canonical_free_energy(order: np.ndarray) -> np.ndarray:
    """Canonical local free energy for R=I/3+Q on the trace-one slice."""
    state = order + IDENTITY / 3.0
    eigenvalues = np.linalg.eigvalsh(state)
    if np.any(eigenvalues <= 0.0):
        return np.full(eigenvalues.shape[:-1], np.inf)
    second = np.sum(eigenvalues**2, axis=-1)
    third = np.sum(eigenvalues**3, axis=-1)
    entropy = np.sum(eigenvalues * np.log(eigenvalues), axis=-1)
    radial = (2.0 / 7.0) * (1.0 - second**2 / third)
    exterior = 1.0 - second
    return entropy + BETA * (radial + exterior)


def canonical_radial_functions():
    value = sp.symbols("u", real=True)
    longitudinal = sp.Rational(1, 3) + sp.Rational(2, 3) * GAP * value
    transverse = sp.Rational(1, 3) - sp.Rational(1, 3) * GAP * value
    second = longitudinal**2 + 2 * transverse**2
    third = longitudinal**3 + 2 * transverse**3
    free = (
        longitudinal * sp.log(longitudinal)
        + 2 * transverse * sp.log(transverse)
        + BETA * (sp.Rational(2, 7) * (1 - second**2 / third) + 1 - second)
    )
    vacuum = float(free.subs(value, 1.0))
    potential = free - vacuum
    return (
        sp.lambdify(value, potential, "numpy"),
        sp.lambdify(value, sp.diff(potential, value), "numpy"),
    )


def solve_canonical_profile():
    potential, potential_derivative = canonical_radial_functions()
    radius_symbol, value_symbol = sp.symbols("r u", positive=True)
    nonpotential = (
        4 * GAP**2 * value_symbol**2 * (1 - value_symbol**2) ** 2
        + 2 * value_symbol**4 * (value_symbol**2 - 2) ** 2 / radius_symbol**2
    )
    nonpotential_derivative = sp.lambdify(
        (radius_symbol, value_symbol), sp.diff(nonpotential, value_symbol), "numpy"
    )
    epsilon = 1.0e-4
    outer = 50.0
    mesh = np.geomspace(epsilon, outer, 1500)
    initial = mesh**2 / (mesh**2 + 1.4**2)
    initial_derivative = 2.0 * mesh * 1.4**2 / (mesh**2 + 1.4**2) ** 2

    def equation(radius: np.ndarray, field: np.ndarray) -> np.ndarray:
        value, derivative = field
        coefficient = (2.0 / 3.0) * GAP**2 * radius**2 + 16.0 * value**2
        coefficient_r = (4.0 / 3.0) * GAP**2 * radius
        coefficient_u = 32.0 * value
        force = nonpotential_derivative(radius, value) + radius**2 * potential_derivative(value)
        second = (
            force - coefficient_u * derivative**2 - 2.0 * coefficient_r * derivative
        ) / (2.0 * coefficient)
        return np.vstack((derivative, second))

    solution = solve_bvp(
        equation,
        lambda left, right: np.array([left[0], right[0] - 1.0]),
        mesh,
        np.vstack((initial, initial_derivative)),
        tol=2.0e-7,
        max_nodes=100000,
    )
    integration_radius = np.geomspace(epsilon, outer, 40000)
    value, derivative = solution.sol(integration_radius)
    derivative_density = (
        (2.0 / 3.0) * GAP**2 * derivative**2
        + 4.0 * GAP**2 * value**2 * (1.0 - value**2) ** 2 / integration_radius**2
    )
    curvature_density = (
        16.0 * value**2 * derivative**2 / integration_radius**2
        + 2.0 * value**4 * (value**2 - 2.0) ** 2 / integration_radius**4
    )
    potential_density = potential(value)
    measure = 4.0 * np.pi * integration_radius**2
    parts = [
        float(np.trapezoid(measure * density, integration_radius))
        for density in [derivative_density, curvature_density, potential_density]
    ]
    parts[1] += 8.0 * np.pi / outer
    return solution, {
        "bvp_status": int(solution.status),
        "maximum_rms_ode_residual": float(np.max(solution.rms_residuals)),
        "half_height_radius": float(np.interp(0.5, value, integration_radius)),
        "energy_parts_with_tail_correction": parts,
        "corrected_total_energy": float(sum(parts)),
        "corrected_virial_residual": float(parts[0] - parts[1] + 3.0 * parts[2]),
        "canonical_potential_at_isotropic_core": float(potential(0.0)),
        "canonical_potential_at_ordered_vacuum": float(potential(1.0)),
        "canonical_barrier_maximum": float(np.max(potential(np.linspace(0.0, 1.0, 1001)))),
    }


def solid_harmonics(points: np.ndarray):
    x, y, z = points.T
    values = [
        (0, "1", np.ones_like(x), np.zeros((len(points), 3))),
        (1, "x", x, np.column_stack((np.ones_like(x), np.zeros_like(x), np.zeros_like(x)))),
        (1, "y", y, np.column_stack((np.zeros_like(x), np.ones_like(x), np.zeros_like(x)))),
        (1, "z", z, np.column_stack((np.zeros_like(x), np.zeros_like(x), np.ones_like(x)))),
        (2, "xy", x * y, np.column_stack((y, x, np.zeros_like(x)))),
        (2, "xz", x * z, np.column_stack((z, np.zeros_like(x), x))),
        (2, "yz", y * z, np.column_stack((np.zeros_like(x), z, y))),
        (2, "x2-y2", x**2 - y**2, np.column_stack((2 * x, -2 * y, np.zeros_like(x)))),
        (
            2,
            "2z2-x2-y2",
            2 * z**2 - x**2 - y**2,
            np.column_stack((-2 * x, -2 * y, 4 * z)),
        ),
        (
            3,
            "x(5z2-r2)",
            x * (4 * z**2 - x**2 - y**2),
            np.column_stack((4 * z**2 - 3 * x**2 - y**2, -2 * x * y, 8 * x * z)),
        ),
        (
            3,
            "y(5z2-r2)",
            y * (4 * z**2 - x**2 - y**2),
            np.column_stack((-2 * x * y, 4 * z**2 - x**2 - 3 * y**2, 8 * y * z)),
        ),
        (
            3,
            "z(5z2-3r2)",
            z * (2 * z**2 - 3 * x**2 - 3 * y**2),
            np.column_stack((-6 * x * z, -6 * y * z, 6 * z**2 - 3 * x**2 - 3 * y**2)),
        ),
        (
            3,
            "z(x2-y2)",
            z * (x**2 - y**2),
            np.column_stack((2 * x * z, -2 * y * z, x**2 - y**2)),
        ),
        (3, "xyz", x * y * z, np.column_stack((y * z, x * z, x * y))),
        (
            3,
            "x(x2-3y2)",
            x * (x**2 - 3 * y**2),
            np.column_stack((3 * x**2 - 3 * y**2, -6 * x * y, np.zeros_like(x))),
        ),
        (
            3,
            "y(3x2-y2)",
            y * (3 * x**2 - y**2),
            np.column_stack((6 * x * y, 3 * x**2 - 3 * y**2, np.zeros_like(x))),
        ),
    ]
    return values


def make_galerkin_fields(
    points: np.ndarray,
    box_radius: float,
    scales: tuple[float, ...],
    angular_degrees: tuple[int, ...] = (0, 1, 2),
):
    radius = np.linalg.norm(points, axis=1)
    direction = np.zeros_like(points)
    nonzero = radius > 1.0e-14
    direction[nonzero] = points[nonzero] / radius[nonzero, None]
    fields = []
    derivatives = []
    metadata = []
    for angular_degree, angular_name, solid, solid_gradient in solid_harmonics(points):
        if angular_degree not in angular_degrees:
            continue
        for scale in scales:
            cutoff = (1.0 - (radius / box_radius) ** 2) ** 2
            gaussian = np.exp(-(radius / scale) ** 2)
            radial = cutoff * gaussian
            radial_derivative = gaussian * (
                -4.0 * radius * (1.0 - (radius / box_radius) ** 2) / box_radius**2
                - 2.0 * radius * cutoff / scale**2
            )
            scalar = solid * radial
            scalar_derivative = solid_gradient * radial[:, None] + (
                solid * radial_derivative
            )[:, None] * direction
            for tensor_index, tensor in enumerate(TENSOR_BASIS):
                fields.append(scalar[:, None, None] * tensor)
                derivatives.append(
                    np.einsum("gi,mn->gimn", scalar_derivative, tensor)
                )
                metadata.append(
                    {
                        "angular_degree": angular_degree,
                        "angular_name": angular_name,
                        "radial_scale": scale,
                        "tensor_component": tensor_index,
                    }
                )
    fields = np.array(fields)
    derivatives = np.array(derivatives)
    norms = np.sqrt(np.einsum("bgmn,bgmn->b", fields, fields))
    fields /= norms[:, None, None, None]
    derivatives /= norms[:, None, None, None, None]
    return fields, derivatives, metadata


def background_fields(points: np.ndarray, solution):
    radius = np.linalg.norm(points, axis=1)
    direction = np.zeros_like(points)
    nonzero = radius > 1.0e-14
    direction[nonzero] = points[nonzero] / radius[nonzero, None]
    projector = np.einsum("gi,gj->gij", direction, direction)
    projector[~nonzero] = np.diag([1.0, 0.0, 0.0])
    value, derivative = solution.sol(np.maximum(radius, 1.0e-4))
    value[~nonzero] = 0.0
    derivative[~nonzero] = 0.0
    order = GAP * value[:, None, None] * (projector - IDENTITY / 3.0)
    order_derivative = np.zeros((len(points), 3, 3, 3))
    for spatial in range(3):
        projector_derivative = np.zeros_like(projector)
        projector_derivative[nonzero] = (
            np.einsum(
                "gi,gj->gij",
                (IDENTITY[spatial] - direction[:, spatial, None] * direction)[nonzero]
                / radius[nonzero, None],
                direction[nonzero],
            )
            + np.einsum(
                "gi,gj->gij",
                direction[nonzero],
                (IDENTITY[spatial] - direction[:, spatial, None] * direction)[nonzero]
                / radius[nonzero, None],
            )
        )
        order_derivative[:, spatial] = GAP * (
            derivative[:, None, None]
            * direction[:, spatial, None, None]
            * (projector - IDENTITY / 3.0)
            + value[:, None, None] * projector_derivative
        )
    return order, order_derivative


def commutator_contraction(
    left: np.ndarray, first: np.ndarray, second: np.ndarray, weight: np.ndarray
) -> np.ndarray:
    term_one = np.einsum(
        "gmn,bgmk,cgkn,g->bc", left, first, second, weight, optimize=True
    )
    term_two = np.einsum(
        "gmn,cgmk,bgkn,g->bc", left, second, first, weight, optimize=True
    )
    return term_one - term_two


def local_potential_derivatives(order: np.ndarray, step: float = 2.0e-4):
    count = len(order)
    base = canonical_free_energy(order)
    gradient = np.zeros((count, 5))
    hessian = np.zeros((count, 5, 5))
    for first in range(5):
        direction_first = TENSOR_BASIS[first]
        plus = canonical_free_energy(order + step * direction_first)
        minus = canonical_free_energy(order - step * direction_first)
        gradient[:, first] = (plus - minus) / (2.0 * step)
        hessian[:, first, first] = (plus + minus - 2.0 * base) / step**2
        for second in range(first + 1, 5):
            direction_second = TENSOR_BASIS[second]
            value = (
                canonical_free_energy(order + step * (direction_first + direction_second))
                - canonical_free_energy(order + step * (direction_first - direction_second))
                - canonical_free_energy(order + step * (-direction_first + direction_second))
                + canonical_free_energy(order - step * (direction_first + direction_second))
            ) / (4.0 * step**2)
            hessian[:, first, second] = hessian[:, second, first] = value
    return gradient, hessian


def assemble_hessian(
    points: np.ndarray,
    weight: np.ndarray,
    solution,
    box_radius: float,
    scales: tuple[float, ...],
    angular_degrees: tuple[int, ...] = (0, 1, 2),
):
    order, order_derivative = background_fields(points, solution)
    fields, field_derivative, metadata = make_galerkin_fields(
        points, box_radius, scales, angular_degrees
    )
    number = len(fields)

    connection = np.empty((len(points), 3, 3, 3))
    connection_variation = np.empty((number, len(points), 3, 3, 3))
    covariant = np.empty_like(connection)
    covariant_variation = np.empty_like(connection_variation)
    for spatial in range(3):
        connection[:, spatial] = commutator(order, order_derivative[:, spatial]) / GAP**2
        connection_variation[:, :, spatial] = (
            commutator(fields, order_derivative[None, :, spatial])
            + commutator(order[None], field_derivative[:, :, spatial])
        ) / GAP**2
        covariant[:, spatial] = order_derivative[:, spatial] + commutator(
            connection[:, spatial], order
        )
        covariant_variation[:, :, spatial] = (
            field_derivative[:, :, spatial]
            + commutator(connection_variation[:, :, spatial], order[None])
            + commutator(connection[None, :, spatial], fields)
        )

    hessian = np.zeros((number, number))
    gradient = np.zeros(number)
    for spatial in range(3):
        linear = covariant_variation[:, :, spatial].reshape(number, -1)
        weighted = (
            covariant_variation[:, :, spatial] * np.sqrt(weight)[None, :, None, None]
        ).reshape(number, -1)
        hessian += 2.0 * (weighted @ weighted.T)
        gradient += 2.0 * np.einsum(
            "gmn,bgmn,g->b",
            covariant[:, spatial],
            covariant_variation[:, :, spatial],
            weight,
            optimize=True,
        )

        transformed = commutator(covariant[:, spatial], order)
        mixed_connection = commutator_contraction(
            transformed, fields, field_derivative[:, :, spatial], weight
        ) / GAP**2
        hessian += 2.0 * (mixed_connection + mixed_connection.T)
        mixed_covariant = commutator_contraction(
            covariant[:, spatial], connection_variation[:, :, spatial], fields, weight
        )
        hessian += 2.0 * (mixed_covariant + mixed_covariant.T)

    for first in range(3):
        for second in range(first + 1, 3):
            curvature = (
                2.0
                * commutator(order_derivative[:, first], order_derivative[:, second])
                / GAP**2
                + commutator(connection[:, first], connection[:, second])
            )
            curvature_variation = (
                2.0
                * (
                    commutator(
                        field_derivative[:, :, first], order_derivative[None, :, second]
                    )
                    + commutator(
                        order_derivative[None, :, first], field_derivative[:, :, second]
                    )
                )
                / GAP**2
                + commutator(
                    connection_variation[:, :, first], connection[None, :, second]
                )
                + commutator(
                    connection[None, :, first], connection_variation[:, :, second]
                )
            )
            weighted = (
                curvature_variation * np.sqrt(weight)[None, :, None, None]
            ).reshape(number, -1)
            hessian += 2.0 * (weighted @ weighted.T)
            gradient += 2.0 * np.einsum(
                "gmn,bgmn,g->b",
                curvature,
                curvature_variation,
                weight,
                optimize=True,
            )

            derivative_pair = commutator_contraction(
                curvature,
                field_derivative[:, :, first],
                field_derivative[:, :, second],
                weight,
            )
            hessian += (4.0 / GAP**2) * (derivative_pair + derivative_pair.T)

            transformed_first = (
                curvature @ np.swapaxes(connection[:, second], -1, -2)
                - np.swapaxes(connection[:, second], -1, -2) @ curvature
            )
            pair_first = commutator_contraction(
                transformed_first, fields, field_derivative[:, :, first], weight
            ) / GAP**2
            hessian += 2.0 * (pair_first + pair_first.T)

            transformed_second = (
                np.swapaxes(connection[:, first], -1, -2) @ curvature
                - curvature @ np.swapaxes(connection[:, first], -1, -2)
            )
            pair_second = commutator_contraction(
                transformed_second, fields, field_derivative[:, :, second], weight
            ) / GAP**2
            hessian += 2.0 * (pair_second + pair_second.T)

            connection_pair = commutator_contraction(
                curvature,
                connection_variation[:, :, first],
                connection_variation[:, :, second],
                weight,
            )
            hessian += 2.0 * (connection_pair + connection_pair.T)

    potential_gradient, potential_hessian = local_potential_derivatives(order)
    field_components = np.einsum("bgmn,amn->bga", fields, TENSOR_BASIS)
    gradient += np.einsum(
        "bga,ga,g->b", field_components, potential_gradient, weight, optimize=True
    )
    hessian += np.einsum(
        "bga,gad,cgd,g->bc",
        field_components,
        potential_hessian,
        field_components,
        weight,
        optimize=True,
    )

    weighted_fields = (fields * np.sqrt(weight)[None, :, None, None]).reshape(number, -1)
    mass = weighted_fields @ weighted_fields.T
    hessian = 0.5 * (hessian + hessian.T)
    mass = 0.5 * (mass + mass.T)
    inverse_mass_gradient = np.linalg.solve(mass, gradient)
    projected_gradient_norm = float(np.sqrt(gradient @ inverse_mass_gradient))

    vacuum_energy = float(
        canonical_free_energy(GAP * (np.diag([1.0, 0.0, 0.0]) - IDENTITY / 3.0))
    )

    def discretized_energy(coefficients: np.ndarray) -> float:
        perturbed_order = order + np.einsum("b,bgmn->gmn", coefficients, fields)
        perturbed_derivative = order_derivative + np.einsum(
            "b,bgimn->gimn", coefficients, field_derivative
        )
        perturbed_connection = np.empty_like(connection)
        perturbed_covariant = np.empty_like(covariant)
        for spatial in range(3):
            perturbed_connection[:, spatial] = commutator(
                perturbed_order, perturbed_derivative[:, spatial]
            ) / GAP**2
            perturbed_covariant[:, spatial] = perturbed_derivative[:, spatial] + commutator(
                perturbed_connection[:, spatial], perturbed_order
            )
        derivative_energy = np.sum(perturbed_covariant**2, axis=(1, 2, 3))
        curvature_energy = np.zeros(len(points))
        for first in range(3):
            for second in range(first + 1, 3):
                perturbed_curvature = (
                    2.0
                    * commutator(
                        perturbed_derivative[:, first], perturbed_derivative[:, second]
                    )
                    / GAP**2
                    + commutator(
                        perturbed_connection[:, first], perturbed_connection[:, second]
                    )
                )
                curvature_energy += np.sum(perturbed_curvature**2, axis=(1, 2))
        potential_energy = canonical_free_energy(perturbed_order) - vacuum_energy
        return float(np.sum(weight * (derivative_energy + curvature_energy + potential_energy)))

    rng = np.random.default_rng(20260820)
    finite_difference_checks = []
    zero = np.zeros(number)
    base_energy = discretized_energy(zero)
    for _ in range(3):
        direction = rng.normal(size=number)
        direction /= np.sqrt(direction @ mass @ direction)
        perturbation = np.einsum("b,bgmn->gmn", direction, fields)
        step = 1.0e-4 / max(1.0, float(np.max(np.linalg.norm(perturbation, axis=(1, 2)))))
        plus = discretized_energy(step * direction)
        minus = discretized_energy(-step * direction)
        finite_curvature = (plus + minus - 2.0 * base_energy) / step**2
        assembled_curvature = float(direction @ hessian @ direction)
        finite_difference_checks.append(
            {
                "step": step,
                "first_variation_residual": float((plus - minus) / (2.0 * step)),
                "finite_difference_curvature": float(finite_curvature),
                "assembled_curvature": assembled_curvature,
                "relative_curvature_residual": float(
                    abs(finite_curvature - assembled_curvature)
                    / max(1.0, abs(assembled_curvature))
                ),
            }
        )

    eigenvalues, eigenvectors = eigh(hessian, mass, subset_by_index=[0, min(19, number - 1)])

    translation_tests = []
    for spatial in range(3):
        target = -order_derivative[:, spatial]
        right_hand_side = np.einsum(
            "bgmn,gmn,g->b", fields, target, weight, optimize=True
        )
        coefficients = np.linalg.solve(mass, right_hand_side)
        projected_norm = float(coefficients @ mass @ coefficients)
        target_norm = float(np.einsum("gmn,gmn,g->", target, target, weight))
        translation_tests.append(
            {
                "spatial_direction": spatial,
                "captured_L2_fraction": projected_norm / target_norm,
                "projected_rayleigh_quotient": float(
                    coefficients @ hessian @ coefficients / projected_norm
                ),
            }
        )

    lowest_vector = eigenvectors[:, 0]
    degree_weights = {}
    for degree in angular_degrees:
        selection = np.array([item["angular_degree"] == degree for item in metadata])
        partial = lowest_vector * selection
        degree_weights[str(degree)] = float(partial @ mass @ partial)
    normalization = sum(degree_weights.values())
    degree_weights = {key: value / normalization for key, value in degree_weights.items()}
    return {
        "basis_dimension": number,
        "lowest_twenty_generalized_eigenvalues": eigenvalues.tolist(),
        "negative_mode_count_in_computed_window": int(np.sum(eigenvalues < -1.0e-5)),
        "near_zero_mode_count_in_computed_window": int(np.sum(np.abs(eigenvalues) <= 1.0e-5)),
        "lowest_mode_angular_degree_weights": degree_weights,
        "hessian_asymmetry_residual": float(np.max(np.abs(hessian - hessian.T))),
        "mass_smallest_eigenvalue": float(np.linalg.eigvalsh(mass)[0]),
        "projected_first_variation_norm": projected_gradient_norm,
        "translation_projection_tests": translation_tests,
        "directional_finite_difference_checks": finite_difference_checks,
    }


def main() -> None:
    solution, radial = solve_canonical_profile()
    configurations = [
        (4.5, 18, 8, 16, (0.8, 1.6)),
        (5.5, 22, 10, 20, (0.8, 1.6)),
        (5.5, 22, 10, 20, (0.7, 1.2, 2.1)),
        (5.5, 22, 10, 20, (0.55, 0.9, 1.4, 2.2)),
    ]
    spectra = []
    for box_radius, radial_count, polar_count, azimuthal_count, scales in configurations:
        radial_nodes, radial_weights = np.polynomial.legendre.leggauss(radial_count)
        radii = 0.5 * box_radius * (radial_nodes + 1.0)
        radial_weights = 0.5 * box_radius * radial_weights * radii**2
        cosines, polar_weights = np.polynomial.legendre.leggauss(polar_count)
        azimuths = 2.0 * np.pi * np.arange(azimuthal_count) / azimuthal_count
        points = []
        weights = []
        for radius, radial_weight in zip(radii, radial_weights):
            for cosine, polar_weight in zip(cosines, polar_weights):
                sine = np.sqrt(1.0 - cosine**2)
                for azimuth in azimuths:
                    points.append(
                        radius
                        * np.array(
                            [sine * np.cos(azimuth), sine * np.sin(azimuth), cosine]
                        )
                    )
                    weights.append(
                        radial_weight * polar_weight * (2.0 * np.pi / azimuthal_count)
                    )
        points = np.array(points)
        weight = np.array(weights)
        spectrum = assemble_hessian(points, weight, solution, box_radius, scales)
        spectrum.update(
            {
                "box_radius": box_radius,
                "radial_quadrature_order": radial_count,
                "polar_quadrature_order": polar_count,
                "azimuthal_quadrature_order": azimuthal_count,
                "integration_point_count": len(points),
                "radial_scales": list(scales),
                "maximum_angular_degree": 2,
            }
        )
        spectra.append(spectrum)

    old = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v6_bosonic_defect_full_euler_lagrange_stability_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    old_unit = old["boundary_value_problem"]["cases"]["unit"]
    result = {
        "gate": "version6_bosonic_defect_nonradial_stability_gate",
        "parent_potential_consistency": {
            "previous_radial_potential": "Delta^4(1-u^2)^2",
            "previous_potential_was_canonical_parent_derived": False,
            "canonical_local_potential": "F_beta(I/3+Q)-F_beta(R_ordered)",
            "isotropic_and_ordered_phases_coexist": True,
            "previous_unit_energy": old_unit["corrected_total_energy"],
            "previous_half_height_radius": old_unit["half_height_radius"],
            "interpretation": "the earlier radial result applies to an admissible quartic completion, not uniquely to the canonical Tome VI parent",
        },
        "canonical_radial_solution": radial,
        "five_component_galerkin_hessian": {
            "field_space": "real symmetric traceless 3x3 Q tensor",
            "tensor_component_count": 5,
            "angular_degrees_tested": [0, 1, 2],
            "solid_harmonics_per_degree": [1, 3, 5],
            "boundary_condition": "compact radial cutoff at finite ball boundary",
            "spectra": spectra,
        },
        "verdict": {
            "canonical_parent_radial_profile_recomputed": True,
            "old_quartic_radial_profile_remains_valid_for_that_completion": True,
            "old_quartic_profile_is_unique_parent_prediction": False,
            "negative_nonradial_mode_found_in_tested_galerkin_spaces": any(
                item["negative_mode_count_in_computed_window"] > 0 for item in spectra
            ),
            "continuum_full_stability_proved": False,
            "status": "canonical_potential_correction_and_five_component_galerkin_test",
            "next_gate": "version6_bosonic_defect_canonical_continuum_stability_gate",
        },
    }

    assert radial["bvp_status"] == 0
    assert abs(radial["corrected_virial_residual"]) < 2.0e-4
    assert abs(radial["canonical_potential_at_isotropic_core"]) < 1.0e-12
    assert abs(radial["canonical_potential_at_ordered_vacuum"]) < 1.0e-12
    assert all(item["mass_smallest_eigenvalue"] > 1.0e-8 for item in spectra)
    assert all(item["negative_mode_count_in_computed_window"] == 0 for item in spectra)
    assert max(item["projected_first_variation_norm"] for item in spectra) < 1.0e-3
    assert max(
        check["relative_curvature_residual"]
        for item in spectra
        for check in item["directional_finite_difference_checks"]
    ) < 1.0e-5

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()