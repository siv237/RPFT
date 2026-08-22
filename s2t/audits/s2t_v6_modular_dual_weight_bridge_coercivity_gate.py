#!/usr/bin/env python3
"""Audit direct, commutant, KMS and inverse modular bridge weights."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np


def bridge_defects(bridge: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    identity = np.eye(3)
    return identity - bridge.T @ bridge, identity - bridge @ bridge.T


def gns_action(state: np.ndarray, bridge: np.ndarray) -> float:
    left, right = bridge_defects(bridge)
    return float((np.trace(state @ left @ left) + np.trace(state @ right @ right)) / 7.0)


def kms_action(state: np.ndarray, bridge: np.ndarray) -> float:
    left, right = bridge_defects(bridge)
    eigenvalues, eigenvectors = np.linalg.eigh(state)
    sqrt_state = (eigenvectors * np.sqrt(eigenvalues)) @ eigenvectors.T
    value = np.trace(sqrt_state @ left @ sqrt_state @ left)
    value += np.trace(sqrt_state @ right @ sqrt_state @ right)
    return float(value / 7.0)


def inverse_action(state: np.ndarray, bridge: np.ndarray) -> float:
    left, right = bridge_defects(bridge)
    inverse = np.linalg.inv(state)
    return float((np.trace(inverse @ left @ left) + np.trace(inverse @ right @ right)) / 7.0)


def relative_entropy_tracial_reference(state: np.ndarray) -> float:
    eigenvalues = np.linalg.eigvalsh(state)
    return float(-np.mean(np.log(eigenvalues)) - np.log(3.0))


def block_bridge(transverse: np.ndarray) -> np.ndarray:
    bridge = np.zeros((3, 3))
    bridge[0, 0] = 1.0
    bridge[1:, 1:] = transverse
    return bridge


def main() -> None:
    rng = np.random.default_rng(20260819)
    projector = np.diag([1.0, 0.0, 0.0])

    transpose_checks = []
    for _ in range(20):
        raw = rng.normal(size=(3, 3))
        state = raw @ raw.T + np.eye(3)
        state /= np.trace(state)
        bridge = rng.normal(size=(3, 3))
        direct = gns_action(state, bridge)
        commutant = gns_action(state.T, bridge.T)
        transpose_checks.append(
            {
                "direct_action": direct,
                "commutant_action": commutant,
                "residual": direct - commutant,
            }
        )

    boundary_scaling = []
    transverse = np.array([[1.7, -0.4], [0.3, 0.8]])
    bridge = block_bridge(transverse)
    for epsilon in [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4]:
        state = np.diag([1.0 - 2.0 * epsilon, epsilon, epsilon])
        boundary_scaling.append(
            {
                "epsilon": epsilon,
                "gns_action": gns_action(state, bridge),
                "commutant_sum_action": 2.0 * gns_action(state, bridge),
                "kms_action": kms_action(state, bridge),
                "inverse_weight_action": inverse_action(state, bridge),
                "tracial_reference_relative_entropy": relative_entropy_tracial_reference(
                    state
                ),
                "modular_condition_number": float(
                    np.max(np.diag(state)) / np.min(np.diag(state))
                ),
            }
        )

    projector_checks = []
    for _ in range(20):
        transverse_random = rng.normal(size=(2, 2))
        bridge_random = block_bridge(transverse_random)
        projector_checks.append(
            {
                "direct": gns_action(projector, bridge_random),
                "commutant_sum": 2.0 * gns_action(projector, bridge_random),
                "kms": kms_action(projector, bridge_random),
            }
        )

    baseline_curvature = Fraction(-51, 112)
    tracial_relative_entropy_curvature = Fraction(3, 2)
    combined_curvature = baseline_curvature + tracial_relative_entropy_curvature

    result = {
        "gate": "version6_modular_dual_weight_bridge_coercivity_gate",
        "direct_commutant_test": {
            "identity": "S_R(B)=S_{R^T}(B^T) for symmetric real data",
            "maximum_residual": max(abs(row["residual"]) for row in transpose_checks),
            "samples": transpose_checks,
        },
        "projector_valley": {
            "maximum_direct_action": max(abs(row["direct"]) for row in projector_checks),
            "maximum_commutant_sum_action": max(
                abs(row["commutant_sum"]) for row in projector_checks
            ),
            "maximum_kms_action": max(abs(row["kms"]) for row in projector_checks),
            "valley_lifted": False,
        },
        "faithful_boundary_scaling": {
            "samples": boundary_scaling,
            "gns_tends_to_zero": True,
            "kms_tends_to_zero": True,
            "inverse_weight_diverges": True,
            "modular_operator_becomes_unbounded": True,
        },
        "relative_entropy_reference_test": {
            "reference": "I3/3",
            "functional": "D(I3/3 || R) = -(1/3) log det R - log 3",
            "barrier_weight": "1/3",
            "quadratic_curvature": str(tracial_relative_entropy_curvature),
            "combined_with_bridge_instability": str(combined_curvature),
            "instability_survives": combined_curvature < 0,
        },
        "project_archaeology": {
            "tome5_modular_state_is_faithful_gibbs_state": True,
            "tome5_beta_fixed_by_parent": False,
            "tome5_uses_modular_operator_for_orientation": True,
            "tome5_derives_inverse_weight_energy": False,
            "family_R_identified_with_rho_beta": False,
        },
        "verdict": {
            "commutant_conjugation_adds_complementary_weight": False,
            "canonical_GNS_or_KMS_norm_lifts_kernel": False,
            "inverse_modular_weight_is_available_as_new_model_term": True,
            "inverse_modular_weight_derived_by_current_parent": False,
            "canonical_tracial_relative_entropy_preserves_self_start": False,
            "modular_dual_coercivity_parent_action_proved": False,
            "next_gate": "version6_self_consistent_state_bridge_purification_gate",
        },
    }

    assert result["direct_commutant_test"]["maximum_residual"] < 1e-12
    assert result["projector_valley"]["maximum_direct_action"] < 1e-12
    assert result["projector_valley"]["maximum_commutant_sum_action"] < 1e-12
    assert result["projector_valley"]["maximum_kms_action"] < 1e-12
    assert boundary_scaling[-1]["gns_action"] < boundary_scaling[0]["gns_action"]
    assert boundary_scaling[-1]["kms_action"] < boundary_scaling[0]["kms_action"]
    assert (
        boundary_scaling[-1]["inverse_weight_action"]
        > boundary_scaling[0]["inverse_weight_action"]
    )
    assert combined_curvature == Fraction(117, 112)
    assert combined_curvature > 0

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_modular_dual_weight_bridge_coercivity_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()