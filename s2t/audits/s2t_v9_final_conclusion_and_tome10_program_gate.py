#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_final_conclusion_tome10_program import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
STEM = "final_conclusion_and_tome10_program_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/s2t_v9_physical_reopening_reference_scale_mu_"
        "parent_origin_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert sum(certificate.conditional) == 6
    assert sum(certificate.physical) == 3
    assert certificate.physical + certificate.deficit == certificate.conditional
    assert certificate.tome10_dependency.rank() == 6
    assert certificate.tome10_dependency.det() == 1

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "tome9_final_status": {
            "conditional_vector": [1, 1, 1, 1, 1, 1],
            "physical_vector": [1, 0, 1, 1, 0, 0],
            "physical_deficit": [0, 1, 0, 0, 1, 1],
            "conditional_score": "6/6",
            "physical_score": "3/6",
            "deficit_rank": 3,
            "physical_reopening_packages": "0/2",
        },
        "tome9_achievements": [
            "common_four_slot_carrier_architecture",
            "endpoint_module_and_creation_qms_architecture",
            "bidirectional_primitive_kms_completion",
            "conditional_invariant_relative_shape_selector",
            "axiom_augmented_common_parent_with_full_hessian",
            "conditional_blind_dimensionless_predictions",
            "exact_physical_origin_no_go_map",
        ],
        "tome10_program": {
            "title": "quantum RG anomaly and physical scale origin",
            "requirements": [
                "quantum_rg_common_carrier",
                "derived_nonzero_beta_function_or_trace_anomaly",
                "rg_invariant_transmutation_scale",
                "typed_embedding_into_kms_gaussian_parent",
                "physical_measure_and_reference_state_origin",
                "scheme_independent_blind_consequence",
            ],
            "dependency_rank": 6,
            "dependency_determinant": 1,
            "specification_score": "6/6",
            "construction_score": "0/6",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "tome9_completed": True,
            "tome9_conditional_model_closed": True,
            "tome9_physical_four_slot_parent_derived": False,
            "tome9_physical_status_frozen": True,
            "tome10_program_admitted": True,
            "tome10_physical_theory_constructed": False,
        },
        "next_gate": "version10_quantum_rg_common_carrier_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()