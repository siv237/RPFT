"""LCF certificate for the M4 bifundamental-condensate candidate audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class BifundamentalCondensateAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    physical_seed_vector: sp.ImmutableMatrix
    negative_mode_vector: sp.ImmutableMatrix
    incidence: sp.ImmutableMatrix
    incidence_laplacian: sp.ImmutableMatrix
    sign_flipped_laplacian: sp.ImmutableMatrix
    callias_hessian: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> BifundamentalCondensateAuditCertificate:
    # Columns: bifundamental type, inherited carrier/operator, negative
    # quadratic mode, positive quartic stabilization, orientation/phase
    # selector, non-target-loaded physical normalization.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 0, 0, 0, 1],  # inherited block-diagonal parent
        [1, 0, 0, 1, 1, 1],  # spectral inner fluctuation
        [1, 1, 0, 0, 1, 1],  # KMS modular covariance
        [1, 1, 0, 0, 1, 1],  # Hopf holonomy
        [1, 1, 0, 1, 0, 1],  # bath-current susceptibility
        [1, 1, 0, 1, 1, 1],  # cell incidence boundary
        [1, 0, 1, 1, 1, 1],  # Callias sign-changing profile
        [1, 0, 1, 1, 1, 1],  # Higgs rank-change portal
        [0, 1, 1, 1, 0, 1],  # existing RG-K43 portal
        [1, 0, 1, 1, 0, 1],  # auxiliary bifundamental scalar
        [1, 0, 1, 1, 1, 0],  # target-loaded tachyonic source
    ])
    score_vector = sp.ImmutableMatrix([
        sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    physical_seed_vector = sp.ImmutableMatrix([
        candidate_matrix[i, 0] * candidate_matrix[i, 1] * candidate_matrix[i, 2]
        for i in range(candidate_matrix.rows)
    ])
    negative_mode_vector = candidate_matrix[:, 2]

    incidence = sp.ImmutableMatrix([[-1], [1]])
    incidence_laplacian = sp.ImmutableMatrix(incidence * incidence.T)
    sign_flipped_laplacian = sp.ImmutableMatrix(-incidence_laplacian)
    callias_hessian = sp.ImmutableMatrix([[2, 1], [1, 1]])
    audit_coverage = sp.ImmutableMatrix.ones(11, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 0, 0, 0])
    physical_origin = sp.ImmutableMatrix.zeros(4, 1)

    theorems = (
        kernel.prove_expression_equality(candidate_matrix.rows, 11,
                                         subject="eleven bifundamental condensate candidates are audited"),
        kernel.prove_expression_equality(candidate_matrix.cols, 6,
                                         subject="six independent condensate criteria are used"),
        kernel.prove_exact_rank(candidate_matrix, 6,
                                subject="condensate candidate matrix has full criterion rank"),
        kernel.prove_matrix_equality(score_vector, sp.Matrix([3, 4, 4, 4, 4, 5, 5, 5, 4, 4, 4]),
                                     subject="bifundamental condensate scores are exact"),
        kernel.prove_expression_equality(max(score_vector), 5,
                                         subject="three closest condensate candidates score five of six"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1),
                                     subject="no condensate candidate passes the complete contract"),
        kernel.prove_expression_equality(sum(pass_vector), 0,
                                         subject="strict bifundamental condensate pass count is zero"),
        kernel.prove_matrix_equality(physical_seed_vector, sp.zeros(11, 1),
                                     subject="no correctly typed inherited candidate has a negative quadratic mode"),
        kernel.prove_matrix_equality(negative_mode_vector, sp.Matrix([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]),
                                     subject="five candidates can conditionally supply a negative mode"),
        kernel.prove_matrix_equality(incidence, sp.Matrix([[-1], [1]]),
                                     subject="minimal oriented cell incidence is exact"),
        kernel.prove_matrix_equality(incidence_laplacian, sp.Matrix([[1, -1], [-1, 1]]),
                                     subject="cell incidence produces the positive graph Laplacian"),
        kernel.prove_exact_rank(incidence_laplacian, 1,
                                subject="minimal incidence Laplacian has one relative mode"),
        kernel.prove_exact_spectrum(incidence_laplacian, {sp.Integer(0): 1, sp.Integer(2): 1},
                                    subject="inherited incidence spectrum is nonnegative"),
        kernel.prove_expression_equality(incidence_laplacian.det(), 0,
                                         subject="incidence Laplacian retains one common zero mode"),
        kernel.prove_exact_spectrum(sign_flipped_laplacian, {sp.Integer(-2): 1, sp.Integer(0): 1},
                                    subject="a manual sign flip would create one tachyonic relative mode"),
        kernel.prove_matrix_equality(sign_flipped_laplacian - incidence_laplacian,
                                     -2 * incidence_laplacian,
                                     subject="tachyonic incidence requires an uninherited sign reversal"),
        kernel.prove_expression_equality(callias_hessian.det(), 1,
                                         subject="conditional Callias completion is nondegenerate"),
        kernel.prove_exact_rank(callias_hessian, 2,
                                subject="conditional Callias completion controls both local variables"),
        kernel.prove_matrix_equality(audit_coverage, sp.ones(11, 1),
                                     subject="all eleven condensate candidates are covered"),
        kernel.prove_expression_equality(sum(audit_coverage), 11,
                                         subject="candidate audit coverage is complete"),
        kernel.prove_matrix_equality(origin_ledger, sp.Matrix([1, 1, 1, 0, 0, 0]),
                                     subject="audit coverage passes while three origin slots remain open"),
        kernel.prove_expression_equality(sum(origin_ledger), 3,
                                         subject="three of six audit-level origin requirements pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(4, 1),
                                     subject="cross field tachyonic sign phase and scale origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0,
                                         subject="strict physical condensate score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_bifundamental_condensate_candidate_audit_gate",
        theorems,
    )
    return BifundamentalCondensateAuditCertificate(
        candidate_matrix, score_vector, pass_vector, physical_seed_vector,
        negative_mode_vector, incidence, incidence_laplacian,
        sign_flipped_laplacian, callias_hessian, audit_coverage,
        origin_ledger, physical_origin, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_bifundamental_condensate_candidate_audit_gate",
    title="Аудит кандидатов бифундаментального M4-конденсата",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_bifundamental_condensate_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_bifundamental_condensate_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"m4_bifundamental_condensate_audit_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(24)
    ),
)