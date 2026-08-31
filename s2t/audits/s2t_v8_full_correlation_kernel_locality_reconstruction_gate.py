#!/usr/bin/env python3
"""Exact finite audit of full-kernel versus spectrum-only reconstruction."""

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_full_correlation_kernel_locality_reconstruction_gate_results.json"


def adjacency_star_5():
    matrix = np.zeros((5, 5), dtype=float)
    for leaf in range(1, 5):
        matrix[0, leaf] = 1.0
        matrix[leaf, 0] = 1.0
    return matrix


def adjacency_cycle4_plus_point():
    matrix = np.zeros((5, 5), dtype=float)
    for left, right in ((0, 1), (1, 2), (2, 3), (3, 0)):
        matrix[left, right] = 1.0
        matrix[right, left] = 1.0
    return matrix


def symmetric_function(matrix, function):
    values, vectors = np.linalg.eigh(matrix)
    return (vectors * function(values)) @ vectors.T


def heat_kernel(generator, tau):
    return symmetric_function(generator, lambda values: np.exp(-tau * values))


def logarithmic_generator(kernel, tau):
    return symmetric_function(kernel, lambda values: -np.log(values) / tau)


def support_from_generator(generator, tolerance=1.0e-8):
    support = np.zeros_like(generator, dtype=int)
    mask = ~np.eye(generator.shape[0], dtype=bool)
    support[mask & (generator < -tolerance)] = 1
    return support


def minimum_permutation_distance(left, right):
    minimum = float("inf")
    for permutation in itertools.permutations(range(left.shape[0])):
        permuted = right[np.ix_(permutation, permutation)]
        minimum = min(minimum, float(np.linalg.norm(left - permuted, ord="fro")))
    return minimum


star = adjacency_star_5()
cycle_point = adjacency_cycle4_plus_point()
identity = np.eye(5)
h_star = 3.0 * identity - star
h_cycle_point = 3.0 * identity - cycle_point

spectrum_star = np.linalg.eigvalsh(h_star)
spectrum_cycle_point = np.linalg.eigvalsh(h_cycle_point)
assert np.allclose(spectrum_star, spectrum_cycle_point, atol=1.0e-12)
assert np.allclose(spectrum_star, [1.0, 3.0, 3.0, 3.0, 5.0], atol=1.0e-12)

tau_values = (0.1, 0.3, 1.0, 2.0)
tests = []
for tau in tau_values:
    kernel_star = heat_kernel(h_star, tau)
    kernel_cycle_point = heat_kernel(h_cycle_point, tau)
    trace_difference = abs(float(np.trace(kernel_star) - np.trace(kernel_cycle_point)))
    full_kernel_distance = float(np.linalg.norm(kernel_star - kernel_cycle_point, ord="fro"))
    permutation_distance = minimum_permutation_distance(kernel_star, kernel_cycle_point)

    reconstructed_star = logarithmic_generator(kernel_star, tau)
    reconstructed_cycle_point = logarithmic_generator(kernel_cycle_point, tau)
    generator_error_star = float(np.linalg.norm(reconstructed_star - h_star, ord="fro"))
    generator_error_cycle_point = float(
        np.linalg.norm(reconstructed_cycle_point - h_cycle_point, ord="fro")
    )
    support_star = support_from_generator(reconstructed_star)
    support_cycle_point = support_from_generator(reconstructed_cycle_point)

    # Even an unknown positive time rescales the logarithmic generator but
    # leaves the off-diagonal support and its sign unchanged.
    wrong_time_support_star = support_from_generator(logarithmic_generator(kernel_star, 1.7 * tau))
    wrong_time_support_cycle_point = support_from_generator(
        logarithmic_generator(kernel_cycle_point, 1.7 * tau)
    )

    semigroup_error_star = float(
        np.linalg.norm(
            heat_kernel(h_star, tau / 3.0) @ heat_kernel(h_star, 2.0 * tau / 3.0)
            - kernel_star,
            ord="fro",
        )
    )

    assert trace_difference < 1.0e-12
    assert full_kernel_distance > 1.0e-6
    assert permutation_distance > 1.0e-6
    assert generator_error_star < 1.0e-11
    assert generator_error_cycle_point < 1.0e-11
    assert np.array_equal(support_star, star.astype(int))
    assert np.array_equal(support_cycle_point, cycle_point.astype(int))
    assert np.array_equal(wrong_time_support_star, star.astype(int))
    assert np.array_equal(wrong_time_support_cycle_point, cycle_point.astype(int))
    assert semigroup_error_star < 1.0e-12

    tests.append(
        {
            "tau": tau,
            "heat_trace_difference": trace_difference,
            "full_kernel_frobenius_distance_same_labels": full_kernel_distance,
            "minimum_full_kernel_distance_over_vertex_permutations": permutation_distance,
            "logarithmic_generator_error_star": generator_error_star,
            "logarithmic_generator_error_cycle_point": generator_error_cycle_point,
            "adjacency_support_recovered": True,
            "support_survives_unknown_positive_time_rescaling": True,
            "semigroup_error_star": semigroup_error_star,
        }
    )

permutation = np.array([2, 4, 1, 0, 3])
permutation_matrix = identity[permutation]
tau_covariance = 0.3
kernel = heat_kernel(h_star, tau_covariance)
permuted_generator = permutation_matrix @ h_star @ permutation_matrix.T
permuted_kernel = permutation_matrix @ kernel @ permutation_matrix.T
covariance_error = float(
    np.linalg.norm(heat_kernel(permuted_generator, tau_covariance) - permuted_kernel, ord="fro")
)
assert covariance_error < 1.0e-12

required_sources = {
    "early_toe_bridge": "s2t/docs/toe_ugsm_common_shadow_bridge.tex",
    "early_toe_paper": "s2t/docs/toe_ugsm_unified_shadow_paper.tex",
    "version5_no_go": "s2t/gates/version5_reduction_triangle_cocycle_gate.tex",
    "version5_no_go_result": "s2t/results/s2t_v5_reduction_triangle_cocycle_gate_results.json",
}
source_presence = {key: (ROOT / value).exists() for key, value in required_sources.items()}
assert all(source_presence.values())

result = {
    "date": "2026-08-28",
    "gate": "version8_full_correlation_kernel_locality_reconstruction_gate",
    "source_presence": source_presence,
    "finite_model": {
        "geometry_1": "connected star K_1,4",
        "geometry_2": "disconnected C_4 plus isolated point",
        "positive_generators": "H = 3 I - A",
        "common_generator_spectrum": [float(value) for value in spectrum_star],
        "full_kernel": "C_tau = exp(-tau H)",
        "observable_algebra": "distinguished diagonal algebra C^5",
    },
    "tests": tests,
    "basis_covariance": {
        "allowed_change": "simultaneous permutation of minimal projections of C^5",
        "error": covariance_error,
        "passed": True,
    },
    "exact_return_map": {
        "generator": "H = -tau^(-1) log(C_tau)",
        "finite_locality": "off-diagonal negative support of H",
        "known_tau_required_for_support": False,
        "known_scalar_shift_required_for_support": False,
        "connectivity_recovered": True,
    },
    "scope": {
        "spectrum_only_inverse_problem_still_fails": True,
        "full_kernel_with_observable_algebra_distinguishes_cospectral_pair": True,
        "full_spectral_triple_assumed": False,
        "observable_algebra_derived": False,
        "markov_normalization_proved": False,
        "strong_locality_proved": False,
        "physical_s2t_kernel_derived": False,
        "nonfactorized_parent_operator_derived": False,
    },
    "verdict": {
        "status": "positive_reopening_of_intermediate_full_kernel_class",
        "previous_version5_no_go_overturned": False,
        "previous_version5_scope_sharpened": True,
        "reason": (
            "scalar spectral data erase eigenvectors and locality, whereas the full positive "
            "semigroup kernel in a distinguished observable algebra recovers the generator "
            "and the finite adjacency support exactly"
        ),
    },
    "next_gate": {
        "name": "version8_correlation_semigroup_observable_algebra_origin_gate",
        "question": (
            "can the project derive one observable algebra and a positive normalized semigroup "
            "on its physical carrier, rather than supply the diagonal basis by hand?"
        ),
    },
}

payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
OUTPUT.write_text(payload, encoding="utf-8")
print(payload, end="")
print("sha256=" + hashlib.sha256(payload.encode("utf-8")).hexdigest())