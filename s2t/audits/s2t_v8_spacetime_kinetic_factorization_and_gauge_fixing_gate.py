#!/usr/bin/env python3
"""Точный аудит поперечно-продольной кинетической факторизации."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_spacetime_kinetic_factorization_and_gauge_fixing_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_spacetime_kinetic_factorization_and_gauge_fixing import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.ungauged_hessian.rank() == 36
    assert certificate.gauge_fixed_hessian.rank() == 48
    assert certificate.gauge_fixed_hessian * certificate.gauge_fixed_inverse == sp.eye(48)
    assert not certificate.gauge_fixed_inverse.atoms(sp.Float)
    registry = verify_all()
    gate = next(item for item in registry["gates"] if item["identifier"] == "version8_spacetime_kinetic_factorization_and_gauge_fixing_gate")
    assert len(gate["obligations"]) == 8
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "projectors": {"P_T": "diag(0,1,1,1)", "P_L": "diag(1,0,0,0)", "identities": "P_T^2=P_T, P_L^2=P_L, P_T P_L=0, P_T+P_L=I_4"},
        "ungauged_hessian": {"formula": "K_gauge tensor P_T", "dimension": 48, "rank": 36, "nullity": 12},
        "gauge_fixed_hessian": {"formula": "K_gauge tensor (P_T+xi^-1 P_L)", "rank": 48, "inverse": "K_gauge^-1 tensor (P_T+xi P_L)", "inverse_residual": "0"},
        "gauge_parameter": {"transverse_inverse_independent_of_xi": True, "longitudinal_inverse_depends_on_xi": True, "physical_transverse_factor": "K_gauge^-1 tensor P_T"},
        "physical_boundary": {"internal_inverse_factor_obtained": True, "absolute_mobility_scale_derived": False, "environment_correlation_derived": False},
        "registry": {"gate_count": registry["gate_count"], "obligation_count": registry["obligation_count"], "certificate_sha256": registry["certificate_sha256"][gate["identifier"]]},
        "next_gate": "version8_transverse_noise_mobility_environment_origin_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()