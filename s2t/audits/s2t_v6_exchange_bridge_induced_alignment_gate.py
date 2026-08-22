#!/usr/bin/env python3
"""Audit the family-matrix extension of the canonical exchange bridge."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def bridge_action(matrix: np.ndarray) -> float:
    identity = np.eye(3)
    left = identity - matrix.T @ matrix
    right = identity - matrix @ matrix.T
    return float((np.trace(left @ left) + np.trace(right @ right)) / 21.0)


def state_action(state: np.ndarray) -> float:
    return float((6.0 / 7.0) * (np.trace(state @ state) - 1.0 / 3.0))


def main() -> None:
    scalar_residuals = []
    for coupling in np.linspace(0.0, 1.0, 21):
        matrix_value = bridge_action(coupling * np.eye(3))
        scalar_value = 2.0 * (1.0 - coupling**2) ** 2 / 7.0
        scalar_residuals.append(abs(matrix_value - scalar_value))

    rng = np.random.default_rng(20260819)
    fixed_trace = 3.0
    purity_samples = []
    action_samples = []
    for _ in range(1000):
        eigenvalues = rng.dirichlet(np.ones(3)) * fixed_trace
        x = np.diag(eigenvalues)
        purity_samples.append(float(np.trace(x @ x)))
        action_samples.append(float(2.0 * np.trace((np.eye(3) - x) ** 2) / 21.0))

    isotropic_state = np.eye(3) / 3.0
    critical_state = np.diag([2.0 / 3.0, 1.0 / 6.0, 1.0 / 6.0])
    pure_state = np.diag([1.0, 0.0, 0.0])

    critical_cost = state_action(critical_state)
    pure_cost = state_action(pure_state)
    fluctuation_threshold = float(np.log(4.0) + 6.0 / 7.0)

    result = {
        "gate": "version6_exchange_bridge_induced_alignment_gate",
        "matrix_bridge_extension": {
            "action": "(Tr(I-BtB)^2+Tr(I-BBt)^2)/21",
            "maximum_scalar_recovery_residual": max(scalar_residuals),
            "fixed_trace_X": fixed_trace,
            "minimum_sampled_purity": min(purity_samples),
            "theoretical_minimum_purity": fixed_trace**2 / 3.0,
            "minimum_sampled_action": min(action_samples),
            "isotropic_global_minimum": True,
        },
        "normalized_state_dictionary": {
            "identification": "R=(B^t B)/3 on Tr(B^t B)=3",
            "state_action": "(6/7)*(Tr(R^2)-1/3)",
            "effective_alignment_kappa": -6.0 / 7.0,
            "isotropic_cost": state_action(isotropic_state),
            "critical_RP2_state_cost": critical_cost,
            "critical_RP2_state_cost_exact": "1/7",
            "pure_state_cost": pure_cost,
            "sign_favors_alignment": False,
        },
        "fluctuation_kill_threshold": {
            "required_effective_kappa": float(np.log(4.0)),
            "bridge_isotropic_penalty": 6.0 / 7.0,
            "required_negative_fluctuation_coefficient": fluctuation_threshold,
            "exact_expression": "log(4)+6/7",
        },
        "verdict": {
            "canonical_bridge_induces_negative_purity": False,
            "canonical_bridge_stabilizes_isotropic_state": True,
            "RP2_birth_from_current_bridge": False,
            "next_gate": "version6_bridge_fluctuation_determinant_purity_gate",
        },
    }

    assert max(scalar_residuals) < 1.0e-14
    assert state_action(isotropic_state) == 0.0
    assert abs(critical_cost - 1.0 / 7.0) < 1.0e-14
    assert abs(pure_cost - 4.0 / 7.0) < 1.0e-14
    assert min(purity_samples) >= fixed_trace**2 / 3.0 - 1.0e-12
    assert fluctuation_threshold > np.log(4.0)

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_exchange_bridge_induced_alignment_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()