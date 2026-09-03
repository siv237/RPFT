"""LCF certificate for suspension versus Mathai--Quillen auxiliary origin."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SuperconnectionSuspensionAuxiliaryCopyCertificate:
    target_generator: sp.ImmutableMatrix
    sigma_reality: sp.ImmutableMatrix
    suspension_grading: sp.ImmutableMatrix
    suspension_edge: sp.ImmutableMatrix
    doubled_generator: sp.ImmutableMatrix
    doubled_reality: sp.ImmutableMatrix
    bare_dynamical_injection: sp.ImmutableMatrix
    thom_differential: sp.ImmutableMatrix
    thom_grading: sp.ImmutableMatrix
    thom_boson_injection: sp.ImmutableMatrix
    relative_projector: sp.ImmutableMatrix
    relative_boson_image: sp.ImmutableMatrix
    section_operator: sp.ImmutableMatrix
    gaussian_hessian: sp.ImmutableMatrix
    effective_hessian: sp.ImmutableMatrix
    fermionic_jacobian: sp.Expr
    bare_status: sp.ImmutableMatrix
    thom_status: sp.ImmutableMatrix
    physical_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SuperconnectionSuspensionAuxiliaryCopyCertificate:
    identity = sp.eye(8)
    zero = sp.zeros(8)
    weights = [3, -3, 7, 1, -1, -7, 3, -3]
    target_generator = sp.ImmutableMatrix(sp.diag(*weights))

    reality = sp.zeros(8)
    for left, right in ((0, 1), (2, 5), (3, 4), (6, 7)):
        reality[left, right] = reality[right, left] = 1
    sigma_reality = sp.ImmutableMatrix(reality)

    suspension_grading = sp.ImmutableMatrix(sp.diag(identity, -identity))
    suspension_edge = sp.ImmutableMatrix(
        sp.BlockMatrix([[zero, identity], [identity, zero]]).as_explicit()
    )
    doubled_generator = sp.ImmutableMatrix(sp.diag(target_generator, target_generator))
    doubled_reality = sp.ImmutableMatrix(sp.diag(sigma_reality, sigma_reality))

    # A graded suspension supplies a second summand, but the current parent
    # contains no independent field map into it.
    bare_dynamical_injection = sp.ImmutableMatrix.zeros(16, 8)

    # Total differential of the contractible Thom pair chi -> H -> 0.
    thom_differential = sp.ImmutableMatrix(
        sp.BlockMatrix([[zero, zero], [identity, zero]]).as_explicit()
    )
    thom_grading = suspension_grading
    thom_boson_injection = sp.ImmutableMatrix(sp.Matrix.vstack(zero, identity))
    relative_projector = sp.ImmutableMatrix(
        sp.Rational(1, 2)
        * sp.BlockMatrix([[identity, -identity], [-identity, identity]]).as_explicit()
    )
    relative_boson_image = sp.ImmutableMatrix(relative_projector * thom_boson_injection)

    section_operator = target_generator
    gaussian_hessian = sp.ImmutableMatrix(
        sp.BlockMatrix([[identity, target_generator], [target_generator, 49 * identity]]).as_explicit()
    )
    effective_hessian = sp.ImmutableMatrix(49 * identity - target_generator**2)
    fermionic_jacobian = sp.factor(target_generator.det())

    # Criteria: exact type, independent boson, nilpotent pair, positive metric,
    # exact section, inherited origin, no new on-shell boson.
    bare_status = sp.ImmutableMatrix([1, 0, 0, 1, 0, 0, 1])
    thom_status = sp.ImmutableMatrix([1, 1, 1, 1, 1, 0, 1])
    physical_status = thom_status

    theorems = (
        kernel.prove_matrix_equality(sigma_reality**2, identity, subject="Sigma reality squares to one"),
        kernel.prove_matrix_equality(sigma_reality * target_generator * sigma_reality, -target_generator, subject="reality reverses the hypercharge generator"),
        kernel.prove_matrix_equality(suspension_grading**2, sp.eye(16), subject="suspension grading squares to one"),
        kernel.prove_matrix_equality(suspension_edge**2, sp.eye(16), subject="suspension edge is an involution"),
        kernel.prove_matrix_equality(suspension_grading * suspension_edge + suspension_edge * suspension_grading, sp.zeros(16), subject="suspension edge is grading odd"),
        kernel.prove_matrix_equality(doubled_generator * suspension_edge - suspension_edge * doubled_generator, sp.zeros(16), subject="suspension edge is gauge equivariant"),
        kernel.prove_matrix_equality(doubled_reality * suspension_edge - suspension_edge * doubled_reality, sp.zeros(16), subject="suspension edge is Real equivariant"),
        kernel.prove_exact_rank(bare_dynamical_injection, 0, subject="bare suspension supplies no independent dynamical field"),
        kernel.prove_matrix_equality(thom_differential**2, sp.zeros(16), subject="Thom pair differential is nilpotent"),
        kernel.prove_exact_rank(thom_differential, 8, subject="Thom pair is an exact eight-dimensional contractible pair"),
        kernel.prove_matrix_equality(thom_grading * thom_differential + thom_differential * thom_grading, sp.zeros(16), subject="Thom differential is grading odd"),
        kernel.prove_matrix_equality(doubled_generator * thom_differential - thom_differential * doubled_generator, sp.zeros(16), subject="Thom differential is gauge equivariant"),
        kernel.prove_matrix_equality(doubled_reality * thom_differential - thom_differential * doubled_reality, sp.zeros(16), subject="Thom differential is Real equivariant"),
        kernel.prove_diagonal_signature(identity, (0, 0, 8), subject="Thom boson bundle metric is positive definite"),
        kernel.prove_exact_rank(thom_boson_injection, 8, subject="Thom boson is an independent full-rank copy"),
        kernel.prove_exact_rank(relative_boson_image, 8, subject="Thom boson excites all relative Hodge modes"),
        kernel.prove_exact_rank(section_operator, 8, subject="the section s_Q equals the full-rank target generator"),
        kernel.prove_exact_rank(gaussian_hessian, 14, subject="joint Thom Gaussian Hessian has two protected zero modes"),
        kernel.prove_diagonal_signature(effective_hessian, (0, 2, 6), subject="Schur complement is positive semidefinite with two target zero modes"),
        kernel.prove_expression_equality(fermionic_jacobian, 3969, subject="linear Thom section has exact constant Jacobian"),
        kernel.prove_expression_equality(sum(bare_status), 3, subject="bare suspension closes only three of seven origin criteria"),
        kernel.prove_expression_equality(sum(thom_status), 6, subject="conditional Mathai Quillen completion closes six of seven criteria"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_suspension_auxiliary_copy_parent_origin_gate",
        theorems,
    )
    return SuperconnectionSuspensionAuxiliaryCopyCertificate(
        target_generator,
        sigma_reality,
        suspension_grading,
        suspension_edge,
        doubled_generator,
        doubled_reality,
        bare_dynamical_injection,
        thom_differential,
        thom_grading,
        thom_boson_injection,
        relative_projector,
        relative_boson_image,
        section_operator,
        gaussian_hessian,
        effective_hessian,
        fermionic_jacobian,
        bare_status,
        thom_status,
        physical_status,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_suspension_auxiliary_copy_parent_origin_gate",
    title="Родитель suspension auxiliary copy и Mathai--Quillen достройка",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_suspension_auxiliary_copy_parent_origin_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_suspension_auxiliary_copy_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(
            f"h15_r2_superconnection_suspension_auxiliary_copy_{index:02d}",
            lambda index=index: build_certificate().theorems[index],
        )
        for index in range(22)
    ),
)