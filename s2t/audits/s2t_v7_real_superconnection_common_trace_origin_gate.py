#!/usr/bin/env python3
"""Test whether the formal three-block heat functional is one Quillen supertrace."""

import hashlib
import json
from pathlib import Path

import numpy as np


TIMES = (0.1, 0.7, 1.0, 2.0, 5.0)


def heat_trace(matrix, t):
    eigenvalues = np.linalg.eigvalsh(matrix)
    return float(np.sum(np.exp(-t * eigenvalues)))


def odd_heat_supertrace(block, t):
    plus_square = block.conj().T @ block
    minus_square = block @ block.conj().T
    return heat_trace(plus_square, t) - heat_trace(minus_square, t)


def rounded(values):
    return [float(f"{value:.12g}") for value in values]


def main():
    rng = np.random.default_rng(20260828)
    rectangular_tests = []
    for n_minus, n_plus in ((3, 5), (4, 4), (6, 2)):
        block = (rng.normal(size=(n_minus, n_plus))
                 + 1j * rng.normal(size=(n_minus, n_plus)))
        values = [odd_heat_supertrace(block, t) for t in TIMES]
        expected = n_plus - n_minus
        scaled = [odd_heat_supertrace(scale * block, 1.0)
                  for scale in (0.2, 0.7, 1.0, 1.9)]
        assert max(abs(value - expected) for value in values + scaled) < 1e-10
        rectangular_tests.append({
            "dimensions_minus_plus": [n_minus, n_plus],
            "expected_index": expected,
            "heat_supertraces": rounded(values),
            "scale_test_at_t_1": rounded(scaled),
        })

    q = np.diag([0.7, 1.1, 1.4])
    role_involution = np.diag([-1.0, -1.0, 1.0])
    target_weighted_trace = float(np.trace(
        role_involution @ np.diag(np.exp(-np.diag(q) ** 2))))
    oddness_defect = float(np.linalg.norm(
        role_involution @ q + q @ role_involution))

    doubled_block = q
    doubled_supertraces = [odd_heat_supertrace(doubled_block, t) for t in TIMES]
    assert oddness_defect > 1.0
    assert max(abs(value) for value in doubled_supertraces) < 1e-12

    previous_path = (Path(__file__).resolve().parents[1] / "results"
                     / "s2t_v7_common_carrier_root_stationarity_gate_results.json")
    previous = json.loads(previous_path.read_text(encoding="utf-8"))
    full_minimum = previous["full_hessian"]["minimum_eigenvalue"]
    assert full_minimum > 1.0

    result = {
        "gate": "version7_real_superconnection_common_trace_origin_gate",
        "finite_odd_operator_identity": {
            "operator": "A=[[0,B^*],[B,0]]",
            "supertrace": "Str exp(-t*A^2)=dim(H_plus)-dim(H_minus)=index(B)",
            "rectangular_tests": rectangular_tests,
            "field_derivatives_vanish": True,
        },
        "target_role_insertion": {
            "K": "diag(-1,-1,+1)",
            "weighted_trace_example": target_weighted_trace,
            "anticommutator_norm_KQ_plus_QK": oddness_defect,
            "Q_is_odd_for_K": False,
            "interpretation": "Tr(K exp(-Q^2)) reproduces signs only by an extra role involution",
        },
        "canonical_odd_doubling": {
            "construction": "D_Q=[[0,Q^*],[Q,0]]",
            "heat_supertraces": rounded(doubled_supertraces),
            "real_doubling_then_physical_half_trace": "still zero/index-only",
        },
        "comparison_with_previous_gate": {
            "formal_full_hessian_minimum": full_minimum,
            "formal_functional_is_nonconstant": True,
            "can_equal_index_only_supertrace": False,
        },
        "verdict": {
            "single_ordinary_quillen_heat_supertrace_origin": False,
            "real_structure_rescues_degree_zero_potential": False,
            "manual_role_involution_would_reproduce_signs": True,
            "manual_role_involution_admissible_as_derivation": False,
            "scope": "finite-dimensional degree-zero heat supertrace",
            "status": "quillen_heat_supertrace_no_go_derived_relative_involution_or_curvature_norm_open",
            "next_gate": "version7_derived_relative_involution_curvature_norm_gate",
        },
    }
    out = (Path(__file__).resolve().parents[1] / "results"
           / "s2t_v7_real_superconnection_common_trace_origin_gate_results.json")
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(out)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()