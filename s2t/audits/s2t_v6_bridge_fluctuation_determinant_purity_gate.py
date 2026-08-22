#!/usr/bin/env python3
"""Audit the state-weighted bridge Hessian and one-loop purity coefficient."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np


def physical_hessian_eigenvalues(probabilities: np.ndarray) -> np.ndarray:
    diagonal = (16.0 / 7.0) * probabilities
    off_diagonal = np.array(
        [
            (8.0 / 7.0) * (probabilities[i] + probabilities[j])
            for i in range(3)
            for j in range(i + 1, 3)
        ]
    )
    return np.sort(np.concatenate([diagonal, off_diagonal]))


def one_loop(probabilities: np.ndarray) -> float:
    return float(0.5 * np.sum(np.log(physical_hessian_eigenvalues(probabilities))))


def entropy(probabilities: np.ndarray) -> float:
    return float(np.sum(probabilities * np.log(probabilities)))


def main() -> None:
    isotropic = np.ones(3) / 3.0
    isotropic_eigenvalues = physical_hessian_eigenvalues(isotropic)

    epsilon_values = np.logspace(-6, -2, 9)
    extracted_coefficients = []
    for epsilon in epsilon_values:
        perturbation = np.array([epsilon, -epsilon, 0.0])
        state = isotropic + perturbation
        delta_purity = float(perturbation @ perturbation)
        extracted_coefficients.append(
            (one_loop(state) - one_loop(isotropic)) / delta_purity
        )

    induced_kappa = Fraction(45, 16)
    classical_penalty = Fraction(6, 7)
    entropy_coefficient = Fraction(3, 2)
    total_quadratic = entropy_coefficient + classical_penalty - induced_kappa
    threshold = float(np.log(4.0) + float(classical_penalty))

    boundary_scan = []
    for epsilon in (1e-1, 1e-2, 1e-4, 1e-6, 1e-8):
        state = np.array([(1.0 - epsilon) / 2.0, (1.0 - epsilon) / 2.0, epsilon])
        boundary_scan.append(
            {
                "epsilon": epsilon,
                "one_loop_effective_action": one_loop(state),
                "smallest_physical_hessian_eigenvalue": float(
                    np.min(physical_hessian_eigenvalues(state))
                ),
            }
        )

    result = {
        "gate": "version6_bridge_fluctuation_determinant_purity_gate",
        "state_weighted_bridge": {
            "state": "tau5 tensor R",
            "normalized": True,
            "recovers_uniform_trace_at_R_equal_I3_over_3": True,
            "new_classical_coefficient_added": False,
        },
        "physical_hessian": {
            "zero_orbit_modes": 3,
            "physical_symmetric_modes": 6,
            "diagonal_eigenvalues": "(16/7)*r_i",
            "offdiagonal_eigenvalues": "(8/7)*(r_i+r_j)",
            "isotropic_eigenvalues": [float(v) for v in isotropic_eigenvalues],
            "isotropic_expected_value": 16.0 / 21.0,
        },
        "one_loop_purity_expansion": {
            "formula": "0.5*(sum log r_i + sum log(r_i+r_j)) + constant",
            "extracted_quadratic_coefficients": extracted_coefficients,
            "exact_quadratic_coefficient": "-45/16",
            "induced_alignment_kappa": float(induced_kappa),
            "required_threshold_log4_plus_6_over_7": threshold,
            "threshold_passed": float(induced_kappa) > threshold,
            "entropy_plus_bridge_minus_loop_exact": f"{total_quadratic.numerator}/{total_quadratic.denominator}",
            "entropy_plus_bridge_minus_loop": float(total_quadratic),
            "isotropic_local_instability": total_quadratic < 0,
        },
        "breakdown_test": {
            "boundary_scan": boundary_scan,
            "one_loop_action_unbounded_toward_rank_loss": True,
            "fluctuation_mass_vanishes_at_same_boundary": True,
            "finite_nonlinear_saturation_derived": False,
        },
        "measure_status": {
            "flat_measure_on_physical_symmetric_modes": "control_assumption",
            "full_BV_measure_derived": False,
            "polar_jacobian_included": False,
        },
        "verdict": {
            "self_started_local_RP2_instability": "conditional_pass",
            "external_time_kick_required_for_local_instability": False,
            "stable_ordered_phase_proved": False,
            "matter_birth_proved": False,
            "next_gate": "version6_state_weighted_bridge_nonperturbative_saturation_gate",
        },
    }

    assert np.allclose(isotropic_eigenvalues, np.ones(6) * 16.0 / 21.0)
    assert abs(extracted_coefficients[0] + 45.0 / 16.0) < 2.0e-4
    assert total_quadratic == Fraction(-51, 112)
    assert float(induced_kappa) > threshold
    assert boundary_scan[-1]["one_loop_effective_action"] < boundary_scan[0]["one_loop_effective_action"]
    assert boundary_scan[-1]["smallest_physical_hessian_eigenvalue"] < 1.0e-7

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_bridge_fluctuation_determinant_purity_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()