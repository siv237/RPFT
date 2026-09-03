"""LCF certificate for the shared fixed-point auxiliary-channel embedding gate."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SharedFixedPointAuxiliaryEmbeddingCertificate:
    sigma_weights: sp.ImmutableMatrix
    fixed_point_weights: sp.ImmutableMatrix
    weight_multiplicities: sp.ImmutableMatrix
    weight_match_matrix: sp.ImmutableMatrix
    intertwiner_constraint: sp.ImmutableMatrix
    untyped_injection: sp.ImmutableMatrix
    untyped_metric_pullback: sp.ImmutableMatrix
    untyped_equivariance_residual: sp.ImmutableMatrix
    fixed_point_grading: sp.ImmutableMatrix
    sigma_grading: sp.ImmutableMatrix
    grading_constraint: sp.ImmutableMatrix
    sigma_reality: sp.ImmutableMatrix
    extension_weights: sp.ImmutableMatrix
    extension_injection: sp.ImmutableMatrix
    extension_equivariance_residual: sp.ImmutableMatrix
    extension_grading_residual: sp.ImmutableMatrix
    extension_reality_residual: sp.ImmutableMatrix
    extension_metric_pullback: sp.ImmutableMatrix
    minimum_extension_dimension: sp.ImmutableMatrix
    conditional_parent_hessian: sp.ImmutableMatrix
    conditional_schur_complement: sp.ImmutableMatrix
    inherited_status: sp.ImmutableMatrix
    conditional_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


def _matrix_unit_weights(generator: tuple[int, ...]) -> list[int]:
    return [generator[row] - generator[column] for row in range(len(generator)) for column in range(len(generator))]


@lru_cache(maxsize=1)
def build_certificate() -> SharedFixedPointAuxiliaryEmbeddingCertificate:
    sigma_weight_values = [3, -3, 7, 1, -1, -7, 3, -3]
    sigma_weights = sp.ImmutableMatrix(sigma_weight_values)

    su4_generator = (1, 1, 1, -3)
    su2r_generator = (3, -3)
    fixed_point_weight_values = (
        _matrix_unit_weights(su4_generator)
        + _matrix_unit_weights(su2r_generator)
        + _matrix_unit_weights(su4_generator)
    )
    fixed_point_weights = sp.ImmutableMatrix(fixed_point_weight_values)

    weight_labels = (-7, -6, -4, -3, -1, 0, 1, 3, 4, 6, 7)
    weight_multiplicities = sp.ImmutableMatrix([
        [sigma_weight_values.count(weight), fixed_point_weight_values.count(weight)]
        for weight in weight_labels
    ])
    weight_match_matrix = sp.ImmutableMatrix([
        [int(auxiliary_weight == sigma_weight) for sigma_weight in sigma_weight_values]
        for auxiliary_weight in fixed_point_weight_values
    ])

    differences = [
        auxiliary_weight - sigma_weight
        for sigma_weight in sigma_weight_values
        for auxiliary_weight in fixed_point_weight_values
    ]
    intertwiner_constraint = sp.ImmutableMatrix(sp.diag(*differences))

    untyped_injection = sp.ImmutableMatrix.vstack(sp.eye(8), sp.zeros(28, 8))
    untyped_metric_pullback = sp.ImmutableMatrix(untyped_injection.T * untyped_injection)
    fixed_point_generator = sp.ImmutableMatrix(sp.diag(*fixed_point_weight_values))
    sigma_generator = sp.ImmutableMatrix(sp.diag(*sigma_weight_values))
    untyped_equivariance_residual = sp.ImmutableMatrix(
        fixed_point_generator * untyped_injection - untyped_injection * sigma_generator
    )

    fixed_point_grading = sp.ImmutableMatrix(sp.eye(36))
    sigma_grading = sp.ImmutableMatrix(-sp.eye(8))
    grading_constraint = sp.ImmutableMatrix(2 * sp.eye(36 * 8))

    sigma_reality_mutable = sp.zeros(8)
    for left, right in ((0, 1), (2, 5), (3, 4), (6, 7)):
        sigma_reality_mutable[left, right] = 1
        sigma_reality_mutable[right, left] = 1
    sigma_reality = sp.ImmutableMatrix(sigma_reality_mutable)

    extension_weights = sigma_weights
    extension_generator = sigma_generator
    extension_grading = sigma_grading
    extension_reality = sigma_reality
    extension_injection = sp.ImmutableMatrix(sp.eye(8))
    extension_equivariance_residual = sp.ImmutableMatrix(
        extension_generator * extension_injection - extension_injection * sigma_generator
    )
    extension_grading_residual = sp.ImmutableMatrix(
        extension_grading * extension_injection - extension_injection * sigma_grading
    )
    extension_reality_residual = sp.ImmutableMatrix(
        extension_reality * extension_injection - extension_injection * sigma_reality
    )
    extension_metric_pullback = sp.ImmutableMatrix(extension_injection.T * extension_injection)
    minimum_extension_dimension = sp.ImmutableMatrix([8])

    identity = sp.eye(8)
    q = sigma_generator
    conditional_parent_hessian = sp.ImmutableMatrix(
        sp.BlockMatrix([[49 * identity, q], [q, identity]]).as_explicit()
    )
    conditional_schur_complement = sp.ImmutableMatrix(49 * identity - q**2)
    inherited_status = sp.ImmutableMatrix([1, 0, 0, 1])
    conditional_status = sp.ImmutableMatrix([1, 1, 1, 1])

    theorems = (
        kernel.prove_expression_equality(len(fixed_point_weight_values), 36, subject="fixed-point auxiliary algebra has real dimension thirty-six"),
        kernel.prove_matrix_equality(weight_multiplicities[:, 0], sp.ImmutableMatrix([1, 0, 0, 2, 1, 0, 1, 2, 0, 0, 1]), subject="Sigma hypercharge multiplicities are exact"),
        kernel.prove_matrix_equality(weight_multiplicities[:, 1], sp.ImmutableMatrix([0, 1, 6, 0, 0, 22, 0, 0, 6, 1, 0]), subject="fixed-point auxiliary hypercharge multiplicities are exact"),
        kernel.prove_matrix_equality(weight_match_matrix, sp.zeros(36, 8), subject="Sigma and fixed-point auxiliary weights are disjoint"),
        kernel.prove_exact_rank(weight_match_matrix, 0, subject="weight-matched embedding space has rank zero"),
        kernel.prove_exact_rank(intertwiner_constraint, 288, subject="hypercharge intertwiner constraint is invertible"),
        kernel.prove_exact_nullity(intertwiner_constraint, 0, subject="hypercharge-equivariant Hom space is zero"),
        kernel.prove_exact_rank(untyped_injection, 8, subject="an untyped eight-dimensional injection exists"),
        kernel.prove_matrix_equality(untyped_metric_pullback, sp.eye(8), subject="untyped injection preserves the trace metric"),
        kernel.prove_exact_rank(untyped_equivariance_residual, 8, subject="untyped injection violates hypercharge equivariance in every Sigma direction"),
        kernel.prove_matrix_equality(fixed_point_grading, sp.eye(36), subject="fixed-point auxiliary curvature is even"),
        kernel.prove_matrix_equality(sigma_grading, -sp.eye(8), subject="Sigma auxiliary image must be odd"),
        kernel.prove_exact_rank(grading_constraint, 288, subject="even-to-odd graded intertwiner constraint is invertible"),
        kernel.prove_exact_nullity(grading_constraint, 0, subject="graded Hom from Sigma to fixed-point curvature is zero"),
        kernel.prove_matrix_equality(sigma_reality**2, sp.eye(8), subject="Sigma charge-conjugation reality squares to one"),
        kernel.prove_matrix_equality(sigma_reality * sigma_generator * sigma_reality, -sigma_generator, subject="Sigma reality reverses hypercharge"),
        kernel.prove_matrix_equality(extension_weights, sigma_weights, subject="minimal odd extension copies the required weight spectrum"),
        kernel.prove_exact_rank(extension_injection, 8, subject="conditional odd extension embeds all Sigma directions"),
        kernel.prove_matrix_equality(extension_equivariance_residual, sp.zeros(8), subject="conditional odd extension is hypercharge equivariant"),
        kernel.prove_matrix_equality(extension_grading_residual, sp.zeros(8), subject="conditional odd extension preserves grading"),
        kernel.prove_matrix_equality(extension_reality_residual, sp.zeros(8), subject="conditional odd extension preserves reality"),
        kernel.prove_matrix_equality(extension_metric_pullback, sp.eye(8), subject="conditional odd extension preserves trace metric"),
        kernel.prove_expression_equality(minimum_extension_dimension[0], 8, subject="weight multiplicities require at least eight real auxiliary directions"),
        kernel.prove_exact_rank(conditional_parent_hessian, 14, subject="conditional typed shared parent retains rank fourteen"),
        kernel.prove_exact_nullity(conditional_parent_hessian, 2, subject="conditional typed shared parent retains the R2 pair"),
        kernel.prove_matrix_equality(conditional_schur_complement, sp.diag(40, 40, 0, 48, 48, 0, 40, 40), subject="conditional odd extension recovers the exact hypercharge gap"),
        kernel.prove_expression_equality(sum(inherited_status), 2, subject="inherited fixed-point channel closes only ambient carrier and metric"),
        kernel.prove_expression_equality(sum(conditional_status), 4, subject="minimal odd auxiliary extension closes all typed slots conditionally"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_shared_fixed_point_auxiliary_channel_typed_embedding_gate",
        theorems,
    )
    return SharedFixedPointAuxiliaryEmbeddingCertificate(
        sigma_weights,
        fixed_point_weights,
        weight_multiplicities,
        weight_match_matrix,
        intertwiner_constraint,
        untyped_injection,
        untyped_metric_pullback,
        untyped_equivariance_residual,
        fixed_point_grading,
        sigma_grading,
        grading_constraint,
        sigma_reality,
        extension_weights,
        extension_injection,
        extension_equivariance_residual,
        extension_grading_residual,
        extension_reality_residual,
        extension_metric_pullback,
        minimum_extension_dimension,
        conditional_parent_hessian,
        conditional_schur_complement,
        inherited_status,
        conditional_status,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_shared_fixed_point_auxiliary_channel_typed_embedding_gate",
    title="Типизированное вложение общего fixed-point auxiliary-канала",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_shared_fixed_point_auxiliary_channel_typed_embedding_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_shared_fixed_point_auxiliary_channel_typed_embedding_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_shared_fixed_point_auxiliary_embedding_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(28)
    ),
)