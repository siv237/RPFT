#!/usr/bin/env python3
"""Точный аудит полево-шумового отображения и переноса метрики."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_field_to_noise_chain_map_pullback_metric_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_field_to_noise_chain_map_pullback_metric import (  # noqa: E402
    build_certificate,
)
from s2t.proofdsl.examples.version8_full_noise_trace_frame import (  # noqa: E402
    build_certificate as build_trace_frame_certificate,
)
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    trace_frame = build_trace_frame_certificate()
    assert certificate.map_matrix == sp.eye(42)
    assert certificate.pullback_metric == trace_frame.trace_metric
    assert certificate.pullback_dual == trace_frame.dual_rate_metric
    assert certificate.pullback_metric * certificate.pullback_dual == sp.eye(42)
    assert certificate.gauge_action_count == 12
    assert certificate.intertwining_check_count == 504
    assert not certificate.pullback_metric.atoms(sp.Float)
    assert not certificate.pullback_dual.atoms(sp.Float)

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"]
        == "version8_field_to_noise_chain_map_pullback_metric_gate"
    )
    assert len(gate["obligations"]) == 8

    metric = certificate.pullback_metric
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "map": {
            "formula": "J(delta A,delta B_s,delta B_t)=[[delta B_s,delta A^*],[delta A,delta B_t]]",
            "coordinate_matrix": "I_42",
            "rank": 42,
            "kernel_dimension": 0,
            "gauge_generators": certificate.gauge_action_count,
            "exact_intertwining_checks": certificate.intertwining_check_count,
            "intertwining_defects": 0,
        },
        "metric": {
            "pullback_identity": "G_field=J^* K J=K",
            "rank": int(metric.rank()),
            "off_diagonal_nonzero_entries": sum(
                1
                for row in range(42)
                for column in range(42)
                if row != column and metric[row, column] != 0
            ),
            "diagonal_entries": [str(entry) for entry in metric.diagonal()],
            "inverse_identity": "R_field=G_field^-1=K^-1",
            "inverse_residual": "0",
        },
        "normalization_boundary": {
            "equivariant_family": "S=diag(s_transfer I_30,s_gauge I_12)",
            "pulled_metric": "S^* K S=diag(s_transfer^2 K_transfer,s_gauge^2 K_gauge)",
            "gauge_covariance_alone_selects_relative_scale": False,
            "literal_superconnection_embedding_selects_unit_coordinates": True,
        },
        "physical_boundary": {
            "kinematic_field_noise_isomorphism_obtained": True,
            "parent_hessian_derived_from_trace_map": False,
            "physical_mobility_derived_without_riesz_principle": False,
            "absolute_time_derived": False,
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "version8_field_noise_metric_to_parent_hessian_comparison_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()