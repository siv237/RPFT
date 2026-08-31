#!/usr/bin/env python3
"""Test whether the existing parent action uniquely determines C_tau."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_physical_correlation_kernel_parent_action_origin_gate_results.json"
TOL = 1.0e-10
FAMILIES = ["linking", "SU3", "SU2", "U1", "QLYR", "XLdR"]


def normalized(values: np.ndarray) -> np.ndarray:
    return values / np.sum(values)


def main() -> None:
    cross_result = json.loads(
        (ROOT / "s2t/results/s2t_v8_cross_arrow_covariance_origin_gate_results.json").read_text()
    )
    rate_result = json.loads(
        (ROOT / "s2t/results/s2t_v8_common_chain_dirichlet_rate_metric_gate_results.json").read_text()
    )
    freeze_result = json.loads(
        (ROOT / "s2t/results/s2t_v7_qualitative_parent_mass_metric_freeze_gate_results.json").read_text()
    )
    gauge_result = json.loads(
        (ROOT / "s2t/results/s2t_v7_common_gauge_f0_anchor_gate_results.json").read_text()
    )

    pair = np.array(
        cross_result["polar_linking_cross_structure"]["linking_pair_matrix"],
        dtype=float,
    )
    # One representative parent Hessian.  The first four unit entries do not
    # claim a derivation; they make the action-to-dynamics obstruction as
    # favourable as possible.  The Q/X block is the actual project block.
    hessian = np.eye(6)
    hessian[-2:, -2:] = pair
    covariance = np.linalg.inv(hessian)
    assert np.min(np.linalg.eigvalsh(hessian)) > 0.0

    mobilities = {
        "isotropic": np.ones(6),
        "family_anisotropic": np.array([2.0, 0.5, 3.0, 0.7, 1.2, 0.8]),
        "transfer_fast": np.array([4.0, 1.0, 1.0, 1.0, 4.0, 4.0]),
        "gauge_fast": np.array([1.0, 4.0, 4.0, 4.0, 1.0, 1.0]),
        "cross_split": np.array([1.0, 1.0, 1.0, 1.0, 0.25, 3.0]),
    }
    tau = 0.4
    mobility_tests = []
    kernels = []
    for name, entries in mobilities.items():
        mobility = np.diag(entries)
        drift = mobility @ hessian
        # The same Gaussian covariance is stationary for every positive M:
        # A Sigma + Sigma A^T = 2 M, A=M H, Sigma=H^-1.
        lyapunov_residual = float(
            np.linalg.norm(drift @ covariance + covariance @ drift.T - 2.0 * mobility)
        )
        kernel = expm(-tau * drift)
        kernels.append(kernel)
        assert lyapunov_residual < TOL
        assert np.max(np.real(np.linalg.eigvals(drift))) > 0.0
        mobility_tests.append(
            {
                "name": name,
                "mobility_diagonal": entries.tolist(),
                "normalized_short_time_family_rates": normalized(entries).tolist(),
                "stationary_covariance_residual": lyapunov_residual,
                "kernel_trace_at_tau_0_4": float(np.trace(kernel).real),
                "kernel_frobenius_norm_at_tau_0_4": float(np.linalg.norm(kernel)),
            }
        )

    pairwise_kernel_distances = []
    names = list(mobilities)
    for i in range(len(kernels)):
        for j in range(i + 1, len(kernels)):
            distance = float(np.linalg.norm(kernels[i] - kernels[j]))
            assert distance > 1.0e-3
            pairwise_kernel_distances.append(
                {"left": names[i], "right": names[j], "frobenius_distance": distance}
            )

    # Even the already-derived cross Hessian does not select one covariance
    # rule or eta.  Record the family-level Q/X ratios supplied by the three
    # candidate prescriptions at eta=1.
    eta_one = next(
        row
        for row in cross_result["relative_metric_scan"]
        if row["relative_metric_weight_eta"] == 1.0
    )
    classical = np.array(eta_one["classical_normalized_pair_covariance"])
    quantum = np.array(eta_one["quantum_normalized_pair_covariance"])
    pair_hessian = np.array(eta_one["pair_hessian"])
    heat = expm(-pair_hessian)
    cross_rules = {
        "classical_H_inverse": classical,
        "quantum_H_inverse_half": quantum,
        "heat_exp_minus_H": heat / np.trace(heat),
    }
    cross_rule_rows = []
    for name, matrix in cross_rules.items():
        cross_rule_rows.append(
            {
                "rule": name,
                "QLYR_to_XLdR_diagonal_ratio": float(matrix[0, 0] / matrix[1, 1]),
                "normalized_offdiagonal": float(matrix[0, 1]),
                "normalized_matrix": matrix.tolist(),
            }
        )
    ratios = [row["QLYR_to_XLdR_diagonal_ratio"] for row in cross_rule_rows]
    assert max(ratios) - min(ratios) > 1.0e-2

    protocol_text = (ROOT / "s2t/docs/research_protocol_toe_ugsm.tex").read_text(
        encoding="utf-8"
    )
    bridge_text = (ROOT / "s2t/docs/toe_ugsm_unified_shadow_paper.tex").read_text(
        encoding="utf-8"
    )
    assert "постулируются" in protocol_text
    assert "\\hat C_\\sigma \\sim" in bridge_text
    assert not freeze_result["frozen_boundaries"]["unique_parent_action_derived"]
    assert not freeze_result["frozen_boundaries"]["unique_mass_metric_derived"]
    assert not freeze_result["frozen_boundaries"]["full_spacetime_gauge_closure_obtained"]
    assert not gauge_result["verdict"]["common_physical_gauge_anchor_admitted"]
    assert not cross_result["verdict"]["unique_nonzero_covariance_scale_derived"]
    assert rate_result["invariant_metric_cone"]["linear_span_rank"] == 6

    coverage = {
        "linking": "incidence and shape known; mobility/overall coefficient not derived",
        "SU3": "generator representation known; physical gauge mobility not derived",
        "SU2": "generator representation known; physical gauge mobility not derived",
        "U1": "generator representation known; physical gauge mobility not derived",
        "QLYR": "cross Hessian axis known; eta, prescription and scale not derived",
        "XLdR": "cross Hessian axis known; eta, prescription and scale not derived",
    }

    result = {
        "date": "2026-08-29",
        "gate": "version8_physical_correlation_kernel_parent_action_origin_gate",
        "fixed_parent_hessian_test": {
            "family_order": FAMILIES,
            "hessian": hessian.tolist(),
            "stationary_covariance": covariance.tolist(),
            "number_of_positive_mobility_choices": len(mobilities),
            "all_share_exact_same_stationary_covariance": True,
            "all_produce_distinct_finite_time_kernels": True,
            "mobility_tests": mobility_tests,
            "pairwise_kernel_distances": pairwise_kernel_distances,
            "identity": "A=M H, Sigma=H^-1 implies A Sigma + Sigma A^T=2M",
        },
        "cross_parent_prescription_ambiguity": {
            "eta": 1.0,
            "candidate_rules": cross_rule_rows,
            "QLYR_XLdR_ratio_not_rule_independent": True,
            "existing_parent_selects_axis_only": True,
        },
        "project_parent_coverage": {
            "families": coverage,
            "six_family_span_rank": 6,
            "unique_parent_action_derived_in_tome7": False,
            "unique_mass_metric_derived_in_tome7": False,
            "full_spacetime_gauge_closure_obtained": False,
            "common_physical_gauge_anchor_admitted": False,
            "cross_covariance_scale_derived": False,
        },
        "source_audit": {
            "TOE_gaussian_kernel_is_postulated": True,
            "TOE_UGSM_heat_kernel_bridge_is_approximate": True,
            "parent_action_alone_determines_equilibrium_measure_not_mobility": True,
            "independent_fluctuation_dissipation_or_bath_spectral_density_required": True,
        },
        "verdict": {
            "existing_parent_action_uniquely_determines_C_tau": False,
            "existing_parent_action_uniquely_determines_six_rates": False,
            "same_action_can_have_different_physical_kernels": True,
            "status": "parent_action_equilibrium_shape_pass_dynamical_mobility_no_go",
            "next_gate": "version8_fluctuation_dissipation_mobility_origin_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()