#!/usr/bin/env python3
"""Континуальная внутренняя щель полного стационарного вихря."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit


ROOT = Path(__file__).resolve().parents[2]
CALIBRATION_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_full_tensor_translation_calibration_gate.py"
TAIL_RESULT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_tensor_high_angular_coercivity_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_tensor_internal_gap_gate_results.json"


def main() -> None:
    calibration = runpy.run_path(str(CALIBRATION_AUDIT))
    module = calibration["load_calibrated_module"]()
    model = module["setup_model"]()
    tail = json.loads(TAIL_RESULT.read_text(encoding="utf-8"))

    node_counts = [70, 100, 140, 200, 280, 400, 560]
    blocks = {
        "critical_plus": (1, 1),
        "critical_minus": (-1, -1),
        "nearest_plus": (1, 0),
        "nearest_minus": (-1, 0),
        "former_candidate_plus": (1, -1),
        "former_candidate_minus": (-1, 1),
        "neutral_axisymmetric": (0, 0),
    }
    convergence = {}
    for nodes in node_counts:
        prepared = module["prepare_grid"](model, nodes)
        convergence[str(nodes)] = {
            name: {
                "character": character,
                "integer_label": label,
                **module["block_spectrum"](
                    model, prepared, character, label, eigen_count=3
                ),
            }
            for name, (character, label) in blocks.items()
        }

    fit_nodes = np.array([200.0, 280.0, 400.0, 560.0])
    fit_variable = 1.0 / (fit_nodes - 1.0) ** 2

    def values(name, level=0):
        return np.array([
            convergence[str(int(nodes))][name]["eigenvalues"][level]
            for nodes in fit_nodes
        ])

    critical_values = values("critical_plus")
    nearest_values = values("nearest_plus")
    former_values = values("former_candidate_plus")
    second_critical_values = values("critical_plus", level=1)
    critical_fit = np.polyfit(fit_variable, critical_values, 1)
    nearest_fit = np.polyfit(fit_variable, nearest_values, 1)
    former_fit = np.polyfit(fit_variable, former_values, 1)
    second_fit = np.polyfit(fit_variable, second_critical_values, 1)
    critical_limit = float(critical_fit[1])
    nearest_limit = float(nearest_fit[1])
    former_limit = float(former_fit[1])
    second_critical_limit = float(second_fit[1])

    all_nodes = np.array(node_counts, dtype=float)
    all_critical = np.array([
        convergence[str(nodes)]["critical_plus"]["eigenvalues"][0]
        for nodes in node_counts
    ])

    def power_law(nodes, limit, amplitude, order):
        return limit + amplitude / (nodes - 1.0) ** order

    nonlinear_fit, _ = curve_fit(
        power_law,
        all_nodes[3:],
        all_critical[3:],
        p0=[critical_limit, -3.6, 2.0],
        maxfev=20000,
    )
    maximum_conjugacy_residual = max(
        abs(
            convergence[str(nodes)]["critical_plus"]["eigenvalues"][level]
            - convergence[str(nodes)]["critical_minus"]["eigenvalues"][level]
        )
        for nodes in node_counts for level in range(3)
    )
    maximum_hermiticity_residual = max(
        row["hermiticity_residual"]
        for nodes in convergence.values() for row in nodes.values()
    )
    fit_residual = float(np.max(np.abs(
        np.polyval(critical_fit, fit_variable) - critical_values
    )))

    result = {
        "gate": "version6_bosonic_defect_full_tensor_internal_gap_gate",
        "parent_tail_certificate": {
            "gate": tail["gate"],
            "all_integer_angular_labels_covered": tail[
                "global_full_tensor_operator"
            ]["all_integer_angular_labels_covered"],
            "negative_internal_mode_found": tail[
                "global_full_tensor_operator"
            ]["negative_internal_mode_found"],
        },
        "operator": {
            "stationary_four_profile_background": True,
            "calibrated_background_gauge": True,
            "node_counts": node_counts,
            "tracked_blocks": blocks,
            "eigenvalues_per_block": 3,
        },
        "convergence": convergence,
        "continuum_fit": {
            "fit_node_counts": fit_nodes.astype(int).tolist(),
            "fit_variable": "1/(N-1)^2",
            "critical_internal_gap": critical_limit,
            "nearest_competitor_limit": nearest_limit,
            "former_candidate_limit": former_limit,
            "second_level_same_block_limit": second_critical_limit,
            "separation_from_nearest_competitor": nearest_limit - critical_limit,
            "separation_from_second_same_block_level": second_critical_limit - critical_limit,
            "critical_fit_maximum_residual": fit_residual,
            "critical_drift_400_to_560": float(abs(
                convergence["560"]["critical_plus"]["eigenvalues"][0]
                - convergence["400"]["critical_plus"]["eigenvalues"][0]
            )),
            "nonlinear_power_fit_limit": float(nonlinear_fit[0]),
            "nonlinear_power_fit_amplitude": float(nonlinear_fit[1]),
            "nonlinear_power_fit_order": float(nonlinear_fit[2]),
        },
        "symmetry_checks": {
            "maximum_critical_conjugacy_residual": maximum_conjugacy_residual,
            "maximum_hermiticity_residual": maximum_hermiticity_residual,
        },
        "verdict": {
            "translation_pair_excluded": True,
            "global_internal_gap_strictly_positive": bool(critical_limit > 3.0),
            "critical_block_isolated_from_nearest_competitor": bool(
                nearest_limit - critical_limit > 0.04
            ),
            "full_transverse_linear_stability_closed": True,
            "closed_loop_stability_checked": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_curved_string_effective_action_gate",
        },
    }

    assert result["parent_tail_certificate"]["all_integer_angular_labels_covered"]
    assert not result["parent_tail_certificate"]["negative_internal_mode_found"]
    assert result["verdict"]["global_internal_gap_strictly_positive"]
    assert result["verdict"]["critical_block_isolated_from_nearest_competitor"]
    assert 1.9 < result["continuum_fit"]["nonlinear_power_fit_order"] < 2.1
    assert fit_residual < 1.0e-7
    assert maximum_conjugacy_residual < 1.0e-10
    assert maximum_hermiticity_residual < 1.0e-10
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(OUT)


if __name__ == "__main__":
    main()