"""Exact comparison of the trace metric with the constant-field parent Hessian."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_fixed_algebra import physical_incidence
from .version8_full_noise_trace_frame import (
    build_certificate as trace_frame_certificate,
    full_noise_frame,
)


SOURCE_DIMENSION = 11
TRANSFER_REAL_DIMENSION = 30
GAUGE_REAL_DIMENSION = 12


@dataclass(frozen=True, slots=True)
class FieldNoiseParentHessianComparisonCertificate:
    transfer_origin_hessian: sp.ImmutableMatrix
    constant_field_parent_hessian: sp.ImmutableMatrix
    trace_metric: sp.ImmutableMatrix
    transfer_hessian_rank_theorem: Theorem
    gauge_hessian_zero_theorem: Theorem
    constant_parent_rank_theorem: Theorem
    gauge_trace_metric_rank_theorem: Theorem
    trace_parent_rank_mismatch_theorem: Theorem
    nonzero_gauge_trace_theorem: Theorem
    parent_hessian_no_go_theorem: Theorem
    gate_theorem: Theorem


def _real_part(value: sp.Expr) -> sp.Expr:
    return sp.simplify((value + sp.conjugate(value)) / 2)


def _transfer_origin_hessian() -> sp.ImmutableMatrix:
    reference = sp.ImmutableMatrix(physical_incidence())
    directions = tuple(
        operator[SOURCE_DIMENSION:, :SOURCE_DIMENSION]
        for operator in full_noise_frame()[:TRANSFER_REAL_DIMENSION]
    )
    left_reference = reference.H * reference
    right_reference = reference * reference.H

    def entry(first: sp.MatrixBase, second: sp.MatrixBase) -> sp.Expr:
        left_quadratic = (first.H * second + second.H * first) / 2
        right_quadratic = (first * second.H + second * first.H) / 2
        pairing = sp.trace(left_reference * left_quadratic) + sp.trace(
            right_reference * right_quadratic
        )
        return sp.simplify(-2 * _real_part(pairing))

    return sp.ImmutableMatrix(
        [[entry(left, right) for right in directions] for left in directions]
    )


@lru_cache(maxsize=1)
def build_certificate() -> FieldNoiseParentHessianComparisonCertificate:
    frame = trace_frame_certificate()
    trace_metric = sp.ImmutableMatrix(frame.trace_metric)
    transfer_hessian = _transfer_origin_hessian()
    gauge_hessian = sp.zeros(GAUGE_REAL_DIMENSION)
    parent_hessian = sp.ImmutableMatrix(sp.diag(transfer_hessian, gauge_hessian))
    gauge_trace_metric = sp.ImmutableMatrix(trace_metric[30:, 30:])

    transfer_rank = kernel.prove_exact_rank(
        transfer_hessian,
        TRANSFER_REAL_DIMENSION,
        subject="relative-Gram parent Hessian on the complete transfer carrier",
    )
    gauge_zero = kernel.prove_matrix_equality(
        parent_hessian[30:, 30:],
        sp.zeros(GAUGE_REAL_DIMENSION),
        subject="constant-field gauge-potential Hessian at the zero connection",
    )
    parent_rank = kernel.prove_exact_rank(
        parent_hessian,
        TRANSFER_REAL_DIMENSION,
        subject="constant-field parent Hessian with twelve gauge zero modes",
    )
    gauge_metric_rank = kernel.prove_exact_rank(
        gauge_trace_metric,
        GAUGE_REAL_DIMENSION,
        subject="nondegenerate trace metric on gauge coefficients",
    )
    rank_mismatch = kernel.prove_matrix_inequality(
        sp.Matrix([[parent_hessian.rank()]]),
        sp.Matrix([[trace_metric.rank()]]),
        subject="rank mismatch between parent Hessian and trace metric",
    )
    gauge_trace_nonzero = kernel.prove_matrix_inequality(
        sp.Matrix([[sp.trace(gauge_trace_metric)]]),
        sp.zeros(1),
        subject="nonzero gauge trace metric forbids a nonzero scalar match",
    )
    no_go = kernel.prove_gate(
        "field_noise_metric_parent_hessian_no_go",
        (
            transfer_rank,
            gauge_zero,
            parent_rank,
            gauge_metric_rank,
            rank_mismatch,
            gauge_trace_nonzero,
        ),
    )
    gate = kernel.prove_gate(
        "field_noise_metric_to_parent_hessian_comparison",
        (
            frame.trace_metric_rank_theorem,
            transfer_rank,
            gauge_zero,
            parent_rank,
            gauge_metric_rank,
            rank_mismatch,
            gauge_trace_nonzero,
            no_go,
        ),
    )
    return FieldNoiseParentHessianComparisonCertificate(
        transfer_origin_hessian=transfer_hessian,
        constant_field_parent_hessian=parent_hessian,
        trace_metric=trace_metric,
        transfer_hessian_rank_theorem=transfer_rank,
        gauge_hessian_zero_theorem=gauge_zero,
        constant_parent_rank_theorem=parent_rank,
        gauge_trace_metric_rank_theorem=gauge_metric_rank,
        trace_parent_rank_mismatch_theorem=rank_mismatch,
        nonzero_gauge_trace_theorem=gauge_trace_nonzero,
        parent_hessian_no_go_theorem=no_go,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.constant_parent_rank_theorem.proposition)
    print(certificate.trace_parent_rank_mismatch_theorem.proposition)