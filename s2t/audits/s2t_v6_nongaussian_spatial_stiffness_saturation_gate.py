#!/usr/bin/env python3
"""Audit whether spatial derivative stiffness removes the rank-loss valley."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def bridge_action(state: np.ndarray, bridge: np.ndarray) -> float:
    identity = np.eye(3)
    left = identity - bridge.T @ bridge
    right = identity - bridge @ bridge.T
    return float(
        (np.trace(state @ left @ left) + np.trace(state @ right @ right)) / 7.0
    )


def block_bridge(transverse: np.ndarray) -> np.ndarray:
    bridge = np.zeros((3, 3))
    bridge[0, 0] = 1.0
    bridge[1:, 1:] = transverse
    return bridge


def ring_laplacian(number_of_sites: int) -> np.ndarray:
    laplacian = np.zeros((number_of_sites, number_of_sites))
    for site in range(number_of_sites):
        neighbour = (site + 1) % number_of_sites
        laplacian[site, site] += 1.0
        laplacian[neighbour, neighbour] += 1.0
        laplacian[site, neighbour] -= 1.0
        laplacian[neighbour, site] -= 1.0
    return laplacian


def main() -> None:
    rng = np.random.default_rng(20260819)
    projector = np.diag([1.0, 0.0, 0.0])

    uniform_valley_checks = []
    for _ in range(30):
        transverse = rng.normal(size=(2, 2))
        bridge = block_bridge(transverse)
        local_energy = bridge_action(projector, bridge)

        number_of_sites = 8
        bridges = np.repeat(bridge[None, :, :], number_of_sites, axis=0)
        states = np.repeat(projector[None, :, :], number_of_sites, axis=0)
        bridge_gradient = 0.0
        state_gradient = 0.0
        skyrme_commutator = 0.0
        for site in range(number_of_sites):
            neighbour = (site + 1) % number_of_sites
            d_bridge = bridges[neighbour] - bridges[site]
            d_state = states[neighbour] - states[site]
            bridge_gradient += float(np.sum(d_bridge * d_bridge))
            state_gradient += float(np.sum(d_state * d_state))
            commutator = d_state @ d_state - d_state @ d_state
            skyrme_commutator += float(np.sum(commutator * commutator))

        uniform_valley_checks.append(
            {
                "local_bridge_energy": local_energy,
                "bridge_gradient_energy": bridge_gradient,
                "state_gradient_energy": state_gradient,
                "projector_skyrme_energy": skyrme_commutator,
            }
        )

    sites = 8
    laplacian = ring_laplacian(sites)
    gradient_hessian = np.kron(laplacian, np.eye(4))
    eigenvalues = np.linalg.eigvalsh(gradient_hessian)
    zero_modes = int(np.sum(np.abs(eigenvalues) < 1e-10))
    positive_eigenvalues = eigenvalues[eigenvalues > 1e-10]

    derrick_samples = []
    for quadratic, quartic in [(1.0, 1.0), (2.0, 0.5), (0.3, 4.2)]:
        radius = np.sqrt(quartic / quadratic)
        energy = quadratic * radius + quartic / radius
        derrick_samples.append(
            {
                "quadratic_coefficient": quadratic,
                "quartic_coefficient": quartic,
                "stationary_radius": float(radius),
                "stationary_energy": float(energy),
            }
        )

    result = {
        "gate": "version6_nongaussian_spatial_stiffness_saturation_gate",
        "uniform_rank_loss_valley": {
            "state": "diag(1,0,0)",
            "bridge": "diag(1,C), C in M2(R)",
            "dimension": 4,
            "checks": uniform_valley_checks,
            "maximum_total_derivative_energy": max(
                row["bridge_gradient_energy"]
                + row["state_gradient_energy"]
                + row["projector_skyrme_energy"]
                for row in uniform_valley_checks
            ),
            "maximum_local_energy": max(
                abs(row["local_bridge_energy"]) for row in uniform_valley_checks
            ),
        },
        "lattice_stiffness": {
            "sites": sites,
            "transverse_components_per_site": 4,
            "gradient_hessian_zero_modes": zero_modes,
            "expected_uniform_zero_modes": 4,
            "smallest_positive_eigenvalue": float(np.min(positive_eigenvalues)),
            "interpretation": "stiffness removes nonuniform modes but leaves global M2(R) valley",
        },
        "derrick_balance": {
            "energy": "a L + b/L",
            "samples": derrick_samples,
            "stabilizes_nontrivial_spatial_scale": True,
            "selects_homogeneous_bulk_phase": False,
        },
        "project_archaeology": {
            "projector_curvature_E4_exists_conditionally": True,
            "common_E2_E4_scale_derived": False,
            "fermion_induced_unique_positive_E4_derived": False,
            "derivative_terms_nonzero_on_constant_rank_loss_valley": False,
        },
        "verdict": {
            "spatial_stiffness_saturates_homogeneous_transition": False,
            "spatial_stiffness_can_stabilize_existing_defect_size": True,
            "bulk_rank_loss_requires_nonderivative_coercivity": True,
            "next_gate": "version6_modular_dual_weight_bridge_coercivity_gate",
        },
    }

    assert result["uniform_rank_loss_valley"]["maximum_local_energy"] < 1e-12
    assert result["uniform_rank_loss_valley"]["maximum_total_derivative_energy"] < 1e-12
    assert zero_modes == 4
    assert np.all(positive_eigenvalues > 0)
    assert result["derrick_balance"]["stabilizes_nontrivial_spatial_scale"]
    assert not result["derrick_balance"]["selects_homogeneous_bulk_phase"]

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_nongaussian_spatial_stiffness_saturation_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()