#!/usr/bin/env python3
"""Test whether the existing affine/Hodge parent can select old/new copies."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_affine_hodge_copy_selector_no_go_gate_results.json"


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def copy_rotation(theta: float) -> np.ndarray:
    return np.array(
        [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]],
        dtype=complex,
    )


def hodge_action(matrix: np.ndarray) -> float:
    target = np.eye(matrix.shape[0], dtype=complex)
    residual = matrix @ matrix.conj().T - target
    return float(np.linalg.norm(residual, "fro") ** 2)


def kernel_projector(matrix: np.ndarray) -> np.ndarray:
    gram = matrix @ matrix.conj().T
    return np.eye(matrix.shape[1], dtype=complex) - matrix.conj().T @ np.linalg.inv(gram) @ matrix


def main() -> None:
    previous = load_result("s2t_v7_four_vertex_vectorlike_selector_gate_results.json")
    assert previous["verdict"]["status"] == "conditional_positive_selector_missing"

    identity3 = np.eye(3, dtype=complex)
    zero3 = np.zeros((3, 3), dtype=complex)
    vacuum = np.hstack((identity3, zero3))
    old_projector = np.block([[identity3, zero3], [zero3, zero3]])
    initial_kernel = kernel_projector(vacuum)
    assert np.linalg.matrix_rank(vacuum) == 3
    assert abs(np.trace(initial_kernel).real - 3.0) < 1e-12

    angles = np.linspace(0.0, np.pi / 2.0, 17)
    baseline_singular_values = np.linalg.svd(vacuum, compute_uv=False)
    baseline_action = hodge_action(vacuum)
    orbit_rows = []
    for theta in angles:
        rotation = np.kron(copy_rotation(float(theta)), identity3)
        moved = vacuum @ rotation
        projector = kernel_projector(moved)
        orbit_rows.append(
            {
                "theta": float(theta),
                "action": hodge_action(moved),
                "singular_value_residual": float(
                    np.linalg.norm(np.linalg.svd(moved, compute_uv=False) - baseline_singular_values)
                ),
                "kernel_projector_displacement": float(np.linalg.norm(projector - initial_kernel, "fro")),
                "kernel_overlap_with_old_copy": float(np.trace(projector @ old_projector).real),
            }
        )

    maximum_action_residual = max(abs(row["action"] - baseline_action) for row in orbit_rows)
    maximum_singular_residual = max(row["singular_value_residual"] for row in orbit_rows)
    maximum_projector_displacement = max(row["kernel_projector_displacement"] for row in orbit_rows)
    overlap_range = [
        min(row["kernel_overlap_with_old_copy"] for row in orbit_rows),
        max(row["kernel_overlap_with_old_copy"] for row in orbit_rows),
    ]
    assert maximum_action_residual < 1e-24
    assert maximum_singular_residual < 1e-12
    assert maximum_projector_displacement > 2.4
    assert overlap_range[0] < 1e-12 and overlap_range[1] > 3.0 - 1e-12

    # The affine projector acts on C^4 and is tensored with the identity of
    # copy space.  It therefore commutes exactly with every U(2) copy rotation.
    p3 = np.eye(4, dtype=complex) - np.ones((4, 4), dtype=complex) / 4.0
    lifted_p3 = np.kron(p3, np.eye(2, dtype=complex))
    affine_commutators = []
    for theta in angles:
        lifted_rotation = np.kron(np.eye(4, dtype=complex), copy_rotation(float(theta)))
        affine_commutators.append(float(np.linalg.norm(lifted_p3 @ lifted_rotation - lifted_rotation @ lifted_p3)))
    assert max(affine_commutators) < 1e-12

    # The represented algebra acts identically on exact old/new duplicates.
    # Consequently I_family tensor M2(C) lies in its commutant.
    rng = np.random.default_rng(20260827)
    represented = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    represented = np.kron(represented, np.eye(2, dtype=complex))
    matrix_units = []
    commutant_residuals = []
    for row in range(2):
        for column in range(2):
            unit = np.zeros((2, 2), dtype=complex)
            unit[row, column] = 1.0
            lifted_unit = np.kron(np.eye(3, dtype=complex), unit)
            matrix_units.append(lifted_unit)
            commutant_residuals.append(float(np.linalg.norm(represented @ lifted_unit - lifted_unit @ represented)))
    commutant_rank = int(np.linalg.matrix_rank(np.stack([unit.reshape(-1) for unit in matrix_units], axis=1)))
    assert commutant_rank == 4
    assert max(commutant_residuals) < 1e-12

    # A central finite-difference estimate along the copy orbit is exactly
    # flat at the coisometric vacuum.
    step = 1e-4
    action_plus = hodge_action(vacuum @ np.kron(copy_rotation(step), identity3))
    action_minus = hodge_action(vacuum @ np.kron(copy_rotation(-step), identity3))
    orbit_hessian = (action_plus - 2.0 * baseline_action + action_minus) / step**2
    assert abs(orbit_hessian) < 1e-20

    result = {
        "gate": "version7_affine_hodge_copy_selector_no_go_gate",
        "copy_orbit": {
            "mass_matrix_shape": list(vacuum.shape),
            "kernel_dimension": int(round(np.trace(initial_kernel).real)),
            "sample_count": len(orbit_rows),
            "maximum_hodge_action_residual": maximum_action_residual,
            "maximum_singular_value_residual": maximum_singular_residual,
            "maximum_kernel_projector_displacement": maximum_projector_displacement,
            "kernel_overlap_with_old_copy_range": overlap_range,
            "orbit_hessian": float(orbit_hessian),
            "samples": orbit_rows,
        },
        "affine_lift": {
            "rank_P3": int(np.linalg.matrix_rank(p3)),
            "copy_factor": "I2",
            "maximum_commutator_with_copy_U2": max(affine_commutators),
            "P3_selects_copy_line": False,
        },
        "commutant": {
            "contained_copy_algebra": "M2(C)",
            "verified_complex_dimension": commutant_rank,
            "maximum_matrix_unit_commutator": max(commutant_residuals),
            "represented_algebra_distinguishes_old_new_duplicates": False,
        },
        "analytic_statement": {
            "transformation": "M -> M (U_copy tensor I_family)",
            "MM_star_invariant": True,
            "kernel_projector_conjugates": True,
            "singular_value_Hodge_functional_selects_orientation": False,
            "Real_or_class15_breaks_copy_U2": False,
        },
        "verdict": {
            "existing_affine_Hodge_parent_selects_kernel_dimension": True,
            "existing_affine_Hodge_parent_selects_kernel_orientation": False,
            "existing_affine_Hodge_parent_selects_six_of_eleven_edges": False,
            "status": "closed_as_copy_selector",
            "next_gate": "derive or exclude a noncentral copy-space operator from an oriented path algebra or Morita corner without preselecting the desired six edges",
        },
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()