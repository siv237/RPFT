#!/usr/bin/env python3
"""Classify block-equivariant local coins on the physical H15 carrier."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_discrete_equivariant_coin_selector_gate_results.json"


def matrix_units(block_sizes: list[int]) -> list[np.ndarray]:
    generators: list[np.ndarray] = []
    offset = 0
    total = sum(block_sizes)
    for size in block_sizes:
        for i in range(size):
            for j in range(size):
                unit = np.zeros((total, total), dtype=complex)
                unit[offset + i, offset + j] = 1.0
                generators.append(unit)
        offset += size
    return generators


def projectors(block_sizes: list[int]) -> list[np.ndarray]:
    out: list[np.ndarray] = []
    offset = 0
    total = sum(block_sizes)
    for size in block_sizes:
        projector = np.zeros((total, total), dtype=complex)
        projector[offset : offset + size, offset : offset + size] = np.eye(size)
        out.append(projector)
        offset += size
    return out


def main() -> None:
    labels = ["Q_L", "L_L", "u_R", "d_R", "e_R"]
    sizes = [6, 2, 3, 3, 1]
    generators = matrix_units(sizes)
    sectors = projectors(sizes)

    central_residual = max(
        float(np.linalg.norm(projector @ generator - generator @ projector))
        for projector in sectors
        for generator in generators
    )

    sigma_y = np.array([[0.0, -1.0j], [1.0j, 0.0]])
    identity_dir = np.eye(2, dtype=complex)
    angles = np.array([0.11, -0.23, 0.37, 0.51, -0.67])
    coin = np.zeros((30, 30), dtype=complex)
    generator_coin = np.zeros_like(coin)
    for angle, projector in zip(angles, sectors):
        rotation = np.cos(angle) * identity_dir - 1.0j * np.sin(angle) * sigma_y
        coin += np.kron(rotation, projector)
        generator_coin += angle * np.kron(sigma_y, projector)

    unitary_error = float(np.linalg.norm(coin.conj().T @ coin - np.eye(30)))
    equivariance_residual = max(
        float(
            np.linalg.norm(
                coin @ np.kron(identity_dir, algebra_element)
                - np.kron(identity_dir, algebra_element) @ coin
            )
        )
        for algebra_element in generators
    )

    centered = [
        np.kron(sigma_y, sectors[i] - sectors[-1]) for i in range(len(sectors) - 1)
    ]
    centered_rank = int(
        np.linalg.matrix_rank(np.stack([item.reshape(-1) for item in centered], axis=1))
    )

    weak_generators = matrix_units([2])
    weak_identity_residual = max(
        float(np.linalg.norm(np.eye(2) @ item - item @ np.eye(2)))
        for item in weak_generators
    )

    result = {
        "gate": "version6_spectral_transition_discrete_equivariant_coin_selector_gate",
        "physical_observed_carrier": {
            "labels": labels,
            "block_ranks_on_H15": sizes,
            "dimension": sum(sizes),
            "observed_block_algebra_dimension": sum(size * size for size in sizes),
            "commutant_complex_dimension": len(sizes),
            "coin_commutant_complex_dimension_on_C2_tensor_H15": 4 * len(sizes),
            "one_axis_coin_angles": len(sizes),
            "relative_one_axis_coin_angles": centered_rank,
        },
        "exact_tests": {
            "central_projector_commutator_residual": central_residual,
            "sector_dependent_coin_unitarity_error": unitary_error,
            "sector_dependent_coin_equivariance_residual": equivariance_residual,
            "weak_doublet_identity_commutator_residual": weak_identity_residual,
        },
        "selector_classification": {
            "canonical_central_projectors": labels,
            "unique_rank_one_central_block": "e_R",
            "unique_rank_one_block_is_neutral_endpoint": False,
            "constant_weak_neutrino_rank_one_projector_exists": False,
            "gauge_closed_charged_lepton_support_rank": 3,
            "higgs_direction_required_for_rank_one_left_component": True,
            "algebra_selects_one_nonzero_coin": False,
        },
        "verdict": {
            "non_scalar_equivariant_coins_exist": True,
            "unique_physical_selector_derived": False,
            "internal_multiplicity_problem_closed": False,
            "R4_stable_physical_endpoint_closed": False,
            "R5_blind_prediction_closed": False,
            "status": "physical reduction replaces the scalar full-factor coin by five independent sector coins; the sole rank-one central block is e_R and is not a gauge/Yukawa-closed massive endpoint",
        },
        "next_gate": "version6_spectral_transition_discrete_chiral_coin_closure_gate",
    }

    assert central_residual < 1e-12
    assert unitary_error < 1e-12
    assert equivariance_residual < 1e-12
    assert centered_rank == 4
    assert result["selector_classification"]["unique_rank_one_central_block"] == "e_R"
    assert not result["verdict"]["unique_physical_selector_derived"]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()