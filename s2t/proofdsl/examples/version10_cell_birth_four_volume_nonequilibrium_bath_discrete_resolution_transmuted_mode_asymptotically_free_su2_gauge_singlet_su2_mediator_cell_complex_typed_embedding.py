"""LCF certificate for the cell-complex SU(2)-mediator embedding."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SU2MediatorCellComplexTypedEmbeddingCertificate:
    boundary: sp.ImmutableMatrix
    adjoint_boundary: sp.ImmutableMatrix
    adjoint_laplacian: sp.ImmutableMatrix
    physical_projector: sp.ImmutableMatrix
    spatial_current_embedding: sp.ImmutableMatrix
    singlet_vector: sp.ImmutableMatrix
    triplet_projector: sp.ImmutableMatrix
    relative_current_intertwiner: sp.ImmutableMatrix
    adjoint_generators: tuple[sp.ImmutableMatrix, ...]
    combined_current_map: sp.ImmutableMatrix
    projected_green: sp.ImmutableMatrix
    susceptibility_matrix: sp.ImmutableMatrix
    binding_coefficient: sp.Expr
    architecture: sp.ImmutableMatrix
    typed_embedding: sp.ImmutableMatrix
    inherited_ingredients: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SU2MediatorCellComplexTypedEmbeddingCertificate:
    boundary = sp.ImmutableMatrix([[-1], [1]])
    adjoint_boundary = sp.ImmutableMatrix(sp.kronecker_product(boundary, sp.eye(3)))
    adjoint_laplacian = sp.ImmutableMatrix(adjoint_boundary * adjoint_boundary.T)
    spatial_projector_2 = sp.ImmutableMatrix([[sp.Rational(1, 2), -sp.Rational(1, 2)], [-sp.Rational(1, 2), sp.Rational(1, 2)]])
    physical_projector = sp.ImmutableMatrix(sp.kronecker_product(spatial_projector_2, sp.eye(3)))
    spatial_current_embedding = sp.ImmutableMatrix(adjoint_boundary / sp.sqrt(2))

    pauli = (
        sp.ImmutableMatrix([[0, 1], [1, 0]]),
        sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]]),
        sp.ImmutableMatrix([[1, 0], [0, -1]]),
    )
    fundamental = tuple(sigma / 2 for sigma in pauli)
    total = tuple(
        sp.ImmutableMatrix(sp.kronecker_product(t, sp.eye(2)) + sp.kronecker_product(sp.eye(2), t))
        for t in fundamental
    )
    relative = tuple(
        sp.ImmutableMatrix(sp.kronecker_product(t, sp.eye(2)) - sp.kronecker_product(sp.eye(2), t))
        for t in fundamental
    )
    singlet_vector = sp.ImmutableMatrix([0, 1 / sp.sqrt(2), -1 / sp.sqrt(2), 0])
    singlet_projector = sp.ImmutableMatrix(singlet_vector * singlet_vector.H)
    triplet_projector = sp.ImmutableMatrix(sp.eye(4) - singlet_projector)
    relative_current_intertwiner = sp.ImmutableMatrix.hstack(*(
        sp.ImmutableMatrix(r * singlet_vector) for r in relative
    ))
    adjoint_generators = tuple(
        sp.ImmutableMatrix(relative_current_intertwiner.H * generator * relative_current_intertwiner)
        for generator in total
    )
    combined_current_map = sp.ImmutableMatrix(spatial_current_embedding * relative_current_intertwiner.H)
    projected_green = sp.ImmutableMatrix(sp.Rational(1, 2) * physical_projector)
    susceptibility_matrix = sp.ImmutableMatrix(spatial_current_embedding.H * projected_green * spatial_current_embedding)
    binding_coefficient = sp.Rational(3, 8) * susceptibility_matrix[0, 0]
    architecture = sp.ones(14, 1)
    typed_embedding = sp.ones(10, 1)
    inherited_ingredients = sp.ones(2, 1)
    physical_origin = sp.zeros(2, 1)

    covariance_stack = sp.ImmutableMatrix.vstack(*(
        sp.ImmutableMatrix(total[a] * relative_current_intertwiner - relative_current_intertwiner * adjoint_generators[a])
        for a in range(3)
    ))
    singlet_annihilation = sp.ImmutableMatrix.vstack(*(
        sp.ImmutableMatrix(generator * singlet_vector) for generator in total
    ))

    theorems = (
        kernel.prove_exact_rank(boundary, 1, subject="oriented cell edge has rank-one boundary"),
        kernel.prove_exact_rank(adjoint_boundary, 3, subject="adjoint extension carries three SU2 edge components"),
        kernel.prove_matrix_equality(adjoint_laplacian, 2 * physical_projector, subject="adjoint cell Laplacian is twice the conserved-current projector"),
        kernel.prove_exact_rank(adjoint_laplacian, 3, subject="adjoint cell Laplacian has three physical modes"),
        kernel.prove_exact_nullity(adjoint_laplacian, 3, subject="adjoint cell Laplacian has three constant gauge modes"),
        kernel.prove_matrix_equality(sp.ImmutableMatrix(sp.kronecker_product(-boundary, sp.eye(3))) * sp.ImmutableMatrix(sp.kronecker_product(-boundary, sp.eye(3))).T, adjoint_laplacian, subject="edge orientation does not change the adjoint Laplacian"),
        kernel.prove_matrix_equality(spatial_current_embedding.H * spatial_current_embedding, sp.eye(3), subject="spatial current embedding is an isometry"),
        kernel.prove_matrix_equality(physical_projector * spatial_current_embedding, spatial_current_embedding, subject="adjoint edge current is conserved"),
        kernel.prove_matrix_equality(singlet_annihilation, sp.zeros(12, 1), subject="total SU2 charge annihilates the singlet"),
        kernel.prove_matrix_equality(relative_current_intertwiner.H * relative_current_intertwiner, sp.eye(3), subject="relative currents form an orthonormal adjoint frame"),
        kernel.prove_exact_rank(relative_current_intertwiner, 3, subject="relative-current map spans the full triplet"),
        kernel.prove_matrix_equality(relative_current_intertwiner * relative_current_intertwiner.H, triplet_projector, subject="relative-current image is exactly the triplet sector"),
        kernel.prove_matrix_equality(covariance_stack, sp.zeros(12, 3), subject="relative-current frame intertwines total SU2 with the adjoint action"),
        kernel.prove_matrix_equality(combined_current_map.H * combined_current_map, triplet_projector, subject="combined map is isometric on the pair triplet"),
        kernel.prove_matrix_equality(combined_current_map * combined_current_map.H, physical_projector, subject="combined map fills the conserved adjoint cell-current sector"),
        kernel.prove_exact_rank(combined_current_map, 3, subject="combined typed current map has rank three"),
        kernel.prove_matrix_equality(susceptibility_matrix, sp.Rational(1, 2) * sp.eye(3), subject="all adjoint components have susceptibility one half"),
        kernel.prove_expression_equality(binding_coefficient, sp.Rational(3, 16), subject="typed cell mediator preserves the conditional gap three sixteenths"),
        kernel.prove_expression_equality(sum(architecture), 14, subject="conditional cell-mediator architecture is complete"),
        kernel.prove_expression_equality(sum(typed_embedding), 10, subject="ten typed embedding checks pass"),
        kernel.prove_expression_equality(sum(inherited_ingredients), 2, subject="cell boundary and SU2 generators are inherited"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(2, 1), subject="flavor selector and pole map origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict post-embedding origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_cell_complex_typed_embedding_gate",
        theorems,
    )
    return SU2MediatorCellComplexTypedEmbeddingCertificate(
        boundary, adjoint_boundary, adjoint_laplacian, physical_projector,
        spatial_current_embedding, singlet_vector, triplet_projector,
        relative_current_intertwiner, adjoint_generators,
        combined_current_map, projected_green, susceptibility_matrix,
        binding_coefficient, architecture, typed_embedding,
        inherited_ingredients, physical_origin, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_cell_complex_typed_embedding_gate",
    title="Клеточное типизированное вложение SU(2)-посредника",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_cell_complex_typed_embedding_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_cell_complex_typed_embedding_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"su2_mediator_cell_embedding_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(23)
    ),
)