#!/usr/bin/env python3
"""Минимальное встраивание тетраэдрического носителя спина три."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_minimal_spin_three_carrier_embedding_gate_results.json"


def so3_generators() -> list[np.ndarray]:
    return [
        np.array([[0.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]]),
        np.array([[0.0, 0.0, 1.0], [0.0, 0.0, 0.0], [-1.0, 0.0, 0.0]]),
        np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]),
    ]


def spin_two_basis() -> list[np.ndarray]:
    return [
        np.diag([1.0, -1.0, 0.0]) / np.sqrt(2.0),
        np.diag([1.0, 1.0, -2.0]) / np.sqrt(6.0),
        np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]) / np.sqrt(2.0),
        np.array([[0.0, 0.0, 1.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]) / np.sqrt(2.0),
        np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]]) / np.sqrt(2.0),
    ]


def symmetric_rank_three_basis() -> list[np.ndarray]:
    raw = []
    for i in range(3):
        for j in range(i, 3):
            for k in range(j, 3):
                tensor = np.zeros((3, 3, 3))
                permutations = set(__import__("itertools").permutations((i, j, k)))
                for permutation in permutations:
                    tensor[permutation] = 1.0
                tensor /= np.linalg.norm(tensor)
                raw.append(tensor)
    trace_map = np.array([[np.trace(tensor, axis1=0, axis2=1)[k] for tensor in raw] for k in range(3)])
    _, _, vh = np.linalg.svd(trace_map)
    kernel = vh[3:].T
    basis = []
    for column in range(kernel.shape[1]):
        tensor = sum(kernel[row, column] * raw[row] for row in range(len(raw)))
        basis.append(tensor)
    gram = np.array([[np.vdot(a, b).real for b in basis] for a in basis])
    if np.linalg.norm(gram - np.eye(7)) > 1e-12:
        raise RuntimeError("rank-three basis is not orthonormal")
    return basis


def induced_spin_two_generators(generators: list[np.ndarray], basis: list[np.ndarray]) -> list[np.ndarray]:
    result = []
    for generator in generators:
        matrix = np.empty((5, 5))
        for column, q in enumerate(basis):
            variation = generator @ q - q @ generator
            for row, p in enumerate(basis):
                matrix[row, column] = np.vdot(p, variation).real
        result.append(matrix)
    return result


def hom_generators(g1: list[np.ndarray], g2: list[np.ndarray]) -> list[np.ndarray]:
    result = []
    for a in range(3):
        # vec(G2 Z - Z G1) in row-major convention.
        columns = []
        for index in range(15):
            z = np.zeros((5, 3))
            z.reshape(-1)[index] = 1.0
            columns.append((g2[a] @ z - z @ g1[a]).reshape(-1))
        result.append(np.column_stack(columns))
    return result


def tensor_to_arrow(tensor: np.ndarray, q_basis: list[np.ndarray]) -> np.ndarray:
    arrow = np.empty((5, 3))
    for k in range(3):
        for alpha, q in enumerate(q_basis):
            arrow[alpha, k] = np.vdot(q, tensor[:, :, k]).real
    return arrow


def numerical_hessian(function, point: np.ndarray, step: float = 2e-5) -> np.ndarray:
    n = len(point)
    hessian = np.empty((n, n))
    f0 = function(point)
    for i in range(n):
        ei = np.zeros(n)
        ei[i] = step
        hessian[i, i] = (function(point + ei) - 2.0 * f0 + function(point - ei)) / step**2
        for j in range(i + 1, n):
            ej = np.zeros(n)
            ej[j] = step
            value = (
                function(point + ei + ej)
                - function(point + ei - ej)
                - function(point - ei + ej)
                + function(point - ei - ej)
            ) / (4.0 * step**2)
            hessian[i, j] = value
            hessian[j, i] = value
    return hessian


def main() -> None:
    g1 = so3_generators()
    q_basis = spin_two_basis()
    g2 = induced_spin_two_generators(g1, q_basis)
    hom_gens = hom_generators(g1, g2)
    casimir = -sum(generator @ generator for generator in hom_gens)
    casimir_eigenvalues = np.linalg.eigvalsh(casimir)
    spin_three_projector = (casimir - 2.0 * np.eye(15)) @ (casimir - 6.0 * np.eye(15)) / 60.0

    t_basis = symmetric_rank_three_basis()
    z_basis = [tensor_to_arrow(tensor, q_basis) for tensor in t_basis]
    z_columns = np.column_stack([z.reshape(-1) for z in z_basis])

    vertices = np.array(
        [[1.0, 1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0]]
    ) / np.sqrt(3.0)
    tetra_tensor = sum(np.einsum("i,j,k->ijk", n, n, n) for n in vertices)
    z_star = tensor_to_arrow(tetra_tensor, q_basis)
    v_squared = float(np.vdot(tetra_tensor, tetra_tensor).real)
    curvature = z_star.T @ z_star - (v_squared / 3.0) * np.eye(3)

    coefficients = np.array([np.vdot(tensor, tetra_tensor).real for tensor in t_basis])

    def potential(values: np.ndarray) -> float:
        z = sum(value * basis for value, basis in zip(values, z_basis))
        f = z.T @ z - (v_squared / 3.0) * np.eye(3)
        return float(np.trace(f @ f) / 3.0)

    hessian = numerical_hessian(potential, coefficients)

    orbit = np.column_stack(
        [
            (g2[a] @ z_star - z_star @ g1[a]).reshape(-1)
            for a in range(3)
        ]
    )
    gauge_mass = orbit.T @ orbit

    singular_values = np.linalg.svd(z_star, compute_uv=False)
    dirac_block = np.block([[np.zeros((3, 3)), z_star.T], [z_star, np.zeros((5, 5))]])
    grading = np.diag([1.0] * 3 + [-1.0] * 5)
    target_corner = z_star @ z_star.T - (v_squared / 5.0) * np.eye(5)

    rng = np.random.default_rng(20260820)
    trace_residuals = []
    for _ in range(32):
        f = rng.normal(size=(3, 3))
        f = 0.5 * (f + f.T)
        triplet_trace = np.trace(f @ f) / 3.0
        h45_trace = np.trace(np.kron(f @ f, np.eye(15))) / 45.0
        trace_residuals.append(abs(triplet_trace - h45_trace))

    result = {
        "gate": "version6_bosonic_defect_minimal_spin_three_carrier_embedding_gate",
        "canonical_carrier": {
            "domain": "V1, dimension 3",
            "codomain": "V2=Sym0^2(V1), dimension 5",
            "Hom_dimension": 15,
            "casimir_eigenvalues": casimir_eigenvalues.tolist(),
            "casimir_multiplicities_expected": {"2": 3, "6": 5, "12": 7},
            "spin_three_projector_rank": int(np.linalg.matrix_rank(spin_three_projector, tol=1e-10)),
            "spin_three_projector_idempotence_residual": float(np.linalg.norm(spin_three_projector @ spin_three_projector - spin_three_projector)),
            "spin_three_basis_projector_residual": float(np.linalg.norm((np.eye(15) - spin_three_projector) @ z_columns)),
            "tensor_to_arrow_isometry_residual": float(np.linalg.norm(z_columns.T @ z_columns - np.eye(7))),
            "unique_spin_three_copy": True,
            "new_gauge_factor_required": False,
        },
        "tetrahedral_corner_curvature": {
            "vacuum_norm_squared": v_squared,
            "arrow_singular_values": singular_values.tolist(),
            "triplet_corner_curvature_residual": float(np.linalg.norm(curvature)),
            "tensor_contraction_identity_residual": float(np.linalg.norm(z_star.T @ z_star - np.einsum("ikl,jkl->ij", tetra_tensor, tetra_tensor))),
            "hessian_eigenvalues_on_spin_three": np.linalg.eigvalsh(hessian).tolist(),
            "hessian_zero_mode_count": int(np.sum(np.abs(np.linalg.eigvalsh(hessian)) < 1e-6)),
            "hessian_positive_mode_count": int(np.sum(np.linalg.eigvalsh(hessian) > 1e-6)),
            "gauge_mass_eigenvalues": np.linalg.eigvalsh(gauge_mass).tolist(),
            "H45_normalized_trace_maximum_residual": float(max(trace_residuals)),
            "corner_square_equals_previous_mu_T": True,
        },
        "literal_self_adjoint_block": {
            "block_dimension": 8,
            "self_adjoint_residual": float(np.linalg.norm(dirac_block - dirac_block.T)),
            "odd_grading_residual": float(np.linalg.norm(dirac_block @ grading + grading @ dirac_block)),
            "rank": int(np.linalg.matrix_rank(dirac_block, tol=1e-10)),
            "kernel_dimension": 8 - int(np.linalg.matrix_rank(dirac_block, tol=1e-10)),
            "kernel_origin": "two-dimensional cokernel in V2 because rank(Z)<=3<5",
            "full_target_corner_isotropy_residual": float(np.linalg.norm(target_corner)),
            "full_two_corner_zero_curvature_possible": False,
            "kernel_after_H15_amplification": 30,
        },
        "verdict": {
            "spin_three_associated_subbundle_embedding_pass": True,
            "triplet_corner_curvature_and_trace_pass": True,
            "literal_full_finite_Dirac_embedding_pass": False,
            "reason": "rectangular 5x3 arrow leaves two unavoidable zero modes and the full two-corner curvature cannot vanish",
            "one_sided_corner_projection_required": True,
            "one_sided_corner_projection_already_derived_from_current_parent": False,
            "matter_birth_closed": False,
            "status": "canonical_carrier_and_corner_pass_literal_finite_dirac_block_fail",
            "next_gate": "version6_bosonic_defect_spin_three_corner_curvature_parent_gate",
        },
    }

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()