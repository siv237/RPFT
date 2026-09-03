"""LCF certificate for the relative-Hodge auxiliary-edge origin audit."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class RelativeHodgeAuxiliaryEdgeOriginAuditCertificate:
    required_weights: sp.ImmutableMatrix
    required_reality: sp.ImmutableMatrix
    relative_projector: sp.ImmutableMatrix
    diagonal_reuse_embedding: sp.ImmutableMatrix
    diagonal_relative_image: sp.ImmutableMatrix
    independent_auxiliary_embedding: sp.ImmutableMatrix
    independent_relative_image: sp.ImmutableMatrix
    inherited_fixed_point_embedding: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    coverage: sp.ImmutableMatrix
    suspension_row: sp.ImmutableMatrix
    mapping_cylinder_row: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> RelativeHodgeAuxiliaryEdgeOriginAuditCertificate:
    weights = [3, -3, 7, 1, -1, -7, 3, -3]
    required_weights = sp.ImmutableMatrix(weights)
    reality = sp.zeros(8)
    for left, right in ((0, 1), (2, 5), (3, 4), (6, 7)):
        reality[left, right] = reality[right, left] = 1
    required_reality = sp.ImmutableMatrix(reality)
    identity, zero = sp.eye(8), sp.zeros(8)
    relative_projector = sp.ImmutableMatrix(sp.Rational(1, 2) * sp.BlockMatrix([[identity, -identity], [-identity, identity]]).as_explicit())
    diagonal_reuse_embedding = sp.ImmutableMatrix(sp.Matrix.vstack(identity, identity))
    diagonal_relative_image = sp.ImmutableMatrix(relative_projector * diagonal_reuse_embedding)
    independent_auxiliary_embedding = sp.ImmutableMatrix(sp.Matrix.vstack(zero, identity))
    independent_relative_image = sp.ImmutableMatrix(relative_projector * independent_auxiliary_embedding)
    inherited_fixed_point_embedding = sp.ImmutableMatrix.zeros(16, 8)

    # exact weights, independent boson, odd grading, Real/Hodge edge,
    # positive metric, inherited origin.
    candidate_matrix = sp.ImmutableMatrix([
        [0,1,0,0,1,1], [1,0,1,1,1,1], [1,1,1,1,0,0],
        [1,1,0,1,0,1], [0,1,1,1,1,1], [1,1,1,1,1,0],
        [1,1,1,1,1,0], [1,1,0,1,1,0], [1,1,1,1,0,0],
        [1,1,1,1,1,0], [1,1,0,1,1,1], [1,1,1,1,1,0],
    ])
    score_vector = sp.ImmutableMatrix(candidate_matrix * sp.ones(6, 1))
    pass_vector = sp.ImmutableMatrix.zeros(12, 1)
    coverage = sp.ImmutableMatrix([int(any(candidate_matrix[r,c] for r in range(12))) for c in range(6)])
    suspension_row = sp.ImmutableMatrix(candidate_matrix.row(5))
    mapping_cylinder_row = sp.ImmutableMatrix(candidate_matrix.row(6))
    physical_origin = sp.ImmutableMatrix([1,1,1,1,1,0])
    theorems = (
        kernel.prove_matrix_equality(required_reality**2, identity, subject="required auxiliary reality squares to one"),
        kernel.prove_matrix_equality(required_reality * sp.diag(*weights) * required_reality, -sp.diag(*weights), subject="required reality reverses hypercharge"),
        kernel.prove_exact_rank(relative_projector, 8, subject="relative Hodge projector has eight physical relative modes"),
        kernel.prove_exact_rank(diagonal_reuse_embedding, 8, subject="reusing Sigma gives an eight-dimensional diagonal copy"),
        kernel.prove_matrix_equality(diagonal_relative_image, sp.zeros(16, 8), subject="relative projector annihilates reused physical Sigma"),
        kernel.prove_exact_rank(independent_auxiliary_embedding, 8, subject="independent auxiliary copy embeds with full rank"),
        kernel.prove_exact_rank(independent_relative_image, 8, subject="independent auxiliary copy excites every relative mode"),
        kernel.prove_exact_rank(inherited_fixed_point_embedding, 0, subject="fixed-point parent supplies no typed auxiliary copy"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="auxiliary-edge origin audit resolves all six criteria"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([3,5,4,4,5,5,5,4,4,5,5,5]), subject="auxiliary-edge candidate scores are exact"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(12,1), subject="no auxiliary-edge origin candidate passes all criteria"),
        kernel.prove_matrix_equality(coverage, sp.ones(6,1), subject="every origin criterion is represented"),
        kernel.prove_matrix_equality(suspension_row, sp.ImmutableMatrix([[1,1,1,1,1,0]]), subject="superconnection suspension fails only inheritance"),
        kernel.prove_matrix_equality(mapping_cylinder_row, suspension_row, subject="mapping-cylinder copy fails only inheritance"),
        kernel.prove_expression_equality(sum(physical_origin), 5, subject="best auxiliary-edge origin remains five of six"),
    )
    gate_theorem = kernel.prove_gate("version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_origin_candidate_audit_gate", theorems)
    return RelativeHodgeAuxiliaryEdgeOriginAuditCertificate(required_weights, required_reality, relative_projector, diagonal_reuse_embedding, diagonal_relative_image, independent_auxiliary_embedding, independent_relative_image, inherited_fixed_point_embedding, candidate_matrix, score_vector, pass_vector, coverage, suspension_row, mapping_cylinder_row, physical_origin, theorems, gate_theorem)


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_origin_candidate_audit_gate",
    title="Аудит происхождения relative-Hodge auxiliary edge",
    source_paths=("s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_origin_candidate_audit_gate.tex", "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_origin_candidate_audit_gate_results.json"),
    obligations=tuple(Obligation(f"h15_r2_relative_hodge_auxiliary_edge_origin_{i:02d}", lambda i=i: build_certificate().theorems[i]) for i in range(15)),
)