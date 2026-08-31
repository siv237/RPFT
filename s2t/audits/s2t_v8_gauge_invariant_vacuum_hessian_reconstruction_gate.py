#!/usr/bin/env python3
"""Точный аудит горизонтальной реконструкции вакуумного гессиана."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_gauge_invariant_vacuum_hessian_reconstruction_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_gauge_invariant_vacuum_hessian_reconstruction import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.orbit_metric == 14 * sp.eye(3)
    assert certificate.orbit_projector.rank() == 3
    assert certificate.horizontal_projector.rank() == 27
    assert certificate.quotient_hessian.rank() == 26
    assert len(certificate.quotient_hessian.nullspace()) == 4
    assert certificate.scalar_fourth_moment == sp.Rational(1118917, 882)
    assert certificate.bosonic_fourth_moment == sp.Rational(226371884, 159201)
    assert certificate.full_quadratic_numerator == sp.Rational(211725392, 159201)
    assert not certificate.quotient_hessian.atoms(sp.Float)

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"] == "version8_gauge_invariant_vacuum_hessian_reconstruction_gate"
    )
    assert len(gate["obligations"]) == 12
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "horizontal_quotient": {
            "orbit_dimension": 3,
            "orbit_metric": "14 I_3",
            "horizontal_dimension": 27,
            "quotient_hessian_rank": 26,
            "quotient_hessian_nullity": 4,
            "goldstone_zero_modes": 3,
            "horizontal_flat_modes": 1,
        },
        "fourth_moments": {
            "scalar_quotient": "1118917/882",
            "gauge": "36897/722",
            "bosonic_bv": "226371884/159201",
            "fermionic": -92,
            "full_quadratic_numerator": "211725392/159201",
        },
        "verdict": {
            "goldstone_kernel_repaired": True,
            "quadratic_bv_ledger_derived": True,
            "unique_horizontal_flat_direction_present": True,
            "nonlinear_gauge_invariant_parent_derived": False,
            "unconditional_physical_B_derived": False,
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_horizontal_flat_direction_parent_lift_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()