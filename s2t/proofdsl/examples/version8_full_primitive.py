"""Exact assembly certificate for the full primitive Tome VIII QMS."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from ..lindblad import LindbladGenerator
from ..structures import Morphism, Space
from .version8_fixed_algebra import build_certificate as build_fixed_certificate
from .version8_fixed_algebra import physical_incidence
from .version8_gauge_twirl_kraus import (
    _endpoint_gauge_generators,
    build_certificate as build_cross_certificate,
    cross_arrow_families,
    kraus_generator,
)


@dataclass(frozen=True, slots=True)
class FullPrimitiveCertificate:
    jump_count: int
    group_sizes: tuple[int, ...]
    gksl_theorem: Theorem
    trace_theorem: Theorem
    unital_theorem: Theorem
    endpoint_theorem: Theorem
    scalar_fixed_theorem: Theorem
    qlyr_closure_theorem: Theorem
    xldr_closure_theorem: Theorem
    positive_weight_theorem: Theorem
    gap_theorem: Theorem


def _jumps() -> tuple[sp.ImmutableMatrix, ...]:
    incidence = physical_incidence()
    linking = sp.zeros(21)
    linking[:11, 11:] = incidence.H
    linking[11:, :11] = incidence
    raw = _endpoint_gauge_generators()
    gauge = (
        tuple(sp.ImmutableMatrix(item / 2) for item in raw[:7])
        + (sp.ImmutableMatrix(raw[7] / (2 * sp.sqrt(3))),)
        + tuple(sp.ImmutableMatrix(item / 2) for item in raw[8:11])
        + (sp.ImmutableMatrix(raw[11]),)
    )
    qlyr, xldr = cross_arrow_families()
    cross = tuple(
        jump.matrix for jump in kraus_generator("full_primitive_cross", qlyr + xldr).jumps
    )
    return (sp.ImmutableMatrix(linking),) + gauge + cross


@lru_cache(maxsize=1)
def build_certificate() -> FullPrimitiveCertificate:
    endpoint = Space("E_s+E_t", 21)
    jumps = _jumps()
    morphisms = tuple(
        Morphism(f"F_{index + 1}", endpoint, endpoint, matrix)
        for index, matrix in enumerate(jumps)
    )
    zero = Morphism("H_0^full", endpoint, endpoint, sp.zeros(21))
    generator = LindbladGenerator.make(
        "full_primitive_QMS", zero, morphisms, [sp.Integer(1)] * len(morphisms)
    )
    trace = kernel.prove_generator_trace_preserving(generator)
    unital = kernel.prove_generator_unital(generator)
    endpoint_theorem = kernel.prove_block_subalgebra_invariant(
        generator, (11, 10), subject="full primitive endpoint observable algebra"
    )

    fixed = build_fixed_certificate()
    cross = build_cross_certificate()
    scalar = kernel.prove_fixed_algebra_intersection(
        fixed.fixed_theorem,
        cross.cross_kernel_theorem,
        subject="base gauge-linking C2 intersected with the full cross bridge",
    )
    qlyr_closure = kernel.prove_fixed_algebra_intersection(
        fixed.fixed_theorem,
        kernel.prove_exact_nullity(
            cross.qlyr_central_matrix, 1, subject="QLYR central restriction"
        ),
        subject="QLYR alone closes the base central C2",
    )
    xldr_closure = kernel.prove_fixed_algebra_intersection(
        fixed.fixed_theorem,
        kernel.prove_exact_nullity(
            cross.xldr_central_matrix, 1, subject="XLdR central restriction"
        ),
        subject="XLdR alone closes the base central C2",
    )
    weights = tuple(sp.Symbol(name, positive=True) for name in (
        "kappa_link", "kappa_SU3", "kappa_SU2", "kappa_U1", "kappa_QLYR", "kappa_XLdR"
    ))
    groups = (1, 8, 3, 1, 6, 6)
    positive_family = kernel.prove_positive_selfadjoint_dirichlet_family(
        generator,
        groups,
        weights,
        scalar,
        subject="all strictly positive relative-rate choices",
    )
    gap = kernel.prove_positive_gap_from_scalar_dirichlet_kernel(
        positive_family, subject="strict decay gap above the scalar fixed line"
    )
    return FullPrimitiveCertificate(
        jump_count=len(jumps),
        group_sizes=groups,
        gksl_theorem=generator.theorem,
        trace_theorem=trace,
        unital_theorem=unital,
        endpoint_theorem=endpoint_theorem,
        scalar_fixed_theorem=scalar,
        qlyr_closure_theorem=qlyr_closure,
        xldr_closure_theorem=xldr_closure,
        positive_weight_theorem=positive_family,
        gap_theorem=gap,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.jump_count, certificate.group_sizes)
    print(certificate.scalar_fixed_theorem.proposition)