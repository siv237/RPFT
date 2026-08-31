#!/usr/bin/env python3
"""Аудит селектора совместимой комплексной структуры и метрики."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_horizontal_phase_cotangent_complex_structure_metric_selector_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_horizontal_phase_cotangent_complex_structure_metric_selector import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.full_real_dimension == 52
    assert certificate.pulled_trace_metric.rank() == 42
    assert len(certificate.pulled_trace_metric.nullspace()) == 10
    assert certificate.pulled_transfer_metric.rank() == 30
    assert len(certificate.pulled_transfer_metric.nullspace()) == 22
    assert certificate.first_complex_structure**2 == -sp.eye(52)
    assert certificate.second_complex_structure**2 == -sp.eye(52)
    assert certificate.first_metric_extension != certificate.second_metric_extension
    assert not certificate.second_metric_extension.atoms(sp.Float)

    registry = verify_all()
    gate = next(item for item in registry["gates"] if item["identifier"] == "version8_horizontal_phase_cotangent_complex_structure_metric_selector_gate")
    assert len(gate["obligations"]) == 12
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "carrier_mismatch": {
            "symplectic_real_dimension": 52,
            "full_trace_metric_dimension": 42,
            "full_trace_pullback_rank": 42,
            "full_trace_nullity": 10,
            "transfer_trace_metric_dimension": 30,
            "transfer_trace_nullity": 22,
        },
        "compatible_extensions": {
            "two_exact_distinct_witnesses": True,
            "both_preserve_old_normalized_trace_metric": True,
            "both_satisfy_J_squared_minus_identity": True,
            "both_satisfy_g_equals_Omega_J": True,
            "continuous_scale_remains_on_five_missing_symplectic_pairs": True,
        },
        "verdict": {
            "existing_trace_metric_selects_full_positive_metric": False,
            "existing_trace_metric_selects_unique_complex_structure": False,
            "symplectic_form_alone_selects_positive_metric": False,
            "horizontal_phase_lifted": False,
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_horizontal_phase_missing_trace_metric_completion_origin_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()