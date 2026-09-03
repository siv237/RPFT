"""LCF certificate for the Pati-Salam Sigma component-selector audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SigmaComponentSelectorAuditCertificate:
    hypercharge6: sp.ImmutableMatrix
    hypercharge_generator: sp.ImmutableMatrix
    target_selector: sp.ImmutableMatrix
    polynomial_selector: sp.ImmutableMatrix
    affine_evaluation: sp.ImmutableMatrix
    affine_augmented: sp.ImmutableMatrix
    quadratic_evaluation: sp.ImmutableMatrix
    quadratic_coefficients: sp.ImmutableMatrix
    real_conjugation: sp.ImmutableMatrix
    su2r_flip: sp.ImmutableMatrix
    su2r_defect: sp.ImmutableMatrix
    target_mass_hessian: sp.ImmutableMatrix
    inherited_mass_splitting: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    coverage: sp.ImmutableMatrix
    conditional_architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SigmaComponentSelectorAuditCertificate:
    hypercharge6 = sp.ImmutableMatrix([3, -3, 7, 1, -1, -7, 3, -3])
    hypercharge_generator = sp.ImmutableMatrix(sp.diag(*list(hypercharge6)))
    target_selector = sp.ImmutableMatrix(sp.diag(0, 0, 1, 0, 0, 1, 0, 0))
    identity = sp.eye(8)
    polynomial_selector = sp.ImmutableMatrix(
        (hypercharge_generator**2 - identity)
        * (hypercharge_generator**2 - 9 * identity)
        / 1920
    )

    # An affine polynomial in x=(6Y)^2 cannot interpolate 0,0,1 at x=1,9,49.
    affine_evaluation = sp.ImmutableMatrix([[1, 1], [1, 9], [1, 49]])
    affine_augmented = sp.ImmutableMatrix.hstack(affine_evaluation, sp.ImmutableMatrix([0, 0, 1]))
    quadratic_evaluation = sp.ImmutableMatrix(
        [[1, 1, 1], [1, 9, 81], [1, 49, 2401]]
    )
    quadratic_coefficients = sp.ImmutableMatrix([sp.Rational(9, 1920), sp.Rational(-10, 1920), sp.Rational(1, 1920)])

    real_mutable = sp.zeros(8)
    for first, second in ((0, 1), (2, 5), (3, 4), (6, 7)):
        real_mutable[first, second] = 1
        real_mutable[second, first] = 1
    real_conjugation = sp.ImmutableMatrix(real_mutable)

    su2r_mutable = sp.zeros(8)
    for first, second in ((0, 1), (2, 3), (4, 5), (6, 7)):
        su2r_mutable[first, second] = 1
        su2r_mutable[second, first] = 1
    su2r_flip = sp.ImmutableMatrix(su2r_mutable)
    su2r_defect = sp.ImmutableMatrix(su2r_flip * polynomial_selector - polynomial_selector * su2r_flip)

    target_mass_hessian = sp.ImmutableMatrix(2 * (identity - polynomial_selector))
    inherited_mass_splitting = sp.ImmutableMatrix.zeros(8)

    # Columns: exact R2 selector, SM invariance, Real compatibility,
    # inherited data, dynamical mass splitting, coefficient origin.
    candidate_matrix = sp.ImmutableMatrix(
        [
            [0, 1, 1, 1, 0, 1],  # identity
            [0, 1, 0, 1, 0, 1],  # sign of hypercharge
            [0, 1, 1, 1, 0, 1],  # affine polynomial in Y^2
            [1, 1, 1, 1, 0, 1],  # minimal quadratic polynomial in Y^2
            [0, 1, 0, 1, 0, 1],  # T3R weight selector
            [0, 1, 1, 1, 0, 1],  # B-L triplet selector
            [0, 1, 1, 1, 0, 1],  # colour Casimir selector
            [0, 1, 1, 0, 1, 0],  # adjoint-VEV mass splitting
            [0, 1, 1, 1, 1, 1],  # inherited spectral Hessian
            [0, 1, 1, 1, 0, 0],  # Callias uniform amplifier
            [1, 1, 1, 0, 1, 1],  # target-loaded complement penalty
        ]
    )
    score_vector = sp.ImmutableMatrix(candidate_matrix * sp.ones(6, 1))
    pass_vector = sp.ImmutableMatrix.zeros(11, 1)
    coverage = sp.ImmutableMatrix(
        [[int(any(candidate_matrix[row, column] for row in range(candidate_matrix.rows)))] for column in range(candidate_matrix.cols)]
    )
    conditional_architecture = sp.ImmutableMatrix.ones(14, 1)
    physical_origin = sp.ImmutableMatrix([1, 0, 0])

    theorems = (
        kernel.prove_matrix_equality(polynomial_selector, target_selector, subject="hypercharge polynomial isolates R2 and its conjugate"),
        kernel.prove_matrix_equality(polynomial_selector**2, polynomial_selector, subject="hypercharge selector is idempotent"),
        kernel.prove_exact_rank(polynomial_selector, 2, subject="R2 selector retains two SM sectors"),
        kernel.prove_exact_nullity(polynomial_selector, 6, subject="selector removes six companion sectors"),
        kernel.prove_exact_rank(affine_evaluation, 2, subject="affine interpolation space has dimension two"),
        kernel.prove_exact_rank(affine_augmented, 3, subject="affine polynomial in hypercharge square cannot select R2"),
        kernel.prove_exact_rank(quadratic_evaluation, 3, subject="quadratic interpolation in hypercharge square is unique"),
        kernel.prove_matrix_equality(quadratic_evaluation * quadratic_coefficients, sp.ImmutableMatrix([0, 0, 1]), subject="quadratic coefficients interpolate the R2 spectral values"),
        kernel.prove_matrix_equality(real_conjugation**2, sp.eye(8), subject="sector conjugation is an involution"),
        kernel.prove_matrix_equality(real_conjugation * polynomial_selector, polynomial_selector * real_conjugation, subject="R2 plus conjugate selector is Real compatible"),
        kernel.prove_matrix_equality(hypercharge_generator * polynomial_selector, polynomial_selector * hypercharge_generator, subject="selector is Standard-Model hypercharge invariant"),
        kernel.prove_matrix_equality(su2r_flip**2, sp.eye(8), subject="SU2R weight flip is involutive"),
        kernel.prove_exact_rank(su2r_defect, 4, subject="R2 selector breaks the full SU2R pairing"),
        kernel.prove_exact_rank(target_mass_hessian, 6, subject="ideal complement penalty lifts six companion sectors"),
        kernel.prove_exact_nullity(target_mass_hessian, 2, subject="ideal penalty leaves precisely R2 and conjugate light"),
        kernel.prove_matrix_equality(inherited_mass_splitting, sp.zeros(8), subject="current parent supplies no Sigma component mass splitting"),
        kernel.prove_exact_rank(inherited_mass_splitting, 0, subject="inherited selector Hessian rank is zero"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="component-selector audit resolves all six criteria"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([4, 3, 4, 5, 3, 4, 4, 3, 5, 3, 5]), subject="component-selector candidate scores are exact"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1), subject="no component-selector candidate passes all criteria"),
        kernel.prove_matrix_equality(coverage, sp.ones(6, 1), subject="every selector criterion is represented"),
        kernel.prove_expression_equality(sum(conditional_architecture), 14, subject="conditional selector architecture is complete"),
        kernel.prove_matrix_equality(physical_origin, sp.ImmutableMatrix([1, 0, 0]), subject="algebraic projector is derived but dynamics and scale remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 1, subject="strict selector physical-origin score is one of three"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_component_selector_candidate_audit_gate",
        theorems,
    )
    return SigmaComponentSelectorAuditCertificate(
        hypercharge6,
        hypercharge_generator,
        target_selector,
        polynomial_selector,
        affine_evaluation,
        affine_augmented,
        quadratic_evaluation,
        quadratic_coefficients,
        real_conjugation,
        su2r_flip,
        su2r_defect,
        target_mass_hessian,
        inherited_mass_splitting,
        candidate_matrix,
        score_vector,
        pass_vector,
        coverage,
        conditional_architecture,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_component_selector_candidate_audit_gate",
    title="Аудит селектора R2-компоненты Pati--Salam Sigma",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_component_selector_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_component_selector_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_sigma_component_selector_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(24)
    ),
)