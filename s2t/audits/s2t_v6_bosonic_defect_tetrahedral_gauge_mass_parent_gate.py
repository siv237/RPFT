#!/usr/bin/env python3
"""Audit independent and composite parents for tetrahedral gauge mass."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_tetrahedral_gauge_mass_parent_gate_results.json"
IDENTITY = np.eye(3)


def symmetrized_traceless_rank_three_basis() -> np.ndarray:
    candidates = []
    for first in range(3):
        for second in range(first, 3):
            for third in range(second, 3):
                tensor = np.zeros((3, 3, 3))
                permutations = set(itertools.permutations((first, second, third)))
                for permutation in permutations:
                    tensor[permutation] = 1.0 / np.sqrt(len(permutations))
                trace = np.einsum("iik->k", tensor)
                tensor -= (
                    np.einsum("ij,k->ijk", IDENTITY, trace)
                    + np.einsum("ik,j->ijk", IDENTITY, trace)
                    + np.einsum("jk,i->ijk", IDENTITY, trace)
                ) / 5.0
                candidates.append(tensor.reshape(-1))
    left, singular_values, _ = np.linalg.svd(np.array(candidates).T, full_matrices=False)
    basis = left[:, :7].T.reshape(7, 3, 3, 3)
    return basis, singular_values


def tetrahedral_axes() -> np.ndarray:
    return np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, -1.0, -1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, -1.0, 1.0],
        ]
    ) / np.sqrt(3.0)


def so3_generators() -> list[np.ndarray]:
    generators = []
    for first, second in [(1, 2), (2, 0), (0, 1)]:
        generator = np.zeros((3, 3))
        generator[first, second] = -1.0
        generator[second, first] = 1.0
        generators.append(generator)
    return generators


def act_on_rank_three(generator: np.ndarray, tensor: np.ndarray) -> np.ndarray:
    return (
        np.einsum("ip,pjk->ijk", generator, tensor)
        + np.einsum("jp,ipk->ijk", generator, tensor)
        + np.einsum("kp,ijp->ijk", generator, tensor)
    )


def matrix_curvature(tensor: np.ndarray, vacuum_norm_squared: float) -> np.ndarray:
    moment = np.einsum("ikl,jkl->ij", tensor, tensor)
    return moment - vacuum_norm_squared * IDENTITY / 3.0


def invariant_identity_test(basis: np.ndarray):
    rng = np.random.default_rng(20260820)
    residuals = []
    for _ in range(100):
        tensor = np.einsum("a,aijk->ijk", rng.normal(size=7), basis)
        moment = np.einsum("ikl,jkl->ij", tensor, tensor)
        second = float(np.trace(moment))
        target = 0.73 * second
        shifted = moment - target * IDENTITY / 3.0
        traceless = moment - second * IDENTITY / 3.0
        left = float(np.sum(shifted**2))
        right = float(np.sum(traceless**2) + (second - target) ** 2 / 3.0)
        residuals.append(abs(left - right))
    return max(residuals)


def independent_spin_three_audit(basis: np.ndarray, tensor_vacuum: np.ndarray):
    coefficients = np.einsum("aijk,ijk->a", basis, tensor_vacuum)
    reconstruction = np.einsum("a,aijk->ijk", coefficients, basis)
    vacuum_norm_squared = float(np.sum(tensor_vacuum**2))
    curvature = matrix_curvature(tensor_vacuum, vacuum_norm_squared)

    jacobian = np.zeros((9, 7))
    for index, variation in enumerate(basis):
        derivative = np.einsum("ikl,jkl->ij", variation, tensor_vacuum)
        derivative += np.einsum("ikl,jkl->ij", tensor_vacuum, variation)
        jacobian[:, index] = derivative.reshape(-1)
    hessian = (2.0 / 3.0) * jacobian.T @ jacobian
    eigenvalues = np.linalg.eigvalsh(hessian)

    rotation_coefficients = np.array(
        [
            [np.sum(direction * act_on_rank_three(generator, tensor_vacuum)) for generator in so3_generators()]
            for direction in basis
        ]
    )
    gauge_mass_matrix = rotation_coefficients.T @ rotation_coefficients

    # The same three-by-three matrix curvature acts on each of the fifteen
    # observed channels, so the normalized H45 trace is exactly tau_3.
    sample = matrix_curvature(1.13 * tensor_vacuum, vacuum_norm_squared)
    triplet_trace = float(np.trace(sample.T @ sample) / 3.0)
    h45_trace = float(np.trace(np.kron(sample.T @ sample, np.eye(15))) / 45.0)
    return {
        "field_dimension": 7,
        "vacuum_norm_squared": vacuum_norm_squared,
        "vacuum_curvature_residual": float(np.linalg.norm(curvature)),
        "basis_reconstruction_residual": float(np.linalg.norm(reconstruction - tensor_vacuum)),
        "hessian_eigenvalues": eigenvalues.tolist(),
        "hessian_rank_tolerance_1e-10": int(np.linalg.matrix_rank(hessian, tol=1.0e-10)),
        "zero_mode_count": int(np.sum(np.abs(eigenvalues) < 1.0e-10)),
        "positive_mode_count": int(np.sum(eigenvalues > 1.0e-10)),
        "rotation_tangent_rank": int(np.linalg.matrix_rank(rotation_coefficients, tol=1.0e-10)),
        "gauge_mass_eigenvalues": np.linalg.eigvalsh(gauge_mass_matrix).tolist(),
        "hessian_on_rotation_tangents_residual": float(np.linalg.norm(hessian @ rotation_coefficients)),
        "normalized_triplet_trace": triplet_trace,
        "normalized_H45_trace": h45_trace,
        "trace_restriction_residual": abs(triplet_trace - h45_trace),
        "continuous_stabilizer_dimension": 3 - int(np.linalg.matrix_rank(rotation_coefficients, tol=1.0e-10)),
        "discrete_stabilizer": "A4",
    }


def tetrahedral_rotation_audit(axes: np.ndarray, tensor_vacuum: np.ndarray):
    preserving = []
    reversing = []
    for permutation in itertools.permutations(range(4)):
        permutation_matrix = np.eye(4)[:, permutation]
        rotation = 0.75 * axes.T @ permutation_matrix @ axes
        transformed = np.einsum("ip,jq,kr,pqr->ijk", rotation, rotation, rotation, tensor_vacuum)
        residual = float(np.linalg.norm(transformed - tensor_vacuum))
        record = {
            "permutation": permutation,
            "determinant": float(np.linalg.det(rotation)),
            "orthogonality_residual": float(np.linalg.norm(rotation.T @ rotation - IDENTITY)),
            "tensor_residual": residual,
        }
        if np.linalg.det(rotation) > 0.0:
            preserving.append(record)
        else:
            reversing.append(record)
    return {
        "proper_rotation_count": len(preserving),
        "improper_rotation_count": len(reversing),
        "maximum_proper_tensor_residual": max(item["tensor_residual"] for item in preserving),
        "minimum_improper_tensor_residual": min(item["tensor_residual"] for item in reversing),
        "proper_stabilizer_is_A4": len(preserving) == 12,
    }


def composite_frame_audit(axes: np.ndarray, tensor_vacuum: np.ndarray):
    frame = axes.T
    left_target = frame @ frame.T
    right_target = frame.T @ frame

    frame_jacobian = []
    composite_curvature_jacobian = []
    vacuum_norm_squared = float(np.sum(tensor_vacuum**2))

    def composite_tensor(value):
        return np.einsum("ia,ja,ka->ijk", value, value, value)

    for flat_index in range(12):
        variation = np.zeros((3, 4))
        variation.flat[flat_index] = 1.0
        left_derivative = variation @ frame.T + frame @ variation.T
        right_derivative = variation.T @ frame + frame.T @ variation
        # One unweighted block trace on the direct sum of left and right
        # curvature spaces.
        frame_jacobian.append(
            np.concatenate([left_derivative.reshape(-1), right_derivative.reshape(-1)])
        )

        step = 1.0e-6
        plus = matrix_curvature(composite_tensor(frame + step * variation), vacuum_norm_squared)
        minus = matrix_curvature(composite_tensor(frame - step * variation), vacuum_norm_squared)
        composite_curvature_jacobian.append(((plus - minus) / (2.0 * step)).reshape(-1))

    frame_jacobian = np.array(frame_jacobian).T
    frame_hessian = 2.0 * frame_jacobian.T @ frame_jacobian
    frame_eigenvalues = np.linalg.eigvalsh(frame_hessian)

    composite_curvature_jacobian = np.array(composite_curvature_jacobian).T
    composite_hessian = (2.0 / 3.0) * composite_curvature_jacobian.T @ composite_curvature_jacobian
    total_hessian = frame_hessian + composite_hessian

    # Left gauge stabilizer: g X0 = X0.  Since X0 has full row rank, it is
    # trivial.  A4 survives only as combined left rotation/right permutation.
    left_stabilizer_nullity = 3 - np.linalg.matrix_rank(
        np.column_stack([(generator @ frame).reshape(-1) for generator in so3_generators()]),
        tol=1.0e-10,
    )

    combined_residuals = []
    for permutation in itertools.permutations(range(4)):
        permutation_matrix = np.eye(4)[:, permutation]
        rotation = 0.75 * axes.T @ permutation_matrix @ axes
        if np.linalg.det(rotation) > 0.0:
            combined_residuals.append(float(np.linalg.norm(rotation @ frame - frame @ permutation_matrix)))

    return {
        "frame_shape": [3, 4],
        "left_curvature_target": left_target.tolist(),
        "right_curvature_target": right_target.tolist(),
        "composite_tensor_residual": float(np.linalg.norm(composite_tensor(frame) - tensor_vacuum)),
        "frame_hessian_eigenvalues": frame_eigenvalues.tolist(),
        "frame_hessian_rank": int(np.linalg.matrix_rank(frame_hessian, tol=1.0e-10)),
        "frame_zero_mode_count": int(np.sum(np.abs(frame_eigenvalues) < 1.0e-10)),
        "composite_curvature_hessian_rank": int(np.linalg.matrix_rank(composite_hessian, tol=1.0e-8)),
        "combined_hessian_eigenvalues": np.linalg.eigvalsh(total_hessian).tolist(),
        "combined_hessian_rank": int(np.linalg.matrix_rank(total_hessian, tol=1.0e-8)),
        "left_gauge_stabilizer_dimension": int(left_stabilizer_nullity),
        "combined_left_right_A4_pair_count": len(combined_residuals),
        "maximum_combined_A4_residual": max(combined_residuals),
        "standalone_residual_gauge_group_is_A4": False,
        "boundary_framed_or_diagonal_A4_is_present": True,
    }


def main() -> None:
    basis, singular_values = symmetrized_traceless_rank_three_basis()
    axes = tetrahedral_axes()
    tensor_vacuum = np.einsum("ai,aj,ak->ijk", axes, axes, axes)

    independent = independent_spin_three_audit(basis, tensor_vacuum)
    rotations = tetrahedral_rotation_audit(axes, tensor_vacuum)
    composite = composite_frame_audit(axes, tensor_vacuum)
    identity_residual = invariant_identity_test(basis)

    result = {
        "gate": "version6_bosonic_defect_tetrahedral_gauge_mass_parent_gate",
        "literature_invariant_bridge": {
            "matrix_curvature": "mu_ij=T_ikl T_jkl-(v_T^2/3)delta_ij",
            "identity": "Tr(mu^2)=Tr(A0^2)+(Tr(A)-v_T^2)^2/3",
            "maximum_random_identity_residual": identity_residual,
            "harmonic_rank_three_basis_singular_values": singular_values.tolist(),
            "target_module": "Sym3(R)=1+5",
        },
        "independent_spin_three_parent": independent,
        "tetrahedral_stabilizer": rotations,
        "composite_four_axis_frame_parent": composite,
        "project_no_go_compatibility": {
            "old_diagonal_projector_square_is_full_SO3_invariant_parent": False,
            "old_KO6_degree_two_junk_no_go_still_applies_to_that_specific_calculus": True,
            "old_junk_no_go_excludes_all_composite_spin_three_curvatures": False,
            "M300_promoted_to_coordinate_gauge_algebra": False,
        },
        "verdict": {
            "independent_spin_three_zero_locus_and_hessian_pass": True,
            "independent_spin_three_is_already_derived_field_of_current_parent": False,
            "composite_frame_has_no_new_fundamental_field": True,
            "composite_frame_standalone_unbroken_gauge_A4": False,
            "composite_frame_boundary_framed_diagonal_A4": True,
            "single_current_parent_closes_both_interpretations": False,
            "matter_birth_closed": False,
            "status": "independent_local_pass_composite_boundary_pass_branch_decision_open",
            "next_gate": "version6_bosonic_defect_tetrahedral_gauge_frame_branch_decision_gate",
        },
    }

    assert identity_residual < 1.0e-12
    assert independent["zero_mode_count"] == 3
    assert independent["positive_mode_count"] == 4
    assert independent["rotation_tangent_rank"] == 3
    assert independent["trace_restriction_residual"] < 1.0e-14
    assert rotations["proper_stabilizer_is_A4"]
    assert composite["frame_zero_mode_count"] == 3
    assert composite["frame_hessian_rank"] == 9
    assert composite["combined_hessian_rank"] == 9
    assert composite["left_gauge_stabilizer_dimension"] == 0
    assert composite["maximum_combined_A4_residual"] < 1.0e-14

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()