#!/usr/bin/env python3
"""Радиальный гессиан трёхпрофильного Z3-вихря."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh


ROOT = Path(__file__).resolve().parents[2]
PROFILE_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_defect_profile_gate.py"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_q_tetrahedral_vortex_radial_stability_gate_results.json"


def main() -> None:
    module = runpy.run_path(str(PROFILE_AUDIT))
    solution = module["solve_profile"]()
    A, B, C, G = module["A"], module["B"], module["C"], module["G"]
    polynomial = module["POLYNOMIAL"]

    def second_a(a, b):
        return sum(v * i * (i - 1) * a ** (i - 2) * b**j for (i, j), v in polynomial.items() if i >= 2)
    def second_b(a, b):
        return sum(v * j * (j - 1) * a**i * b ** (j - 2) for (i, j), v in polynomial.items() if j >= 2)
    def mixed_ab(a, b):
        return sum(v * i * j * a ** (i - 1) * b ** (j - 1) for (i, j), v in polynomial.items() if i and j)

    def spectrum(node_count: int):
        x = np.linspace(0.0, 1.0, node_count)
        radius = 1.0e-4 + (20.0 - 1.0e-4) * x**1.3
        k, a, b = solution.sol(radius)[[0, 2, 4]]
        dimension = 3 * node_count
        hessian = lil_matrix((dimension, dimension))
        metric = lil_matrix((dimension, dimension))
        for element in range(node_count - 1):
            left, right = radius[element], radius[element + 1]
            width = right - left; middle = 0.5 * (left + right)
            km = 0.5 * (k[element] + k[element + 1])
            am = 0.5 * (a[element] + a[element + 1])
            bm = 0.5 * (b[element] + b[element + 1])
            derivative = np.array([[1.0, -1.0], [-1.0, 1.0]]) / width
            mass = width * np.array([[2.0, 1.0], [1.0, 2.0]]) / 6.0
            diagonal = [
                (G / middle, C * am**2 / middle, G / middle),
                (A * middle, C * (1.0 - km) ** 2 / middle + middle * second_a(am, bm), A * middle),
                (B * middle, middle * second_b(am, bm), B * middle),
            ]
            for field, (stiffness, potential, weight) in enumerate(diagonal):
                indices = [field * node_count + element, field * node_count + element + 1]
                local_hessian = stiffness * derivative + potential * mass
                local_metric = weight * mass
                for i in range(2):
                    for j in range(2):
                        hessian[indices[i], indices[j]] += local_hessian[i, j]
                        metric[indices[i], indices[j]] += local_metric[i, j]
            for first, second, coupling in [
                (0, 1, -2.0 * C * am * (1.0 - km) / middle),
                (1, 2, middle * mixed_ab(am, bm)),
            ]:
                left_indices = [first * node_count + element, first * node_count + element + 1]
                right_indices = [second * node_count + element, second * node_count + element + 1]
                local = coupling * mass
                for i in range(2):
                    for j in range(2):
                        hessian[left_indices[i], right_indices[j]] += local[i, j]
                        hessian[right_indices[j], left_indices[i]] += local[i, j]

        # Dirichlet: delta K=delta a=0 at both ends, delta b=0 at infinity.
        # The core condition delta b'(0)=0 is the natural finite-element boundary condition.
        fixed = {0, node_count - 1, node_count, 2 * node_count - 1, 3 * node_count - 1}
        keep = np.array([index for index in range(dimension) if index not in fixed])
        hessian = hessian.tocsr()[keep][:, keep]
        metric = metric.tocsr()[keep][:, keep]
        eigenvalues = np.sort(eigsh(hessian, k=8, M=metric, sigma=0.0, which="LM", return_eigenvectors=False))
        return eigenvalues

    convergence = {str(n): spectrum(n).tolist() for n in [100, 160, 240, 360, 500]}
    finest = np.array(convergence["500"])
    result = {
        "gate": "version6_bosonic_defect_q_tetrahedral_vortex_radial_stability_gate",
        "operator": {
            "sector": "axisymmetric coupled fluctuations delta K, delta a, delta b",
            "gauge_and_scalar_metric_included": True,
            "finite_element_node_counts": [100, 160, 240, 360, 500],
            "lowest_eigenvalue_convergence": {n: values[0] for n, values in convergence.items()},
            "finest_eigenvalues": finest.tolist(),
        },
        "stability": {
            "negative_mode_count_checked": int(np.sum(finest < -1.0e-6)),
            "zero_mode_count_checked": int(np.sum(np.abs(finest) < 1.0e-6)),
            "positive_checked_mode_count": int(np.sum(finest > 1.0e-6)),
            "minimum_eigenvalue": float(finest[0]),
            "minimum_grid_drift_360_to_500": float(abs(np.array(convergence["360"])[0] - finest[0])),
        },
        "boundary": {
            "nonaxisymmetric_angular_sectors_checked": False,
            "longitudinal_wave_numbers_checked": False,
            "full_gauge_fixed_hessian_checked": False,
            "absolute_scale_derived": False,
        },
        "verdict": {
            "axisymmetric_radial_stability_passes": True,
            "full_vortex_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_q_tetrahedral_vortex_angular_stability_gate",
        },
    }
    assert result["stability"]["negative_mode_count_checked"] == 0
    assert result["stability"]["zero_mode_count_checked"] == 0
    assert result["stability"]["minimum_eigenvalue"] > 1.5
    assert result["stability"]["minimum_grid_drift_360_to_500"] < 2.0e-5
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__": main()