#!/usr/bin/env python3
"""Exact audit of the minimal new data for the charged dynamic parent."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "baryon_c0_charged_mediator_dynamic_parent_minimal_new_data_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v8_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_charged_mediator_dynamic_parent_data_admission_gate_results.json").read_text(encoding="utf-8"))
    gate = f"version8_{STEM}"
    assert predecessor["next_gate"] == gate

    energy, chi, hbar = sp.symbols("E_star chi hbar", positive=True)
    gamma = energy / 7
    clock_energy = energy
    coupling_energy = chi * energy
    tick = hbar / energy
    rate = chi**2 * energy / hbar
    outputs = sp.Matrix([gamma, clock_energy, coupling_energy, tick, rate])
    jacobian = outputs.jacobian([energy, chi])
    assert jacobian.rank() == 2

    coordinate_minor = sp.Matrix([clock_energy, coupling_energy]).jacobian([energy, chi])
    assert sp.simplify(coordinate_minor.det()) == energy

    assert sp.simplify(clock_energy * tick - hbar) == 0
    assert sp.simplify(rate * tick - chi**2) == 0
    assert sp.simplify(coupling_energy**2 * tick / hbar**2 - rate) == 0
    assert sp.simplify(7 * gamma - clock_energy) == 0

    witness_scale_1 = outputs.subs({energy: 1, chi: 1, hbar: 1})
    witness_scale_2 = outputs.subs({energy: 2, chi: 1, hbar: 1})
    witness_coupling_2 = outputs.subs({energy: 1, chi: 2, hbar: 1})
    assert witness_scale_1 != witness_scale_2
    assert witness_scale_1 != witness_coupling_2
    assert witness_scale_2[-1] / witness_scale_1[-1] == 2
    assert witness_coupling_2[-1] / witness_scale_1[-1] == 4

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "typed_identification": {
            "common_resonant_quantum": "E_star=E_C=7 gamma",
            "dimensionless_coupling": "chi=g/E_star",
            "derived_gamma": "gamma=E_star/7",
            "derived_coupling_energy": "g=chi E_star",
            "derived_tick": "tau_C=hbar/E_star",
            "derived_rate": "Gamma=chi^2 E_star/hbar",
            "relative_rate": "Gamma tau_C=chi^2",
        },
        "independence_audit": {
            "continuous_input_coordinates": ["E_star", "chi"],
            "derived_output_coordinates": ["gamma", "E_C", "g", "tau_C", "Gamma"],
            "jacobian_rank": jacobian.rank(),
            "nonzero_coordinate_minor": "det d(E_C,g)/d(E_star,chi)=E_star",
            "continuous_parameter_count_is_minimal": True,
        },
        "exact_witnesses": {
            "base": [str(x) for x in witness_scale_1],
            "double_energy": [str(x) for x in witness_scale_2],
            "double_chi": [str(x) for x in witness_coupling_2],
            "double_energy_rate_ratio": 2,
            "double_chi_rate_ratio": 4,
        },
        "minimal_new_data": {
            "discrete_or_structural": [
                "conditional endpoint/carrier extension",
                "choice of transport primitive",
            ],
            "continuous": ["one positive common energy E_star", "one positive dimensionless coupling chi"],
            "total_independent_slots": 4,
            "previous_apparent_slots": 5,
            "reduction": 1,
            "vacuum_is_derived_once_positive_local_parent_is_given": True,
        },
        "ledgers": {
            "dependency_reduction_satisfied": 7,
            "dependency_reduction_tested": 7,
            "minimal_data_classification_satisfied": 4,
            "minimal_data_classification_tested": 4,
            "inherited_selection_satisfied": 0,
            "inherited_selection_tested": 4,
        },
        "verdict": {
            "five_apparent_inputs_are_independent": False,
            "minimal_continuous_parameter_count": 2,
            "minimal_total_new_data_slots": 4,
            "common_energy_and_coupling_are_selected": False,
            "full_dynamic_parent_derived": False,
        },
        "next_gate": "version8_baryon_c0_charged_mediator_common_energy_scale_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()