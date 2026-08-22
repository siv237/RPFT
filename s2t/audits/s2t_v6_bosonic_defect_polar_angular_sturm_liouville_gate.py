#!/usr/bin/env python3
"""Полярные угловые блоки исправленного эффективного вихря."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh


ROOT = Path(__file__).resolve().parents[2]
CORRECTED_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_corrected_vortex_nonradial_stability_gate.py"
PROFILE_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_defect_profile_gate.py"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_polar_angular_sturm_liouville_gate_results.json"


def main(initialize_only: bool = False) -> None:
    corrected = runpy.run_path(str(CORRECTED_AUDIT))
    profile_module = runpy.run_path(str(PROFILE_AUDIT))
    solution, derivative_a, _ = corrected["corrected_profile"]()
    polynomial = profile_module["POLYNOMIAL"]
    A, B, G = corrected["A"], corrected["B"], corrected["G"]

    def second_a(a, b):
        return sum(
            value * i * (i - 1) * a ** (i - 2) * b**j
            for (i, j), value in polynomial.items() if i >= 2
        )

    def second_b(a, b):
        return sum(
            value * j * (j - 1) * a**i * b ** (j - 2)
            for (i, j), value in polynomial.items() if j >= 2
        )

    def mixed_ab(a, b):
        return sum(
            value * i * j * a ** (i - 1) * b ** (j - 1)
            for (i, j), value in polynomial.items() if i and j
        )

    def add_square(matrix, local_indices, coefficients, weight):
        coefficients = np.asarray(coefficients, dtype=complex)
        local = weight * np.outer(coefficients.conj(), coefficients)
        for row, global_row in enumerate(local_indices):
            for column, global_column in enumerate(local_indices):
                value = local[row, column]
                if value != 0.0:
                    matrix[global_row, global_column] += value

    def add_local_matrix(matrix, local_indices, local):
        for row, global_row in enumerate(local_indices):
            for column, global_column in enumerate(local_indices):
                value = local[row, column]
                if value != 0.0:
                    matrix[global_row, global_column] += value

    def block_spectrum(node_count: int, angular_number: int, eigen_count: int = 6):
        coordinate = np.linspace(0.0, 1.0, node_count)
        radius = 1.0e-4 + (20.0 - 1.0e-4) * coordinate**1.35
        dimension = 5 * node_count
        hessian = lil_matrix((dimension, dimension), dtype=complex)
        metric = lil_matrix((dimension, dimension), dtype=complex)
        imaginary_m = 1j * angular_number

        for element in range(node_count - 1):
            left, right = radius[element], radius[element + 1]
            width = right - left
            middle = 0.5 * (left + right)
            k, a, ap, b = solution.sol(middle)[[0, 2, 3, 4]]
            average = np.array([0.5, 0.5])
            derivative = np.array([-1.0 / width, 1.0 / width])
            radial_weight = middle * width

            # Local ordering: u_L,u_R,v_L,v_R,p_L,p_R,q_L,q_R,w_L,w_R.
            local_indices = []
            for field in range(5):
                local_indices.extend([field * node_count + element, field * node_count + element + 1])

            def coefficients(**fields):
                row = np.zeros(10, dtype=complex)
                offsets = {"u": 0, "v": 2, "p": 4, "q": 6, "w": 8}
                for name, values in fields.items():
                    row[offsets[name]:offsets[name] + 2] = values
                return row

            # |delta D_r phi|^2 = |u'|^2 + |v'-a p|^2.
            add_square(hessian, local_indices, coefficients(u=derivative), A * radial_weight)
            add_square(
                hessian, local_indices,
                coefficients(v=derivative, p=-a * average),
                A * radial_weight,
            )

            # r^{-2}|delta D_theta phi|^2 in the co-rotating scalar frame.
            add_square(
                hessian, local_indices,
                coefficients(u=imaginary_m * average, v=-(1.0 - k) * average),
                A * width / middle,
            )
            add_square(
                hessian, local_indices,
                coefficients(
                    u=(1.0 - k) * average,
                    v=imaginary_m * average,
                    q=-middle * a * average,
                ),
                A * width / middle,
            )

            # The covariant derivative is nonlinear in (A,phi). Its second
            # variation contains -delta A J delta phi, which couples to the
            # nonzero background derivative. Omitting these terms destroys
            # the exact translational zero mode.
            kinetic_cross = np.zeros((10, 10), dtype=complex)
            local_mass = width * np.array([[2.0, 1.0], [1.0, 2.0]]) / 6.0
            # 2 A r a' Re(v* p).
            kinetic_cross[2:4, 4:6] = A * middle * ap * local_mass
            kinetic_cross[4:6, 2:4] = A * middle * ap * local_mass
            # -2 A a(1-k) Re(u* q).
            kinetic_cross[0:2, 6:8] = -A * a * (1.0 - k) * local_mass
            kinetic_cross[6:8, 0:2] = -A * a * (1.0 - k) * local_mass
            add_local_matrix(hessian, local_indices, kinetic_cross)

            # Neutral scalar.
            add_square(hessian, local_indices, coefficients(w=derivative), B * radial_weight)
            add_square(
                hessian, local_indices,
                coefficients(w=imaginary_m * average),
                B * width / middle,
            )

            # Curvature and background-gauge square.
            add_square(
                hessian, local_indices,
                coefficients(
                    p=-imaginary_m * average / middle,
                    q=derivative + average / middle,
                ),
                G * radial_weight,
            )
            add_square(
                hessian, local_indices,
                coefficients(
                    v=-(A / G) * a * average,
                    p=derivative + average / middle,
                    q=imaginary_m * average / middle,
                ),
                G * radial_weight,
            )

            # Local potential Hessian. The phase component v has curvature V_a/a.
            va = derivative_a(a, b)
            phase_curvature = va / max(a, 1.0e-10)
            potential = np.zeros((10, 10), dtype=complex)
            mass = width * middle * np.array([[2.0, 1.0], [1.0, 2.0]]) / 6.0
            potential[0:2, 0:2] = second_a(a, b) * mass
            potential[2:4, 2:4] = phase_curvature * mass
            potential[8:10, 8:10] = second_b(a, b) * mass
            potential[0:2, 8:10] = mixed_ab(a, b) * mass
            potential[8:10, 0:2] = mixed_ab(a, b) * mass
            add_local_matrix(hessian, local_indices, potential)

            metric_mass = radial_weight * np.array([[2.0, 1.0], [1.0, 2.0]]) / 6.0
            for field, coefficient in enumerate([A, A, G, G, B]):
                indices = [field * node_count + element, field * node_count + element + 1]
                add_local_matrix(metric, indices, coefficient * metric_mass)

        # Regularity at the origin is imposed in the Cartesian circular basis:
        # u+i v and p+i q carry harmonic m+1, while u-i v and p-i q carry
        # harmonic m-1; w carries m. This removes the artificial core modes
        # admitted by a merely excised inner circle.
        outer_fixed = {(field + 1) * node_count - 1 for field in range(5)}
        core_u, core_v = 0, node_count
        core_p, core_q = 2 * node_count, 3 * node_count
        core_w = 4 * node_count
        fixed = set(outer_fixed)
        eliminated = set()
        relations = {}
        if angular_number == 0:
            fixed.update([core_u, core_v, core_p, core_q])
        elif abs(angular_number) == 1:
            fixed.add(core_w)
            sign = 1.0 if angular_number == 1 else -1.0
            eliminated.update([core_v, core_q])
            relations[core_u] = [(core_u, 1.0), (core_v, 1j * sign)]
            relations[core_p] = [(core_p, 1.0), (core_q, 1j * sign)]
        else:
            fixed.update([core_u, core_v, core_p, core_q, core_w])

        independent = [
            index for index in range(dimension)
            if index not in fixed and index not in eliminated
        ]
        transformation = lil_matrix((dimension, len(independent)), dtype=complex)
        for column, index in enumerate(independent):
            if index in relations:
                for target, value in relations[index]:
                    transformation[target, column] = value
            else:
                transformation[index, column] = 1.0
        transformation = transformation.tocsr()
        hessian = transformation.conj().T @ hessian.tocsr() @ transformation
        metric = transformation.conj().T @ metric.tocsr() @ transformation
        values = eigsh(
            hessian, k=eigen_count, M=metric, which="SA",
            ncv=max(40, 5 * eigen_count), tol=2.0e-7,
            maxiter=12000, return_eigenvectors=False,
        )
        return np.sort(np.real(values))

    global BLOCK_SPECTRUM
    BLOCK_SPECTRUM = block_spectrum
    if initialize_only:
        return

    node_counts = [100, 160, 240]
    angular_numbers = list(range(-8, 9))
    convergence = {
        str(nodes): {
            str(angular): block_spectrum(nodes, angular).tolist()
            for angular in angular_numbers
        }
        for nodes in node_counts
    }
    calibration_node_count = 360
    calibration = {
        str(angular): block_spectrum(calibration_node_count, angular).tolist()
        for angular in [-1, 0, 1]
    }
    finest = convergence[str(node_counts[-1])]
    minima = {angular: values[0] for angular, values in finest.items()}
    translation_convergence = {
        str(nodes): float(convergence[str(nodes)]["1"][0])
        for nodes in node_counts
    }
    translation_convergence[str(calibration_node_count)] = float(calibration["1"][0])
    fit_nodes = np.array(sorted(int(nodes) for nodes in translation_convergence))
    fit_values = np.array([translation_convergence[str(nodes)] for nodes in fit_nodes])
    translation_order = float(np.polyfit(
        np.log(1.0 / (fit_nodes - 1.0)), np.log(fit_values), 1
    )[0])
    calibrated_internal_gap = float(calibration["0"][0])
    internal_gap_drift = float(abs(calibrated_internal_gap - float(finest["0"][0])))
    translation_resolved = bool(
        calibration["1"][0] < 1.0e-4 and translation_order > 1.5
    )
    result = {
        "gate": "version6_bosonic_defect_polar_angular_sturm_liouville_gate",
        "operator": {
            "fields": ["co-rotating amplitude u", "co-rotating phase v", "radial connection p", "angular connection q", "neutral amplitude w"],
            "gauge_fixing": "polar background gauge div(delta A)-(A/G)(J phi0).delta phi",
            "covariant_translation_tangent": "-D_j phi with compensating gauge parameter +A_j",
            "full_second_variation_cross_terms_included": True,
            "core_regularity": "u+iv,p+iq ~ r^|m+1|; u-iv,p-iq ~ r^|m-1|; w ~ r^|m|",
            "angular_numbers": angular_numbers,
            "radial_node_counts": node_counts,
            "outer_radius": 20.0,
            "inner_radius": 1.0e-4,
            "spectra": convergence,
            "fine_calibration_node_count": calibration_node_count,
            "fine_calibration_spectra": calibration,
        },
        "finest_grid": {
            "minimum_by_angular_number": minima,
            "negative_mode_count": int(sum(value < -1.0e-5 for value in minima.values())),
            "translation_channel_candidates": [-1, 1],
            "translation_candidate_lowest_eigenvalues": {
                "-1": float(minima["-1"]),
                "1": float(minima["1"]),
            },
            "lowest_other_channel_eigenvalue": float(min(
                value for angular, value in minima.items() if angular not in {"-1", "1"}
            )),
            "translation_eigenvalue_convergence": translation_convergence,
            "translation_convergence_order": translation_order,
            "calibrated_axisymmetric_internal_gap": calibrated_internal_gap,
            "internal_gap_drift_240_to_360": internal_gap_drift,
        },
        "verdict": {
            "polar_blocks_constructed": True,
            "negative_mode_found": bool(any(value < -1.0e-5 for value in minima.values())),
            "translation_zero_mode_resolved": translation_resolved,
            "checked_angular_window": [-8, 8],
            "checked_angular_window_nonnegative": bool(all(value >= -1.0e-5 for value in minima.values())),
            "positive_internal_gap_in_checked_window": bool(calibrated_internal_gap > 4.0),
            "continuum_internal_gap_closed": False,
            "full_spin2_spin3_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_polar_high_angular_coercivity_gate",
        },
    }
    assert result["operator"]["gauge_fixing"].startswith("polar background gauge")
    assert result["finest_grid"]["negative_mode_count"] == 0
    assert result["verdict"]["translation_zero_mode_resolved"]
    assert result["verdict"]["positive_internal_gap_in_checked_window"]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()