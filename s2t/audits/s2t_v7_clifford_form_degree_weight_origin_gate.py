#!/usr/bin/env python3
"""Audit whether form degree or Clifford trace derives beta below 8/15."""

from __future__ import annotations

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
OUTPUT = ROOT / "s2t/results/s2t_v7_clifford_form_degree_weight_origin_gate_results.json"


def euclidean_gamma_matrices() -> list[np.ndarray]:
    identity = np.eye(2, dtype=complex)
    sigma_1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [
        np.kron(sigma_1, identity),
        np.kron(sigma_2, identity),
        np.kron(sigma_3, sigma_1),
        np.kron(sigma_3, sigma_2),
    ]


def clifford_two_form(field: np.ndarray, gamma: list[np.ndarray]) -> np.ndarray:
    result = np.zeros((4, 4), dtype=complex)
    for first in range(4):
        for second in range(first + 1, 4):
            result += field[first, second] * gamma[first] @ gamma[second]
    return result


def main() -> None:
    gamma = euclidean_gamma_matrices()
    identity = np.eye(4, dtype=complex)
    clifford_residual = max(
        np.max(np.abs(gamma[first] @ gamma[second]
                      + gamma[second] @ gamma[first]
                      - 2.0 * float(first == second) * identity))
        for first in range(4) for second in range(4)
    )
    assert clifford_residual < 1.0e-12

    rng = np.random.default_rng(20260828)
    maximum_two_form_isometry_residual = 0.0
    maximum_scalar_isometry_residual = 0.0
    maximum_ordered_sum_ratio_residual = 0.0
    for _ in range(200):
        raw = rng.normal(size=(4, 4))
        field = raw - raw.T
        clifford = clifford_two_form(field, gamma)
        hodge_norm = float(sum(field[mu, nu] ** 2
                               for mu in range(4) for nu in range(mu + 1, 4)))
        clifford_norm = float(np.trace(clifford.conj().T @ clifford).real / 4.0)
        ordered_component_norm = float(np.sum(field**2))
        maximum_two_form_isometry_residual = max(
            maximum_two_form_isometry_residual, abs(clifford_norm - hodge_norm)
        )
        maximum_ordered_sum_ratio_residual = max(
            maximum_ordered_sum_ratio_residual,
            abs(ordered_component_norm - 2.0 * hodge_norm),
        )

        scalar = float(rng.normal())
        scalar_clifford = scalar * identity
        scalar_norm = float(
            np.trace(scalar_clifford.conj().T @ scalar_clifford).real / 4.0
        )
        maximum_scalar_isometry_residual = max(
            maximum_scalar_isometry_residual, abs(scalar_norm - scalar**2)
        )

    assert maximum_two_form_isometry_residual < 1.0e-11
    assert maximum_scalar_isometry_residual < 1.0e-12
    assert maximum_ordered_sum_ratio_residual < 1.0e-11

    # In the current construction both finite curvatures are spacetime
    # zero-forms and represented internal even/two-step moments.  Hence the
    # common spin trace is the scalar identity trace for both sectors.
    derived_beta = 1.0
    reference, variations, labels, down_cut = physical_blocks()
    physical_origin, physical_vacuum = physical_hessians(reference, variations)
    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))
    origin_values = eigvalsh(edge_origin + derived_beta * physical_origin)
    vacuum_values = eigvalsh(edge_vacuum + derived_beta * physical_vacuum)
    assert signature(origin_values) == [21, 0, 6]
    assert signature(vacuum_values) == [0, 0, 27]

    result = {
        "gate": "version7_clifford_form_degree_weight_origin_gate",
        "current_bidegree": {
            "edge_spacetime_form_degree": 0,
            "vertex_spacetime_form_degree": 0,
            "edge_internal_status": "represented even quadratic Hodge moment",
            "vertex_internal_status": "represented even quadratic Gram moment",
            "degree_distinguishes_sectors": False,
        },
        "clifford_audit": {
            "euclidean_dimension": 4,
            "spinor_dimension": 4,
            "maximum_clifford_relation_residual": float(clifford_residual),
            "maximum_scalar_isometry_residual": maximum_scalar_isometry_residual,
            "maximum_two_form_isometry_residual": maximum_two_form_isometry_residual,
            "maximum_ordered_component_double_count_residual": (
                maximum_ordered_sum_ratio_residual
            ),
            "normalized_clifford_trace_is_hodge_isometry": True,
            "apparent_factor_half_is_antisymmetric_index_bookkeeping": True,
        },
        "derived_weight": {
            "beta": derived_beta,
            "inside_required_window_0_to_8_over_15": False,
            "origin_signature": signature(origin_values),
            "vacuum_signature": signature(vacuum_values),
        },
        "forbidden_escape": {
            "declare_vertex_block_spacetime_two_form_after_hessian": True,
            "mix_ordered_component_norm_with_hodge_norm": True,
            "reason": "changes represented calculus or component convention sector by sector",
        },
        "verdict": {
            "form_degree_derives_beta_half": False,
            "clifford_trace_derives_beta_half": False,
            "current_route_closed": True,
            "status": "form_degree_clifford_origin_no_go_common_carrier_multiplicity_open",
            "next_gate": "version7_common_irreducible_trace_multiplicity_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()