#!/usr/bin/env python3
"""Audit one-scale calibration of the Version VII edge Hodge parent."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_single_scale_calibration_closure_gate_results.json"


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def signature(values: np.ndarray, tolerance: float = 1.0e-12) -> dict[str, int]:
    return {
        "negative": int(np.sum(values < -tolerance)),
        "zero": int(np.sum(np.abs(values) <= tolerance)),
        "positive": int(np.sum(values > tolerance)),
    }


def main() -> None:
    hodge = load_result(
        "s2t_v7_edge_grading_hodge_superconnection_parent_gate_results.json"
    )
    field_carrier = load_result(
        "s2t_v7_edge_coherence_field_space_superconnection_gate_results.json"
    )
    projector = load_result(
        "s2t_v7_rooted_cycle_isotypic_edge_projector_gate_results.json"
    )

    selected_count = projector["projector_union"]["selected_rank"]
    unwanted_count = projector["projector_union"]["complement_rank"]
    assert selected_count == 6 and unwanted_count == 5
    assert hodge["single_hodge_action"]["bounded_below"]

    # L = Z/2 sum[(dx)^2+(dy)^2] - kappa V_mu.  The physical quadratic
    # scale is M0^2=kappa*mu^2/Z.  All Hessian eigenvalues below are divided
    # by this common scale.
    origin_dimensionless = np.array(
        [-4.0] * (2 * selected_count) + [4.0] * (2 * unwanted_count)
    )
    vacuum_dimensionless = np.array(
        [8.0] * selected_count
        + [0.0] * selected_count
        + [4.0] * (2 * unwanted_count)
    )
    assert signature(origin_dimensionless) == {
        "negative": 12,
        "zero": 0,
        "positive": 10,
    }
    assert signature(vacuum_dimensionless) == {
        "negative": 0,
        "zero": 6,
        "positive": 16,
    }

    radial_mass_over_m0 = np.sqrt(8.0)
    unwanted_mass_over_m0 = 2.0
    mass_ratio = radial_mass_over_m0 / unwanted_mass_over_m0
    correlation_length_ratio = unwanted_mass_over_m0 / radial_mass_over_m0
    assert abs(mass_ratio - np.sqrt(2.0)) < 1.0e-12

    # Hold M0=sqrt(lambda_eff)*v fixed while varying the unresolved
    # dimensionless kinetic/potential ratio lambda_eff=kappa/Z^2.
    fixed_m0 = 1.0
    lambda_values = np.array([0.25, 1.0, 4.0])
    canonical_vevs = fixed_m0 / np.sqrt(lambda_values)
    radial_masses = np.full(3, radial_mass_over_m0 * fixed_m0)
    unwanted_masses = np.full(3, unwanted_mass_over_m0 * fixed_m0)
    quartic_vertices = lambda_values.copy()
    codimension_one_tension_proxy = canonical_vevs**2 * fixed_m0
    assert np.max(radial_masses) - np.min(radial_masses) < 1.0e-12
    assert np.max(unwanted_masses) - np.min(unwanted_masses) < 1.0e-12
    assert len(set(quartic_vertices.tolist())) == 3
    assert len(set(codimension_one_tension_proxy.tolist())) == 3

    finite_metric_eigenvalues = field_carrier["kinetic_metric"]["eigenvalues"]
    finite_metric = float(finite_metric_eigenvalues[0])
    absolute_kinetic_derived = field_carrier["verdict"][
        "absolute_spacetime_heat_kernel_normalization_closed"
    ]
    assert np.max(np.abs(np.array(finite_metric_eigenvalues) - 3.0)) < 1.0e-12
    assert abs(finite_metric - 3.0) < 1.0e-12
    assert absolute_kinetic_derived is False

    result = {
        "gate": "version7_single_scale_calibration_closure_gate",
        "effective_lagrangian": {
            "formula": "L=Z/2*sum_e |partial z_e|^2-kappa*S_mu(z)",
            "canonical_field": "phi=sqrt(Z)*z",
            "canonical_vacuum_amplitude": "v=sqrt(Z)*mu",
            "effective_quartic": "lambda_eff=kappa/Z^2",
            "single_quadratic_scale": "M0^2=kappa*mu^2/Z=lambda_eff*v^2",
        },
        "linear_spectrum_in_M0_units": {
            "origin_eigenvalues": {
                "minus_4": 12,
                "plus_4": 10,
            },
            "vacuum_eigenvalues": {
                "zero": 6,
                "plus_4": 10,
                "plus_8": 6,
            },
            "origin_signature": signature(origin_dimensionless),
            "vacuum_signature": signature(vacuum_dimensionless),
            "selected_radial_mass_over_M0": float(radial_mass_over_m0),
            "unwanted_mass_over_M0": float(unwanted_mass_over_m0),
            "radial_to_unwanted_mass_ratio": float(mass_ratio),
            "radial_to_unwanted_correlation_length_ratio": float(
                correlation_length_ratio
            ),
            "one_mass_calibration_closes_linear_spectrum": True,
        },
        "fixed_M0_degeneracy": {
            "M0": fixed_m0,
            "lambda_eff_values": lambda_values.tolist(),
            "canonical_v_values": canonical_vevs.tolist(),
            "selected_radial_masses": radial_masses.tolist(),
            "unwanted_masses": unwanted_masses.tolist(),
            "quartic_vertex_proxies": quartic_vertices.tolist(),
            "codimension_one_tension_proxies_v2_M0": (
                codimension_one_tension_proxy.tolist()
            ),
            "linear_spectrum_changes": False,
            "interactions_and_nonlinear_energies_change": True,
        },
        "kinetic_parent_status": {
            "finite_trace_metric_eigenvalue": finite_metric,
            "finite_metric_positive_and_common": True,
            "absolute_heat_kernel_kinetic_coefficient_derived": absolute_kinetic_derived,
            "lambda_eff_fixed_by_current_parent": False,
            "physical_time_normalization_derived": False,
        },
        "verdict": {
            "one_dimensionful_input_suffices_for_internal_linear_masses": True,
            "dimensionless_mass_ratio_sqrt_2_predicted": True,
            "one_input_suffices_for_full_nonlinear_EFT": False,
            "status": "partial_positive_linear_one_scale_full_closure_open",
            "next_gate": "derive or rule out the spacetime kinetic-to-Hodge-potential normalization from one product superconnection heat-kernel coefficient",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()