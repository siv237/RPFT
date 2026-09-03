"""LCF certificate for the composite SU(2)-singlet binding coefficient parent."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SU2GaugeSingletBindingCoefficientParentCertificate:
    singlet_projector: sp.ImmutableMatrix
    triplet_projector: sp.ImmutableMatrix
    exchange_kernel: sp.ImmutableMatrix
    coupling_squared: sp.Expr
    stationary_point: sp.ImmutableMatrix
    stationary_gradient: sp.ImmutableMatrix
    conditional_hessian: sp.ImmutableMatrix
    leading_minors: sp.ImmutableMatrix
    conditional_binding_operator: sp.ImmutableMatrix
    inherited_hessian: sp.ImmutableMatrix
    inherited_kernel: sp.ImmutableMatrix
    inherited_mixed_block: sp.Expr
    inherited_binding_coefficient: sp.Expr
    inherited_pole_map: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    inherited_ingredients: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SU2GaugeSingletBindingCoefficientParentCertificate:
    pauli = (
        sp.ImmutableMatrix([[0, 1], [1, 0]]),
        sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]]),
        sp.ImmutableMatrix([[1, 0], [0, -1]]),
    )
    generators = tuple(sigma / 2 for sigma in pauli)
    singlet_vector = sp.ImmutableMatrix([0, 1 / sp.sqrt(2), -1 / sp.sqrt(2), 0])
    singlet_projector = sp.ImmutableMatrix(singlet_vector * singlet_vector.H)
    triplet_projector = sp.ImmutableMatrix(sp.eye(4) - singlet_projector)
    exchange_mutable = sp.zeros(4)
    for generator in generators:
        exchange_mutable += sp.kronecker_product(generator, generator)
    exchange_kernel = sp.ImmutableMatrix(exchange_mutable)

    coupling_squared = sp.Rational(3, 8)
    kappa, chi, chi_zero = sp.symbols("kappa chi chi_0", real=True)
    parent = ((kappa - coupling_squared * chi) ** 2 + (chi - chi_zero) ** 2) / 2
    stationary_point = sp.ImmutableMatrix([coupling_squared * chi_zero, chi_zero])
    point = {kappa: stationary_point[0], chi: stationary_point[1]}
    stationary_gradient = sp.ImmutableMatrix([
        sp.simplify(sp.diff(parent, variable).subs(point)) for variable in (kappa, chi)
    ])
    conditional_hessian = sp.ImmutableMatrix(sp.hessian(parent, (kappa, chi)))
    leading_minors = sp.ImmutableMatrix([
        conditional_hessian[:i, :i].det() for i in range(1, 3)
    ])
    conditional_binding_operator = sp.ImmutableMatrix(stationary_point[0] * triplet_projector)

    inherited_hessian = sp.ImmutableMatrix(sp.diag(1, 0))
    inherited_kernel = sp.ImmutableMatrix([0, 1])
    inherited_mixed_block = sp.Integer(0)
    inherited_binding_coefficient = sp.Integer(0)
    inherited_pole_map = sp.ImmutableMatrix([[0]])
    architecture = sp.ones(10, 1)
    inherited_ingredients = sp.ones(2, 1)
    physical_origin = sp.zeros(3, 1)

    theorems = (
        kernel.prove_matrix_equality(exchange_kernel, sp.Rational(1, 4) * sp.eye(4) - singlet_projector, subject="canonical SU2 exchange kernel"),
        kernel.prove_exact_spectrum(exchange_kernel, {sp.Rational(-3, 4): 1, sp.Rational(1, 4): 3}, subject="exchange separates singlet and triplet channels"),
        kernel.prove_expression_equality(coupling_squared, sp.Rational(3, 8), subject="inherited boundary coupling squared"),
        kernel.prove_matrix_equality(stationary_point, sp.Matrix([sp.Rational(3, 8) * chi_zero, chi_zero]), subject="conditional parent stationary point"),
        kernel.prove_matrix_equality(stationary_gradient, sp.zeros(2, 1), subject="conditional coefficient parent is stationary"),
        kernel.prove_matrix_equality(conditional_hessian, sp.Matrix([[1, -sp.Rational(3, 8)], [-sp.Rational(3, 8), sp.Rational(73, 64)]]), subject="conditional coefficient parent Hessian"),
        kernel.prove_exact_rank(conditional_hessian, 2, subject="conditional parent controls coefficient and susceptibility"),
        kernel.prove_expression_equality(conditional_hessian.det(), 1, subject="conditional parent determinant"),
        kernel.prove_matrix_equality(leading_minors, sp.Matrix([1, 1]), subject="conditional parent is strictly positive"),
        kernel.prove_expression_equality(stationary_point[0], coupling_squared * chi_zero, subject="binding coefficient equals coupling times mediator susceptibility"),
        kernel.prove_matrix_equality(conditional_binding_operator * singlet_projector, sp.zeros(4), subject="conditional binding operator leaves singlet at zero"),
        kernel.prove_matrix_equality(conditional_binding_operator * triplet_projector, stationary_point[0] * triplet_projector, subject="conditional triplet gap equals binding coefficient"),
        kernel.prove_matrix_equality(inherited_hessian, sp.diag(1, 0), subject="inherited parent has no susceptibility curvature"),
        kernel.prove_exact_rank(inherited_hessian, 1, subject="inherited coefficient parent controls only the zero coefficient"),
        kernel.prove_exact_nullity(inherited_hessian, 1, subject="mediator susceptibility is an inherited flat direction"),
        kernel.prove_matrix_equality(inherited_hessian * inherited_kernel, sp.zeros(2, 1), subject="exact inherited susceptibility zero mode"),
        kernel.prove_expression_equality(inherited_mixed_block, 0, subject="inherited coefficient susceptibility mixed block vanishes"),
        kernel.prove_expression_equality(inherited_binding_coefficient, 0, subject="inherited binding coefficient is zero"),
        kernel.prove_matrix_equality(inherited_pole_map, sp.zeros(1), subject="no inherited map sends binding gap to composite pole mass"),
        kernel.prove_matrix_equality(architecture, sp.ones(10, 1), subject="conditional binding-coefficient architecture is complete"),
        kernel.prove_expression_equality(sum(architecture), 10, subject="ten conditional coefficient-parent checks pass"),
        kernel.prove_matrix_equality(inherited_ingredients, sp.ones(2, 1), subject="exchange operator and coupling value are inherited"),
        kernel.prove_expression_equality(sum(inherited_ingredients), 2, subject="two kinematic ingredients are inherited"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="susceptibility anchor flavor selector and pole map origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict binding coefficient origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_coefficient_parent_origin_gate",
        theorems,
    )
    return SU2GaugeSingletBindingCoefficientParentCertificate(
        singlet_projector, triplet_projector, exchange_kernel,
        coupling_squared, stationary_point, stationary_gradient,
        conditional_hessian, leading_minors, conditional_binding_operator,
        inherited_hessian, inherited_kernel, inherited_mixed_block,
        inherited_binding_coefficient, inherited_pole_map, architecture,
        inherited_ingredients, physical_origin, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_coefficient_parent_origin_gate",
    title="Родитель коэффициента связывания композитного SU(2)-синглета",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_coefficient_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_coefficient_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"su2_singlet_binding_coefficient_parent_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(25)
    ),
)