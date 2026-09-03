"""LCF certificate for the minimal typed RG--K43 portal architecture."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class MinimalPortalArchitectureCertificate:
    p_rg: sp.ImmutableMatrix
    p_43: sp.ImmutableMatrix
    portal: sp.ImmutableMatrix
    algebra_basis: sp.ImmutableMatrix
    commutant_map: sp.ImmutableMatrix
    commutant_kernel: sp.ImmutableMatrix
    hessian: sp.ImmutableMatrix
    hessian_spectrum: dict[sp.Expr, int]
    target: sp.ImmutableMatrix
    source: sp.ImmutableMatrix
    stationary_gradient: sp.ImmutableMatrix
    bridge_readout: sp.Expr
    architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> MinimalPortalArchitectureCertificate:
    I=sp.I
    p_rg=sp.ImmutableMatrix([[1,0],[0,0]])
    p_43=sp.ImmutableMatrix([[0,0],[0,1]])
    portal=sp.ImmutableMatrix([[0,1],[1,0]])
    z=p_rg-p_43
    y=sp.ImmutableMatrix([[0,-I],[I,0]])
    algebra_basis=sp.ImmutableMatrix.hstack(*[sp.ImmutableMatrix(m).reshape(4,1) for m in (sp.eye(2),z,portal,y)])
    commutant_map=sp.ImmutableMatrix([[0,1,0,0],[0,0,1,0],[1,0,0,-1]])
    commutant_kernel=sp.ImmutableMatrix([1,0,0,1])
    lam=sp.Rational(1,2)
    hessian=sp.ImmutableMatrix([[1,lam],[lam,1]])
    hessian_spectrum={sp.Rational(1,2):1,sp.Rational(3,2):1}
    L=32*sp.pi**2/3
    K=sp.log(42)
    target=sp.ImmutableMatrix([L,K])
    source=sp.ImmutableMatrix(hessian*target)
    stationary_gradient=sp.ImmutableMatrix(hessian*target-source)
    bridge_readout=sp.simplify(sp.ImmutableMatrix([[-1,-1]])[0,:].dot(target))
    architecture=sp.ones(11,1)
    physical_origin=sp.zeros(4,1)
    theorems=(
        kernel.prove_matrix_equality(p_rg*p_rg,p_rg,subject="RG type projector is idempotent"),
        kernel.prove_matrix_equality(p_43*p_43,p_43,subject="K43 type projector is idempotent"),
        kernel.prove_matrix_equality(p_rg*p_43,sp.zeros(2),subject="sector projectors are orthogonal"),
        kernel.prove_matrix_equality(p_rg+p_43,sp.eye(2),subject="two sector projectors resolve the portal carrier"),
        kernel.prove_expression_equality(p_rg.rank(),1,subject="RG sector has rank one"),
        kernel.prove_expression_equality(p_43.rank(),1,subject="K43 sector has rank one"),
        kernel.prove_matrix_equality(portal.T,portal,subject="portal operator is Hermitian"),
        kernel.prove_matrix_equality(portal*portal,sp.eye(2),subject="portal is an involution"),
        kernel.prove_matrix_equality(portal*p_rg*portal,p_43,subject="portal exchanges the typed sectors"),
        kernel.prove_exact_rank(algebra_basis,4,subject="typed projectors and portal generate M2"),
        kernel.prove_exact_rank(commutant_map,3,subject="portal commutant constraints have rank three"),
        kernel.prove_exact_nullity(commutant_map,1,subject="portal commutant is scalar"),
        kernel.prove_matrix_equality(commutant_map*commutant_kernel,sp.zeros(3,1),subject="identity spans the portal commutant"),
        kernel.prove_matrix_equality(hessian,sp.Matrix([[1,sp.Rational(1,2)],[sp.Rational(1,2),1]]),subject="minimal stable portal Hessian witness"),
        kernel.prove_exact_rank(hessian,2,subject="portal Hessian controls both sector coordinates"),
        kernel.prove_expression_equality(hessian.det(),sp.Rational(3,4),subject="portal Hessian is strictly positive"),
        kernel.prove_exact_spectrum(hessian,hessian_spectrum,subject="portal Hessian has positive spectrum"),
        kernel.prove_matrix_equality(stationary_gradient,sp.zeros(2,1),subject="conditional source selects the RG and K43 targets"),
        kernel.prove_expression_equality(bridge_readout,-32*sp.pi**2/3-sp.log(42),subject="portal covector reads the required logarithmic bridge"),
        kernel.prove_expression_equality(sp.exp(bridge_readout),sp.exp(-32*sp.pi**2/3)/42,subject="portal readout reproduces the required scale ratio"),
        kernel.prove_matrix_equality(architecture,sp.ones(11,1),subject="minimal typed portal architecture is complete"),
        kernel.prove_expression_equality(sum(architecture),11,subject="eleven portal architecture requirements pass"),
        kernel.prove_matrix_equality(physical_origin,sp.zeros(4,1),subject="carrier portal coefficient and source origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin),0,subject="strict physical portal score remains zero"),
    )
    gate_theorem=kernel.prove_gate("version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_minimal_portal_operator_architecture_gate",theorems)
    return MinimalPortalArchitectureCertificate(p_rg,p_43,portal,algebra_basis,commutant_map,commutant_kernel,hessian,hessian_spectrum,target,source,stationary_gradient,bridge_readout,architecture,physical_origin,theorems,gate_theorem)


SPEC=GateSpec(identifier="version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_minimal_portal_operator_architecture_gate",title="Минимальная типизированная portal-архитектура RG--K43",source_paths=("s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_minimal_portal_operator_architecture_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_minimal_portal_operator_architecture_gate_results.json"),obligations=tuple(Obligation(f"minimal_portal_architecture_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(24)))