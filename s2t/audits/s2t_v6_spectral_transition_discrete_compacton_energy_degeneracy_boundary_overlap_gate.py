#!/usr/bin/env python3
"""Audit energy degeneracy, nonlinear selection, and boundary overlap of the +/-i compactons."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_discrete_compacton_energy_degeneracy_boundary_overlap_gate_results.json"
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)


def chiral_generator(block: np.ndarray) -> np.ndarray:
    higgs_eff = sum(block[d, :2] * np.conj(block[d, 2]) for d in range(2))
    out = np.zeros((3, 3), dtype=complex)
    out[:2, 2] = higgs_eff
    out[2, :2] = np.conj(higgs_eff)
    return out


def local_generator(block: np.ndarray) -> np.ndarray:
    return np.kron(SIGMA_Y, chiral_generator(block))


def local_coin(block: np.ndarray, coupling: float) -> np.ndarray:
    generator = local_generator(block)
    values, vectors = np.linalg.eigh(generator)
    unitary = (vectors * np.exp(-1.0j * coupling * values)) @ vectors.conj().T
    return (unitary @ block.reshape(6)).reshape(2, 3)


def step(state: np.ndarray, coupling: float) -> np.ndarray:
    coined = np.empty_like(state)
    for site, block in enumerate(state):
        coined[site] = local_coin(block, coupling)
    shifted = np.empty_like(coined)
    shifted[:, 0, :] = np.roll(coined[:, 0, :], 1, axis=0)
    shifted[:, 1, :] = np.roll(coined[:, 1, :], -1, axis=0)
    return shifted


def selected_state(relative_phase: complex, sites: int = 64) -> np.ndarray:
    vector = np.array([0.5, 0.0, 0.5], dtype=complex)
    center = sites // 2
    state = np.zeros((sites, 2, 3), dtype=complex)
    state[center, 1, :] = vector
    state[center + 1, 0, :] = relative_phase * vector
    return state


def branch_state(sign: int, sites: int = 64) -> np.ndarray:
    # sign=+1 gives eigenphase +i; sign=-1 gives eigenphase -i.
    return selected_state(-1.0j * sign, sites)


def state_real_invariants(state: np.ndarray) -> dict[str, float]:
    probability = np.sum(np.abs(state) ** 2, axis=(1, 2))
    sites = np.arange(len(state), dtype=float)
    center = float(np.sum(sites * probability))
    radius_squared = float(np.sum((sites - center) ** 2 * probability))
    inverse_participation = float(np.sum(probability**2))

    nonlinear_intensity = 0.0
    composite_higgs_norm = 0.0
    generator_expectation = 0.0
    generator_square_expectation = 0.0
    for block in state:
        weak = np.sum(np.abs(block[:, :2]) ** 2, axis=1)
        right = np.abs(block[:, 2]) ** 2
        nonlinear_intensity += float(np.sum(weak * right))
        higgs_eff = sum(block[d, :2] * np.conj(block[d, 2]) for d in range(2))
        composite_higgs_norm += float(np.vdot(higgs_eff, higgs_eff).real)
        vector = block.reshape(6)
        generator = local_generator(block)
        generator_expectation += float(np.vdot(vector, generator @ vector).real)
        generator_square_expectation += float(
            np.vdot(vector, generator @ generator @ vector).real
        )
    return {
        "norm": float(np.vdot(state, state).real),
        "center": center,
        "radius_squared": radius_squared,
        "inverse_participation": inverse_participation,
        "nonlinear_intensity_sum_pq": nonlinear_intensity,
        "composite_higgs_norm_squared": composite_higgs_norm,
        "instantaneous_coin_generator_expectation": generator_expectation,
        "instantaneous_coin_generator_square_expectation": generator_square_expectation,
    }


def character_weights(state: np.ndarray, plus: np.ndarray, minus: np.ndarray) -> tuple[float, float]:
    return float(abs(np.vdot(plus, state)) ** 2), float(abs(np.vdot(minus, state)) ** 2)


def character_projector(operator: np.ndarray, eigenvalue: complex) -> np.ndarray:
    return sum(
        eigenvalue ** (-exponent) * np.linalg.matrix_power(operator, exponent)
        for exponent in range(4)
    ) / 4.0


def normalized_projector_vector(projector: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(projector)
    vector = vectors[:, int(np.argmax(values))]
    return vector / np.linalg.norm(vector)


def rk4_gradient_flow(initial: float, final_time: float, steps: int) -> float:
    def velocity(weight: float) -> float:
        return 4.0 * weight * (1.0 - weight) * (2.0 * weight - 1.0)

    value = initial
    step_size = final_time / steps
    for _ in range(steps):
        k1 = velocity(value)
        k2 = velocity(value + 0.5 * step_size * k1)
        k3 = velocity(value + 0.5 * step_size * k2)
        k4 = velocity(value + step_size * k3)
        value += step_size * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    return float(value)


def main() -> None:
    coupling = 2.0 * np.pi
    plus = branch_state(+1)
    minus = branch_state(-1)
    plus /= np.linalg.norm(plus)
    minus /= np.linalg.norm(minus)

    branch_data = {}
    for label, state, eigenphase in (("+i", plus, 1.0j), ("-i", minus, -1.0j)):
        evolved = step(state, coupling)
        branch_data[label] = {
            "one_step_eigenstate_residual": float(np.linalg.norm(evolved - eigenphase * state)),
            "real_invariants": state_real_invariants(state),
            "quasienergy_angle_principal": float(-np.angle(eigenphase)),
            "quasienergy_absolute_angle": float(abs(np.angle(eigenphase))),
        }

    invariant_names = list(branch_data["+i"]["real_invariants"])
    real_invariant_differences = {
        name: abs(
            branch_data["+i"]["real_invariants"][name]
            - branch_data["-i"]["real_invariants"][name]
        )
        for name in invariant_names
    }

    # Exact nonlinear phase family: all points have the same local real energy data.
    phase_scan = []
    maximum_weight_drift = 0.0
    maximum_real_energy_spread = 0.0
    reference_invariants = None
    for phase in np.linspace(0.0, 2.0 * np.pi, 33)[:-1]:
        state = selected_state(np.exp(1.0j * phase))
        state /= np.linalg.norm(state)
        initial_weights = character_weights(state, plus, minus)
        initial_invariants = state_real_invariants(state)
        if reference_invariants is None:
            reference_invariants = initial_invariants
        maximum_real_energy_spread = max(
            maximum_real_energy_spread,
            *(abs(initial_invariants[name] - reference_invariants[name]) for name in invariant_names),
        )
        evolved = state.copy()
        for _ in range(40):
            evolved = step(evolved, coupling)
        final_weights = character_weights(evolved, plus, minus)
        maximum_weight_drift = max(
            maximum_weight_drift,
            abs(initial_weights[0] - final_weights[0]),
            abs(initial_weights[1] - final_weights[1]),
        )
        phase_scan.append(
            {
                "phase_over_pi": float(phase / np.pi),
                "initial_weight_plus_i": initial_weights[0],
                "initial_weight_minus_i": initial_weights[1],
                "final_weight_plus_i": final_weights[0],
                "final_weight_minus_i": final_weights[1],
                "initial_D_chi": 4.0 * initial_weights[0] * initial_weights[1],
                "final_D_chi": 4.0 * final_weights[0] * final_weights[1],
            }
        )

    # Boundary spectra for alpha and 1-alpha are exactly paired by n -> -n-1.
    alpha_plus = 0.25
    alpha_minus = 0.75
    boundary_spectral_pair_residuals = []
    for integer in range(-64, 65):
        mapped = -integer - 1
        boundary_spectral_pair_residuals.append(
            abs((integer + alpha_plus) ** 2 - (mapped + alpha_minus) ** 2)
        )

    determinant_modulus_scan = {}
    for rho in (0.1, 0.3, 1.0, 3.0, 10.0):
        values = {}
        for label, alpha in (("+i", alpha_plus), ("-i", alpha_minus)):
            values[label] = float(
                np.log(
                    (np.cosh(2.0 * np.pi * rho) - np.cos(2.0 * np.pi * alpha))
                    / (np.cosh(2.0 * np.pi * rho) - 1.0)
                )
            )
        values["difference"] = abs(values["+i"] - values["-i"])
        determinant_modulus_scan[str(rho)] = values

    # Affine boundary height h=-P3 gives the same energy to all nontrivial characters.
    cycle = np.zeros((4, 4), dtype=complex)
    for source, target in enumerate((1, 2, 3, 0)):
        cycle[target, source] = 1.0
    uniform = np.ones(4, dtype=complex) / 2.0
    p3 = np.eye(4) - np.outer(uniform, uniform.conj())
    height = -p3
    projectors = {
        "+i": character_projector(cycle, 1.0j),
        "-1": character_projector(cycle, -1.0),
        "-i": character_projector(cycle, -1.0j),
    }
    vectors = {label: normalized_projector_vector(projector) for label, projector in projectors.items()}
    affine_height_energies = {
        label: float(np.vdot(vector, height @ vector).real)
        for label, vector in vectors.items()
    }

    # A scalar normal derivative cannot mix inequivalent C4 characters.
    scalar_boundary_overlap = complex(np.vdot(vectors["+i"], vectors["-i"]))
    rng = np.random.default_rng(20260821)
    equivariant_overlap_residuals = []
    for _ in range(64):
        coefficients = rng.normal(size=4) + 1.0j * rng.normal(size=4)
        operator = sum(
            coefficients[power_index] * np.linalg.matrix_power(cycle, power_index)
            for power_index in range(4)
        )
        equivariant_overlap_residuals.append(
            abs(np.vdot(vectors["+i"], operator @ vectors["-i"]))
        )

    character_mixer = np.outer(vectors["+i"], vectors["-i"].conj())
    mixer_minus_character_residual = float(
        np.linalg.norm(cycle @ character_mixer @ cycle.conj().T + character_mixer)
    )
    mixer_scalar_character_residual = float(
        np.linalg.norm(cycle @ character_mixer @ cycle.conj().T - character_mixer)
    )

    gradient_flow_scan = {}
    for initial in (0.49, 0.499, 0.5, 0.501, 0.51):
        final = rk4_gradient_flow(initial, final_time=10.0, steps=20000)
        gradient_flow_scan[str(initial)] = {
            "initial_weight_plus_i": initial,
            "final_weight_plus_i": final,
            "initial_D_chi": 4.0 * initial * (1.0 - initial),
            "final_D_chi": 4.0 * final * (1.0 - final),
        }

    result = {
        "gate": "version6_spectral_transition_discrete_compacton_energy_degeneracy_boundary_overlap_gate",
        "exact_branch_comparison": {
            "branches": branch_data,
            "real_invariant_absolute_differences": real_invariant_differences,
            "maximum_real_invariant_difference": max(real_invariant_differences.values()),
            "profiles_are_complex_conjugate": True,
            "support_and_radius_exactly_equal": True,
            "signed_principal_quasienergies_opposite": True,
            "absolute_quasienergy_equal": True,
            "physical_static_energy_functional_defined_by_current_walk": False,
        },
        "nonlinear_phase_family": {
            "phase_count": len(phase_scan),
            "maximum_character_weight_drift_after_40_steps": maximum_weight_drift,
            "maximum_real_invariant_spread": maximum_real_energy_spread,
            "equal_mixture_is_nonlinearly_unstable_in_exact_walk": False,
            "self_focusing_of_character_population_observed": False,
            "scan": phase_scan,
        },
        "boundary_real_action": {
            "twists": {"+i": alpha_plus, "-i": alpha_minus},
            "spectral_pairing": "(n+1/4)^2=(-n-1+3/4)^2",
            "maximum_squared_spectrum_pair_residual": max(boundary_spectral_pair_residuals),
            "determinant_modulus_scan": determinant_modulus_scan,
            "maximum_determinant_modulus_difference": max(
                item["difference"] for item in determinant_modulus_scan.values()
            ),
            "affine_height_energies": affine_height_energies,
            "eta_invariants_opposite": [0.5, -0.5],
            "eta_changes_real_boundary_energy": False,
        },
        "boundary_overlap": {
            "scalar_normal_derivative_overlap": [
                float(scalar_boundary_overlap.real),
                float(scalar_boundary_overlap.imag),
            ],
            "maximum_C4_equivariant_operator_overlap": max(equivariant_overlap_residuals),
            "scalar_or_C4_equivariant_boundary_operator_mixes_plus_minus_i": False,
            "required_mixer_character": "-1",
            "mixer_transforms_as_minus_one_residual": mixer_minus_character_residual,
            "mixer_transforms_as_scalar_residual": mixer_scalar_character_residual,
            "affine_P3_contains_minus_one_mediator_line": True,
            "minus_one_boundary_mode_profile_or_condensate_derived": False,
        },
        "projected_Dchi_gradient": {
            "dimensionless_flow": "dw_plus/ds=4 w_plus(1-w_plus)(2w_plus-1)",
            "gradient_flow_scan": gradient_flow_scan,
            "equal_mixture_is_fixed": True,
            "equal_mixture_is_unstable_under_biased_gradient_flow": True,
            "P3_fixes_flow_direction_but_not_physical_time_metric": True,
            "physical_rate_derived": False,
        },
        "verdict": {
            "plus_minus_compacton_real_energies_exactly_degenerate": True,
            "boundary_real_actions_exactly_degenerate": True,
            "nonlinear_walk_amplifies_character_bias": False,
            "scalar_boundary_derivative_generates_transition": False,
            "coefficient_free_gradient_flow_selects_after_bias": True,
            "gradient_flow_is_parent_dynamics": False,
            "new_structural_clue": "the unique off-diagonal plus/minus i mixer carries C4 character -1, which already exists as the third affine P3 line; a derived dynamical boundary mode in that line could mediate coherent mixing, but dissipation would still require its continuum spectral density or an open channel",
            "status": "all currently defined real bulk, nonlinear, affine-height, and boundary-determinant energies are exactly equal for the plus/minus i compactons. The exact nonlinear phase family conserves character weights, and a scalar normal derivative has zero boundary overlap. A projected Dchi gradient would select a branch in dimensionless relaxation time, but declaring that gradient law supplies the missing dissipation. The only nontrivial new clue is the affine -1 character line required by the off-diagonal boundary mixer",
            "next_gate": "version6_spectral_transition_discrete_compacton_character_resolved_radiation_form_factor_gate",
        },
    }

    assert max(real_invariant_differences.values()) < 1.0e-14
    assert maximum_weight_drift < 1.0e-11
    # The analytic spread is zero; the center accumulator reaches 1.42e-14
    # roundoff for one sampled phase on binary64.
    assert maximum_real_energy_spread < 2.0e-14
    assert max(boundary_spectral_pair_residuals) == 0.0
    assert result["boundary_real_action"]["maximum_determinant_modulus_difference"] < 1.0e-14
    assert max(abs(value + 1.0) for value in affine_height_energies.values()) < 1.0e-14
    assert abs(scalar_boundary_overlap) < 1.0e-14
    assert max(equivariant_overlap_residuals) < 1.0e-13
    assert mixer_minus_character_residual < 1.0e-14
    assert mixer_scalar_character_residual > 1.0
    assert gradient_flow_scan["0.49"]["final_weight_plus_i"] < 1.0e-6
    assert gradient_flow_scan["0.51"]["final_weight_plus_i"] > 1.0 - 1.0e-6
    assert gradient_flow_scan["0.5"]["final_weight_plus_i"] == 0.5

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()