#!/usr/bin/env python3
"""Точный аудит determinant-line допуска горизонтальной фазы."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_horizontal_phase_determinant_line_admission_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_horizontal_phase_determinant_line_admission import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    expected = sp.Matrix([0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0])
    assert certificate.cofactor_vector == expected
    assert certificate.source_determinant_charge == -2
    assert certificate.target_determinant_charge == -2
    assert certificate.relative_determinant_charge == 0
    assert certificate.invariant_functional_dimension == 0
    assert not certificate.cofactor_vector.atoms(sp.Float)

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"] == "version8_horizontal_phase_determinant_line_admission_gate"
    )
    assert len(gate["obligations"]) == 12
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "cofactor_line": {
            "primitive_vector": [0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0],
            "norm_squared": 2,
            "horizontal_phase_weight": 33,
            "source_determinant_hypercharge": -2,
            "target_determinant_hypercharge": -2,
            "relative_determinant_hypercharge": 0,
        },
        "scalar_trivialization": {
            "invariant_linear_functional_dimension": 0,
            "real_pair_retains_phase": False,
            "distinct_vacuum_normalized_contractions": 2,
            "canonical_contraction_derived": False,
        },
        "verdict": {
            "phase_sensitive_cofactor_exists": True,
            "canonical_gauge_invariant_scalar_exists": False,
            "determinant_line_lifts_horizontal_mode": False,
            "manual_vacuum_kernel_contraction_admitted": False,
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_horizontal_phase_heavy_arrow_cycle_admission_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()