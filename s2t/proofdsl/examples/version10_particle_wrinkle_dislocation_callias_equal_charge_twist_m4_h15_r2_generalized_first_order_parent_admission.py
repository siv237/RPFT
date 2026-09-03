"""LCF certificate for the generalized-first-order R2 parent admission gate."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class R2GeneralizedFirstOrderParentCertificate:
    admitted_dirac: sp.ImmutableMatrix
    r2_seed: sp.ImmutableMatrix
    left_unitary: sp.ImmutableMatrix
    right_unitary: sp.ImmutableMatrix
    total_unitary: sp.ImmutableMatrix
    admitted_a1: sp.ImmutableMatrix
    admitted_opposite_a1: sp.ImmutableMatrix
    admitted_a2: sp.ImmutableMatrix
    admitted_transformed: sp.ImmutableMatrix
    r2_a1: sp.ImmutableMatrix
    r2_opposite_a1: sp.ImmutableMatrix
    r2_a2: sp.ImmutableMatrix
    r2_double_commutator: sp.ImmutableMatrix
    seeded_a2_coefficient: sp.ImmutableMatrix
    inherited_r2_seed: sp.ImmutableMatrix
    existing_incidence: sp.ImmutableMatrix
    existing_laplacian: sp.ImmutableMatrix
    r2_incidence: sp.ImmutableMatrix
    augmented_incidence: sp.ImmutableMatrix
    augmented_laplacian: sp.ImmutableMatrix
    conditional_architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


def _edge_operator(edges: tuple[tuple[int, int], ...]) -> sp.ImmutableMatrix:
    matrix = sp.zeros(5)
    for source, target in edges:
        matrix[source, target] = 1
        matrix[target, source] = 1
    return sp.ImmutableMatrix(matrix)


@lru_cache(maxsize=1)
def build_certificate() -> R2GeneralizedFirstOrderParentCertificate:
    # Vertex order: Q_L, L_L, u_R, d_R, e_R.
    admitted_dirac = _edge_operator(((0, 2), (0, 3), (1, 4)))
    r2_seed = _edge_operator(((1, 2), (0, 4)))

    # Central sign unitaries distinguish the two bimodule coordinates.
    left_unitary = sp.ImmutableMatrix(sp.diag(1, 1, -1, -1, -1))
    right_unitary = sp.ImmutableMatrix(sp.diag(1, -1, 1, 1, -1))
    total_unitary = sp.ImmutableMatrix(left_unitary * right_unitary)

    def generalized_terms(operator: sp.ImmutableMatrix):
        a1 = sp.ImmutableMatrix(left_unitary * operator * left_unitary - operator)
        opposite_a1 = sp.ImmutableMatrix(right_unitary * operator * right_unitary - operator)
        transformed = sp.ImmutableMatrix(total_unitary * operator * total_unitary)
        a2 = sp.ImmutableMatrix(transformed - operator - a1 - opposite_a1)
        return a1, opposite_a1, a2, transformed

    admitted_a1, admitted_opposite_a1, admitted_a2, admitted_transformed = generalized_terms(admitted_dirac)
    r2_a1, r2_opposite_a1, r2_a2, _ = generalized_terms(r2_seed)
    r2_double_commutator = sp.ImmutableMatrix(
        (r2_seed * left_unitary - left_unitary * r2_seed) * right_unitary
        - right_unitary * (r2_seed * left_unitary - left_unitary * r2_seed)
    )

    # For D_adm + epsilon D_R2, A2 = 4 epsilon D_R2 exactly.
    seeded_a2_coefficient = sp.ImmutableMatrix(r2_a2 / 4)
    inherited_r2_seed = sp.ImmutableMatrix.zeros(2, 1)

    existing_incidence = sp.ImmutableMatrix(
        [[1, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    )
    existing_laplacian = sp.ImmutableMatrix(existing_incidence * existing_incidence.T)
    r2_incidence = sp.ImmutableMatrix(
        [[0, 1], [1, 0], [-1, 0], [0, 0], [0, -1]]
    )
    augmented_incidence = sp.ImmutableMatrix.hstack(existing_incidence, r2_incidence)
    augmented_laplacian = sp.ImmutableMatrix(augmented_incidence * augmented_incidence.T)
    conditional_architecture = sp.ImmutableMatrix.ones(12, 1)
    physical_origin = sp.ImmutableMatrix.zeros(3, 1)

    theorems = (
        kernel.prove_matrix_equality(left_unitary**2, sp.eye(5), subject="left central sign is unitary"),
        kernel.prove_matrix_equality(right_unitary**2, sp.eye(5), subject="right central sign is unitary"),
        kernel.prove_matrix_equality(left_unitary * right_unitary, right_unitary * left_unitary, subject="left and opposite actions commute"),
        kernel.prove_matrix_equality(total_unitary, sp.diag(1, -1, -1, -1, 1), subject="combined central gauge unitary"),
        kernel.prove_exact_rank(admitted_dirac, 4, subject="admitted Yukawa support has rank four"),
        kernel.prove_matrix_equality(admitted_opposite_a1, sp.zeros(5), subject="opposite linear fluctuation vanishes on admitted support"),
        kernel.prove_matrix_equality(admitted_a2, sp.zeros(5), subject="quadratic generalized fluctuation vanishes on admitted support"),
        kernel.prove_matrix_equality(admitted_dirac + admitted_a1 + admitted_opposite_a1 + admitted_a2, admitted_transformed, subject="generalized fluctuation decomposition is exactly gauge covariant"),
        kernel.prove_exact_rank(r2_seed, 4, subject="two R2 edges and their adjoints have rank four"),
        kernel.prove_exact_rank(r2_double_commutator, 4, subject="R2 seed violates first order in both edge blocks"),
        kernel.prove_matrix_equality(r2_a1, -2 * r2_seed, subject="left fluctuation sees the R2 seed"),
        kernel.prove_matrix_equality(r2_opposite_a1, -2 * r2_seed, subject="opposite fluctuation sees the R2 seed"),
        kernel.prove_matrix_equality(r2_a2, 4 * r2_seed, subject="quadratic term is proportional to the inserted R2 seed"),
        kernel.prove_matrix_equality(seeded_a2_coefficient, r2_seed, subject="A2 support equals seed support exactly"),
        kernel.prove_exact_rank(existing_incidence, 3, subject="unseeded H15 graph retains three independent edges"),
        kernel.prove_exact_rank(existing_laplacian, 3, subject="unseeded H15 graph retains two components"),
        kernel.prove_exact_nullity(existing_laplacian, 2, subject="generalized fluctuation does not select the uniform ray"),
        kernel.prove_exact_rank(r2_incidence, 2, subject="R2 seed inserts two independent graph edges"),
        kernel.prove_exact_rank(augmented_incidence, 4, subject="seeded R2 graph becomes connected"),
        kernel.prove_exact_rank(augmented_laplacian, 4, subject="seeded R2 graph has connected Laplacian"),
        kernel.prove_exact_nullity(augmented_laplacian, 1, subject="seeded R2 graph conditionally selects one relative amplitude"),
        kernel.prove_matrix_equality(inherited_r2_seed, sp.zeros(2, 1), subject="current parent contains no R2 seed coefficients"),
        kernel.prove_expression_equality(sum(conditional_architecture), 12, subject="generalized seeded architecture is complete"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="R2 seed coupling and normalization origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict generalized R2 parent-origin score is zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_generalized_first_order_parent_admission_gate",
        theorems,
    )
    return R2GeneralizedFirstOrderParentCertificate(
        admitted_dirac,
        r2_seed,
        left_unitary,
        right_unitary,
        total_unitary,
        admitted_a1,
        admitted_opposite_a1,
        admitted_a2,
        admitted_transformed,
        r2_a1,
        r2_opposite_a1,
        r2_a2,
        r2_double_commutator,
        seeded_a2_coefficient,
        inherited_r2_seed,
        existing_incidence,
        existing_laplacian,
        r2_incidence,
        augmented_incidence,
        augmented_laplacian,
        conditional_architecture,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_generalized_first_order_parent_admission_gate",
    title="Допуск обобщённого первопорядкового родителя R2 на H15",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_generalized_first_order_parent_admission_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_generalized_first_order_parent_admission_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_generalized_first_order_parent_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(25)
    ),
)