#!/usr/bin/env python3
"""Migrate the full primitive Markov generator to the exact LCF eDSL."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_full_primitive_markov_generator_lcf_migration_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_full_primitive import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.jump_count == 25
    assert certificate.group_sizes == (1, 8, 3, 1, 6, 6)
    assert certificate.endpoint_theorem.proposition.data["checked_matrix_units"] == 221
    assert certificate.scalar_fixed_theorem.proposition.data["fixed_dimension"] == 1
    assert certificate.qlyr_closure_theorem.proposition.data["fixed_dimension"] == 1
    assert certificate.xldr_closure_theorem.proposition.data["fixed_dimension"] == 1
    assert certificate.positive_weight_theorem.proposition.data["relative_weights_selected"] is False

    old = json.loads(
        (ROOT / "s2t/results/s2t_v8_full_primitive_markov_generator_assembly_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    assert old["assembled_generator"]["self_adjoint_lindblad_jump_count"] == 25
    assert old["fixed_algebra"]["dimension"] == 1
    assert old["positive_weight_robustness"]["fixed_dimension_always_one"]

    registry = verify_all()
    registered = next(
        gate for gate in registry["gates"]
        if gate["identifier"] == "version8_full_primitive_markov_generator_assembly_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 9

    result = {
        "date": "2026-08-29",
        "gate": "version8_full_primitive_markov_generator_lcf_migration_gate",
        "exact_assembly": {
            "observable_algebra": "M11(C) direct_sum M10(C)",
            "jump_count": 25,
            "group_sizes_link_SU3_SU2_U1_QLYR_XLdR": list(certificate.group_sizes),
            "gksl": True,
            "unital": True,
            "trace_preserving": True,
            "endpoint_matrix_units_checked": 221,
        },
        "primitivity": {
            "base_fixed_dimension_without_cross": 2,
            "full_fixed_dimension": 1,
            "fixed_algebra": "C I21",
            "QLYR_alone_closes_C2": True,
            "XLdR_alone_closes_C2": True,
            "strict_finite_dimensional_decay_gap": True,
        },
        "positive_rate_family": {
            "all_six_weights_strictly_positive": True,
            "fixed_algebra_independent_of_positive_weights": True,
            "trace_detailed_balance_holds_termwise": True,
            "trace_detailed_balance_selects_relative_weights": False,
            "absolute_physical_rate_derived": False,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "certificate_sha256": registry["certificate_sha256"][
                "version8_full_primitive_markov_generator_assembly_gate"
            ],
        },
        "verdict": {
            "qualitative_primitivity_lcf_checked": True,
            "rate_metric_still_open": True,
            "status": "lcf-checked-primitive-class-rate-metric-open",
            "next_gate": "version8_kms_nontracial_relative_rate_lcf_migration_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()