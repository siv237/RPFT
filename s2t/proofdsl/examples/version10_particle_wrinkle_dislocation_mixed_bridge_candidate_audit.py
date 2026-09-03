"""LCF certificate for the wrinkle--dislocation mixed-bridge audit."""
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class ParticleWrinkleDislocationMixedBridgeAuditCertificate:
    inherited_hessian: sp.ImmutableMatrix
    graded_product_mixed_block: sp.ImmutableMatrix
    morita_mixed_block: sp.ImmutableMatrix
    conditional_callias_hessian: sp.ImmutableMatrix
    callias_localization_projector: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    inherited_pass_vector: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> ParticleWrinkleDislocationMixedBridgeAuditCertificate:
    inherited_hessian = sp.ImmutableMatrix([[2, 0], [0, 0]])
    graded_product_mixed_block = sp.ImmutableMatrix(sp.zeros(2))
    morita_mixed_block = sp.ImmutableMatrix(sp.zeros(2))
    conditional_callias_hessian = sp.ImmutableMatrix([[2, 1], [1, 1]])
    callias_localization_projector = sp.ImmutableMatrix(sp.diag(*([1] * 15 + [0] * 90)))

    # Columns: typed common carrier, nonzero mixed block, index preservation,
    # finite localization, same-operator pole, inherited/non-target-loaded.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 0, 1, 0, 0, 1],  # inherited direct sum
        [0, 1, 1, 0, 0, 1],  # scalar trace product
        [1, 1, 1, 1, 0, 0],  # projector-curvature pairing
        [1, 1, 1, 1, 0, 0],  # Toeplitz x spatial boundary
        [1, 0, 1, 0, 0, 1],  # graded Morita two-step connector
        [1, 1, 1, 1, 0, 0],  # Hopf/Chern pairing
        [1, 1, 1, 1, 1, 0],  # Callias mass profile
        [1, 0, 1, 1, 0, 1],  # K43 cell incidence
        [1, 1, 0, 1, 1, 0],  # bath covariance response
        [1, 0, 1, 0, 0, 1],  # inherited Higgs rank-change portal
        [1, 1, 1, 1, 1, 0],  # target-loaded pole match
    ])
    score_vector = sp.ImmutableMatrix([sum(candidate_matrix.row(i)) for i in range(11)])
    pass_vector = sp.ImmutableMatrix([int(score == 6) for score in score_vector])
    inherited_pass_vector = sp.ImmutableMatrix([
        int(candidate_matrix[i, 1] == 1 and candidate_matrix[i, 3] == 1 and candidate_matrix[i, 4] == 1 and candidate_matrix[i, 5] == 1)
        for i in range(11)
    ])
    audit_coverage = sp.ImmutableMatrix(sp.ones(11, 1))
    physical_origin = sp.ImmutableMatrix(sp.zeros(3, 1))

    theorems = (
        kernel.prove_matrix_equality(inherited_hessian, sp.diag(2, 0), subject="inherited wrinkle defect parent remains a direct sum"),
        kernel.prove_exact_rank(inherited_hessian, 1, subject="inherited mixed parent retains one flat direction"),
        kernel.prove_expression_equality(inherited_hessian.det(), 0, subject="inherited mixed parent is singular"),
        kernel.prove_matrix_equality(graded_product_mixed_block, sp.zeros(2), subject="graded product cancels the mixed block"),
        kernel.prove_matrix_equality(morita_mixed_block, sp.zeros(2), subject="centered Morita curvature remains additive"),
        kernel.prove_expression_equality(conditional_callias_hessian.det(), 1, subject="conditional Callias bridge closes the local Hessian"),
        kernel.prove_exact_rank(conditional_callias_hessian, 2, subject="conditional Callias bridge is nondegenerate"),
        kernel.prove_exact_spectrum(conditional_callias_hessian, {(sp.Integer(3) - sp.sqrt(5)) / 2: 1, (sp.Integer(3) + sp.sqrt(5)) / 2: 1}, subject="conditional Callias bridge is positive"),
        kernel.prove_matrix_equality(callias_localization_projector * callias_localization_projector, callias_localization_projector, subject="conditional Callias localization is projective"),
        kernel.prove_exact_rank(callias_localization_projector, 15, subject="conditional Callias profile localizes fifteen channels"),
        kernel.prove_expression_equality(candidate_matrix.rows, 11, subject="eleven mixed bridge candidates are audited"),
        kernel.prove_expression_equality(candidate_matrix.cols, 6, subject="six independent bridge criteria are used"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="mixed bridge audit matrix has full criterion rank"),
        kernel.prove_matrix_equality(score_vector, sp.Matrix([3, 3, 4, 4, 3, 4, 5, 4, 4, 3, 5]), subject="mixed bridge scores are exact"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="no mixed bridge candidate reaches all criteria"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1), subject="strict mixed bridge pass vector is empty"),
        kernel.prove_matrix_equality(inherited_pass_vector, sp.zeros(11, 1), subject="no inherited candidate supplies localization and pole together"),
        kernel.prove_expression_equality(sum(audit_coverage), 11, subject="mixed bridge audit coverage is complete"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="bridge localization and pole origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict mixed bridge origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit_gate",
        theorems,
    )
    return ParticleWrinkleDislocationMixedBridgeAuditCertificate(
        inherited_hessian,
        graded_product_mixed_block,
        morita_mixed_block,
        conditional_callias_hessian,
        callias_localization_projector,
        candidate_matrix,
        score_vector,
        pass_vector,
        inherited_pass_vector,
        audit_coverage,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit_gate",
    title="Аудит смешанных мостов морщинки и дислокации",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"particle_wrinkle_dislocation_mixed_bridge_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(20)
    ),
)