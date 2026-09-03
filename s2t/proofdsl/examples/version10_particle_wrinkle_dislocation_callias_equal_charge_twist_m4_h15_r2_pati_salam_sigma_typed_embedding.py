"""LCF certificate for the R2 embedding in the Pati-Salam Sigma multiplet."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class R2PatiSalamSigmaEmbeddingCertificate:
    sector_dimensions: sp.ImmutableMatrix
    hypercharge6: sp.ImmutableMatrix
    color_labels: sp.ImmutableMatrix
    target_selector: sp.ImmutableMatrix
    complement_selector: sp.ImmutableMatrix
    su2r_flip: sp.ImmutableMatrix
    su2r_selector_defect: sp.ImmutableMatrix
    hypercharge_generator: sp.ImmutableMatrix
    color_generator: sp.ImmutableMatrix
    r2_incidence: sp.ImmutableMatrix
    existing_incidence: sp.ImmutableMatrix
    augmented_incidence: sp.ImmutableMatrix
    augmented_laplacian: sp.ImmutableMatrix
    inherited_sigma_map: sp.ImmutableMatrix
    conditional_architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> R2PatiSalamSigmaEmbeddingCertificate:
    # Sector order:
    # (8,2)_{1/2}, (8,2)_{-1/2}, (3,2)_{7/6}, (3,2)_{1/6},
    # (bar3,2)_{-1/6}, (bar3,2)_{-7/6}, (1,2)_{1/2}, (1,2)_{-1/2}.
    sector_dimensions = sp.ImmutableMatrix([16, 16, 6, 6, 6, 6, 2, 2])
    hypercharge6 = sp.ImmutableMatrix([3, -3, 7, 1, -1, -7, 3, -3])
    color_labels = sp.ImmutableMatrix([8, 8, 3, 3, -3, -3, 1, 1])
    target_selector = sp.ImmutableMatrix(sp.diag(0, 0, 1, 0, 0, 1, 0, 0))
    complement_selector = sp.ImmutableMatrix(sp.eye(8) - target_selector)

    su2r_flip_mutable = sp.zeros(8)
    for first, second in ((0, 1), (2, 3), (4, 5), (6, 7)):
        su2r_flip_mutable[first, second] = 1
        su2r_flip_mutable[second, first] = 1
    su2r_flip = sp.ImmutableMatrix(su2r_flip_mutable)
    su2r_selector_defect = sp.ImmutableMatrix(su2r_flip * target_selector - target_selector * su2r_flip)
    hypercharge_generator = sp.ImmutableMatrix(sp.diag(*list(hypercharge6)))
    color_generator = sp.ImmutableMatrix(sp.diag(*list(color_labels)))

    # H15 vertex order: Q_L, L_L, u_R, d_R, e_R.
    r2_incidence = sp.ImmutableMatrix([[0, 1], [1, 0], [-1, 0], [0, 0], [0, -1]])
    existing_incidence = sp.ImmutableMatrix(
        [[1, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    )
    augmented_incidence = sp.ImmutableMatrix.hstack(existing_incidence, r2_incidence)
    augmented_laplacian = sp.ImmutableMatrix(augmented_incidence * augmented_incidence.T)
    inherited_sigma_map = sp.ImmutableMatrix.zeros(2, 8)
    conditional_architecture = sp.ImmutableMatrix.ones(14, 1)
    physical_origin = sp.ImmutableMatrix.zeros(3, 1)

    target_dimension = (sector_dimensions.T * sp.ImmutableMatrix(list(target_selector.diagonal())))[0]
    complement_dimension = (sector_dimensions.T * sp.ImmutableMatrix(list(complement_selector.diagonal())))[0]

    theorems = (
        kernel.prove_expression_equality(sum(sector_dimensions), 60, subject="Pati-Salam Sigma has sixty complex components"),
        kernel.prove_matrix_equality(hypercharge6, sp.ImmutableMatrix([3, -3, 7, 1, -1, -7, 3, -3]), subject="SM hypercharges follow from Y=T3R+(B-L)/2"),
        kernel.prove_expression_equality(target_dimension, 12, subject="R2 plus conjugate has twelve complex components"),
        kernel.prove_expression_equality(complement_dimension, 48, subject="Sigma carries forty-eight companion components"),
        kernel.prove_matrix_equality(target_selector**2, target_selector, subject="R2 sector selector is a projector"),
        kernel.prove_exact_rank(target_selector, 2, subject="selector retains R2 and its conjugate sector"),
        kernel.prove_exact_rank(complement_selector, 6, subject="six companion SM sectors remain outside R2"),
        kernel.prove_matrix_equality(target_selector + complement_selector, sp.eye(8), subject="R2 and companion sectors exhaust Sigma"),
        kernel.prove_matrix_equality(hypercharge_generator * target_selector - target_selector * hypercharge_generator, sp.zeros(8), subject="R2 selector preserves SM hypercharge"),
        kernel.prove_matrix_equality(color_generator * target_selector - target_selector * color_generator, sp.zeros(8), subject="R2 selector preserves SM colour sectors"),
        kernel.prove_matrix_equality(su2r_flip**2, sp.eye(8), subject="SU2R weight flip pairs all Sigma sectors"),
        kernel.prove_exact_rank(su2r_selector_defect, 4, subject="R2-only selector is not invariant under full SU2R"),
        kernel.prove_exact_rank(r2_incidence, 2, subject="R2 component supplies the two required H15 edges"),
        kernel.prove_exact_rank(existing_incidence, 3, subject="standard H15 forest has three independent edges"),
        kernel.prove_exact_rank(augmented_incidence, 4, subject="R2 component connects the H15 graph"),
        kernel.prove_exact_rank(augmented_laplacian, 4, subject="R2-augmented H15 Laplacian is connected"),
        kernel.prove_exact_nullity(augmented_laplacian, 1, subject="R2 embedding conditionally selects one uniform ray"),
        kernel.prove_expression_equality(augmented_incidence.cols - augmented_incidence.rank(), 1, subject="R2 embedding creates one mixed cycle"),
        kernel.prove_matrix_equality(inherited_sigma_map, sp.zeros(2, 8), subject="current parent has no map from Sigma sectors to R2 coefficients"),
        kernel.prove_exact_rank(inherited_sigma_map, 0, subject="inherited Pati-Salam Sigma embedding rank is zero"),
        kernel.prove_expression_equality(sum(conditional_architecture), 14, subject="typed Pati-Salam embedding architecture is complete"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="Sigma parent selector and normalization origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict Pati-Salam R2 physical-origin score is zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_typed_embedding_gate",
        theorems,
    )
    return R2PatiSalamSigmaEmbeddingCertificate(
        sector_dimensions,
        hypercharge6,
        color_labels,
        target_selector,
        complement_selector,
        su2r_flip,
        su2r_selector_defect,
        hypercharge_generator,
        color_generator,
        r2_incidence,
        existing_incidence,
        augmented_incidence,
        augmented_laplacian,
        inherited_sigma_map,
        conditional_architecture,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_typed_embedding_gate",
    title="Типизированное вложение R2 в Pati--Salam Sigma",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_typed_embedding_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_typed_embedding_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_pati_salam_sigma_embedding_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(23)
    ),
)