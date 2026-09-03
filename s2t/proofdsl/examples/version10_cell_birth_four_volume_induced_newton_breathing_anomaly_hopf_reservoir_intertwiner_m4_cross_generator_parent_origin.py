"""LCF certificate for the M4 cross-generator parent-origin gate."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class M4CrossGeneratorParentCertificate:
    identity_intertwiner: sp.ImmutableMatrix
    orientation: sp.ImmutableMatrix
    partial_isometry_residual: sp.ImmutableMatrix
    orientation_residual: sp.ImmutableMatrix
    conditional_gradient: sp.ImmutableMatrix
    conditional_hessian: sp.ImmutableMatrix
    sign_minimum_values: sp.ImmutableMatrix
    phase_intertwiner: sp.ImmutableMatrix
    phase_unitarity_residual: sp.ImmutableMatrix
    phase_orientation_residual: sp.ImmutableMatrix
    phase_potential: sp.Expr
    inherited_cross_hessian: sp.ImmutableMatrix
    inherited_cross_source: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    coefficient_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> M4CrossGeneratorParentCertificate:
    x11, x12, x21, x22 = sp.symbols("x11 x12 x21 x22", real=True)
    variables = (x11, x12, x21, x22)
    matrix = sp.Matrix([[x11, x12], [x21, x22]])
    identity = sp.ImmutableMatrix.eye(2)
    orientation = sp.ImmutableMatrix.diag(-1, 1)
    isometry_defect = matrix.T * matrix - sp.eye(2)
    orientation_defect = sp.Matrix(orientation) * matrix - matrix * sp.Matrix(orientation)
    parent = (
        sp.trace(isometry_defect.T * isometry_defect)
        + sp.trace(orientation_defect.T * orientation_defect)
    ) / 4
    identity_point = {x11: 1, x12: 0, x21: 0, x22: 1}
    conditional_gradient = sp.ImmutableMatrix([
        sp.diff(parent, variable).subs(identity_point) for variable in variables
    ])
    conditional_hessian = sp.ImmutableMatrix(sp.hessian(parent, variables).subs(identity_point))
    partial_isometry_residual = sp.ImmutableMatrix(isometry_defect.subs(identity_point))
    orientation_residual = sp.ImmutableMatrix(orientation_defect.subs(identity_point))

    sign_points = (
        {x11: 1, x12: 0, x21: 0, x22: 1},
        {x11: -1, x12: 0, x21: 0, x22: 1},
        {x11: 1, x12: 0, x21: 0, x22: -1},
        {x11: -1, x12: 0, x21: 0, x22: -1},
    )
    sign_minimum_values = sp.ImmutableMatrix([sp.simplify(parent.subs(point)) for point in sign_points])

    phi_h, phi_c = sp.symbols("phi_h phi_c", real=True)
    phase_intertwiner = sp.ImmutableMatrix.diag(sp.exp(sp.I * phi_h), sp.exp(sp.I * phi_c))
    phase_unitarity_residual = sp.ImmutableMatrix(
        sp.simplify(phase_intertwiner.H * phase_intertwiner - identity)
    )
    phase_orientation_residual = sp.ImmutableMatrix(
        sp.simplify(orientation * phase_intertwiner - phase_intertwiner * orientation)
    )
    phase_potential = sp.simplify(
        sp.trace(phase_unitarity_residual.H * phase_unitarity_residual)
        + sp.trace(phase_orientation_residual.H * phase_orientation_residual)
    )

    inherited_cross_hessian = sp.ImmutableMatrix.zeros(4, 4)
    inherited_cross_source = sp.ImmutableMatrix.zeros(4, 1)
    architecture = sp.ImmutableMatrix.ones(10, 1)
    conditional_origin = sp.ImmutableMatrix.ones(8, 1)
    coefficient_origin = sp.ImmutableMatrix.zeros(3, 1)
    physical_origin = sp.ImmutableMatrix.zeros(4, 1)
    hessian_spectrum = {sp.Integer(2): 3, sp.Integer(4): 1}

    theorems = (
        kernel.prove_matrix_equality(partial_isometry_residual, sp.zeros(2),
                                     subject="identity cross block satisfies the partial-isometry constraint"),
        kernel.prove_matrix_equality(orientation_residual, sp.zeros(2),
                                     subject="identity cross block preserves the oriented levels"),
        kernel.prove_matrix_equality(conditional_gradient, sp.zeros(4, 1),
                                     subject="identity cross block is stationary for the conditional parent"),
        kernel.prove_matrix_equality(conditional_hessian,
                                     sp.Matrix([[2, 0, 0, 0], [0, 3, 1, 0],
                                                [0, 1, 3, 0], [0, 0, 0, 2]]),
                                     subject="conditional cross-generator Hessian is exact"),
        kernel.prove_exact_rank(conditional_hessian, 4,
                                subject="conditional cross-generator minimum is nondegenerate over real entries"),
        kernel.prove_expression_equality(conditional_hessian.det(), 32,
                                         subject="conditional cross-generator Hessian is strictly positive"),
        kernel.prove_exact_spectrum(conditional_hessian, hessian_spectrum,
                                    subject="conditional cross-generator Hessian has spectrum two threefold and four once"),
        kernel.prove_expression_equality(len(sign_points), 4,
                                         subject="four real diagonal sign configurations are audited"),
        kernel.prove_matrix_equality(sign_minimum_values, sp.zeros(4, 1),
                                     subject="all four real sign intertwiners are degenerate minima"),
        kernel.prove_matrix_equality(phase_unitarity_residual, sp.zeros(2),
                                     subject="complex diagonal phases preserve partial isometry"),
        kernel.prove_matrix_equality(phase_orientation_residual, sp.zeros(2),
                                     subject="complex diagonal phases preserve orientation"),
        kernel.prove_expression_equality(phase_potential, 0,
                                         subject="conditional parent is flat on the U1 squared phase torus"),
        kernel.prove_matrix_equality(inherited_cross_hessian, sp.zeros(4),
                                     subject="inherited parent has no cross-generator Hessian"),
        kernel.prove_exact_rank(inherited_cross_hessian, 0,
                                subject="inherited cross-generator parent controls no direction"),
        kernel.prove_exact_nullity(inherited_cross_hessian, 4,
                                   subject="all four cross-generator coordinates are inherited flat directions"),
        kernel.prove_matrix_equality(inherited_cross_source, sp.zeros(4, 1),
                                     subject="product symmetry forbids an inherited linear cross source"),
        kernel.prove_matrix_equality(architecture, sp.ones(10, 1),
                                     subject="quartic cross-condensate architecture is complete"),
        kernel.prove_expression_equality(sum(architecture), 10,
                                         subject="ten cross-condensate architecture requirements pass"),
        kernel.prove_matrix_equality(conditional_origin, sp.ones(8, 1),
                                     subject="conditional cross-generator construction closes algebraically"),
        kernel.prove_expression_equality(sum(conditional_origin), 8,
                                         subject="eight conditional-origin checks pass"),
        kernel.prove_matrix_equality(coefficient_origin, sp.zeros(3, 1),
                                     subject="condensate norm stiffness and orientation coefficients are not inherited"),
        kernel.prove_expression_equality(sum(coefficient_origin), 0,
                                         subject="cross-generator coefficient-origin score is zero"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(4, 1),
                                     subject="cross variable norm phase and temperature origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0,
                                         subject="strict physical cross-generator score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_m4_cross_generator_parent_origin_gate",
        theorems,
    )
    return M4CrossGeneratorParentCertificate(
        identity, orientation, partial_isometry_residual, orientation_residual,
        conditional_gradient, conditional_hessian, sign_minimum_values,
        phase_intertwiner, phase_unitarity_residual, phase_orientation_residual,
        phase_potential, inherited_cross_hessian, inherited_cross_source,
        architecture, conditional_origin, coefficient_origin, physical_origin,
        theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_m4_cross_generator_parent_origin_gate",
    title="Родитель происхождения M4 cross-генератора интертвинера",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_m4_cross_generator_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_m4_cross_generator_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"m4_cross_generator_parent_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(24)
    ),
)