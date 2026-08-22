#!/usr/bin/env python3
"""Audit the character-resolved compacton form factor into the walk radiation continuum."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_discrete_compacton_character_resolved_radiation_form_factor_gate_results.json"
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)


def chiral_generator(block: np.ndarray) -> np.ndarray:
    higgs_eff = sum(block[d, :2] * np.conj(block[d, 2]) for d in range(2))
    out = np.zeros((3, 3), dtype=complex)
    out[:2, 2] = higgs_eff
    out[2, :2] = np.conj(higgs_eff)
    return out


def local_coin(block: np.ndarray, coupling: float) -> np.ndarray:
    generator = np.kron(SIGMA_Y, chiral_generator(block))
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


def four_steps(state: np.ndarray, coupling: float) -> np.ndarray:
    for _ in range(4):
        state = step(state, coupling)
    return state


def branch_state(relative_sign: int, sites: int) -> np.ndarray:
    center = sites // 2
    local = np.array([0.5, 0.0, 0.5], dtype=complex)
    state = np.zeros((sites, 2, 3), dtype=complex)
    state[center, 1, :] = local
    state[center + 1, 0, :] = relative_sign * 1.0j * local
    return state


def jacobian_action(base: np.ndarray, direction: np.ndarray, epsilon: float = 1.0e-6) -> np.ndarray:
    coupling = 2.0 * np.pi
    return (
        four_steps(base + epsilon * direction, coupling)
        - four_steps(base - epsilon * direction, coupling)
    ) / (2.0 * epsilon)


def outside_core(state: np.ndarray) -> np.ndarray:
    center = len(state) // 2
    outside = state.copy()
    outside[center : center + 2] = 0.0
    return outside


def nonlinear_core_scan(plus: np.ndarray, minus: np.ndarray) -> dict[str, object]:
    coupling = 2.0 * np.pi
    center = len(plus) // 2
    cycles = 20
    scan = {}
    for label, direction, amplitudes in (
        ("eta_oriented_radiative", minus, (1.0e-4, 3.0e-4, 1.0e-3)),
        ("orthogonal_neutral", -1.0j * minus, (1.0e-3,)),
    ):
        branch = {}
        for amplitude in amplitudes:
            state = plus + amplitude * direction
            state /= np.linalg.norm(state)
            initial_minus_weight = float(abs(np.vdot(minus, state)) ** 2)
            core_history = []
            for time in range(4 * cycles + 1):
                if time % 4 == 0:
                    density = np.sum(np.abs(state) ** 2, axis=(1, 2))
                    core_history.append(float(density[center] + density[center + 1]))
                if time < 4 * cycles:
                    state = step(state, coupling)
            core = np.zeros_like(state)
            core[center : center + 2] = state[center : center + 2]
            final_minus_weight = float(abs(np.vdot(minus, core)) ** 2)
            final_plus_weight = float(abs(np.vdot(plus, core)) ** 2)
            predicted_loss = 1.0 - np.exp(-4.0 * np.pi**2 * amplitude**2 * cycles)
            branch[str(amplitude)] = {
                "initial_minus_character_weight": initial_minus_weight,
                "final_minus_character_weight_in_core": final_minus_weight,
                "final_plus_character_weight_in_core": final_plus_weight,
                "final_core_probability": core_history[-1],
                "radiated_probability": 1.0 - core_history[-1],
                "weak_limit_exponential_prediction": float(predicted_loss),
                "prediction_absolute_error": float(abs((1.0 - core_history[-1]) - predicted_loss)),
                "core_probability_history_per_cycle": core_history,
            }
        scan[label] = branch
    return {"cycles": cycles, "scan": scan}


def main() -> None:
    sites = 256
    plus = branch_state(+1, sites)
    minus = branch_state(-1, sites)
    center = sites // 2

    branch_overlap = complex(np.vdot(plus, minus))
    plus_phase_residual = float(np.linalg.norm(step(plus, 2.0 * np.pi) - 1.0j * plus))
    minus_phase_residual = float(np.linalg.norm(step(minus, 2.0 * np.pi) + 1.0j * minus))

    # For H_theta=e^{i theta}T+e^{-i theta}T^dagger, the tangent from |+i>
    # is -i e^{-i theta}|-i>. The eta-oriented coefficient -i means theta=-pi/2.
    quadrature_scan = {}
    maximum_quadrature_formula_residual = 0.0
    for theta in np.linspace(-np.pi, np.pi, 17):
        direction = -1.0j * np.exp(-1.0j * theta) * minus
        evolved = jacobian_action(plus, direction)
        radiation_norm = float(np.linalg.norm(outside_core(evolved)))
        formula = float(2.0 * np.pi * abs(np.sin(theta)))
        maximum_quadrature_formula_residual = max(
            maximum_quadrature_formula_residual, abs(radiation_norm - formula)
        )
        quadrature_scan[str(theta / np.pi)] = {
            "theta_over_pi": float(theta / np.pi),
            "radiation_norm_after_one_return": radiation_norm,
            "formula_2pi_abs_sin_theta": formula,
        }

    neutral_direction = -1.0j * minus
    eta_direction = minus
    neutral_evolved = jacobian_action(plus, neutral_direction)
    eta_evolved = jacobian_action(plus, eta_direction)
    neutral_fixed_residual = float(np.linalg.norm(neutral_evolved - neutral_direction))
    eta_source_projection = complex(np.vdot(minus, eta_evolved))
    first_outgoing_packet = eta_evolved - eta_direction
    first_outgoing_norm = float(np.linalg.norm(first_outgoing_packet))
    first_outgoing_norm_squared = float(np.vdot(first_outgoing_packet, first_outgoing_packet).real)

    # Repeated Jacobian action emits spatially disjoint packets before periodic wrap-around.
    outgoing_packets = []
    state = eta_direction.copy()
    secular_scan = []
    for cycle in range(1, 9):
        evolved = jacobian_action(plus, state)
        packet = evolved - state
        outgoing_packets.append(packet)
        state = evolved
        secular_scan.append(
            {
                "cycle": cycle,
                "total_tangent_norm_squared": float(np.vdot(state, state).real),
                "outside_core_norm_squared": float(
                    np.vdot(outside_core(state), outside_core(state)).real
                ),
                "minus_source_projection": [
                    float(np.vdot(minus, state).real),
                    float(np.vdot(minus, state).imag),
                ],
            }
        )

    packet_gram = np.array(
        [[np.vdot(left, right) for right in outgoing_packets] for left in outgoing_packets]
    )
    packet_norms = np.sqrt(np.real(np.diag(packet_gram)))
    maximum_packet_norm_residual = float(np.max(np.abs(packet_norms - 2.0 * np.pi)))
    maximum_packet_overlap = float(
        np.max(np.abs(packet_gram - np.diag(np.diag(packet_gram))))
    )
    maximum_secular_norm_residual = max(
        abs(item["total_tangent_norm_squared"] - (1.0 + 4.0 * np.pi**2 * item["cycle"]))
        for item in secular_scan
    )

    # Fourier form factor at multiplier one of the four-step vacuum shift.
    positions = np.arange(sites) - center
    resonant_momenta = (0.0, 0.5 * np.pi, np.pi, 1.5 * np.pi)
    resonant_form_factors = {}
    for momentum in resonant_momenta:
        amplitude = np.einsum(
            "x,xdi->di", np.exp(-1.0j * momentum * positions), first_outgoing_packet
        )
        resonant_form_factors[str(momentum / np.pi)] = float(np.linalg.norm(amplitude) ** 2)
    spectral_density_at_multiplier_one = float(
        sum(resonant_form_factors.values()) / (8.0 * np.pi)
    )
    golden_rule_coefficient = float(2.0 * np.pi * spectral_density_at_multiplier_one)

    nonlinear = nonlinear_core_scan(branch_state(+1, 512), branch_state(-1, 512))
    weak_scan = nonlinear["scan"]["eta_oriented_radiative"]
    neutral_scan = nonlinear["scan"]["orthogonal_neutral"]

    result = {
        "gate": "version6_spectral_transition_discrete_compacton_character_resolved_radiation_form_factor_gate",
        "exact_branches": {
            "plus_i_one_step_residual": plus_phase_residual,
            "minus_i_one_step_residual": minus_phase_residual,
            "branch_overlap": [float(branch_overlap.real), float(branch_overlap.imag)],
            "four_step_linearization_base": "+i compacton",
        },
        "character_quadratures": {
            "hermitian_mixer": "H_theta=e^{i theta}T+e^{-i theta}T^dagger",
            "tangent": "delta_Psi=-i e^{-i theta}|-i>",
            "quadrature_scan": quadrature_scan,
            "maximum_2pi_abs_sin_theta_formula_residual": maximum_quadrature_formula_residual,
            "theta_zero_neutral_fixed_residual": neutral_fixed_residual,
            "reduced_eta_phase_minus_i_theta": -0.5,
            "eta_oriented_radiation_norm": first_outgoing_norm,
            "eta_oriented_radiation_norm_squared": first_outgoing_norm_squared,
            "eta_source_projection_after_return": [
                float(eta_source_projection.real), float(eta_source_projection.imag)
            ],
            "orthogonal_phase_quadrature_is_exact_compacton_manifold_tangent": True,
        },
        "outgoing_channel": {
            "packet_count": len(outgoing_packets),
            "packet_norms": packet_norms.tolist(),
            "maximum_packet_norm_residual_from_2pi": maximum_packet_norm_residual,
            "maximum_distinct_packet_overlap": maximum_packet_overlap,
            "secular_scan": secular_scan,
            "maximum_norm_squared_residual_from_1_plus_4pi2_n": maximum_secular_norm_residual,
            "interpretation": "each return emits a new outward packet of norm 2pi while the character-source projection remains one; this is a generalized secular source, not a decaying eigenmode",
        },
        "spectral_form_factor": {
            "vacuum_four_step_multiplier": "exp(plus_or_minus 4 i k)",
            "resonant_momenta_over_pi": [0.0, 0.5, 1.0, 1.5],
            "resonant_form_factor_norm_squared": resonant_form_factors,
            "spectral_density_at_multiplier_one": spectral_density_at_multiplier_one,
            "golden_rule_coefficient_per_four_step_cycle": golden_rule_coefficient,
            "coefficient_identity": "2pi*rho_rad(0)=4pi^2",
            "absolutely_continuous_outgoing_channel_detected": True,
        },
        "nonlinear_validation": nonlinear,
        "capture_test": {
            "eta_radiative_smallest_amplitude_final_minus_weight": weak_scan["0.0001"]["final_minus_character_weight_in_core"],
            "eta_radiative_smallest_amplitude_initial_minus_weight": weak_scan["0.0001"]["initial_minus_character_weight"],
            "eta_radiative_smallest_amplitude_core_loss": weak_scan["0.0001"]["radiated_probability"],
            "neutral_amplitude_core_loss": neutral_scan["0.001"]["radiated_probability"],
            "undesired_character_is_damped": False,
            "compacton_core_is_depleted": True,
            "generic_complex_character_tangent_has_neutral_quadrature": True,
        },
        "verdict": {
            "character_resolved_radiation_form_factor_nonzero": True,
            "dimensionless_radiation_coefficient_derived": True,
            "coefficient_per_cycle": "4pi^2 times squared eta-oriented perturbation amplitude",
            "radiation_is_capture": False,
            "reason": "the source projection remains fixed while orthogonal outgoing packets accumulate; nonlinear evolution loses compacton core probability without suppressing the minus-character weight, and the orthogonal phase quadrature remains exactly neutral",
            "manual_gamma_replaced_by_successful_autonomous_capture_rate": False,
            "status": "the full Floquet Jacobian has a nonzero, analytically normalized form factor from the eta-oriented -1 character quadrature into the spatial radiation continuum. The density at the resonant multiplier is 2pi and gives the exact weak coefficient 4pi^2 per four-step cycle. However this is a secular emitter rather than amplitude damping: the undesired character component is not depleted, the compacton core radiates, and the orthogonal character quadrature is a fixed tangent of the exact compacton manifold. The mechanism therefore destabilizes the compacton instead of selecting one branch",
            "next_gate": "version6_spectral_transition_discrete_compacton_branch_status_freeze_gate",
        },
    }

    assert plus_phase_residual < 1.0e-12
    assert minus_phase_residual < 1.0e-12
    assert abs(branch_overlap) < 1.0e-14
    assert neutral_fixed_residual < 1.0e-8
    assert maximum_quadrature_formula_residual < 2.0e-7
    assert abs(first_outgoing_norm - 2.0 * np.pi) < 2.0e-8
    assert abs(first_outgoing_norm_squared - 4.0 * np.pi**2) < 2.0e-7
    assert abs(eta_source_projection - 1.0) < 2.0e-8
    assert maximum_packet_norm_residual < 3.0e-8
    assert maximum_packet_overlap < 5.0e-8
    assert maximum_secular_norm_residual < 2.0e-6
    assert abs(spectral_density_at_multiplier_one - 2.0 * np.pi) < 2.0e-8
    assert abs(golden_rule_coefficient - 4.0 * np.pi**2) < 2.0e-7
    assert weak_scan["0.0001"]["prediction_absolute_error"] < 2.0e-8
    assert weak_scan["0.0001"]["final_minus_character_weight_in_core"] > 0.99 * weak_scan["0.0001"]["initial_minus_character_weight"]
    assert abs(neutral_scan["0.001"]["radiated_probability"]) < 2.0e-12

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()