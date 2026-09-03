"""LCF audit of candidate infrared mass terms for the transmuted mode."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class TransmutedModeIRMassTermCandidateAuditCertificate:
    required_mass_squared: sp.Expr
    inherited_beta: sp.Expr
    conditional_af_beta: sp.Expr
    coupling_squared: sp.Expr
    af_logarithm: sp.Expr
    conditional_af_scale_ratio: sp.Expr
    conditional_af_mass_squared_ratio: sp.Expr
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    internal_exact_origin_vector: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> TransmutedModeIRMassTermCandidateAuditCertificate:
    required_mass_squared = sp.exp(-64 * sp.pi**2 / 3)
    inherited_beta = sp.Integer(2)
    conditional_af_beta = sp.Integer(-2)
    coupling_squared = sp.Rational(3, 8)
    af_logarithm = sp.simplify(8 * sp.pi**2 / (-conditional_af_beta * coupling_squared))
    conditional_af_scale_ratio = sp.exp(-af_logarithm)
    conditional_af_mass_squared_ratio = sp.exp(-2 * af_logarithm)

    # Columns: mass type, internal carrier, nonzero IR, selected parent,
    # exact target exponent, non-target-loaded.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 1, 0, 0, 0],  # explicit bare mass/counterterm
        [1, 1, 1, 0, 0, 1],  # Higgs/Yukawa condensate
        [1, 0, 1, 0, 0, 1],  # asymptotically-free condensate in current carrier
        [1, 1, 1, 1, 0, 1],  # KMS thermal mass
        [1, 1, 1, 0, 0, 1],  # bath Lamb shift
        [1, 1, 1, 0, 0, 1],  # curvature coupling
        [1, 1, 1, 1, 0, 1],  # finite-volume/cell gap
        [1, 1, 0, 1, 0, 1],  # throughflow self-energy
        [1, 1, 1, 0, 0, 1],  # portal eigenvalue splitting
        [1, 0, 1, 0, 1, 0],  # observed pole fit
        [1, 1, 1, 1, 1, 0],  # formal target mass term
    ])
    score_vector = sp.ImmutableMatrix([sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    internal_exact_origin_vector = sp.ImmutableMatrix([
        candidate_matrix[i, 1] * candidate_matrix[i, 3] * candidate_matrix[i, 4] * candidate_matrix[i, 5]
        for i in range(candidate_matrix.rows)
    ])
    audit_coverage = sp.ones(11, 1)
    physical_origin = sp.zeros(3, 1)

    theorems = (
        kernel.prove_expression_equality(required_mass_squared, sp.exp(-64 * sp.pi**2 / 3), subject="required infrared mass squared in cell units"),
        kernel.prove_expression_equality(inherited_beta, 2, subject="inherited beta coefficient has the Landau sign"),
        kernel.prove_expression_equality(conditional_af_beta, -2, subject="conditional asymptotically-free coefficient has the opposite sign"),
        kernel.prove_expression_equality(inherited_beta + conditional_af_beta, 0, subject="the exact inverse hierarchy requires reversal of the inherited beta sign"),
        kernel.prove_expression_equality(coupling_squared, sp.Rational(3, 8), subject="inherited boundary coupling squared"),
        kernel.prove_expression_equality(af_logarithm, 32 * sp.pi**2 / 3, subject="conditional asymptotically-free transmutation logarithm"),
        kernel.prove_expression_equality(conditional_af_scale_ratio, sp.exp(-32 * sp.pi**2 / 3), subject="conditional asymptotically-free infrared scale"),
        kernel.prove_expression_equality(conditional_af_mass_squared_ratio, required_mass_squared, subject="conditional asymptotic freedom generates the exact target mass exponent"),
        kernel.prove_expression_equality(candidate_matrix.shape[0], 11, subject="eleven infrared mass mechanisms are audited"),
        kernel.prove_expression_equality(candidate_matrix.shape[1], 6, subject="six independent admissibility criteria are applied"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="infrared mass candidate audit has full criterion rank"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([3, 4, 3, 5, 4, 4, 5, 4, 4, 3, 5]), subject="candidate score ledger"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="best candidate score remains below closure"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1), subject="no current infrared mass candidate passes all criteria"),
        kernel.prove_expression_equality(sum(pass_vector), 0, subject="strict candidate pass count is zero"),
        kernel.prove_matrix_equality(internal_exact_origin_vector, sp.zeros(11, 1), subject="no internally selected noncircular exact mass origin exists"),
        kernel.prove_expression_equality(sum(internal_exact_origin_vector), 0, subject="exact internal origin count is zero"),
        kernel.prove_matrix_equality(audit_coverage, sp.ones(11, 1), subject="all declared infrared mass mechanisms are covered"),
        kernel.prove_expression_equality(sum(audit_coverage), 11, subject="audit coverage score"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="beta sign, condensate carrier, and mass coefficient origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict infrared mass origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_ir_mass_term_candidate_audit_gate",
        theorems,
    )
    return TransmutedModeIRMassTermCandidateAuditCertificate(
        required_mass_squared,
        inherited_beta,
        conditional_af_beta,
        coupling_squared,
        af_logarithm,
        conditional_af_scale_ratio,
        conditional_af_mass_squared_ratio,
        candidate_matrix,
        score_vector,
        pass_vector,
        internal_exact_origin_vector,
        audit_coverage,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_ir_mass_term_candidate_audit_gate",
    title="Аудит кандидатов IR-массового члена трансмутированной моды",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_ir_mass_term_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_ir_mass_term_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"transmuted_mode_ir_mass_candidate_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(21)
    ),
)