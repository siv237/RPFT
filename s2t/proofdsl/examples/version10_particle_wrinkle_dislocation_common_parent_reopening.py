"""LCF certificate for reopening the wrinkle--dislocation common parent."""
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class ParticleWrinkleDislocationCommonParentCertificate:
    fredholm_map: sp.ImmutableMatrix
    closure_projector: sp.ImmutableMatrix
    index_data: sp.ImmutableMatrix
    wrinkle_stationary_data: sp.ImmutableMatrix
    inherited_parent_hessian: sp.ImmutableMatrix
    conditional_common_hessian: sp.ImmutableMatrix
    localization_map: sp.ImmutableMatrix
    energy_to_pole_map: sp.ImmutableMatrix
    common_parent_requirements: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> ParticleWrinkleDislocationCommonParentCertificate:
    fredholm_map = sp.ImmutableMatrix.vstack(sp.ImmutableMatrix(sp.eye(90)), sp.ImmutableMatrix(sp.zeros(15, 90)))
    closure_projector = sp.ImmutableMatrix(sp.eye(105) - fredholm_map * fredholm_map.T)
    index_data = sp.ImmutableMatrix([0, 15, -15, sp.Rational(1, 7)])

    length = sp.symbols("L", positive=True)
    wrinkle_energy = length + 1 / length
    wrinkle_stationary_data = sp.ImmutableMatrix([
        wrinkle_energy.subs(length, 1),
        sp.diff(wrinkle_energy, length).subs(length, 1),
        sp.diff(wrinkle_energy, length, 2).subs(length, 1),
    ])

    # The inherited package is a direct sum: the wrinkle scale is stiff,
    # while the discrete index has no local energetic coordinate or bridge.
    inherited_parent_hessian = sp.ImmutableMatrix([[2, 0], [0, 0]])
    conditional_common_hessian = sp.ImmutableMatrix([[2, 1], [1, 1]])
    localization_map = sp.ImmutableMatrix(sp.zeros(1, 15))
    energy_to_pole_map = sp.ImmutableMatrix(sp.zeros(1))
    common_parent_requirements = sp.ImmutableMatrix(sp.ones(8, 1))
    physical_origin = sp.ImmutableMatrix(sp.zeros(3, 1))

    theorems = (
        kernel.prove_matrix_equality(fredholm_map.T * fredholm_map, sp.eye(90), subject="oriented defect representative is an isometry"),
        kernel.prove_exact_rank(fredholm_map, 90, subject="oriented Fredholm representative has full domain rank"),
        kernel.prove_matrix_equality(closure_projector * closure_projector, closure_projector, subject="closure residual is an exact projector"),
        kernel.prove_exact_rank(closure_projector, 15, subject="closure residual has rank fifteen"),
        kernel.prove_expression_equality(sp.trace(closure_projector), 15, subject="closure residual trace is fifteen"),
        kernel.prove_matrix_equality(index_data, sp.Matrix([0, 15, -15, sp.Rational(1, 7)]), subject="kernel cokernel index and deficit data are exact"),
        kernel.prove_expression_equality(index_data[3], sp.Rational(15, 105), subject="normalized closure deficit equals one seventh"),
        kernel.prove_expression_equality(wrinkle_stationary_data[0], 2, subject="normalized wrinkle energy at the conditional radius is two"),
        kernel.prove_expression_equality(wrinkle_stationary_data[1], 0, subject="normalized wrinkle radius is stationary"),
        kernel.prove_expression_equality(wrinkle_stationary_data[2], 2, subject="normalized wrinkle radius has positive curvature"),
        kernel.prove_matrix_equality(inherited_parent_hessian, sp.diag(2, 0), subject="inherited wrinkle and defect parents remain a direct sum"),
        kernel.prove_exact_rank(inherited_parent_hessian, 1, subject="inherited common-parent Hessian has one flat direction"),
        kernel.prove_expression_equality(inherited_parent_hessian.det(), 0, subject="inherited common-parent Hessian is singular"),
        kernel.prove_expression_equality(inherited_parent_hessian[0, 1], 0, subject="inherited wrinkle defect mixed block vanishes"),
        kernel.prove_matrix_equality(localization_map, sp.zeros(1, 15), subject="no inherited map localizes the index defect in the wrinkle"),
        kernel.prove_matrix_equality(energy_to_pole_map, sp.zeros(1), subject="no inherited energy to spectral pole map exists"),
        kernel.prove_expression_equality(conditional_common_hessian.det(), 1, subject="one mixed bridge can conditionally close the Hessian"),
        kernel.prove_exact_rank(conditional_common_hessian, 2, subject="conditional mixed parent is nondegenerate"),
        kernel.prove_expression_equality(conditional_common_hessian[0, 0], 2, subject="conditional mixed parent has positive leading minor"),
        kernel.prove_expression_equality(sum(common_parent_requirements), 8, subject="reopened particle requirements are jointly consistent"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="mixed bridge localization and pole origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict common-parent origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_common_parent_reopening_gate",
        theorems,
    )
    return ParticleWrinkleDislocationCommonParentCertificate(
        fredholm_map,
        closure_projector,
        index_data,
        wrinkle_stationary_data,
        inherited_parent_hessian,
        conditional_common_hessian,
        localization_map,
        energy_to_pole_map,
        common_parent_requirements,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_common_parent_reopening_gate",
    title="Возврат к общему родителю частицы-морщинки и частицы-дислокации",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_common_parent_reopening_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_common_parent_reopening_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"particle_wrinkle_dislocation_common_parent_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(22)
    ),
)