#!/usr/bin/env python3
"""Аудит локализации смены ранга нейтринной опоры на вихревом фоне."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_rank_change_localization_gate_results.json"


def potential(s: float, t: float, k: float) -> float:
    """Зависящая от s=|H|^2 часть с необязательным core-suppressor 3 k s."""
    return 6.0 * s * s - (2.0 * t + 6.0 - 3.0 * k) * s


def stationary_s(t: float, k: float) -> float:
    return max(0.0, t / 6.0 + 0.5 - k / 4.0)


def main() -> None:
    parent = json.loads(
        (RESULTS / "s2t_v6_bosonic_defect_mass_portal_parent_gate_results.json").read_text()
    )
    neutrino = json.loads(
        (RESULTS / "s2t_v6_spectral_transition_neutrino_line_parent_gate_results.json").read_text()
    )

    t_grid = np.linspace(0.0, 3.0, 301)
    k_grid = np.linspace(0.0, 1.0, 101)
    values = np.array([[stationary_s(t, k) for k in k_grid] for t in t_grid])

    finite_difference_residual = 0.0
    minimum_test_residual = 0.0
    for t, k in ((0.0, 0.0), (0.0, 1.0), (0.7, 0.0), (1.4, 1.0), (3.0, 0.4)):
        s = stationary_s(t, k)
        h = 1.0e-6
        derivative = (potential(s + h, t, k) - potential(s - h, t, k)) / (2.0 * h)
        finite_difference_residual = max(finite_difference_residual, abs(derivative))
        scan = np.linspace(0.0, max(2.0, s + 1.0), 20001)
        scan_min = scan[int(np.argmin([potential(x, t, k) for x in scan]))]
        minimum_test_residual = max(minimum_test_residual, abs(scan_min - s))

    current_parent_minimum = float(min(stationary_s(t, 0.0) for t in t_grid))
    optimistic_minimum = float(values.min())
    critical_k_at_t0 = 2.0
    critical_k_formula_samples = [2.0 + 2.0 * t / 3.0 for t in (0.0, 0.5, 1.0, 3.0)]

    result = {
        "gate": "version6_spectral_transition_rank_change_localization_gate",
        "input_certificates": {
            "M300_radial_Higgs_coupling_exists": parent["higgs_portal_test"]["radial_amplitude_H2_coupling_exists"],
            "Q_shape_Higgs_portal_coefficient": parent["higgs_portal_test"]["Tr_Q2_H2_coefficient_in_minimal_M300_parent"],
            "regular_rank_changing_support_exists": neutrino["verdict"]["polynomial_neutrino_transition_support_exists"],
        },
        "pointwise_model": {
            "variable": "s=|H|^2",
            "current_parent_s_dependent_potential": "6 s^2-(2 T+6) s",
            "optimistic_test_extension": "+3 k s, 0<=k<=1",
            "stationary_minimizer": "max(0,T/6+1/2-k/4)",
            "radial_amplitude_domain": "T>=0",
            "current_parent_k": 0.0,
        },
        "localization_audit": {
            "minimum_s_current_parent_for_T_ge_0": current_parent_minimum,
            "minimum_s_with_unit_strength_optimistic_suppressor": optimistic_minimum,
            "critical_k_formula": "k_crit(T)=2+(2/3)T",
            "critical_k_at_T_zero": critical_k_at_t0,
            "critical_k_samples": critical_k_formula_samples,
            "H_zero_reached_in_current_parent": False,
            "H_zero_reached_for_0_le_k_le_1": False,
            "W_nu_rank_in_vortex_core_current_parent": 1,
            "localized_rank_change_0_to_1": False,
        },
        "numerical_checks": {
            "finite_difference_stationarity_residual": finite_difference_residual,
            "grid_minimizer_residual": minimum_test_residual,
            "sampled_T_count": len(t_grid),
            "sampled_k_count": len(k_grid),
        },
        "interpretation": {
            "radial_coupling_effect": "positive T raises rather than suppresses the Higgs norm",
            "shape_portal_available": False,
            "unit_suppressor_is_part_of_current_parent": False,
            "missing_structure": "a representation-compatible connector or a derived core term with strength k>=k_crit(T)",
        },
        "verdict": {
            "existing_radial_bridge_localizes_H_zero": False,
            "existing_vortex_localizes_neutrino_rank_change": False,
            "hidden_shape_portal_found": False,
            "physical_closure": False,
            "status": "the M300 radial term keeps |H|^2 strictly positive; even an optimistic unit core penalty cannot reach H=0, so the rank-changing support is not localized by the current vortex",
        },
        "next_gate": "version6_spectral_transition_radial_bridge_vortex_connector_gate",
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()