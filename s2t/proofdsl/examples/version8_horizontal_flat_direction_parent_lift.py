"""Exact origin and parent-lift obstruction for the horizontal flat phase."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_fixed_algebra import physical_incidence
from .version8_full_42_carrier_base_k_determinant_compatibility import (
    build_certificate as determinant_certificate,
)
from .version8_full_noise_trace_frame import (
    build_certificate as frame_certificate,
    full_noise_frame,
)
from .version8_gauge_invariant_vacuum_hessian_reconstruction import (
    build_certificate as quotient_certificate,
)


@dataclass(frozen=True, slots=True)
class HorizontalFlatDirectionParentLiftCertificate:
    phase_coordinates: sp.ImmutableMatrix
    phase_metric: sp.ImmutableMatrix
    orbit_phase_coupling: sp.ImmutableMatrix
    horizontal_phase_direction: sp.ImmutableMatrix
    phase_reconstruction_theorem: Theorem
    phase_metric_theorem: Theorem
    gram_hessian_phase_kernel_theorem: Theorem
    orbit_phase_coupling_theorem: Theorem
    horizontal_phase_theorem: Theorem
    quotient_flat_theorem: Theorem
    left_gram_invariance_theorem: Theorem
    right_gram_invariance_theorem: Theorem
    maximal_minor_carrier_theorem: Theorem
    trace_parent_no_go_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HorizontalFlatDirectionParentLiftCertificate:
    determinant = determinant_certificate()
    quotient = quotient_certificate()
    transfer_metric = sp.ImmutableMatrix(frame_certificate().trace_metric[:30, :30])
    transfer_frame = full_noise_frame()[:30]
    incidence = sp.ImmutableMatrix(physical_incidence())

    up_phase = sp.zeros(30, 1)
    up_phase[7] = -sp.Rational(1, 2)
    up_phase[9] = sp.Rational(1, 2)
    rest_phase = sp.zeros(30, 1)
    rest_phase[1] = 1
    rest_phase[7] = sp.Rational(1, 2)
    rest_phase[9] = -sp.Rational(1, 2)
    phase_coordinates = sp.ImmutableMatrix(up_phase.row_join(rest_phase))

    def reconstruct(coordinates: sp.MatrixBase) -> sp.MatrixBase:
        result = sp.zeros(10, 11)
        for coefficient, frame_element in zip(coordinates, transfer_frame):
            result += coefficient * frame_element[11:, :11]
        return result

    up_projector = sp.diag(*([1] * 3 + [0] * 7))
    rest_projector = sp.eye(10) - up_projector
    reconstructed = sp.Matrix.vstack(
        reconstruct(up_phase),
        reconstruct(rest_phase),
    )
    expected = sp.Matrix.vstack(
        sp.I * up_projector * incidence,
        sp.I * rest_projector * incidence,
    )
    phase_reconstruction = kernel.prove_matrix_equality(
        reconstructed,
        expected,
        subject="two independent target-isotypic phase tangents",
    )
    phase_metric = sp.ImmutableMatrix(phase_coordinates.T * transfer_metric * phase_coordinates)
    phase_metric_theorem = kernel.prove_matrix_equality(
        phase_metric,
        sp.diag(6, 20),
        subject="trace metric on the up/rest phase plane",
    )
    gram_phase_kernel = kernel.prove_matrix_equality(
        sp.Matrix(determinant.scalar_hessian) * phase_coordinates,
        sp.zeros(30, 2),
        subject="both phase tangents lie in the fixed Gram Hessian kernel",
    )

    orbit_basis = sp.Matrix(quotient.orbit_basis)
    orbit_phase_coupling = sp.ImmutableMatrix(
        orbit_basis.T * transfer_metric * phase_coordinates
    )
    orbit_phase_coupling_theorem = kernel.prove_matrix_equality(
        orbit_phase_coupling,
        sp.Matrix([[0, 0], [0, 0], [-6, 8]]),
        subject="coupling of the phase plane to the broken gauge orbit",
    )
    horizontal_phase = sp.ImmutableMatrix(phase_coordinates * sp.Matrix([4, 3]))
    horizontal_phase_theorem = kernel.prove_matrix_equality(
        orbit_basis.T * transfer_metric * horizontal_phase,
        sp.zeros(3, 1),
        subject="unique primitive horizontal phase combination four-to-three",
    )
    quotient_flat = kernel.prove_matrix_equality(
        sp.Matrix(quotient.quotient_hessian) * horizontal_phase,
        sp.zeros(30, 1),
        subject="horizontal four-to-three phase remains flat after the quotient",
    )

    z = sp.Symbol("z", nonzero=True)
    phase_matrix = sp.diag(*([z**4] * 3 + [z**3] * 7))
    inverse_phase_matrix = sp.diag(*([z**-4] * 3 + [z**-3] * 7))
    phased_incidence = phase_matrix * incidence
    formal_adjoint = incidence.H * inverse_phase_matrix
    left_gram_invariance = kernel.prove_matrix_equality(
        phased_incidence * formal_adjoint,
        incidence * incidence.H,
        subject="left Gram endpoint is invariant on the horizontal phase circle",
    )
    right_gram_invariance = kernel.prove_matrix_equality(
        formal_adjoint * phased_incidence,
        incidence.H * incidence,
        subject="right Gram endpoint is invariant on the horizontal phase circle",
    )

    maximal_minor_carrier = sp.binomial(11, 10) * sp.binomial(10, 10)
    maximal_minor_theorem = kernel.prove_expression_equality(
        maximal_minor_carrier,
        11,
        subject="maximal minors of a ten-by-eleven transfer form a covector, not a scalar determinant",
    )
    trace_parent_no_go = kernel.prove_gate(
        "all_gram_and_trace_word_parents_are_blind_to_the_horizontal_phase",
        (
            gram_phase_kernel,
            horizontal_phase_theorem,
            left_gram_invariance,
            right_gram_invariance,
            maximal_minor_theorem,
        ),
    )
    gate = kernel.prove_gate(
        "horizontal_flat_direction_parent_lift",
        (
            phase_reconstruction,
            phase_metric_theorem,
            gram_phase_kernel,
            orbit_phase_coupling_theorem,
            horizontal_phase_theorem,
            quotient_flat,
            left_gram_invariance,
            right_gram_invariance,
            maximal_minor_theorem,
            trace_parent_no_go,
        ),
    )
    return HorizontalFlatDirectionParentLiftCertificate(
        phase_coordinates=phase_coordinates,
        phase_metric=phase_metric,
        orbit_phase_coupling=orbit_phase_coupling,
        horizontal_phase_direction=horizontal_phase,
        phase_reconstruction_theorem=phase_reconstruction,
        phase_metric_theorem=phase_metric_theorem,
        gram_hessian_phase_kernel_theorem=gram_phase_kernel,
        orbit_phase_coupling_theorem=orbit_phase_coupling_theorem,
        horizontal_phase_theorem=horizontal_phase_theorem,
        quotient_flat_theorem=quotient_flat,
        left_gram_invariance_theorem=left_gram_invariance,
        right_gram_invariance_theorem=right_gram_invariance,
        maximal_minor_carrier_theorem=maximal_minor_theorem,
        trace_parent_no_go_theorem=trace_parent_no_go,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.phase_metric)
    print(certificate.orbit_phase_coupling)
    print(certificate.horizontal_phase_direction.T)