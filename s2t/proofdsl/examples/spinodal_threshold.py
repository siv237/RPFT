"""Exact proof of the first formalization-candidate spinodal threshold."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SpinodalCertificate:
    curvature: sp.Expr
    threshold: sp.Expr
    curvature_theorem: Theorem
    threshold_theorem: Theorem


def build_certificate() -> SpinodalCertificate:
    a, beta = sp.symbols("a beta", positive=True)
    q2 = (3 * a**2 - 2 * a + 1) / 2
    q3 = (3 * a**3 + 3 * a**2 - 3 * a + 1) / 4
    entropy = a * sp.log(a) + (1 - a) * sp.log((1 - a) / 2)
    energy = sp.Rational(2, 7) * (1 - q2**2 / q3) + 1 - q2
    free_energy = entropy + beta * energy
    curvature = sp.simplify(
        sp.diff(free_energy, a, 2).subs(a, sp.Rational(1, 3))
    )
    expected = sp.Rational(9, 2) - sp.Rational(3, 7) * beta
    curvature_theorem = kernel.prove_expression_equality(
        curvature,
        expected,
        subject="spinodal curvature at a=1/3",
    )
    threshold = sp.Rational(21, 2)
    threshold_theorem = kernel.prove_unique_linear_zero(
        expected,
        beta,
        threshold,
        subject="unique spinodal threshold",
        premises=(curvature_theorem,),
    )
    return SpinodalCertificate(
        curvature,
        threshold,
        curvature_theorem,
        threshold_theorem,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(f"curvature: {certificate.curvature}")
    print(f"threshold: {certificate.threshold}")