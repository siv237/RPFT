#!/usr/bin/env python3
"""LCF audit of the trace-dual cross interaction selector."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "s2t/results/s2t_v8_trace_dual_cross_interaction_selector_gate_results.json"
)
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_trace_dual_cross_coupling import (  # noqa: E402
    build_certificate,
)
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.field_metric_eigenvalue == 3
    assert certificate.canonical_rate_eigenvalue == sp.Rational(1, 3)
    assert certificate.interaction_coupling_eigenvalue == 1 / sp.sqrt(3)
    assert certificate.field_metric_theorem.proposition.data["shape"] == [12, 12]
    assert certificate.generator_scaling_theorem.proposition.data["basis_size"] == 441
    equivalence = certificate.environment_equivalence_theorem.proposition.data
    assert equivalence["orthogonal_environment_relabelling"]
    assert equivalence["reduced_channel_unique_up_to_scale"]
    freedom = certificate.coupling_freedom_theorem.proposition.data
    assert freedom["full_commutant_dimension"] == 8
    assert freedom["symmetric_commutant_dimension"] == 4

    registry = verify_all()
    registered = next(
        gate
        for gate in registry["gates"]
        if gate["identifier"] == "version8_trace_dual_cross_interaction_selector_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 9

    result = {
        "date": "2026-08-30",
        "gate": "version8_trace_dual_cross_interaction_selector_gate",
        "cross_field_module": {
            "complex_shape": [2, 3],
            "real_dimension": 12,
            "family_order": ["QLYR", "XLdR"],
            "color_dimension": 3,
            "finite_superconnection_metric": "3 I_12",
            "exact_no_float_derivation": True,
        },
        "metric_dual_selector": {
            "principle": "minimal environment jump module is the metric dual of the cross amplitude module under the same finite supertrace",
            "field_metric": "K_B=3 I_12",
            "dual_rate_metric": "R=K_B^-1=I_12/3",
            "canonical_coupling": "C_tr=I_12/sqrt(3)",
            "coupling_gram": "C_tr^T C_tr=I_12/3",
            "conditional_on_metric_dual_identification": True,
        },
        "coupling_quotient": {
            "full_real_gauge_commutant_dimension": 8,
            "symmetric_rate_metric_dimension": 4,
            "fixed_scalar_gram_couplings": "C=O/sqrt(3)",
            "orthogonal_condition": "O^T O=I_12",
            "environment_frame_relabelling": True,
            "same_reduced_channel": True,
        },
        "dynamics": {
            "short_time_tangent": "Psi_h=I+(h/3)L_cross+O(h^2)",
            "exact_full_matrix_unit_checks": 441,
            "polar_cross_axis_preserved": True,
            "dimensionless_cross_rate_shape_selected": True,
            "absolute_physical_time_selected": False,
        },
        "scope_boundary": {
            "cross_module_closed": True,
            "linking_rate_selected": False,
            "SU3_rate_selected": False,
            "SU2_rate_selected": False,
            "U1_rate_selected": False,
            "fresh_ancilla_supply_derived": False,
            "metric_dual_environment_principle_derived_from_parent_action": False,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "gate_count": registry["gate_count"],
            "total_obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][
                "version8_trace_dual_cross_interaction_selector_gate"
            ],
        },
        "verdict": {
            "cross_rate_metric_unique_up_to_time_scale": True,
            "status_is_conditional": True,
            "full_physical_qms_closed": False,
            "status": "lcf_checked_conditional_trace_dual_cross_rate_selector",
            "next_gate": "metric_dual_environment_parent_action_origin_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()