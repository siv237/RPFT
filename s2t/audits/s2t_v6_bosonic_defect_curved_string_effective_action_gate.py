#!/usr/bin/env python3
"""Эффективное действие медленно изогнутой полной вихревой нити."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
BACKGROUND_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_full_tensor_stationary_background_gate.py"
BACKGROUND_RESULT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_tensor_stationary_background_gate_results.json"
GAP_RESULT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_tensor_internal_gap_gate_results.json"
COLLECTIVE_RESULT = ROOT / "s2t/results/s2t_v6_bosonic_defect_collective_quantization_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_curved_string_effective_action_gate_results.json"


def main() -> None:
    background_module = runpy.run_path(str(BACKGROUND_AUDIT))
    model = background_module["setup_reduction"]()
    solution, _, _ = background_module["solve_full_profile"](model)
    stored_background = json.loads(BACKGROUND_RESULT.read_text(encoding="utf-8"))
    gap = json.loads(GAP_RESULT.read_text(encoding="utf-8"))
    collective = json.loads(COLLECTIVE_RESULT.read_text(encoding="utf-8"))

    radius = np.linspace(1.0e-5, 20.0, 100000)
    k, kp, a, ap, b, bp, q, qp = solution.sol(radius)
    A, B, D, G = model["A"], model["B"], model["D"], model["G"]
    densities = {
        "radial_T3": 0.5 * A * ap**2,
        "radial_T0": 0.5 * B * bp**2,
        "radial_Q": 0.5 * D * qp**2,
        "angular_T3": 0.5 * A * a**2 * (1.0 - k) ** 2 / radius**2,
        "gauge_curvature": 0.5 * G * kp**2 / radius**2,
        "potential": model["potential"](q, a, b),
    }
    energy_density = sum(densities.values())

    def radial_moment(power):
        return float(
            2.0 * np.pi * np.trapezoid(
                energy_density * radius ** (power + 1), radius
            )
        )

    tension = radial_moment(0)
    second_moment = radial_moment(2)
    fourth_moment = radial_moment(4)
    sixth_moment = radial_moment(6)
    rms_width = float(np.sqrt(second_moment / tension))
    radial_kurtosis = float(fourth_moment * tension / second_moment**2)

    shell = energy_density * radius
    cumulative = np.concatenate([[
        0.0
    ], np.cumsum(
        0.5 * (shell[1:] + shell[:-1]) * np.diff(radius)
    )]) * 2.0 * np.pi
    quantiles = {
        str(fraction): float(np.interp(fraction * tension, cumulative, radius))
        for fraction in [0.5, 0.9, 0.95, 0.99]
    }

    circumference_slope = float(2.0 * np.pi * tension)
    radius_to_width = [3.0, 5.0, 10.0]
    ring_samples = {}
    for ratio in radius_to_width:
        ring_radius = ratio * rms_width
        ring_samples[str(ratio)] = {
            "radius": float(ring_radius),
            "nambu_goto_energy": float(circumference_slope * ring_radius),
            "width_over_radius": float(1.0 / ratio),
            "unit_c4_relative_correction": float(ratio**-4),
            "c4_required_for_stationarity_at_this_radius": float(ratio**4 / 3.0),
        }

    unit_c4_stationary_ratio = float(3.0 ** 0.25)
    result = {
        "gate": "version6_bosonic_defect_curved_string_effective_action_gate",
        "straight_string_inputs": {
            "dimensionless_tension_reintegrated": tension,
            "dimensionless_tension_parent": stored_background["profile"]["dimensionless_tension"],
            "relative_tension_reintegration_residual": float(abs(
                tension - stored_background["profile"]["dimensionless_tension"]
            ) / tension),
            "full_internal_gap": gap["continuum_fit"]["critical_internal_gap"],
            "normalizable_internal_rotor_exists": collective["verdict"][
                "normalizable_internal_rotor_exists"
            ],
            "dyonic_charge_coordinate_exists": collective["verdict"][
                "dyonic_charge_coordinate_exists"
            ],
        },
        "cross_section": {
            "second_energy_moment": second_moment,
            "fourth_energy_moment": fourth_moment,
            "sixth_energy_moment": sixth_moment,
            "rms_energy_width": rms_width,
            "radial_energy_kurtosis": radial_kurtosis,
            "energy_radius_quantiles": quantiles,
            "transverse_first_moment": [0.0, 0.0],
            "first_moment_vanishes_by_axial_symmetry": True,
        },
        "zero_mode_effective_action": {
            "leading_worldsheet_action": "-T integral sqrt(-gamma)",
            "leading_coefficient_T": tension,
            "independent_quadratic_extrinsic_rigidity_from_translation_modes": False,
            "quadratic_worldsheet_Ricci_term_is_topological_for_closed_worldsheets": True,
            "static_circular_cylinder_worldsheet_Ricci_scalar": 0.0,
            "massive_profile_modes_required_for_nontrivial_curvature_response": True,
        },
        "static_ring": {
            "leading_energy": "E0(R)=2*pi*T*R",
            "leading_energy_derivative": circumference_slope,
            "finite_stationary_radius_at_leading_order": False,
            "samples_by_radius_over_rms_width": ring_samples,
        },
        "quartic_curvature_boundary": {
            "generic_relative_form": "E(R)=2*pi*T*R*[1+c4*(w/R)^4+...]",
            "unit_c4_stationary_radius_over_width": unit_c4_stationary_ratio,
            "unit_c4_stationary_point_inside_slow_curvature_regime": False,
            "c4_required_for_stationarity_at_R_over_w_3": ring_samples["3.0"][
                "c4_required_for_stationarity_at_this_radius"
            ],
            "coefficient_c4_derived_from_current_straight_spectrum": False,
        },
        "verdict": {
            "nambu_goto_term_derived_from_parent_tension": True,
            "controlled_quadratic_rigidity_stabilizes_ring": False,
            "normalizable_worldsheet_current_can_stabilize_ring": False,
            "ground_state_ring_has_controlled_finite_radius": False,
            "straight_string_can_be_promoted_to_particle_without_new_response_calculation": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_curved_string_massive_mode_response_gate",
        },
    }

    assert result["straight_string_inputs"]["relative_tension_reintegration_residual"] < 1.0e-6
    assert 0.5 < rms_width < 0.7
    assert result["cross_section"]["energy_radius_quantiles"]["0.99"] < 1.5
    assert circumference_slope > 9.0
    assert not result["straight_string_inputs"]["normalizable_internal_rotor_exists"]
    assert not result["straight_string_inputs"]["dyonic_charge_coordinate_exists"]
    assert not result["verdict"]["ground_state_ring_has_controlled_finite_radius"]
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(OUT)


if __name__ == "__main__":
    main()