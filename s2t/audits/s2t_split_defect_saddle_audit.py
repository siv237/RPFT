import json
import math
from pathlib import Path

import numpy as np


OUTPUT = Path("s2t_split_defect_saddle_results.json")


def main() -> None:
    pi = math.pi
    radius = 1.0
    charge = 1.0
    tension = 1.0
    cycle_weight = 1.0

    carrier_volume = pi**2 * radius**3
    cycle_length = pi * radius
    minimizing_density = charge / cycle_length
    cycle_action = 0.5 * cycle_weight * charge**2 / cycle_length
    fixed_geometry_action = tension * carrier_volume + cycle_action

    rng = np.random.default_rng(20260804)
    sample_count = 256
    grid_size = 8192
    mode_count = 12
    coordinate = np.linspace(0.0, cycle_length, grid_size, endpoint=False)
    sampled_gaps = []
    decomposition_errors = []

    for _ in range(sample_count):
        perturbation = np.zeros_like(coordinate)
        cosine_coefficients = rng.normal(scale=0.35, size=mode_count)
        sine_coefficients = rng.normal(scale=0.35, size=mode_count)
        for mode in range(1, mode_count + 1):
            phase = 2.0 * pi * mode * coordinate / cycle_length
            perturbation += cosine_coefficients[mode - 1] * np.cos(phase)
            perturbation += sine_coefficients[mode - 1] * np.sin(phase)
        perturbation -= float(np.mean(perturbation))

        density = minimizing_density + perturbation
        action = 0.5 * cycle_weight * cycle_length * float(np.mean(density**2))
        expected_gap = (
            0.5 * cycle_weight * cycle_length * float(np.mean(perturbation**2))
        )
        sampled_gaps.append(action - cycle_action)
        decomposition_errors.append(abs((action - cycle_action) - expected_gap))

    radial_derivative_at_one = 3.0 * tension * pi**2 - cycle_weight / (2.0 * pi)
    radial_second_derivative_at_one = 6.0 * tension * pi**2 + cycle_weight / pi
    free_radius_stationary_point = (
        cycle_weight / (6.0 * tension * pi**3)
    ) ** 0.25
    free_radius_stationary_action = (
        tension * pi**2 * free_radius_stationary_point**3
        + cycle_weight / (2.0 * pi * free_radius_stationary_point)
    )

    reconstructed_action = 10.06440597135364
    cycle_weight_needed_for_exact_reconstruction = (
        2.0 * pi * (reconstructed_action - pi**2)
    )

    result = {
        "status": "conditional_fixed_geometry_saddle_constructed_unconstrained_radius_no_go",
        "date": "2026-08-04",
        "action": {
            "formula": "S[X,a]=T Vol(X)+kappa/2 integral_gamma a wedge star a",
            "topological_constraints": [
                "deg(X)=1 on the RP3 fundamental class",
                "integral_gamma a=1 on the systolic generator",
            ],
            "canonical_choice": {"T": tension, "kappa": cycle_weight},
        },
        "fixed_unit_carrier_saddle": {
            "radius": radius,
            "carrier_volume": carrier_volume,
            "cycle_length": cycle_length,
            "minimizing_cycle_form": "a=ds/pi",
            "cycle_form_norm_squared": 1.0 / pi,
            "cycle_action": cycle_action,
            "on_shell_action": fixed_geometry_action,
            "target_candidate": pi**2 + 1.0 / (2.0 * pi),
            "identity_error": abs(
                fixed_geometry_action - (pi**2 + 1.0 / (2.0 * pi))
            ),
            "variational_statement": "Cauchy-Schwarz gives integral f^2 ds >= 1/L, with equality only for f=1/L",
        },
        "stability_audit": {
            "sample_count": sample_count,
            "fourier_modes": mode_count,
            "minimum_sampled_action_gap": min(sampled_gaps),
            "maximum_quadratic_decomposition_error": max(decomposition_errors),
            "analytic_hessian": "delta2 S=kappa integral_gamma (delta f)^2 ds > 0 on nonzero zero-mean perturbations",
        },
        "free_radius_test": {
            "on_shell_function": "S(R)=T pi^2 R^3+kappa/(2 pi R)",
            "derivative_at_R_equals_1": radial_derivative_at_one,
            "second_derivative_at_R_equals_1": radial_second_derivative_at_one,
            "R_equals_1_is_stationary": abs(radial_derivative_at_one) < 1e-12,
            "stationary_radius": free_radius_stationary_point,
            "stationary_action": free_radius_stationary_action,
            "verdict": "the two-term action does not stabilize the unit carrier radius",
        },
        "normalization_gate": {
            "cycle_weight_needed_to_hit_reconstructed_action_with_T_equal_1": cycle_weight_needed_for_exact_reconstruction,
            "canonical_cycle_weight": cycle_weight,
            "warning": "T=1 and kappa=1 must descend from one parent normalization; fitting kappa would destroy the zero-parameter status",
        },
        "theory_effect": {
            "closed": "for a frozen unit RP3 carrier, the candidate is the unique stable minimum in the degree-one, unit-period sector",
            "not_closed": "the same action neither derives the common normalization nor makes R=1 stationary when the overall radius is dynamical",
            "next_gate": "derive the wrapped tension and cycle kinetic term from one parent S2T superconnection or add an independently required radius-stabilizing sector before two-loop matching",
        },
    }

    assert result["fixed_unit_carrier_saddle"]["identity_error"] < 1e-14
    assert result["stability_audit"]["minimum_sampled_action_gap"] > 0.0
    assert result["stability_audit"]["maximum_quadratic_decomposition_error"] < 1e-12
    assert not result["free_radius_test"]["R_equals_1_is_stationary"]

    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "on_shell_action": fixed_geometry_action,
                "minimum_sampled_action_gap": min(sampled_gaps),
                "radial_derivative_at_R_equals_1": radial_derivative_at_one,
                "free_radius_stationary_point": free_radius_stationary_point,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()