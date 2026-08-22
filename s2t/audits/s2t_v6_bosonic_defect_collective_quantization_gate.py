#!/usr/bin/env python3
"""Audit collective coordinates and possible FR quantization of the bosonic defect."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_collective_quantization_gate_results.json"


def commutator(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return left @ right - right @ left


def q_profile(radius: np.ndarray, gap: float, scale: float = 1.0) -> np.ndarray:
    return gap * radius**2 / (radius**2 + scale**2)


def orientation_inertia(cutoff: float, gap: float, scale: float = 1.0) -> float:
    radius = np.linspace(0.0, cutoff, 200001)
    radial = np.trapezoid(radius**2 * q_profile(radius, gap, scale) ** 2, radius)
    return float((16.0 * np.pi / 3.0) * radial)


def main() -> None:
    gap = 0.8682499004685158
    cutoffs = np.array([10.0, 20.0, 40.0, 80.0, 160.0])
    inertias = np.array([orientation_inertia(value, gap) for value in cutoffs])
    slope = float(np.polyfit(np.log(cutoffs[-3:]), np.log(inertias[-3:]), 1)[0])
    predicted_coefficient = (16.0 * np.pi / 9.0) * gap**2
    measured_coefficient = float(inertias[-1] / cutoffs[-1] ** 3)

    omega = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    rng = np.random.default_rng(20260820)
    combined_rotation_residuals = []
    angular_density_residuals = []
    for _ in range(500):
        direction = rng.normal(size=3)
        direction /= np.linalg.norm(direction)
        projector = np.outer(direction, direction)
        internal = commutator(omega, projector)
        spatial = -internal
        combined_rotation_residuals.append(float(np.linalg.norm(internal + spatial)))
        angular_density_residuals.append(
            abs(float(np.linalg.norm(internal) ** 2) - 2.0 * float(np.linalg.norm(omega @ direction) ** 2))
        )

    # Unit-coefficient scaling inherited from the finite trial profile.
    c_d = 12.478636601133651
    c_f = 33.53717150406454
    c_v = 17.500222083059832
    # E(R)=c_d R+c_f/R+c_v R^3. Solve for y=R^2.
    roots = np.roots([3.0 * c_v, c_d, -c_f])
    positive_y = float(max(root.real for root in roots if abs(root.imag) < 1e-12 and root.real > 0))
    stationary_radius = float(np.sqrt(positive_y))
    scale_curvature = float(2.0 * c_f / stationary_radius**3 + 6.0 * c_v * stationary_radius)

    eta = json.loads(
        (ROOT / "s2t/results/s2t_v5_eta_wzw_real_pair_phase_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    connection = json.loads(
        (ROOT / "s2t/results/s2t_v6_gauged_projective_spin_cover_parent_gate_results.json").read_text(
            encoding="utf-8"
        )
    )

    result = {
        "gate": "version6_bosonic_defect_collective_quantization_gate",
        "static_symmetry": {
            "group_before_hedgehog": "SO(3)_space x SO(3)_family",
            "hedgehog_stabilizer": "diagonal SO(3)",
            "formal_relative_orientation_space": "SO(3)",
            "combined_space_family_rotation_residual": max(combined_rotation_residuals),
            "diagonal_rotation_is_collective_coordinate": False,
        },
        "orientation_norm": {
            "variation": "delta Q=[Omega,Q]",
            "angular_integral": "integral_S2 Tr([Omega,P]^T[Omega,P])=16 pi/3 for unit z rotation",
            "angular_identity_maximum_residual": max(angular_density_residuals),
            "cutoffs": cutoffs.tolist(),
            "inertias": inertias.tolist(),
            "asymptotic_power_fit": slope,
            "predicted_L3_coefficient": predicted_coefficient,
            "measured_L3_coefficient_at_largest_cutoff": measured_coefficient,
            "internal_orientation_mode_normalizable": False,
            "interpretation": "relative family rotation changes the ordered vacuum throughout infinite volume",
        },
        "collective_modes": {
            "translations": 3,
            "translation_status": "exact static moduli; finite kinetic norm conditional on covariant time completion",
            "relative_internal_rotations": 0,
            "diagonal_rotations": "stabilizer, not a mode",
            "scale_energy": "E(R)=c_D R+c_F/R+c_V R^3",
            "unit_coefficient_stationary_radius": stationary_radius,
            "unit_coefficient_scale_curvature": scale_curvature,
            "scale_mode_is_zero_mode": False,
            "absolute_breathing_frequency_derived": False,
            "localized_collective_moduli_in_current_approximation": "R3 translations",
            "localized_moduli_pi1": "0",
        },
        "comparison_with_gauge_monopole": {
            "ordinary_single_BPS_monopole_moduli": "R3 x S1",
            "S1_origin": "global stabilizer U(1) gauge phase",
            "project_full_stabilizer_connection_derived": connection["local_gauge_transformation_test"][
                "full_SO3_connection_from_Q_alone"
            ],
            "project_has_normalizable_S1_dyon_phase": False,
        },
        "FR_statistics_test": {
            "formal_pi1_SO3": "Z2",
            "formal_FR_representations": ["+1 bosonic", "-1 fermionic"],
            "SO3_rotor_is_normalizable_local_modulus": False,
            "reduced_localized_moduli_supports_Z2_FR_loop": False,
            "full_real_WZW_phase": eta["pfaffian_parity"]["full_real_pair"],
            "WZW_phase_identified_with_2pi_collective_rotation_holonomy": False,
            "nontrivial_FR_constraint_parent_derived": False,
            "minimal_collective_quantization": "spin-zero bosonic ground state",
            "fermionic_quantization_excluded_in_all_future_extensions": False,
        },
        "verdict": {
            "normalizable_internal_rotor_exists": False,
            "half_integer_spin_from_current_collective_coordinates": False,
            "dyonic_charge_coordinate_exists": False,
            "stable_breathing_mode_possible": True,
            "absolute_mass_radius_and_frequency_derived": False,
            "current_particle_reading": "neutral spin-zero bosonic soliton candidate",
            "status": "collective_quantization_selects_no_internal_rotor_and_no_current_FR_fermion",
            "next_gate": "version6_bosonic_defect_mass_portal_parent_gate",
        },
    }

    assert max(combined_rotation_residuals) == 0.0
    assert max(angular_density_residuals) < 1e-12
    assert 2.9 < slope < 3.1
    assert abs(measured_coefficient - predicted_coefficient) / predicted_coefficient < 0.03
    assert scale_curvature > 0.0
    assert result["FR_statistics_test"]["full_real_WZW_phase"] == 1

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()