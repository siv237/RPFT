#!/usr/bin/env python3
"""Solve root stationarity and the full root-heavy Hessian at t=1."""

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import least_squares

from s2t_v7_weak_aligned_cycle_competition_gate import carrier, spectral_hessian


T = 1.0
MULTIPLICITIES = np.array([3.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0])


def physical_gradient(background, roots):
    values, vectors = eigh(background)
    fp = -2.0 * T * values * np.exp(-T * values ** 2)
    derivative = vectors @ np.diag(fp) @ vectors.conj().T
    return np.array([np.trace(derivative @ root).real for root in roots])


def hodge_gradient(amplitudes):
    q = (amplitudes ** 2 - 1.0) ** 2
    return (8.0 * MULTIPLICITIES * T * amplitudes * (amplitudes ** 2 - 1.0)
            * np.exp(-T * q))


def stationarity(amplitudes, roots):
    background = sum(value * root for value, root in zip(amplitudes, roots))
    return physical_gradient(background, roots) + hodge_gradient(amplitudes)


def hodge_root_hessian(amplitudes):
    delta = amplitudes ** 2 - 1.0
    return (8.0 * MULTIPLICITIES * T * np.exp(-T * delta ** 2)
            * ((3.0 * amplitudes ** 2 - 1.0)
               - 4.0 * T * amplitudes ** 2 * delta ** 2))


def rounded(values):
    return [float(f"{value:.12g}") for value in values]


def main():
    _, roots, heavy, labels, down_cut = carrier()
    solution = least_squares(lambda x: stationarity(x, roots), np.ones(7) * 1.05,
                             bounds=(0.01, 4.0), xtol=1e-13, ftol=1e-13,
                             gtol=1e-13, max_nfev=5000)
    amplitudes = solution.x
    background = sum(value * root for value, root in zip(amplitudes, roots))
    all_variations = roots + heavy
    physical, _, _, _ = spectral_hessian(background, all_variations, T)
    casimir = np.array([1.6] * down_cut + [0.9] * (len(heavy) - down_cut))
    hodge_heavy = 8.0 * T * casimir * np.exp(-T * casimir ** 2)
    hodge_diagonal = np.concatenate([hodge_root_hessian(amplitudes), hodge_heavy])
    total = physical + np.diag(hodge_diagonal)
    root_block = total[:7, :7]
    heavy_block = total[7:, 7:]
    full_eigenvalues = eigh(total, eigvals_only=True)
    gradient = stationarity(amplitudes, roots)

    assert solution.success
    assert np.max(abs(gradient)) < 1e-11
    assert full_eigenvalues[0] > 1.0
    assert eigh(root_block, eigvals_only=True)[0] > 0.0
    assert eigh(heavy_block, eigvals_only=True)[0] > 0.0

    result = {
        "gate": "version7_common_carrier_root_stationarity_gate",
        "formal_functional": "-Tr_H15 exp(-m_ch^2) - Tr_edge exp(-m_C^2) + Tr_phys exp(-Phi^2)",
        "common_heat_parameter": T,
        "root_order": ["QLuR", "QLdR", "LLeR", "LLYR", "XLXR", "XLeR", "YLYR"],
        "stationary_root_amplitudes": rounded(amplitudes),
        "maximum_gradient_residual": float(np.max(abs(gradient))),
        "root_hessian_eigenvalues": rounded(eigh(root_block, eigvals_only=True)),
        "heavy_hessian_minimum": float(eigh(heavy_block, eigvals_only=True)[0]),
        "root_heavy_cross_norm": float(np.max(abs(total[:7, 7:]))),
        "full_hessian": {
            "dimension": len(full_eigenvalues),
            "minimum_eigenvalue": float(full_eigenvalues[0]),
            "signature": [int(np.sum(full_eigenvalues < -1e-10)),
                          int(np.sum(abs(full_eigenvalues) <= 1e-10)),
                          int(np.sum(full_eigenvalues > 1e-10))],
            "eigenvalues": rounded(full_eigenvalues),
        },
        "verdict": {
            "root_stationary_solution_exists": True,
            "full_root_heavy_hessian_positive": True,
            "formal_one_profile_local_vacuum_pass": True,
            "single_real_superconnection_derived": False,
            "status": "formal_local_vacuum_pass_real_superconnection_origin_open",
            "next_gate": "version7_real_superconnection_common_trace_origin_gate",
        },
    }
    out = Path(__file__).resolve().parents[1] / "results" / "s2t_v7_common_carrier_root_stationarity_gate_results.json"
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(out)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()