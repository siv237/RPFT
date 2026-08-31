#!/usr/bin/env python3
"""Reconstruct the six QMS rates from a full operator-valued kernel."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigh, svdvals


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_correlation_kernel_short_time_rate_selector_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v8_common_chain_dirichlet_rate_metric_gate import TERM_ORDER  # noqa: E402
from s2t_v8_kms_nontracial_relative_rate_selector_gate import (  # noqa: E402
    assemble,
    block_diagonal,
    central_density,
)
from s2t_v8_modular_bohr_parent_origin_gate import directed_family_generator  # noqa: E402


def coefficient_design(named_terms: dict[str, np.ndarray]) -> np.ndarray:
    complex_design = np.stack(
        [named_terms[name].reshape(-1) for name in TERM_ORDER], axis=1
    )
    return np.vstack([complex_design.real, complex_design.imag])


def fit_coefficients(matrix: np.ndarray, design: np.ndarray) -> tuple[np.ndarray, float]:
    target = matrix.reshape(-1)
    target_real = np.concatenate([target.real, target.imag])
    coefficients, _, _, _ = np.linalg.lstsq(design, target_real, rcond=None)
    residual = float(np.linalg.norm(design @ coefficients - target_real))
    return coefficients, residual


def semigroup_kernel(
    generator: np.ndarray,
    tau: float,
    sqrt_metric: np.ndarray,
    inverse_sqrt_metric: np.ndarray,
) -> np.ndarray:
    symmetric = sqrt_metric @ generator @ inverse_sqrt_metric
    values, vectors = eigh((symmetric + symmetric.conj().T) / 2.0)
    symmetric_kernel = (vectors * np.exp(tau * values)) @ vectors.conj().T
    return inverse_sqrt_metric @ symmetric_kernel @ sqrt_metric


def logarithmic_generator(
    kernel: np.ndarray,
    tau: float,
    sqrt_metric: np.ndarray,
    inverse_sqrt_metric: np.ndarray,
) -> tuple[np.ndarray, float]:
    symmetric_kernel = sqrt_metric @ kernel @ inverse_sqrt_metric
    symmetric_kernel = (symmetric_kernel + symmetric_kernel.conj().T) / 2.0
    values, vectors = eigh(symmetric_kernel)
    assert np.min(values) > 0.0
    logarithm = (vectors * np.log(values)) @ vectors.conj().T
    generator = inverse_sqrt_metric @ (logarithm / tau) @ sqrt_metric
    return generator, float(np.min(values))


def main() -> None:
    symmetric_terms, _, transfers = assemble()
    ratio = float(np.exp(-2.0))
    source_density, target_density = central_density(ratio)
    metric = block_diagonal(
        [source_density * np.eye(121), target_density * np.eye(100)]
    )
    sqrt_metric = np.diag(np.sqrt(np.diag(metric).real))
    inverse_sqrt_metric = np.diag(1.0 / np.sqrt(np.diag(metric).real))

    named_terms = {
        "linking": directed_family_generator(transfers["linking"], ratio, 1.0),
        "SU3": symmetric_terms["SU3"],
        "SU2": symmetric_terms["SU2"],
        "U1": symmetric_terms["U1"],
        "QLYR": directed_family_generator(transfers["QLYR"], ratio, 1.0),
        "XLdR": directed_family_generator(transfers["XLdR"], ratio, 1.0),
    }
    design = coefficient_design(named_terms)
    singular_values = svdvals(design)
    design_rank = int(np.sum(singular_values > 1.0e-11 * singular_values[0]))
    condition_number = float(singular_values[0] / singular_values[-1])
    assert design_rank == 6

    rng = np.random.default_rng(20260829)
    logarithmic_tests = []
    for sample in range(6):
        # Keep exp(tau L) above floating-point underflow.  Very fast modes at
        # long observation times are physically present but numerically lost;
        # that separate resolution barrier is recorded below.
        true_weights = 10.0 ** rng.uniform(-1.0, 0.5, size=6)
        generator = sum(
            (
                true_weights[index] * named_terms[name]
                for index, name in enumerate(TERM_ORDER)
            ),
            np.zeros((221, 221), complex),
        )
        tau = (0.03, 0.08, 0.2, 0.5, 0.9, 1.4)[sample]
        kernel = semigroup_kernel(generator, tau, sqrt_metric, inverse_sqrt_metric)
        recovered, minimum_kernel_eigenvalue = logarithmic_generator(
            kernel, tau, sqrt_metric, inverse_sqrt_metric
        )
        recovered_weights, fit_residual = fit_coefficients(recovered, design)
        relative_error = float(
            np.linalg.norm(recovered_weights - true_weights)
            / np.linalg.norm(true_weights)
        )
        generator_error = float(
            np.linalg.norm(recovered - generator) / np.linalg.norm(generator)
        )

        # If tau is unknown, log(C_tau) reconstructs tau*kappa.  Normalized
        # relative rates remain identifiable.
        scaled_generator, _ = logarithmic_generator(
            kernel, 1.0, sqrt_metric, inverse_sqrt_metric
        )
        scaled_weights, scaled_fit_residual = fit_coefficients(scaled_generator, design)
        true_normalized = true_weights / np.sum(true_weights)
        recovered_normalized = scaled_weights / np.sum(scaled_weights)
        normalized_error = float(
            np.linalg.norm(recovered_normalized - true_normalized)
        )

        assert relative_error < 1.0e-9
        assert generator_error < 1.0e-9
        assert fit_residual < 1.0e-8
        assert scaled_fit_residual < 1.0e-8
        assert normalized_error < 1.0e-9
        logarithmic_tests.append(
            {
                "tau": tau,
                "true_weights": [float(value) for value in true_weights],
                "recovered_weights": [float(value) for value in recovered_weights],
                "relative_weight_error": relative_error,
                "relative_generator_error": generator_error,
                "fit_residual": fit_residual,
                "minimum_symmetric_kernel_eigenvalue": minimum_kernel_eigenvalue,
                "unknown_tau_normalized_rate_error": normalized_error,
            }
        )

    finite_difference_weights = np.array([0.7, 1.3, 0.9, 1.1, 1.7, 0.4])
    finite_difference_generator = sum(
        (
            finite_difference_weights[index] * named_terms[name]
            for index, name in enumerate(TERM_ORDER)
        ),
        np.zeros((221, 221), complex),
    )
    finite_difference_tests = []
    for epsilon in (1.0e-1, 3.0e-2, 1.0e-2, 3.0e-3, 1.0e-3):
        kernel = semigroup_kernel(
            finite_difference_generator, epsilon, sqrt_metric, inverse_sqrt_metric
        )
        derivative = (kernel - np.eye(221)) / epsilon
        recovered_weights, residual = fit_coefficients(derivative, design)
        relative_error = float(
            np.linalg.norm(recovered_weights - finite_difference_weights)
            / np.linalg.norm(finite_difference_weights)
        )
        finite_difference_tests.append(
            {
                "epsilon": epsilon,
                "relative_weight_error": relative_error,
                "fit_residual": residual,
            }
        )
    assert finite_difference_tests[-1]["relative_weight_error"] < finite_difference_tests[0][
        "relative_weight_error"
    ]

    resolution_probe_weights = np.array([1.0e-2, 1.0e2, 0.3, 2.0, 0.7, 4.0])
    resolution_probe_generator = sum(
        (
            resolution_probe_weights[index] * named_terms[name]
            for index, name in enumerate(TERM_ORDER)
        ),
        np.zeros((221, 221), complex),
    )
    resolution_probe_kernel = semigroup_kernel(
        resolution_probe_generator, 1.4, sqrt_metric, inverse_sqrt_metric
    )
    resolution_symmetric = sqrt_metric @ resolution_probe_kernel @ inverse_sqrt_metric
    resolution_eigenvalues = eigh(
        (resolution_symmetric + resolution_symmetric.conj().T) / 2.0,
        eigvals_only=True,
    )
    numerically_lost_modes = int(np.sum(resolution_eigenvalues <= np.finfo(float).eps))
    assert numerically_lost_modes > 0

    kernel_sources = {
        "toe_bridge": ROOT / "s2t/docs/toe_ugsm_common_shadow_bridge.tex",
        "unified_shadow": ROOT / "s2t/docs/toe_ugsm_unified_shadow_paper.tex",
        "version8_reconstruction": ROOT
        / "s2t/results/s2t_v8_full_correlation_kernel_locality_reconstruction_gate_results.json",
    }
    source_text = {
        name: path.read_text(encoding="utf-8") for name, path in kernel_sources.items()
    }
    assert "\\sim" in source_text["toe_bridge"]
    assert "M11(C) direct_sum M10(C)" not in source_text["toe_bridge"]
    reconstruction_result = json.loads(source_text["version8_reconstruction"])
    assert not reconstruction_result["scope"]["physical_s2t_kernel_derived"]

    result = {
        "date": "2026-08-29",
        "gate": "version8_correlation_kernel_short_time_rate_selector_gate",
        "rate_identifiability": {
            "term_order": TERM_ORDER,
            "design_rank": design_rank,
            "design_condition_number": condition_number,
            "formula_known_tau": "L=tau^(-1) log C_tau",
            "formula_short_time": "L=dC_tau/dtau at tau=0",
            "six_relative_rates_reconstructible_from_full_operator_kernel": True,
            "logarithmic_tests": logarithmic_tests,
        },
        "unknown_time_calibration": {
            "log_kernel_recovers": "tau times all six rates",
            "normalized_relative_rates_recoverable": True,
            "absolute_common_rate_recoverable": False,
            "reason": "tau and the overall generator scale occur only as a product",
        },
        "short_time_finite_difference": {
            "true_weights": [float(value) for value in finite_difference_weights],
            "tests": finite_difference_tests,
            "error_decreases_toward_tau_zero": True,
        },
        "finite_time_resolution_barrier": {
            "probe_tau": 1.4,
            "probe_weights": [float(value) for value in resolution_probe_weights],
            "modes_below_machine_epsilon": numerically_lost_modes,
            "interpretation": "fast modes require sufficiently short-time or high-precision kernel data",
        },
        "project_source_audit": {
            "toe_bridge_relation": "C_sigma is postulated only up to an approximate heat-kernel relation",
            "toe_bridge_uses_symbol_sim": True,
            "toe_kernel_carrier": "spacetime/compact geometric carrier, not M11 direct_sum M10 endpoint algebra",
            "version8_existing_full_kernel_test": "synthetic C5 cospectral control",
            "version8_result_says_physical_kernel_derived": False,
            "independent_physical_endpoint_C_tau_matrix_found": False,
            "current_kernels_are_generated_from_already_chosen_generators": True,
        },
        "verdict": {
            "full_kernel_would_select_five_relative_rate_freedoms": True,
            "calibrated_kernel_would_also_select_absolute_rate": True,
            "current_project_supplies_independent_physical_full_kernel": False,
            "status": "conditional_exact_rate_reconstruction_pass_physical_correlation_kernel_absent",
            "next_gate": "version8_physical_correlation_kernel_parent_action_origin_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()