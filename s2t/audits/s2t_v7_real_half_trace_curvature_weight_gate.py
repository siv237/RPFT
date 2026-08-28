#!/usr/bin/env python3
"""Audit whether Real doubling and one physical half-trace derive beta=1/2."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (
    edge_hessians,
    physical_blocks,
    physical_hessians,
    signature,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_real_half_trace_curvature_weight_gate_results.json"


def main() -> None:
    # Both preceding actions already use the same Hodge convention:
    # one half of the trace over the two endpoint moment-map blocks.
    oriented_edge_prefactor = Fraction(1, 2)
    oriented_vertex_prefactor = Fraction(1, 2)
    real_multiplicity = Fraction(2, 1)
    physical_half_trace = Fraction(1, 2)

    effective_edge = oriented_edge_prefactor * real_multiplicity * physical_half_trace
    effective_vertex = (
        oriented_vertex_prefactor * real_multiplicity * physical_half_trace
    )
    uniform_ratio = effective_vertex / effective_edge
    assert effective_edge == effective_vertex == Fraction(1, 2)
    assert uniform_ratio == 1

    # A factor one half can be manufactured only by acting asymmetrically on
    # the vertex sector.  This is precisely a sector-dependent central weight.
    asymmetric_vertex_half = Fraction(1, 2)
    manufactured_ratio = uniform_ratio * asymmetric_vertex_half
    assert manufactured_ratio == Fraction(1, 2)

    reference, variations, labels, down_cut = physical_blocks()
    physical_origin, physical_vacuum = physical_hessians(reference, variations)
    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))

    equal_origin_values = eigvalsh(edge_origin + physical_origin)
    half_origin_values = eigvalsh(edge_origin + 0.5 * physical_origin)
    equal_vacuum_values = eigvalsh(edge_vacuum + physical_vacuum)
    half_vacuum_values = eigvalsh(edge_vacuum + 0.5 * physical_vacuum)

    assert signature(equal_origin_values) == [21, 0, 6]
    assert signature(half_origin_values) == [7, 0, 20]
    assert signature(equal_vacuum_values) == [0, 0, 27]
    assert signature(half_vacuum_values) == [0, 0, 27]

    result = {
        "gate": "version7_real_half_trace_curvature_weight_gate",
        "trace_bookkeeping": {
            "edge_oriented_prefactor": str(oriented_edge_prefactor),
            "vertex_oriented_prefactor": str(oriented_vertex_prefactor),
            "real_multiplicity_both_blocks": int(real_multiplicity),
            "one_global_physical_half_trace": str(physical_half_trace),
            "effective_edge_prefactor": str(effective_edge),
            "effective_vertex_prefactor": str(effective_vertex),
            "derived_beta": str(uniform_ratio),
            "target_beta": "1/2",
        },
        "degree_and_clifford_test": {
            "edge_curvature_component_degree": 0,
            "vertex_curvature_component_degree": 0,
            "form_degree_factor_distinguishes_blocks": False,
            "common_clifford_identity_trace_distinguishes_blocks": False,
            "degree_two_reassignment_is_new_structure": True,
        },
        "hessian_consequence": {
            "uniform_real_half_trace_beta_one_origin_signature": signature(
                equal_origin_values
            ),
            "uniform_real_half_trace_beta_one_vacuum_signature": signature(
                equal_vacuum_values
            ),
            "conditional_beta_half_origin_signature": signature(half_origin_values),
            "conditional_beta_half_vacuum_signature": signature(half_vacuum_values),
            "beta_one_origin_minimum_eigenvalue": float(equal_origin_values[0]),
            "beta_half_heavy_gap": float(half_origin_values[7]),
        },
        "asymmetric_escape": {
            "extra_vertex_only_half_factor": str(asymmetric_vertex_half),
            "manufactured_beta": str(manufactured_ratio),
            "is_one_global_trace_operation": False,
            "is_free_central_sector_weight": True,
        },
        "verdict": {
            "real_doubling_changes_relative_weight": False,
            "global_half_trace_changes_relative_weight": False,
            "beta_half_derived": False,
            "uniform_construction_gives_beta_one": True,
            "status": "real_half_trace_origin_no_go_form_degree_calculus_open",
            "next_gate": "version7_clifford_form_degree_weight_origin_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()