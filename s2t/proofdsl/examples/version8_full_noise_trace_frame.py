"""Exact construction of the full 42-real noise frame and trace metric."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_fixed_algebra import physical_incidence
from .version8_full_noise_cotangent_carrier import build_certificate as carrier_certificate
from .version8_gauge_twirl_kraus import (
    _dirac_jump,
    _endpoint_gauge_generators,
    cross_arrow_families,
    internal_control_arrows,
)


@dataclass(frozen=True, slots=True)
class FullNoiseTraceFrameCertificate:
    orbit_dimensions: tuple[int, ...]
    transfer_complex_dimension: int
    transfer_real_dimension: int
    gauge_real_dimension: int
    full_frame_dimension: int
    added_linking_directions: int
    added_internal_directions: int
    trace_metric: sp.ImmutableMatrix
    dual_rate_metric: sp.ImmutableMatrix
    orbit_dimension_theorem: Theorem
    transfer_rank_theorem: Theorem
    full_frame_rank_theorem: Theorem
    trace_metric_rank_theorem: Theorem
    transfer_gauge_orthogonality_theorem: Theorem
    trace_dual_identity_theorem: Theorem
    missing_direction_decomposition_theorem: Theorem
    frame_gate_theorem: Theorem


def _column_basis(matrices: list[sp.ImmutableMatrix]) -> list[sp.ImmutableMatrix]:
    columns = sp.Matrix.hstack(*(sp.Matrix(list(item)) for item in matrices))
    pivots = columns.rref()[1]
    return [matrices[index] for index in pivots]


def _linking_orbit_basis() -> tuple[list[sp.ImmutableMatrix], tuple[int, ...]]:
    basis = [sp.ImmutableMatrix(physical_incidence())]
    dimensions = [1]
    generators = _endpoint_gauge_generators()
    for _ in range(4):
        generated = list(basis)
        for arrow in basis:
            for generator in generators:
                generated.append(
                    sp.ImmutableMatrix(
                        generator[11:, 11:] * arrow - arrow * generator[:11, :11]
                    )
                )
        basis = _column_basis(generated)
        dimensions.append(len(basis))
        if dimensions[-1] == dimensions[-2]:
            break
    return basis, tuple(dimensions)


def full_noise_frame() -> tuple[sp.ImmutableMatrix, ...]:
    linking, _ = _linking_orbit_basis()
    qlyr, xldr = cross_arrow_families()
    internal = internal_control_arrows()
    heavy_complex = list(qlyr[::2]) + list(xldr[::2]) + list(internal[::2])
    transfer_complex = _column_basis(linking + heavy_complex)
    transfer_frame: list[sp.ImmutableMatrix] = []
    for arrow in transfer_complex:
        transfer_frame.extend((_dirac_jump(arrow), _dirac_jump(sp.I * arrow)))
    return tuple(transfer_frame + list(_endpoint_gauge_generators()))


@lru_cache(maxsize=1)
def build_certificate() -> FullNoiseTraceFrameCertificate:
    carrier = carrier_certificate()
    linking, orbit_dimensions = _linking_orbit_basis()
    full_frame = list(full_noise_frame())
    transfer_frame = full_frame[:30]
    gauge_frame = full_frame[30:]
    transfer_complex = _column_basis(
        linking
        + list(cross_arrow_families()[0][::2])
        + list(cross_arrow_families()[1][::2])
        + list(internal_control_arrows()[::2])
    )
    flattened_transfer = sp.Matrix.hstack(
        *(sp.Matrix(list(item)) for item in transfer_complex)
    )
    flattened_full = sp.Matrix.hstack(*(sp.Matrix(list(item)) for item in full_frame))
    trace_metric = sp.ImmutableMatrix(
        [
            [sp.simplify(sp.trace(left.H * right)) for right in full_frame]
            for left in full_frame
        ]
    )
    dual_rate = sp.ImmutableMatrix(trace_metric.inv())

    orbit_theorem = kernel.prove_expression_equality(
        len(linking), 5, subject="five-complex-dimensional linking gauge orbit"
    )
    transfer_rank = kernel.prove_exact_rank(
        flattened_transfer, 15, subject="full gauge-closed complex transfer frame"
    )
    full_rank = kernel.prove_exact_rank(
        flattened_full, 42, subject="full mixed-real Hermitian noise frame"
    )
    metric_rank = kernel.prove_exact_rank(
        trace_metric, 42, subject="nondegenerate full finite-trace noise metric"
    )
    orthogonality = kernel.prove_matrix_equality(
        trace_metric[:30, 30:],
        sp.zeros(30, 12),
        subject="exact transfer-gauge trace orthogonality",
    )
    dual_identity = kernel.prove_matrix_equality(
        trace_metric * dual_rate,
        sp.eye(42),
        subject="full trace metric and cotangent rate tensor are inverse",
    )
    missing_decomposition = kernel.prove_expression_equality(
        (2 * 5 - 1) + 2 * 4,
        carrier.missing_real_directions,
        subject="nine linking-orbit plus eight internal directions close the deficit",
    )
    gate = kernel.prove_gate(
        "full_noise_trace_frame",
        (
            orbit_theorem,
            transfer_rank,
            full_rank,
            metric_rank,
            orthogonality,
            dual_identity,
            missing_decomposition,
        ),
    )
    return FullNoiseTraceFrameCertificate(
        orbit_dimensions=orbit_dimensions,
        transfer_complex_dimension=15,
        transfer_real_dimension=30,
        gauge_real_dimension=12,
        full_frame_dimension=42,
        added_linking_directions=9,
        added_internal_directions=8,
        trace_metric=trace_metric,
        dual_rate_metric=dual_rate,
        orbit_dimension_theorem=orbit_theorem,
        transfer_rank_theorem=transfer_rank,
        full_frame_rank_theorem=full_rank,
        trace_metric_rank_theorem=metric_rank,
        transfer_gauge_orthogonality_theorem=orthogonality,
        trace_dual_identity_theorem=dual_identity,
        missing_direction_decomposition_theorem=missing_decomposition,
        frame_gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.orbit_dimensions)
    print(certificate.trace_metric_rank_theorem.proposition)