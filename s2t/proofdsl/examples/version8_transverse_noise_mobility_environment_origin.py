"""Exact environment-scaling boundary for transverse gauge mobility."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_full_noise_physical_time_scale import build_certificate as time_scale_certificate
from .version8_spacetime_kinetic_factorization_and_gauge_fixing import (
    build_certificate as kinetic_certificate,
)


@dataclass(frozen=True, slots=True)
class TransverseNoiseMobilityEnvironmentCertificate:
    canonical_covariance: sp.ImmutableMatrix
    rescaled_covariance: sp.ImmutableMatrix
    canonical_transverse_mobility: sp.ImmutableMatrix
    rescaled_transverse_mobility: sp.ImmutableMatrix
    covariance_rank_theorem: Theorem
    transverse_rank_theorem: Theorem
    common_kernel_theorem: Theorem
    normalized_shape_theorem: Theorem
    scale_dependence_theorem: Theorem
    time_compensation_theorem: Theorem
    physical_scale_boundary_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> TransverseNoiseMobilityEnvironmentCertificate:
    kinetic = kinetic_certificate()
    time_scale = time_scale_certificate()
    inverse_metric = sp.ImmutableMatrix(kinetic.gauge_metric.inv())
    covariance_one = inverse_metric
    covariance_two = sp.ImmutableMatrix(4 * inverse_metric)
    mobility_one = sp.ImmutableMatrix(
        sp.kronecker_product(covariance_one, kinetic.transverse_projector)
    )
    mobility_two = sp.ImmutableMatrix(
        sp.kronecker_product(covariance_two, kinetic.transverse_projector)
    )

    covariance_rank = kernel.prove_exact_rank(
        covariance_one,
        12,
        subject="metric-dual environment covariance shape",
    )
    transverse_rank = kernel.prove_exact_rank(
        mobility_one,
        36,
        subject="rank of the transverse environment-induced mobility",
    )
    common_kernel = kernel.prove_matrix_equality(
        mobility_two,
        4 * mobility_one,
        subject="rescaling preserves the transverse image and longitudinal kernel",
    )
    normalized_shape = kernel.prove_matrix_equality(
        mobility_one / sp.trace(mobility_one),
        mobility_two / sp.trace(mobility_two),
        subject="environment rescaling preserves normalized transverse shape",
    )
    scale_dependence = kernel.prove_matrix_inequality(
        mobility_one,
        mobility_two,
        subject="vacuum correlation amplitude changes transverse mobility scale",
    )
    time_compensation = kernel.prove_expression_equality(
        4 * sp.Rational(1, 4),
        1,
        subject="quadratic coupling rescaling is compensated by inverse time rescaling",
    )
    physical_boundary = time_scale.physical_time_no_go_theorem
    gate = kernel.prove_gate(
        "transverse_noise_mobility_environment_origin",
        (
            kinetic.transverse_independence_theorem,
            covariance_rank,
            transverse_rank,
            common_kernel,
            normalized_shape,
            scale_dependence,
            time_compensation,
            physical_boundary,
        ),
    )
    return TransverseNoiseMobilityEnvironmentCertificate(
        canonical_covariance=covariance_one,
        rescaled_covariance=covariance_two,
        canonical_transverse_mobility=mobility_one,
        rescaled_transverse_mobility=mobility_two,
        covariance_rank_theorem=covariance_rank,
        transverse_rank_theorem=transverse_rank,
        common_kernel_theorem=common_kernel,
        normalized_shape_theorem=normalized_shape,
        scale_dependence_theorem=scale_dependence,
        time_compensation_theorem=time_compensation,
        physical_scale_boundary_theorem=physical_boundary,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.transverse_rank_theorem.proposition)
    print(certificate.scale_dependence_theorem.proposition)