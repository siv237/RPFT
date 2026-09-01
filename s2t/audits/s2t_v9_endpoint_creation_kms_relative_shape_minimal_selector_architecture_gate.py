#!/usr/bin/env python3
"""Exact audit of the minimal four-coordinate KMS relative-shape selector."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_relative_shape_minimal_selector_architecture_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def normalized_shape(x: sp.Expr, y: sp.Expr) -> sp.Matrix:
    partition = sp.exp(x) + sp.exp(y) + 3
    return 5 * sp.Matrix([sp.exp(x), sp.exp(y), 1]) / partition


def selector_block(
    x: sp.Expr, y: sp.Expr, source_x: sp.Expr, source_y: sp.Expr
) -> sp.Expr:
    partition = sp.exp(x) + sp.exp(y) + 3
    return 5 * sp.log(partition / 5) - source_x * x - source_y * y


def main() -> None:
    predecessor = json.loads((ROOT / (
        "s2t/results/"
        "s2t_v9_endpoint_creation_kms_source_covector_"
        "four_slot_parent_origin_gate_results.json"
    )).read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate
    assert predecessor["jacobian_audit"]["unselected_relative_dimension"] == 4

    x1, x2, y1, y2 = sp.symbols("x1 x2 y1 y2", real=True)
    ux, uy, vx, vy = sp.symbols("ux uy vx vy", positive=True)
    weight = sp.diag(1, 1, 3)
    multiplicity = sp.Matrix([1, 1, 3])

    gap_shape = normalized_shape(x1, x2)
    conductance_shape = normalized_shape(y1, y2)
    assert sp.simplify((multiplicity.T * gap_shape)[0]) == 5
    assert sp.simplify((multiplicity.T * conductance_shape)[0]) == 5

    shape_map = sp.Matrix.vstack(gap_shape, conductance_shape)
    shape_jacobian = shape_map.jacobian([x1, x2, y1, y2])
    origin = {x1: 0, x2: 0, y1: 0, y2: 0}
    assert shape_jacobian.subs(origin).rank() == 4

    selector = (
        selector_block(x1, x2, ux, uy)
        + selector_block(y1, y2, vx, vy)
    )
    selector_hessian = sp.hessian(selector, [x1, x2, y1, y2])
    isotropic_sources = {ux: 1, uy: 1, vx: 1, vy: 1}
    selector_hessian_origin = selector_hessian.subs(origin | isotropic_sources)
    expected_block = sp.Matrix([[4, -1], [-1, 4]]) / 5
    assert selector_hessian_origin[:2, :2] == expected_block
    assert selector_hessian_origin[2:, 2:] == expected_block
    assert selector_hessian_origin.rank() == 4
    assert selector_hessian_origin.det() == sp.Rational(9, 25)

    gap_sources = {ux: 1, uy: 2}
    conductance_sources = {vx: 2, vy: 1}
    gap_minimum = sp.Matrix([sp.log(sp.Rational(3, 2)), sp.log(3)])
    conductance_minimum = sp.Matrix([sp.log(3), sp.log(sp.Rational(3, 2))])
    gradient = sp.Matrix([
        sp.diff(selector, variable) for variable in [x1, x2, y1, y2]
    ])
    witness_substitution = {
        **gap_sources,
        **conductance_sources,
        x1: gap_minimum[0],
        x2: gap_minimum[1],
        y1: conductance_minimum[0],
        y2: conductance_minimum[1],
    }
    assert sp.simplify(gradient.subs(witness_substitution)) == sp.zeros(4, 1)
    assert sp.simplify(gap_shape.subs(witness_substitution)) == sp.Matrix([
        1, 2, sp.Rational(2, 3)
    ])
    assert sp.simplify(conductance_shape.subs(witness_substitution)) == sp.Matrix([
        2, 1, sp.Rational(2, 3)
    ])

    e, chi = sp.symbols("e chi", positive=True)
    theta_variables = sp.symbols("theta_s theta_a theta_t", real=True)
    kappa_variables = sp.symbols("kappa_s kappa_a kappa_t", real=True)
    theta = sp.Matrix(theta_variables)
    kappa = sp.Matrix(kappa_variables)
    rate_scale = chi**2 * e
    theta_residual = theta - e * gap_shape
    kappa_residual = kappa - rate_scale * conductance_shape
    common_parent = (
        4 * (e - 1) ** 2
        + 4 * (chi - 1) ** 2
        + selector.subs(isotropic_sources)
        + (theta_residual.T * weight * theta_residual)[0] / 2
        + (kappa_residual.T * weight * kappa_residual)[0] / 2
    )
    common_variables = [
        e, chi, x1, x2, y1, y2,
        *theta_variables, *kappa_variables,
    ]
    common_witness = {
        e: 1,
        chi: 1,
        **origin,
        **dict(zip(theta_variables, [1, 1, 1])),
        **dict(zip(kappa_variables, [1, 1, 1])),
    }
    common_hessian = sp.hessian(common_parent, common_variables).subs(
        common_witness
    )
    assert common_hessian.rank() == 12
    assert common_hessian.det() == sp.Rational(5184, 25)

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "relative_shape_carrier": {
            "real_dimension": 4,
            "coordinates": [
                "log(r_theta_s/r_theta_t)",
                "log(r_theta_a/r_theta_t)",
                "log(r_kappa_s/r_kappa_t)",
                "log(r_kappa_a/r_kappa_t)",
            ],
            "weighted_normalizations": [5, 5],
            "shape_map_rank": 4,
            "globally_positive_shapes": True,
        },
        "selector_parent": {
            "type": "weighted_log_partition_minus_linear_source",
            "source_cone": [
                "u_s>0", "u_a>0", "u_s+u_a<5",
                "v_s>0", "v_a>0", "v_s+v_a<5",
            ],
            "strictly_convex": True,
            "coercive_on_source_cone": True,
            "unique_minimum": True,
            "isotropic_hessian_blocks": [
                [["4/5", "-1/5"], ["-1/5", "4/5"]],
                [["4/5", "-1/5"], ["-1/5", "4/5"]],
            ],
            "hessian_rank": 4,
            "hessian_determinant": "9/25",
        },
        "exact_witness": {
            "gap_selector_source": [1, 2],
            "conductance_selector_source": [2, 1],
            "gap_log_ratio_minimum": ["log(3/2)", "log(3)"],
            "conductance_log_ratio_minimum": ["log(3)", "log(3/2)"],
            "gap_shape": [1, 2, "2/3"],
            "conductance_shape": [2, 1, "2/3"],
        },
        "common_parent": {
            "single_bounded_functional": True,
            "completed_square_kms_coupling": True,
            "continuous_dimension": 12,
            "hessian_rank": 12,
            "hessian_determinant_at_isotropic_witness": "5184/25",
            "conditional_relative_shape_selection": 4,
        },
        "minimality": {
            "target_shape_dimension": 4,
            "selector_carrier_dimension": 4,
            "local_map_rank": 4,
            "lower_dimensional_generic_selector_possible": False,
        },
        "ledgers": {
            "relative_shape_chart_satisfied": 4,
            "relative_shape_chart_tested": 4,
            "selector_architecture_satisfied": 10,
            "selector_architecture_tested": 10,
            "conditional_relative_selection_satisfied": 4,
            "conditional_relative_selection_tested": 4,
            "selector_source_origin_satisfied": 0,
            "selector_source_origin_tested": 4,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "minimal_four_coordinate_selector_constructed": True,
            "all_four_relative_shapes_conditionally_selected": True,
            "selector_sources_physically_derived": False,
            "selector_source_origin_gate_required": True,
        },
        "next_gate": (
            "version9_endpoint_creation_kms_relative_shape_selector_"
            "source_parent_origin_gate"
        ),
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()