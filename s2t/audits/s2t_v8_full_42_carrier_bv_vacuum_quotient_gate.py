#!/usr/bin/env python3
"""Точный аудит BV/голдстоуновского quotient полного 42-мерного носителя."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_full_42_carrier_bv_vacuum_quotient_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_full_42_carrier_bv_vacuum_quotient import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.physical_chiral_projector.rank() == 42
    assert certificate.physical_fermion_fourth_moment == 92
    assert certificate.gauge_orbit_coordinates.rank() == 3
    assert certificate.orbit_hessian_restriction.rank() == 3
    assert sp.trace(certificate.orbit_hessian_restriction) == 34
    assert certificate.fixed_background_candidate_numerator == sp.Rational(4360268, 3249)
    assert not certificate.orbit_hessian_restriction.atoms(sp.Float)

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"] == "version8_full_42_carrier_bv_vacuum_quotient_gate"
    )
    assert len(gate["obligations"]) == 10
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "fermion_projection": {
            "internal_dimension": 21,
            "spin_dimension": 4,
            "physical_projector_rank": 42,
            "raw_finite_fourth_moment": 46,
            "physical_chiral_fourth_moment": 92,
            "determinant_sign": -1,
        },
        "bv_goldstone_audit": {
            "broken_gauge_orbit_rank": 3,
            "orbit_hessian_rank": 3,
            "orbit_hessian_trace": 34,
            "goldstone_kernel_condition_satisfied": False,
        },
        "ledger": {
            "fixed_background_bosonic_numerator": "4659176/3249",
            "fermion_contribution": -92,
            "algebraic_candidate_before_bv_repair": "4360268/3249",
            "physical_full_B_derived": False,
        },
        "verdict": {
            "fermion_multiplicity_closed": True,
            "previous_scalar_hessian_is_physical_bv_hessian": False,
            "previous_bosonic_ledger_is_physical": False,
            "gauge_invariant_vacuum_hessian_required": True,
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_gauge_invariant_vacuum_hessian_reconstruction_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()