#!/usr/bin/env python3
"""Test whether chain degree and a common Dirichlet metric fix family rates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh, svdvals


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_common_chain_dirichlet_rate_metric_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v8_kms_nontracial_relative_rate_selector_gate import (  # noqa: E402
    assemble,
    block_diagonal,
    central_density,
    pair_vector,
)
from s2t_v8_modular_bohr_parent_origin_gate import (  # noqa: E402
    directed_family_generator,
)


TERM_ORDER = ["linking", "SU3", "SU2", "U1", "QLYR", "XLdR"]
DEGREES = {
    "linking": 2,
    "SU3": 0,
    "SU2": 0,
    "U1": 0,
    "QLYR": 2,
    "XLdR": 2,
}


def kernel_dimension(matrix: np.ndarray) -> int:
    singular_values = svdvals(matrix)
    threshold = max(TOL, 1.0e-11 * float(singular_values[0]))
    return int(np.sum(singular_values <= threshold))


def generator_diagnostics(
    named_terms: dict[str, np.ndarray], weights: dict[str, float], metric: np.ndarray
) -> dict:
    generator = sum(
        (weights[name] * named_terms[name] for name in TERM_ORDER),
        np.zeros((221, 221), complex),
    )
    fixed_dimension = kernel_dimension(generator)
    sqrt_diagonal = np.sqrt(np.diag(metric).real)
    sqrt_metric = np.diag(sqrt_diagonal)
    inverse_sqrt_metric = np.diag(1.0 / sqrt_diagonal)
    symmetric = sqrt_metric @ generator @ inverse_sqrt_metric
    symmetry_residual = float(np.linalg.norm(metric @ generator - generator.conj().T @ metric))
    similarity_residual = float(np.linalg.norm(symmetric - symmetric.conj().T))
    spectrum = eigvalsh((symmetric + symmetric.conj().T) / 2.0)
    gap = float(-spectrum[-fixed_dimension - 1]) if fixed_dimension < 221 else 0.0
    return {
        "weights_linking_SU3_SU2_U1_QLYR_XLdR": [float(weights[name]) for name in TERM_ORDER],
        "fixed_algebra_dimension": fixed_dimension,
        "KMS_symmetry_residual": symmetry_residual,
        "similarity_self_adjoint_residual": similarity_residual,
        "decay_gap": gap,
        "largest_decay": float(-spectrum[0]),
        "positive_eigenvalue_count": int(np.sum(spectrum > TOL)),
    }


def main() -> None:
    symmetric_terms, _, transfers = assemble()
    ratio = float(np.exp(-2.0))
    source_density, target_density = central_density(ratio)
    metric = block_diagonal(
        [source_density * np.eye(121), target_density * np.eye(100)]
    )
    density_vector = pair_vector(
        source_density * np.eye(11), target_density * np.eye(10)
    )

    named_terms = {
        "linking": directed_family_generator(transfers["linking"], ratio, 1.0),
        "SU3": symmetric_terms["SU3"],
        "SU2": symmetric_terms["SU2"],
        "U1": symmetric_terms["U1"],
        "QLYR": directed_family_generator(transfers["QLYR"], ratio, 1.0),
        "XLdR": directed_family_generator(transfers["XLdR"], ratio, 1.0),
    }

    termwise = {}
    for name, term in named_terms.items():
        kms_residual = float(np.linalg.norm(metric @ term - term.conj().T @ metric))
        stationarity_residual = float(np.linalg.norm(term.conj().T @ density_vector))
        termwise[name] = {
            "chain_degree": DEGREES[name],
            "superoperator_HS_norm": float(np.linalg.norm(term)),
            "KMS_symmetry_residual": kms_residual,
            "stationarity_residual": stationarity_residual,
        }
        assert kms_residual < TOL
        assert stationarity_residual < TOL

    flattened = np.stack([named_terms[name].reshape(-1) for name in TERM_ORDER], axis=1)
    singular_values = svdvals(flattened)
    family_span_rank = int(np.sum(singular_values > 1.0e-10 * singular_values[0]))
    assert family_span_rank == 6

    rng = np.random.default_rng(20260829)
    positive_weight_scan = []
    for _ in range(64):
        values = 10.0 ** rng.uniform(-4.0, 4.0, size=6)
        weights = dict(zip(TERM_ORDER, values))
        row = generator_diagnostics(named_terms, weights, metric)
        assert row["fixed_algebra_dimension"] == 1
        assert row["KMS_symmetry_residual"] < TOL
        assert row["positive_eigenvalue_count"] == 0
        positive_weight_scan.append(row)

    # If the metric is required to depend only on |ad_N|, there are still
    # two spectral projectors: degree zero and degree two.
    degree_ratio_scan = []
    for transfer_to_gauge in np.logspace(-4.0, 4.0, 41):
        weights = {
            name: float(transfer_to_gauge if DEGREES[name] == 2 else 1.0)
            for name in TERM_ORDER
        }
        row = generator_diagnostics(named_terms, weights, metric)
        assert row["fixed_algebra_dimension"] == 1
        assert row["KMS_symmetry_residual"] < TOL
        degree_ratio_scan.append(
            {"transfer_to_gauge_weight": float(transfer_to_gauge), **row}
        )

    natural_representatives = {}
    representative_weights = {
        "identity_metric_f_of_adN2_equals_1": {
            name: 1.0 for name in TERM_ORDER
        },
        "pure_commutator_metric_f_x_equals_x": {
            name: float(DEGREES[name] ** 2) for name in TERM_ORDER
        },
        "identity_plus_commutator_f_x_equals_1_plus_x": {
            name: float(1 + DEGREES[name] ** 2) for name in TERM_ORDER
        },
        "heat_metric_f_x_equals_exp_minus_x": {
            name: float(np.exp(-(DEGREES[name] ** 2))) for name in TERM_ORDER
        },
        "resolvent_metric_f_x_equals_1_over_1_plus_x": {
            name: float(1.0 / (1 + DEGREES[name] ** 2)) for name in TERM_ORDER
        },
        "equal_superoperator_norm": {
            name: float(1.0 / termwise[name]["superoperator_HS_norm"])
            for name in TERM_ORDER
        },
    }
    for name, weights in representative_weights.items():
        row = generator_diagnostics(named_terms, weights, metric)
        natural_representatives[name] = row
        assert row["KMS_symmetry_residual"] < TOL

    pure_commutator = natural_representatives[
        "pure_commutator_metric_f_x_equals_x"
    ]
    assert pure_commutator["fixed_algebra_dimension"] > 1
    primitive_representatives = [
        row
        for name, row in natural_representatives.items()
        if name != "pure_commutator_metric_f_x_equals_x"
    ]
    assert all(row["fixed_algebra_dimension"] == 1 for row in primitive_representatives)
    representative_gaps = [row["decay_gap"] for row in primitive_representatives]
    assert max(representative_gaps) / min(representative_gaps) > 2.0

    prior = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v8_chain_orientation_index_defect_selector_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert prior["KMS_branch_selection"]["selected_rate_ratio"] == ratio

    result = {
        "date": "2026-08-29",
        "gate": "version8_common_chain_dirichlet_rate_metric_gate",
        "selected_KMS_background": {
            "state": "rho_N proportional to exp(-N_boundary)",
            "target_to_source_density_ratio": ratio,
            "upward_to_downward_rate_ratio": ratio,
        },
        "termwise_Dirichlet_data": termwise,
        "invariant_metric_cone": {
            "independent_named_families": TERM_ORDER,
            "linear_span_rank": family_span_rank,
            "positive_KMS_symmetric_coefficients": 6,
            "relative_coefficients_after_removing_overall_time_scale": 5,
            "KMS_or_stationarity_selects_them": False,
        },
        "chain_degree_only_metric": {
            "degree_zero_families": [name for name in TERM_ORDER if DEGREES[name] == 0],
            "degree_two_families": [name for name in TERM_ORDER if DEGREES[name] == 2],
            "spectral_projector_count": 2,
            "relative_parameter_after_overall_scale": 1,
            "scan_samples": len(degree_ratio_scan),
            "all_positive_ratios_primitive_and_KMS": True,
            "gap_minimum": min(row["decay_gap"] for row in degree_ratio_scan),
            "gap_maximum": max(row["decay_gap"] for row in degree_ratio_scan),
            "sample_rows": degree_ratio_scan,
        },
        "natural_metric_representatives": natural_representatives,
        "positive_weight_robustness": {
            "samples": len(positive_weight_scan),
            "independent_range": "1e-4 through 1e4",
            "all_primitive": True,
            "all_KMS_symmetric": True,
            "gap_minimum": min(row["decay_gap"] for row in positive_weight_scan),
            "gap_maximum": max(row["decay_gap"] for row in positive_weight_scan),
            "sample_rows": positive_weight_scan,
        },
        "no_go": {
            "pure_adN_squared_metric_keeps_gauge_diffusion": False,
            "pure_adN_squared_fixed_algebra_dimension": pure_commutator[
                "fixed_algebra_dimension"
            ],
            "adding_a_degree_zero_floor_is_unique": False,
            "common_chain_degree_selects_one_rate_metric": False,
            "reason": "ad_N^2 has distinct degree-zero and degree-two projectors, while full gauge covariance permits still finer independent family weights",
        },
        "verdict": {
            "one_reproducible_equal_weight_representative_exists": True,
            "unique_relative_rate_metric_derived": False,
            "dimensionless_exp_minus_2_up_down_ratio_preserved": True,
            "status": "chain_degree_KMS_ratio_closed_common_Dirichlet_rate_metric_no_go",
            "next_gate": "version8_correlation_kernel_short_time_rate_selector_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()