#!/usr/bin/env python3
"""Test modular, collision and spectral-gap candidates for intrinsic time."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh, expm


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_intrinsic_noise_clock_dilation_gate_results.json"
TOL = 1.0e-10

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import physical_blocks  # noqa: E402
from s2t_v8_minimal_covariant_stinespring_carrier_gate import (  # noqa: E402
    channel,
    positive_square_root,
)


def block_generator(incidence: np.ndarray) -> np.ndarray:
    target_dimension, source_dimension = incidence.shape
    source_gram = incidence.conj().T @ incidence
    target_gram = incidence @ incidence.conj().T
    source_diagonal = (
        -0.5 * np.kron(np.eye(source_dimension), source_gram)
        -0.5 * np.kron(source_gram.T, np.eye(source_dimension))
    )
    target_diagonal = (
        -0.5 * np.kron(np.eye(target_dimension), target_gram)
        -0.5 * np.kron(target_gram.T, np.eye(target_dimension))
    )
    return np.block(
        [
            [source_diagonal, np.kron(incidence.T, incidence.conj().T)],
            [np.kron(incidence.conj(), incidence), target_diagonal],
        ]
    )


def pair_vector(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    return np.concatenate(
        [source.reshape(-1, order="F"), target.reshape(-1, order="F")]
    )


def pair_matrix(vector: np.ndarray) -> np.ndarray:
    source = vector[: 11**2].reshape((11, 11), order="F")
    target = vector[11**2 :].reshape((10, 10), order="F")
    return np.block(
        [
            [source, np.zeros((11, 10), complex)],
            [np.zeros((10, 11), complex), target],
        ]
    )


def split_matrix(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return matrix[:11, :11], matrix[11:, 11:]


def rounded(values) -> list[float]:
    return [float(f"{value:.12g}") for value in values]


def main() -> None:
    _, variations, labels, _ = physical_blocks()
    heavy = variations[7:]
    cross_indices = [
        index
        for index, label in enumerate(labels)
        if label.startswith(("QLYR", "XLdR"))
    ]
    incidences = [
        heavy[index] / np.linalg.norm(heavy[index], ord="fro")
        for index in cross_indices
    ]
    jumps = [
        np.block(
            [
                [np.zeros((11, 11), complex), incidence.conj().T],
                [incidence, np.zeros((10, 10), complex)],
            ]
        )
        for incidence in incidences
    ]
    jump_sum = sum(jump @ jump for jump in jumps)
    generator = sum(block_generator(incidence) for incidence in incidences)
    positive_generator_values = eigvalsh(-generator)
    kernel_dimension = int(np.sum(np.abs(positive_generator_values) < TOL))
    nonzero_values = positive_generator_values[kernel_dimension:]
    unit_gap = float(nonzero_values[0])
    assert kernel_dimension == 46
    assert abs(unit_gap - 0.5) < TOL

    rate_scan = []
    for rate in (1.0e-6, 1.0e-3, 1.0, 1.0e3, 1.0e6):
        rate_scan.append(
            {
                "rate_kappa": rate,
                "kernel_dimension": kernel_dimension,
                "smallest_nonzero_decay": rate * unit_gap,
                "largest_decay": rate * float(nonzero_values[-1]),
            }
        )

    quark_source = np.diag([1.0] * 6 + [0.0] * 5)
    quark_target = np.diag([1.0] * 6 + [0.0] * 4)
    lepton_source = np.eye(11) - quark_source
    lepton_target = np.eye(10) - quark_target
    quark_projector = pair_matrix(pair_vector(quark_source, quark_target))
    lepton_projector = pair_matrix(pair_vector(lepton_source, lepton_target))

    uniform_state = np.eye(21) / 21.0
    uniform_modular_hamiltonian = -np.log(1.0 / 21.0) * np.eye(21)
    uniform_modular_generator_norm = float(
        np.linalg.norm(
            1j
            * (
                uniform_modular_hamiltonian @ quark_projector
                - quark_projector @ uniform_modular_hamiltonian
            )
        )
    )
    uniform_state_motion_norm = float(
        np.linalg.norm(
            uniform_modular_hamiltonian @ uniform_state
            - uniform_state @ uniform_modular_hamiltonian
        )
    )

    # A faithful state in the selected C^2 fixed algebra can distinguish the
    # two sectors, but its modular automorphism still fixes both populations.
    quark_weight, lepton_weight = 0.6, 0.4
    central_state = (
        quark_weight * quark_projector / 12.0
        + lepton_weight * lepton_projector / 9.0
    )
    state_values, state_vectors = np.linalg.eigh(central_state)
    central_modular_hamiltonian = state_vectors @ np.diag(-np.log(state_values)) @ state_vectors.conj().T

    def modular_action(observable: np.ndarray) -> np.ndarray:
        return 1j * (
            central_modular_hamiltonian @ observable
            - observable @ central_modular_hamiltonian
        )

    central_modular_projector_norms = [
        float(np.linalg.norm(modular_action(projector)))
        for projector in (quark_projector, lepton_projector)
    ]

    quark_source_vector, quark_target_vector = split_matrix(quark_projector)
    dissipative_quark_motion = generator @ pair_vector(
        quark_source_vector, quark_target_vector
    )
    dissipative_quark_motion_norm = float(np.linalg.norm(dissipative_quark_motion))
    assert uniform_modular_generator_norm == 0.0
    assert uniform_state_motion_norm == 0.0
    assert max(central_modular_projector_norms) < TOL
    assert dissipative_quark_motion_norm > 1.0

    # Repeated fresh-ancilla collisions converge to exp(tL) when p=t/n, but
    # the identification of n and p with physical duration remains extra.
    rng = np.random.default_rng(20260828)
    source_seed = rng.normal(size=(11, 11)) + 1j * rng.normal(size=(11, 11))
    target_seed = rng.normal(size=(10, 10)) + 1j * rng.normal(size=(10, 10))
    source_observable = source_seed + source_seed.conj().T
    target_observable = target_seed + target_seed.conj().T
    initial_vector = pair_vector(source_observable, target_observable)
    macroscopic_time = 0.1
    exact_vector = expm(macroscopic_time * generator) @ initial_vector
    exact_matrix = pair_matrix(exact_vector)

    collision_scan = []
    for collisions in (1, 2, 5, 10, 100, 1000):
        step = macroscopic_time / collisions
        no_jump = positive_square_root(np.eye(21) - step * jump_sum)
        kraus = [no_jump] + [np.sqrt(step) * jump for jump in jumps]
        evolved = pair_matrix(initial_vector)
        for _ in range(collisions):
            evolved = channel(kraus, evolved)
        error = float(np.linalg.norm(evolved - exact_matrix))
        collision_scan.append(
            {
                "fresh_ancilla_collisions": collisions,
                "step_probability": step,
                "error_from_exp_tL": error,
            }
        )
    assert all(
        collision_scan[index + 1]["error_from_exp_tL"]
        < collision_scan[index]["error_from_exp_tL"]
        for index in range(len(collision_scan) - 1)
    )
    assert collision_scan[-1]["error_from_exp_tL"] < 1.0e-3

    previous = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v8_minimal_covariant_stinespring_carrier_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    projective_time = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v6_projective_quench_parent_dynamics_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    four_tick_clock = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v6_clock_controlled_energy_conserving_quench_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert not previous["verdict"]["autonomous_continuous_time_dilation_derived"]
    assert projective_time["verdict"]["existing_modular_time"] == "orients_chain_but_not_projective_quench"
    assert not four_tick_clock["verdict"]["canonical_order_four_clock_is_autonomous_refrigerator"]

    result = {
        "date": "2026-08-28",
        "gate": "version8_intrinsic_noise_clock_dilation_gate",
        "dimensionless_semigroup": {
            "formula": "T_u=exp(u L_cross)",
            "cross_generator_kernel_dimension": kernel_dimension,
            "unit_rate_smallest_nonzero_decay": unit_gap,
            "unit_rate_largest_decay": float(nonzero_values[-1]),
            "rate_rescaling_scan": rate_scan,
            "fixed_algebra_and_covariance_structure_change_under_positive_rate_rescaling": False,
        },
        "modular_time_test": {
            "uniform_stationary_state": "I21/21",
            "uniform_modular_generator_on_quark_projector_norm": uniform_modular_generator_norm,
            "uniform_state_motion_norm": uniform_state_motion_norm,
            "faithful_C2_state_sector_weights": [quark_weight, lepton_weight],
            "central_projector_modular_motion_norms": central_modular_projector_norms,
            "dissipative_quark_projector_motion_norm": dissipative_quark_motion_norm,
            "modular_flow_reproduces_cross_sector_dissipation": False,
            "reason": "the state-generated modular flow is reversible and fixes the sector populations",
        },
        "fresh_ancilla_collision_limit": {
            "macroscopic_dimensionless_time": macroscopic_time,
            "rule": "p=u/n with one fresh 13-dimensional ancilla per collision",
            "convergence_scan": collision_scan,
            "continuous_limit_recovered": True,
            "fresh_ancilla_supply_derived": False,
            "physical_duration_per_collision_derived": False,
        },
        "inherited_clock_candidates": {
            "tome6_modular_flow_orients_but_does_not_switch": True,
            "tome6_four_tick_clock_is_autonomous_noise_source": False,
            "new_clock_system_coupling_to_cross_environment_derived": False,
        },
        "verdict": {
            "canonical_dimensionless_lindblad_time_exists": True,
            "cross_noise_multiplicity_space_derived": True,
            "modular_time_generates_required_dissipation": False,
            "collision_limit_generates_semigroup_conditionally": True,
            "intrinsic_physical_rate_derived": False,
            "autonomous_fresh_noise_supply_derived": False,
            "status": "dimensionless_noise_time_positive_physical_clock_rate_no_go",
            "next_gate": "version8_detailed_balance_relative_rate_selector_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()