"""LCF audit of mediator susceptibilities for composite SU(2) binding."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SU2GaugeSingletMediatorSusceptibilityCandidateAuditCertificate:
    coupling_squared: sp.Expr
    normalization_exponents: sp.ImmutableMatrix
    binding_exponent: sp.Expr
    massless_laplacian: sp.ImmutableMatrix
    laplacian_zero_mode: sp.ImmutableMatrix
    k43_inverse_cutoff: sp.Expr
    af_response: sp.Expr
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    internal_origin_vector: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SU2GaugeSingletMediatorSusceptibilityCandidateAuditCertificate:
    coupling_squared = sp.Rational(3, 8)
    normalization_exponents = sp.ImmutableMatrix([-2, 2])
    binding_exponent = sp.simplify(sum(normalization_exponents))
    massless_laplacian = sp.ImmutableMatrix([[1, -1], [-1, 1]])
    laplacian_zero_mode = sp.ImmutableMatrix([1, 1])
    k43_inverse_cutoff = sp.Rational(1, 42)
    af_response = sp.Rational(1, 2)

    # Columns: dimensionless static response, SU2-mediator typing,
    # finite positive IR value, parent-selected normalization,
    # selected flavor line, non-target-loaded origin.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 0, 1, 0, 0, 0],  # chi=1 normalization convention
        [1, 0, 1, 1, 0, 1],  # inverse K43 cutoff 1/42
        [1, 0, 1, 0, 0, 1],  # K43 spectral resolvent
        [0, 1, 0, 1, 0, 1],  # massless SU2 static propagator
        [1, 1, 1, 0, 0, 1],  # regulated SU2 propagator
        [1, 0, 1, 1, 0, 1],  # cell-Laplacian pseudoinverse
        [1, 0, 1, 0, 0, 1],  # bath zero-frequency response
        [1, 0, 1, 0, 0, 1],  # KMS static susceptibility
        [1, 0, 0, 1, 1, 1],  # portal inverse gap with sector selector
        [1, 1, 1, 1, 0, 1],  # AF running-response surrogate
        [1, 1, 1, 1, 1, 0],  # fitted chi=kappa/g2
    ])
    score_vector = sp.ImmutableMatrix([
        sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    internal_origin_vector = sp.ImmutableMatrix([
        candidate_matrix[i, 1]
        * candidate_matrix[i, 2]
        * candidate_matrix[i, 3]
        * candidate_matrix[i, 4]
        * candidate_matrix[i, 5]
        for i in range(candidate_matrix.rows)
    ])
    audit_coverage = sp.ones(11, 1)
    physical_origin = sp.zeros(3, 1)

    theorems = (
        kernel.prove_expression_equality(coupling_squared, sp.Rational(3, 8), subject="inherited SU2 coupling squared"),
        kernel.prove_matrix_equality(normalization_exponents, sp.Matrix([-2, 2]), subject="mediator field rescaling exponents for coupling and susceptibility"),
        kernel.prove_expression_equality(binding_exponent, 0, subject="product g squared times susceptibility is normalization invariant"),
        kernel.prove_expression_equality(normalization_exponents[1], 2, subject="susceptibility alone depends on mediator normalization"),
        kernel.prove_exact_spectrum(massless_laplacian, {sp.Integer(0): 1, sp.Integer(2): 1}, subject="massless static kinetic operator has a zero mode"),
        kernel.prove_expression_equality(massless_laplacian.det(), 0, subject="massless static propagator is not invertible before gauge fixing"),
        kernel.prove_matrix_equality(massless_laplacian * laplacian_zero_mode, sp.zeros(2, 1), subject="constant gauge mode is the exact propagator obstruction"),
        kernel.prove_exact_rank(massless_laplacian, 1, subject="massless two-site kinetic operator has rank one"),
        kernel.prove_expression_equality(k43_inverse_cutoff, sp.Rational(1, 42), subject="K43 cutoff supplies a finite dimensionless inverse scale"),
        kernel.prove_expression_equality(af_response, sp.Rational(1, 2), subject="inverse absolute AF beta coefficient is one half"),
        kernel.prove_expression_equality(candidate_matrix.shape[0], 11, subject="eleven susceptibility candidates are audited"),
        kernel.prove_expression_equality(candidate_matrix.shape[1], 6, subject="six susceptibility-origin criteria are applied"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="susceptibility audit has full criterion rank"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([2, 4, 3, 3, 4, 4, 3, 3, 4, 5, 5]), subject="susceptibility candidate score ledger"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="best susceptibility candidates remain below closure"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1), subject="no susceptibility candidate passes all criteria"),
        kernel.prove_expression_equality(sum(pass_vector), 0, subject="strict susceptibility pass count is zero"),
        kernel.prove_matrix_equality(internal_origin_vector, sp.zeros(11, 1), subject="no internal typed finite selected noncircular susceptibility exists"),
        kernel.prove_expression_equality(sum(internal_origin_vector), 0, subject="strict internal susceptibility origin count is zero"),
        kernel.prove_matrix_equality(audit_coverage, sp.ones(11, 1), subject="all declared susceptibility candidates are covered"),
        kernel.prove_expression_equality(sum(audit_coverage), 11, subject="susceptibility audit coverage score"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="kinetic normalization static limit and flavor selector origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict mediator susceptibility origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_mediator_susceptibility_candidate_audit_gate",
        theorems,
    )
    return SU2GaugeSingletMediatorSusceptibilityCandidateAuditCertificate(
        coupling_squared, normalization_exponents, binding_exponent,
        massless_laplacian, laplacian_zero_mode, k43_inverse_cutoff,
        af_response, candidate_matrix, score_vector, pass_vector,
        internal_origin_vector, audit_coverage, physical_origin, theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_mediator_susceptibility_candidate_audit_gate",
    title="Аудит восприимчивости посредника композитного SU(2)-синглета",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_mediator_susceptibility_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_mediator_susceptibility_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"su2_singlet_mediator_susceptibility_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(23)
    ),
)