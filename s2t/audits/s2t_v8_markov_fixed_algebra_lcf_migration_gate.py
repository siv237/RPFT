#!/usr/bin/env python3
"""Migrate the Tome VIII fixed-algebra selector to the exact LCF eDSL."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_markov_fixed_algebra_lcf_migration_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_fixed_algebra import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.gauge_commutant_dimension == 13
    assert certificate.one_sided_kernel_dimension == 4
    assert certificate.full_fixed_dimension == 2
    assert certificate.quark_projector_rank == 12
    assert certificate.lepton_projector_rank == 9

    old_result_path = ROOT / "s2t/results/s2t_v8_markov_fixed_algebra_selector_gate_results.json"
    old_result = json.loads(old_result_path.read_text(encoding="utf-8"))
    old_fixed = old_result["final_fixed_algebra"]
    comparison = {
        "old_numerical_dimension": old_fixed["dimension"],
        "exact_lcf_dimension": certificate.full_fixed_dimension,
        "old_quark_rank": old_fixed["quark_projector_rank"],
        "exact_quark_rank": certificate.quark_projector_rank,
        "old_lepton_rank": old_fixed["lepton_vectorlike_projector_rank"],
        "exact_lepton_rank": certificate.lepton_projector_rank,
    }
    assert comparison == {
        "old_numerical_dimension": 2,
        "exact_lcf_dimension": 2,
        "old_quark_rank": 12,
        "exact_quark_rank": 12,
        "old_lepton_rank": 9,
        "exact_lepton_rank": 9,
    }

    registry = verify_all()
    registered = next(
        item
        for item in registry["gates"]
        if item["identifier"] == "version8_markov_fixed_algebra_selector_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 3

    result = {
        "date": "2026-08-29",
        "gate": "version8_markov_fixed_algebra_lcf_migration_gate",
        "exact_endpoint_representation": {
            "source_dimension": 11,
            "target_dimension": 10,
            "block_diagonal_gauge_commutant_dimension": 13,
        },
        "linking_constraints": {
            "forward_equation": "A X_source = X_target A",
            "backward_equation": "X_source A^* = A^* X_target",
            "one_sided_kernel_dimension": certificate.one_sided_kernel_dimension,
            "full_self_adjoint_kernel_dimension": certificate.full_fixed_dimension,
            "exact_system_shape": [220, 13],
            "exact_system_rank": 11,
        },
        "fixed_algebra": {
            "algebra": "C P_quark direct_sum C P_lepton_vectorlike",
            "dimension": certificate.full_fixed_dimension,
            "quark_projector_rank": certificate.quark_projector_rank,
            "lepton_vectorlike_projector_rank": certificate.lepton_projector_rank,
            "projectors_complementary": True,
        },
        "comparison_with_original_numerical_gate": comparison,
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "certificate_sha256": registry["certificate_sha256"][
                "version8_markov_fixed_algebra_selector_gate"
            ],
        },
        "verdict": {
            "original_dimension_two_confirmed_exactly": True,
            "original_projector_ranks_confirmed_exactly": True,
            "floating_point_tolerance_required": False,
            "one_sided_linking_equation_is_sufficient": False,
            "full_self_adjoint_commutant_is_required": True,
            "status": "lcf-checked",
            "next_gate": "version8_linking_qms_gksl_lcf_migration_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()