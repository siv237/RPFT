"""Exact Kraus/Choi certificate for the one-step cross-arrow channel."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..channel import KrausChannel
from ..kernel import Theorem, kernel
from ..structures import Morphism, Space
from .version8_gauge_twirl_kraus import (
    build_certificate as build_gauge_certificate,
    cross_arrow_families,
    kraus_generator,
)


@dataclass(frozen=True, slots=True)
class StinespringCertificate:
    gram_spectrum: tuple[tuple[int, int], ...]
    maximum_step: sp.Expr
    benchmark_step: sp.Expr
    jump_gram_theorem: Theorem
    gram_spectrum_theorem: Theorem
    step_window_theorem: Theorem
    channel_theorem: Theorem
    trace_theorem: Theorem
    endpoint_theorem: Theorem
    interior_rank_theorem: Theorem
    minimal_environment_theorem: Theorem
    covariance_theorem: Theorem
    tangent_theorem: Theorem
    semigroup_no_go_theorem: Theorem


def _jumps() -> tuple[sp.ImmutableMatrix, ...]:
    qlyr, xldr = cross_arrow_families()
    generator = kraus_generator("stinespring_cross_frame", qlyr + xldr)
    return tuple(jump.matrix for jump in generator.jumps)


def _gram(jumps: tuple[sp.ImmutableMatrix, ...]) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(
        [
            [sp.simplify(sp.trace(left.H * right)) for right in jumps]
            for left in jumps
        ]
    )


def _jump_sum(jumps: tuple[sp.ImmutableMatrix, ...]) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(
        sum((jump.H * jump for jump in jumps), sp.zeros(jumps[0].rows))
    )


def _channel_at(
    jumps: tuple[sp.ImmutableMatrix, ...], gram: sp.ImmutableMatrix, step: sp.Expr
) -> KrausChannel:
    endpoint = Space("E_s+E_t", 21)
    diagonal = [sp.sqrt(sp.simplify(1 - step * value)) for value in gram.diagonal()]
    no_jump = Morphism("K_0", endpoint, endpoint, sp.diag(*diagonal))
    operators = [no_jump]
    operators.extend(
        Morphism(f"K_{index + 1}", endpoint, endpoint, sp.sqrt(step) * jump)
        for index, jump in enumerate(jumps)
    )
    return KrausChannel.make(f"Phi_{step}", operators)


def benchmark_channel() -> KrausChannel:
    """Return the exact interior channel used by downstream history tests."""

    jumps = _jumps()
    return _channel_at(jumps, _jump_sum(jumps), sp.Rational(1, 12))


def _corner_basis() -> tuple[sp.ImmutableMatrix, ...]:
    basis = []
    for start, dimension in ((0, 11), (11, 10)):
        for row in range(dimension):
            for column in range(dimension):
                unit = sp.zeros(21)
                unit[start + row, start + column] = 1
                basis.append(sp.ImmutableMatrix(unit))
    return tuple(basis)


@lru_cache(maxsize=1)
def build_certificate() -> StinespringCertificate:
    jumps = _jumps()
    frame_gram = _gram(jumps)
    jump_gram_theorem = kernel.prove_matrix_equality(
        frame_gram,
        2 * sp.eye(12),
        subject="Hilbert-Schmidt Gram matrix of the cross-arrow jumps",
    )
    gram = _jump_sum(jumps)
    spectrum = Counter(int(value) for value in gram.diagonal())
    expected_diagonal = sorted([0] * 9 + [1] * 6 + [2] * 3 + [3] * 2 + [6])
    gram_spectrum_theorem = kernel.prove_matrix_equality(
        sp.ImmutableMatrix(sorted(gram.diagonal())),
        sp.ImmutableMatrix(expected_diagonal),
        subject="spectrum of the diagonal cross-arrow Gram operator",
    )
    step_parameter = sp.Symbol("p", nonnegative=True)
    step_window = kernel.prove_identity_minus_psd_window(
        gram,
        step_parameter,
        sp.Rational(1, 6),
        subject="one-step Stinespring no-jump square root",
    )

    symbolic_no_jump = sp.diag(
        *[sp.sqrt(sp.simplify(1 - step_parameter * value)) for value in gram.diagonal()]
    )
    channel_theorem = kernel.prove_kraus_family_on_psd_window(
        symbolic_no_jump,
        jumps,
        step_parameter,
        step_window,
        subject="cross-arrow Kraus family on its exact PSD window",
    )
    trace_theorem = kernel.prove_kraus_family_on_psd_window(
        symbolic_no_jump,
        jumps,
        step_parameter,
        step_window,
        subject="trace-preserving cross-arrow Kraus family on its exact PSD window",
        dual=True,
    )

    benchmark = sp.Rational(1, 12)
    channel = _channel_at(jumps, gram, benchmark)
    kernel.prove_kraus_channel_trace_preserving(channel)
    endpoint_theorem = kernel.prove_block_subalgebra_invariant(
        channel,
        (11, 10),
        subject="endpoint algebra under the exact one-step channel",
    )
    minimal_environment = kernel.prove_minimal_stinespring_dimension(
        channel,
        13,
        subject="minimal one-step cross-arrow environment",
    )

    symbolic_columns = [
        sp.ImmutableMatrix(441, 1, list(symbolic_no_jump))
    ] + [
        sp.sqrt(step_parameter) * sp.ImmutableMatrix(441, 1, list(jump))
        for jump in jumps
    ]
    interior_rank = kernel.prove_exact_rank(
        sp.ImmutableMatrix.hstack(*symbolic_columns),
        13,
        subject="Kraus rank for every positive interior step",
    )

    gauge = build_gauge_certificate()
    covariance = kernel.prove_covariant_channel_from_orthogonal_frame(
        channel,
        gauge.gauge_covariance_theorem,
        gauge.basis_invariance_theorem,
        subject="gauge-covariant minimal Stinespring environment",
    )
    tangent = kernel.prove_kraus_family_tangent(
        symbolic_no_jump,
        jumps,
        step_parameter,
        subject="one-step channel tangent equals the cross-arrow GKSL generator",
        premises=(step_window,),
    )

    first = _channel_at(jumps, gram, sp.Rational(1, 50))
    second = _channel_at(jumps, gram, sp.Rational(3, 100))
    added = _channel_at(jumps, gram, sp.Rational(1, 20))
    semigroup_witness = None
    composed_image = None
    added_image = None
    for observable in _corner_basis():
        composed = first.act(second.act(observable))
        direct = added.act(observable)
        if composed != direct:
            semigroup_witness = observable
            composed_image = composed
            added_image = direct
            break
    assert semigroup_witness is not None
    semigroup_no_go = kernel.prove_matrix_inequality(
        composed_image,
        added_image,
        subject="Phi_1/50 composed Phi_3/100 differs from Phi_1/20",
    )

    return StinespringCertificate(
        gram_spectrum=tuple(sorted(spectrum.items())),
        maximum_step=sp.Rational(1, 6),
        benchmark_step=benchmark,
        jump_gram_theorem=jump_gram_theorem,
        gram_spectrum_theorem=gram_spectrum_theorem,
        step_window_theorem=step_window,
        channel_theorem=channel_theorem,
        trace_theorem=trace_theorem,
        endpoint_theorem=endpoint_theorem,
        interior_rank_theorem=interior_rank,
        minimal_environment_theorem=minimal_environment,
        covariance_theorem=covariance,
        tangent_theorem=tangent,
        semigroup_no_go_theorem=semigroup_no_go,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.gram_spectrum)
    print(certificate.minimal_environment_theorem.proposition)