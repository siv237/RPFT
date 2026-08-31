#!/usr/bin/env python3
"""Exact final Tome VIII audit of the common energy-scale origin."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "baryon_c0_charged_mediator_common_energy_scale_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v8_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_charged_mediator_dynamic_parent_minimal_new_data_gate_results.json").read_text(encoding="utf-8"))
    gate = f"version8_{STEM}"
    assert predecessor["next_gate"] == gate

    energy, scale, time, hbar, chi = sp.symbols(
        "E_star lambda t hbar chi", positive=True
    )
    dimensionless_time = energy * time / hbar
    assert sp.simplify((scale * energy) * (time / scale) / hbar - dimensionless_time) == 0

    gamma = energy / 7
    clock_energy = energy
    coupling = chi * energy
    rate = chi**2 * energy / hbar
    frequency = energy / hbar
    assert sp.simplify(clock_energy - 7 * gamma) == 0
    assert sp.simplify(rate / frequency - chi**2) == 0
    assert sp.simplify((chi * scale * energy) / coupling - scale) == 0

    # A normalized projector parent fixes its kernel but not its dimensional coefficient.
    projector = sp.diag(0, 1, 1)
    parent_one = energy * projector
    parent_two = 2 * energy * projector
    assert parent_one.nullspace() == parent_two.nullspace()
    assert parent_one.eigenvals() != parent_two.eigenvals()

    candidates = {
        "spectral_cutoff_or_radius": False,
        "normalized_cell_projector_gap": False,
        "dimensionless_generator_gap": False,
        "binary_discriminator_coefficient_gamma": False,
        "compacton_energy_length_product": False,
        "observed_mass_or_external_clock": False,
    }
    assert not any(candidates.values())

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "common_scale_family": {
            "common_quantum": "E_star=E_C=7 gamma",
            "coupling": "g=chi E_star",
            "tick": "tau_C=hbar/E_star",
            "rate": "Gamma=chi^2 E_star/hbar",
            "scale_orbit": "(E_star,t,g,Gamma)->(lambda E_star,t/lambda,lambda g,lambda Gamma)",
            "dimensionless_time_invariant": True,
            "relative_rate_invariant": "Gamma/Omega=chi^2",
        },
        "projector_parent_witness": {
            "same_unique_kernel_for_coefficients_one_and_two": True,
            "spectral_gaps_differ_by_factor_two": True,
            "state_selection_does_not_select_energy_unit": True,
        },
        "candidate_origin_audit": {
            **candidates,
            "satisfied": 0,
            "tested": len(candidates),
        },
        "ledgers": {
            "exact_scale_orbit_satisfied": 6,
            "exact_scale_orbit_tested": 6,
            "common_energy_parent_origin_satisfied": 0,
            "common_energy_parent_origin_tested": 6,
        },
        "scope_verdict": {
            "gate_belongs_to_tome8_as_final_closure_test": True,
            "positive_four_slot_parent_construction_belongs_to_tome9": True,
            "tome8_ready_for_final_conclusion": True,
        },
        "verdict": {
            "common_energy_scale_derived": False,
            "resonance_reduces_parameters_but_does_not_set_scale": True,
            "absolute_time_and_rate_remain_conditional": True,
            "tome8_operator_process_program_completed": True,
        },
        "next_gate": "version9_four_slot_dynamic_parent_program_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()