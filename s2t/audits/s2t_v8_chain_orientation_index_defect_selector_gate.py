#!/usr/bin/env python3
"""Select the chain-number orientation using the inherited chiral index sign."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_chain_orientation_index_defect_selector_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import physical_blocks  # noqa: E402


def polar_coisometry(matrix: np.ndarray) -> np.ndarray:
    left, singular_values, right = np.linalg.svd(matrix, full_matrices=False)
    assert np.min(singular_values) > TOL
    return left @ right


def chiral_action(matrix: np.ndarray, grading_sign: int) -> float:
    """Norm of [d,d*]-sign*Gamma for Gamma=(-I_source,+I_target)."""
    source_dimension = matrix.shape[1]
    target_dimension = matrix.shape[0]
    source_block = -(matrix.conj().T @ matrix)
    target_block = matrix @ matrix.conj().T
    gamma_source = -grading_sign * np.eye(source_dimension)
    gamma_target = grading_sign * np.eye(target_dimension)
    return float(
        (
            np.linalg.norm(source_block - gamma_source, ord="fro") ** 2
            + np.linalg.norm(target_block - gamma_target, ord="fro") ** 2
        )
        / (source_dimension + target_dimension)
    )


def main() -> None:
    reference, _, _, _ = physical_blocks()
    coisometry = polar_coisometry(reference)
    source_dimension = coisometry.shape[1]
    target_dimension = coisometry.shape[0]
    real_dimension = 2 * source_dimension * target_dimension

    source_defect = np.eye(source_dimension) - coisometry.conj().T @ coisometry
    target_defect = np.eye(target_dimension) - coisometry @ coisometry.conj().T
    source_kernel_dimension = int(
        np.sum(np.linalg.eigvalsh(coisometry.conj().T @ coisometry) < TOL)
    )
    adjoint_kernel_dimension = int(
        np.sum(np.linalg.eigvalsh(coisometry @ coisometry.conj().T) < TOL)
    )
    fredholm_index = source_kernel_dimension - adjoint_kernel_dimension
    assert source_dimension == 11
    assert target_dimension == 10
    assert source_kernel_dimension == 1
    assert adjoint_kernel_dimension == 0
    assert fredholm_index == 1
    assert abs(np.trace(source_defect).real - 1.0) < TOL
    assert np.linalg.norm(target_defect) < TOL

    gamma = block_gamma = np.diag(
        np.concatenate([-np.ones(source_dimension), np.ones(target_dimension)])
    )
    number_endpoint = np.diag(
        np.concatenate([np.zeros(source_dimension), 2.0 * np.ones(target_dimension)])
    )
    reversed_number_endpoint = 2.0 * np.eye(source_dimension + target_dimension) - number_endpoint
    centered_number_residual = float(
        np.linalg.norm(number_endpoint - np.eye(21) - gamma)
    )
    reversed_centered_number_residual = float(
        np.linalg.norm(reversed_number_endpoint - np.eye(21) + gamma)
    )
    assert centered_number_residual < TOL
    assert reversed_centered_number_residual < TOL
    assert abs(-np.trace(gamma).real - fredholm_index) < TOL
    assert abs(-np.trace(-gamma).real + fredholm_index) < TOL

    zero = np.zeros_like(coisometry)
    selected_zero_action = chiral_action(zero, +1)
    reversed_zero_action = chiral_action(zero, -1)
    selected_vacuum_action = chiral_action(coisometry, +1)
    reversed_at_coisometry_action = chiral_action(coisometry, -1)
    assert abs(selected_zero_action - 1.0) < TOL
    assert abs(reversed_zero_action - 1.0) < TOL
    assert abs(selected_vacuum_action - 1.0 / 21.0) < TOL
    assert abs(reversed_at_coisometry_action - 81.0 / 21.0) < TOL

    selected_zero_hessian_eigenvalue = -8.0 / 21.0
    reversed_zero_hessian_eigenvalue = 8.0 / 21.0
    selected_hessian_signature = [real_dimension, 0, 0]
    reversed_hessian_signature = [0, 0, real_dimension]

    radial_rows = []
    for parameter in np.linspace(0.0, 2.0, 401):
        selected_numeric = chiral_action(parameter * coisometry, +1)
        reversed_numeric = chiral_action(parameter * coisometry, -1)
        selected_exact = (1.0 + 20.0 * (1.0 - parameter**2) ** 2) / 21.0
        reversed_exact = (1.0 + 20.0 * (1.0 + parameter**2) ** 2) / 21.0
        assert abs(selected_numeric - selected_exact) < TOL
        assert abs(reversed_numeric - reversed_exact) < TOL
        radial_rows.append(
            {
                "t": float(parameter),
                "selected_action": selected_numeric,
                "reversed_action": reversed_numeric,
            }
        )
    selected_minimum = min(radial_rows, key=lambda row: row["selected_action"])
    reversed_minimum = min(radial_rows, key=lambda row: row["reversed_action"])
    assert abs(selected_minimum["t"] - 1.0) < TOL
    assert abs(reversed_minimum["t"]) < TOL

    prior = json.loads(
        (
            ROOT / "s2t/results/s2t_v8_modular_bohr_parent_origin_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    forward = prior["directed_chain_number_QMS"]["forward_orientation"]
    reverse = prior["directed_chain_number_QMS"]["reverse_orientation"]
    assert forward["primitive"] and reverse["primitive"]
    assert abs(forward["target_to_source_density_ratio"] - np.exp(-2.0)) < TOL
    assert abs(reverse["target_to_source_density_ratio"] - np.exp(2.0)) < TOL

    result = {
        "date": "2026-08-29",
        "gate": "version8_chain_orientation_index_defect_selector_gate",
        "polar_index_data": {
            "operator": "U:C11 to C10",
            "UU_star_residual": float(np.linalg.norm(target_defect)),
            "source_defect_trace": float(np.trace(source_defect).real),
            "kernel_U": source_kernel_dimension,
            "kernel_U_star": adjoint_kernel_dimension,
            "Fredholm_index_U": fredholm_index,
        },
        "grading_chain_dictionary": {
            "inherited_chiral_grading": "Gamma=diag(-I11,+I10)",
            "chain_number": "N_boundary=diag(0*I11,2*I10)",
            "identity": "N_boundary-I21=Gamma",
            "identity_residual": centered_number_residual,
            "reversed_identity": "(2I21-N_boundary)-I21=-Gamma",
            "reversed_identity_residual": reversed_centered_number_residual,
            "index_identity": "index(U)=-Tr(Gamma)=+1",
        },
        "rank_change_orientation_test": {
            "selected_sign": {
                "grading": "Gamma",
                "zero_action": selected_zero_action,
                "zero_hessian_eigenvalue": selected_zero_hessian_eigenvalue,
                "zero_hessian_signature_negative_zero_positive": selected_hessian_signature,
                "radial_minimum": selected_minimum,
                "coisometry_action": selected_vacuum_action,
                "coisometry_vacuum": True,
                "rank_change_from_zero": True,
            },
            "reversed_sign": {
                "grading": "-Gamma",
                "zero_action": reversed_zero_action,
                "zero_hessian_eigenvalue": reversed_zero_hessian_eigenvalue,
                "zero_hessian_signature_negative_zero_positive": reversed_hessian_signature,
                "radial_minimum": reversed_minimum,
                "coisometry_action": reversed_at_coisometry_action,
                "coisometry_vacuum": False,
                "rank_change_from_zero": False,
            },
            "radial_scan_samples": len(radial_rows),
            "radial_formula_selected": "[1+20(1-t^2)^2]/21",
            "radial_formula_reversed": "[1+20(1+t^2)^2]/21",
        },
        "KMS_branch_selection": {
            "selected_chain_orientation": "N_boundary=diag(0*I11,2*I10)",
            "selected_rate_ratio": float(np.exp(-2.0)),
            "rejected_rate_ratio": float(np.exp(2.0)),
            "selected_QMS_decay_gap": forward["decay_gap"],
            "selection_principle": "compatibility with the inherited rank-changing chiral Hodge sign and index +1",
            "continuous_fit_used": False,
        },
        "remaining_boundary": {
            "dimensionless_orientation_selected": True,
            "dimensionless_up_down_ratio_selected": True,
            "base_intensities_linking_QLYR_XLdR_selected": False,
            "gauge_intensities_selected": False,
            "physical_energy_unit_selected": False,
            "physical_time_unit_selected": False,
            "status": "index_selects_chain_orientation_and_exp_minus_2_ratio_base_rate_metric_open",
        },
        "verdict": {
            "twofold_chain_orientation_closed": True,
            "forward_exp_minus_2_branch_passes": True,
            "reverse_exp_plus_2_branch_passes_rank_change_parent": False,
            "next_gate": "version8_common_chain_dirichlet_rate_metric_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()