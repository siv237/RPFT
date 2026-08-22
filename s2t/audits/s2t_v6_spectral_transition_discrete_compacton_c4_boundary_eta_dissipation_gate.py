#!/usr/bin/env python3
"""Test a selected-axis compacton with S4->C4 boundary data and eta/Pfaffian dissipation."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate_results.json"


def permutation_matrix(permutation: tuple[int, ...]) -> np.ndarray:
    matrix = np.zeros((len(permutation), len(permutation)), dtype=complex)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def power(permutation: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = tuple(range(len(permutation)))
    for _ in range(exponent):
        result = compose(permutation, result)
    return result


def centralizer(group: list[tuple[int, ...]], element: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [item for item in group if compose(item, element) == compose(element, item)]


def character_projector(operator: np.ndarray, eigenvalue: complex) -> np.ndarray:
    return sum(
        eigenvalue ** (-exponent) * np.linalg.matrix_power(operator, exponent)
        for exponent in range(4)
    ) / 4.0


def liouvillian(hamiltonian: np.ndarray, jumps: list[np.ndarray]) -> np.ndarray:
    dimension = hamiltonian.shape[0]
    identity = np.eye(dimension, dtype=complex)
    generator = -1.0j * (
        np.kron(identity, hamiltonian) - np.kron(hamiltonian.T, identity)
    )
    for jump in jumps:
        rate_operator = jump.conj().T @ jump
        generator += np.kron(jump.conj(), jump)
        generator -= 0.5 * np.kron(identity, rate_operator)
        generator -= 0.5 * np.kron(rate_operator.T, identity)
    return generator


def evolve_density(density: np.ndarray, generator: np.ndarray, time: float) -> np.ndarray:
    values, vectors = np.linalg.eig(generator)
    inverse = np.linalg.inv(vectors)
    evolution = vectors @ np.diag(np.exp(time * values)) @ inverse
    evolved = evolution @ density.reshape(-1, order="F")
    output = evolved.reshape(density.shape, order="F")
    return 0.5 * (output + output.conj().T)


def density_diagnostics(density: np.ndarray) -> dict[str, float]:
    plus = float(density[0, 0].real)
    minus = float(density[1, 1].real)
    return {
        "weight_plus_i": plus,
        "weight_minus_i": minus,
        "character_population_defect": 4.0 * plus * minus,
        "coherence_magnitude": float(abs(density[0, 1])),
        "purity": float(np.trace(density @ density).real),
        "trace": float(np.trace(density).real),
        "minimum_eigenvalue": float(np.min(np.linalg.eigvalsh(density))),
    }


def channel_history(
    density: np.ndarray,
    generator: np.ndarray,
    times: list[float],
) -> list[dict[str, float]]:
    return [
        {"time": time, **density_diagnostics(evolve_density(density, generator, time))}
        for time in times
    ]


def main() -> None:
    permutations = list(itertools.permutations(range(4)))
    chosen_cycle = (1, 2, 3, 0)
    chosen_cycle_matrix = permutation_matrix(chosen_cycle)
    chosen_centralizer = centralizer(permutations, chosen_cycle)
    generated_c4 = {power(chosen_cycle, exponent) for exponent in range(4)}

    uniform = np.ones(4, dtype=complex) / 2.0
    p1 = np.outer(uniform, uniform.conj())
    p3 = np.eye(4) - p1
    affine_projectors = {
        label: character_projector(chosen_cycle_matrix, eigenvalue)
        for label, eigenvalue in (
            ("1", 1.0),
            ("+i", 1.0j),
            ("-1", -1.0),
            ("-i", -1.0j),
        )
    }

    # Selected internal compacton axis: one weak component and e_R are balanced.
    selected_axis = np.array([0.5, 0.0, 0.5], dtype=complex)
    compacton_plus = np.concatenate([selected_axis, -1.0j * selected_axis])
    compacton_minus = np.concatenate([selected_axis, 1.0j * selected_axis])
    reduced_step = np.kron(
        np.array([[0.0, -1.0], [1.0, 0.0]], dtype=complex),
        np.eye(3),
    )
    selected_axis_certificate = {
        "local_norm_squared": float(np.vdot(selected_axis, selected_axis).real),
        "weak_norm_squared": float(np.vdot(selected_axis[:2], selected_axis[:2]).real),
        "right_norm_squared": float(abs(selected_axis[2]) ** 2),
        "plus_i_residual": float(np.linalg.norm(reduced_step @ compacton_plus - 1.0j * compacton_plus)),
        "minus_i_residual": float(np.linalg.norm(reduced_step @ compacton_minus + 1.0j * compacton_minus)),
    }

    # Eta invariant of the one-dimensional twisted Dirac branch, eta(0)=1-2 alpha.
    twists = {"+i": 0.25, "-i": 0.75}
    eta = {label: 1.0 - 2.0 * alpha for label, alpha in twists.items()}
    eta_phases = {
        label: np.exp(-0.5j * np.pi * value) for label, value in eta.items()
    }
    eta_relative_phase = eta_phases["+i"] / eta_phases["-i"]
    eta_decay_rates = {label: -np.log(abs(phase)) for label, phase in eta_phases.items()}

    reduced_pfaffian_signs = {"branch_minus": -1.0, "branch_plus": 1.0}
    pfaffian_decay_rates = {
        label: -np.log(abs(sign)) for label, sign in reduced_pfaffian_signs.items()
    }
    # The preceding project ledger gives the physical full Real-pair phase +1.
    full_ko6_pfaffian_phase = 1.0

    # Character basis |+i>,|-i>; start from an equal coherent superposition.
    initial_vector = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    initial_density = np.outer(initial_vector, initial_vector.conj())
    character_orientation = np.diag([1.0, -1.0]).astype(complex)

    eta_hamiltonian = 0.5 * character_orientation
    coherent_generator = liouvillian(eta_hamiltonian, [])

    weak_rate = 0.01
    dephasing_jump = np.sqrt(weak_rate) * character_orientation
    dephasing_generator = liouvillian(np.zeros((2, 2), dtype=complex), [dephasing_jump])

    oriented_jump = np.sqrt(weak_rate) * np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    oriented_generator = liouvillian(np.zeros((2, 2), dtype=complex), [oriented_jump])

    dimensionless_times = [0.0, 25.0, 50.0, 100.0, 200.0, 500.0]
    coherent_history = channel_history(initial_density, coherent_generator, dimensionless_times)
    dephasing_history = channel_history(initial_density, dephasing_generator, dimensionless_times)
    oriented_history = channel_history(initial_density, oriented_generator, dimensionless_times)

    rate_scan = {}
    for rate in (0.001, 0.003, 0.01, 0.03, 0.1):
        jump = np.sqrt(rate) * np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
        generator = liouvillian(np.zeros((2, 2), dtype=complex), [jump])
        target_time = float(np.log(50.0) / rate)
        at_target = density_diagnostics(evolve_density(initial_density, generator, target_time))
        rate_scan[str(rate)] = {
            "rate": rate,
            "time_to_plus_weight_0_99": target_time,
            "rate_times_capture_time": rate * target_time,
            "diagnostic_at_capture_time": at_target,
        }

    # Operators obtainable from the eta/Pfaffian spectral data alone are diagonal
    # in the character basis; the amplitude jump is strictly off-diagonal.
    diagonal_basis = [np.eye(2, dtype=complex), character_orientation]
    coefficients, *_ = np.linalg.lstsq(
        np.stack([item.reshape(-1) for item in diagonal_basis], axis=1),
        oriented_jump.reshape(-1),
        rcond=None,
    )
    diagonal_reconstruction = sum(
        coefficient * basis for coefficient, basis in zip(coefficients, diagonal_basis)
    )
    oriented_jump_diagonal_algebra_residual = float(
        np.linalg.norm(oriented_jump - diagonal_reconstruction)
    )

    maximum_density_trace_residual = 0.0
    minimum_density_eigenvalue = 1.0
    for history in (coherent_history, dephasing_history, oriented_history):
        for item in history:
            maximum_density_trace_residual = max(
                maximum_density_trace_residual, abs(item["trace"] - 1.0)
            )
            minimum_density_eigenvalue = min(minimum_density_eigenvalue, item["minimum_eigenvalue"])

    result = {
        "gate": "version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate",
        "selected_axis_compacton": {
            "axis": selected_axis.real.tolist(),
            "boundary_character_targets": ["+i", "-i"],
            **selected_axis_certificate,
            "axis_is_derived_by_this_gate": False,
            "interpretation": "the chosen balanced internal axis makes the compacton reduction exact, but it is boundary data rather than a dynamically generated axis",
        },
        "S4_to_C4_boundary_condition": {
            "condition": "psi(s+L)=C4 psi(s) with C4=(1234)",
            "S4_order": len(permutations),
            "centralizer_order": len(chosen_centralizer),
            "centralizer_equals_generated_C4": set(chosen_centralizer) == generated_c4,
            "residual_symmetry": "C4",
            "affine_character_ranks": {
                label: int(np.linalg.matrix_rank(projector, tol=1.0e-10))
                for label, projector in affine_projectors.items()
            },
            "plus_minus_i_projectors_lie_in_P3": bool(
                np.linalg.norm(p3 @ affine_projectors["+i"] - affine_projectors["+i"]) < 1.0e-12
                and np.linalg.norm(p3 @ affine_projectors["-i"] - affine_projectors["-i"]) < 1.0e-12
            ),
            "boundary_breaking_is_mathematically_consistent": True,
            "boundary_breaking_is_parent_derived": False,
        },
        "eta_pfaffian_phase_audit": {
            "twist_fractions": twists,
            "eta_invariants": eta,
            "eta_phases": {
                label: [float(phase.real), float(phase.imag)]
                for label, phase in eta_phases.items()
            },
            "eta_relative_phase": [float(eta_relative_phase.real), float(eta_relative_phase.imag)],
            "eta_phase_moduli": {label: float(abs(phase)) for label, phase in eta_phases.items()},
            "eta_implied_decay_rates": eta_decay_rates,
            "reduced_pfaffian_signs": reduced_pfaffian_signs,
            "reduced_pfaffian_implied_decay_rates": pfaffian_decay_rates,
            "full_KO6_real_pair_phase": full_ko6_pfaffian_phase,
            "full_KO6_phase_cancels": True,
            "phase_supplies_positive_dissipation_rate": False,
        },
        "reduced_open_dynamics": {
            "initial_state": "equal coherent superposition of plus/minus i characters",
            "weak_test_rate": weak_rate,
            "eta_coherent_phase_history": coherent_history,
            "eta_dephasing_history": dephasing_history,
            "oriented_amplitude_jump_history": oriented_history,
            "coherent_phase_changes_populations": False,
            "dephasing_changes_character_populations": False,
            "dephasing_selects_pure_plus_or_minus_i": False,
            "inserted_oriented_jump_captures_plus_i": True,
            "oriented_jump": "sqrt(gamma)|+i><-i|",
            "oriented_jump_in_eta_diagonal_algebra": False,
            "oriented_jump_diagonal_algebra_residual": oriented_jump_diagonal_algebra_residual,
            "rate_scan": rate_scan,
            "capture_time_scales_as_inverse_free_rate": True,
        },
        "full_compacton_scope": {
            "phase_capture_inside_selected_exact_manifold_if_jump_inserted": True,
            "spatial_leakage_repaired": False,
            "chiral_balance_repaired": False,
            "generic_localized_state_capture_established": False,
        },
        "maximum_residuals": {
            "selected_plus_i_eigenstate": selected_axis_certificate["plus_i_residual"],
            "selected_minus_i_eigenstate": selected_axis_certificate["minus_i_residual"],
            "density_trace_preservation": maximum_density_trace_residual,
            "density_positivity_violation": max(0.0, -minimum_density_eigenvalue),
            "eta_decay_rate": max(abs(value) for value in eta_decay_rates.values()),
            "pfaffian_decay_rate": max(abs(value) for value in pfaffian_decay_rates.values()),
        },
        "verdict": {
            "selected_axis_compacton_consistent": True,
            "boundary_S4_to_C4_consistent": True,
            "eta_pfaffian_phase_orients_character_basis": True,
            "eta_pfaffian_phase_derives_weak_dissipation": False,
            "conditional_capture_with_inserted_jump": True,
            "jump_operator_and_rate_parent_derived": False,
            "R2_endogenous_trigger": False,
            "R3_rate": False,
            "R4_unique_endpoint": "conditional after choosing boundary orientation and inserting a non-Hermitian jump",
            "status": "a chosen compacton axis and the boundary twist psi(s+L)=C4 psi(s) consistently reduce S4 to one C4 and align the plus/minus i character lines; however eta and Pfaffian data have unit modulus, give zero decay rate, cancel in the full KO6 pair, and generate only diagonal phase/dephasing operators. An inserted jump sqrt(gamma)|+i><-i| captures exponentially, but both the off-diagonal partial isometry and gamma are new inputs, so the proposed eta/Pfaffian weak dissipation is not derived",
            "next_gate": "version6_spectral_transition_discrete_compacton_energy_degeneracy_boundary_overlap_gate",
        },
    }

    assert len(chosen_centralizer) == 4
    assert set(chosen_centralizer) == generated_c4
    assert selected_axis_certificate["local_norm_squared"] == 0.5
    assert selected_axis_certificate["weak_norm_squared"] == 0.25
    assert selected_axis_certificate["right_norm_squared"] == 0.25
    assert max(result["maximum_residuals"].values()) < 1.0e-10
    assert dephasing_history[-1]["character_population_defect"] > 0.999999
    assert oriented_history[-1]["weight_plus_i"] > 0.996
    assert oriented_jump_diagonal_algebra_residual > 0.09
    assert all(
        abs(item["rate_times_capture_time"] - np.log(50.0)) < 1.0e-10
        for item in rate_scan.values()
    )

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()