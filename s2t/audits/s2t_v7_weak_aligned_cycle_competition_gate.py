#!/usr/bin/env python3
"""Exact Gaussian Hessian for the surviving down and weak cycle pairs."""

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigh


NAMES = ["QL", "LL", "uR", "dR", "eR", "XL", "XR", "YL", "YR"]
DIMS = {"QL": 6, "LL": 2, "uR": 3, "dR": 3, "eR": 1,
        "XL": 1, "XR": 1, "YL": 2, "YR": 2}
OFFSETS = {}
TOTAL = 0
for name in NAMES:
    OFFSETS[name] = TOTAL
    TOTAL += DIMS[name]


def edge(target, source, block):
    matrix = np.zeros((TOTAL, TOTAL), dtype=complex)
    i, j = OFFSETS[target], OFFSETS[source]
    matrix[i:i + DIMS[target], j:j + DIMS[source]] = block
    matrix[j:j + DIMS[source], i:i + DIMS[target]] = block.conj().T
    return matrix


def carrier():
    h = np.array([[0.0], [1.0]])
    ht = np.array([[1.0], [0.0]])
    i2, i3 = np.eye(2), np.eye(3)
    roots = [
        edge("uR", "QL", np.kron(i3, ht.T)),
        edge("dR", "QL", np.kron(i3, h.T)),
        edge("eR", "LL", h.T), edge("YR", "LL", i2),
        edge("XR", "XL", np.ones((1, 1))),
        edge("eR", "XL", np.ones((1, 1))), edge("YR", "YL", i2),
    ]
    variables, labels = [], []

    def add_complex(label, target, source, block):
        variables.extend([edge(target, source, block),
                          edge(target, source, 1j * block)])
        labels.extend([label + "_re", label + "_im"])

    for color in range(3):
        unit = np.eye(3)[:, [color]]
        add_complex(f"QLYR_c{color}", "QL", "YR", np.kron(unit, i2))
        add_complex(f"XLdR_c{color}", "dR", "XL", unit)
    down_cut = len(variables)
    for weak in range(2):
        unit = np.eye(2)[[weak], :]
        add_complex(f"LLXR_w{weak}", "XR", "LL", unit)
        add_complex(f"YLeR_w{weak}", "eR", "YL", unit)
    return sum(roots), roots, variables, labels, down_cut


def spectral_hessian(background, variables, t):
    values, vectors = eigh(background)
    fp = -2.0 * t * values * np.exp(-t * values ** 2)
    fpp = (4.0 * t ** 2 * values ** 2 - 2.0 * t) * np.exp(-t * values ** 2)
    divided = np.empty((TOTAL, TOTAL))
    for i, left in enumerate(values):
        for j, right in enumerate(values):
            divided[i, j] = (fpp[i] if abs(left - right) < 1e-11 else
                             (fp[i] - fp[j]) / (left - right))
    rotated = [vectors.conj().T @ item @ vectors for item in variables]
    hessian = np.array([
        [np.real(np.sum(divided * first * second.T)) for second in rotated]
        for first in rotated
    ])
    return hessian, values, vectors, fp


def rounded(values):
    return [float(f"{value:.12g}") for value in values]


def main():
    background, roots, variables, labels, down_cut = carrier()
    benchmarks = {}
    for t in (0.1, 1.0, 10.0):
        hessian, spectrum, vectors, fp = spectral_hessian(background, variables, t)
        down = hessian[:down_cut, :down_cut]
        weak = hessian[down_cut:, down_cut:]
        root_gradient = [float(np.trace(
            (vectors @ np.diag(fp) @ vectors.conj().T) @ root).real)
                         for root in roots]
        benchmarks[str(t)] = {
            "full_signature": [int(np.sum(eigh(hessian, eigvals_only=True) < -1e-10)),
                               int(np.sum(abs(eigh(hessian, eigvals_only=True)) <= 1e-10)),
                               int(np.sum(eigh(hessian, eigvals_only=True) > 1e-10))],
            "down_eigenvalues": rounded(eigh(down, eigvals_only=True)),
            "weak_eigenvalues": rounded(eigh(weak, eigvals_only=True)),
            "down_weak_cross_norm": float(np.max(abs(hessian[:down_cut, down_cut:]))),
            "root_gradient": rounded(root_gradient),
        }

    scan = []
    for t in np.logspace(-4, 2, 401):
        hessian, _, _, _ = spectral_hessian(background, variables, float(t))
        down_min = float(eigh(hessian[:down_cut, :down_cut], eigvals_only=True)[0])
        weak_min = float(eigh(hessian[down_cut:, down_cut:], eigvals_only=True)[0])
        scan.append((float(t), down_min, weak_min))

    assert TOTAL == 21 and len(variables) == 20 and down_cut == 12
    assert all(item[2] < 0.0 for item in scan)
    assert all(data["down_weak_cross_norm"] < 1e-12 for data in benchmarks.values())
    assert all(any(abs(value) > 1e-8 for value in data["root_gradient"])
               for data in benchmarks.values())

    result = {
        "gate": "version7_weak_aligned_cycle_competition_gate",
        "carrier": {"complex_dimension": TOTAL, "heavy_real_dimension": len(variables),
                    "down_real_dimension": down_cut,
                    "weak_real_dimension": len(variables) - down_cut,
                    "background_spectrum": rounded(eigh(background, eigvals_only=True))},
        "method": "Daleckii-Krein divided-difference Hessian of Tr exp(-t Phi^2)",
        "benchmarks": benchmarks,
        "log_scan": {"t_min": 1e-4, "t_max": 100.0, "points": len(scan),
                     "weak_min_always_negative": True,
                     "most_negative_weak_value": min(item[2] for item in scan),
                     "down_has_positive_window": any(item[1] > 0.0 for item in scan)},
        "asymptotics": {"small_t": "negative quadratic term from -t Tr Phi^2",
                        "large_t": "negative kernel-to-P6 bridge contribution tends to zero from below"},
        "verdict": {"exact_gaussian_autonomous_parent_pass": False,
                    "reason": "weak sector retains a negative mode and the singlet background has nonzero root tadpoles",
                    "manual_hodge_plus_gaussian_sum_allowed": False,
                    "status": "exact_gaussian_no_go_common_functional_still_open",
                    "next_gate": "version7_exact_profile_hodge_cycle_unification_gate"},
    }
    out = Path(__file__).resolve().parents[1] / "results" / "s2t_v7_weak_aligned_cycle_competition_gate_results.json"
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(out)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()