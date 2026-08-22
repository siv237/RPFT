#!/usr/bin/env python3
"""Audit the minimal energy-conserving qutrit/four-tick cooling model."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def maximum_ground_population(clock_probabilities: np.ndarray) -> float:
    """Ky Fan maximum over additive-energy blocks for Hs=(0,1,1), Hc=(0,1,2,3)."""
    p = clock_probabilities
    return float(
        (
            p[0]
            + max(p[1], p[0])
            + max(p[2], p[1])
            + max(p[3], p[2])
        )
        / 3.0
    )


def random_simplex(rng: np.random.Generator, count: int) -> np.ndarray:
    samples = rng.exponential(size=(count, 4))
    return samples / np.sum(samples, axis=1, keepdims=True)


def main() -> None:
    coexistence_axis = 0.9121665962741361
    coexistence_beta = 1.5426695408602848
    transverse = 0.5 * (1.0 - coexistence_axis)

    effective_gap = float(
        np.log(2.0 * coexistence_axis / (1.0 - coexistence_axis))
        / coexistence_beta
    )
    resonant_tick_duration = float(np.pi / (2.0 * effective_gap))

    vertices = np.eye(4)
    vertex_bounds = np.array([maximum_ground_population(vertex) for vertex in vertices])
    rng = np.random.default_rng(20260819)
    samples = random_simplex(rng, 100000)
    sampled_bounds = np.array(
        [maximum_ground_population(sample) for sample in samples]
    )
    exact_bound = 2.0 / 3.0

    result = {
        "gate": "version6_clock_controlled_energy_conserving_quench_gate",
        "minimal_resonant_model": {
            "system_hamiltonian": "epsilon diag(0,1,1)",
            "clock_hamiltonian": "epsilon diag(0,1,2,3)",
            "system_transverse_degeneracy": 2,
            "clock_gap_degeneracy": 1,
            "initial_system_state": "I3/3",
            "allowed_unitaries": "[W,Hs+Hc]=0",
        },
        "target_phase": {
            "coexistence_axis_weight": coexistence_axis,
            "coexistence_transverse_weight": transverse,
            "gibbs_gap_in_effective_energy_units": effective_gap,
            "resonant_four_tick_duration_if_gap_is_tuned": resonant_tick_duration,
        },
        "energy_block_bound": {
            "formula": "[p0+max(p1,p0)+max(p2,p1)+max(p3,p2)]/3",
            "vertex_values": vertex_bounds.tolist(),
            "exact_maximum_axis_weight": exact_bound,
            "sampled_maximum_axis_weight": float(np.max(sampled_bounds)),
            "target_exceeds_bound": coexistence_axis > exact_bound,
            "axis_weight_deficit": coexistence_axis - exact_bound,
        },
        "degeneracy_obstruction": {
            "initial_orthogonal_excited_components": 2,
            "ground_clock_states_at_one_resonant_gap": 1,
            "minimum_required_gap_degeneracy_for_full_transfer": 2,
            "order_four_character_eigenvalues": ["1", "i", "-1", "-i"],
            "order_four_quasienergies_nondegenerate_mod_period": True,
            "canonical_four_character_clock_supplies_required_degeneracy": False,
        },
        "resource_options": {
            "add_second_resonant_clock_channel": True,
            "use_existing_multiplicity_as_energy_degeneracy": "not yet attributed",
            "break_transverse_doublet": "forbidden if RP2 orbit is to remain exact",
            "use_initial_system_clock_correlations": "possible but new resource",
            "allow_nonadditive_interaction_energy": "possible but must be parent-derived",
        },
        "maximum_residuals": {
            "sampled_bound_violation": float(
                max(0.0, np.max(sampled_bounds) - exact_bound)
            ),
            "vertex_bound_residual": float(
                abs(np.max(vertex_bounds) - exact_bound)
            ),
            "target_normalization": float(
                abs(coexistence_axis + 2.0 * transverse - 1.0)
            ),
        },
        "verdict": {
            "minimal_non_degenerate_four_tick_clock_reaches_target": False,
            "energy_conserving_axis_ceiling": exact_bound,
            "entropy_capacity_alone_was_sufficient_but_not_energy_degeneracy": True,
            "canonical_order_four_clock_is_autonomous_refrigerator": False,
            "existing_project_multiplicity_may_reopen_gate": True,
            "matter_birth_fully_derived": False,
            "next_gate": "version6_existing_multiplicity_resonant_sink_gate",
        },
    }

    assert np.max(vertex_bounds) == exact_bound
    assert np.max(sampled_bounds) <= exact_bound + 1e-12
    assert coexistence_axis > exact_bound
    assert all(value < 1e-12 for value in result["maximum_residuals"].values())

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_clock_controlled_energy_conserving_quench_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()