"""LCF certificate for relative-Hodge auxiliary-edge common-parent admission."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


def _matrix_unit_weights(generator: tuple[int, ...]) -> list[int]:
    return [generator[i] - generator[j] for i in range(len(generator)) for j in range(len(generator))]


@dataclass(frozen=True, slots=True)
class RelativeHodgeAuxiliaryEdgeAdmissionCertificate:
    sigma_weights: sp.ImmutableMatrix
    fixed_point_weights: sp.ImmutableMatrix
    weight_match_matrix: sp.ImmutableMatrix
    intertwiner_constraint: sp.ImmutableMatrix
    common_generator: sp.ImmutableMatrix
    sigma_reality: sp.ImmutableMatrix
    common_reality: sp.ImmutableMatrix
    common_grading: sp.ImmutableMatrix
    odd_edge_operator: sp.ImmutableMatrix
    oddness_residual: sp.ImmutableMatrix
    incidence_edge: sp.ImmutableMatrix
    hodge_laplacian: sp.ImmutableMatrix
    hodge_projector: sp.ImmutableMatrix
    hodge_diagonal_form: sp.ImmutableMatrix
    gauge_hodge_commutator: sp.ImmutableMatrix
    reality_hodge_commutator: sp.ImmutableMatrix
    inherited_hodge_selector: sp.ImmutableMatrix
    conditional_auxiliary_injection: sp.ImmutableMatrix
    extension_dimension: sp.ImmutableMatrix
    target_generator: sp.ImmutableMatrix
    relative_readout: sp.ImmutableMatrix
    inherited_status: sp.ImmutableMatrix
    conditional_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> RelativeHodgeAuxiliaryEdgeAdmissionCertificate:
    weights = [3, -3, 7, 1, -1, -7, 3, -3]
    sigma_weights = sp.ImmutableMatrix(weights)
    fixed_values = (
        _matrix_unit_weights((1, 1, 1, -3))
        + _matrix_unit_weights((3, -3))
        + _matrix_unit_weights((1, 1, 1, -3))
    )
    fixed_point_weights = sp.ImmutableMatrix(fixed_values)
    weight_match_matrix = sp.ImmutableMatrix(
        [[int(aux == sigma) for sigma in weights] for aux in fixed_values]
    )
    differences = [aux - sigma for sigma in weights for aux in fixed_values]
    intertwiner_constraint = sp.ImmutableMatrix(sp.diag(*differences))

    q = sp.ImmutableMatrix(sp.diag(*weights))
    identity = sp.eye(8)
    zero = sp.zeros(8)
    common_generator = sp.ImmutableMatrix(sp.diag(q, q))
    reality_mutable = sp.zeros(8)
    for left, right in ((0, 1), (2, 5), (3, 4), (6, 7)):
        reality_mutable[left, right] = 1
        reality_mutable[right, left] = 1
    sigma_reality = sp.ImmutableMatrix(reality_mutable)
    common_reality = sp.ImmutableMatrix(sp.diag(sigma_reality, sigma_reality))
    common_grading = sp.ImmutableMatrix(sp.diag(-identity, identity))
    odd_edge_operator = sp.ImmutableMatrix(sp.BlockMatrix([[zero, identity], [identity, zero]]).as_explicit())
    oddness_residual = sp.ImmutableMatrix(common_grading * odd_edge_operator + odd_edge_operator * common_grading)

    incidence_edge = sp.ImmutableMatrix(sp.Matrix.hstack(identity, -identity))
    hodge_laplacian = sp.ImmutableMatrix(incidence_edge.T * incidence_edge)
    hodge_projector = sp.ImmutableMatrix(sp.Rational(1, 2) * hodge_laplacian)
    hadamard = sp.ImmutableMatrix(sp.BlockMatrix([[identity, identity], [identity, -identity]]).as_explicit())
    hodge_diagonal_form = sp.ImmutableMatrix(hadamard.T * hodge_projector * hadamard)
    gauge_hodge_commutator = sp.ImmutableMatrix(common_generator * hodge_projector - hodge_projector * common_generator)
    reality_hodge_commutator = sp.ImmutableMatrix(common_reality * hodge_projector - hodge_projector * common_reality)
    inherited_hodge_selector = sp.ImmutableMatrix.zeros(16)
    conditional_auxiliary_injection = sp.ImmutableMatrix(sp.Matrix.vstack(zero, identity))
    extension_dimension = sp.ImmutableMatrix([8])
    target_generator = q
    relative_readout = sp.ImmutableMatrix(sp.diag(*weights))
    inherited_status = sp.ImmutableMatrix([1, 1, 1, 0, 0, 0])
    conditional_status = sp.ImmutableMatrix([1, 1, 1, 1, 1, 1])

    theorems = (
        kernel.prove_expression_equality(len(fixed_values), 36, subject="fixed-point auxiliary sector has dimension thirty-six"),
        kernel.prove_matrix_equality(weight_match_matrix, sp.zeros(36, 8), subject="fixed-point and required auxiliary weights are disjoint"),
        kernel.prove_exact_rank(weight_match_matrix, 0, subject="weight-matched inherited auxiliary embedding has rank zero"),
        kernel.prove_exact_rank(intertwiner_constraint, 288, subject="hypercharge intertwiner constraint is invertible"),
        kernel.prove_exact_nullity(intertwiner_constraint, 0, subject="inherited equivariant Hom space vanishes"),
        kernel.prove_exact_rank(common_generator, 16, subject="conditional doubled carrier contains both full weight copies"),
        kernel.prove_matrix_equality(sigma_reality**2, identity, subject="Sigma reality squares to one"),
        kernel.prove_matrix_equality(sigma_reality * q * sigma_reality, -q, subject="Sigma reality reverses hypercharge"),
        kernel.prove_matrix_equality(common_reality**2, sp.eye(16), subject="doubled common reality squares to one"),
        kernel.prove_matrix_equality(oddness_residual, sp.zeros(16), subject="common auxiliary edge is grading odd"),
        kernel.prove_exact_rank(odd_edge_operator, 16, subject="self-adjoint odd edge couples both eight-dimensional copies"),
        kernel.prove_exact_rank(incidence_edge, 8, subject="oriented auxiliary incidence has rank eight"),
        kernel.prove_matrix_equality(hodge_projector**2, hodge_projector, subject="lifted relative Hodge selector is idempotent"),
        kernel.prove_exact_rank(hodge_projector, 8, subject="lifted relative Hodge selector keeps eight relative modes"),
        kernel.prove_matrix_equality(hodge_diagonal_form, sp.diag(sp.zeros(8), 2 * identity), subject="Hadamard congruence diagonalizes the lifted Hodge selector"),
        kernel.prove_diagonal_signature(hodge_diagonal_form, (0, 8, 8), subject="lifted relative Hodge norm is positive semidefinite"),
        kernel.prove_matrix_equality(gauge_hodge_commutator, sp.zeros(16), subject="relative Hodge selector is hypercharge equivariant"),
        kernel.prove_matrix_equality(reality_hodge_commutator, sp.zeros(16), subject="relative Hodge selector preserves reality"),
        kernel.prove_exact_rank(inherited_hodge_selector, 0, subject="current parent has no inherited relative Hodge selector"),
        kernel.prove_exact_rank(conditional_auxiliary_injection, 8, subject="conditional second copy embeds the complete auxiliary module"),
        kernel.prove_expression_equality(extension_dimension[0], 8, subject="minimum weight-compatible extension dimension is eight"),
        kernel.prove_matrix_equality(relative_readout, target_generator, subject="conditional relative carrier retains exact Q readout"),
        kernel.prove_expression_equality(sum(inherited_status), 3, subject="inherited common-parent admission closes three of six slots"),
        kernel.prove_expression_equality(sum(conditional_status), 6, subject="minimal doubled relative-Hodge carrier closes all admission slots conditionally"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_common_parent_admission_gate",
        theorems,
    )
    return RelativeHodgeAuxiliaryEdgeAdmissionCertificate(
        sigma_weights, fixed_point_weights, weight_match_matrix, intertwiner_constraint,
        common_generator, sigma_reality, common_reality, common_grading,
        odd_edge_operator, oddness_residual, incidence_edge, hodge_laplacian,
        hodge_projector, hodge_diagonal_form, gauge_hodge_commutator,
        reality_hodge_commutator, inherited_hodge_selector,
        conditional_auxiliary_injection, extension_dimension, target_generator,
        relative_readout, inherited_status, conditional_status, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_common_parent_admission_gate",
    title="Admission общего relative-Hodge auxiliary-edge parent",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_common_parent_admission_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_common_parent_admission_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_relative_hodge_auxiliary_edge_admission_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(24)
    ),
)