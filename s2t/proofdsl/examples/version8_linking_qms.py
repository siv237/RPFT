"""Exact GKSL certificate for the Tome VIII linking QMS."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from ..lindblad import LindbladGenerator
from ..structures import Morphism, Space
from .version8_fixed_algebra import physical_incidence


@dataclass(frozen=True, slots=True)
class LinkingQMSCertificate:
    incidence_rank: int
    linking_fixed_dimension: int
    gksl_theorem: Theorem
    trace_theorem: Theorem
    unital_theorem: Theorem
    corner_invariance_theorem: Theorem
    corner_formula_theorem: Theorem
    fixed_dimension_theorem: Theorem


def _corner_basis() -> tuple[sp.ImmutableMatrix, ...]:
    basis = []
    for start, dimension in ((0, 11), (11, 10)):
        for row in range(dimension):
            for column in range(dimension):
                unit = sp.zeros(21)
                unit[start + row, start + column] = 1
                basis.append(sp.ImmutableMatrix(unit))
    return tuple(basis)


def _corner_formula(matrix: sp.MatrixBase) -> sp.ImmutableMatrix:
    incidence = physical_incidence()
    source = matrix[:11, :11]
    target = matrix[11:, 11:]
    source_gram = incidence.H * incidence
    target_gram = incidence * incidence.H
    source_image = (
        incidence.H * target * incidence
        - sp.Rational(1, 2) * (source_gram * source + source * source_gram)
    )
    target_image = (
        incidence * source * incidence.H
        - sp.Rational(1, 2) * (target_gram * target + target * target_gram)
    )
    return sp.ImmutableMatrix(sp.diag(source_image, target_image))


def _linking_commutant_system() -> sp.ImmutableMatrix:
    incidence = physical_incidence()
    forward = sp.Matrix.hstack(
        sp.kronecker_product(sp.eye(11), incidence),
        -sp.kronecker_product(incidence.T, sp.eye(10)),
    )
    backward = sp.Matrix.hstack(
        sp.kronecker_product(incidence, sp.eye(11)),
        -sp.kronecker_product(sp.eye(10), incidence.T),
    )
    return sp.ImmutableMatrix(sp.Matrix.vstack(forward, backward))


@lru_cache(maxsize=1)
def build_certificate() -> LinkingQMSCertificate:
    incidence = physical_incidence()
    endpoint = Space("E_s+E_t", 21)
    linking = sp.zeros(21)
    linking[:11, 11:] = incidence.H
    linking[11:, :11] = incidence
    linking_morphism = Morphism("D_A", endpoint, endpoint, linking)
    zero_hamiltonian = Morphism("H_0", endpoint, endpoint, sp.zeros(21))
    generator = LindbladGenerator.make(
        "linking_QMS", zero_hamiltonian, [linking_morphism], [sp.Integer(1)]
    )
    trace_theorem = kernel.prove_generator_trace_preserving(generator)
    unital_theorem = kernel.prove_generator_unital(generator)
    corner_invariance = kernel.prove_block_subalgebra_invariant(
        generator,
        (11, 10),
        subject="M_11 direct_sum M_10 endpoint algebra",
    )
    basis = _corner_basis()
    corner_formula = kernel.prove_linear_maps_equal_on_basis(
        basis,
        generator.act,
        _corner_formula,
        subject="explicit linking corner GKSL formula",
        premises=(corner_invariance,),
    )
    fixed_dimension = kernel.prove_exact_nullity(
        _linking_commutant_system(),
        41,
        subject="block-diagonal linking fixed algebra",
    )
    assert incidence.rank() == 10
    return LinkingQMSCertificate(
        incidence_rank=10,
        linking_fixed_dimension=41,
        gksl_theorem=generator.theorem,
        trace_theorem=trace_theorem,
        unital_theorem=unital_theorem,
        corner_invariance_theorem=corner_invariance,
        corner_formula_theorem=corner_formula,
        fixed_dimension_theorem=fixed_dimension,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(f"incidence rank: {certificate.incidence_rank}")
    print(f"linking fixed dimension: {certificate.linking_fixed_dimension}")
    print(certificate.gksl_theorem.proposition)