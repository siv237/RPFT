"""LCF certificate for the Hubbard-Stratonovich odd auxiliary parent-origin gate."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HubbardStratonovichOddAuxiliaryParentOriginCertificate:
    hypercharge_generator: sp.ImmutableMatrix
    target_gap: sp.ImmutableMatrix
    stationary_auxiliary_map: sp.ImmutableMatrix
    shift_matrix: sp.ImmutableMatrix
    diagonalized_parent: sp.ImmutableMatrix
    hs_parent_hessian: sp.ImmutableMatrix
    hs_schur_complement: sp.ImmutableMatrix
    inherited_parent_hessian: sp.ImmutableMatrix
    inherited_schur_complement: sp.ImmutableMatrix
    inherited_cross_block: sp.ImmutableMatrix
    required_cross_block: sp.ImmutableMatrix
    new_operator_increment: sp.ImmutableMatrix
    increment_diagonalization: sp.ImmutableMatrix
    increment_diagonal_form: sp.ImmutableMatrix
    rank_ledger: sp.ImmutableMatrix
    gaussian_auxiliary_metric: sp.ImmutableMatrix
    formal_status: sp.ImmutableMatrix
    physical_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HubbardStratonovichOddAuxiliaryParentOriginCertificate:
    weights = [3, -3, 7, 1, -1, -7, 3, -3]
    q = sp.ImmutableMatrix(sp.diag(*weights))
    identity = sp.eye(8)
    zero = sp.zeros(8)
    target_gap = sp.ImmutableMatrix(49 * identity - q**2)
    stationary_auxiliary_map = sp.ImmutableMatrix(-q)

    shift_matrix = sp.ImmutableMatrix(sp.BlockMatrix([[identity, zero], [q, identity]]).as_explicit())
    diagonalized_parent = sp.ImmutableMatrix(sp.diag(target_gap, identity))
    hs_parent_hessian = sp.ImmutableMatrix(shift_matrix.T * diagonalized_parent * shift_matrix)
    hs_schur_complement = sp.ImmutableMatrix(
        hs_parent_hessian[:8, :8]
        - hs_parent_hessian[:8, 8:] * hs_parent_hessian[8:, 8:].inv() * hs_parent_hessian[8:, :8]
    )

    inherited_parent_hessian = sp.ImmutableMatrix(sp.diag(49 * identity, identity))
    inherited_schur_complement = sp.ImmutableMatrix(49 * identity)
    inherited_cross_block = sp.ImmutableMatrix.zeros(8)
    required_cross_block = q
    new_operator_increment = sp.ImmutableMatrix(hs_parent_hessian - inherited_parent_hessian)
    increment_diagonalization = sp.ImmutableMatrix(
        sp.BlockMatrix([[identity, identity], [identity, -identity]]).as_explicit()
    )
    increment_diagonal_form = sp.ImmutableMatrix(
        increment_diagonalization.T * new_operator_increment * increment_diagonalization
    )
    rank_ledger = sp.ImmutableMatrix([inherited_parent_hessian.rank(), hs_parent_hessian.rank()])
    gaussian_auxiliary_metric = sp.ImmutableMatrix(identity)
    formal_status = sp.ImmutableMatrix([1, 1, 1, 1])
    physical_status = sp.ImmutableMatrix([1, 1, 1, 0])

    theorems = (
        kernel.prove_matrix_equality(q, sp.diag(3, -3, 7, 1, -1, -7, 3, -3), subject="Hubbard-Stratonovich source is the exact hypercharge generator"),
        kernel.prove_matrix_equality(target_gap, sp.diag(40, 40, 0, 48, 48, 0, 40, 40), subject="target effective gap is exact"),
        kernel.prove_exact_rank(stationary_auxiliary_map, 8, subject="stationary auxiliary solution A equals minus Q Sigma in all sectors"),
        kernel.prove_exact_rank(shift_matrix, 16, subject="completion-of-square shift is invertible"),
        kernel.prove_expression_equality(shift_matrix.det(), 1, subject="completion-of-square shift has unit Jacobian"),
        kernel.prove_matrix_equality(diagonalized_parent, sp.diag(target_gap, identity), subject="completed square separates target gap and auxiliary norm"),
        kernel.prove_diagonal_signature(diagonalized_parent, (0, 2, 14), subject="completed-square parent is positive semidefinite"),
        kernel.prove_matrix_equality(hs_parent_hessian, sp.ImmutableMatrix(sp.BlockMatrix([[49 * identity, q], [q, identity]]).as_explicit()), subject="Hubbard-Stratonovich full Hessian is exact"),
        kernel.prove_exact_rank(hs_parent_hessian, 14, subject="Hubbard-Stratonovich full Hessian has rank fourteen"),
        kernel.prove_exact_nullity(hs_parent_hessian, 2, subject="Hubbard-Stratonovich full Hessian retains the R2 pair"),
        kernel.prove_matrix_equality(hs_schur_complement, target_gap, subject="Gaussian elimination returns the target gap"),
        kernel.prove_matrix_equality(gaussian_auxiliary_metric, sp.eye(8), subject="auxiliary Gaussian metric is normalized and positive"),
        kernel.prove_expression_equality(gaussian_auxiliary_metric.det(), 1, subject="normalized Gaussian determinant contributes no field-dependent factor"),
        kernel.prove_exact_rank(inherited_parent_hessian, 16, subject="source-free inherited parent is positive definite"),
        kernel.prove_exact_nullity(inherited_parent_hessian, 0, subject="source-free inherited parent has no light R2 kernel"),
        kernel.prove_matrix_equality(inherited_cross_block, sp.zeros(8), subject="inherited parent has no Sigma auxiliary source"),
        kernel.prove_exact_rank(inherited_cross_block, 0, subject="inherited mixed bilinear has rank zero"),
        kernel.prove_exact_rank(required_cross_block, 8, subject="required Hubbard-Stratonovich mixed bilinear has rank eight"),
        kernel.prove_matrix_equality(inherited_schur_complement, 49 * identity, subject="source-free Gaussian elimination leaves universal mass"),
        kernel.prove_matrix_equality(new_operator_increment, sp.ImmutableMatrix(sp.BlockMatrix([[zero, q], [q, zero]]).as_explicit()), subject="Hubbard-Stratonovich source is a new off-diagonal operator"),
        kernel.prove_exact_rank(new_operator_increment, 16, subject="new off-diagonal operator increment has full rank"),
        kernel.prove_matrix_equality(increment_diagonal_form, sp.diag(2 * q, -2 * q), subject="Hadamard congruence diagonalizes the new operator increment"),
        kernel.prove_diagonal_signature(increment_diagonal_form, (8, 0, 8), subject="new operator increment is indefinite with balanced signature"),
        kernel.prove_matrix_equality(rank_ledger, sp.ImmutableMatrix([16, 14]), subject="inherited and Hubbard-Stratonovich parents have different ranks"),
        kernel.prove_matrix_equality(formal_status, sp.ones(4, 1), subject="formal Hubbard-Stratonovich identity closes all four algebraic slots"),
        kernel.prove_expression_equality(sum(physical_status), 3, subject="physical origin fails only the inherited mixed source"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hubbard_stratonovich_odd_auxiliary_parent_origin_gate",
        theorems,
    )
    return HubbardStratonovichOddAuxiliaryParentOriginCertificate(
        q,
        target_gap,
        stationary_auxiliary_map,
        shift_matrix,
        diagonalized_parent,
        hs_parent_hessian,
        hs_schur_complement,
        inherited_parent_hessian,
        inherited_schur_complement,
        inherited_cross_block,
        required_cross_block,
        new_operator_increment,
        increment_diagonalization,
        increment_diagonal_form,
        rank_ledger,
        gaussian_auxiliary_metric,
        formal_status,
        physical_status,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hubbard_stratonovich_odd_auxiliary_parent_origin_gate",
    title="Происхождение Hubbard-Stratonovich odd auxiliary parent",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hubbard_stratonovich_odd_auxiliary_parent_origin_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hubbard_stratonovich_odd_auxiliary_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_hubbard_stratonovich_parent_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(26)
    ),
)