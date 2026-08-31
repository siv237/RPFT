"""Exact transverse-longitudinal factorization of the gauge Hessian."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_full_noise_trace_frame import build_certificate as trace_frame_certificate
from .version8_metric_dual_environment_parent_action import (
    build_certificate as parent_origin_certificate,
)


@dataclass(frozen=True, slots=True)
class SpacetimeKineticFactorizationCertificate:
    gauge_metric: sp.ImmutableMatrix
    transverse_projector: sp.ImmutableMatrix
    longitudinal_projector: sp.ImmutableMatrix
    ungauged_hessian: sp.ImmutableMatrix
    gauge_fixed_hessian: sp.ImmutableMatrix
    gauge_fixed_inverse: sp.ImmutableMatrix
    projector_theorem: Theorem
    ungauged_rank_theorem: Theorem
    ungauged_nullity_theorem: Theorem
    gauge_fixed_rank_theorem: Theorem
    inverse_theorem: Theorem
    transverse_independence_theorem: Theorem
    longitudinal_dependence_theorem: Theorem
    dynamical_boundary_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SpacetimeKineticFactorizationCertificate:
    frame = trace_frame_certificate()
    parent_origin = parent_origin_certificate()
    gauge_metric = sp.ImmutableMatrix(frame.trace_metric[30:, 30:])
    gauge_inverse = sp.ImmutableMatrix(gauge_metric.inv())

    longitudinal = sp.ImmutableMatrix(sp.diag(1, 0, 0, 0))
    transverse = sp.ImmutableMatrix(sp.eye(4) - longitudinal)
    projector_residual = sp.diag(
        transverse * transverse - transverse,
        longitudinal * longitudinal - longitudinal,
        transverse * longitudinal,
        transverse + longitudinal - sp.eye(4),
    )
    projector_theorem = kernel.prove_matrix_equality(
        projector_residual,
        sp.zeros(16),
        subject="exact transverse-longitudinal projector decomposition",
    )

    ungauged = sp.ImmutableMatrix(sp.kronecker_product(gauge_metric, transverse))
    ungauged_rank = kernel.prove_exact_rank(
        ungauged,
        36,
        subject="rank of the ungauged four-dimensional gauge Hessian",
    )
    ungauged_nullity = kernel.prove_exact_nullity(
        ungauged,
        12,
        subject="longitudinal gauge kernel before gauge fixing",
    )

    xi = sp.Symbol("xi", positive=True)
    spacetime_fixed = sp.ImmutableMatrix(transverse + longitudinal / xi)
    fixed = sp.ImmutableMatrix(sp.kronecker_product(gauge_metric, spacetime_fixed))
    fixed_inverse = sp.ImmutableMatrix(
        sp.kronecker_product(gauge_inverse, transverse + xi * longitudinal)
    )
    fixed_rank = kernel.prove_exact_rank(
        fixed,
        48,
        subject="full rank after covariant gauge fixing",
    )
    inverse_theorem = kernel.prove_matrix_equality(
        fixed * fixed_inverse,
        sp.eye(48),
        subject="factorized inverse of the gauge-fixed Hessian",
    )

    projector_48_transverse = sp.kronecker_product(sp.eye(12), transverse)
    inverse_xi_one = sp.kronecker_product(
        gauge_inverse, transverse + longitudinal
    )
    inverse_xi_two = sp.kronecker_product(
        gauge_inverse, transverse + 2 * longitudinal
    )
    transverse_independence = kernel.prove_matrix_equality(
        projector_48_transverse * inverse_xi_one * projector_48_transverse,
        projector_48_transverse * inverse_xi_two * projector_48_transverse,
        subject="gauge-parameter independence of the transverse inverse",
    )
    longitudinal_dependence = kernel.prove_matrix_inequality(
        inverse_xi_one,
        inverse_xi_two,
        subject="gauge-parameter dependence of the full inverse",
    )

    dynamical_boundary = parent_origin.parent_origin_no_go_theorem
    gate = kernel.prove_gate(
        "spacetime_kinetic_factorization_and_gauge_fixing",
        (
            frame.trace_metric_rank_theorem,
            projector_theorem,
            ungauged_rank,
            ungauged_nullity,
            fixed_rank,
            inverse_theorem,
            transverse_independence,
            longitudinal_dependence,
            dynamical_boundary,
        ),
    )
    return SpacetimeKineticFactorizationCertificate(
        gauge_metric=gauge_metric,
        transverse_projector=transverse,
        longitudinal_projector=longitudinal,
        ungauged_hessian=ungauged,
        gauge_fixed_hessian=fixed,
        gauge_fixed_inverse=fixed_inverse,
        projector_theorem=projector_theorem,
        ungauged_rank_theorem=ungauged_rank,
        ungauged_nullity_theorem=ungauged_nullity,
        gauge_fixed_rank_theorem=fixed_rank,
        inverse_theorem=inverse_theorem,
        transverse_independence_theorem=transverse_independence,
        longitudinal_dependence_theorem=longitudinal_dependence,
        dynamical_boundary_theorem=dynamical_boundary,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.ungauged_rank_theorem.proposition)
    print(certificate.ungauged_nullity_theorem.proposition)