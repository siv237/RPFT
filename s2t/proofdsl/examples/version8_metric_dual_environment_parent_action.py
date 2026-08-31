"""Exact no-go for deriving the metric-dual bath from the field action alone."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from ..lindblad import LindbladGenerator
from ..structures import Morphism, Space
from .version8_gauge_twirl_kraus import (
    _endpoint_gauge_generators,
    cross_arrow_families,
    kraus_generator,
)
from .version8_microscopic_interaction_hamiltonian import _jumps
from .version8_trace_dual_cross_coupling import build_certificate as trace_dual_certificate


DIMENSION = 12
SYSTEM_DIMENSION = 21


@dataclass(frozen=True, slots=True)
class MetricDualEnvironmentParentActionCertificate:
    alternative_rate_metric: sp.ImmutableMatrix
    dynamical_witness: tuple[int, int]
    field_metric_theorem: Theorem
    dual_metric_theorem: Theorem
    parent_underdetermination_theorem: Theorem
    distinct_dynamics_theorem: Theorem
    absolute_scale_no_go_theorem: Theorem
    parent_origin_no_go_theorem: Theorem


def _generator(name: str, rates: tuple[sp.Expr, ...]) -> LindbladGenerator:
    endpoint = Space("E_s+E_t", SYSTEM_DIMENSION)
    zero = Morphism(f"H_0_{name}", endpoint, endpoint, sp.zeros(SYSTEM_DIMENSION))
    return LindbladGenerator.make(
        name,
        zero,
        tuple(
            Morphism(f"D_{name}_{index}", endpoint, endpoint, jump)
            for index, jump in enumerate(_jumps())
        ),
        rates,
    )


@lru_cache(maxsize=1)
def build_certificate() -> MetricDualEnvironmentParentActionCertificate:
    trace_dual = trace_dual_certificate()
    field_metric = sp.ImmutableMatrix(3 * sp.eye(DIMENSION))
    canonical_rate = sp.ImmutableMatrix(sp.eye(DIMENSION) / 3)
    alternative_rate = sp.ImmutableMatrix(
        sp.diag(*([sp.Rational(1, 3)] * 6 + [sp.Rational(2, 3)] * 6))
    )

    parent_underdetermination = kernel.prove_parent_action_rate_metric_underdetermination(
        field_metric,
        canonical_rate,
        alternative_rate,
        _jumps(),
        _endpoint_gauge_generators(),
        subject="two gauge-compatible bath completions of one cross-field action",
        premises=(trace_dual.field_metric_theorem, trace_dual.dual_metric_theorem),
    )

    canonical_generator = _generator(
        "riesz_dual_cross", tuple([sp.Rational(1, 3)] * DIMENSION)
    )
    alternative_generator = _generator(
        "anisotropic_parent_completion",
        tuple([sp.Rational(1, 3)] * 6 + [sp.Rational(2, 3)] * 6),
    )
    witness = None
    canonical_image = None
    alternative_image = None
    for row in range(SYSTEM_DIMENSION):
        for column in range(SYSTEM_DIMENSION):
            unit = sp.zeros(SYSTEM_DIMENSION)
            unit[row, column] = 1
            left = canonical_generator.act(unit)
            right = alternative_generator.act(unit)
            if left != right:
                witness = (row, column)
                canonical_image = left
                alternative_image = right
                break
        if witness is not None:
            break
    assert witness is not None
    assert canonical_image is not None and alternative_image is not None
    distinct_dynamics = kernel.prove_matrix_inequality(
        canonical_image,
        alternative_image,
        subject="same field action admits distinct reduced cross dynamics",
    )

    parent_origin_no_go = kernel.prove_gate(
        "metric_dual_environment_parent_action_origin_no_go",
        (
            trace_dual.field_metric_theorem,
            trace_dual.dual_metric_theorem,
            parent_underdetermination,
            distinct_dynamics,
            trace_dual.absolute_scale_no_go_theorem,
        ),
    )
    return MetricDualEnvironmentParentActionCertificate(
        alternative_rate_metric=alternative_rate,
        dynamical_witness=witness,
        field_metric_theorem=trace_dual.field_metric_theorem,
        dual_metric_theorem=trace_dual.dual_metric_theorem,
        parent_underdetermination_theorem=parent_underdetermination,
        distinct_dynamics_theorem=distinct_dynamics,
        absolute_scale_no_go_theorem=trace_dual.absolute_scale_no_go_theorem,
        parent_origin_no_go_theorem=parent_origin_no_go,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.parent_underdetermination_theorem.proposition)
    print(certificate.dynamical_witness)