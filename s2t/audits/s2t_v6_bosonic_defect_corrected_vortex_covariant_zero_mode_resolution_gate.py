#!/usr/bin/env python3
"""Ковариантная фиксация калибровки и отрицательная мода исправленного вихря."""

from __future__ import annotations

import json
import math
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PARENT_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_corrected_vortex_nonradial_stability_gate.py"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_corrected_vortex_covariant_zero_mode_resolution_gate_results.json"


def main() -> None:
    parent = runpy.run_path(str(PARENT_AUDIT))
    solution, derivative_a, derivative_b = parent["corrected_profile"]()
    calculate = parent["calculate"]

    grid_sizes = [24, 32, 40, 48]
    convergence = {
        str(grid): calculate(
            solution, derivative_a, derivative_b, grid,
            box_radius=10.0, eigen_count=4, gauge_sign=-1.0,
        )
        for grid in grid_sizes
    }
    boundary_checks = {
        str(radius): calculate(
            solution, derivative_a, derivative_b, 40,
            box_radius=radius, eigen_count=2, gauge_sign=-1.0,
        )
        for radius in [8.0, 12.0]
    }

    minima = {grid: data["eigenvalues"][0] for grid, data in convergence.items()}
    finest = convergence["48"]
    finest_minimum = finest["eigenvalues"][0]
    finest_weights = finest["mode_block_weights"][0]
    boundary_minima = {radius: data["eigenvalues"][0] for radius, data in boundary_checks.items()}
    critical_wave_number = math.sqrt(-finest_minimum)

    result = {
        "gate": "version6_bosonic_defect_corrected_vortex_covariant_zero_mode_resolution_gate",
        "gauge_sign_audit": {
            "covariant_derivative": "D_i phi=partial_i phi-A_i J phi",
            "gauge_condition": "div(delta A)-(A/G)(J phi0).delta phi=0",
            "faddeev_popov_principal_form": "-Delta+(A/G)|phi0|^2",
            "previous_plus_sign_has_elliptic_positive_mass_term": False,
            "corrected_minus_sign_has_elliptic_positive_mass_term": True,
            "gauge_fixing_quadratic_form_is_nonnegative": True,
        },
        "grid_convergence": convergence,
        "boundary_checks_at_grid_40": boundary_checks,
        "negative_mode": {
            "lowest_eigenvalue_by_grid": minima,
            "finest_lowest_eigenvalue": finest_minimum,
            "drift_40_to_48": abs(minima["48"] - minima["40"]),
            "boundary_lowest_eigenvalues": boundary_minima,
            "finest_mode_block_weights": finest_weights,
            "isolated_from_next_mode": finest["eigenvalues"][1] > 0.0,
            "longitudinal_dispersion": "lambda(k_z)=lambda(0)+k_z^2",
            "unstable_longitudinal_band_abs_kz_below": critical_wave_number,
        },
        "interpretation_boundary": {
            "negative_mode_is_created_by_positive_gauge_fixing_term": False,
            "nonlinear_endpoint_computed": False,
            "endpoint_is_hopf_loop": False,
            "full_spin2_spin3_operator_checked": False,
            "matter_birth_closed": False,
        },
        "verdict": {
            "straight_corrected_vortex_is_linearly_unstable_in_effective_sector": True,
            "previous_soft_cluster_is_consistent_with_residual_gauge_contamination": True,
            "next_gate": "version6_bosonic_defect_corrected_vortex_negative_mode_nonlinear_saturation_gate",
        },
    }

    assert minima["32"] < -0.05
    assert minima["40"] < -0.15
    assert minima["48"] < -0.15
    assert result["negative_mode"]["drift_40_to_48"] < 0.03
    assert all(value < -0.1 for value in boundary_minima.values())
    assert 0.4 < finest_weights["charged_scalar"] < 0.6
    assert 0.4 < finest_weights["gauge_field"] < 0.6
    assert result["negative_mode"]["isolated_from_next_mode"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()