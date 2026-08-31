"""Exact trace-dual selector for the cross repeated-interaction coupling."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations

import sympy as sp

from ..kernel import Theorem, kernel
from ..lindblad import LindbladGenerator
from ..structures import Morphism, Space
from .version8_cross_covariance import build_certificate as build_cross_certificate
from .version8_gauge_twirl_kraus import cross_arrow_families, kraus_generator
from .version8_microscopic_interaction_hamiltonian import (
    build_certificate as build_microscopic_certificate,
)


SYSTEM_DIMENSION = 21
CROSS_REAL_DIMENSION = 12


@dataclass(frozen=True, slots=True)
class TraceDualCrossCouplingCertificate:
    field_metric_eigenvalue: sp.Expr
    canonical_rate_eigenvalue: sp.Expr
    interaction_coupling_eigenvalue: sp.Expr
    field_metric_theorem: Theorem
    dual_metric_theorem: Theorem
    coupling_gram_theorem: Theorem
    tangent_theorem: Theorem
    generator_scaling_theorem: Theorem
    environment_equivalence_theorem: Theorem
    polar_axis_compatibility_theorem: Theorem
    coupling_freedom_theorem: Theorem
    absolute_scale_no_go_theorem: Theorem
    conditional_selector_theorem: Theorem


def _composite_derivative(field: sp.MatrixBase) -> sp.ImmutableMatrix:
    result = sp.zeros(3, 6)
    for output, (first, second) in enumerate(combinations(range(3), 2)):
        result[output, first] = sp.Rational(1, 2) * field[1, second]
        result[output, second] = -sp.Rational(1, 2) * field[1, first]
        result[output, 3 + first] = -sp.Rational(1, 2) * field[0, second]
        result[output, 3 + second] = sp.Rational(1, 2) * field[0, first]
    return sp.ImmutableMatrix(result)


def _finite_dirac_variation(field: sp.MatrixBase) -> sp.ImmutableMatrix:
    edge = sp.ImmutableMatrix(6, 1, list(field))
    composite = _composite_derivative(field)
    operator = sp.zeros(10)
    operator[1:7, 0:1] = edge
    operator[0:1, 1:7] = edge.H
    operator[7:10, 1:7] = composite
    operator[1:7, 7:10] = composite.H
    return sp.ImmutableMatrix(operator)


def _field_basis() -> tuple[sp.ImmutableMatrix, ...]:
    basis = []
    for family in range(2):
        for color in range(3):
            for phase in (sp.Integer(1), sp.I):
                field = sp.zeros(2, 3)
                field[family, color] = phase
                basis.append(sp.ImmutableMatrix(field))
    return tuple(basis)


def _jumps() -> tuple[sp.ImmutableMatrix, ...]:
    qlyr, xldr = cross_arrow_families()
    generator = kraus_generator("trace_dual_cross_frame", qlyr + xldr)
    return tuple(jump.matrix for jump in generator.jumps)


def _matrix_unit_basis() -> tuple[sp.ImmutableMatrix, ...]:
    basis = []
    for row in range(SYSTEM_DIMENSION):
        for column in range(SYSTEM_DIMENSION):
            unit = sp.zeros(SYSTEM_DIMENSION)
            unit[row, column] = 1
            basis.append(sp.ImmutableMatrix(unit))
    return tuple(basis)


@lru_cache(maxsize=1)
def build_certificate() -> TraceDualCrossCouplingCertificate:
    field_operators = tuple(_finite_dirac_variation(item) for item in _field_basis())
    field_metric = sp.ImmutableMatrix(
        [
            [sp.simplify(sp.re(sp.trace(left * right))) for right in field_operators]
            for left in field_operators
        ]
    )
    expected_field_metric = 3 * sp.eye(CROSS_REAL_DIMENSION)
    field_metric_theorem = kernel.prove_matrix_equality(
        field_metric,
        expected_field_metric,
        subject="common finite trace metric on the full cross amplitude module",
    )

    dual_metric = sp.ImmutableMatrix(field_metric.inv())
    expected_dual_metric = sp.eye(CROSS_REAL_DIMENSION) / 3
    dual_metric_theorem = kernel.prove_matrix_equality(
        dual_metric,
        expected_dual_metric,
        subject="metric-dual cross rate tensor",
    )
    canonical_coupling = sp.eye(CROSS_REAL_DIMENSION) / sp.sqrt(3)
    coupling_gram_theorem = kernel.prove_algebraic_field_matrix_equality(
        canonical_coupling.T * canonical_coupling,
        expected_dual_metric,
        extensions=(sp.sqrt(3),),
        subject="canonical trace-dual interaction coupling Gram",
    )

    jumps = _jumps()
    gram = sp.ImmutableMatrix(
        sum((jump.H * jump for jump in jumps), sp.zeros(SYSTEM_DIMENSION))
    )
    step = sp.Symbol("h", nonnegative=True)
    scaled_jumps = tuple(-sp.I * jump / sp.sqrt(3) for jump in jumps)
    tangent_theorem = kernel.prove_kraus_family_tangent(
        sp.eye(SYSTEM_DIMENSION) - step * gram / 6,
        scaled_jumps,
        step,
        subject="trace-dual repeated-interaction tangent",
        premises=(dual_metric_theorem, coupling_gram_theorem),
    )

    qlyr, xldr = cross_arrow_families()
    base_generator = kraus_generator("unscaled_cross", qlyr + xldr)
    endpoint = Space("E_s+E_t", SYSTEM_DIMENSION)
    zero = Morphism("H_0_trace_dual", endpoint, endpoint, sp.zeros(SYSTEM_DIMENSION))
    scaled_generator = LindbladGenerator.make(
        "trace_dual_cross",
        zero,
        tuple(
            Morphism(
                f"D_trace_dual_{index}",
                endpoint,
                endpoint,
                jump / sp.sqrt(3),
            )
            for index, jump in enumerate(jumps)
        ),
        [sp.Integer(1)] * CROSS_REAL_DIMENSION,
    )
    generator_scaling_theorem = kernel.prove_linear_maps_equal_on_basis(
        _matrix_unit_basis(),
        scaled_generator.act,
        lambda observable: base_generator.act(observable) / 3,
        subject="trace-dual generator equals one third of the unit cross generator",
        premises=(scaled_generator.theorem, base_generator.theorem),
    )

    environment_equivalence_theorem = (
        kernel.prove_scaled_coupling_environment_equivalence(
            dual_metric_theorem,
            dimension=CROSS_REAL_DIMENSION,
            scale=sp.Rational(1, 3),
            subject="all scalar-Gram cross couplings differ by environment relabelling",
        )
    )
    pair_matrix = build_cross_certificate().pair_matrix
    polar_axis_compatibility_theorem = kernel.prove_matrix_equality(
        expected_dual_metric[:2, :2] * pair_matrix,
        pair_matrix / 3,
        subject="trace-dual mobility preserves the polar cross-family axes",
    )

    microscopic = build_microscopic_certificate()
    coupling_freedom_theorem = microscopic.coupling_commutant_theorem
    absolute_scale_no_go_theorem = microscopic.scale_no_go_theorem
    conditional_selector_theorem = kernel.prove_gate(
        "trace_dual_cross_coupling_selector",
        (
            field_metric_theorem,
            dual_metric_theorem,
            coupling_gram_theorem,
            tangent_theorem,
            generator_scaling_theorem,
            environment_equivalence_theorem,
            polar_axis_compatibility_theorem,
            coupling_freedom_theorem,
            absolute_scale_no_go_theorem,
        ),
    )

    return TraceDualCrossCouplingCertificate(
        field_metric_eigenvalue=sp.Integer(3),
        canonical_rate_eigenvalue=sp.Rational(1, 3),
        interaction_coupling_eigenvalue=1 / sp.sqrt(3),
        field_metric_theorem=field_metric_theorem,
        dual_metric_theorem=dual_metric_theorem,
        coupling_gram_theorem=coupling_gram_theorem,
        tangent_theorem=tangent_theorem,
        generator_scaling_theorem=generator_scaling_theorem,
        environment_equivalence_theorem=environment_equivalence_theorem,
        polar_axis_compatibility_theorem=polar_axis_compatibility_theorem,
        coupling_freedom_theorem=coupling_freedom_theorem,
        absolute_scale_no_go_theorem=absolute_scale_no_go_theorem,
        conditional_selector_theorem=conditional_selector_theorem,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.field_metric_theorem.proposition)
    print(certificate.environment_equivalence_theorem.proposition)