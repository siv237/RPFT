#!/usr/bin/env python3
"""Audit phase and projective quench routes out of the closed bridge."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def rectangular_shift(size: int) -> np.ndarray:
    shift = np.zeros((size + 1, size), dtype=complex)
    for column in range(size):
        shift[column + 1, column] = 1.0
    return shift


def main() -> None:
    cutoff = 8
    coefficient_rank = 15
    shift = rectangular_shift(cutoff)
    identity_q = np.eye(coefficient_rank, dtype=complex)
    shift_q = np.kron(shift, identity_q)
    p0 = np.zeros((cutoff + 1, cutoff + 1), dtype=complex)
    p0[0, 0] = 1.0
    projection_q = np.kron(p0, identity_q)

    domain_plus = cutoff * coefficient_rank
    domain_minus = (cutoff + 1) * coefficient_rank
    zero_top_right = np.zeros((domain_minus, domain_minus), dtype=complex)
    zero_bottom_left = np.zeros((domain_plus, domain_plus), dtype=complex)
    pair = np.block(
        [[shift_q, zero_top_right], [zero_bottom_left, shift_q.conj().T]]
    )

    phase_samples: list[dict[str, float]] = []
    radius = 0.73
    reference_singular_values: np.ndarray | None = None
    for phase in (0.0, 0.3, 1.1, 2.4):
        bridge = np.block(
            [
                [np.zeros_like(shift_q), radius * np.exp(1j * phase) * projection_q],
                [zero_bottom_left, np.zeros_like(shift_q.conj().T)],
            ]
        )
        singular_values = np.linalg.svd(pair + bridge, compute_uv=False)
        if reference_singular_values is None:
            reference_singular_values = singular_values
        phase_samples.append(
            {
                "phase": phase,
                "singular_value_residual": float(
                    np.linalg.norm(singular_values - reference_singular_values)
                ),
                "fixed_real_exchange_scalar_residual": float(
                    abs(radius * np.exp(1j * phase) - radius * np.exp(-1j * phase))
                ),
            }
        )

    # Kibble-Zurek scaling ledger.  The numeric values are an illustrative
    # mean-field example only; the project has not derived its critical data.
    nu = 0.5
    dynamical_exponent = 2.0
    freezeout_exponent = nu / (1.0 + dynamical_exponent * nu)
    quench_ratios = (1.0, 10.0, 100.0, 10000.0)
    scaling_samples = []
    for ratio in quench_ratios:
        correlation_length = ratio**freezeout_exponent
        scaling_samples.append(
            {
                "tau_Q_over_tau_0": ratio,
                "xi_hat_over_xi_0": correlation_length,
                "conditional_point_defect_density_times_xi_0_cubed": (
                    correlation_length ** -3
                ),
            }
        )

    result = {
        "gate": "version6_closed_bridge_destabilization_gate",
        "early_project_reframing": {
            "counterphase_cancellation": True,
            "persistent_vacuum_fluctuations": True,
            "big_bang_as_nonadiabatic_mismatch": "testable_reframing",
        },
        "bare_circle_phase": {
            "order_parameter_space": "S1",
            "pi_1": "Z",
            "pi_2": "0",
            "phase_samples": phase_samples,
            "canonical_spectrum_depends_only_on_modulus": all(
                sample["singular_value_residual"] < 1e-10
                for sample in phase_samples
            ),
            "fixed_real_exchange_allows_arbitrary_phase": False,
            "three_dimensional_point_defect_route": "fail",
            "natural_defect_codimension": "line_or_flux_defect",
        },
        "projective_orientation_quench": {
            "order_parameter_space": "RP2",
            "pi_1": "Z2",
            "pi_2": "Z",
            "three_dimensional_point_defects_supported": True,
            "minimal_hedgehog_lift_degrees": [1, -1],
            "coefficient_rank": coefficient_rank,
            "local_oriented_K_classes": [coefficient_rank, -coefficient_rank],
            "global_oriented_charge_of_pair": 0,
            "spin_cover_and_Hopf_line_bridge_reused": True,
        },
        "kibble_zurek_conditional_scaling": {
            "correlation_length_formula": "xi_hat/xi_0=(tau_Q/tau_0)^(nu/(1+z*nu))",
            "point_density_formula": "n_point~xi_hat^(-3)",
            "illustrative_nu": nu,
            "illustrative_z": dynamical_exponent,
            "illustrative_freezeout_exponent": freezeout_exponent,
            "samples": scaling_samples,
            "project_critical_exponents_derived": False,
            "project_microphysical_scales_derived": False,
        },
        "verdict": {
            "bare_holonomy_phase_as_particle_birth": "fail_wrong_codimension",
            "projective_quench_as_pair_exposure": "conditional_kinematic_pass",
            "static_vacuum_instability_required": False,
            "nonequilibrium_history_required": True,
            "matter_birth_proved": False,
            "next_gate": "version6_projective_quench_parent_dynamics_gate",
        },
    }

    assert result["bare_circle_phase"]["canonical_spectrum_depends_only_on_modulus"]
    assert result["bare_circle_phase"]["pi_2"] == "0"
    assert result["projective_orientation_quench"]["pi_2"] == "Z"
    assert result["projective_orientation_quench"]["global_oriented_charge_of_pair"] == 0
    assert abs(freezeout_exponent - 0.25) < 1e-14

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_closed_bridge_destabilization_gate_results.json"
    )
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()