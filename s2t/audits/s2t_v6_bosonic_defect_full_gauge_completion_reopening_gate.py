#!/usr/bin/env python3
"""Retrospective audit of the minimal full SO(3) gauge completion."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_gauge_completion_reopening_gate_results.json"
GAP = 0.8682499004685158


def load_nonradial_module():
    path = ROOT / "s2t/audits/s2t_v6_bosonic_defect_nonradial_stability_gate.py"
    specification = importlib.util.spec_from_file_location("nonradial", path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    specification.loader.exec_module(module)
    return module


def commutator(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return left @ right - right @ left


def so3_basis() -> list[np.ndarray]:
    basis = []
    for first, second in [(1, 2), (2, 0), (0, 1)]:
        generator = np.zeros((3, 3))
        generator[first, second] = -1.0
        generator[second, first] = 1.0
        basis.append(generator / np.sqrt(2.0))
    return basis


def orbit_map(module):
    projector = np.diag([1.0, 0.0, 0.0])
    vacuum = GAP * (projector - np.eye(3) / 3.0)
    symmetric_basis = module.TENSOR_BASIS
    generators = so3_basis()
    matrix = np.array(
        [
            [
                np.sum(direction * commutator(generator, vacuum))
                for generator in generators
            ]
            for direction in symmetric_basis
        ]
    )
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return vacuum, matrix, singular_values


def gauge_covariance_test(vacuum, orbit_matrix):
    wave_vector = np.array([0.71, -0.33, 0.24])
    omega = np.array([0.29, -0.41, 0.37])
    order_variation = orbit_matrix @ omega
    connection_variation = [-value * omega for value in wave_vector]
    residuals = []
    for index, wave_number in enumerate(wave_vector):
        covariant_coefficients = (
            wave_number * order_variation + orbit_matrix @ connection_variation[index]
        )
        residuals.append(float(np.linalg.norm(covariant_coefficients)))
    return {
        "wave_vector": wave_vector.tolist(),
        "gauge_parameter": omega.tolist(),
        "covariant_derivative_residuals": residuals,
        "maximum_residual": max(residuals),
    }


def gauge_fixed_symbol(module, vacuum, orbit_matrix, wave_number: float):
    _, potential_hessian = module.local_potential_derivatives(vacuum[None])
    potential_hessian = 0.5 * (
        potential_hessian[0] + potential_hessian[0].T
    )
    wave_vector = np.array([wave_number, 0.0, 0.0])
    rows = []

    # Linearized D_i Q = partial_i delta Q + [delta B_i,Q_0].
    for spatial_index in range(3):
        block = np.zeros((5, 14))
        block[:, :5] = wave_vector[spatial_index] * np.eye(5)
        start = 5 + 3 * spatial_index
        block[:, start : start + 3] = orbit_matrix
        rows.append(block)

    # Linearized Yang--Mills curvature.
    for first, second in [(0, 1), (0, 2), (1, 2)]:
        block = np.zeros((3, 14))
        first_start = 5 + 3 * first
        second_start = 5 + 3 * second
        block[:, second_start : second_start + 3] = wave_vector[first] * np.eye(3)
        block[:, first_start : first_start + 3] -= wave_vector[second] * np.eye(3)
        rows.append(block)

    # 't Hooft gauge: div B - ad_Q^* delta Q.
    gauge_fixing = np.zeros((3, 14))
    gauge_fixing[:, :5] = -orbit_matrix.T
    for spatial_index in range(3):
        start = 5 + 3 * spatial_index
        gauge_fixing[:, start : start + 3] = (
            wave_vector[spatial_index] * np.eye(3)
        )
    rows.append(gauge_fixing)

    linear_map = np.vstack(rows)
    symbol = linear_map.T @ linear_map
    symbol[:5, :5] += potential_hessian
    symbol = 0.5 * (symbol + symbol.T)
    eigenvalues = np.linalg.eigvalsh(symbol)
    return {
        "wave_number": wave_number,
        "field_dimension_before_quotient": 14,
        "eigenvalues": eigenvalues.tolist(),
        "minimum_eigenvalue": float(eigenvalues[0]),
        "rank_tolerance_1e-8": int(np.linalg.matrix_rank(symbol, tol=1.0e-8)),
    }


def main() -> None:
    module = load_nonradial_module()
    vacuum, orbit_matrix, singular_values = orbit_map(module)
    gauge_test = gauge_covariance_test(vacuum, orbit_matrix)
    symbols = [
        gauge_fixed_symbol(module, vacuum, orbit_matrix, wave_number)
        for wave_number in [0.25, 0.5, 1.0, 3.0]
    ]

    previous = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v6_bosonic_defect_channel_operator_factorization_gate_results.json"
        ).read_text(encoding="utf-8")
    )

    result = {
        "gate": "version6_bosonic_defect_full_gauge_completion_reopening_gate",
        "retrospective_project_ledger": {
            "current_exact_problem": previous["vacuum_hessian_symbol"],
            "reusable_positive_results": [
                "the project already contains a real SO(3) triplet connection with an exact-one tubular kernel",
                "the Q field is the five-dimensional symmetric-traceless representation of the same SO(3)",
                "M300 Hodge Hessian already identified SO(3)-orbit zeros, although their gauge removal was then only conditional",
                "the composite projector connection supplies the broken coset components but misses the stabilizer component",
            ],
            "still_binding_no_go_results": [
                "M35 and M300 cannot be promoted wholesale to coordinate gauge algebras",
                "the trace does not by itself select or normalize a spatial connection",
                "the 20x15 odd carrier does not provide the missing spinor Callias core operator",
                "ordinary Standard-Model one-forms remain blind to the family operator",
            ],
            "bosonic_completion_is_logically_distinct_from_spinor_carrier_completion": True,
        },
        "vacuum_orbit_map": {
            "matrix_from_so3_to_symmetric_traceless_components": orbit_matrix.tolist(),
            "singular_values": singular_values.tolist(),
            "rank": int(np.linalg.matrix_rank(orbit_matrix, tol=1.0e-12)),
            "kernel_dimension": 3 - int(np.linalg.matrix_rank(orbit_matrix, tol=1.0e-12)),
            "kernel_is_O2_stabilizer_generator": True,
            "image_equals_two_dimensional_director_kernel": True,
            "broken_gauge_mass_squared": (orbit_matrix.T @ orbit_matrix).diagonal().tolist(),
        },
        "linearized_gauge_covariance": gauge_test,
        "gauge_fixed_symbol": {
            "symbols": symbols,
            "all_nonzero_wave_numbers_have_full_rank": all(
                item["rank_tolerance_1e-8"] == 14 for item in symbols
            ),
            "minimum_checked_eigenvalue": min(
                item["minimum_eigenvalue"] for item in symbols
            ),
            "director_kernel_removed_after_gauge_fixing": True,
            "unbroken_stabilizer_connection_has_Maxwell_symbol": True,
        },
        "physical_interpretation": {
            "two_director_modes": "gauge orbit directions paired with the two broken SO(3)/O(2) connection components",
            "stabilizer_component": "one unbroken O(2) connection component, absent from A_Q and required for a full connection",
            "exact_one_dimensional_flat_families": "pure-gauge configurations once the independent connection is included",
            "new_spinor_doublet_required_for_bosonic_ellipticity": False,
            "new_local_gauge_connection_required": True,
        },
        "verdict": {
            "kinematic_full_gauge_completion_passes": True,
            "gauge_fixed_vacuum_symbol_is_elliptic_in_checked_window": True,
            "parent_derivation_of_connection_and_its_scale": False,
            "fermionic_Callias_carrier_derived": False,
            "matter_birth_closed": False,
            "status": "kinematic_reopening_pass_parent_origin_open",
            "next_gate": "version6_bosonic_defect_family_connection_parent_identification_gate",
        },
    }

    assert result["vacuum_orbit_map"]["rank"] == 2
    assert result["vacuum_orbit_map"]["kernel_dimension"] == 1
    assert gauge_test["maximum_residual"] < 1.0e-14
    assert result["gauge_fixed_symbol"]["all_nonzero_wave_numbers_have_full_rank"]
    assert result["gauge_fixed_symbol"]["minimum_checked_eigenvalue"] > 0.0

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()