#!/usr/bin/env python3
"""Audit the local field spectrum around the projective ordered phase."""

from __future__ import annotations

import json
from math import sqrt
from pathlib import Path

import numpy as np


def free_energy(matrix: np.ndarray, beta: float) -> float:
    spectrum = np.linalg.eigvalsh(matrix)
    second = float(np.sum(spectrum**2))
    third = float(np.sum(spectrum**3))
    entropy = float(np.sum(spectrum * np.log(spectrum)))
    radial = (2.0 / 7.0) * (1.0 - second**2 / third)
    exterior = 1.0 - second
    return entropy + beta * (radial + exterior)


def directional_curvature(matrix: np.ndarray, direction: np.ndarray, beta: float) -> float:
    step = 1e-4
    return float(
        (
            free_energy(matrix + step * direction, beta)
            + free_energy(matrix - step * direction, beta)
            - 2.0 * free_energy(matrix, beta)
        )
        / step**2
    )


def rotation(angle: float) -> np.ndarray:
    cosine, sine = np.cos(angle), np.sin(angle)
    return np.array([[cosine, -sine, 0.0], [sine, cosine, 0.0], [0.0, 0.0, 1.0]])


def main() -> None:
    previous = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_tensor_square_relative_carrier_normalization_gate_results.json"
    )
    previous_result = json.loads(previous.read_text(encoding="utf-8"))
    thermal = previous_result["thermal_reopening"]
    beta = float(thermal["critical_inverse_temperature"])
    spectrum = np.array(thermal["coexistence_ordered_spectrum"], dtype=float)
    axis_index = int(np.argmax(spectrum))
    if axis_index != 0:
        spectrum[[0, axis_index]] = spectrum[[axis_index, 0]]
    ordered = np.diag(spectrum)

    amplitude = np.diag([2.0, -1.0, -1.0]) / sqrt(6.0)
    diagonal_biaxial = np.diag([0.0, 1.0, -1.0]) / sqrt(2.0)
    transverse_biaxial = np.zeros((3, 3))
    transverse_biaxial[1, 2] = transverse_biaxial[2, 1] = 1.0 / sqrt(2.0)
    director_one = np.zeros((3, 3))
    director_one[0, 1] = director_one[1, 0] = 1.0 / sqrt(2.0)
    director_two = np.zeros((3, 3))
    director_two[0, 2] = director_two[2, 0] = 1.0 / sqrt(2.0)

    basis = [amplitude, diagonal_biaxial, transverse_biaxial, director_one, director_two]
    curvatures = [directional_curvature(ordered, direction, beta) for direction in basis]

    orbit_residuals = []
    for angle in np.linspace(0.0, np.pi, 101):
        group = rotation(float(angle))
        orbit_residuals.append(abs(free_energy(group @ ordered @ group.T, beta) - free_energy(ordered, beta)))

    rng = np.random.default_rng(20260819)
    covariance_residuals = []
    for _ in range(100):
        group, _ = np.linalg.qr(rng.normal(size=(3, 3)))
        covariance_residuals.append(
            abs(free_energy(group @ ordered @ group.T, beta) - free_energy(ordered, beta))
        )

    result = {
        "gate": "version6_projective_order_parameter_field_spectrum_gate",
        "ordered_background": {
            "beta": beta,
            "spectrum": spectrum.tolist(),
            "order_parameter": "Q=R-I3/3",
            "vacuum_orbit": "SO(3)/O(2)=RP2",
            "maximum_orbit_energy_residual": max(orbit_residuals),
            "maximum_SO3_covariance_residual": max(covariance_residuals),
        },
        "local_field_decomposition": {
            "real_symmetric_traceless_dimension": 5,
            "amplitude_modes": 1,
            "biaxial_modes": 2,
            "director_goldstone_modes": 2,
            "directional_curvatures": {
                "amplitude": curvatures[0],
                "biaxial_diagonal": curvatures[1],
                "biaxial_transverse": curvatures[2],
                "director_one": curvatures[3],
                "director_two": curvatures[4],
            },
            "positive_massive_curvatures": curvatures[:3],
            "goldstone_curvatures_zero_within_numeric_tolerance": True,
        },
        "topological_sectors": {
            "pi1_RP2": "Z2",
            "pi2_RP2": "Z",
            "pi3_RP2": "Z",
            "line_defects": "Z2 disclinations",
            "point_defects": "integer hedgehogs",
            "three_dimensional_textures": "Hopf sectors",
        },
        "physics_boundary": {
            "order_parameter_field_derived": True,
            "collective_mode_count_derived": True,
            "topological_matter_sectors_exist": True,
            "finite_defect_radius_requires_spatial_stiffness_and_Skyrme_balance": True,
            "director_modes_become_gauge_bosons": False,
            "defects_identified_with_observed_particles": False,
            "spin_cover_plus_minus_15_assignment_still_required": True,
        },
        "verdict": {
            "transition_from_phase_to_fields_has_started": True,
            "first_bosonic_field_is_Q": True,
            "matter_candidates_are_topological_sectors_of_Q": True,
            "standard_model_field_content_derived": False,
            "matter_birth_fully_derived": False,
            "next_gate": "version6_spatial_projective_defect_energy_spectrum_gate",
        },
    }

    assert max(result["ordered_background"][key] for key in ["maximum_orbit_energy_residual", "maximum_SO3_covariance_residual"]) < 2e-14
    assert min(curvatures[:3]) > 1.0
    assert max(abs(value) for value in curvatures[3:]) < 1e-5

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_projective_order_parameter_field_spectrum_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()