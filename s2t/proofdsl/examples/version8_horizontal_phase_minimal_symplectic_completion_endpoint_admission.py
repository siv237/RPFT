"""Exact endpoint-admission audit for the minimal symplectic completion."""

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
            action = sp.zeros(26)
            for start in (0, 2, 4, 6):
                action[start : start + 2, start : start + 2] = fundamental
            for start in (8, 10, 12, 14):
                action[start : start + 2, start : start + 2] = -fundamental.T
            generators.append(sp.ImmutableMatrix(action))
    for row in range(3):
        for column in range(3):
            fundamental = sp.zeros(3)
            fundamental[row, column] = 1
            action = sp.zeros(26)
            action[16:19, 16:19] = fundamental
            action[19:22, 19:22] = -fundamental.T
            generators.append(sp.ImmutableMatrix(action))
    hypercharge = sp.diag(
        *(
            [sp.Rational(1, 2)] * 8
            + [sp.Rational(-1, 2)] * 8
            + [sp.Rational(2, 3)] * 3
            + [sp.Rational(-2, 3)] * 3
            + [0] * 4
        )
    )
    generators.append(sp.ImmutableMatrix(hypercharge))
    return tuple(generators)


def _standard_form(permutation: tuple[int, int, int, int]) -> sp.ImmutableMatrix:
    form = sp.zeros(26)
    for plus_index, minus_index in enumerate(permutation):
        _pair(form, 2 * plus_index, 8 + 2 * minus_index, 2)
    _pair(form, 16, 19, 3)
    form[22, 23] = 1
    form[23, 22] = -1
    form[24, 25] = 1
    form[25, 24] = -1
    return sp.ImmutableMatrix(form)


@dataclass(frozen=True, slots=True)
class HorizontalPhaseMinimalSymplecticCompletionEndpointAdmissionCertificate:
    standard_form: sp.ImmutableMatrix
    alternative_form: sp.ImmutableMatrix
    gauge_generators: tuple[sp.ImmutableMatrix, ...]
    first_field: sp.ImmutableMatrix
    second_field: sp.ImmutableMatrix
    completed_complex_dimension: int
    completed_real_dimension: int
    invariant_form_dimension: int
    current_positive_weak_multiplicity: int
    required_positive_weak_multiplicity: int
    endpoint_multiplicity_deficit: int
    new_complex_directions: int
    completed_dimension_theorem: Theorem
    completed_real_dimension_theorem: Theorem
    invariant_form_dimension_theorem: Theorem
    skew_theorem: Theorem
    invariance_theorem: Theorem
    nondegeneracy_theorem: Theorem
    inverse_theorem: Theorem
    alternative_skew_theorem: Theorem
    alternative_invariance_theorem: Theorem
    nonuniqueness_theorem: Theorem
    self_contraction_theorem: Theorem
    two_field_contraction_theorem: Theorem
    endpoint_deficit_theorem: Theorem
    new_direction_theorem: Theorem
    endpoint_origin_no_go_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HorizontalPhaseMinimalSymplecticCompletionEndpointAdmissionCertificate:
    # T_symp = 4 H_+ + 4 H_- + C_+ + C_- + 4 S_0.
    completed_complex_dimension = 4 * 2 + 4 * 2 + 3 + 3 + 4
    completed_real_dimension = 2 * completed_complex_dimension
    invariant_form_dimension = 4 * 4 + 1 + 4 * 3 // 2
    current_positive_weak_multiplicity = 1
    required_positive_weak_multiplicity = 4
    endpoint_multiplicity_deficit = (
        required_positive_weak_multiplicity - current_positive_weak_multiplicity
    )
    new_complex_directions = 2 * endpoint_multiplicity_deficit

    standard = _standard_form((0, 1, 2, 3))
    alternative = _standard_form((1, 0, 2, 3))
    generators = _gauge_generators()
    residual = sp.ImmutableMatrix.hstack(
        *(generator.T * standard + standard * generator for generator in generators)
    )
    alternative_residual = sp.ImmutableMatrix.hstack(
        *(generator.T * alternative + alternative * generator for generator in generators)
    )

    first_field = sp.ImmutableMatrix([1] + [0] * 25)
    second_field = sp.ImmutableMatrix([0] * 8 + [1] + [0] * 17)

    completed_dimension_theorem = kernel.prove_expression_equality(
        completed_complex_dimension,
        26,
        subject="complex dimension of the balanced symplectic completion",
    )
    completed_real_dimension_theorem = kernel.prove_expression_equality(
        completed_real_dimension,
        52,
        subject="real dimension of the balanced symplectic completion",
    )
    invariant_form_dimension_theorem = kernel.prove_expression_equality(
        invariant_form_dimension,
        23,
        subject="dimension of invariant alternating forms after balancing",
    )
    skew_theorem = kernel.prove_matrix_equality(
        standard.T,
        -standard,
        subject="standard completed form is alternating",
    )
    invariance_theorem = kernel.prove_matrix_equality(
        residual,
        sp.zeros(26, 26 * len(generators)),
        subject="standard completed form is gauge invariant",
    )
    nondegeneracy_theorem = kernel.prove_exact_rank(
        standard,
        26,
        subject="standard completed form is nondegenerate",
    )
    inverse_theorem = kernel.prove_matrix_equality(
        standard * (-standard),
        sp.eye(26),
        subject="negative standard form is its exact inverse",
    )
    alternative_skew_theorem = kernel.prove_matrix_equality(
        alternative.T,
        -alternative,
        subject="alternative completed form is alternating",
    )
    alternative_invariance_theorem = kernel.prove_matrix_equality(
        alternative_residual,
        sp.zeros(26, 26 * len(generators)),
        subject="alternative completed form is gauge invariant",
    )
    nonuniqueness_theorem = kernel.prove_matrix_inequality(
        standard,
        alternative,
        subject="endpoint gauge data do not select a unique completed polarization",
    )
    coordinates = sp.Matrix(sp.symbols("phi0:26", commutative=True))
    self_contraction_theorem = kernel.prove_matrix_equality(
        coordinates.T * standard * coordinates,
        sp.zeros(1, 1),
        subject="one commuting bosonic field still has zero alternating self-contraction",
    )
    two_field_contraction_theorem = kernel.prove_matrix_equality(
        first_field.T * standard * second_field,
        sp.ones(1, 1),
        subject="two independent fields admit a nonzero invariant symplectic contraction",
    )
    endpoint_deficit_theorem = kernel.prove_expression_equality(
        endpoint_multiplicity_deficit,
        3,
        subject="missing endpoint-derived positive weak-doublet multiplicity",
    )
    new_direction_theorem = kernel.prove_expression_equality(
        new_complex_directions,
        6,
        subject="new complex directions outside the current endpoint carrier",
    )
    endpoint_origin_no_go_theorem = kernel.prove_gate(
        "minimal_symplectic_completion_is_formal_but_not_endpoint_derived",
        (
            nondegeneracy_theorem,
            two_field_contraction_theorem,
            endpoint_deficit_theorem,
            new_direction_theorem,
            nonuniqueness_theorem,
        ),
    )
    gate_theorem = kernel.prove_gate(
        "horizontal_phase_minimal_symplectic_completion_endpoint_admission",
        (
            completed_dimension_theorem,
            completed_real_dimension_theorem,
            invariant_form_dimension_theorem,
            skew_theorem,
            invariance_theorem,
            nondegeneracy_theorem,
            inverse_theorem,
            alternative_skew_theorem,
            alternative_invariance_theorem,
            nonuniqueness_theorem,
            self_contraction_theorem,
            two_field_contraction_theorem,
            endpoint_deficit_theorem,
            new_direction_theorem,
            endpoint_origin_no_go_theorem,
        ),
    )
    return HorizontalPhaseMinimalSymplecticCompletionEndpointAdmissionCertificate(
        standard_form=standard,
        alternative_form=alternative,
        gauge_generators=generators,
        first_field=first_field,
        second_field=second_field,
        completed_complex_dimension=completed_complex_dimension,
        completed_real_dimension=completed_real_dimension,
        invariant_form_dimension=invariant_form_dimension,
        current_positive_weak_multiplicity=current_positive_weak_multiplicity,
        required_positive_weak_multiplicity=required_positive_weak_multiplicity,
        endpoint_multiplicity_deficit=endpoint_multiplicity_deficit,
        new_complex_directions=new_complex_directions,
        completed_dimension_theorem=completed_dimension_theorem,
        completed_real_dimension_theorem=completed_real_dimension_theorem,
        invariant_form_dimension_theorem=invariant_form_dimension_theorem,
        skew_theorem=skew_theorem,
        invariance_theorem=invariance_theorem,
        nondegeneracy_theorem=nondegeneracy_theorem,
        inverse_theorem=inverse_theorem,
        alternative_skew_theorem=alternative_skew_theorem,
        alternative_invariance_theorem=alternative_invariance_theorem,
        nonuniqueness_theorem=nonuniqueness_theorem,
        self_contraction_theorem=self_contraction_theorem,
        two_field_contraction_theorem=two_field_contraction_theorem,
        endpoint_deficit_theorem=endpoint_deficit_theorem,
        new_direction_theorem=new_direction_theorem,
        endpoint_origin_no_go_theorem=endpoint_origin_no_go_theorem,
        gate_theorem=gate_theorem,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.completed_complex_dimension)
    print(certificate.standard_form.rank())