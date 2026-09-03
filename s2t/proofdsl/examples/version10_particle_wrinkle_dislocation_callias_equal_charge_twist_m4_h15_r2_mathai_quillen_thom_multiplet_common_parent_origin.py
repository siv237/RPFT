"""LCF certificate for the Mathai--Quillen Thom multiplet parent audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class MathaiQuillenThomMultipletParentCertificate:
    target_generator: sp.ImmutableMatrix
    sigma_reality: sp.ImmutableMatrix
    relative_projector: sp.ImmutableMatrix
    suspension_swap: sp.ImmutableMatrix
    suspension_grading: sp.ImmutableMatrix
    oriented_edge: sp.ImmutableMatrix
    thom_differential: sp.ImmutableMatrix
    field_parity: sp.ImmutableMatrix
    field_gauge_generator: sp.ImmutableMatrix
    field_reality: sp.ImmutableMatrix
    inherited_field_injection: sp.ImmutableMatrix
    conditional_bosonic_injection: sp.ImmutableMatrix
    inherited_odd_injection: sp.ImmutableMatrix
    bosonic_hessian: sp.ImmutableMatrix
    fermionic_operator: sp.ImmutableMatrix
    bosonic_determinant: sp.Expr
    fermionic_determinant: sp.Expr
    normalized_measure_ratio: sp.Expr
    conditional_status: sp.ImmutableMatrix
    inherited_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> MathaiQuillenThomMultipletParentCertificate:
    identity = sp.eye(8)
    zero = sp.zeros(8)
    target_generator = sp.ImmutableMatrix(sp.diag(3, -3, 7, 1, -1, -7, 3, -3))

    reality = sp.zeros(8)
    for left, right in ((0, 1), (2, 5), (3, 4), (6, 7)):
        reality[left, right] = reality[right, left] = 1
    sigma_reality = sp.ImmutableMatrix(reality)

    relative_projector = sp.ImmutableMatrix(
        sp.Rational(1, 2)
        * sp.BlockMatrix([[identity, -identity], [-identity, identity]]).as_explicit()
    )
    suspension_swap = sp.ImmutableMatrix(sp.eye(16) - 2 * relative_projector)
    suspension_grading = sp.ImmutableMatrix(sp.diag(identity, -identity))
    plus = sp.Rational(1, 2) * (sp.eye(16) + suspension_grading)
    minus = sp.Rational(1, 2) * (sp.eye(16) - suspension_grading)
    oriented_edge = sp.ImmutableMatrix(minus * suspension_swap * plus)

    # Full finite-dimensional Thom quartet ordered as (Sigma, psi, chi, H).
    thom_differential = sp.ImmutableMatrix(
        sp.BlockMatrix(
            [
                [zero, zero, zero, zero],
                [identity, zero, zero, zero],
                [zero, zero, zero, zero],
                [zero, zero, identity, zero],
            ]
        ).as_explicit()
    )
    field_parity = sp.ImmutableMatrix(sp.diag(identity, -identity, -identity, identity))
    field_gauge_generator = sp.ImmutableMatrix(
        sp.diag(target_generator, target_generator, target_generator, target_generator)
    )
    field_reality = sp.ImmutableMatrix(
        sp.diag(sigma_reality, sigma_reality, sigma_reality, sigma_reality)
    )

    inherited_field_injection = sp.ImmutableMatrix(
        sp.Matrix.vstack(identity, zero, zero, zero)
    )
    conditional_bosonic_injection = sp.ImmutableMatrix(
        sp.BlockMatrix(
            [
                [identity, zero],
                [zero, zero],
                [zero, zero],
                [zero, identity],
            ]
        ).as_explicit()
    )
    inherited_odd_injection = sp.ImmutableMatrix.zeros(32, 16)

    # After the standard auxiliary contour shift, the localized bosonic
    # quadratic form is ||Q Sigma||^2 + ||H||^2.  The odd bilinear is chi Q psi.
    bosonic_hessian = sp.ImmutableMatrix(sp.diag(target_generator**2, identity))
    fermionic_operator = target_generator
    bosonic_determinant = sp.factor(bosonic_hessian.det())
    fermionic_determinant = sp.factor(fermionic_operator.det())
    normalized_measure_ratio = sp.factor(fermionic_determinant**2 / bosonic_determinant)

    # exact section, carrier differential, full quartet, odd statistics,
    # positive measure, determinant cancellation, inherited origin,
    # zero on-shell cohomology.
    conditional_status = sp.ImmutableMatrix([1, 1, 1, 1, 1, 1, 0, 1])
    inherited_status = sp.ImmutableMatrix([1, 1, 0, 0, 1, 0, 0, 0])

    expected_oriented = sp.BlockMatrix([[zero, zero], [identity, zero]]).as_explicit()
    theorems = (
        kernel.prove_matrix_equality(relative_projector**2, relative_projector, subject="relative Hodge operator is a projector"),
        kernel.prove_matrix_equality(suspension_swap, sp.eye(16) - 2 * relative_projector, subject="suspension swap is derived from the Hodge projector"),
        kernel.prove_matrix_equality(suspension_swap**2, sp.eye(16), subject="derived suspension swap is involutive"),
        kernel.prove_matrix_equality(oriented_edge, expected_oriented, subject="oriented suspension edge equals the Thom pair differential"),
        kernel.prove_matrix_equality(oriented_edge**2, sp.zeros(16), subject="oriented carrier edge is nilpotent"),
        kernel.prove_exact_rank(oriented_edge, 8, subject="oriented carrier edge has full Thom-pair rank"),
        kernel.prove_matrix_equality(thom_differential**2, sp.zeros(32), subject="full Thom quartet differential is nilpotent"),
        kernel.prove_exact_rank(thom_differential, 16, subject="full Thom quartet is exact"),
        kernel.prove_matrix_equality(field_parity * thom_differential + thom_differential * field_parity, sp.zeros(32), subject="Thom differential is field-parity odd"),
        kernel.prove_matrix_equality(field_gauge_generator * thom_differential - thom_differential * field_gauge_generator, sp.zeros(32), subject="Thom differential is gauge equivariant"),
        kernel.prove_matrix_equality(field_reality * thom_differential - thom_differential * field_reality, sp.zeros(32), subject="Thom differential is Real equivariant"),
        kernel.prove_exact_rank(inherited_field_injection, 8, subject="current parent supplies only physical Sigma"),
        kernel.prove_exact_rank(conditional_bosonic_injection, 16, subject="conditional parent supplies both bosonic coordinates"),
        kernel.prove_exact_rank(inherited_odd_injection, 0, subject="current parent supplies no Thom odd fields"),
        kernel.prove_exact_rank(target_generator, 8, subject="Thom section Q Sigma has full rank"),
        kernel.prove_exact_rank(bosonic_hessian, 16, subject="localized bosonic quadratic form is nondegenerate"),
        kernel.prove_diagonal_signature(bosonic_hessian, (0, 0, 16), subject="localized bosonic measure is positive"),
        kernel.prove_expression_equality(fermionic_determinant, 3969, subject="Thom odd determinant is exact"),
        kernel.prove_expression_equality(bosonic_determinant, fermionic_determinant**2, subject="bosonic determinant is the square of the odd determinant"),
        kernel.prove_expression_equality(normalized_measure_ratio, 1, subject="normalized Thom determinant ratio cancels exactly"),
        kernel.prove_expression_equality(32 - conditional_bosonic_injection.rank(), 16, subject="conditional bosonic completion still lacks sixteen odd directions"),
        kernel.prove_expression_equality(sum(conditional_status), 7, subject="full conditional Thom quartet closes seven of eight criteria"),
        kernel.prove_expression_equality(sum(inherited_status), 3, subject="current parent closes only three of eight Thom criteria"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_thom_multiplet_common_parent_origin_gate",
        theorems,
    )
    return MathaiQuillenThomMultipletParentCertificate(
        target_generator,
        sigma_reality,
        relative_projector,
        suspension_swap,
        suspension_grading,
        oriented_edge,
        thom_differential,
        field_parity,
        field_gauge_generator,
        field_reality,
        inherited_field_injection,
        conditional_bosonic_injection,
        inherited_odd_injection,
        bosonic_hessian,
        fermionic_operator,
        bosonic_determinant,
        fermionic_determinant,
        normalized_measure_ratio,
        conditional_status,
        inherited_status,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_thom_multiplet_common_parent_origin_gate",
    title="Общий parent Mathai--Quillen Thom-мультиплета",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_thom_multiplet_common_parent_origin_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_thom_multiplet_common_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(
            f"h15_r2_mathai_quillen_thom_multiplet_parent_{index:02d}",
            lambda index=index: build_certificate().theorems[index],
        )
        for index in range(23)
    ),
)