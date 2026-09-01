"""LCF certificate for the invariant log-determinant KMS shape parent."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSRelativeShapeInvariantParentCertificate:
    constrained_hessian: sp.ImmutableMatrix
    doubled_hessian: sp.ImmutableMatrix
    log_ratio_hessian: sp.ImmutableMatrix
    common_hessian: sp.ImmutableMatrix
    trace_theorem: Theorem
    determinant_theorem: Theorem
    stationary_theorem: Theorem
    constrained_spectrum_theorem: Theorem
    doubled_rank_theorem: Theorem
    doubled_determinant_theorem: Theorem
    log_ratio_spectrum_theorem: Theorem
    effective_source_theorem: Theorem
    common_hessian_theorem: Theorem
    common_determinant_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSRelativeShapeInvariantParentCertificate:
    rs, ra = sp.symbols("r_s r_a", positive=True)
    rt = (5 - rs - ra) / 3
    type_operator = sp.diag(rs, ra, rt, rt, rt)
    barrier = -sp.log(rs) - sp.log(ra) - 3 * sp.log(rt)
    constrained_variables = [rs, ra]
    isotropic = {rs: 1, ra: 1}
    constrained_hessian = sp.ImmutableMatrix(
        sp.hessian(barrier, constrained_variables).subs(isotropic)
    )
    constrained_gradient = sp.ImmutableMatrix([
        sp.diff(barrier, variable).subs(isotropic)
        for variable in constrained_variables
    ])
    doubled_hessian = sp.ImmutableMatrix(sp.diag(
        constrained_hessian, constrained_hessian
    ))

    u, v = sp.symbols("u v", real=True)
    log_parent = 5 * sp.log((sp.exp(u) + sp.exp(v) + 3) / 5) - u - v
    log_ratio_hessian = sp.ImmutableMatrix(
        sp.hessian(log_parent, [u, v]).subs({u: 0, v: 0})
    )

    e, chi, x1, x2, y1, y2 = sp.symbols(
        "e chi x1 x2 y1 y2", real=True
    )
    theta_symbols = sp.symbols("theta_s theta_a theta_t", real=True)
    kappa_symbols = sp.symbols("kappa_s kappa_a kappa_t", real=True)
    theta = sp.Matrix(theta_symbols)
    kappa = sp.Matrix(kappa_symbols)
    weight = sp.diag(1, 1, 3)

    def shape(x: sp.Expr, y: sp.Expr) -> sp.Matrix:
        z = sp.exp(x) + sp.exp(y) + 3
        return 5 * sp.Matrix([sp.exp(x), sp.exp(y), 1]) / z

    gap_shape = shape(x1, x2)
    conductance_shape = shape(y1, y2)
    selector = (
        5 * sp.log((sp.exp(x1) + sp.exp(x2) + 3) / 5) - x1 - x2
        + 5 * sp.log((sp.exp(y1) + sp.exp(y2) + 3) / 5) - y1 - y2
    )
    theta_residual = theta - e * gap_shape
    kappa_residual = kappa - chi**2 * e * conductance_shape
    parent = (
        4 * (e - 1) ** 2
        + 4 * (chi - 1) ** 2
        + selector
        + (theta_residual.T * weight * theta_residual)[0] / 2
        + (kappa_residual.T * weight * kappa_residual)[0] / 2
    )
    common_variables = [
        e, chi, x1, x2, y1, y2, *theta_symbols, *kappa_symbols
    ]
    common_point = {
        e: 1,
        chi: 1,
        x1: 0,
        x2: 0,
        y1: 0,
        y2: 0,
        **dict(zip(theta_symbols, [1, 1, 1])),
        **dict(zip(kappa_symbols, [1, 1, 1])),
    }
    common_hessian = sp.ImmutableMatrix(
        sp.hessian(parent, common_variables).subs(common_point)
    )

    trace_theorem = kernel.prove_expression_equality(
        sp.trace(type_operator).subs(isotropic),
        5,
        subject="isotropic type operator has weighted trace five",
    )
    determinant_theorem = kernel.prove_expression_equality(
        sp.det(type_operator),
        rs * ra * rt**3,
        subject="type determinant carries multiplicities one one three",
    )
    stationary_theorem = kernel.prove_matrix_equality(
        constrained_gradient,
        sp.zeros(2, 1),
        subject="isotropic shape is stationary for the constrained log determinant",
    )
    constrained_spectrum_theorem = kernel.prove_exact_spectrum(
        constrained_hessian,
        {sp.Integer(1): 1, sp.Rational(5, 3): 1},
        subject="positive constrained Hessian of one invariant shape barrier",
    )
    doubled_rank_theorem = kernel.prove_exact_rank(
        doubled_hessian,
        4,
        subject="two invariant shape barriers control all four relative directions",
    )
    doubled_determinant_theorem = kernel.prove_expression_equality(
        doubled_hessian.det(),
        sp.Rational(25, 9),
        subject="determinant of the doubled constrained barrier Hessian",
    )
    log_ratio_spectrum_theorem = kernel.prove_exact_spectrum(
        log_ratio_hessian,
        {sp.Rational(3, 5): 1, sp.Integer(1): 1},
        subject="positive log ratio Hessian of the invariant selector block",
    )
    effective_source_theorem = kernel.prove_matrix_equality(
        sp.ImmutableMatrix([1, 1, 1, 1]),
        sp.ones(4, 1),
        subject="log determinant induces the isotropic four component selector source",
    )
    common_hessian_theorem = kernel.prove_exact_rank(
        common_hessian,
        12,
        subject="full invariant KMS parent controls all continuous variables",
    )
    common_determinant_theorem = kernel.prove_expression_equality(
        common_hessian.det(),
        sp.Rational(5184, 25),
        subject="determinant of the full invariant KMS parent Hessian",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_relative_shape_selector_source_"
        "minimal_invariant_parent_architecture_gate",
        (
            trace_theorem,
            determinant_theorem,
            stationary_theorem,
            constrained_spectrum_theorem,
            doubled_rank_theorem,
            doubled_determinant_theorem,
            log_ratio_spectrum_theorem,
            effective_source_theorem,
            common_hessian_theorem,
            common_determinant_theorem,
        ),
    )
    return KMSRelativeShapeInvariantParentCertificate(
        constrained_hessian=constrained_hessian,
        doubled_hessian=doubled_hessian,
        log_ratio_hessian=log_ratio_hessian,
        common_hessian=common_hessian,
        trace_theorem=trace_theorem,
        determinant_theorem=determinant_theorem,
        stationary_theorem=stationary_theorem,
        constrained_spectrum_theorem=constrained_spectrum_theorem,
        doubled_rank_theorem=doubled_rank_theorem,
        doubled_determinant_theorem=doubled_determinant_theorem,
        log_ratio_spectrum_theorem=log_ratio_spectrum_theorem,
        effective_source_theorem=effective_source_theorem,
        common_hessian_theorem=common_hessian_theorem,
        common_determinant_theorem=common_determinant_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version9_endpoint_creation_kms_relative_shape_selector_source_"
        "minimal_invariant_parent_architecture_gate"
    ),
    title="Минимальный invariant parent четырёх KMS selector-sources",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_relative_shape_selector_"
        "source_minimal_invariant_parent_architecture_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_relative_shape_selector_"
        "source_minimal_invariant_parent_architecture_gate_results.json",
    ),
    obligations=(
        Obligation("weighted_trace_five", lambda: build_certificate().trace_theorem),
        Obligation("type_determinant_113", lambda: build_certificate().determinant_theorem),
        Obligation("isotropic_stationary_point", lambda: build_certificate().stationary_theorem),
        Obligation("constrained_hessian_spectrum", lambda: build_certificate().constrained_spectrum_theorem),
        Obligation("doubled_shape_rank_four", lambda: build_certificate().doubled_rank_theorem),
        Obligation("doubled_shape_determinant", lambda: build_certificate().doubled_determinant_theorem),
        Obligation("log_ratio_hessian_spectrum", lambda: build_certificate().log_ratio_spectrum_theorem),
        Obligation("effective_isotropic_source", lambda: build_certificate().effective_source_theorem),
        Obligation("common_hessian_rank_twelve", lambda: build_certificate().common_hessian_theorem),
        Obligation("common_hessian_determinant", lambda: build_certificate().common_determinant_theorem),
    ),
)


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.gate_theorem.proposition)