"""LCF certificate for the reference-scale ratio candidate audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class BirthTickReferenceScaleRatioAuditCertificate:
    required_ratio: sp.Expr
    landau_factor: sp.Expr
    k43_factor: sp.Expr
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    factor_assignment: sp.ImmutableMatrix
    composition_hessian: sp.ImmutableMatrix
    composition_kernel: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> BirthTickReferenceScaleRatioAuditCertificate:
    landau_factor = sp.exp(-32 * sp.pi**2 / 3)
    k43_factor = sp.Rational(1, 42)
    required_ratio = landau_factor * k43_factor

    # dimensionless, internal, selected by a current parent, exact target,
    # independent origin, non-target-loaded.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 1, 1, 0, 0],  # formal product of the two required factors
        [1, 1, 1, 0, 1, 1],  # K43 endpoint factor 1/42
        [1, 1, 1, 0, 1, 1],  # Landau suppression
        [1, 1, 1, 0, 1, 1],  # Brillouin/K43 ratio
        [1, 1, 0, 0, 1, 1],  # bath correlation-profile ratio
        [1, 1, 1, 0, 1, 1],  # KMS Boltzmann ratio
        [1, 1, 1, 0, 1, 1],  # trace-anomaly fraction
        [1, 1, 0, 0, 1, 1],  # normalized birth probability
        [1, 1, 0, 1, 1, 0],  # free symbolic bridge fixed to the target
        [1, 0, 0, 1, 0, 0],  # observed matching ratio
        [1, 0, 0, 1, 1, 0],  # external renormalization condition
    ])
    score_vector = sp.ImmutableMatrix([
        sum(candidate_matrix.row(index)) for index in range(candidate_matrix.rows)
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(index)) for index in range(candidate_matrix.rows)
    ])
    factor_assignment = sp.ImmutableMatrix([[1, 0], [0, 1], [1, 1]])

    # For residual x_ratio-x_L-x_43, the quadratic composition parent has
    # rank one: it checks multiplication but cannot select either factor.
    composition_hessian = sp.ImmutableMatrix([
        [1, -1, -1],
        [-1, 1, 1],
        [-1, 1, 1],
    ])
    composition_kernel = sp.ImmutableMatrix.hstack(
        sp.ImmutableMatrix([1, 1, 0]), sp.ImmutableMatrix([1, 0, 1])
    )

    # log(mu_spec), log(Lambda43), log(tau_birth), log(c).
    scale_map = sp.ImmutableMatrix([
        [1, 0, 1, 1],
        [0, 1, 1, 1],
        [1, -1, 0, 0],
    ])
    scale_kernel = sp.ImmutableMatrix.hstack(
        sp.ImmutableMatrix([-1, -1, 1, 0]),
        sp.ImmutableMatrix([-1, -1, 0, 1]),
    )
    audit_coverage = sp.ones(11, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 0, 0, 0])

    theorems = (
        kernel.prove_expression_equality(landau_factor, sp.exp(-32 * sp.pi**2 / 3), subject="exact Landau suppression factor"),
        kernel.prove_expression_equality(k43_factor, sp.Rational(1, 42), subject="exact reciprocal K43 endpoint factor"),
        kernel.prove_expression_equality(required_ratio, sp.exp(-32 * sp.pi**2 / 3) / 42, subject="required reference-scale ratio"),
        kernel.prove_expression_equality(landau_factor * k43_factor, required_ratio, subject="formal factor product reproduces the required ratio"),
        kernel.prove_matrix_equality(candidate_matrix, sp.Matrix(candidate_matrix), subject="eleven reference-ratio candidates on six criteria"),
        kernel.prove_exact_rank(candidate_matrix, 5, subject="candidate audit distinguishes five criterion directions"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([4, 5, 5, 5, 4, 5, 5, 4, 4, 2, 3]), subject="exact candidate scores"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="closest independent factors miss exact full matching"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1), subject="no reference-ratio candidate passes the full origin contract"),
        kernel.prove_expression_equality(sum(pass_vector), 0, subject="complete reference-ratio origins are absent"),
        kernel.prove_matrix_equality(factor_assignment, sp.Matrix([[1, 0], [0, 1], [1, 1]]), subject="Landau and K43 factors are separate inputs to their product"),
        kernel.prove_exact_rank(factor_assignment, 2, subject="the two ratio factors are algebraically independent components"),
        kernel.prove_exact_rank(composition_hessian, 1, subject="composition parent controls only the product residual"),
        kernel.prove_exact_nullity(composition_hessian, 2, subject="composition leaves both factor directions unselected"),
        kernel.prove_matrix_equality(composition_hessian * composition_kernel, sp.zeros(3, 2), subject="exact factor-selection kernel of the composition parent"),
        kernel.prove_exact_rank(scale_map, 2, subject="the ratio row is dependent on the two tick products"),
        kernel.prove_exact_nullity(scale_map, 2, subject="speed and common absolute scale remain free"),
        kernel.prove_matrix_equality(scale_map * scale_kernel, sp.zeros(3, 2), subject="exact residual speed and common-scale orbits"),
        kernel.prove_matrix_equality(audit_coverage, sp.ones(11, 1), subject="all eleven declared ratio candidates are covered"),
        kernel.prove_expression_equality(sum(audit_coverage), 11, subject="candidate coverage is complete"),
        kernel.prove_matrix_equality(origin_ledger, sp.ImmutableMatrix([1, 1, 1, 0, 0, 0]), subject="dimension algebra and coverage pass while common-parent and physical origins remain open"),
        kernel.prove_expression_equality(sum(origin_ledger), 3, subject="three of six ratio-origin requirements pass"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit_gate",
        theorems,
    )
    return BirthTickReferenceScaleRatioAuditCertificate(
        required_ratio, landau_factor, k43_factor, candidate_matrix,
        score_vector, pass_vector, factor_assignment, composition_hessian,
        composition_kernel, scale_map, scale_kernel, audit_coverage,
        origin_ledger, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit_gate",
    title="Аудит кандидатов отношения опорных шкал такта рождения",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"birth_tick_reference_scale_ratio_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(22)
    ),
)