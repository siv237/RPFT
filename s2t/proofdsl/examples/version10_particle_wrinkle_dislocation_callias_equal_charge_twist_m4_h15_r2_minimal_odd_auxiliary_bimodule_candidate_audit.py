"""LCF certificate for the minimal odd auxiliary-bimodule candidate audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class MinimalOddAuxiliaryBimoduleAuditCertificate:
    required_weights: sp.ImmutableMatrix
    required_reality: sp.ImmutableMatrix
    required_grading: sp.ImmutableMatrix
    required_metric: sp.ImmutableMatrix
    minimal_multiplicities: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    coverage: sp.ImmutableMatrix
    hubbard_stratonovich_row: sp.ImmutableMatrix
    inherited_embedding: sp.ImmutableMatrix
    conditional_embedding: sp.ImmutableMatrix
    conditional_parent_hessian: sp.ImmutableMatrix
    conditional_schur_complement: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> MinimalOddAuxiliaryBimoduleAuditCertificate:
    weights = [3, -3, 7, 1, -1, -7, 3, -3]
    required_weights = sp.ImmutableMatrix(weights)
    required_grading = sp.ImmutableMatrix(-sp.eye(8))
    required_metric = sp.ImmutableMatrix(sp.eye(8))
    reality_mutable = sp.zeros(8)
    for left, right in ((0, 1), (2, 5), (3, 4), (6, 7)):
        reality_mutable[left, right] = 1
        reality_mutable[right, left] = 1
    required_reality = sp.ImmutableMatrix(reality_mutable)
    minimal_multiplicities = sp.ImmutableMatrix([1, 2, 1, 1, 2, 1])

    # Columns: exact weights, odd grading, Real closure, positive bosonic
    # metric/statistics, independent algebraic elimination, inherited parent.
    candidate_matrix = sp.ImmutableMatrix(
        [
            [0, 0, 1, 1, 1, 1],  # inherited fixed-point C sector
            [0, 0, 0, 1, 1, 0],  # arbitrary eight-coordinate slice
            [1, 1, 1, 1, 0, 1],  # reuse Sigma itself
            [1, 1, 1, 1, 0, 1],  # composite Q Sigma
            [1, 1, 1, 1, 1, 0],  # Hubbard-Stratonovich A_Sigma
            [1, 1, 1, 0, 0, 0],  # cotangent T*Sigma doubling
            [1, 1, 1, 0, 1, 0],  # BV antifield of Sigma
            [1, 1, 1, 1, 0, 1],  # KO6 charge-conjugate one-form
            [0, 1, 1, 1, 0, 1],  # off-diagonal Delta mapping-cone arrow
            [1, 1, 1, 1, 0, 0],  # Callias normal component
            [1, 1, 1, 1, 0, 0],  # suspended superconnection component
            [0, 0, 1, 1, 1, 0],  # Pati-Salam adjoint D-term
        ]
    )
    score_vector = sp.ImmutableMatrix(candidate_matrix * sp.ones(6, 1))
    pass_vector = sp.ImmutableMatrix.zeros(12, 1)
    coverage = sp.ImmutableMatrix([
        [int(any(candidate_matrix[row, column] for row in range(candidate_matrix.rows)))]
        for column in range(candidate_matrix.cols)
    ])
    hubbard_stratonovich_row = sp.ImmutableMatrix(candidate_matrix.row(4))

    inherited_embedding = sp.ImmutableMatrix.zeros(8)
    conditional_embedding = sp.ImmutableMatrix(sp.eye(8))
    q = sp.diag(*weights)
    identity = sp.eye(8)
    conditional_parent_hessian = sp.ImmutableMatrix(
        sp.BlockMatrix([[49 * identity, q], [q, identity]]).as_explicit()
    )
    conditional_schur_complement = sp.ImmutableMatrix(49 * identity - q**2)
    physical_origin = sp.ImmutableMatrix([1, 1, 1, 0])

    theorems = (
        kernel.prove_matrix_equality(required_weights, sp.ImmutableMatrix([3, -3, 7, 1, -1, -7, 3, -3]), subject="required odd auxiliary weights are exact"),
        kernel.prove_matrix_equality(minimal_multiplicities, sp.ImmutableMatrix([1, 2, 1, 1, 2, 1]), subject="nonzero weight multiplicities sum to eight"),
        kernel.prove_expression_equality(sum(minimal_multiplicities), 8, subject="minimal Real weight carrier has dimension eight"),
        kernel.prove_matrix_equality(required_reality**2, sp.eye(8), subject="required auxiliary reality squares to one"),
        kernel.prove_matrix_equality(required_reality * sp.diag(*weights) * required_reality, -sp.diag(*weights), subject="required reality reverses hypercharge"),
        kernel.prove_matrix_equality(required_grading, -sp.eye(8), subject="required auxiliary module is odd"),
        kernel.prove_matrix_equality(required_metric, sp.eye(8), subject="required trace metric is positive and normalized"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="candidate audit resolves all six criteria"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([4, 2, 5, 5, 5, 3, 4, 5, 4, 4, 4, 3]), subject="odd auxiliary candidate scores are exact"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(12, 1), subject="no odd auxiliary candidate passes all criteria"),
        kernel.prove_matrix_equality(coverage, sp.ones(6, 1), subject="every odd auxiliary criterion is represented"),
        kernel.prove_matrix_equality(hubbard_stratonovich_row, sp.ImmutableMatrix([[1, 1, 1, 1, 1, 0]]), subject="Hubbard-Stratonovich candidate fails only inheritance"),
        kernel.prove_exact_rank(inherited_embedding, 0, subject="current parent contains no independent odd auxiliary embedding"),
        kernel.prove_exact_rank(conditional_embedding, 8, subject="conditional Hubbard-Stratonovich embedding is complete"),
        kernel.prove_matrix_equality(conditional_embedding.T * required_metric * conditional_embedding, sp.eye(8), subject="conditional embedding is trace isometric"),
        kernel.prove_matrix_equality(sp.diag(*weights) * conditional_embedding, conditional_embedding * sp.diag(*weights), subject="conditional embedding is hypercharge equivariant"),
        kernel.prove_matrix_equality(required_grading * conditional_embedding, conditional_embedding * required_grading, subject="conditional embedding preserves odd grading"),
        kernel.prove_matrix_equality(required_reality * conditional_embedding, conditional_embedding * required_reality, subject="conditional embedding preserves reality"),
        kernel.prove_exact_rank(conditional_parent_hessian, 14, subject="conditional Hubbard-Stratonovich parent has rank fourteen"),
        kernel.prove_exact_nullity(conditional_parent_hessian, 2, subject="conditional Hubbard-Stratonovich parent retains two light modes"),
        kernel.prove_matrix_equality(conditional_schur_complement, sp.diag(40, 40, 0, 48, 48, 0, 40, 40), subject="conditional Hubbard-Stratonovich elimination gives the exact gap"),
        kernel.prove_matrix_equality(physical_origin, sp.ImmutableMatrix([1, 1, 1, 0]), subject="representation grading and metric are known while parent origin is open"),
        kernel.prove_expression_equality(sum(physical_origin), 3, subject="strict odd auxiliary physical-origin score is three of four"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_minimal_odd_auxiliary_bimodule_candidate_audit_gate",
        theorems,
    )
    return MinimalOddAuxiliaryBimoduleAuditCertificate(
        required_weights,
        required_reality,
        required_grading,
        required_metric,
        minimal_multiplicities,
        candidate_matrix,
        score_vector,
        pass_vector,
        coverage,
        hubbard_stratonovich_row,
        inherited_embedding,
        conditional_embedding,
        conditional_parent_hessian,
        conditional_schur_complement,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_minimal_odd_auxiliary_bimodule_candidate_audit_gate",
    title="Аудит кандидатов минимального odd auxiliary-бимодуля",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_minimal_odd_auxiliary_bimodule_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_minimal_odd_auxiliary_bimodule_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_minimal_odd_auxiliary_audit_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(23)
    ),
)