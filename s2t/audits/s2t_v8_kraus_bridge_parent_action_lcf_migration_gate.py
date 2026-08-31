#!/usr/bin/env python3
"""Migrate the Kraus parent-action Hessian gate to the exact LCF eDSL."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_kraus_bridge_parent_action_lcf_migration_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_kraus_parent_hessian import (  # noqa: E402
    build_certificate,
)
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.cross_coefficient == sp.Rational(7, 36)
    assert certificate.cross_total_coefficient == sp.Rational(7, 3)
    assert certificate.gaussian_unit_rate == sp.Rational(35, 96)
    assert certificate.bridge_signature_theorem.proposition.data == {
        "negative": 0,
        "zero": 15,
        "positive": 12,
        "dimension": 27,
    }
    assert certificate.origin_signature_theorem.proposition.data == {
        "negative": 7,
        "zero": 0,
        "positive": 20,
        "dimension": 27,
    }
    assert certificate.vacuum_signature_theorem.proposition.data == {
        "negative": 0,
        "zero": 0,
        "positive": 27,
        "dimension": 27,
    }

    old_path = ROOT / "s2t/results/s2t_v8_kraus_bridge_parent_action_hessian_gate_results.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    assert old["field_dependent_dirichlet_term"]["cross_direction_coefficient"] == "7/36"
    assert old["field_dependent_dirichlet_term"]["hessian_signature"] == [0, 15, 12]
    assert old["vacuum_rate_test"]["tree_level_bridge_rate"] == 0.0
    assert abs(
        old["gaussian_fluctuation_probe"]["unit_strength_decay"]
        - float(sp.Rational(35, 96))
    ) < 1.0e-12

    registry = verify_all()
    registered = next(
        gate
        for gate in registry["gates"]
        if gate["identifier"] == "version8_kraus_bridge_parent_action_hessian_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 11

    result = {
        "date": "2026-08-29",
        "gate": "version8_kraus_bridge_parent_action_lcf_migration_gate",
        "exact_field_dirichlet_term": {
            "cross_real_directions": 12,
            "internal_control_directions": 8,
            "coefficient_per_cross_direction": "7/36",
            "total_unit_covariance_decay": "7/3",
            "field_hessian": "(7/18) I_12",
            "embedded_27d_signature": [0, 15, 12],
        },
        "symbolic_hessian_compatibility": {
            "bridge_weight_assumption": "lambda_bridge >= 0",
            "origin_signature_for_every_allowed_weight": [7, 0, 20],
            "vacuum_signature_for_every_allowed_weight": [0, 0, 27],
            "finite_weight_scan_needed": False,
            "scope": "the exact 27-dimensional real slice used by the source gate",
        },
        "tree_vacuum": {
            "cross_coordinates": "z_0=...=z_11=0",
            "field_energy": "0",
            "field_gradient": "zero",
            "kraus_weight_vector": "(z_0^2,...,z_11^2)=0",
            "tree_level_generator": "zero",
            "positive_second_variation": True,
        },
        "covariance_and_rate": {
            "symbolic_positive_family_scales": ["c_Q > 0", "c_X > 0"],
            "central_decay": "7(c_Q+c_X)/6",
            "unit_strength_gaussian_probe": "35/96",
            "overall_fluctuation_strength_derived": False,
            "unique_physical_rate_derived": False,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "certificate_sha256": registry["certificate_sha256"][
                "version8_kraus_bridge_parent_action_hessian_gate"
            ],
        },
        "verdict": {
            "positive_parent_term_exact": True,
            "all_nonnegative_weights_preserve_tested_signatures": True,
            "classical_vacuum_launches_bridge": False,
            "mass_is_not_noise_rate": True,
            "covariance_or_dilation_still_required": True,
            "status": "lcf-checked-kinematic-parent-tree-rate-no-go",
            "next_gate": "version8_cross_arrow_covariance_lcf_migration_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()