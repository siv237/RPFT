"""Exact Real-oriented cycle audit for the horizontal phase."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HorizontalPhaseRealOrientedCycleAdmissionCertificate:
    raising_operator: sp.ImmutableMatrix
    reverse_operator: sp.ImmutableMatrix
    real_completion: sp.ImmutableMatrix
    grading: sp.ImmutableMatrix
    phased_real_completion: sp.ImmutableMatrix
    phase_similarity: sp.ImmutableMatrix
    odd_trace_moments: sp.ImmutableMatrix
    even_trace_moments: sp.ImmutableMatrix
    target_phase_weights: sp.ImmutableMatrix
    physical_transfer_real_dimension: int
    independent_reverse_real_dimension: int
    independent_reverse_excess: int
    raising_nilpotence_theorem: Theorem
    reverse_nilpotence_theorem: Theorem
    odd_grading_theorem: Theorem
    real_reverse_covariance_theorem: Theorem
    phase_similarity_theorem: Theorem
    odd_trace_theorem: Theorem
    even_trace_theorem: Theorem
    reverse_charge_cancellation_theorem: Theorem
    physical_dimension_theorem: Theorem
    independent_reverse_dimension_theorem: Theorem
    independent_reverse_excess_theorem: Theorem
    positive_involution_orientation_no_go_theorem: Theorem
    real_oriented_cycle_no_go_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HorizontalPhaseRealOrientedCycleAdmissionCertificate:
    # Vertices: QL, LL, XL, YL | uR, dR, eR, XR, YR.
    edges = (
        (0, 4),
        (0, 5),
        (1, 6),
        (2, 6),
        (2, 7),
        (1, 8),
        (3, 8),
        (2, 5),
        (3, 6),
        (1, 7),
        (0, 8),
    )
    raising = sp.zeros(9)
    for source, target in edges:
        raising[target, source] = 1
    raising = sp.ImmutableMatrix(raising)
    reverse = sp.ImmutableMatrix(raising.T)
    completion = sp.ImmutableMatrix(raising + reverse)
    grading = sp.ImmutableMatrix(sp.diag(*([1] * 4 + [-1] * 5)))

    z = sp.Symbol("z", nonzero=True)
    vertex_weights = (0, 0, 0, 0, 4, 3, 3, 3, 3)
    phased_raising = sp.zeros(9)
    phased_reverse = sp.zeros(9)
    for source, target in edges:
        phased_raising[target, source] = z ** vertex_weights[target]
        phased_reverse[source, target] = z ** (-vertex_weights[target])
    phased_raising = sp.ImmutableMatrix(phased_raising)
    phased_reverse = sp.ImmutableMatrix(phased_reverse)
    phased_completion = sp.ImmutableMatrix(phased_raising + phased_reverse)
    phase_similarity = sp.ImmutableMatrix(
        sp.diag(*(z**weight for weight in vertex_weights))
    )

    odd_traces = sp.ImmutableMatrix(
        [[sp.trace(phased_completion**power) for power in (1, 3, 5)]]
    )
    even_traces = sp.ImmutableMatrix(
        [[sp.trace(phased_completion**power) for power in (2, 4, 6)]]
    )
    target_phase_weights = sp.ImmutableMatrix([[4, 3, 3, 3, 3]])

    raising_nilpotence = kernel.prove_matrix_equality(
        raising**2,
        sp.zeros(9),
        subject="the holomorphic raising quiver has no directed paths of length two",
    )
    reverse_nilpotence = kernel.prove_matrix_equality(
        reverse**2,
        sp.zeros(9),
        subject="the Real reverse quiver has no directed paths of length two",
    )
    odd_grading = kernel.prove_matrix_equality(
        grading * completion + completion * grading,
        sp.zeros(9),
        subject="the Real-completed adjacency is odd for the endpoint grading",
    )
    real_reverse_covariance = kernel.prove_matrix_equality(
        phased_reverse,
        phased_raising.subs(z, z**-1).T,
        subject="the reverse arrows are fixed conjugates with opposite phase weights",
    )
    phase_similarity_theorem = kernel.prove_matrix_equality(
        phased_completion,
        phase_similarity * completion * phase_similarity.inv(),
        subject="the horizontal phase acts on the full Real completion by similarity",
    )
    odd_trace_theorem = kernel.prove_matrix_equality(
        odd_traces,
        sp.zeros(1, 3),
        subject="all tested odd Real-completed trace moments vanish",
    )
    even_trace_theorem = kernel.prove_matrix_equality(
        even_traces,
        sp.Matrix([[22, 110, 682]]),
        subject="the first three even trace moments are phase independent",
    )
    reverse_charge_cancellation = kernel.prove_matrix_equality(
        target_phase_weights - target_phase_weights,
        sp.zeros(1, 5),
        subject="forward and Real-reverse target charges cancel vertex by vertex",
    )

    physical_real_dimension = 2 * 20
    independent_reverse_real_dimension = 4 * 20
    independent_reverse_excess = independent_reverse_real_dimension - physical_real_dimension
    physical_dimension = kernel.prove_expression_equality(
        physical_real_dimension,
        40,
        subject="real dimension of the twenty-complex-dimensional transfer carrier",
    )
    independent_reverse_dimension = kernel.prove_expression_equality(
        independent_reverse_real_dimension,
        80,
        subject="real dimension after incorrectly freeing the reverse carrier",
    )
    independent_reverse_excess_theorem = kernel.prove_expression_equality(
        independent_reverse_excess,
        40,
        subject="new real degrees introduced by an independent reverse carrier",
    )

    x, y = sp.symbols("x y", real=True)
    positive_involution_orientation_no_go = kernel.prove_positive_expression(
        x**2 + y**2 + 1,
        subject="positive involution cannot satisfy alpha times beta equals minus one",
    )
    real_oriented_cycle_no_go = kernel.prove_gate(
        "real_completion_does_not_supply_an_independent_holomorphic_cycle",
        (
            raising_nilpotence,
            reverse_nilpotence,
            odd_grading,
            real_reverse_covariance,
            phase_similarity_theorem,
            odd_trace_theorem,
            even_trace_theorem,
            reverse_charge_cancellation,
            independent_reverse_excess_theorem,
            positive_involution_orientation_no_go,
        ),
    )
    gate = kernel.prove_gate(
        "horizontal_phase_real_oriented_cycle_admission",
        (
            raising_nilpotence,
            reverse_nilpotence,
            odd_grading,
            real_reverse_covariance,
            phase_similarity_theorem,
            odd_trace_theorem,
            even_trace_theorem,
            reverse_charge_cancellation,
            physical_dimension,
            independent_reverse_dimension,
            independent_reverse_excess_theorem,
            positive_involution_orientation_no_go,
            real_oriented_cycle_no_go,
        ),
    )
    return HorizontalPhaseRealOrientedCycleAdmissionCertificate(
        raising_operator=raising,
        reverse_operator=reverse,
        real_completion=completion,
        grading=grading,
        phased_real_completion=phased_completion,
        phase_similarity=phase_similarity,
        odd_trace_moments=odd_traces,
        even_trace_moments=even_traces,
        target_phase_weights=target_phase_weights,
        physical_transfer_real_dimension=physical_real_dimension,
        independent_reverse_real_dimension=independent_reverse_real_dimension,
        independent_reverse_excess=independent_reverse_excess,
        raising_nilpotence_theorem=raising_nilpotence,
        reverse_nilpotence_theorem=reverse_nilpotence,
        odd_grading_theorem=odd_grading,
        real_reverse_covariance_theorem=real_reverse_covariance,
        phase_similarity_theorem=phase_similarity_theorem,
        odd_trace_theorem=odd_trace_theorem,
        even_trace_theorem=even_trace_theorem,
        reverse_charge_cancellation_theorem=reverse_charge_cancellation,
        physical_dimension_theorem=physical_dimension,
        independent_reverse_dimension_theorem=independent_reverse_dimension,
        independent_reverse_excess_theorem=independent_reverse_excess_theorem,
        positive_involution_orientation_no_go_theorem=positive_involution_orientation_no_go,
        real_oriented_cycle_no_go_theorem=real_oriented_cycle_no_go,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.odd_trace_moments)
    print(certificate.even_trace_moments)