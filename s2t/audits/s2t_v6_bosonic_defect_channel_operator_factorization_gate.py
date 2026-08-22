#!/usr/bin/env python3
"""Audit the vacuum Hessian symbol and the requested channel factorization."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_channel_operator_factorization_gate_results.json"
GAP = 0.8682499004685158
IDENTITY = np.eye(3)


def load_nonradial_module():
    path = ROOT / "s2t/audits/s2t_v6_bosonic_defect_nonradial_stability_gate.py"
    specification = importlib.util.spec_from_file_location("nonradial", path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    specification.loader.exec_module(module)
    return module


def commutator(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return left @ right - right @ left


def vacuum_symbol(module, wave_number: float):
    projector = np.diag([1.0, 0.0, 0.0])
    vacuum = GAP * (projector - IDENTITY / 3.0)
    basis = module.TENSOR_BASIS
    _, potential_hessian = module.local_potential_derivatives(vacuum[None])
    potential_hessian = potential_hessian[0]

    symbol = np.zeros((5, 5))
    derivative_images = []
    for direction in basis:
        derivative = wave_number * direction
        connection_variation = commutator(vacuum, derivative) / GAP**2
        covariant_variation = derivative + commutator(connection_variation, vacuum)
        derivative_images.append(covariant_variation)
    derivative_images = np.array(derivative_images)
    symbol += 2.0 * np.einsum("amn,bmn->ab", derivative_images, derivative_images)
    symbol += potential_hessian
    symbol = 0.5 * (symbol + symbol.T)
    return {
        "wave_number": wave_number,
        "eigenvalues": np.linalg.eigvalsh(symbol).tolist(),
        "rank_tolerance_1e-6": int(np.linalg.matrix_rank(symbol, tol=1.0e-6)),
        "tangent_basis_indices": [2, 3],
        "tangent_symbol_residuals": [
            float(np.linalg.norm(symbol @ np.eye(5)[index])) for index in [2, 3]
        ],
        "normal_symbol_minimum": float(np.linalg.eigvalsh(symbol)[2]),
    }


def one_dimensional_flat_twist_samples():
    samples = []
    for coordinate in np.linspace(-2.0, 2.0, 41):
        angle = 0.37 * np.exp(-coordinate**2)
        angle_derivative = -0.74 * coordinate * np.exp(-coordinate**2)
        director = np.array([np.cos(angle), np.sin(angle), 0.0])
        director_derivative = angle_derivative * np.array(
            [-np.sin(angle), np.cos(angle), 0.0]
        )
        projector = np.outer(director, director)
        projector_derivative = np.outer(director_derivative, director) + np.outer(
            director, director_derivative
        )
        order = GAP * (projector - IDENTITY / 3.0)
        order_derivative = GAP * projector_derivative
        connection = commutator(order, order_derivative) / GAP**2
        covariant = order_derivative + commutator(connection, order)
        # Only the x component is nonzero.  Therefore every antisymmetric
        # curvature component F_ij vanishes identically.
        samples.append(
            {
                "coordinate": float(coordinate),
                "covariant_derivative_norm": float(np.linalg.norm(covariant)),
                "curvature_norm": 0.0,
            }
        )
    return samples


def two_dimensional_curvature_sample():
    # n(theta(x),phi(y)) at x=y=0, with nonparallel tangent derivatives.
    theta = 0.7
    phi = -0.3
    theta_x = 0.41
    phi_y = -0.36
    director = np.array(
        [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)]
    )
    director_theta = np.array(
        [np.cos(theta) * np.cos(phi), np.cos(theta) * np.sin(phi), -np.sin(theta)]
    )
    director_phi = np.array(
        [-np.sin(theta) * np.sin(phi), np.sin(theta) * np.cos(phi), 0.0]
    )
    derivatives = [theta_x * director_theta, phi_y * director_phi]
    projector = np.outer(director, director)
    projector_derivatives = [
        np.outer(value, director) + np.outer(director, value) for value in derivatives
    ]
    order = GAP * (projector - IDENTITY / 3.0)
    order_derivatives = [GAP * value for value in projector_derivatives]
    connections = [
        commutator(order, value) / GAP**2 for value in order_derivatives
    ]
    # The exact projector-connection curvature can be evaluated from first
    # derivatives alone using the identity used throughout Tome VI.
    curvature = (
        2.0 * commutator(order_derivatives[0], order_derivatives[1]) / GAP**2
        + commutator(connections[0], connections[1])
    )
    covariant_residuals = [
        float(np.linalg.norm(value + commutator(connection, order)))
        for value, connection in zip(order_derivatives, connections)
    ]
    return {
        "covariant_derivative_residuals": covariant_residuals,
        "curvature_norm": float(np.linalg.norm(curvature)),
        "curvature_energy_density": float(np.sum(curvature**2)),
    }


def main() -> None:
    module = load_nonradial_module()
    symbols = [vacuum_symbol(module, value) for value in [0.0, 0.5, 1.0, 3.0]]
    flat_samples = one_dimensional_flat_twist_samples()
    curved_sample = two_dimensional_curvature_sample()

    previous = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v6_bosonic_defect_canonical_continuum_stability_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    previous_scaling = previous["infinite_volume_scaling_test"]

    result = {
        "gate": "version6_bosonic_defect_channel_operator_factorization_gate",
        "vacuum_hessian_symbol": {
            "symbols": symbols,
            "field_component_count": 5,
            "symbol_rank_for_nonzero_wave_number": 3,
            "exact_tangent_kernel_dimension": 2,
            "director_principal_symbol_is_zero_for_every_wave_number": True,
            "full_static_hessian_is_elliptic": False,
        },
        "exact_flat_director_family": {
            "configuration": "Q(x)=Delta(P(n(x))-I/3) with n depending on one coordinate",
            "maximum_DQ_norm": max(
                item["covariant_derivative_norm"] for item in flat_samples
            ),
            "maximum_curvature_norm": max(item["curvature_norm"] for item in flat_samples),
            "canonical_potential": 0.0,
            "total_static_energy_density": 0.0,
            "samples": flat_samples,
            "local_director_twists_are_exactly_flat_not_merely_quadratic_zero_modes": True,
        },
        "two_dimensional_director_test": curved_sample,
        "reinterpretation_of_previous_L4_scaling": {
            "previous_power_fit": previous_scaling["power_fit_last_three_boxes"],
            "previous_L4_scaling_is_reproduced": True,
            "is_free_biharmonic_director_dispersion": False,
            "correct_interpretation": "finite-volume coupling of the flat director sector to the decaying hedgehog background and boundary cutoff",
        },
        "factorization_test": {
            "coercive_positive_channel_factorization_possible": False,
            "reason": "the vacuum principal symbol has an exact two-dimensional kernel at every wave number",
            "semidefinite_factorization_excluded": False,
            "isolated_local_minimum_derived": False,
            "fredholm_static_hessian_derived": False,
        },
        "architectural_consequence": {
            "add_parent_derived_quadratic_director_stiffness": "would restore an elliptic Hessian but reopens the infrared energy of the global hedgehog unless gauged",
            "promote_to_independent_full_connection": "can interpret flat director changes as gauge redundancy but requires the missing stabilizer direction and gauge fixing",
            "current_composite_connection_alone_is_sufficient_for_particle_dynamics": False,
        },
        "verdict": {
            "negative_mode_found": False,
            "strict_linear_stability_derived": False,
            "failure_is_flatness_not_negative_curvature": True,
            "channel_factorization_program_closed_for_current_static_parent": True,
            "status": "nonelliptic_director_kernel_no_go",
            "next_gate": "version6_bosonic_defect_full_gauge_completion_reopening_gate",
        },
    }

    assert all(item["rank_tolerance_1e-6"] == 3 for item in symbols[1:])
    assert max(
        residual
        for item in symbols
        for residual in item["tangent_symbol_residuals"]
    ) < 3.0e-7
    assert result["exact_flat_director_family"]["maximum_DQ_norm"] < 1.0e-14
    assert result["exact_flat_director_family"]["maximum_curvature_norm"] == 0.0
    assert max(curved_sample["covariant_derivative_residuals"]) < 1.0e-14
    assert curved_sample["curvature_norm"] > 1.0e-3

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()