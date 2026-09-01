#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_gaussian_reference_state_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
STEM = "physical_reopening_gaussian_reference_state_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/s2t_v9_physical_reopening_common_origin_"
        "carrier_admission_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.lyapunov_map.rank() == 55
    assert len(certificate.lyapunov_map.nullspace()) == 0
    assert certificate.ratio_orbit_map.rank() == 1
    assert len(certificate.ratio_orbit_map.nullspace()) == 1

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "ou_architecture": {
            "coordinate_dimension": 10,
            "symmetric_covariance_dimension": 55,
            "drift": "B=gamma I_10",
            "diffusion": "D=delta I_10",
            "stationary_covariance": "S=(delta/gamma) I_10",
            "lyapunov_equation": "B S + S B^T = 2 D",
            "lyapunov_rank": 55,
            "lyapunov_nullity": 0,
            "reversible": True,
        },
        "nonuniqueness_witnesses": [
            {"gamma": 1, "delta": 1, "covariance": "I_10"},
            {"gamma": 1, "delta": 2, "covariance": "2 I_10"},
        ],
        "coefficient_boundary": {
            "free_ratio": "delta/gamma",
            "common_rescaling": "(gamma,delta)->(s gamma,s delta)",
            "orbit_rank": 1,
            "orbit_nullity": 1,
            "unit_covariance_ratio_derived": False,
        },
        "scores": {
            "gaussian_stationary_architecture": "1/1",
            "conditional_unit_reference_state": "1/1",
            "physical_reference_state_origin": "0/1",
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
            "unique_covariance_for_fixed_ou_coefficients": True,
            "unit_reference_covariance_selected_by_structure": False,
            "gaussian_reference_state_parent_origin_derived": False,
            "physical_program_reopened": False,
        },
        "next_gate": "version9_physical_reopening_reference_scale_mu_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()