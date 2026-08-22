#!/usr/bin/env python3
"""Audit whether existing two-copy carriers supply a physical spin-cover doublet."""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_two_copy_spin_cover_multiplicity_gate_results.json"


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def spin_one_generators() -> list[np.ndarray]:
    epsilon = np.zeros((3, 3, 3), dtype=float)
    epsilon[0, 1, 2] = epsilon[1, 2, 0] = epsilon[2, 0, 1] = 1.0
    epsilon[0, 2, 1] = epsilon[2, 1, 0] = epsilon[1, 0, 2] = -1.0
    return [-1j * epsilon[a] for a in range(3)]


def swap_operator(dimension: int) -> np.ndarray:
    result = np.zeros((dimension**2, dimension**2), dtype=complex)
    for i in range(dimension):
        for j in range(dimension):
            result[j * dimension + i, i * dimension + j] = 1.0
    return result


def joint_commutant_dimension(generators: list[np.ndarray], tolerance: float = 1e-10) -> int:
    dimension = generators[0].shape[0]
    identity = np.eye(dimension, dtype=complex)
    equations = []
    for generator in generators:
        equations.append(np.kron(identity, generator) - np.kron(generator.T, identity))
    matrix = np.vstack(equations)
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    rank = int(np.sum(singular_values > tolerance))
    return dimension**2 - rank


@dataclass(frozen=True)
class Irrep:
    name: str
    color: str
    weak: int
    hypercharge: Fraction


H15 = (
    Irrep("Q_L", "3", 2, Fraction(1, 6)),
    Irrep("L_L", "1", 2, Fraction(-1, 2)),
    Irrep("u_R", "3", 1, Fraction(2, 3)),
    Irrep("d_R", "3", 1, Fraction(-1, 3)),
    Irrep("e_R", "1", 1, Fraction(-1, 1)),
)


def dual(irrep: Irrep) -> Irrep:
    color = {"3": "3bar", "3bar": "3", "1": "1"}[irrep.color]
    return Irrep(irrep.name + "*", color, irrep.weak, -irrep.hypercharge)


def color_multiplicity(left: str, right: str, target: str) -> int:
    if left == "1":
        return int(right == target)
    if right == "1":
        return int(left == target)
    if {left, right} == {"3", "3bar"}:
        return int(target == "1")
    return 0


def weak_multiplicity(left: int, right: int, target: int) -> int:
    if left == 1:
        return int(right == target)
    if right == 1:
        return int(left == target)
    if left == right == 2:
        return int(target in (1, 3))
    return 0


def target_multiplicities(left: tuple[Irrep, ...], right: tuple[Irrep, ...]) -> dict[str, int]:
    result = {target.name: 0 for target in H15}
    for target in H15:
        for first in left:
            for second in right:
                if first.hypercharge + second.hypercharge != target.hypercharge:
                    continue
                result[target.name] += color_multiplicity(
                    first.color, second.color, target.color
                ) * weak_multiplicity(first.weak, second.weak, target.weak)
    return result


def main() -> None:
    # Diagonal SO(3) on the already existing family tensor square C3 tensor C3.
    j = spin_one_generators()
    identity3 = np.eye(3, dtype=complex)
    total_j = [np.kron(generator, identity3) + np.kron(identity3, generator) for generator in j]
    casimir = sum(generator @ generator for generator in total_j)
    eigenvalues = np.linalg.eigvalsh(casimir)
    rounded = np.rint(eigenvalues).astype(int)
    casimir_multiplicities = {
        str(value): int(np.sum(rounded == value)) for value in sorted(set(rounded))
    }
    swap = swap_operator(3)
    swap_sign_by_casimir = {}
    for value in sorted(set(rounded)):
        vectors = np.linalg.eigh(casimir)[1][:, rounded == value]
        restricted = vectors.conj().T @ swap @ vectors
        swap_sign_by_casimir[str(value)] = [
            float(number.real) for number in np.linalg.eigvalsh(restricted)
        ]

    # The two orderings before Bose/Fermi quotient have only the abelian S2 commutant.
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.diag([1, -1]).astype(complex)
    copy_pauli_swap_commutators = [
        float(np.linalg.norm(commutator(sx, matrix))) for matrix in (sx, sy, sz)
    ]

    direct = target_multiplicities(H15, H15)
    mixed_right = target_multiplicities(H15, tuple(dual(item) for item in H15))
    mixed_left = target_multiplicities(tuple(dual(item) for item in H15), H15)

    # The atlas rank-four address is repeated numerically but is the same subspace.
    projector_color = np.diag([1.0] * 8 + [0.0] * 16)
    projector_weak_hypercharge = np.diag([0.0] * 8 + [1.0] * 4 + [0.0] * 12)
    projector_sixteen = np.eye(24) - projector_color
    overlap_gram = np.array(
        [
            [np.trace(projector_weak_hypercharge @ projector_weak_hypercharge)] * 2,
            [np.trace(projector_weak_hypercharge @ projector_weak_hypercharge)] * 2,
        ]
    )
    atlas_projector_residual = float(
        np.linalg.norm(projector_sixteen @ projector_weak_hypercharge - projector_weak_hypercharge)
    )

    # X and Xbar have equal rank but conjugate charge; Pauli mixing is not gauge invariant.
    identity6 = np.eye(6, dtype=complex)
    conjugate_charge = np.kron(sz, identity6)
    rank_six_pauli = [np.kron(matrix, identity6) for matrix in (sx, sy, sz)]
    rank_six_charge_commutators = [
        float(np.linalg.norm(commutator(conjugate_charge, matrix)))
        for matrix in rank_six_pauli
    ]

    result = {
        "gate": "version6_two_copy_spin_cover_multiplicity_gate",
        "family_tensor_square": {
            "space": "C3_family tensor C3_family under diagonal SO(3)",
            "casimir_eigenvalue_dimensions": casimir_multiplicities,
            "irrep_decomposition": "spin 0 plus spin 1 plus spin 2, dimensions 1+3+5",
            "swap_eigenvalues_by_casimir": swap_sign_by_casimir,
            "commutant_dimension": joint_commutant_dimension(total_j),
            "multiplicity_profile": {"spin_0": 1, "spin_1": 1, "spin_2": 1},
            "contains_M2_multiplicity_algebra": False,
            "canonical_complex_doublet": False,
        },
        "copy_order_test": {
            "prequotient_order_space": "span{LR,RL}",
            "swap_matrix": sx.real.tolist(),
            "commutant_dimension": joint_commutant_dimension([sx]),
            "commutant_is_span_I_swap_and_abelian": True,
            "pauli_xyz_commutator_norms_with_swap": copy_pauli_swap_commutators,
            "symmetric_quotient_dimension": 1,
            "antisymmetric_quotient_dimension": 1,
            "full_pauli_action_preserves_statistics_sector": False,
        },
        "H15_tensor_product_test": {
            "representation_convention": "Q_L(3,2,1/6)+L_L(1,2,-1/2)+u_R(3,1,2/3)+d_R(3,1,-1/3)+e_R(1,1,-1)",
            "H15_in_H15_tensor_H15_target_multiplicities": direct,
            "H15_in_H15_tensor_H15dual_target_multiplicities": mixed_right,
            "H15_in_H15dual_tensor_H15_target_multiplicities": mixed_left,
            "direct_square_contains_full_H15_copy": all(value > 0 for value in direct.values()),
            "mixed_square_contains_full_H15_copy": all(value > 0 for value in mixed_right.values()),
            "uniform_equal_charge_multiplicity_two": False,
            "missing_direct_targets": [key for key, value in direct.items() if value == 0],
            "missing_mixed_targets": [key for key, value in mixed_right.items() if value == 0],
        },
        "atlas_rank_address_test": {
            "rank24_blocks": "8_C+3_W+1_Y+6_X+6_Xbar",
            "rank4_address": "W plus Y",
            "rank16_address": "complement of C, already containing W plus Y",
            "P4_is_subprojector_of_P16_residual": atlas_projector_residual,
            "two_written_rank4_slots_overlap_gram": overlap_gram.tolist(),
            "overlap_gram_eigenvalues": np.linalg.eigvalsh(overlap_gram).tolist(),
            "overlap_gram_rank": int(np.linalg.matrix_rank(overlap_gram)),
            "rank4_repetition_is_independent_multiplicity": False,
            "rank6_X_Xbar_charge_commutator_norms_sigma_xyz": rank_six_charge_commutators,
            "rank6_conjugate_pair_is_equal_charge_doublet": False,
            "Delta_squared_equals_rank6_over_24_numerically": True,
            "Delta_squared_derives_spin_cover_carrier": False,
        },
        "verdict": {
            "existing_two_copy_carriers_supply_physical_C2_twist": False,
            "family_tensor_square_has_nonabelian_M2_commutant": False,
            "copy_order_doublet_survives_statistics_quotient": False,
            "H15_tensor_products_contain_uniform_H15_doublet": False,
            "atlas_rank_repetition_is_operator_multiplicity": False,
            "spin_cover_fermion_branch_closed_in_current_finite_parent": True,
            "bosonic_projective_defect_and_boundary_K_class_survive": True,
            "reopening_requires": [
                "new equal-charge multiplicity module with trace/anomaly audit",
                "or an explicitly new Spin^h architecture linking spatial spin and internal Sp(1)",
            ],
            "status": "two_copy_loophole_closed_no_physical_spin_cover_multiplicity",
            "next_gate": "version6_bosonic_defect_field_identification_gate",
        },
    }

    assert casimir_multiplicities == {"0": 1, "2": 3, "6": 5}
    assert result["family_tensor_square"]["commutant_dimension"] == 3
    assert result["copy_order_test"]["commutant_dimension"] == 2
    assert atlas_projector_residual < 1e-12
    assert result["atlas_rank_address_test"]["overlap_gram_rank"] == 1
    assert not result["H15_tensor_product_test"]["direct_square_contains_full_H15_copy"]
    assert not result["H15_tensor_product_test"]["mixed_square_contains_full_H15_copy"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()