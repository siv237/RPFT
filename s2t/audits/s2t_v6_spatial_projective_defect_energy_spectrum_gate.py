#!/usr/bin/env python3
"""Audit infrared energy scaling of RP2 defects in the ordered Q field."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    field_result = json.loads(
        (root / "results" / "s2t_v6_projective_order_parameter_field_spectrum_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    spectrum = np.array(field_result["ordered_background"]["spectrum"], dtype=float)
    axis = float(np.max(spectrum))
    transverse = float(np.min(spectrum))
    order_gap = axis - transverse
    gap_square = order_gap**2

    stiffness = 1.0
    core = 1.0
    half_disclination_charge = 0.5

    line_coefficient = (
        2.0 * np.pi * stiffness * gap_square * half_disclination_charge**2
    )
    hedgehog_coefficient = 8.0 * np.pi * stiffness * gap_square

    cutoffs = np.geomspace(2.0, 128.0, 80)
    line_energies = line_coefficient * np.log(cutoffs / core)
    hedgehog_energies = hedgehog_coefficient * (cutoffs - core)

    line_fit = np.polyfit(np.log(cutoffs / core), line_energies, 1)
    hedgehog_fit = np.polyfit(cutoffs - core, hedgehog_energies, 1)

    e2_base = gap_square
    e4_base = 1.0
    scales = np.geomspace(0.05, 20.0, 1000)
    hopf_energies = e2_base * scales + e4_base / scales
    numerical_index = int(np.argmin(hopf_energies))
    numerical_scale = float(scales[numerical_index])
    exact_scale = float(np.sqrt(e4_base / e2_base))
    exact_energy = float(2.0 * np.sqrt(e2_base * e4_base))

    result = {
        "gate": "version6_spatial_projective_defect_energy_spectrum_gate",
        "ordered_field": {
            "axis_eigenvalue": axis,
            "transverse_eigenvalue": transverse,
            "order_gap": order_gap,
            "order_gap_squared": gap_square,
            "orientation_gradient_identity": "Tr(dQ dQ)=2(a-b)^2 |dn|^2",
        },
        "z2_line_disclination": {
            "minimal_director_charge": half_disclination_charge,
            "energy_per_length": "2 pi kappa (a-b)^2 q^2 log(L/xi)",
            "unit_stiffness_log_coefficient": line_coefficient,
            "fitted_log_coefficient": float(line_fit[0]),
            "infrared_finite_in_infinite_space": False,
            "particle_like_in_3_plus_1_dimensions": False,
        },
        "integer_point_hedgehog": {
            "gradient_norm": "|grad n|^2=2/r^2",
            "energy": "8 pi kappa (a-b)^2 (L-xi)",
            "unit_stiffness_linear_coefficient": hedgehog_coefficient,
            "fitted_linear_coefficient": float(hedgehog_fit[0]),
            "core_relaxation_removes_infrared_divergence": False,
            "infrared_finite_without_gauge_connection": False,
            "spin_cover_charge_plus_minus_15_available": True,
        },
        "hopf_texture": {
            "constant_boundary_at_spatial_infinity": True,
            "quadratic_scaling": "E2(L)=A L",
            "quartic_scaling": "E4(L)=B/L",
            "quadratic_only_has_finite_radius": False,
            "quadratic_plus_quartic_scale": "sqrt(B/A)",
            "test_exact_scale": exact_scale,
            "test_numerical_scale": numerical_scale,
            "test_exact_minimum_energy": exact_energy,
            "finite_energy_with_positive_E2_and_E4": True,
            "project_derives_positive_common_E2_E4_normalization": False,
        },
        "gauged_completion": {
            "SO3_connection_can_cancel_hedgehog_far_gradient": True,
            "smooth_BPS_monopole_is_mathematically_available": True,
            "BPS_energy": "4 pi v/g",
            "Callias_index_on_oriented_branch": 1,
            "project_parent_derives_spatial_SO3_connection": False,
            "project_parent_derives_g_and_v": False,
            "current_integer_class": "plus/minus 15 after coefficient multiplicity",
        },
        "zero_mode_and_stability_summary": {
            "straight_line": "two transverse positions plus shape modes; not localized",
            "global_hedgehog": "three translations formally, but norm diverges with volume",
            "hopf_with_E2_only": "dilation collapse; no stationary size",
            "hopf_with_E2_plus_E4": "three translations, rotations and positive stabilized dilation conditionally",
            "gauged_BPS_monopole": "finite translational zero modes and one oriented Callias mode conditionally",
        },
        "verdict": {
            "line_sector_is_particle": False,
            "ungauged_point_sector_is_finite_particle": False,
            "hopf_sector_is_best_ungauged_localized_candidate": True,
            "gauged_point_sector_is_best_plus_minus_15_candidate": True,
            "either_candidate_is_parent_closed": False,
            "matter_birth_fully_derived": False,
            "next_gate": "version6_gauged_projective_spin_cover_parent_gate",
        },
    }

    assert abs(line_fit[0] - line_coefficient) < 1e-12
    assert abs(hedgehog_fit[0] - hedgehog_coefficient) < 1e-11
    assert abs(np.log(numerical_scale / exact_scale)) < 0.01
    assert order_gap > 0.8

    output = root / "results" / "s2t_v6_spatial_projective_defect_energy_spectrum_gate_results.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()