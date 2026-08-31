"""Exact compatible-complex-structure and trace-metric selector audit."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel


def _omega52() -> sp.ImmutableMatrix:
    omega = sp.zeros(52)
    for pair in range(26):
        start = 2 * pair
        omega[start, start + 1] = 1
        omega[start + 1, start] = -1
    return sp.ImmutableMatrix(omega)


def _metric_extension(scale: sp.Expr) -> sp.ImmutableMatrix:
    diagonal: list[sp.Expr] = [sp.Integer(1)] * 42
    for _ in range(5):
        diagonal.extend((scale, 1 / scale))
    return sp.ImmutableMatrix(sp.diag(*diagonal))


@dataclass(frozen=True, slots=True)
class HorizontalPhaseCotangentComplexStructureMetricSelectorCertificate:
    symplectic_form: sp.ImmutableMatrix
    trace_projection_42: sp.ImmutableMatrix
    transfer_projection_30: sp.ImmutableMatrix
    pulled_trace_metric: sp.ImmutableMatrix
    pulled_transfer_metric: sp.ImmutableMatrix
    first_metric_extension: sp.ImmutableMatrix
    second_metric_extension: sp.ImmutableMatrix
    first_complex_structure: sp.ImmutableMatrix
    second_complex_structure: sp.ImmutableMatrix
    full_real_dimension: int
    trace_metric_dimension: int
    trace_metric_deficit: int
    transfer_metric_deficit: int
    full_dimension_theorem: Theorem
    trace_pullback_rank_theorem: Theorem
    trace_pullback_nullity_theorem: Theorem
    transfer_pullback_rank_theorem: Theorem
    transfer_pullback_nullity_theorem: Theorem
    first_complex_structure_theorem: Theorem
    second_complex_structure_theorem: Theorem
    first_compatibility_theorem: Theorem
    second_compatibility_theorem: Theorem
    trace_restriction_theorem: Theorem
    extension_nonuniqueness_theorem: Theorem
    trace_metric_selector_no_go_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HorizontalPhaseCotangentComplexStructureMetricSelectorCertificate:
    full_real_dimension = 52
    trace_metric_dimension = 42
    trace_metric_deficit = full_real_dimension - trace_metric_dimension
    transfer_metric_deficit = full_real_dimension - 30
    omega = _omega52()
    projection_42 = sp.ImmutableMatrix.hstack(sp.eye(42), sp.zeros(42, 10))
    projection_30 = sp.ImmutableMatrix.hstack(sp.eye(30), sp.zeros(30, 22))
    pulled_trace = sp.ImmutableMatrix(projection_42.T * projection_42)
    pulled_transfer = sp.ImmutableMatrix(projection_30.T * projection_30)
    first_metric = _metric_extension(sp.Integer(1))
    second_metric = _metric_extension(sp.Integer(2))
    first_complex = sp.ImmutableMatrix(-omega * first_metric)
    second_complex = sp.ImmutableMatrix(-omega * second_metric)

    full_dimension_theorem = kernel.prove_expression_equality(
        full_real_dimension,
        52,
        subject="real dimension of the completed symplectic carrier",
    )
    trace_pullback_rank_theorem = kernel.prove_exact_rank(
        pulled_trace,
        42,
        subject="maximal rank supplied by the existing full trace metric",
    )
    trace_pullback_nullity_theorem = kernel.prove_exact_nullity(
        pulled_trace,
        10,
        subject="unavoidable trace-metric deficit on the symplectic carrier",
    )
    transfer_pullback_rank_theorem = kernel.prove_exact_rank(
        pulled_transfer,
        30,
        subject="rank supplied by the existing transfer trace metric",
    )
    transfer_pullback_nullity_theorem = kernel.prove_exact_nullity(
        pulled_transfer,
        22,
        subject="transfer-only metric deficit on the symplectic carrier",
    )
    first_complex_structure_theorem = kernel.prove_matrix_equality(
        first_complex**2,
        -sp.eye(52),
        subject="first metric extension defines a compatible complex structure",
    )
    second_complex_structure_theorem = kernel.prove_matrix_equality(
        second_complex**2,
        -sp.eye(52),
        subject="second metric extension defines a compatible complex structure",
    )
    first_compatibility_theorem = kernel.prove_matrix_equality(
        omega * first_complex,
        first_metric,
        subject="first positive metric equals Omega J",
    )
    second_compatibility_theorem = kernel.prove_matrix_equality(
        omega * second_complex,
        second_metric,
        subject="second positive metric equals Omega J",
    )
    trace_restriction_theorem = kernel.prove_matrix_equality(
        projection_42 * second_metric * projection_42.T,
        sp.eye(42),
        subject="both compatible extensions preserve the normalized old trace metric",
    )
    extension_nonuniqueness_theorem = kernel.prove_matrix_inequality(
        first_metric,
        second_metric,
        subject="the old trace metric admits distinct compatible positive extensions",
    )
    no_go = kernel.prove_gate(
        "existing_trace_metric_does_not_select_a_unique_compatible_complex_structure",
        (
            trace_pullback_rank_theorem,
            trace_pullback_nullity_theorem,
            first_complex_structure_theorem,
            second_complex_structure_theorem,
            trace_restriction_theorem,
            extension_nonuniqueness_theorem,
        ),
    )
    gate = kernel.prove_gate(
        "horizontal_phase_cotangent_complex_structure_metric_selector",
        (
            full_dimension_theorem,
            trace_pullback_rank_theorem,
            trace_pullback_nullity_theorem,
            transfer_pullback_rank_theorem,
            transfer_pullback_nullity_theorem,
            first_complex_structure_theorem,
            second_complex_structure_theorem,
            first_compatibility_theorem,
            second_compatibility_theorem,
            trace_restriction_theorem,
            extension_nonuniqueness_theorem,
            no_go,
        ),
    )
    return HorizontalPhaseCotangentComplexStructureMetricSelectorCertificate(
        symplectic_form=omega,
        trace_projection_42=projection_42,
        transfer_projection_30=projection_30,
        pulled_trace_metric=pulled_trace,
        pulled_transfer_metric=pulled_transfer,
        first_metric_extension=first_metric,
        second_metric_extension=second_metric,
        first_complex_structure=first_complex,
        second_complex_structure=second_complex,
        full_real_dimension=full_real_dimension,
        trace_metric_dimension=trace_metric_dimension,
        trace_metric_deficit=trace_metric_deficit,
        transfer_metric_deficit=transfer_metric_deficit,
        full_dimension_theorem=full_dimension_theorem,
        trace_pullback_rank_theorem=trace_pullback_rank_theorem,
        trace_pullback_nullity_theorem=trace_pullback_nullity_theorem,
        transfer_pullback_rank_theorem=transfer_pullback_rank_theorem,
        transfer_pullback_nullity_theorem=transfer_pullback_nullity_theorem,
        first_complex_structure_theorem=first_complex_structure_theorem,
        second_complex_structure_theorem=second_complex_structure_theorem,
        first_compatibility_theorem=first_compatibility_theorem,
        second_compatibility_theorem=second_compatibility_theorem,
        trace_restriction_theorem=trace_restriction_theorem,
        extension_nonuniqueness_theorem=extension_nonuniqueness_theorem,
        trace_metric_selector_no_go_theorem=no_go,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.trace_metric_deficit)