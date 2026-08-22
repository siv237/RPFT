#!/usr/bin/env python3
"""Аудит калибровочно-кадровой тетраэдрической развилки Тома VI."""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_tetrahedral_gauge_frame_branch_decision_gate_results.json"


def tensor_product(j_left: int, j_right: int) -> Counter[int]:
    return Counter({j: 1 for j in range(abs(j_left - j_right), j_left + j_right + 1)})


def hom_decomposition(target: list[int], source: list[int]) -> Counter[int]:
    result: Counter[int] = Counter()
    for jt in target:
        for js in source:
            result.update(tensor_product(jt, js))
    return result


def dimension(decomposition: Counter[int]) -> int:
    return sum(mult * (2 * j + 1) for j, mult in decomposition.items())


def parity(perm: tuple[int, ...]) -> int:
    inversions = sum(perm[i] > perm[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


def permutation_matrix(perm: tuple[int, ...]) -> np.ndarray:
    matrix = np.zeros((4, 4))
    for column, row in enumerate(perm):
        matrix[row, column] = 1.0
    return matrix


def so3_generators() -> list[np.ndarray]:
    return [
        np.array([[0.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]]),
        np.array([[0.0, 0.0, 1.0], [0.0, 0.0, 0.0], [-1.0, 0.0, 0.0]]),
        np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]),
    ]


def act_rank_three(generator: np.ndarray, tensor: np.ndarray) -> np.ndarray:
    return (
        np.einsum("ia,ajk->ijk", generator, tensor)
        + np.einsum("ja,iak->ijk", generator, tensor)
        + np.einsum("ka,ija->ijk", generator, tensor)
    )


def main() -> None:
    vertices = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, -1.0, -1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, -1.0, 1.0],
        ]
    ) / np.sqrt(3.0)
    frame = vertices.T
    weights = np.full(4, 0.25)

    first_moment = np.einsum("a,ai->i", weights, vertices)
    second_moment = np.einsum("a,ai,aj->ij", weights, vertices, vertices)
    third_moment = np.einsum("a,ai,aj,ak->ijk", weights, vertices, vertices, vertices)

    rotations = []
    proper_residuals = []
    improper_residuals = []
    combined_residuals = []
    for perm in itertools.permutations(range(4)):
        u = permutation_matrix(perm)
        rotation = frame @ u @ frame.T @ np.linalg.inv(frame @ frame.T)
        rotations.append(rotation)
        residual = np.linalg.norm(np.einsum("ia,jb,kc,abc->ijk", rotation, rotation, rotation, third_moment) - third_moment)
        combined_residuals.append(np.linalg.norm(rotation @ frame - frame @ u))
        if np.linalg.det(rotation) > 0:
            proper_residuals.append(residual)
        else:
            improper_residuals.append(residual)

    generators = so3_generators()
    frame_orbit = np.column_stack([(generator @ frame).reshape(-1) for generator in generators])
    tensor_orbit = np.column_stack([act_rank_three(generator, third_moment).reshape(-1) for generator in generators])
    gauge_mass = tensor_orbit.T @ tensor_orbit

    end_v3 = hom_decomposition([1], [1])
    hom_v4_v3 = hom_decomposition([1], [0, 1])
    k_family = [0, 1, 1, 1]  # C4=(0+1), затем два триплетных узла.
    end_k_family = hom_decomposition(k_family, k_family)

    # Внешний симметрический куб векторного представления: Sym^3(V1)=V3+V1.
    external_symmetric_cube = Counter({3: 1, 1: 1})

    result = {
        "gate": "version6_bosonic_defect_tetrahedral_gauge_frame_branch_decision_gate",
        "current_parent_representation_ledger": {
            "End_V3": {str(j): end_v3[j] for j in sorted(end_v3)},
            "End_V3_dimension": dimension(end_v3),
            "Hom_V4_to_V3": {str(j): hom_v4_v3[j] for j in sorted(hom_v4_v3)},
            "Hom_V4_to_V3_dimension": dimension(hom_v4_v3),
            "End_Kfam": {str(j): end_k_family[j] for j in sorted(end_k_family)},
            "End_Kfam_dimension": dimension(end_k_family),
            "spin_three_multiplicity_in_End_Kfam": end_k_family[3],
            "ordinary_matrix_products_remain_in_End_Kfam": True,
            "spin_three_from_ordinary_parent_operator_polynomial": False,
            "external_Sym3_V3": {str(j): external_symmetric_cube[j] for j in sorted(external_symmetric_cube)},
            "external_Sym3_V3_dimension": dimension(external_symmetric_cube),
            "spin_three_multiplicity_in_external_Sym3_V3": external_symmetric_cube[3],
        },
        "uniform_tetrahedral_moment": {
            "weights": weights.tolist(),
            "first_moment_norm": float(np.linalg.norm(first_moment)),
            "second_moment_isotropy_residual": float(np.linalg.norm(second_moment - np.eye(3) / 3.0)),
            "third_moment_norm_squared": float(np.vdot(third_moment, third_moment).real),
            "proper_stabilizer_count": len(proper_residuals),
            "improper_tetrahedral_operation_count": len(improper_residuals),
            "maximum_proper_third_moment_residual": float(max(proper_residuals)),
            "maximum_combined_frame_permutation_residual": float(max(combined_residuals)),
            "third_moment_continuous_orbit_rank": int(np.linalg.matrix_rank(tensor_orbit, tol=1e-10)),
            "gauge_mass_eigenvalues_from_third_moment": np.linalg.eigvalsh(gauge_mass).tolist(),
            "interpretation": "zero vector and quadrupole order, nonzero tetrahedral rank-three order",
        },
        "ordered_frame_branch": {
            "frame_rank": int(np.linalg.matrix_rank(frame)),
            "left_gauge_orbit_rank": int(np.linalg.matrix_rank(frame_orbit, tol=1e-10)),
            "left_continuous_stabilizer_dimension": 3 - int(np.linalg.matrix_rank(frame_orbit, tol=1e-10)),
            "left_discrete_stabilizer_is_trivial": True,
            "diagonal_A4_pair_count": sum(parity(perm) > 0 for perm in itertools.permutations(range(4))),
            "right_permutation_action_is_inner_gauge_symmetry_of_commutative_C4": False,
            "project_status_of_full_S4": "conditional affine-family postulate, not derived local gauge group",
        },
        "branch_decision": {
            "uniform_moment_is_valid_tetrahedral_composite_order": True,
            "uniform_moment_is_already_a_dynamic_field_of_current_parent": False,
            "independent_spin_three_is_already_in_current_operator_carrier": False,
            "ordered_frame_leaves_gauge_A4": False,
            "ordered_frame_leaves_diagonal_global_or_boundary_A4": True,
            "current_one_connection_parent_yields_genuine_SO3_to_A4_Higgs_phase": False,
            "minimal_way_to_retain_gauge_A4_and_Z3_holonomy": "add or derive one spin-three carrier Sym0^3(V3)",
            "alternative_repair": "gauge a second frame SO3 and break the product to a diagonal gauge SO3 before tetrahedral reduction",
            "alternative_repair_rejected_by_current_minimality": True,
            "matter_birth_closed": False,
            "status": "current_parent_no_go_minimal_spin_three_carrier_extension_selected",
            "next_gate": "version6_bosonic_defect_minimal_spin_three_carrier_embedding_gate",
        },
    }

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()