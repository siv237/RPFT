#!/usr/bin/env python3
"""Audit whether the four-state carrier can absorb the ordering entropy."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def von_neumann_entropy(matrix: np.ndarray) -> float:
    eigenvalues = np.linalg.eigvalsh(matrix)
    positive = eigenvalues[eigenvalues > 1e-14]
    return float(-np.sum(positive * np.log(positive)))


def reduced_system(matrix: np.ndarray, d_system: int, d_clock: int) -> np.ndarray:
    tensor = matrix.reshape(d_system, d_clock, d_system, d_clock)
    return np.einsum("icjc->ij", tensor)


def reduced_clock(matrix: np.ndarray, d_system: int, d_clock: int) -> np.ndarray:
    tensor = matrix.reshape(d_system, d_clock, d_system, d_clock)
    return np.einsum("icid->cd", tensor)


def state_pieces(axis_weight: float) -> tuple[float, float]:
    state = np.array(
        [axis_weight, 0.5 * (1.0 - axis_weight), 0.5 * (1.0 - axis_weight)]
    )
    second = float(np.sum(state**2))
    third = float(np.sum(state**3))
    energy = (2.0 / 7.0) * (1.0 - second**2 / third) + 1.0 - second
    entropy = float(-np.sum(state * np.log(state)))
    return entropy, energy


def equal_weight_ensemble(spectrum: np.ndarray) -> np.ndarray:
    dimension = spectrum.size
    vectors = []
    for k in range(dimension):
        phases = np.exp(2j * np.pi * k * np.arange(dimension) / dimension)
        vectors.append(np.sqrt(spectrum) * phases)
    return np.stack(vectors)


def main() -> None:
    d_system = 3
    d_clock = 4
    coexistence_axis = 0.9121665962741361
    coexistence_beta = 1.5426695408602848
    ordered_spectrum = np.array(
        [coexistence_axis, 0.5 * (1.0 - coexistence_axis), 0.5 * (1.0 - coexistence_axis)]
    )
    isotropic = np.eye(d_system) / d_system

    entropy_isotropic = float(np.log(d_system))
    entropy_ordered, energy_ordered = state_pieces(coexistence_axis)
    _, energy_isotropic = state_pieces(1.0 / 3.0)
    entropy_export = entropy_isotropic - entropy_ordered
    energy_release = energy_isotropic - energy_ordered
    clock_entropy_capacity = float(np.log(d_clock))
    minimum_sink_dimension = int(np.ceil(np.exp(entropy_export) - 1e-12))

    clock_zero = np.zeros((d_clock, d_clock), dtype=complex)
    clock_zero[0, 0] = 1.0
    initial_global = np.kron(isotropic, clock_zero)

    ensemble = equal_weight_ensemble(ordered_spectrum)
    target_vectors = []
    for clock_index, system_vector in enumerate(ensemble):
        clock_vector = np.zeros(d_clock, dtype=complex)
        clock_vector[clock_index] = 1.0
        target_vectors.append(np.kron(system_vector, clock_vector))
    target_vectors = np.stack(target_vectors)
    target_global = sum(
        np.outer(vector, vector.conj()) for vector in target_vectors
    ) / d_system

    target_system = reduced_system(target_global, d_system, d_clock)
    target_clock = reduced_clock(target_global, d_system, d_clock)
    target_global_entropy = von_neumann_entropy(target_global)
    target_system_entropy = von_neumann_entropy(target_system)
    target_clock_entropy = von_neumann_entropy(target_clock)
    target_mutual_information = (
        target_system_entropy + target_clock_entropy - target_global_entropy
    )

    initial_spectrum = np.linalg.eigvalsh(initial_global)
    target_spectrum = np.linalg.eigvalsh(target_global)
    target_gram = target_vectors @ target_vectors.conj().T

    result = {
        "gate": "version6_internal_entropy_transfer_cooling_gate",
        "ordering_budget": {
            "isotropic_system_entropy": entropy_isotropic,
            "coexistence_ordered_entropy": entropy_ordered,
            "entropy_export_required": entropy_export,
            "isotropic_effective_energy": energy_isotropic,
            "coexistence_ordered_effective_energy": energy_ordered,
            "effective_energy_released": energy_release,
            "coexistence_identity_beta_delta_energy_equals_delta_entropy": (
                coexistence_beta * energy_release
            ),
        },
        "four_state_carrier": {
            "dimension": d_clock,
            "maximum_entropy_capacity_from_pure_state": clock_entropy_capacity,
            "fraction_of_capacity_used_by_ordering": entropy_export / clock_entropy_capacity,
            "minimum_pure_sink_dimension_from_entropy_bound": minimum_sink_dimension,
            "entropy_capacity_sufficient": clock_entropy_capacity >= entropy_export,
        },
        "explicit_closed_unitary_kinematics": {
            "initial_global_spectrum": initial_spectrum.tolist(),
            "target_global_spectrum": target_spectrum.tolist(),
            "same_global_spectrum_implies_unitary_orbit": True,
            "target_system_spectrum": np.linalg.eigvalsh(target_system).tolist(),
            "target_clock_spectrum": np.linalg.eigvalsh(target_clock).tolist(),
            "target_global_entropy": target_global_entropy,
            "target_system_entropy": target_system_entropy,
            "target_clock_entropy": target_clock_entropy,
            "target_mutual_information": target_mutual_information,
        },
        "clock_backreaction": {
            "clock_initially_pure": True,
            "clock_final_entropy": target_clock_entropy,
            "clock_final_rank": int(np.linalg.matrix_rank(target_clock, tol=1e-12)),
            "phase_clock_preserved_by_constructed_transfer": False,
            "finite_clock_recurrence_avoided": False,
        },
        "missing_parent_data": {
            "clock_hamiltonian_from_U4_alone": False,
            "energy_conserving_system_clock_coupling": False,
            "autonomous_control_hamiltonian": False,
            "monotone_reduced_beta_law": False,
            "thermodynamic_or_coarse_grained_limit": False,
        },
        "maximum_residuals": {
            "target_vector_orthonormality": float(
                np.linalg.norm(target_gram - np.eye(d_system))
            ),
            "global_spectrum_preservation": float(
                np.linalg.norm(initial_spectrum - target_spectrum)
            ),
            "target_system_state": float(
                np.linalg.norm(target_system - np.diag(ordered_spectrum))
            ),
            "entropy_free_energy_coexistence": abs(
                coexistence_beta * energy_release - entropy_export
            ),
            "entropy_balance": abs(
                (target_clock_entropy - 0.0)
                - entropy_export
                - target_mutual_information
            ),
        },
        "verdict": {
            "four_state_carrier_can_absorb_ordering_entropy_kinematically": True,
            "closed_unitary_orbit_to_ordered_reduced_state_exists": True,
            "four_tick_shift_itself_derives_cooling": False,
            "autonomous_energy_conserving_cooling_derived": False,
            "irreversible_internal_arrow_derived": False,
            "matter_birth_fully_derived": False,
            "next_gate": "version6_clock_controlled_energy_conserving_quench_gate",
        },
    }

    assert minimum_sink_dimension == 3
    assert clock_entropy_capacity > entropy_export
    assert all(value < 2e-12 for value in result["maximum_residuals"].values())

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_internal_entropy_transfer_cooling_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()