#!/usr/bin/env python3
"""LCF audit of the parent-action origin of the metric-dual environment."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "s2t/results/"
    "s2t_v8_metric_dual_environment_parent_action_origin_gate_results.json"
)
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_metric_dual_environment_parent_action import (  # noqa: E402
    build_certificate,
)
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    theorem = certificate.parent_underdetermination_theorem.proposition.data
    assert theorem["same_field_restriction"]
    assert theorem["positive_gauge_compatible_completions"] == 2
    assert theorem["completions_not_scale_equivalent"]
    assert theorem["field_action_selects_unique_bath_rate"] is False
    assert theorem["riesz_equation_selects_unique_rate"]
    assert theorem["riesz_condition_is_additional"]
    assert certificate.alternative_rate_metric == sp.diag(
        *([sp.Rational(1, 3)] * 6 + [sp.Rational(2, 3)] * 6)
    )
    assert certificate.dynamical_witness == (0, 8)

    registry = verify_all()
    registered = next(
        gate
        for gate in registry["gates"]
        if gate["identifier"]
        == "version8_metric_dual_environment_parent_action_origin_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 6

    result = {
        "date": "2026-08-30",
        "gate": "version8_metric_dual_environment_parent_action_origin_gate",
        "common_field_action": {
            "cross_real_dimension": 12,
            "field_metric": "K_B=3 I_12",
            "quadratic_restriction": "S_field=(1/2) x^T K_B x",
        },
        "exact_counterexample": {
            "canonical_rate": "R_1=I_12/3",
            "alternative_rate": "R_2=diag(I_6/3,2 I_6/3)",
            "both_positive": True,
            "both_gauge_compatible": True,
            "same_field_restriction": True,
            "same_minimal_jump_dimension": True,
            "not_scale_equivalent": True,
            "distinct_reduced_generator_witness": [0, 8],
        },
        "parent_hessians": {
            "canonical": "diag(3 I_12,3 I_12)",
            "alternative": "diag(3 I_12,3 I_6,(3/2) I_6)",
        },
        "riesz_boundary": {
            "extra_condition": "K_B R=I_12",
            "unique_solution": "R=K_B^-1=I_12/3",
            "condition_follows_from_existing_field_action": False,
            "lagrange_multiplier_can_impose_but_not_derive_condition": True,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "gate_count": registry["gate_count"],
            "total_obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][
                "version8_metric_dual_environment_parent_action_origin_gate"
            ],
        },
        "verdict": {
            "metric_dual_rate_is_unique_given_riesz_condition": True,
            "riesz_condition_derived_from_old_parent_action": False,
            "absolute_physical_time_selected": False,
            "status": "lcf_checked_parent_action_origin_no_go",
            "next_gate": "full_noise_cotangent_parent_or_fresh_ancilla_source_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()