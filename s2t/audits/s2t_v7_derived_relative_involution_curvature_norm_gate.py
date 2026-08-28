#!/usr/bin/env python3
"""Test a positive edge plus relative-incidence Hodge curvature norm."""

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_weak_aligned_cycle_competition_gate import carrier, OFFSETS, DIMS


BETA = 0.5
ROOT_MULTIPLICITIES = np.array([3.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0])


def physical_blocks():
    background, roots, heavy, labels, down_cut = carrier()
    left_names = ["QL", "LL", "XL", "YL"]
    right_names = ["uR", "dR", "eR", "XR", "YR"]
    left = np.concatenate([np.arange(OFFSETS[name], OFFSETS[name] + DIMS[name])
                           for name in left_names])
    right = np.concatenate([np.arange(OFFSETS[name], OFFSETS[name] + DIMS[name])
                            for name in right_names])

    def oriented(matrix):
        return matrix[np.ix_(right, left)]

    return oriented(background), [oriented(item) for item in roots + heavy], labels, down_cut


def physical_hessians(reference, variations):
    left_reference = reference.conj().T @ reference
    right_reference = reference @ reference.conj().T

    def linearized(item):
        return (reference.conj().T @ item + item.conj().T @ reference,
                reference @ item.conj().T + item @ reference.conj().T)

    linear = [linearized(item) for item in variations]
    vacuum = np.array([[np.real(np.vdot(first[0], second[0])
                                + np.vdot(first[1], second[1]))
                        for second in linear] for first in linear])

    def quadratic(first, second):
        return ((first.conj().T @ second + second.conj().T @ first) / 2.0,
                (first @ second.conj().T + second @ first.conj().T) / 2.0)

    origin = np.array([[-2.0 * np.real(
        np.vdot(left_reference, quadratic(first, second)[0])
        + np.vdot(right_reference, quadratic(first, second)[1]))
        for second in variations] for first in variations])
    return origin, vacuum


def edge_hessians(down_cut, total):
    origin = np.concatenate([
        -4.0 * ROOT_MULTIPLICITIES,
        np.full(down_cut, 4.0 * 1.6),
        np.full(total - 7 - down_cut, 4.0 * 0.9),
    ])
    vacuum = np.concatenate([
        8.0 * ROOT_MULTIPLICITIES,
        np.full(down_cut, 4.0 * 1.6),
        np.full(total - 7 - down_cut, 4.0 * 0.9),
    ])
    return np.diag(origin), np.diag(vacuum)


def signature(values):
    return [int(np.sum(values < -1e-10)), int(np.sum(abs(values) <= 1e-10)),
            int(np.sum(values > 1e-10))]


def rounded(values):
    return [float(f"{value:.12g}") for value in values]


def main():
    reference, variations, labels, down_cut = physical_blocks()
    physical_origin, physical_vacuum = physical_hessians(reference, variations)
    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))

    def heavy_minimum(beta):
        matrix = edge_origin + beta * physical_origin
        return float(eigvalsh(matrix[7:, 7:])[0])

    critical_beta = brentq(heavy_minimum, 0.5, 0.7)
    origin = edge_origin + BETA * physical_origin
    vacuum = edge_vacuum + BETA * physical_vacuum
    equal_weight_origin = edge_origin + physical_origin
    origin_values = eigvalsh(origin)
    vacuum_values = eigvalsh(vacuum)
    equal_values = eigvalsh(equal_weight_origin)

    assert reference.shape == (10, 11) and len(variations) == 27
    assert signature(origin_values) == [7, 0, 20]
    assert signature(vacuum_values) == [0, 0, 27]
    assert abs(critical_beta - 8.0 / 15.0) < 1e-10
    assert signature(equal_values) != [7, 0, 20]
    assert vacuum_values[0] > 5.5 and origin_values[7] > 0.39

    result = {
        "gate": "version7_derived_relative_involution_curvature_norm_gate",
        "carrier": {"oriented_physical_shape": [10, 11],
                    "tested_real_slice_dimension": len(variations),
                    "root_directions": 7, "heavy_directions": 20},
        "positive_action": {
            "edge_part": "derived edge Hodge norm with root levels 1 and Casimirs 8/5,9/10",
            "physical_part": "1/2*(||A^*A-A0^*A0||^2+||AA^*-A0A0^*||^2)",
            "combination": "S_edge + beta*S_physical",
            "benchmark_beta": BETA,
        },
        "origin_hessian": {"signature": signature(origin_values),
                           "eigenvalues": rounded(origin_values),
                           "heavy_gap": float(origin_values[7])},
        "vacuum_hessian": {"signature": signature(vacuum_values),
                           "minimum_eigenvalue": float(vacuum_values[0]),
                           "eigenvalues": rounded(vacuum_values)},
        "normalization_test": {
            "critical_beta": critical_beta,
            "exact_candidate": "8/15",
            "allowed_heavy_window": "0 <= beta < 8/15",
            "beta_half_passes": True,
            "equal_weight_beta_one_signature": signature(equal_values),
            "beta_half_derived_from_real_half_trace": False,
        },
        "verdict": {
            "positive_curvature_norm_local_pass": True,
            "correct_origin_selector": True,
            "strictly_stable_target_vacuum": True,
            "free_relative_weight_eliminated": False,
            "status": "one_ratio_local_pass_beta_half_origin_open",
            "next_gate": "version7_real_half_trace_curvature_weight_gate",
        },
    }
    out = (Path(__file__).resolve().parents[1] / "results"
           / "s2t_v7_derived_relative_involution_curvature_norm_gate_results.json")
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(out)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()