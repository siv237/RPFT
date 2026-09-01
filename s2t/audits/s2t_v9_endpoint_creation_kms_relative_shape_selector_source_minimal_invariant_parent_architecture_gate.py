#!/usr/bin/env python3
"""Exact and ProofDSL audit of the invariant KMS relative-shape parent."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version9_kms_relative_shape_invariant_parent import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = (
    "endpoint_creation_kms_relative_shape_selector_source_"
    "minimal_invariant_parent_architecture_gate"
)
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_relative_shape_selector_"
        "source_parent_origin_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    certificate = build_certificate()
    verified = verify_gate(SPEC)
    assert verified.theorem.proposition.kind == "verified_gate"
    assert len(verified.obligations) == 10
    assert certificate.doubled_hessian.rank() == 4
    assert certificate.doubled_hessian.det() == sp.Rational(25, 9)
    assert certificate.common_hessian.rank() == 12
    assert certificate.common_hessian.det() == sp.Rational(5184, 25)

    rs, ra = sp.symbols("r_s r_a", positive=True)
    rt = (5 - rs - ra) / 3
    constrained_hessian = sp.hessian(
        -sp.log(rs) - sp.log(ra) - 3 * sp.log(rt),
        [rs, ra],
    ).subs({rs: 1, ra: 1})
    assert constrained_hessian.eigenvals() == {
        sp.Integer(1): 1,
        sp.Rational(5, 3): 1,
    }

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "invariant_parent": {
            "type_operator": "diag(r_s,r_a,r_t,r_t,r_t)",
            "constraint": "r_s+r_a+3r_t=5",
            "functional_per_package": "-log(r_s r_a r_t^3)",
            "source_free_in_type_operator_coordinates": True,
            "block_unitary_invariant": True,
            "positive_boundary_coercive": True,
        },
        "selected_package": {
            "gap_shape": [1, 1, 1],
            "conductance_shape": [1, 1, 1],
            "effective_selector_source": [1, 1, 1, 1],
            "dimensionless_gaps_equal": True,
            "conductances_equal_per_channel": True,
        },
        "exact_hessians": {
            "single_constrained": [["4/3", "1/3"], ["1/3", "4/3"]],
            "single_spectrum": [[1, 1], ["5/3", 1]],
            "doubled_rank": 4,
            "doubled_determinant": "25/9",
            "single_log_ratio_spectrum": [["3/5", 1], [1, 1]],
            "common_parent_rank": 12,
            "common_parent_determinant": "5184/25",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "gate_identifier": verified.spec.identifier,
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
            "analytic_boundary": (
                "global log-barrier minimum uses weighted AM-GM outside "
                "the current finite-dimensional kernel"
            ),
        },
        "ledgers": {
            "invariant_parent_architecture_satisfied": 10,
            "invariant_parent_architecture_tested": 10,
            "proofdsl_obligations_satisfied": 10,
            "proofdsl_obligations_tested": 10,
            "conditional_selector_source_selection_satisfied": 4,
            "conditional_selector_source_selection_tested": 4,
            "logdet_parent_origin_satisfied": 0,
            "logdet_parent_origin_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "minimal_invariant_parent_constructed": True,
            "isotropic_selector_sources_conditionally_selected": True,
            "algebraic_core_lcf_checked": True,
            "global_minimum_analytic_not_lcf_checked": True,
            "logdet_parent_physically_derived": False,
            "logdet_origin_gate_required": True,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_relative_shape_logdet_parent_"
            "measure_origin_gate"
        ),
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()