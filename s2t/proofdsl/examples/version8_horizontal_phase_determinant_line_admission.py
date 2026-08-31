"""Exact determinant-line admission audit for the horizontal phase."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from ..structures import Irrep, IsotypicBlock, SemisimpleRepresentation, Space, intertwiner_profile
from .version8_fixed_algebra import GROUP, _endpoint_representations, physical_incidence


@dataclass(frozen=True, slots=True)
class HorizontalPhaseDeterminantLineAdmissionCertificate:
    cofactor_vector: sp.ImmutableMatrix
    phased_cofactor_vector: sp.ImmutableMatrix
    source_determinant_charge: sp.Expr
    target_determinant_charge: sp.Expr
    relative_determinant_charge: sp.Expr
    invariant_functional_dimension: int
    cofactor_kernel_theorem: Theorem
    cofactor_norm_theorem: Theorem
    cofactor_phase_theorem: Theorem
    phase_exponent_theorem: Theorem
    source_charge_theorem: Theorem
    target_charge_theorem: Theorem
    relative_charge_theorem: Theorem
    invariant_functional_no_go_theorem: Theorem
    real_pair_modulus_theorem: Theorem
    background_contraction_theorem: Theorem
    contraction_nonuniqueness_theorem: Theorem
    determinant_line_no_go_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HorizontalPhaseDeterminantLineAdmissionCertificate:
    incidence = sp.ImmutableMatrix(physical_incidence())
    cofactor = sp.ImmutableMatrix(
        sp.Matrix(
            [
                (-1) ** column
                * incidence[:, [index for index in range(11) if index != column]].det()
                for column in range(11)
            ]
        )
    )
    cofactor_kernel = kernel.prove_matrix_equality(
        incidence * cofactor,
        sp.zeros(10, 1),
        subject="maximal-minor cofactor vector spans the incidence kernel",
    )
    cofactor_norm = kernel.prove_expression_equality(
        (cofactor.H * cofactor)[0],
        2,
        subject="squared norm of the primitive incidence cofactor vector",
    )

    z = sp.Symbol("z", nonzero=True)
    phase_matrix = sp.diag(*([z**4] * 3 + [z**3] * 7))
    phased_incidence = sp.ImmutableMatrix(phase_matrix * incidence)
    phased_cofactor = sp.ImmutableMatrix(
        sp.Matrix(
            [
                (-1) ** column
                * phased_incidence[:, [index for index in range(11) if index != column]].det()
                for column in range(11)
            ]
        )
    )
    phase_exponent = 3 * 4 + 7 * 3
    cofactor_phase = kernel.prove_matrix_equality(
        phased_cofactor,
        z**33 * cofactor,
        subject="determinant-line cofactor transforms with horizontal phase weight thirty-three",
    )
    phase_exponent_theorem = kernel.prove_expression_equality(
        phase_exponent,
        33,
        subject="horizontal determinant character exponent",
    )

    source_charge = sp.simplify(
        6 * sp.Rational(1, 6)
        + 4 * sp.Rational(-1, 2)
        - 1
    )
    target_charge = sp.simplify(
        3 * sp.Rational(2, 3)
        + 3 * sp.Rational(-1, 3)
        - 2
        + 2 * sp.Rational(-1, 2)
    )
    relative_charge = sp.simplify(target_charge - source_charge)
    source_charge_theorem = kernel.prove_expression_equality(
        source_charge,
        -2,
        subject="total hypercharge of the source determinant character",
    )
    target_charge_theorem = kernel.prove_expression_equality(
        target_charge,
        -2,
        subject="total hypercharge of the target determinant character",
    )
    relative_charge_theorem = kernel.prove_expression_equality(
        relative_charge,
        0,
        subject="cancellation of source and target determinant characters",
    )

    source_representation, _ = _endpoint_representations()
    trivial = Irrep(GROUP, "(1,1)_0", 1)
    trivial_representation = SemisimpleRepresentation(
        "trivial_scalar",
        Space("C", 1),
        (IsotypicBlock(trivial),),
    )
    functional_profile = intertwiner_profile(source_representation, trivial_representation)
    invariant_functional_no_go = kernel.prove_intertwiner_rank_no_go(
        functional_profile,
        requested_rank=1,
        subject="no gauge-invariant linear functional contracts the maximal-minor carrier",
    )

    real_pair_modulus = sp.simplify((z**-33 * cofactor.H) * (z**33 * cofactor))
    real_pair_modulus_theorem = kernel.prove_matrix_equality(
        real_pair_modulus,
        sp.Matrix([[2]]),
        subject="Real-paired determinant-line norm is blind to the horizontal phase",
    )

    first_contraction = sp.zeros(1, 11)
    first_contraction[0, 6] = -1
    second_contraction = sp.zeros(1, 11)
    second_contraction[0, 9] = 1
    background_contraction = kernel.prove_matrix_equality(
        sp.Matrix.hstack(first_contraction * cofactor, second_contraction * cofactor),
        sp.Matrix([[1, 1]]),
        subject="two distinct background contractions agree at the chosen incidence vacuum",
    )
    contraction_nonuniqueness = kernel.prove_matrix_inequality(
        first_contraction,
        second_contraction,
        subject="vacuum-normalized determinant-line contractions are not unique",
    )
    determinant_line_no_go = kernel.prove_gate(
        "horizontal_phase_determinant_line_has_no_canonical_scalar_trivialization",
        (
            cofactor_phase,
            relative_charge_theorem,
            invariant_functional_no_go,
            real_pair_modulus_theorem,
            contraction_nonuniqueness,
        ),
    )
    gate = kernel.prove_gate(
        "horizontal_phase_determinant_line_admission",
        (
            cofactor_kernel,
            cofactor_norm,
            cofactor_phase,
            phase_exponent_theorem,
            source_charge_theorem,
            target_charge_theorem,
            relative_charge_theorem,
            invariant_functional_no_go,
            real_pair_modulus_theorem,
            background_contraction,
            contraction_nonuniqueness,
            determinant_line_no_go,
        ),
    )
    return HorizontalPhaseDeterminantLineAdmissionCertificate(
        cofactor_vector=cofactor,
        phased_cofactor_vector=phased_cofactor,
        source_determinant_charge=source_charge,
        target_determinant_charge=target_charge,
        relative_determinant_charge=relative_charge,
        invariant_functional_dimension=functional_profile.hom_dimension,
        cofactor_kernel_theorem=cofactor_kernel,
        cofactor_norm_theorem=cofactor_norm,
        cofactor_phase_theorem=cofactor_phase,
        phase_exponent_theorem=phase_exponent_theorem,
        source_charge_theorem=source_charge_theorem,
        target_charge_theorem=target_charge_theorem,
        relative_charge_theorem=relative_charge_theorem,
        invariant_functional_no_go_theorem=invariant_functional_no_go,
        real_pair_modulus_theorem=real_pair_modulus_theorem,
        background_contraction_theorem=background_contraction,
        contraction_nonuniqueness_theorem=contraction_nonuniqueness,
        determinant_line_no_go_theorem=determinant_line_no_go,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.cofactor_vector.T)
    print(certificate.relative_determinant_charge)
    print(certificate.invariant_functional_dimension)