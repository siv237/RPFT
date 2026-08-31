#!/usr/bin/env python3
"""Test whether the cross-sector Kraus bridge is already dynamical in Tome VII."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_kraus_bridge_parent_action_hessian_gate_results.json"
TOL = 1.0e-10

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (  # noqa: E402
    edge_hessians,
    physical_blocks,
    signature,
)


def block_generator(incidence: np.ndarray) -> np.ndarray:
    """Return -ad(D_incidence)^2/2 on the two endpoint matrix algebras."""
    target_dimension, source_dimension = incidence.shape
    source_gram = incidence.conj().T @ incidence
    target_gram = incidence @ incidence.conj().T
    source_diagonal = (
        -0.5 * np.kron(np.eye(source_dimension), source_gram)
        -0.5 * np.kron(source_gram.T, np.eye(source_dimension))
    )
    target_diagonal = (
        -0.5 * np.kron(np.eye(target_dimension), target_gram)
        -0.5 * np.kron(target_gram.T, np.eye(target_dimension))
    )
    return np.block(
        [
            [source_diagonal, np.kron(incidence.T, incidence.conj().T)],
            [np.kron(incidence.conj(), incidence), target_diagonal],
        ]
    )


def pair_vector(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    return np.concatenate(
        [source.reshape(-1, order="F"), target.reshape(-1, order="F")]
    )


def rounded(values) -> list[float]:
    return [float(f"{value:.12g}") for value in values]


def main() -> None:
    reference, variations, heavy_labels, down_cut = physical_blocks()
    heavy_variations = variations[7:]
    assert len(variations) == 27
    assert len(heavy_variations) == len(heavy_labels) == 20

    source_dimension = reference.shape[1]
    target_dimension = reference.shape[0]
    quark_source = np.diag([1.0] * 6 + [0.0] * 5)
    quark_target = np.diag([1.0] * 6 + [0.0] * 4)
    lepton_source = np.eye(source_dimension) - quark_source
    lepton_target = np.eye(target_dimension) - quark_target
    quark_unit = pair_vector(quark_source, quark_target) / np.sqrt(12.0)
    lepton_unit = pair_vector(lepton_source, lepton_target) / 3.0
    central_contrast = (
        3.0 * quark_unit - np.sqrt(12.0) * lepton_unit
    ) / np.sqrt(21.0)
    assert abs(np.linalg.norm(central_contrast) - 1.0) < TOL

    coefficients = []
    for label, variation in zip(heavy_labels, heavy_variations):
        normalized = variation / np.linalg.norm(variation, ord="fro")
        generator = block_generator(normalized)
        coefficient = float(
            np.real(-np.vdot(central_contrast, generator @ central_contrast))
        )
        coefficients.append(coefficient)

    cross_mask = np.array(
        [label.startswith(("QLYR", "XLdR")) for label in heavy_labels]
    )
    control_mask = ~cross_mask
    assert int(np.sum(cross_mask)) == 12
    assert np.max(np.abs(np.array(coefficients)[control_mask])) < TOL
    assert np.max(np.abs(np.array(coefficients)[cross_mask] - 7.0 / 36.0)) < TOL
    assert abs(sum(np.array(coefficients)[cross_mask]) - 7.0 / 3.0) < TOL

    # E_bridge(z)=-<Q,L_z Q>=sum_i d_i z_i^2.  Therefore its real Hessian
    # is diag(2 d_i).  It is positive semidefinite and supported only on the
    # twelve colored cross-arrow coordinates.
    bridge_hessian = np.zeros((27, 27))
    bridge_hessian[7:, 7:] = np.diag(2.0 * np.array(coefficients))
    bridge_values = eigvalsh(bridge_hessian)
    assert signature(bridge_values) == [0, 15, 12]

    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))
    positive_weights = (0.0, 1.0e-6, 0.1, 1.0, 1.0e3, 1.0e6)
    hessian_scan = []
    for weight in positive_weights:
        origin_values = eigvalsh(edge_origin + weight * bridge_hessian)
        vacuum_values = eigvalsh(edge_vacuum + weight * bridge_hessian)
        row = {
            "bridge_weight": weight,
            "origin_signature": signature(origin_values),
            "origin_heavy_gap": float(origin_values[7]),
            "vacuum_signature": signature(vacuum_values),
            "vacuum_minimum_eigenvalue": float(vacuum_values[0]),
        }
        assert row["origin_signature"] == [7, 0, 20]
        assert row["vacuum_signature"] == [0, 0, 27]
        hessian_scan.append(row)

    # At the Tome VII vacuum all cross-arrow heavy fields vanish.  The
    # field-dependent Kraus generator and its transition rate consequently
    # vanish there, even though its second variation is positive.
    zero_coordinates = np.zeros(12)
    unit_coordinates = np.ones(12)
    cross_coefficients = np.array(coefficients)[cross_mask]
    rate_at_vacuum = float(np.dot(cross_coefficients, zero_coordinates**2))
    unit_covariance_rate = float(np.sum(cross_coefficients * unit_coordinates))
    assert rate_at_vacuum == 0.0
    assert abs(unit_covariance_rate - 7.0 / 3.0) < TOL

    # A common covariance C=c I is a useful benchmark, not a unique output:
    # gauge covariance allows independent positive weights on QLYR and XLdR.
    covariance_scan = []
    for scale in (1.0e-6, 1.0e-3, 1.0, 1.0e3, 1.0e6):
        decay = scale * unit_covariance_rate
        covariance_scan.append(
            {
                "isotropic_covariance_scale": scale,
                "central_kernel_dimension": 1,
                "central_decay_eigenvalue": decay,
            }
        )
    assert all(row["central_decay_eigenvalue"] > 0 for row in covariance_scan)
    family_covariance_scan = []
    for qlyr_scale, xldr_scale in (
        (1.0e-3, 1.0),
        (1.0, 1.0e-3),
        (1.0, 1.0),
        (1.0, 10.0),
        (10.0, 1.0),
    ):
        decay = (7.0 / 6.0) * (qlyr_scale + xldr_scale)
        family_covariance_scan.append(
            {
                "QLYR_covariance_scale": qlyr_scale,
                "XLdR_covariance_scale": xldr_scale,
                "central_kernel_dimension": 1,
                "central_decay_eigenvalue": decay,
            }
        )

    # A Gaussian fluctuation prescription based on the positive heavy
    # Hessian also retains an arbitrary overall fluctuation strength T.
    heavy_masses = np.diag(edge_vacuum)[7:]
    cross_masses = heavy_masses[cross_mask]
    gaussian_unit_rate = float(
        np.sum(np.array(coefficients)[cross_mask] / cross_masses)
    )
    gaussian_scale_scan = [
        {
            "fluctuation_strength": strength,
            "induced_central_decay": strength * gaussian_unit_rate,
        }
        for strength in (0.1, 1.0, 10.0)
    ]
    assert abs(gaussian_unit_rate - 35.0 / 96.0) < TOL

    previous = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v8_gauge_twirl_cross_sector_kraus_bridge_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    tome7 = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v7_qualitative_parent_mass_metric_freeze_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert previous["verdict"]["C2_superselection_survives"] is False
    assert tome7["frozen_positive_core"]["stationary_zero_has_seven_negative_modes"]

    result = {
        "date": "2026-08-28",
        "gate": "version8_kraus_bridge_parent_action_hessian_gate",
        "field_dependent_dirichlet_term": {
            "formula": "E_bridge(z)=-<Q,L_z Q>=sum_i d_i z_i^2",
            "cross_direction_coefficient": "7/36",
            "cross_direction_coefficients": rounded(
                np.array(coefficients)[cross_mask]
            ),
            "control_direction_coefficients": rounded(
                np.array(coefficients)[control_mask]
            ),
            "total_unit_covariance_decay": unit_covariance_rate,
            "hessian_signature": signature(bridge_values),
            "interpretation": "positive mass correction on 12 cross-arrow heavy directions",
        },
        "tome7_hessian_compatibility": {
            "tested_real_slice_dimension": 27,
            "positive_bridge_weight_scan": hessian_scan,
            "origin_signature_preserved_for_all_tested_positive_weights": True,
            "target_signature_preserved_for_all_tested_positive_weights": True,
            "bridge_term_launches_cross_arrows": False,
            "reason": "a positive quadratic Dirichlet term raises rather than reverses their heavy masses",
        },
        "vacuum_rate_test": {
            "cross_arrow_vacuum_coordinates": rounded(zero_coordinates),
            "tree_level_bridge_rate": rate_at_vacuum,
            "nonzero_tree_level_process_present": False,
            "second_variation_nonzero": True,
        },
        "covariance_requirement": {
            "unit_isotropic_covariance_decay": unit_covariance_rate,
            "common_scalar_covariance_scan": covariance_scan,
            "independent_family_covariance_scan": family_covariance_scan,
            "qualitative_fixed_algebra_independent_of_positive_scale": True,
            "quantitative_decay_rate_independent_of_scale": False,
            "gauge_symmetry_relates_QLYR_and_XLdR_rates": False,
            "minimum_undetermined_positive_family_scales": 2,
            "common_isotropic_covariance_is_derived": False,
        },
        "gaussian_fluctuation_probe": {
            "prescription": "C_T=T*(H_heavy)^-1 restricted to cross arrows",
            "unit_strength_decay": gaussian_unit_rate,
            "scale_scan": gaussian_scale_scan,
            "overall_fluctuation_strength_derived": False,
        },
        "verdict": {
            "gauge_covariant_kraus_bridge_kinematically_admitted": True,
            "positive_parent_term_preserves_tome7_signatures": True,
            "nonzero_rate_from_existing_classical_vacuum": False,
            "environment_or_quantum_covariance_required": True,
            "unique_rate_derived": False,
            "status": "kinematic_bridge_positive_classical_parent_rate_no_go",
            "next_gate": "version8_cross_arrow_covariance_origin_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()