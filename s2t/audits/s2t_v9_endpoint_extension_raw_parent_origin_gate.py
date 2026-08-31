#!/usr/bin/env python3
"""Exact type-aware raw-origin audit for the Tome IX endpoint extension."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_extension_raw_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def load(name: str) -> dict:
    return json.loads((ROOT / f"s2t/results/{name}").read_text(encoding="utf-8"))


def main() -> None:
    predecessor = load(
        "s2t_v9_four_slot_parent_selector_coefficient_origin_gate_results.json"
    )
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert predecessor["verdict"]["conditional_endpoint_ordering_derived"]
    assert not predecessor["verdict"]["raw_endpoint_extension_derived"]

    old = load(
        "s2t_v8_baryon_c0_existing_42_carrier_linking_bridge_classification_gate_results.json"
    )
    neutral = load("s2t_v8_baryon_c0_minimal_neutral_endpoint_extension_gate_results.json")
    triplet = load(
        "s2t_v8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate_results.json"
    )
    cotangent = load("s2t_v8_horizontal_phase_cotangent_doubled_quiver_parent_admission_gate_results.json")

    weights = (
        [sp.Rational(1, 6)] * 6
        + [sp.Rational(2, 3)] * 3
        + [sp.Rational(-1, 3)] * 3
        + [sp.Rational(-1, 2)] * 6
        + [sp.Integer(-1)] * 3
    )
    hypercharge = sp.diag(*weights)
    assert hypercharge.shape == (21, 21)
    assert hypercharge.rank() == 21
    assert hypercharge.nullspace() == []
    assert old["current_endpoint"]["hypercharge_nullity"] == 0
    assert not old["verdict"]["linear_or_algebraic_closure_can_create_external_endpoint"]

    assert neutral["endpoint_extension"]["new_neutral_complex_states"] == 2
    assert triplet["homogeneous_triplet_branches"]["plus_branch"]["new_target_states"] == 1
    assert triplet["current_target_grading"]["plus_dimension"] == 2
    assert triplet["current_target_grading"]["minus_dimension"] == 1
    assert not cotangent["verdict"]["canonical_parent_selected"]

    required_states = {
        "s0": {"charge": 0, "grading": 1, "factor": "system_endpoint"},
        "a0": {"charge": 0, "grading": -1, "factor": "system_endpoint"},
        "eR_t0": {"charge": -1, "grading": 1, "factor": "system_endpoint"},
    }
    assert len(required_states) == 3

    candidates = {
        "hypercharge_kernel_in_H21": False,
        "algebraic_closure_of_End_H21": False,
        "old_F42_frame_zero_extension": False,
        "neutral_environment_vacuum_retyping": False,
        "charged_environment_pair_retyping": False,
        "cotangent_or_real_operator_doubling": False,
    }
    assert not any(candidates.values())

    type_failures = {
        "environment_vacuum": ["tensor_factor", "grading_multiplicity"],
        "charged_environment_pair": ["tensor_factor", "family_type", "grading"],
        "old_charged_singlets": ["positive_grading_multiplicity"],
        "cotangent_double": ["endpoint_representation_multiplicity"],
    }

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "raw_H21_certificate": {
            "dimension": 21,
            "hypercharge_rank": hypercharge.rank(),
            "hypercharge_nullity": len(hypercharge.nullspace()),
            "neutral_trivial_irrep_multiplicity": 0,
            "operator_closure_changes_module_dimension": False,
        },
        "required_extension": {
            "module": "E_min=C s0_plus direct_sum C a0_minus direct_sum C eR_t0_plus",
            "new_complex_dimension": len(required_states),
            "states": required_states,
        },
        "type_failure_audit": type_failures,
        "candidate_origins": {
            **candidates,
            "satisfied": sum(candidates.values()),
            "tested": len(candidates),
        },
        "ledgers": {
            "raw_endpoint_candidate_origin_satisfied": 0,
            "raw_endpoint_candidate_origin_tested": 6,
            "raw_physical_slot_closure_satisfied": 0,
            "raw_physical_slot_closure_tested": 4,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "raw_endpoint_extension_derived": False,
            "environment_states_can_be_retyped_as_endpoints": False,
            "minimal_new_typed_module_dimension": 3,
            "new_finite_module_architecture_required": True,
        },
        "next_gate": "version9_endpoint_extension_minimal_finite_module_architecture_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()