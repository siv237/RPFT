#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_physical_origin_reopening_criterion import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
STEM = "axiom_augmented_physical_origin_reopening_criterion_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_axiom_augmented_"
        "conditional_program_status_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.package_map.rank() == 2
    assert certificate.package_map * certificate.conditional_packages == certificate.deficit
    assert certificate.package_map * certificate.physical_packages == sp.zeros(3, 1)

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "open_physical_criteria": [
            "physical_scale_and_coupling_selection",
            "physical_hessian",
            "unconditional_blind_dimensionless_consequence",
        ],
        "deficit_vector": [1, 1, 1],
        "reopening_packages": [
            "physical_scale_and_coupling_origin",
            "physical_logdet_parent_origin",
        ],
        "package_map": [[1, 0], [0, 1], [0, 1]],
        "package_rank": 2,
        "conditional_package_availability": [1, 1],
        "physical_package_availability": [0, 0],
        "scores": {
            "conditional_deficit_coverage": "3/3",
            "physical_deficit_coverage": "0/3",
            "physical_reopening_packages": "0/2",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "minimal_reopening_criterion_established": True,
            "two_independent_physical_origin_packages_required": True,
            "physical_program_reopened": False,
            "tome9_status_freeze_remains": True,
        },
        "next_gate": "version9_physical_reopening_common_origin_carrier_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()