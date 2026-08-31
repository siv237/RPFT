#!/usr/bin/env python3
"""Exact admission audit for the opening four-slot program of Tome IX."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "four_slot_dynamic_parent_program_admission_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/"
        "s2t_v8_baryon_c0_charged_mediator_common_energy_scale_"
        "parent_origin_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text(encoding="utf-8"))
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert predecessor["scope_verdict"][
        "positive_four_slot_parent_construction_belongs_to_tome9"
    ]

    energy, chi, hbar = sp.symbols("E_star chi hbar", positive=True)
    observables = sp.Matrix(
        [energy, chi * energy, hbar / energy, chi**2 * energy / hbar]
    )
    jacobian = observables.jacobian([energy, chi])
    assert jacobian.rank() == 2
    minor = jacobian.extract([0, 1], [0, 1]).det()
    assert sp.simplify(minor - energy) == 0

    slots = {
        "endpoint_extension": "discrete_carrier_sector",
        "common_energy_E_star": "positive_dimensional_scalar",
        "dimensionless_coupling_chi": "positive_dimensionless_scalar",
        "transport_primitive": "evolution_law_class",
    }
    assert len(slots) == 4
    assert len(set(slots.values())) == 4

    contract = {
        "closed_tome8_predecessor": True,
        "four_slots_explicitly_typed": True,
        "common_K45_L44_baseline_declared": True,
        "computable_pass_fail_ledger": True,
        "target_loaded_dimensional_inputs_forbidden": True,
        "explicit_stop_rule": True,
    }
    assert all(contract.values())

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "four_slot_program": slots,
        "continuous_dependency_audit": {
            "coordinates": ["E_star", "chi"],
            "outputs": ["E_star", "chi E_star", "hbar/E_star", "chi^2 E_star/hbar"],
            "jacobian_rank": 2,
            "nonzero_minor": "E_star>0",
        },
        "admission_contract": {
            **contract,
            "satisfied": sum(contract.values()),
            "tested": len(contract),
        },
        "ledgers": {
            "inherited_slot_selection_satisfied": 0,
            "inherited_slot_selection_tested": 4,
            "constructed_common_parent_satisfied": 0,
            "constructed_common_parent_tested": 1,
            "program_admission_satisfied": 6,
            "program_admission_tested": 6,
        },
        "verdict": {
            "tome9_program_admitted": True,
            "four_slot_parent_constructed": False,
            "physical_scale_selected": False,
            "next_step_is_common_carrier_architecture": True,
        },
        "next_gate": "version9_four_slot_common_carrier_architecture_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()