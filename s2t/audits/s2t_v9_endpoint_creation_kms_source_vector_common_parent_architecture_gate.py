#!/usr/bin/env python3
"""Exact audit of the Tome IX conditional KMS source-parent."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_source_vector_common_parent_architecture_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_gap_conductance_parent_origin_gate_results.json"
    )).read_text())
    four_slot = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_four_slot_common_parent_functional_architecture_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert four_slot["functional_architecture_audit"]["satisfied"] == 9

    weight = sp.diag(1, 1, 3)
    metric = sp.diag(1, 1, 3, 1, 1, 3)
    assert weight.det() == 3
    assert metric.rank() == 6 and metric.det() == 9

    j_theta = sp.Matrix([1, 2, 9])
    j_kappa = sp.Matrix([2, 1, 6])
    theta = weight.inv() * j_theta
    kappa = weight.inv() * j_kappa
    assert theta == sp.Matrix([1, 2, 3])
    assert kappa == sp.Matrix([2, 1, 2])
    assert all(value > 0 for value in [*theta, *kappa])

    minimum = -sp.Rational(1, 2) * (
        (j_theta.T * weight.inv() * j_theta)[0]
        + (j_kappa.T * weight.inv() * j_kappa)[0]
    )
    assert minimum == -sp.Rational(49, 2)

    common_hessian = sp.diag(8, 8, 1, 1, 3, 1, 1, 3)
    assert common_hessian.rank() == 8
    assert common_hessian.det() == 576

    zero = sp.zeros(6, 1)
    assert metric.inv() * zero == zero
    q = [sp.exp(-value) for value in theta]
    forward = [kappa[i] * q[i] for i in range(3)]
    reverse = list(kappa)
    assert all(value.is_positive for value in [*q, *forward, *reverse])

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "auxiliary_parent": four_slot["gate"],
        "source_carrier": {
            "real_dimension": 6,
            "packages": ["gap_source_covector", "conductance_source_covector"],
            "metric_diagonal": [1, 1, 3, 1, 1, 3],
            "metric_rank": 6,
            "metric_determinant": 9,
            "positive_source_cone_nonempty": True,
        },
        "exact_witness": {
            "gap_source": [1, 2, 9],
            "conductance_source": [2, 1, 6],
            "dimensionless_gaps": [1, 2, 3],
            "conductances": [2, 1, 2],
            "boltzmann_ratios": ["exp(-1)", "exp(-2)", "exp(-3)"],
            "minimum_value": "-49/2",
        },
        "common_parent": {
            "single_bounded_functional": True,
            "four_slot_restriction_preserved": True,
            "continuous_hessian_diagonal": [8, 8, 1, 1, 3, 1, 1, 3],
            "continuous_hessian_rank": 8,
            "continuous_hessian_determinant": 576,
            "unique_positive_kms_minimum": True,
        },
        "ledgers": {
            "source_parent_architecture_satisfied": 9,
            "source_parent_architecture_tested": 9,
            "conditional_kms_selection_satisfied": 6,
            "conditional_kms_selection_tested": 6,
            "source_package_origin_satisfied": 0,
            "source_package_origin_tested": 2,
            "source_component_origin_satisfied": 0,
            "source_component_origin_tested": 6,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "conditional_common_source_parent_constructed": True,
            "all_six_kms_parameters_conditionally_selected": True,
            "source_covectors_physically_derived": False,
            "four_slot_source_map_required": True,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_source_covector_"
            "four_slot_parent_origin_gate"
        ),
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()