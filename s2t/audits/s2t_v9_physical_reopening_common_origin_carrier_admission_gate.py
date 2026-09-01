#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_physical_reopening_common_origin_carrier import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
STEM = "physical_reopening_common_origin_carrier_admission_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/s2t_v9_axiom_augmented_physical_origin_"
        "reopening_criterion_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.common_operator.shape == (10, 10)
    assert certificate.common_hessian.rank() == 6
    assert certificate.common_hessian.det() == 36
    assert certificate.scale_orbit_map.rank() == 1
    assert len(certificate.scale_orbit_map.nullspace()) == 1

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "common_carrier": {
            "kind": "ten_dimensional_positive_gaussian_covariance",
            "dimension": 10,
            "operator": "diag(e R_theta, e chi^2 R_kappa)",
            "trace": "5 e (1+chi^2)",
            "determinant": "e^10 chi^10 det(R_theta) det(R_kappa)",
        },
        "spectral_entropy_parent": {
            "functional": "Tr(Q)-log(det(Q))-10",
            "gaussian_relative_entropy_factor": 2,
            "stationary_point": [1, 1, 0, 0, 0, 0],
            "hessian_rank": 6,
            "hessian_determinant": 36,
            "hessian_spectrum": ["15-5*sqrt(5)", "15+5*sqrt(5)", "1", "1", "3/5", "3/5"],
        },
        "scale_boundary": {
            "dimensionless_scale": "e=E_*/mu",
            "common_rescaling": "(E_*,mu)->(s E_*,s mu)",
            "orbit_rank": 1,
            "orbit_nullity": 1,
            "absolute_reference_scale_derived": False,
        },
        "scores": {
            "common_carrier_architecture": "1/1",
            "conditional_joint_selection": "2/2",
            "physical_origin_packages": "0/2",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "common_origin_carrier_admitted": True,
            "bounded_conditional_parent_constructed": True,
            "existing_physical_carrier_origin_derived": False,
            "absolute_physical_scale_derived": False,
            "physical_program_reopened": False,
        },
        "next_gate": "version9_physical_reopening_gaussian_reference_state_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()