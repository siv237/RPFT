"""Exact common-a4 relative kinetic weight and its lift boundary."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_full_field_kinetic_supermetric_assembly import (
    build_certificate as supermetric_certificate,
)


@dataclass(frozen=True, slots=True)
class FullFieldKineticRelativeWeightCertificate:
    gamma_matrices: tuple[sp.ImmutableMatrix, ...]
    gamma_five: sp.ImmutableMatrix
    scalar_coefficient: sp.Expr
    gauge_coefficient: sp.Expr
    scalar_to_gauge_ratio: sp.Expr
    clifford_theorem: Theorem
    scalar_trace_theorem: Theorem
    gauge_trace_theorem: Theorem
    positive_gauge_theorem: Theorem
    relative_weight_theorem: Theorem
    common_trace_theorem: Theorem
    lift_boundary_theorem: Theorem
    gate_theorem: Theorem


def _gamma_matrices() -> tuple[sp.ImmutableMatrix, ...]:
    sigma_one = sp.Matrix([[0, 1], [1, 0]])
    sigma_two = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sigma_three = sp.diag(1, -1)
    zero = sp.zeros(2)
    identity = sp.eye(2)
    matrices = []
    for sigma in (sigma_one, sigma_two, sigma_three):
        matrices.append(
            sp.ImmutableMatrix(
                sp.Matrix.vstack(
                    sp.Matrix.hstack(zero, -sp.I * sigma),
                    sp.Matrix.hstack(sp.I * sigma, zero),
                )
            )
        )
    matrices.append(
        sp.ImmutableMatrix(
            sp.Matrix.vstack(
                sp.Matrix.hstack(zero, identity),
                sp.Matrix.hstack(identity, zero),
            )
        )
    )
    return tuple(matrices)


@lru_cache(maxsize=1)
def build_certificate() -> FullFieldKineticRelativeWeightCertificate:
    supermetric = supermetric_certificate()
    gamma = _gamma_matrices()
    gamma_five = sp.ImmutableMatrix(gamma[0] * gamma[1] * gamma[2] * gamma[3])

    clifford_residual = sp.diag(
        *(
            gamma[mu] * gamma[nu]
            + gamma[nu] * gamma[mu]
            - 2 * int(mu == nu) * sp.eye(4)
            for mu in range(4)
            for nu in range(4)
        )
    )
    clifford = kernel.prove_matrix_equality(
        clifford_residual,
        sp.zeros(64),
        subject="Euclidean four-dimensional Clifford relations",
    )

    scalar_vertex = -sp.I * gamma[0] * gamma_five
    scalar_coefficient = sp.simplify(sp.trace(scalar_vertex**2) / 2)
    scalar_trace = kernel.prove_expression_equality(
        scalar_coefficient,
        2,
        subject="spin trace coefficient of the scalar kinetic term",
    )

    gamma_twelve = (gamma[0] * gamma[1] - gamma[1] * gamma[0]) / 2
    curvature_endomorphism = -gamma_twelve
    two_form_norm = 2
    gauge_heat_coefficient = sp.simplify(
        sp.trace(curvature_endomorphism**2) / 2
        + sp.Rational(1, 12) * sp.trace(sp.eye(4)) * two_form_norm
    )
    gauge_coefficient = sp.simplify(gauge_heat_coefficient / two_form_norm)
    gauge_trace = kernel.prove_expression_equality(
        gauge_coefficient,
        -sp.Rational(2, 3),
        subject="spin trace coefficient multiplying anti-Hermitian curvature squared",
    )
    positive_gauge = kernel.prove_expression_equality(
        -gauge_coefficient,
        sp.Rational(2, 3),
        subject="positive Hermitian gauge kinetic coefficient",
    )
    ratio = sp.simplify(scalar_coefficient / (-gauge_coefficient))
    relative_weight = kernel.prove_expression_equality(
        ratio,
        3,
        subject="common-a4 scalar-to-gauge kinetic weight ratio",
    )
    common_trace = kernel.prove_expression_equality(
        supermetric.transfer_metric.rank() + supermetric.gauge_metric.rank(),
        42,
        subject="both kinetic blocks use the same full finite trace metric",
    )
    lift_boundary = kernel.prove_gate(
        "common_a4_dirac_lift_boundary",
        (supermetric.relative_weight_freedom_theorem,),
    )
    gate = kernel.prove_gate(
        "full_field_kinetic_relative_weight_parent_origin",
        (
            clifford,
            scalar_trace,
            gauge_trace,
            positive_gauge,
            relative_weight,
            common_trace,
            lift_boundary,
        ),
    )
    return FullFieldKineticRelativeWeightCertificate(
        gamma_matrices=gamma,
        gamma_five=gamma_five,
        scalar_coefficient=scalar_coefficient,
        gauge_coefficient=gauge_coefficient,
        scalar_to_gauge_ratio=ratio,
        clifford_theorem=clifford,
        scalar_trace_theorem=scalar_trace,
        gauge_trace_theorem=gauge_trace,
        positive_gauge_theorem=positive_gauge,
        relative_weight_theorem=relative_weight,
        common_trace_theorem=common_trace,
        lift_boundary_theorem=lift_boundary,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.scalar_coefficient)
    print(certificate.gauge_coefficient)
    print(certificate.scalar_to_gauge_ratio)