#!/usr/bin/env python3
"""Audit the canonical nonlinear state-squaring feedback candidate."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def normalize(matrix: np.ndarray) -> np.ndarray:
    return matrix / np.trace(matrix)


def square_map(matrix: np.ndarray) -> np.ndarray:
    return normalize(matrix @ matrix)


def entropy(matrix: np.ndarray) -> float:
    eigenvalues = np.linalg.eigvalsh(matrix)
    positive = eigenvalues[eigenvalues > 1e-14]
    return float(-np.sum(positive * np.log(positive)))


def random_state(rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(3, 3))
    gram = matrix @ matrix.T
    return normalize(gram)


def main() -> None:
    isotropic = np.eye(3) / 3.0
    direction = np.diag([2.0, -1.0, -1.0])
    epsilon = 1e-7
    perturbed = isotropic + epsilon * direction
    mapped = square_map(perturbed)
    discrete_gain = float(
        np.linalg.norm(mapped - isotropic) / np.linalg.norm(perturbed - isotropic)
    )

    coexistence_axis = 0.9121665962741361
    coexistence = np.diag(
        [
            coexistence_axis,
            0.5 * (1.0 - coexistence_axis),
            0.5 * (1.0 - coexistence_axis),
        ]
    )
    coexistence_after = square_map(coexistence)

    rho_one = isotropic
    rho_two = np.diag([1.0, 0.0, 0.0])
    convex_mixture = 0.5 * (rho_one + rho_two)
    affine_defect = float(
        np.linalg.norm(
            square_map(convex_mixture)
            - 0.5 * (square_map(rho_one) + square_map(rho_two))
        )
    )

    rng = np.random.default_rng(20260819)
    entropy_changes = []
    purity_changes = []
    equivariance_residuals = []
    for _ in range(200):
        state = random_state(rng)
        output = square_map(state)
        entropy_changes.append(entropy(output) - entropy(state))
        purity_changes.append(
            float(np.trace(output @ output) - np.trace(state @ state))
        )
        q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
        equivariance_residuals.append(
            float(
                np.linalg.norm(square_map(q @ state @ q.T) - q @ output @ q.T)
            )
        )

    iterated = coexistence.copy()
    axis_history = [float(iterated[0, 0])]
    for _ in range(8):
        iterated = square_map(iterated)
        axis_history.append(float(iterated[0, 0]))

    result = {
        "gate": "version6_nonlinear_affine_feedback_instability_gate",
        "canonical_candidate": {
            "conditional_map": "P(R)=R^2/Tr(R^2)",
            "stay_amplitude": "K_stay(R)=sqrt(R)",
            "leak_amplitude": "K_leak(R)=sqrt(I-R)",
            "pointwise_completeness": "K_stay^*K_stay+K_leak^*K_leak=I",
            "SO3_equivariant": True,
            "preselected_axis_required": False,
        },
        "isotropic_linearization": {
            "discrete_traceless_gain_exact": 2.0,
            "discrete_traceless_gain_numeric": discrete_gain,
            "continuous_flow": "dR/dtau=R^2-Tr(R^2)R",
            "continuous_traceless_growth_rate": 1.0 / 3.0,
            "isotropic_fixed_point": True,
            "isotropic_linearly_unstable": True,
        },
        "coexistence_test": {
            "input_spectrum": np.linalg.eigvalsh(coexistence).tolist(),
            "output_spectrum": np.linalg.eigvalsh(coexistence_after).tolist(),
            "input_entropy": entropy(coexistence),
            "output_entropy": entropy(coexistence_after),
            "output_axis_weight": float(coexistence_after[0, 0]),
            "finite_full_rank_phase_is_fixed": False,
            "overshoots_toward_rank_one": True,
        },
        "iteration": {
            "axis_weight_history_from_coexistence": axis_history,
            "rank_one_projectors_are_attractors": True,
            "only_full_rank_fixed_point": "I3/3",
        },
        "ensemble_linearity_obstruction": {
            "convex_linearity_defect": affine_defect,
            "fixed_linear_CPTP_channel_realizes_map_for_all_states": False,
            "requires": [
                "postselection/conditioning",
                "multiple copies",
                "measurement feedback",
                "or a derived nonlinear mean-field limit",
            ],
        },
        "random_state_checks": {
            "maximum_entropy_change": float(np.max(entropy_changes)),
            "minimum_purity_change": float(np.min(purity_changes)),
            "maximum_SO3_equivariance_residual": float(
                np.max(equivariance_residuals)
            ),
        },
        "project_boundary": {
            "affine_P3_resonant_corner_available": True,
            "modular_square_root_available": True,
            "state_dependent_Kraus_operator_parent_derived": False,
            "two_copy_deterministic_realization_parent_derived": False,
            "finite_ordered_phase_saturation": False,
        },
        "verdict": {
            "coefficient_free_axis_amplifier_exists": True,
            "amplifier_is_SO3_equivariant": True,
            "amplifier_is_autonomous_linear_quantum_channel": False,
            "amplifier_stabilizes_observed_full_rank_crystal": False,
            "nonlinear_feedback_is_a_valid_next_parent_target": True,
            "matter_birth_fully_derived": False,
            "next_gate": "version6_two_copy_affine_dilation_gate",
        },
    }

    assert abs(discrete_gain - 2.0) < 2e-6
    assert affine_defect > 0.1
    assert result["random_state_checks"]["maximum_entropy_change"] < 1e-12
    assert result["random_state_checks"]["minimum_purity_change"] > -1e-12
    assert result["random_state_checks"]["maximum_SO3_equivariance_residual"] < 2e-14

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_nonlinear_affine_feedback_instability_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()