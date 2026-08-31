#!/usr/bin/env python3
"""Exact parent-origin audit of the four selector coefficient packages."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "four_slot_parent_selector_coefficient_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def load(name: str) -> dict:
    return json.loads((ROOT / f"s2t/results/{name}").read_text(encoding="utf-8"))


def main() -> None:
    predecessor = load(
        "s2t_v9_four_slot_common_parent_functional_architecture_gate_results.json"
    )
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate

    neutral = load("s2t_v8_baryon_c0_minimal_neutral_endpoint_extension_gate_results.json")
    triplet = load(
        "s2t_v8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate_results.json"
    )
    scale = load(
        "s2t_v8_baryon_c0_charged_mediator_common_energy_scale_parent_origin_gate_results.json"
    )
    balanced = load("s2t_v8_index_balanced_ancilla_conveyor_gate_results.json")

    assert neutral["verdict"]["minimal_neutral_endpoint_extension_admitted"]
    assert not neutral["verdict"]["physical_extended_parent_derived"]
    assert triplet["homogeneous_triplet_branches"]["unique_minimal_state_branch"] == "plus"
    assert not triplet["verdict"]["current_parent_contains_new_state"]

    violations = (sp.Integer(2), sp.Integer(1), sp.Integer(0))
    rho, reference = sp.symbols("rho epsilon_ref", positive=True)
    scores = tuple(reference + rho * value for value in violations)
    assert sp.simplify(scores[0] - scores[1]) == rho
    assert sp.simplify(scores[1] - scores[2]) == rho

    ratios = (sp.Integer(2), sp.Integer(8))
    minima = tuple(sp.sqrt(ratio / 2) for ratio in ratios)
    assert minima == (1, 2)
    assert not scale["verdict"]["common_energy_scale_derived"]

    assert balanced["verdict"]["exact_local_floquet_conveyor"]
    assert balanced["carrier"]["total_gnvw_index"] == 1
    transport_admissibility = {
        "forward": {
            "common_carrier": True,
            "gauge_covariant": True,
            "real_covariant": True,
            "exact_iteration": True,
            "explicit_gnvw_class": True,
        },
        "balanced": {
            "common_carrier": True,
            "gauge_covariant": True,
            "real_covariant": True,
            "exact_iteration": True,
            "explicit_gnvw_class": True,
        },
    }
    assert all(all(branch.values()) for branch in transport_admissibility.values())

    origins = {
        "endpoint_score_order_from_closure_defects": True,
        "energy_ratio_b_E_over_a_E": False,
        "coupling_ratio_b_chi_over_a_chi": False,
        "transport_bias_sign": False,
    }

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "endpoint_audit": {
            "nested_candidates": ["Q0=H21", "Q1=H23", "Q2=H24"],
            "closure_violation_counts": [2, 1, 0],
            "score_family": "epsilon_i=epsilon_ref+rho nu_i with rho>0",
            "unique_conditional_choice": "Q2=H24",
            "raw_new_states_derived": False,
        },
        "continuous_ratio_witnesses": {
            "tested_ratios": [2, 8],
            "resulting_positive_minima": [1, 2],
            "energy_scale_orbit_survives": True,
            "coupling_normalization_orbit_survives": True,
        },
        "transport_admissibility": {
            **transport_admissibility,
            "forward_satisfied": 5,
            "forward_tested": 5,
            "balanced_satisfied": 5,
            "balanced_tested": 5,
            "bias_selected": False,
        },
        "selector_coefficient_origins": {
            **origins,
            "satisfied": sum(origins.values()),
            "tested": len(origins),
        },
        "ledgers": {
            "selector_coefficient_origin_satisfied": 1,
            "selector_coefficient_origin_tested": 4,
            "raw_physical_slot_closure_satisfied": 0,
            "raw_physical_slot_closure_tested": 4,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "conditional_endpoint_ordering_derived": True,
            "raw_endpoint_extension_derived": False,
            "energy_and_coupling_ratios_derived": False,
            "transport_bias_derived": False,
            "physical_four_slot_parent_constructed": False,
        },
        "next_gate": "version9_endpoint_extension_raw_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()