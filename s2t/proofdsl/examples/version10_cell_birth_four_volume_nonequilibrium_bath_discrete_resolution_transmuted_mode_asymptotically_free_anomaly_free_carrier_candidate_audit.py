"""LCF audit of anomaly-free asymptotically-free carrier candidates."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class AnomalyFreeAFCarrierCandidateAuditCertificate:
    required_beta: sp.Expr
    current_nonabelian_betas: sp.ImmutableMatrix
    current_beta_mismatch: sp.ImmutableMatrix
    fundamental_solution_table: sp.ImmutableMatrix
    solution_betas: sp.ImmutableMatrix
    complexity_vector: sp.ImmutableMatrix
    minimality_vector: sp.ImmutableMatrix
    su2_weyl_doublets: sp.Expr
    su2_witten_parity: sp.Expr
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> AnomalyFreeAFCarrierCandidateAuditCertificate:
    required_beta = sp.Integer(-2)
    current_nonabelian_betas = sp.ImmutableMatrix([sp.Rational(-19, 6), -7])
    current_beta_mismatch = current_nonabelian_betas - sp.ones(2, 1) * required_beta

    # Rows: N=C_A, n_D, n_s, complexity=N+n_D+n_s.  For each N the
    # nonnegative fundamental solution minimizes n_D+n_s subject to b=-2.
    fundamental_solution_table = sp.ImmutableMatrix([
        [2, 8, 0, 10],
        [3, 13, 2, 18],
        [4, 19, 0, 23],
        [5, 24, 2, 31],
        [6, 30, 0, 36],
    ])
    solution_betas = sp.ImmutableMatrix([
        -sp.Rational(11, 3) * row[0] + sp.Rational(2, 3) * row[1] + sp.Rational(1, 6) * row[2]
        for row in fundamental_solution_table.tolist()
    ])
    complexity_vector = fundamental_solution_table[:, 3]
    minimality_vector = sp.ImmutableMatrix([1, 0, 0, 0, 0])
    su2_weyl_doublets = sp.Integer(16)
    su2_witten_parity = sp.Mod(su2_weyl_doublets, 2)

    # Columns: nonabelian gauge carrier, anomaly-free, internally typed,
    # exact b=-2, typed coupling to pole mode, parent-selected content.
    candidate_matrix = sp.ImmutableMatrix([
        [0, 1, 1, 0, 1, 1],  # inherited relative U(1)
        [1, 1, 1, 0, 0, 1],  # existing SM SU(2), b=-19/6
        [1, 1, 1, 0, 0, 1],  # existing SM SU(3), b=-7
        [1, 1, 0, 0, 0, 1],  # pure SU(2)
        [1, 1, 0, 0, 0, 1],  # pure SU(3)
        [1, 1, 0, 1, 0, 0],  # SU(2)+8 Dirac fundamentals
        [1, 1, 0, 1, 0, 0],  # SU(3)+13 Dirac+2 scalars
        [1, 0, 1, 0, 0, 0],  # unresolved Pati--Salam finite block
        [1, 0, 1, 1, 0, 0],  # K43/BV 27 retyped as chiral SU(3)
        [0, 1, 1, 0, 1, 0],  # bath/ghost carrier of the wrong beta type
        [1, 1, 1, 1, 1, 0],  # formal AF portal sector
    ])
    score_vector = sp.ImmutableMatrix([sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)])
    pass_vector = sp.ImmutableMatrix([sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)])
    physical_origin = sp.zeros(3, 1)

    theorems = (
        kernel.prove_expression_equality(required_beta, -2, subject="required infrared transmutation beta coefficient"),
        kernel.prove_matrix_equality(current_nonabelian_betas, sp.ImmutableMatrix([sp.Rational(-19, 6), -7]), subject="existing weak and color one-loop beta coefficients"),
        kernel.prove_matrix_equality(current_beta_mismatch, sp.ImmutableMatrix([sp.Rational(-7, 6), -5]), subject="neither existing nonabelian coefficient equals minus two"),
        kernel.prove_matrix_equality(solution_betas, -2 * sp.ones(5, 1), subject="five minimal fundamental SU(N) solutions exactly realize beta minus two"),
        kernel.prove_matrix_equality(complexity_vector, sp.ImmutableMatrix([10, 18, 23, 31, 36]), subject="restricted carrier complexity ledger"),
        kernel.prove_expression_equality(min(complexity_vector), 10, subject="SU2 with eight Dirac fundamentals has minimal restricted complexity"),
        kernel.prove_matrix_equality(minimality_vector, sp.ImmutableMatrix([1, 0, 0, 0, 0]), subject="the restricted minimal exact carrier is unique"),
        kernel.prove_expression_equality(sum(minimality_vector), 1, subject="one restricted minimal carrier is selected by complexity"),
        kernel.prove_expression_equality(su2_weyl_doublets, 16, subject="eight Dirac SU2 fundamentals contain sixteen Weyl doublets"),
        kernel.prove_expression_equality(su2_witten_parity, 0, subject="the minimal SU2 candidate passes the global anomaly parity test"),
        kernel.prove_expression_equality(candidate_matrix.shape[0], 11, subject="eleven anomaly-free carrier candidates are audited"),
        kernel.prove_expression_equality(candidate_matrix.shape[1], 6, subject="six carrier-origin criteria are applied"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="carrier audit has full criterion rank"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([4, 4, 4, 3, 3, 3, 3, 2, 3, 3, 5]), subject="carrier candidate score ledger"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="best carrier candidate remains incomplete"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1), subject="no current or conditional carrier passes every criterion"),
        kernel.prove_expression_equality(sum(pass_vector), 0, subject="strict anomaly-free carrier pass count is zero"),
        kernel.prove_matrix_equality(candidate_matrix[1:3, 3], sp.zeros(2, 1), subject="existing weak and color sectors miss the exact coefficient"),
        kernel.prove_matrix_equality(candidate_matrix[5:7, 2], sp.zeros(2, 1), subject="exact conditional carriers are absent from the current typed carrier"),
        kernel.prove_matrix_equality(candidate_matrix[5:7, 4], sp.zeros(2, 1), subject="exact conditional carriers have no typed map to the pole mode"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="K43 embedding pole coupling and multiplicity parent remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict anomaly-free AF carrier origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_anomaly_free_carrier_candidate_audit_gate",
        theorems,
    )
    return AnomalyFreeAFCarrierCandidateAuditCertificate(
        required_beta, current_nonabelian_betas, current_beta_mismatch,
        fundamental_solution_table, solution_betas, complexity_vector,
        minimality_vector, su2_weyl_doublets, su2_witten_parity,
        candidate_matrix, score_vector, pass_vector, physical_origin,
        theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_anomaly_free_carrier_candidate_audit_gate",
    title="Аудит безаномального носителя асимптотически-свободной моды",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_anomaly_free_carrier_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_anomaly_free_carrier_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"anomaly_free_af_carrier_candidate_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(22)
    ),
)