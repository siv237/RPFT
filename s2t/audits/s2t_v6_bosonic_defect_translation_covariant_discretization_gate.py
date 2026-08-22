#!/usr/bin/env python3
"""Ковариантное отделение переносов от внутреннего спектра вихря."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
PARENT = ROOT / "s2t/results/s2t_v6_bosonic_defect_corrected_vortex_negative_mode_nonlinear_saturation_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_translation_covariant_discretization_gate_results.json"


def main() -> None:
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    relaxations = parent["center_pinned_discrete_stationary_vortices"]

    grids = np.array(sorted(int(grid) for grid in relaxations), dtype=int)
    spacing = np.array([relaxations[str(grid)]["spacing"] for grid in grids])
    lowest = np.array([
        relaxations[str(grid)]["relaxed_hessian_eigenvalues"][0]
        for grid in grids
    ])
    negative_counts = np.array([
        relaxations[str(grid)]["relaxed_negative_mode_count"]
        for grid in grids
    ])
    gradient_rms = np.array([
        relaxations[str(grid)]["projected_gradient_rms"]
        for grid in grids
    ])

    # В непрерывной записи Phi_X(x)=Phi_0(x-X) энергия не зависит от X.
    # Поэтому в координатах (X,Y,xi_internal) переносный блок гессиана
    # тождественно нулевой. Численные уровни закреплённой сетки нельзя
    # использовать как оценку массы переносов или как внутренний зазор.
    collective_translation_block = np.zeros((2, 2))
    representative_internal_block = np.diag(
        relaxations[str(grids[-1])]["relaxed_hessian_eigenvalues"]
    )
    extended_hessian = np.block([
        [collective_translation_block, np.zeros((2, representative_internal_block.shape[0]))],
        [np.zeros((representative_internal_block.shape[0], 2)), representative_internal_block],
    ])
    extended_spectrum = np.linalg.eigvalsh(extended_hessian)

    last_ratio = float(lowest[-1] / lowest[-2])
    result = {
        "gate": "version6_bosonic_defect_translation_covariant_discretization_gate",
        "input": {
            "parent_gate": parent["gate"],
            "grids": grids.tolist(),
            "spacings": spacing.tolist(),
            "center_pinned_lowest_eigenvalues": lowest.tolist(),
            "negative_mode_counts": negative_counts.tolist(),
            "maximum_projected_gradient_rms": float(np.max(gradient_rms)),
        },
        "collective_coordinate_completion": {
            "coordinates": ["X", "Y"],
            "field_family": "Phi_X(x)=Phi_0(x-X)",
            "translation_hessian_block": collective_translation_block.tolist(),
            "translation_zero_mode_count": 2,
            "mixed_translation_internal_block": "zero by translation invariance at a stationary solution",
            "representative_extended_spectrum_grid_41": extended_spectrum.tolist(),
        },
        "refinement_diagnostic": {
            "lowest_level_ratio_grid_41_over_33": last_ratio,
            "lowest_center_pinned_level_decreases_under_last_refinement": bool(lowest[-1] < lowest[-2]),
            "strict_positive_internal_gap_certified": False,
            "reason": "the center constraint removes translations but the lowest residual level still softens with refinement",
        },
        "verdict": {
            "translation_modes_exactly_restored_as_collective_zero_modes": True,
            "peierls_nabarro_level_is_physical_mass": False,
            "negative_mode_found_after_centered_stationarization": False,
            "effective_internal_operator_nonnegative_on_checked_grids": True,
            "continuum_internal_gap_closed": False,
            "full_spin2_spin3_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_centered_angular_channel_decomposition_gate",
        },
    }

    assert np.all(negative_counts == 0)
    assert np.max(gradient_rms) < 1.0e-6
    assert np.count_nonzero(np.abs(extended_spectrum) < 1.0e-14) == 2
    assert np.all(extended_spectrum[2:] > 0.0)
    assert lowest[-1] < lowest[-2]
    assert not result["verdict"]["continuum_internal_gap_closed"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()