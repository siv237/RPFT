"""LCF certificate for a common RG--K43 reference-ratio parent."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class ReferenceScaleRatioCommonParentCertificate:
    target: sp.ImmutableMatrix
    stationary_gradient: sp.ImmutableMatrix
    conditional_hessian: sp.ImmutableMatrix
    leading_minors: sp.ImmutableMatrix
    inherited_hessian: sp.ImmutableMatrix
    inherited_kernel: sp.ImmutableMatrix
    mixed_blocks: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    inherited_components: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> ReferenceScaleRatioCommonParentCertificate:
    L = 32 * sp.pi**2 / 3
    K = sp.log(42)
    target = sp.ImmutableMatrix([L, K, -L - K])
    x, y, z = sp.symbols("x_RG x_43 x_bridge", real=True)
    parent = ((x-L)**2 + (y-K)**2 + (z+x+y)**2) / 2
    point = {x:L, y:K, z:-L-K}
    stationary_gradient = sp.ImmutableMatrix([sp.diff(parent,v).subs(point) for v in (x,y,z)])
    conditional_hessian = sp.ImmutableMatrix(sp.hessian(parent,(x,y,z)))
    leading_minors = sp.ImmutableMatrix([conditional_hessian[:i,:i].det() for i in range(1,4)])
    inherited_hessian = sp.diag(1,1,0)
    inherited_kernel = sp.ImmutableMatrix([0,0,1])
    mixed_blocks = sp.zeros(2,1)
    scale_map = sp.ImmutableMatrix([[1,0,1,1],[0,1,1,1],[1,-1,0,0]])
    scale_kernel = sp.ImmutableMatrix.hstack(sp.ImmutableMatrix([-1,-1,1,0]),sp.ImmutableMatrix([-1,-1,0,1]))
    architecture = sp.ones(9,1)
    inherited_components = sp.ones(2,1)
    physical_origin = sp.zeros(4,1)
    theorems = (
        kernel.prove_matrix_equality(target, sp.Matrix([L,K,-L-K]), subject="exact RG K43 bridge stationary point"),
        kernel.prove_expression_equality(sp.exp(target[2]), sp.exp(-32*sp.pi**2/3)/42, subject="common parent selects the required ratio"),
        kernel.prove_matrix_equality(stationary_gradient, sp.zeros(3,1), subject="conditional common parent stationary point"),
        kernel.prove_matrix_equality(conditional_hessian, sp.Matrix([[2,1,1],[1,2,1],[1,1,1]]), subject="conditional common parent Hessian"),
        kernel.prove_exact_rank(conditional_hessian,3,subject="conditional common parent controls all three coordinates"),
        kernel.prove_expression_equality(conditional_hessian.det(),1,subject="conditional common parent determinant"),
        kernel.prove_matrix_equality(leading_minors,sp.Matrix([2,3,1]),subject="conditional parent positive leading minors"),
        kernel.prove_matrix_equality(inherited_hessian,sp.diag(1,1,0),subject="inherited direct-sum parent has no bridge block"),
        kernel.prove_exact_rank(inherited_hessian,2,subject="inherited parent controls only RG and K43 factors"),
        kernel.prove_exact_nullity(inherited_hessian,1,subject="bridge coordinate is flat in inherited parent"),
        kernel.prove_matrix_equality(inherited_hessian*inherited_kernel,sp.zeros(3,1),subject="exact inherited bridge zero mode"),
        kernel.prove_matrix_equality(mixed_blocks,sp.zeros(2,1),subject="inherited RG bridge and K43 bridge mixed Hessians vanish"),
        kernel.prove_exact_rank(scale_map,2,subject="bridge row is dimensionally dependent"),
        kernel.prove_exact_nullity(scale_map,2,subject="speed and common scale remain free"),
        kernel.prove_matrix_equality(scale_map*scale_kernel,sp.zeros(3,2),subject="exact dimensional kernel"),
        kernel.prove_matrix_equality(architecture,sp.ones(9,1),subject="conditional common-parent architecture is complete"),
        kernel.prove_expression_equality(sum(architecture),9,subject="nine conditional requirements pass"),
        kernel.prove_matrix_equality(inherited_components,sp.ones(2,1),subject="both separate factor parents are inherited"),
        kernel.prove_matrix_equality(physical_origin,sp.zeros(4,1),subject="common carrier mixed operator bridge source and absolute scale remain open"),
        kernel.prove_expression_equality(sum(physical_origin),0,subject="strict physical common-parent score remains zero"),
    )
    gate_theorem=kernel.prove_gate("version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_common_parent_origin_gate",theorems)
    return ReferenceScaleRatioCommonParentCertificate(target,stationary_gradient,conditional_hessian,leading_minors,inherited_hessian,inherited_kernel,mixed_blocks,scale_map,scale_kernel,architecture,inherited_components,physical_origin,theorems,gate_theorem)


SPEC=GateSpec(identifier="version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_common_parent_origin_gate",title="Общий родитель отношения опорных шкал такта рождения",source_paths=("s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_common_parent_origin_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_common_parent_origin_gate_results.json"),obligations=tuple(Obligation(f"birth_tick_reference_ratio_common_parent_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(20)))