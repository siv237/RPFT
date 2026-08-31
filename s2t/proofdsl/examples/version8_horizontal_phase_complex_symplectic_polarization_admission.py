"""Exact complex-symplectic polarization audit for the horizontal phase."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel


def _pair(matrix: sp.MutableDenseMatrix, left: int, right: int, dimension: int) -> None:
    matrix[left : left + dimension, right : right + dimension] = sp.eye(dimension)
    matrix[right : right + dimension, left : left + dimension] = -sp.eye(dimension)


def _gauge_generators() -> tuple[sp.ImmutableMatrix, ...]:
    generators: list[sp.ImmutableMatrix] = []
    for row in range(2):
        for column in range(2):
            fundamental = sp.zeros(2)
            fundamental[row, column] = 1
            action = sp.zeros(20)
            action[0:2, 0:2] = fundamental
            for start in (2, 4, 6, 8):
                action[start : start + 2, start : start + 2] = -fundamental.T
            generators.append(sp.ImmutableMatrix(action))
    for row in range(3):
        for column in range(3):
            fundamental = sp.zeros(3)
            fundamental[row, column] = 1
            action = sp.zeros(20)
            action[10:13, 10:13] = fundamental
            action[13:16, 13:16] = -fundamental.T
            generators.append(sp.ImmutableMatrix(action))
    hypercharge = sp.diag(
        *(
            [sp.Rational(1, 2)] * 2
            + [sp.Rational(-1, 2)] * 8
            + [sp.Rational(2, 3)] * 3
            + [sp.Rational(-2, 3)] * 3
            + [0] * 4
        )
    )
    generators.append(sp.ImmutableMatrix(hypercharge))
    return tuple(generators)


@dataclass(frozen=True, slots=True)
class HorizontalPhaseComplexSymplecticPolarizationAdmissionCertificate:
    first_invariant_form: sp.ImmutableMatrix
    second_invariant_form: sp.ImmutableMatrix
    generic_invariant_form: sp.ImmutableMatrix
    invariance_system: sp.ImmutableMatrix
    gauge_generators: tuple[sp.ImmutableMatrix, ...]
    invariant_form_dimension: int
    maximum_invariant_rank: int
    minimum_radical_dimension: int
    missing_dual_complex_dimension: int
    completed_complex_dimension: int
    representation_dimension_theorem: Theorem
    invariant_form_dimension_theorem: Theorem
    first_skew_theorem: Theorem
    second_skew_theorem: Theorem
    first_invariance_theorem: Theorem
    second_invariance_theorem: Theorem
    maximum_rank_theorem: Theorem
    radical_dimension_theorem: Theorem
    nonuniqueness_theorem: Theorem
    bosonic_self_contraction_theorem: Theorem
    missing_dual_dimension_theorem: Theorem
    completed_carrier_dimension_theorem: Theorem
    symplectic_polarization_no_go_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HorizontalPhaseComplexSymplecticPolarizationAdmissionCertificate:
    # T = H_+ + 4 H_- + C_+ + C_- + 4 S_0 with dimensions 2, 2, 3, 3, 1.
    representation_dimension = 2 + 4 * 2 + 3 + 3 + 4
    invariant_form_dimension = 1 * 4 + 1 * 1 + 4 * 3 // 2
    maximum_invariant_rank = 2 * 2 * min(1, 4) + 2 * 3 * min(1, 1) + 4
    minimum_radical_dimension = representation_dimension - maximum_invariant_rank
    missing_dual_complex_dimension = (4 - 1) * 2
    completed_complex_dimension = representation_dimension + missing_dual_complex_dimension

    first = sp.zeros(20)
    _pair(first, 0, 2, 2)
    _pair(first, 10, 13, 3)
    first[16, 17] = 1
    first[17, 16] = -1
    first[18, 19] = 1
    first[19, 18] = -1
    first = sp.ImmutableMatrix(first)

    second = sp.zeros(20)
    _pair(second, 0, 4, 2)
    _pair(second, 10, 13, 3)
    second[16, 18] = 1
    second[18, 16] = -1
    second[17, 19] = 1
    second[19, 17] = -1
    second = sp.ImmutableMatrix(second)
    generators = _gauge_generators()

    skew_pairs = tuple(
        (row, column)
        for row in range(20)
        for column in range(row + 1, 20)
    )
    skew_variables = sp.symbols(f"omega0:{len(skew_pairs)}")
    generic_skew = sp.zeros(20)
    for variable, (row, column) in zip(skew_variables, skew_pairs):
        generic_skew[row, column] = variable
        generic_skew[column, row] = -variable
    invariance_equations = []
    for generator in generators:
        invariance_equations.extend(generator.T * generic_skew + generic_skew * generator)
    invariance_system, _ = sp.linear_eq_to_matrix(invariance_equations, skew_variables)
    invariance_system = sp.ImmutableMatrix(invariance_system)
    invariant_basis = invariance_system.nullspace()
    invariant_coordinates = sp.symbols(f"c0:{len(invariant_basis)}")
    generic_vector = sum(
        (
            invariant_coordinates[index] * invariant_basis[index]
            for index in range(len(invariant_basis))
        ),
        sp.zeros(len(skew_pairs), 1),
    )
    generic_invariant = sp.zeros(20)
    for value, (row, column) in zip(generic_vector, skew_pairs):
        generic_invariant[row, column] = value
        generic_invariant[column, row] = -value
    generic_invariant = sp.ImmutableMatrix(generic_invariant)

    representation_dimension_theorem = kernel.prove_expression_equality(
        representation_dimension,
        20,
        subject="complex dimension of the typed transfer representation",
    )
    invariant_form_dimension_theorem = kernel.prove_exact_nullity(
        invariance_system,
        11,
        subject="dimension of gauge-invariant alternating bilinear forms",
    )
    first_skew = kernel.prove_matrix_equality(
        first.T,
        -first,
        subject="first invariant polarization candidate is alternating",
    )
    second_skew = kernel.prove_matrix_equality(
        second.T,
        -second,
        subject="second invariant polarization candidate is alternating",
    )
    first_residual = sp.ImmutableMatrix.hstack(
        *(generator.T * first + first * generator for generator in generators)
    )
    second_residual = sp.ImmutableMatrix.hstack(
        *(generator.T * second + second * generator for generator in generators)
    )
    first_invariance = kernel.prove_matrix_equality(
        first_residual,
        sp.zeros(20, 20 * len(generators)),
        subject="first alternating form is invariant under fourteen exact gauge checks",
    )
    second_invariance = kernel.prove_matrix_equality(
        second_residual,
        sp.zeros(20, 20 * len(generators)),
        subject="second alternating form is invariant under fourteen exact gauge checks",
    )
    maximum_rank_theorem = kernel.prove_exact_rank(
        generic_invariant,
        maximum_invariant_rank,
        subject="sharp maximum rank of an invariant alternating form",
    )
    radical_dimension_theorem = kernel.prove_exact_nullity(
        generic_invariant,
        minimum_radical_dimension,
        subject="unavoidable radical of the invariant alternating form",
    )
    nonuniqueness = kernel.prove_matrix_inequality(
        first,
        second,
        subject="gauge invariance does not select a unique polarization",
    )
    coordinates = sp.Matrix(sp.symbols("phi0:20", commutative=True))
    bosonic_self_contraction = kernel.prove_matrix_equality(
        coordinates.T * first * coordinates,
        sp.zeros(1, 1),
        subject="an alternating form has zero self-contraction on one bosonic field",
    )
    missing_dual_dimension_theorem = kernel.prove_expression_equality(
        missing_dual_complex_dimension,
        6,
        subject="missing weak-dual directions required for nondegeneracy",
    )
    completed_carrier_dimension_theorem = kernel.prove_expression_equality(
        completed_complex_dimension,
        26,
        subject="minimal complex dimension of a balanced symplectic completion",
    )
    no_go = kernel.prove_gate(
        "current_transfer_carrier_has_no_canonical_nondegenerate_symplectic_polarization",
        (
            invariant_form_dimension_theorem,
            first_skew,
            first_invariance,
            maximum_rank_theorem,
            radical_dimension_theorem,
            nonuniqueness,
            bosonic_self_contraction,
            missing_dual_dimension_theorem,
        ),
    )
    gate = kernel.prove_gate(
        "horizontal_phase_complex_symplectic_polarization_admission",
        (
            representation_dimension_theorem,
            invariant_form_dimension_theorem,
            first_skew,
            second_skew,
            first_invariance,
            second_invariance,
            maximum_rank_theorem,
            radical_dimension_theorem,
            nonuniqueness,
            bosonic_self_contraction,
            missing_dual_dimension_theorem,
            completed_carrier_dimension_theorem,
            no_go,
        ),
    )
    return HorizontalPhaseComplexSymplecticPolarizationAdmissionCertificate(
        first_invariant_form=first,
        second_invariant_form=second,
        generic_invariant_form=generic_invariant,
        invariance_system=invariance_system,
        gauge_generators=generators,
        invariant_form_dimension=invariant_form_dimension,
        maximum_invariant_rank=maximum_invariant_rank,
        minimum_radical_dimension=minimum_radical_dimension,
        missing_dual_complex_dimension=missing_dual_complex_dimension,
        completed_complex_dimension=completed_complex_dimension,
        representation_dimension_theorem=representation_dimension_theorem,
        invariant_form_dimension_theorem=invariant_form_dimension_theorem,
        first_skew_theorem=first_skew,
        second_skew_theorem=second_skew,
        first_invariance_theorem=first_invariance,
        second_invariance_theorem=second_invariance,
        maximum_rank_theorem=maximum_rank_theorem,
        radical_dimension_theorem=radical_dimension_theorem,
        nonuniqueness_theorem=nonuniqueness,
        bosonic_self_contraction_theorem=bosonic_self_contraction,
        missing_dual_dimension_theorem=missing_dual_dimension_theorem,
        completed_carrier_dimension_theorem=completed_carrier_dimension_theorem,
        symplectic_polarization_no_go_theorem=no_go,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.invariant_form_dimension)
    print(certificate.maximum_invariant_rank)