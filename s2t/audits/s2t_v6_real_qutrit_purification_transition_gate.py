#!/usr/bin/env python3
"""Audit the real three-level entropy/alignment transition."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def entropy(probabilities: np.ndarray) -> float:
    positive = probabilities[probabilities > 0.0]
    return float(np.sum(positive * np.log(positive)))


def free_energy(probabilities: np.ndarray, kappa: float) -> float:
    return entropy(probabilities) - kappa * (
        float(probabilities @ probabilities) - 1.0 / 3.0
    )


def uniaxial_probabilities(x: float) -> np.ndarray:
    return np.array([x, (1.0 - x) / 2.0, (1.0 - x) / 2.0])


def main() -> None:
    r4_plus = np.array(
        [[13.5, -2.0, 1.5], [-2.0, 17.5, -2.5], [1.5, -2.5, 17.0]]
    )
    r4_eigenvalues = np.linalg.eigvalsh(r4_plus)
    betas = [0.0, 0.1, 1.0, 10.0]
    gibbs_spectra = {}
    for beta in betas:
        weights = np.exp(-beta * (r4_eigenvalues - np.min(r4_eigenvalues)))
        weights /= np.sum(weights)
        gibbs_spectra[str(beta)] = [float(value) for value in weights[::-1]]

    kappa_critical = float(np.log(4.0))
    isotropic = np.ones(3) / 3.0
    ordered = uniaxial_probabilities(2.0 / 3.0)
    coexistence_residual = abs(
        free_energy(isotropic, kappa_critical)
        - free_energy(ordered, kappa_critical)
    )
    stationarity_residual = abs(
        np.log(2.0 * (2.0 / 3.0) / (1.0 - 2.0 / 3.0))
        - kappa_critical * (3.0 * (2.0 / 3.0) - 1.0)
    )
    isotropic_curvature = 4.5 - 3.0 * kappa_critical
    ordered_curvature = (
        1.0 / (2.0 / 3.0)
        + 1.0 / (1.0 - 2.0 / 3.0)
        - 3.0 * kappa_critical
    )

    grid = np.linspace(1.0 / 3.0, 0.999999, 200001)
    phase_scan = {}
    for kappa in (1.0, kappa_critical, 1.45, 1.5, 2.0):
        values = np.array(
            [free_energy(uniaxial_probabilities(float(x)), kappa) for x in grid]
        )
        minimum = float(grid[int(np.argmin(values))])
        phase_scan[f"{kappa:.12g}"] = {
            "global_uniaxial_x": minimum,
            "global_energy": float(np.min(values)),
            "isotropic_energy": free_energy(isotropic, kappa),
        }

    # Independent full-simplex scan: do not assume uniaxiality numerically.
    full_simplex_scan = {}
    simplex_resolution = 801
    for kappa in (kappa_critical, 1.45, 2.0):
        best_energy = float("inf")
        best_spectrum: list[float] | None = None
        for first_index in range(1, simplex_resolution):
            first = first_index / simplex_resolution
            second = np.arange(1, simplex_resolution - first_index) / simplex_resolution
            if second.size == 0:
                continue
            third = 1.0 - first - second
            values = (
                first * np.log(first)
                + second * np.log(second)
                + third * np.log(third)
                - kappa * (first**2 + second**2 + third**2 - 1.0 / 3.0)
            )
            location = int(np.argmin(values))
            if float(values[location]) < best_energy:
                best_energy = float(values[location])
                best_spectrum = sorted(
                    [first, float(second[location]), float(third[location])],
                    reverse=True,
                )
        assert best_spectrum is not None
        full_simplex_scan[f"{kappa:.12g}"] = {
            "minimum_spectrum_descending": best_spectrum,
            "minimum_energy": best_energy,
            "transverse_pair_splitting": abs(best_spectrum[1] - best_spectrum[2]),
        }

    result = {
        "gate": "version6_real_qutrit_purification_transition_gate",
        "existing_linear_gibbs_test": {
            "R4_plus_eigenvalues": [float(value) for value in r4_eigenvalues],
            "R4_plus_ground_is_nondegenerate": True,
            "finite_beta_gibbs_spectra_descending": gibbs_spectra,
            "finite_beta_phase_transition": False,
            "SO3_invariant_linear_H_gives": "I3/3",
            "nonscalar_linear_H_gives": "explicit_fixed_axis",
            "RP2_vacuum_orbit_generated": False,
        },
        "minimal_nonlinear_control": {
            "functional": "Tr(R log R)-kappa*(Tr(R^2)-1/3)",
            "critical_kappa": kappa_critical,
            "critical_kappa_exact": "log(4)",
            "isotropic_spectrum": [1.0 / 3.0] * 3,
            "ordered_coexistence_spectrum": [2.0 / 3.0, 1.0 / 6.0, 1.0 / 6.0],
            "coexistence_energy_residual": coexistence_residual,
            "ordered_stationarity_residual": stationarity_residual,
            "isotropic_local_curvature_at_transition": isotropic_curvature,
            "ordered_local_curvature_at_transition": ordered_curvature,
            "isotropic_spinodal_kappa": 1.5,
            "transition_order": "first_order",
            "ordered_orbit": "SO3/O2=RP2",
            "phase_scan": phase_scan,
            "full_simplex_scan": full_simplex_scan,
        },
        "project_source_audit": {
            "linear_family_state_term_supplies_negative_purity": False,
            "TOE65_fluctuation_term_computed": False,
            "closure_deficit_response_is_prior_state_selector": False,
            "bridge_positive_square_favors_defect": False,
            "formal_one_seventh_exceeds_log4": False,
            "kappa_sign_and_normalization_derived": False,
        },
        "verdict": {
            "exact_RP2_transition_mechanism_found": True,
            "mechanism_derived_from_current_parent": False,
            "full_purification_needed": False,
            "next_gate": "version6_exchange_bridge_induced_alignment_gate",
        },
    }

    assert np.min(np.diff(r4_eigenvalues)) > 1.0e-6
    assert coexistence_residual < 1.0e-12
    assert stationarity_residual < 1.0e-12
    assert isotropic_curvature > 0.0
    assert ordered_curvature > 0.0
    assert 1.0 / 7.0 < kappa_critical < 1.5
    assert abs(phase_scan["1"]["global_uniaxial_x"] - 1.0 / 3.0) < 1.0e-5
    assert phase_scan["2"]["global_uniaxial_x"] > 2.0 / 3.0
    assert full_simplex_scan["1.45"]["transverse_pair_splitting"] < 2.0 / simplex_resolution
    assert full_simplex_scan["2"]["transverse_pair_splitting"] < 2.0 / simplex_resolution

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_real_qutrit_purification_transition_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()