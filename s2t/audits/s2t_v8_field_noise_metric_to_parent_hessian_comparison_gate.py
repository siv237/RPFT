#!/usr/bin/env python3
"""Точное сравнение следовой метрики с постояннополевым гессианом."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_field_noise_metric_to_parent_hessian_comparison_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_field_noise_metric_to_parent_hessian_comparison import (  # noqa: E402
    build_certificate,
)
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    parent = certificate.constant_field_parent_hessian
    metric = certificate.trace_metric
    gauge_metric = metric[30:, 30:]
    assert parent.rank() == 30
    assert metric.rank() == 42
    assert parent[30:, 30:] == sp.zeros(12)
    assert gauge_metric.rank() == 12
    assert not parent.atoms(sp.Float)
    assert not metric.atoms(sp.Float)

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"]
        == "version8_field_noise_metric_to_parent_hessian_comparison_gate"
    )
    assert len(gate["obligations"]) == 8

    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "trace_metric": {
            "rank": int(metric.rank()),
            "gauge_block_rank": int(gauge_metric.rank()),
            "gauge_block_trace": str(sp.trace(gauge_metric)),
            "interpretation": "finite internal coefficient metric",
        },
        "constant_field_parent_hessian": {
            "transfer_block_rank": int(
                certificate.transfer_origin_hessian.rank()
            ),
            "gauge_block": "0_12",
            "gauge_zero_modes": 12,
            "full_rank": int(parent.rank()),
            "origin": "F_B=dB+B wedge B; for dB=0 the action starts at degree four in B",
        },
        "comparison": {
            "rank_pair": [int(parent.rank()), int(metric.rank())],
            "exists_nonzero_scalar_c_with_H_equal_cK": False,
            "exists_any_scalar_c_with_H_equal_cK": False,
            "reason": "the gauge restriction forces c=0 while the transfer Hessian has rank 30",
        },
        "spacetime_boundary": {
            "nonzero_momentum_gauge_hessian": "K_gauge tensor (p^2 g^{mu nu}-p^mu p^nu)",
            "requires_spacetime_index": True,
            "requires_gauge_fixing_for_inverse": True,
            "reduces_canonically_to_internal_K": False,
        },
        "verdict": {
            "kinematic_trace_metric_equals_constant_parent_hessian": False,
            "physical_mobility_derived": False,
            "failure_type": "rank_and_type_mismatch",
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_spacetime_kinetic_factorization_and_gauge_fixing_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()