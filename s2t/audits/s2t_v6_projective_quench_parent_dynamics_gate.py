#!/usr/bin/env python3
"""Audit whether the existing modular state can drive the projective quench."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def matrix_unit(size: int, row: int, column: int) -> np.ndarray:
    unit = np.zeros((size, size), dtype=complex)
    unit[row, column] = 1.0
    return unit


def matrix_power_from_spectrum(
    eigenvalues: np.ndarray, exponent: complex
) -> np.ndarray:
    return np.diag(np.exp(exponent * np.log(eigenvalues)))


def main() -> None:
    beta = 0.73
    block_rank = 3
    heights = np.array(
        [-1.0] * block_rank
        + [0.0] * block_rank
        + [1.0] * block_rank
        + [1.0] * block_rank
        + [0.0] * block_rank
        + [-1.0] * block_rank
    )
    dimension = heights.size
    h_f = np.diag(heights)
    weights = np.exp(-beta * heights)
    rho = np.diag(weights / np.sum(weights))
    trace_state = np.eye(dimension) / dimension

    modular_generator = -np.log(np.diag(rho))
    generator_frequency_residual = float(
        np.linalg.norm(
            (modular_generator[:, None] - modular_generator[None, :])
            - beta * (heights[:, None] - heights[None, :])
        )
    )

    modular_parameter = 0.61
    rho_is = matrix_power_from_spectrum(np.diag(rho), 1j * modular_parameter)
    rho_minus_is = matrix_power_from_spectrum(
        np.diag(rho), -1j * modular_parameter
    )

    # A chain edge between distinct height blocks has nonzero modular frequency.
    chain_edge = matrix_unit(dimension, 3, 0)
    flowed_chain_edge = rho_is @ chain_edge @ rho_minus_is
    chain_edge_motion = float(np.linalg.norm(flowed_chain_edge - chain_edge))

    # Every rank-one projector inside a three-dimensional vertex commutes with h_F,
    # because h_F is scalar on that vertex.  Hence RP2 orientation is stationary.
    rng = np.random.default_rng(20260819)
    projective_residuals: list[float] = []
    for _ in range(12):
        vector = rng.normal(size=block_rank)
        vector /= np.linalg.norm(vector)
        projector = np.outer(vector, vector)
        embedded = np.zeros((dimension, dimension), dtype=complex)
        embedded[3:6, 3:6] = projector
        flowed = rho_is @ embedded @ rho_minus_is
        projective_residuals.append(float(np.linalg.norm(flowed - embedded)))

    flowed_state = rho_is @ rho @ rho_minus_is
    state_invariance_residual = float(np.linalg.norm(flowed_state - rho))
    trace_flow_residual = float(
        np.linalg.norm(trace_state @ chain_edge - chain_edge @ trace_state)
    )
    entropy = float(-np.sum(np.diag(rho) * np.log(np.diag(rho))))
    flowed_entropy = float(
        -np.sum(np.diag(flowed_state).real * np.log(np.diag(flowed_state).real))
    )

    result = {
        "gate": "version6_projective_quench_parent_dynamics_gate",
        "recognized_internal_time_frameworks": {
            "page_wootters_relational_clock": "recognized_but_project_constraint_missing",
            "connes_rovelli_thermal_time": "recognized_and_partially_realized",
            "rovelli_partial_observables": "recognized_relational_language",
        },
        "existing_project_modular_state": {
            "algebra": "M18(C)",
            "beta": beta,
            "state_is_faithful": bool(np.min(np.diag(rho)) > 0.0),
            "state_is_tracial": False,
            "modular_generator": "beta*ad(h_F)",
            "generator_frequency_residual": generator_frequency_residual,
            "chain_edge_motion_norm": chain_edge_motion,
            "chain_orientation_generated": chain_edge_motion > 1e-10,
        },
        "projective_orientation_test": {
            "vertex_block_rank": block_rank,
            "number_of_random_RP2_projectors": len(projective_residuals),
            "maximum_modular_motion_residual": max(projective_residuals),
            "h_F_is_scalar_on_each_triplet": True,
            "existing_modular_flow_rotates_RP2_orientation": False,
        },
        "self_quench_test": {
            "state_invariance_residual": state_invariance_residual,
            "defining_state_is_fixed_by_own_modular_flow": True,
            "von_neumann_entropy_before": entropy,
            "von_neumann_entropy_after": flowed_entropy,
            "entropy_change": flowed_entropy - entropy,
            "modular_flow_is_reversible": True,
            "relaxation_or_arrow_generated": False,
            "self_generated_quench": False,
        },
        "tracial_limit": {
            "beta_zero_state": "I/18",
            "commutator_residual": trace_flow_residual,
            "modular_flow": "trivial",
        },
        "page_wootters_project_candidate": {
            "existing_order_four_loop_dimension": 4,
            "unitary_clock_like_shift_exists": True,
            "clock_system_tensor_factor_fixed": False,
            "global_stationary_constraint_H_clock_plus_H_system": False,
            "clock_system_entanglement_derived": False,
            "status": "open_not_yet_a_relational_clock",
        },
        "verdict": {
            "internal_time_idea": "mathematically_recognized_and_project_relevant",
            "existing_modular_time": "orients_chain_but_not_projective_quench",
            "external_time_in_previous_quench_gate": "provisional_only",
            "matter_and_time_coemergence": "open_hypothesis_not_proved",
            "matter_birth_proved": False,
            "next_gate": "version6_relational_clock_projective_quench_gate",
        },
    }

    assert generator_frequency_residual < 1e-12
    assert chain_edge_motion > 1e-6
    assert max(projective_residuals) < 1e-12
    assert state_invariance_residual < 1e-12
    assert abs(flowed_entropy - entropy) < 1e-12
    assert trace_flow_residual < 1e-12

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_projective_quench_parent_dynamics_gate_results.json"
    )
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()