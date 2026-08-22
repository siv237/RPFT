#!/usr/bin/env python3
"""Audit whether Real-pair compacton radiation is a derived projective cooling parent."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_real_pair_radiative_cooling_parent_gate_results.json"
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)


def load(name: str) -> dict[str, object]:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


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
    return (
        four_steps(base + epsilon * direction, 2.0 * np.pi)
        - four_steps(base - epsilon * direction, 2.0 * np.pi)
    ) / (2.0 * epsilon)


def outside_core(state: np.ndarray) -> np.ndarray:
    center = len(state) // 2
    out = state.copy()
    out[center : center + 2] = 0.0
    return out


def main() -> None:
    reprioritization = load("s2t_v6_spectral_transition_post_compacton_program_reprioritization_gate_results.json")
    radiation = load("s2t_v6_spectral_transition_discrete_compacton_character_resolved_radiation_form_factor_gate_results.json")
    cooling = load("s2t_v6_modular_cooling_projective_transition_gate_results.json")
    entropy = load("s2t_v6_internal_entropy_transfer_cooling_gate_results.json")
    multiplicity = load("s2t_v6_existing_multiplicity_resonant_sink_gate_results.json")
    scale = load("s2t_v6_spectral_transition_discrete_compacton_physical_scale_map_gate_results.json")

    assert reprioritization["selected_route"] == "real_pair_radiative_cooling_parent"
    assert radiation["verdict"]["radiation_is_capture"] is False
    assert cooling["missing_parent_data"]["cooling_law_beta_of_internal_time"] is False
    assert entropy["missing_parent_data"]["energy_conserving_system_clock_coupling"] is False
    assert multiplicity["canonical_affine_coupling_test"]["creates_uniaxial_split"] is False
    assert scale["dimensional_rank_test"]["scale_nullity"] == 1

    sites = 256
    plus = branch_state(+1, sites)
    minus = branch_state(-1, sites)
    plus_packet = outside_core(jacobian_action(plus, minus) - minus)
    minus_packet = outside_core(jacobian_action(minus, plus) - plus)

    plus_flux = float(np.vdot(plus_packet, plus_packet).real)
    minus_flux = float(np.vdot(minus_packet, minus_packet).real)
    half_trace_flux = 0.5 * (plus_flux + minus_flux)
    conjugacy_residual = float(np.linalg.norm(minus_packet - np.conj(plus_packet)))
    real_odd_amplitude_residual = float(np.linalg.norm(plus_packet - np.conj(minus_packet)))
    real_even_energy_residual = float(abs(half_trace_flux - 4.0 * np.pi**2))
    cross_overlap = complex(np.vdot(plus_packet, minus_packet))

    delta_energy = entropy["ordering_budget"]["effective_energy_released"]
    conditional_balance = []
    for cycles in (1, 2, 4, 8, 16, 32):
        delta_if_unit_conversion = float(np.sqrt(delta_energy / (half_trace_flux * cycles)))
        conditional_balance.append(
            {
                "cycles": cycles,
                "delta_if_walk_norm_equals_projective_energy": delta_if_unit_conversion,
                "delta_squared_times_cycles": float(delta_if_unit_conversion**2 * cycles),
                "weak_core_survival_if_same_coefficient": float(np.exp(-half_trace_flux * delta_if_unit_conversion**2 * cycles)),
            }
        )

    parent_ledger = {
        "Real_even_pair_flux_survives_half_trace": True,
        "Real_odd_oriented_amplitude_survives": False,
        "compacton_walk_and_projective_R_share_one_declared_Hilbert_carrier": False,
        "common_parent_action_normalizes_walk_flux_against_projective_energy": False,
        "derived_interaction_between_R_and_outgoing_walk_modes": False,
        "delta_derived_from_parent_state": False,
        "physical_step_time_derived": False,
        "monotone_beta_law_derived": False,
        "outgoing_unitary_radiation_by_itself_exports_von_Neumann_entropy": False,
        "coarse_graining_or_partial_trace_to_define_entropy_sink_derived": False,
        "canonical_affine_link_is_axis_selective": False,
    }
    required_parent_items = [
        "Real_even_pair_flux_survives_half_trace",
        "compacton_walk_and_projective_R_share_one_declared_Hilbert_carrier",
        "common_parent_action_normalizes_walk_flux_against_projective_energy",
        "derived_interaction_between_R_and_outgoing_walk_modes",
        "delta_derived_from_parent_state",
        "monotone_beta_law_derived",
        "coarse_graining_or_partial_trace_to_define_entropy_sink_derived",
    ]
    passed_items = [item for item in required_parent_items if parent_ledger[item]]
    failed_items = [item for item in required_parent_items if not parent_ledger[item]]
    assert passed_items == ["Real_even_pair_flux_survives_half_trace"]
    assert len(failed_items) == 6

    result = {
        "gate": "version6_spectral_transition_real_pair_radiative_cooling_parent_gate",
        "Real_pair_radiation_test": {
            "plus_packet_norm_squared": plus_flux,
            "minus_packet_norm_squared": minus_flux,
            "physical_half_trace_flux": half_trace_flux,
            "expected_4pi2": float(4.0 * np.pi**2),
            "half_trace_flux_residual": real_even_energy_residual,
            "minus_packet_is_conjugate_plus_packet_residual": conjugacy_residual,
            "Real_odd_oriented_amplitude_residual": real_odd_amplitude_residual,
            "cross_overlap": [float(cross_overlap.real), float(cross_overlap.imag)],
            "interpretation": "Real conjugation cancels orientation-sensitive linear data but the positive quadratic radiation flux survives the physical half-trace with coefficient 4pi^2 rather than doubling or vanishing",
        },
        "conditional_energy_matching": {
            "projective_effective_energy_released_at_coexistence": delta_energy,
            "assumption_for_table_only": "one unit of walk tangent norm squared equals one unit of projective effective energy",
            "cycle_scan": conditional_balance,
            "degeneracy": "for an unknown conversion chi, only chi*N*4pi^2*delta^2=DeltaE is fixed; neither chi nor delta nor N is selected",
            "unit_conversion_is_parent_derived": False,
        },
        "entropy_test": {
            "required_export": entropy["ordering_budget"]["entropy_export_required"],
            "global_walk_update_is_unitary": True,
            "global_pure_radiation_state_entropy_increase": 0.0,
            "orthogonal_outgoing_packets_exist": True,
            "entropy_increase_requires_reduced_state_or_coarse_graining": True,
            "projective_system_outgoing_mode_tensor_factor_and_partial_trace_derived": False,
        },
        "parent_ledger": parent_ledger,
        "required_parent_items": required_parent_items,
        "passed_parent_items": passed_items,
        "failed_parent_items": failed_items,
        "projective_thresholds": {
            "coexistence_beta": cooling["free_energy_landscape"]["coexistence_inverse_temperature"],
            "spinodal_beta": cooling["free_energy_landscape"]["isotropic_spinodal_inverse_temperature"],
            "crossing_derived": False,
        },
        "verdict": {
            "Real_pair_positive_radiation_current_nonzero": True,
            "Real_pair_phase_or_oriented_current_nonzero": False,
            "one_energy_conserving_cooling_parent_derived": False,
            "radiation_norm_is_projective_heat_current": False,
            "internal_beta_law_derived": False,
            "route_passes_parent_gate": False,
            "status": "the first obstruction is avoided: the Real-pair half-trace preserves the positive radiation coefficient 4pi^2 even though oriented amplitudes cancel. The parent gate nevertheless fails because the compacton walk and projective order parameter have no shared declared carrier, interaction or common energy normalization; delta and the physical step time remain free, and unitary outgoing packets export no projective entropy without an additional derived subsystem trace. Therefore the existing radiation channel is not yet an internal cooling law.",
            "next_gate": "version6_spectral_transition_radiative_cooling_common_carrier_attribution_gate",
        },
    }

    assert conjugacy_residual < 1.0e-8
    assert real_odd_amplitude_residual < 1.0e-8
    assert real_even_energy_residual < 2.0e-7
    assert abs(half_trace_flux - radiation["spectral_form_factor"]["golden_rule_coefficient_per_four_step_cycle"]) < 2.0e-7
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()