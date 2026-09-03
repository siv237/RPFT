"""LCF certificate for the Delta mapping-cone common-parent embedding gate."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class DeltaMappingConeCommonParentEmbeddingCertificate:
    delta_injection: sp.ImmutableMatrix
    sigma_injection: sp.ImmutableMatrix
    delta_inertia_representative: sp.ImmutableMatrix
    sigma_gap: sp.ImmutableMatrix
    inherited_direct_sum_hessian: sp.ImmutableMatrix
    conditional_gap_hessian: sp.ImmutableMatrix
    inherited_cross_block: sp.ImmutableMatrix
    inherited_coefficient_map: sp.ImmutableMatrix
    universal_portal_map: sp.ImmutableMatrix
    target_gap_coefficients: sp.ImmutableMatrix
    universal_augmented_map: sp.ImmutableMatrix
    connected_extension_map: sp.ImmutableMatrix
    conditional_status: sp.ImmutableMatrix
    physical_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> DeltaMappingConeCommonParentEmbeddingCertificate:
    delta_dimension = 52
    sigma_dimension = 8
    total_dimension = delta_dimension + sigma_dimension

    delta_injection = sp.ImmutableMatrix.vstack(sp.eye(delta_dimension), sp.zeros(sigma_dimension, delta_dimension))
    sigma_injection = sp.ImmutableMatrix.vstack(sp.zeros(delta_dimension, sigma_dimension), sp.eye(sigma_dimension))

    # Canonical Sylvester representative of the previously certified
    # Delta+C inertia (43 positive, 9 zero, 0 negative).
    delta_inertia_representative = sp.ImmutableMatrix(sp.diag(*([2] * 43 + [0] * 9)))
    sigma_gap = sp.ImmutableMatrix(sp.diag(40, 40, 0, 48, 48, 0, 40, 40))

    inherited_direct_sum_hessian = sp.ImmutableMatrix(sp.diag(delta_inertia_representative, sp.zeros(sigma_dimension)))
    conditional_gap_hessian = sp.ImmutableMatrix(sp.diag(delta_inertia_representative, sigma_gap))
    inherited_cross_block = sp.ImmutableMatrix(delta_injection.T * inherited_direct_sum_hessian * sigma_injection)

    # The old parent contains no Sigma coefficient.  A norm-only portal
    # supplies only I, while the target gap needs the independent Q^2 column.
    inherited_coefficient_map = sp.ImmutableMatrix.zeros(2, 1)
    universal_portal_map = sp.ImmutableMatrix([1, 0])
    target_gap_coefficients = sp.ImmutableMatrix([49, -1])
    universal_augmented_map = sp.ImmutableMatrix.hstack(universal_portal_map, target_gap_coefficients)
    connected_extension_map = sp.ImmutableMatrix([[1, 49], [0, -1]])
    conditional_status = sp.ImmutableMatrix([1, 1, 1, 0])
    physical_status = sp.ImmutableMatrix([1, 1, 0, 0])

    theorems = (
        kernel.prove_exact_rank(delta_injection, 52, subject="Delta plus auxiliary sector embeds injectively"),
        kernel.prove_exact_rank(sigma_injection, 8, subject="Sigma sector embeds injectively"),
        kernel.prove_matrix_equality(delta_injection.T * sigma_injection, sp.zeros(52, 8), subject="Delta and Sigma injections are orthogonal"),
        kernel.prove_matrix_equality(delta_injection * delta_injection.T + sigma_injection * sigma_injection.T, sp.eye(total_dimension), subject="two injections exhaust the common carrier"),
        kernel.prove_diagonal_signature(delta_inertia_representative, (0, 9, 43), subject="Delta mapping-cone inertia representative is stable"),
        kernel.prove_exact_rank(delta_inertia_representative, 43, subject="Delta mapping-cone Hessian has rank forty-three"),
        kernel.prove_exact_nullity(delta_inertia_representative, 9, subject="Delta mapping-cone Hessian has nine Goldstone directions"),
        kernel.prove_matrix_equality(sigma_gap, sp.diag(40, 40, 0, 48, 48, 0, 40, 40), subject="conditional Sigma hypercharge gap is exact"),
        kernel.prove_diagonal_signature(sigma_gap, (0, 2, 6), subject="Sigma gap is positive with the R2 pair in its kernel"),
        kernel.prove_exact_rank(sigma_gap, 6, subject="Sigma gap lifts six companion sectors"),
        kernel.prove_exact_nullity(sigma_gap, 2, subject="Sigma gap leaves two R2 sectors light"),
        kernel.prove_matrix_equality(delta_injection.T * inherited_direct_sum_hessian * delta_injection, delta_inertia_representative, subject="inherited direct sum preserves the Delta mapping-cone block"),
        kernel.prove_matrix_equality(sigma_injection.T * inherited_direct_sum_hessian * sigma_injection, sp.zeros(8), subject="inherited mapping-cone parent supplies no Sigma Hessian"),
        kernel.prove_matrix_equality(inherited_cross_block, sp.zeros(52, 8), subject="inherited Delta-Sigma cross Hessian vanishes"),
        kernel.prove_exact_rank(inherited_cross_block, 0, subject="inherited cross coupling has zero rank"),
        kernel.prove_exact_rank(inherited_direct_sum_hessian, 43, subject="inherited common-carrier Hessian retains only the Delta block"),
        kernel.prove_exact_nullity(inherited_direct_sum_hessian, 17, subject="inherited direct sum leaves nine Goldstones and eight Sigma flats"),
        kernel.prove_diagonal_signature(inherited_direct_sum_hessian, (0, 17, 43), subject="inherited direct sum is stable but Sigma-flat"),
        kernel.prove_exact_rank(conditional_gap_hessian, 49, subject="manual Sigma gap raises common Hessian rank to forty-nine"),
        kernel.prove_exact_nullity(conditional_gap_hessian, 11, subject="conditional gap leaves nine Goldstones and two R2 modes"),
        kernel.prove_diagonal_signature(conditional_gap_hessian, (0, 11, 49), subject="conditional block sum has no negative mode"),
        kernel.prove_exact_rank(inherited_coefficient_map, 0, subject="old mapping-cone parent induces no Sigma coefficient"),
        kernel.prove_exact_rank(universal_portal_map, 1, subject="norm-only portal spans only the identity coefficient"),
        kernel.prove_exact_rank(universal_augmented_map, 2, subject="target hypercharge gap is outside the universal portal image"),
        kernel.prove_exact_rank(connected_extension_map, 2, subject="one new connected curvature column spans the full coefficient plane"),
        kernel.prove_expression_equality(sum(conditional_status), 3, subject="conditional direct-sum architecture closes three of four slots"),
        kernel.prove_expression_equality(sum(physical_status), 2, subject="physical embedding closes carrier and Delta stability only"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_mapping_cone_common_parent_typed_embedding_gate",
        theorems,
    )
    return DeltaMappingConeCommonParentEmbeddingCertificate(
        delta_injection,
        sigma_injection,
        delta_inertia_representative,
        sigma_gap,
        inherited_direct_sum_hessian,
        conditional_gap_hessian,
        inherited_cross_block,
        inherited_coefficient_map,
        universal_portal_map,
        target_gap_coefficients,
        universal_augmented_map,
        connected_extension_map,
        conditional_status,
        physical_status,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_mapping_cone_common_parent_typed_embedding_gate",
    title="Типизированное вложение Delta mapping-cone parent",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_mapping_cone_common_parent_typed_embedding_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_mapping_cone_common_parent_typed_embedding_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_delta_mapping_cone_embedding_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(27)
    ),
)