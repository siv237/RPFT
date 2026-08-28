#!/usr/bin/env python3
"""Test the Casimir-weighted Hodge heat profile against the exact cycle trace."""

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq

from s2t_v7_weak_aligned_cycle_competition_gate import carrier, spectral_hessian


def combined_hessian(t):
    background, roots, variables, labels, down_cut = carrier()
    physical, values, vectors, fp = spectral_hessian(background, variables, t)
    casimir = np.array([1.6] * down_cut + [0.9] * (len(variables) - down_cut))
    hodge = np.diag(8.0 * t * casimir * np.exp(-t * casimir ** 2))
    root_gradient = [float(np.trace(
        (vectors @ np.diag(fp) @ vectors.conj().T) @ root).real)
                     for root in roots]
    return physical + hodge, physical, hodge, root_gradient, labels, down_cut


def minimum(t):
    return float(eigh(combined_hessian(t)[0], eigvals_only=True)[0])


def rounded(values):
    return [float(f"{value:.12g}") for value in values]


def main():
    grid = np.logspace(-4, 2, 601)
    minima = np.array([minimum(float(t)) for t in grid])
    changes = []
    for left, right, f_left, f_right in zip(grid[:-1], grid[1:], minima[:-1], minima[1:]):
        if f_left * f_right < 0:
            changes.append(brentq(minimum, float(left), float(right)))

    benchmarks = {}
    for t in (0.1, 1.0, 2.0, 3.0):
        total, physical, hodge, gradient, labels, down_cut = combined_hessian(t)
        eig = eigh(total, eigvals_only=True)
        benchmarks[str(t)] = {
            "minimum_eigenvalue": float(eig[0]),
            "signature": [int(np.sum(eig < -1e-10)), int(np.sum(abs(eig) <= 1e-10)),
                          int(np.sum(eig > 1e-10))],
            "down_minimum": float(eigh(total[:down_cut, :down_cut], eigvals_only=True)[0]),
            "weak_minimum": float(eigh(total[down_cut:, down_cut:], eigvals_only=True)[0]),
            "physical_minimum": float(eigh(physical, eigvals_only=True)[0]),
            "hodge_diagonal": rounded(np.diag(hodge)),
            "root_gradient": rounded(gradient),
        }

    assert changes and changes[0] > 2.0
    assert benchmarks["1.0"]["signature"] == [0, 0, 20]
    assert benchmarks["3.0"]["signature"][0] > 0
    assert any(abs(value) > 1e-8 for value in benchmarks["1.0"]["root_gradient"])

    result = {
        "gate": "version7_exact_profile_hodge_cycle_unification_gate",
        "formal_single_profile": {
            "functional": "-Tr_edge exp(-t*m_C^2) + Tr_phys exp(-t*Phi^2)",
            "reading": "graded direct-sum trace candidate",
            "same_heat_parameter": True,
            "casimir_eigenvalues": {"weak_doublet_1/2": "9/10",
                                     "down_triplet_2/3": "8/5"},
            "hodge_origin_mass": "8*t*c*exp(-t*c^2) per real component",
        },
        "scan": {"t_min": 1e-4, "t_max": 100.0, "points": len(grid),
                 "positive_window_starts_at_small_t": bool(minima[0] > 0),
                 "first_loss_of_positivity": float(changes[0]),
                 "maximum_minimum_eigenvalue": float(np.max(minima)),
                 "t_at_maximum_margin": float(grid[int(np.argmax(minima))])},
        "benchmarks": benchmarks,
        "verdict": {
            "full_heavy_hessian_positive_in_open_window": True,
            "benchmark_t_1_passes": True,
            "singlet_root_stationary": False,
            "common_physical_superconnection_derived": False,
            "status": "heavy_hessian_partial_pass_common_carrier_and_root_stationarity_open",
            "next_gate": "version7_common_carrier_root_stationarity_gate",
        },
    }
    out = Path(__file__).resolve().parents[1] / "results" / "s2t_v7_exact_profile_hodge_cycle_unification_gate_results.json"
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(out)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()