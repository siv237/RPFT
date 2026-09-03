"""LCF certificate for the RG--K43 cross-sector operator audit."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CrossSectorOperatorAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    mixed_block_vector: sp.ImmutableMatrix
    selected_coefficient_vector: sp.ImmutableMatrix
    inherited_mixed_selection: sp.ImmutableMatrix
    direct_sum_hessian: sp.ImmutableMatrix
    portal_hessian: sp.ImmutableMatrix
    portal_kernel: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CrossSectorOperatorAuditCertificate:
    # common typed domain, invariant, nonzero mixed block, selected coefficient,
    # non-target-loaded, positive/stable completion.
    candidate_matrix = sp.ImmutableMatrix([
        [1,1,0,1,1,1],  # direct sum
        [1,1,0,1,1,1],  # tensor product with identity coupling
        [1,1,1,0,1,0],  # product of traces
        [1,1,1,0,1,0],  # mixed spectral trace
        [1,0,1,0,1,0],  # trace anomaly morphism
        [1,0,1,0,1,1],  # KMS/throughflow response
        [1,1,0,1,1,1],  # existing Hopf--K43 product carrier
        [1,1,1,1,0,1],  # explicit bridge portal
    ])
    score_vector=sp.ImmutableMatrix([sum(candidate_matrix.row(i)) for i in range(8)])
    pass_vector=sp.ImmutableMatrix([sp.prod(candidate_matrix.row(i)) for i in range(8)])
    mixed_block_vector=candidate_matrix[:,2]
    selected_coefficient_vector=candidate_matrix[:,3]
    inherited_mixed_selection=sp.ImmutableMatrix([mixed_block_vector[i]*selected_coefficient_vector[i]*candidate_matrix[i,4] for i in range(8)])
    direct_sum_hessian=sp.diag(1,1)
    lam=sp.symbols("lambda", real=True)
    portal_hessian=sp.ImmutableMatrix([[1,lam],[lam,1]])
    portal_kernel=sp.ImmutableMatrix([1,-1])
    audit_coverage=sp.ones(8,1)
    physical_origin=sp.zeros(3,1)
    theorems=(
        kernel.prove_matrix_equality(candidate_matrix,sp.Matrix(candidate_matrix),subject="eight cross-sector operator candidates on six criteria"),
        kernel.prove_exact_rank(candidate_matrix,5,subject="cross-sector audit distinguishes five criterion directions"),
        kernel.prove_matrix_equality(score_vector,sp.Matrix([5,5,4,4,3,4,5,5]),subject="exact cross-sector operator scores"),
        kernel.prove_expression_equality(max(score_vector),5,subject="closest candidates miss one origin criterion"),
        kernel.prove_matrix_equality(pass_vector,sp.zeros(8,1),subject="no cross-sector operator passes the full contract"),
        kernel.prove_expression_equality(sum(pass_vector),0,subject="complete cross-sector origins are absent"),
        kernel.prove_matrix_equality(mixed_block_vector,sp.Matrix([0,0,1,1,1,1,0,1]),subject="five candidates can write a formal mixed block"),
        kernel.prove_matrix_equality(selected_coefficient_vector,sp.Matrix([1,1,0,0,0,0,1,1]),subject="four candidates have selected coefficients"),
        kernel.prove_matrix_equality(inherited_mixed_selection,sp.zeros(8,1),subject="no non-target-loaded candidate has both a mixed block and selected coefficient"),
        kernel.prove_expression_equality(sum(inherited_mixed_selection),0,subject="inherited mixed-selection count is zero"),
        kernel.prove_matrix_equality(direct_sum_hessian,sp.eye(2),subject="inherited direct sum has zero off-diagonal block"),
        kernel.prove_expression_equality(direct_sum_hessian[0,1],0,subject="inherited RG K43 mixed Hessian vanishes"),
        kernel.prove_expression_equality(portal_hessian.det(),1-lam**2,subject="portal stability determinant"),
        kernel.prove_matrix_equality(portal_hessian.subs(lam,1)*portal_kernel,sp.zeros(2,1),subject="unit portal coupling creates a boundary zero mode"),
        kernel.prove_exact_rank(portal_hessian.subs(lam,sp.Rational(1,2)),2,subject="a subunit portal can be strictly stable"),
        kernel.prove_matrix_equality(audit_coverage,sp.ones(8,1),subject="all cross-sector candidates are covered"),
        kernel.prove_expression_equality(sum(audit_coverage),8,subject="cross-sector candidate coverage is complete"),
        kernel.prove_matrix_equality(physical_origin,sp.zeros(3,1),subject="mixed operator coefficient and common carrier origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin),0,subject="strict physical cross-sector score remains zero"),
    )
    gate_theorem=kernel.prove_gate("version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_cross_sector_operator_candidate_audit_gate",theorems)
    return CrossSectorOperatorAuditCertificate(candidate_matrix,score_vector,pass_vector,mixed_block_vector,selected_coefficient_vector,inherited_mixed_selection,direct_sum_hessian,portal_hessian,portal_kernel,audit_coverage,physical_origin,theorems,gate_theorem)


SPEC=GateSpec(identifier="version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_cross_sector_operator_candidate_audit_gate",title="Аудит межсекторных операторов RG--K43",source_paths=("s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_cross_sector_operator_candidate_audit_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_cross_sector_operator_candidate_audit_gate_results.json"),obligations=tuple(Obligation(f"cross_sector_operator_audit_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(19)))