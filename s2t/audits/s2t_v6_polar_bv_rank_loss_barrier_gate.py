#!/usr/bin/env python3
"""Audit the polar/BV Jacobian and logarithmic rank-loss barrier no-go."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.special import exp1


def effective_free_energy(probabilities: np.ndarray, nu: float) -> np.ndarray:
    """Reduced state free energy, up to an irrelevant additive constant."""
    p = np.asarray(probabilities, dtype=float)
    entropy = np.sum(p * np.log(p), axis=-1)
    classical = (6.0 / 7.0) * (np.sum(p * p, axis=-1) - 1.0 / 3.0)
    one_loop = 0.5 * (
        np.sum(np.log(p), axis=-1)
        + np.log(p[..., 0] + p[..., 1])
        + np.log(p[..., 0] + p[..., 2])
        + np.log(p[..., 1] + p[..., 2])
    )
    barrier = -nu * np.sum(np.log(p), axis=-1)
    return entropy + classical + one_loop + barrier


def main() -> None:
    local_base_curvature = Fraction(-51, 112)
    barrier_curvature_per_nu = Fraction(9, 2)
    local_instability_upper_bound = -local_base_curvature / barrier_curvature_per_nu
    pure_vertex_barrier_lower_bound = Fraction(0, 1)

    induced_measures = []
    for environment_dimension in range(3, 16):
        nu = Fraction(environment_dimension - 4, 2)
        local_curvature = local_base_curvature + barrier_curvature_per_nu * nu
        induced_measures.append(
            {
                "K": environment_dimension,
                "nu": float(nu),
                "nu_exact": str(nu),
                "local_curvature": float(local_curvature),
                "local_curvature_exact": str(local_curvature),
                "isotropic_locally_unstable": local_curvature < 0,
                "pure_vertex_suppressed": nu > pure_vertex_barrier_lower_bound,
            }
        )

    grid_size = 1200
    coordinates = np.arange(1, grid_size, dtype=float) / grid_size
    first, second = np.meshgrid(coordinates, coordinates, indexing="ij")
    interior = first + second < 1.0
    simplex = np.stack(
        [first[interior], second[interior], 1.0 - first[interior] - second[interior]],
        axis=1,
    )
    scan = {}
    for nu in (0.0, 0.5, 1.0, 5.5):
        values = effective_free_energy(simplex, nu)
        location = int(np.argmin(values))
        isotropic = np.array([1.0 / 3.0] * 3)
        scan[str(nu)] = {
            "minimum_spectrum": [float(value) for value in simplex[location]],
            "minimum_value": float(values[location]),
            "isotropic_value": float(effective_free_energy(isotropic, nu)),
        }

    svd_radial_power = 3
    transverse_gaussian_power = -4
    residual_power = svd_radial_power + transverse_gaussian_power

    epsilons = np.logspace(-2, -12, 11)
    regulated_integrals = 0.25 * exp1(epsilons)
    asymptotic_ratios = regulated_integrals / np.log(1.0 / epsilons)

    result = {
        "gate": "version6_polar_bv_rank_loss_barrier_gate",
        "polar_svd_measure": {
            "matrix_space": "M2(R)",
            "jacobian": "abs(s1^2-s2^2)",
            "radial_power": svd_radial_power,
            "transverse_gaussian_power": transverse_gaussian_power,
            "residual_power": residual_power,
            "residual_integral": "integral dt/t",
            "compact_orbit_quotient_changes_power": False,
        },
        "logdet_no_go": {
            "base_local_curvature": float(local_base_curvature),
            "base_local_curvature_exact": str(local_base_curvature),
            "barrier_curvature_per_nu": float(barrier_curvature_per_nu),
            "barrier_curvature_per_nu_exact": str(barrier_curvature_per_nu),
            "local_instability_requires_nu_below": float(local_instability_upper_bound),
            "local_instability_bound_exact": str(local_instability_upper_bound),
            "nonperturbative_boundary_partition_growth": "log(1/epsilon)",
            "regulated_radial_integral": {
                "epsilon": [float(value) for value in epsilons],
                "one_quarter_E1": [float(value) for value in regulated_integrals],
                "ratio_to_log_inverse_epsilon": [
                    float(value) for value in asymptotic_ratios
                ],
                "expected_ratio_limit": 0.25,
            },
            "pure_vertex_suppression_requires_nu_above": 0.0,
            "pure_vertex_bound_exact": "0",
            "compatible_interval": "0 < nu < 17/168",
            "compatible_interval_exists": True,
        },
        "real_induced_measure": {
            "density": "det(R)^((K-4)/2)",
            "barrier_coefficient": "nu_K=(K-4)/2",
            "integer_K_audit": induced_measures,
            "K5_positive_carrier_derived_in_project": False,
            "K5_status": "virtual rank 20-15, not a canonical purification carrier",
        },
        "simplex_control_scan": scan,
        "verdict": {
            "polar_or_standard_bv_saturates_flat_valley": False,
            "standard_polar_or_integer_Wishart_barrier_works": False,
            "fractional_logdet_window_remains_open": True,
            "matter_birth_proved": False,
            "next_gate": "version6_fractional_determinant_measure_origin_gate",
        },
    }

    assert residual_power == -1
    assert local_instability_upper_bound == Fraction(17, 168)
    assert pure_vertex_barrier_lower_bound < local_instability_upper_bound
    assert abs(asymptotic_ratios[-1] - 0.25) < 0.01
    assert not any(
        item["isotropic_locally_unstable"] and item["pure_vertex_suppressed"]
        for item in induced_measures
    )

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_polar_bv_rank_loss_barrier_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()