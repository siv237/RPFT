#!/usr/bin/env python3
"""Audit rank-stratum selection for the self-consistent bridge action."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def action(bridge: np.ndarray) -> float:
    x = np.linalg.svd(bridge, compute_uv=False) ** 2
    total = float(np.sum(x))
    if total == 0.0:
        return 2.0 / 7.0
    return float((2.0 / (7.0 * total)) * np.sum(x * (1.0 - x) ** 2))


def partial_isometry(rank: int) -> np.ndarray:
    bridge = np.zeros((3, 3))
    bridge[:rank, :rank] = np.eye(rank)
    return bridge


def numerical_hessian(bridge: np.ndarray, step: float = 2.0e-4) -> np.ndarray:
    origin = bridge.reshape(-1)
    dimension = origin.size
    hessian = np.zeros((dimension, dimension))
    center = action(bridge)
    for i in range(dimension):
        ei = np.zeros(dimension)
        ei[i] = step
        hessian[i, i] = (
            action((origin + ei).reshape(3, 3))
            - 2.0 * center
            + action((origin - ei).reshape(3, 3))
        ) / step**2
        for j in range(i + 1, dimension):
            ej = np.zeros(dimension)
            ej[j] = step
            value = (
                action((origin + ei + ej).reshape(3, 3))
                - action((origin + ei - ej).reshape(3, 3))
                - action((origin - ei + ej).reshape(3, 3))
                + action((origin - ei - ej).reshape(3, 3))
            ) / (4.0 * step**2)
            hessian[i, j] = value
            hessian[j, i] = value
    return hessian


def exterior_square(bridge: np.ndarray) -> float:
    gram = bridge.T @ bridge
    return float(0.5 * (np.trace(gram) ** 2 - np.trace(gram @ gram)))


def raw_direct_crossed_norm(bridge: np.ndarray) -> float:
    direct = np.einsum("ia,jb->iajb", bridge, bridge)
    crossed = np.einsum("ib,ja->iajb", bridge, bridge)
    return float(np.sum((direct - crossed) ** 2))


def state_free_energy(eigenvalues: np.ndarray, purity_coefficient: float) -> float:
    positive = eigenvalues[eigenvalues > 0.0]
    entropy = float(np.sum(positive * np.log(positive)))
    purity = float(np.sum(eigenvalues**2))
    return entropy - purity_coefficient * (purity - 1.0 / 3.0)


def ordered_uniaxial_root(purity_coefficient: float) -> float:
    def equation(axis_weight: float) -> float:
        transverse_weight = (1.0 - axis_weight) / 2.0
        return np.log(axis_weight / transverse_weight) - 2.0 * purity_coefficient * (
            axis_weight - transverse_weight
        )

    left, right = 0.9, 1.0 - 1e-12
    assert equation(left) < 0.0 < equation(right)
    for _ in range(100):
        middle = 0.5 * (left + right)
        if equation(middle) > 0.0:
            right = middle
        else:
            left = middle
    return 0.5 * (left + right)


def main() -> None:
    rng = np.random.default_rng(20260819)
    expected_spectra = {
        1: np.array([0.0] * 4 + [4.0 / 7.0] * 4 + [16.0 / 7.0]),
        2: np.array([0.0] * 5 + [2.0 / 7.0] + [8.0 / 7.0] * 3),
        3: np.array([0.0] * 3 + [16.0 / 21.0] * 6),
    }
    stratum_dimensions = {1: 4, 2: 5, 3: 3}

    strata = []
    maximum_hessian_residual = 0.0
    for rank in (1, 2, 3):
        bridge = partial_isometry(rank)
        eigenvalues = np.linalg.eigvalsh(numerical_hessian(bridge))
        expected = np.sort(expected_spectra[rank])
        residual = float(np.max(np.abs(eigenvalues - expected)))
        maximum_hessian_residual = max(maximum_hessian_residual, residual)
        positive = expected[expected > 0.0]
        strata.append(
            {
                "rank": rank,
                "dimension": stratum_dimensions[rank],
                "normal_dimension": 9 - stratum_dimensions[rank],
                "laplace_beta_exponent": -(9 - stratum_dimensions[rank]) / 2.0,
                "hessian_eigenvalues": eigenvalues.tolist(),
                "expected_hessian_eigenvalues": expected.tolist(),
                "positive_normal_hessian_determinant": float(np.prod(positive)),
                "entropy": float(-np.log(rank)),
                "exterior_square": exterior_square(bridge),
            }
        )

    wedge_checks = []
    for _ in range(50):
        bridge = rng.normal(size=(3, 3))
        raw = raw_direct_crossed_norm(bridge)
        target = 4.0 * exterior_square(bridge)
        wedge_checks.append({"raw": raw, "target": target, "residual": raw - target})

    induced_purity_coefficient = 2.0
    transition_threshold = np.log(4.0)
    axis_weight = ordered_uniaxial_root(induced_purity_coefficient)
    ordered_spectrum = np.array(
        [axis_weight, (1.0 - axis_weight) / 2.0, (1.0 - axis_weight) / 2.0]
    )
    ordered_free_energy = state_free_energy(ordered_spectrum, induced_purity_coefficient)
    isotropic_free_energy = state_free_energy(np.ones(3) / 3.0, induced_purity_coefficient)
    pure_free_energy = state_free_energy(np.array([1.0, 0.0, 0.0]), induced_purity_coefficient)

    result = {
        "gate": "version6_partial_isometry_rank_stratum_selection_gate",
        "zero_strata": strata,
        "morse_bott_measure": {
            "asymptotic_rule": "Z_k ~ C_k beta^{-(9-d_k)/2}",
            "dominant_rank_at_large_beta": 2,
            "reason": "rank two has the largest zero-manifold dimension d_2=5",
            "flat_measure_selects_rank_one": False,
        },
        "reduced_state_topology": {
            "rank_1_orbit": "RP2",
            "rank_2_orbit": "Gr(2,3)=RP2",
            "rank_3_orbit": "point",
            "topology_distinguishes_rank_1_from_rank_2": False,
        },
        "real_structure": {
            "operation": "B -> B^T",
            "rank_preserved": True,
            "selects_rank_one": False,
        },
        "exterior_square_candidate": {
            "identity": "||B_ia B_jb-B_ib B_ja||^2=4||wedge^2 B||^2=4 e_2(B^T B)",
            "maximum_identity_residual": max(abs(row["residual"]) for row in wedge_checks),
            "vanishes_exactly_for_rank_at_most_one": True,
            "normalized_identity": "W(R)=4 e_2(R)=2(1-Tr(R^2))",
            "one_copy_equivalent_purity_coefficient": induced_purity_coefficient,
            "first_order_transition_threshold": float(transition_threshold),
            "threshold_passed": bool(induced_purity_coefficient > transition_threshold),
            "ordered_full_rank_spectrum": ordered_spectrum.tolist(),
            "ordered_free_energy": ordered_free_energy,
            "isotropic_free_energy": isotropic_free_energy,
            "pure_boundary_free_energy": pure_free_energy,
            "ordered_orbit": "RP2",
            "exact_rank_one_selected_at_finite_entropy": False,
            "reason_exact_rank_one_fails": "epsilon log epsilon repels every finite-coupling minimum from the boundary",
            "derived_in_current_bridge_parent": False,
        },
        "verdict": {
            "entropy_selector": "rank 3",
            "flat_morse_bott_measure_selector": "rank 2",
            "topological_selector": "does not distinguish ranks 1 and 2",
            "current_parent_selects_rank_one": False,
            "strongest_reopening_candidate": "normalized direct-minus-crossed exterior-square curvature",
            "next_gate": "version6_exchange_bridge_exterior_square_parent_gate",
        },
    }

    assert maximum_hessian_residual < 2e-6
    assert result["exterior_square_candidate"]["maximum_identity_residual"] < 1e-10
    assert induced_purity_coefficient > transition_threshold
    assert ordered_free_energy < isotropic_free_energy
    assert ordered_free_energy < pure_free_energy
    assert np.all(ordered_spectrum > 0.0)
    assert result["morse_bott_measure"]["dominant_rank_at_large_beta"] == 2

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_partial_isometry_rank_stratum_selection_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()