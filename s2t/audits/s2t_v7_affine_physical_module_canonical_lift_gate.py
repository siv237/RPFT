#!/usr/bin/env python3
"""Audit the corrected affine-to-chiral lift for Tome VII."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


def permutation_matrix(p: tuple[int, ...]) -> np.ndarray:
    u = np.zeros((4, 4))
    for column, row in enumerate(p):
        u[row, column] = 1.0
    return u


V = np.array(
    [
        [1 / np.sqrt(2), -1 / np.sqrt(2), 0.0, 0.0],
        [1 / np.sqrt(6), 1 / np.sqrt(6), -2 / np.sqrt(6), 0.0],
        [1 / np.sqrt(12), 1 / np.sqrt(12), 1 / np.sqrt(12), -3 / np.sqrt(12)],
    ]
)
PERMUTATIONS = [permutation_matrix(p) for p in itertools.permutations(range(4))]
TRIPLET_REPS = [V @ u @ V.T for u in PERMUTATIONS]


def eaff_invariant_projector() -> np.ndarray:
    reps = []
    for u, r in zip(PERMUTATIONS, TRIPLET_REPS):
        matrix = np.zeros((12, 12))
        for k in range(12):
            x = np.zeros((3, 4))
            x.flat[k] = 1.0
            matrix[:, k] = (r @ x @ u.T).ravel()
        reps.append(matrix)
    return sum(reps) / len(reps)


def fixed_rho_orbit_audit() -> dict[str, float | int]:
    basis = []
    for i, j in ((0, 1), (0, 2), (1, 0), (2, 0)):
        e = np.zeros((3, 3))
        e[i, j] = 1.0
        basis.append(e)
    b = np.column_stack([e.ravel() for e in basis])
    projector = b @ np.linalg.inv(b.T @ b) @ b.T
    orbit = []
    residuals = []
    for r in TRIPLET_REPS:
        for e in basis:
            transformed = r @ e @ r.T
            orbit.append(transformed.ravel())
            residuals.append(np.linalg.norm((np.eye(9) - projector) @ transformed.ravel()))
    return {
        "fixed_tangent_dimension": 4,
        "noninvariant_image_count": int(sum(value > 1.0e-10 for value in residuals)),
        "total_image_count": len(residuals),
        "maximum_subspace_residual": float(max(residuals)),
        "orbit_span_dimension": int(np.linalg.matrix_rank(np.column_stack(orbit), tol=1.0e-10)),
    }


def physical_edge_coisometry() -> np.ndarray:
    y = np.zeros((7, 8))
    y[0:3, 0:3] = np.eye(3)
    y[3:6, 3:6] = np.eye(3)
    y[6, 7] = 1.0
    return y


def lifted_action(z: np.ndarray, p_left: np.ndarray) -> float:
    target = np.eye(21)
    return float(
        (
            np.linalg.norm(p_left - z.T @ z, "fro") ** 2
            + np.linalg.norm(z @ z.T - target, "fro") ** 2
        )
        / 45.0
    )


def main() -> None:
    invariant_projector = eaff_invariant_projector()
    invariant_rank = int(np.linalg.matrix_rank(invariant_projector, tol=1.0e-10))
    invariant_residual = float(np.linalg.norm(invariant_projector @ invariant_projector - invariant_projector))
    canonical_vector_residual = float(
        np.linalg.norm(invariant_projector @ V.ravel() - V.ravel())
    )

    rho_audit = fixed_rho_orbit_audit()
    p3 = V.T @ V
    y_star = physical_edge_coisometry()
    z_star = np.kron(V, y_star)
    p_left = np.kron(p3, np.eye(8))
    physical_source_rank = int(round(np.trace(p_left)))
    lifted_rank = int(np.linalg.matrix_rank(z_star, tol=1.0e-10))

    rng = np.random.default_rng(20260826)
    singular_formula_residuals = []
    for _ in range(24):
        raw = rng.normal(size=(21, 32))
        z = raw @ p_left
        sigma = np.linalg.svd(z, compute_uv=False)
        formula = (3.0 + 2.0 * np.sum((1.0 - sigma) ** 2 * (1.0 + sigma) ** 2)) / 45.0
        singular_formula_residuals.append(abs(lifted_action(z, p_left) - formula))

    radial = []
    for t in (0.0, 0.25, 0.5, 1.0, 1.5):
        numeric = lifted_action(t * z_star, p_left)
        analytic = (3.0 + 42.0 * (1.0 - t * t) ** 2) / 45.0
        radial.append(
            {"t": t, "numeric": numeric, "analytic": analytic, "residual": abs(numeric - analytic)}
        )

    result = {
        "gate": "version7_affine_physical_module_canonical_lift_gate",
        "original_carrier": {
            "E_aff_complex_dimension": 12,
            "E_rho_complex_dimension": 4,
            "charged_edge_dimension": 3,
            "claimed_complex_dimension": 144,
            "verdict": "double_family_counting_without_global_tangent_bundle",
        },
        "S4_equivariance": {
            "E_aff_invariant_subspace_dimension": invariant_rank,
            "E_aff_invariant_functional_kernel_dimension": 12 - invariant_rank,
            "averaging_projector_idempotence_residual": invariant_residual,
            "canonical_coisometry_invariant_residual": canonical_vector_residual,
            "contracted_original_complex_kernel_dimension": (12 - invariant_rank) * 12,
            "fixed_E_rho": rho_audit,
        },
        "corrected_carrier": {
            "formula": "E_aff tensor Lambda_ch",
            "complex_multiplicity_dimension": 36,
            "real_multiplicity_tangent_dimension": 72,
            "canonical_embedding": "Hom(C4,V3) tensor Hom(HL,HR) -> Hom(C4 tensor HL,V3 tensor HR)",
        },
        "lifted_hodge_parent": {
            "physical_source_rank": physical_source_rank,
            "target_rank": 21,
            "rank_difference": physical_source_rank - 21,
            "zero_action": lifted_action(np.zeros((21, 32)), p_left),
            "orthonormal_coordinate_hessian_eigenvalue": -8.0 / 45.0,
            "negative_corrected_multiplicity_directions": 72,
            "minimum_lower_bound": 1.0 / 15.0,
            "maximum_singular_value_formula_residual": max(singular_formula_residuals),
        },
        "factorized_witness": {
            "matrix_shape": list(z_star.shape),
            "rank": lifted_rank,
            "action": lifted_action(z_star, p_left),
            "target_coisometry_residual": float(np.linalg.norm(z_star @ z_star.T - np.eye(21))),
            "source_projector_residual": float(
                np.linalg.norm(z_star.T @ z_star - np.kron(p3, y_star.T @ y_star))
            ),
            "full_kernel_dimension": 32 - lifted_rank,
            "reference_kernel_dimension": 8,
            "physical_kernel_dimension": physical_source_rank - lifted_rank,
            "radial_path": radial,
        },
        "contract_update": {
            "original_144_complex_carrier": "fail_double_family_counting",
            "corrected_36_complex_carrier": "pass_typing",
            "stationary_unstable_zero": "pass",
            "bounded_rank_21_minimum": "pass",
            "three_physical_kernel_lines": "pass_as_linear_algebra",
            "full_Real_junk_BRST_BV_hessian": "open",
            "particle_identification": "not_claimed",
        },
        "verdict": {
            "canonical_lift": "positive_after_carrier_correction",
            "next_gate": "full corrected Real module vacuum manifold and Hessian",
        },
    }

    assert invariant_rank == 1
    assert rho_audit["orbit_span_dimension"] == 8
    assert lifted_rank == 21
    assert result["factorized_witness"]["physical_kernel_dimension"] == 3
    assert abs(result["factorized_witness"]["action"] - 1.0 / 15.0) < 1.0e-13
    assert result["lifted_hodge_parent"]["maximum_singular_value_formula_residual"] < 1.0e-9

    output = Path(__file__).resolve().parents[1] / "results" / "s2t_v7_affine_physical_module_canonical_lift_gate_results.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()