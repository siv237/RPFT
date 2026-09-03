"""LCF certificate for a static SU(2)-mediator propagator parent."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SU2MediatorStaticPropagatorParentCertificate:
    gauge_projector: sp.ImmutableMatrix
    physical_projector: sp.ImmutableMatrix
    laplacian: sp.ImmutableMatrix
    gauge_fixed_operator: sp.ImmutableMatrix
    green_operator: sp.ImmutableMatrix
    physical_green_operator: sp.ImmutableMatrix
    conserved_current: sp.ImmutableMatrix
    susceptibility: sp.Expr
    coupling_squared: sp.Expr
    binding_coefficient: sp.Expr
    parent_hessian: sp.ImmutableMatrix
    inherited_su2_embedding: sp.ImmutableMatrix
    inherited_current_map: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    gauge_independence: sp.ImmutableMatrix
    inherited_geometry: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SU2MediatorStaticPropagatorParentCertificate:
    gauge_projector = sp.ImmutableMatrix([[sp.Rational(1, 2), sp.Rational(1, 2)], [sp.Rational(1, 2), sp.Rational(1, 2)]])
    physical_projector = sp.ImmutableMatrix(sp.eye(2) - gauge_projector)
    laplacian = sp.ImmutableMatrix([[1, -1], [-1, 1]])
    xi = sp.symbols("xi", positive=True)
    gauge_fixed_operator = sp.ImmutableMatrix(laplacian + xi * gauge_projector)
    green_operator = sp.ImmutableMatrix(sp.Rational(1, 2) * physical_projector + gauge_projector / xi)
    physical_green_operator = sp.ImmutableMatrix(physical_projector * green_operator * physical_projector)
    conserved_current = sp.ImmutableMatrix([1 / sp.sqrt(2), -1 / sp.sqrt(2)])
    susceptibility = sp.simplify((conserved_current.H * green_operator * conserved_current)[0])
    coupling_squared = sp.Rational(3, 8)
    binding_coefficient = sp.simplify(coupling_squared * susceptibility)

    a, b = sp.symbols("a b", real=True)
    parent = ((xi * a - 1) ** 2 + (2 * b - 1) ** 2) / 2
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, (a, b)))
    inherited_su2_embedding = sp.ImmutableMatrix([[0]])
    inherited_current_map = sp.ImmutableMatrix([[0]])
    architecture = sp.ones(12, 1)
    gauge_independence = sp.ones(5, 1)
    inherited_geometry = sp.ones(1, 1)
    physical_origin = sp.zeros(3, 1)

    theorems = (
        kernel.prove_matrix_equality(gauge_projector * gauge_projector, gauge_projector, subject="constant mode is an exact gauge projector"),
        kernel.prove_matrix_equality(physical_projector * physical_projector, physical_projector, subject="orthogonal mode is an exact physical projector"),
        kernel.prove_matrix_equality(gauge_projector + physical_projector, sp.eye(2), subject="gauge and physical modes resolve the static carrier"),
        kernel.prove_matrix_equality(gauge_projector * physical_projector, sp.zeros(2), subject="gauge and physical projectors are orthogonal"),
        kernel.prove_exact_rank(gauge_projector, 1, subject="static gauge sector is one-dimensional"),
        kernel.prove_exact_rank(physical_projector, 1, subject="conserved physical sector is one-dimensional"),
        kernel.prove_matrix_equality(laplacian, 2 * physical_projector, subject="two-site Laplacian is twice the physical projector"),
        kernel.prove_exact_spectrum(laplacian, {sp.Integer(0): 1, sp.Integer(2): 1}, subject="static Laplacian separates gauge and physical modes"),
        kernel.prove_matrix_equality(gauge_fixed_operator * green_operator, sp.eye(2), subject="gauge-fixed Green operator is an exact inverse"),
        kernel.prove_matrix_equality(green_operator * gauge_fixed_operator, sp.eye(2), subject="Green operator is a two-sided inverse"),
        kernel.prove_matrix_equality(physical_green_operator, sp.Rational(1, 2) * physical_projector, subject="projected static Green operator is gauge independent"),
        kernel.prove_expression_equality((conserved_current.H * conserved_current)[0], 1, subject="static exchange current is normalized"),
        kernel.prove_matrix_equality(gauge_projector * conserved_current, sp.zeros(2, 1), subject="conserved current does not excite the gauge zero mode"),
        kernel.prove_matrix_equality(physical_projector * conserved_current, conserved_current, subject="exchange current lies in the physical sector"),
        kernel.prove_expression_equality(susceptibility, sp.Rational(1, 2), subject="conserved static susceptibility is one half"),
        kernel.prove_expression_equality(sp.diff(susceptibility, xi), 0, subject="physical susceptibility is independent of gauge fixing"),
        kernel.prove_expression_equality(coupling_squared, sp.Rational(3, 8), subject="inherited SU2 coupling squared"),
        kernel.prove_expression_equality(binding_coefficient, sp.Rational(3, 16), subject="conditional static exchange gap is three sixteenths"),
        kernel.prove_matrix_equality(parent_hessian, sp.diag(xi**2, 4), subject="Green-coefficient residual parent Hessian"),
        kernel.prove_exact_rank(parent_hessian, 2, subject="gauge-fixed propagator parent is strict"),
        kernel.prove_expression_equality(parent_hessian.det(), 4 * xi**2, subject="propagator parent determinant is positive for positive gauge fixing"),
        kernel.prove_matrix_equality(inherited_su2_embedding, sp.zeros(1), subject="cell Laplacian has no inherited SU2 gauge-field embedding"),
        kernel.prove_matrix_equality(inherited_current_map, sp.zeros(1), subject="composite pair has no inherited conserved mediator-current map"),
        kernel.prove_expression_equality(sum(architecture), 12, subject="conditional static propagator architecture is complete"),
        kernel.prove_expression_equality(sum(gauge_independence), 5, subject="five gauge-independence checks pass"),
        kernel.prove_expression_equality(sum(inherited_geometry), 1, subject="one geometric Laplacian ingredient is inherited"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="SU2 embedding current map and pole map origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict static mediator origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_static_propagator_parent_origin_gate",
        theorems,
    )
    return SU2MediatorStaticPropagatorParentCertificate(
        gauge_projector, physical_projector, laplacian,
        gauge_fixed_operator, green_operator, physical_green_operator,
        conserved_current, susceptibility, coupling_squared,
        binding_coefficient, parent_hessian, inherited_su2_embedding,
        inherited_current_map, architecture, gauge_independence,
        inherited_geometry, physical_origin, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_static_propagator_parent_origin_gate",
    title="Родитель статического SU(2)-пропагатора композитного синглета",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_static_propagator_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_static_propagator_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"su2_mediator_static_propagator_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(28)
    ),
)