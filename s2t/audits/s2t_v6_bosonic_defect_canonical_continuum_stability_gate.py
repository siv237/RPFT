#!/usr/bin/env python3
"""Classify the lowest channel and audit its infinite-volume scaling."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_canonical_continuum_stability_gate_results.json"


def load_nonradial_module():
    path = ROOT / "s2t/audits/s2t_v6_bosonic_defect_nonradial_stability_gate.py"
    specification = importlib.util.spec_from_file_location("nonradial", path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    specification.loader.exec_module(module)
    return module


def composite_spherical_quadrature(
    box_radius: float,
    interval_order: int = 16,
    polar_order: int = 8,
    azimuthal_order: int = 16,
):
    radial_points = []
    radial_weights = []
    split = min(3.0, box_radius)
    for left, right in [(0.0, split), (split, box_radius)]:
        if right <= left:
            continue
        nodes, weights = np.polynomial.legendre.leggauss(interval_order)
        radius = 0.5 * (right - left) * nodes + 0.5 * (left + right)
        radial_points.extend(radius)
        radial_weights.extend(0.5 * (right - left) * weights * radius**2)

    cosines, polar_weights = np.polynomial.legendre.leggauss(polar_order)
    azimuths = 2.0 * np.pi * np.arange(azimuthal_order) / azimuthal_order
    points = []
    weights = []
    for radius, radial_weight in zip(radial_points, radial_weights):
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
                    radial_weight
                    * polar_weight
                    * (2.0 * np.pi / azimuthal_order)
                )
    return np.array(points), np.array(weights)


def angular_momentum_decomposition(orbital_degree: int, internal_spin: int = 2):
    return {
        str(total): 2 * total + 1
        for total in range(abs(orbital_degree - internal_spin), orbital_degree + internal_spin + 1)
    }


def main() -> None:
    module = load_nonradial_module()
    solution, radial = module.solve_canonical_profile()

    decomposition = {
        str(degree): angular_momentum_decomposition(degree)
        for degree in range(4)
    }
    assert sum(decomposition["2"].values()) == 25
    assert decomposition["2"]["1"] == 3

    box_radii = np.array([6.0, 8.0, 10.0, 12.0])
    scaling_spectra = []
    for box_radius in box_radii:
        points, weights = composite_spherical_quadrature(float(box_radius))
        scales = (0.7, 1.2, 0.35 * box_radius, 0.65 * box_radius, 0.9 * box_radius)
        spectrum = module.assemble_hessian(
            points,
            weights,
            solution,
            float(box_radius),
            scales,
            (2,),
        )
        scaling_spectra.append(
            {
                "box_radius": float(box_radius),
                "basis_dimension": spectrum["basis_dimension"],
                "lowest_six_eigenvalues": spectrum[
                    "lowest_twenty_generalized_eigenvalues"
                ][:6],
                "negative_mode_count": spectrum[
                    "negative_mode_count_in_computed_window"
                ],
                "projected_first_variation_norm": spectrum[
                    "projected_first_variation_norm"
                ],
                "maximum_directional_hessian_residual": max(
                    check["relative_curvature_residual"]
                    for check in spectrum["directional_finite_difference_checks"]
                ),
            }
        )

    lowest = np.array([item["lowest_six_eigenvalues"][0] for item in scaling_spectra])
    full_power = float(np.polyfit(np.log(box_radii), np.log(lowest), 1)[0])
    asymptotic_power = float(np.polyfit(np.log(box_radii[1:]), np.log(lowest[1:]), 1)[0])
    quartic_rescaled = lowest * box_radii**4

    points, weights = composite_spherical_quadrature(6.0, polar_order=10, azimuthal_order=20)
    degree_three = module.assemble_hessian(
        points,
        weights,
        solution,
        6.0,
        (0.7, 1.2, 2.1, 4.0),
        (3,),
    )

    # On the ordered vacuum manifold Q=Delta(P-I/3), A=[P,dP].  The
    # projector identity [[P,dP],P]=-dP makes D_Q Q vanish exactly.  Hence
    # broad director waves have no two-derivative or potential cost and the
    # leading static Rayleigh quotient is quartic in their wave number.
    asymptotic_identity = {
        "ordered_vacuum_covariant_derivative": "D_Q Q=0",
        "ordered_vacuum_potential": "V_can(Q)=0",
        "leading_long_wavelength_term": "integral |F_A|^2",
        "predicted_L2_rayleigh_scaling": "lambda_min proportional to L^-4",
    }

    result = {
        "gate": "version6_bosonic_defect_canonical_continuum_stability_gate",
        "grand_angular_momentum": {
            "internal_tensor_spin": 2,
            "orbital_tensor_product_decompositions": decomposition,
            "previous_lowest_mode_scalar_orbital_degree": 2,
            "previous_lowest_multiplicity": 3,
            "unique_total_J_with_multiplicity_three_in_l2_tensor_spin2": 1,
            "lowest_triplet_classification": "grand angular momentum J=1",
        },
        "infinite_volume_scaling_test": {
            "spectra": scaling_spectra,
            "lowest_eigenvalues": lowest.tolist(),
            "power_fit_all_boxes": full_power,
            "power_fit_last_three_boxes": asymptotic_power,
            "lambda_times_L4": quartic_rescaled.tolist(),
            "asymptotic_identity": asymptotic_identity,
            "approaches_zero_from_above": bool(np.all(lowest > 0.0)),
            "negative_bound_state_seen": False,
        },
        "higher_angular_channel_test": {
            "orbital_degree": 3,
            "basis_dimension": degree_three["basis_dimension"],
            "lowest_twenty_eigenvalues": degree_three[
                "lowest_twenty_generalized_eigenvalues"
            ],
            "negative_mode_count": degree_three[
                "negative_mode_count_in_computed_window"
            ],
            "projected_first_variation_norm": degree_three[
                "projected_first_variation_norm"
            ],
        },
        "normalization_boundary": {
            "static_hessian_sign_is_independent_of_positive_norm_choice": True,
            "reported_eigenvalue_scaling_uses_L2_Q_norm": True,
            "unique_lorentzian_kinetic_metric_parent_derived": False,
            "physical_oscillation_frequencies_derived": False,
        },
        "verdict": {
            "lowest_triplet_is_J1": True,
            "lowest_triplet_is_negative_instability": False,
            "zero_is_static_continuum_threshold": True,
            "quartic_threshold_scaling_supported": True,
            "l3_negative_mode_found": False,
            "all_continuum_channels_proved_nonnegative": False,
            "status": "J1_zero_threshold_identified_without_negative_mode",
            "next_gate": "version6_bosonic_defect_channel_operator_factorization_gate",
        },
    }

    assert all(item["negative_mode_count"] == 0 for item in scaling_spectra)
    assert np.all(lowest > 0.0)
    assert abs(asymptotic_power + 4.0) < 0.2
    assert max(quartic_rescaled[1:]) / min(quartic_rescaled[1:]) < 1.1
    assert degree_three["negative_mode_count_in_computed_window"] == 0
    assert degree_three["lowest_twenty_generalized_eigenvalues"][0] > 2.0
    assert max(
        item["maximum_directional_hessian_residual"] for item in scaling_spectra
    ) < 2.0e-5

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()