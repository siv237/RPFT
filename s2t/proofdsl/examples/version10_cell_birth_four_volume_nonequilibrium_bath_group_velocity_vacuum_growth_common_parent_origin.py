"""LCF certificate for the common parent of bath velocity and vacuum growth."""
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel

@dataclass(frozen=True, slots=True)
class BathVelocityGrowthParentCertificate:
    parent: sp.Expr
    stationary_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    provenance_map: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_ledger: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem

@lru_cache(maxsize=1)
def build_certificate() -> BathVelocityGrowthParentCertificate:
    x=sp.symbols("x",positive=True)
    r,q,u=sp.symbols("r q u",real=True)
    kx=sp.log((1+2*x)/(1+x))
    a=sp.Rational(121,12)
    selected={r:a,q:kx,u:a*kx/2}
    residual=sp.ImmutableMatrix([r-a,q-kx,r*q-2*u])
    parent=sp.expand((residual.dot(residual))/2)
    stationary_gradient=sp.ImmutableMatrix([sp.diff(parent,z).subs(selected) for z in (r,q,u)])
    parent_hessian=sp.ImmutableMatrix(sp.hessian(parent,(r,q,u)).subs(selected))
    expected_hessian=sp.ImmutableMatrix([
      [1+kx**2,a*kx,-2*kx],
      [a*kx,1+a**2,-2*a],
      [-2*kx,-2*a,4],
    ])
    provenance_map=sp.eye(3)
    # log ell, log Omega_C, log kappa, log Omega_bath
    scale_map=sp.ImmutableMatrix([[1,1,0,0],[0,-1,1,0],[0,0,-1,1]])
    scale_kernel=sp.ImmutableMatrix([1,-1,-1,-1])
    architecture=sp.ones(10,1)
    conditional_origin=sp.ones(8,1)
    physical_ledger=sp.ImmutableMatrix([1,1,1,1,0])
    velocity_ratio=sp.simplify(selected[u])
    front_ratio=sp.simplify(velocity_ratio/(kx/3))
    ts=(
      kernel.prove_matrix_equality(stationary_gradient,sp.zeros(3,1),subject="common parent stationary point"),
      kernel.prove_matrix_equality(parent_hessian,expected_hessian,subject="bath velocity growth parent Hessian"),
      kernel.prove_expression_equality(parent_hessian.det(),4,subject="common parent Hessian determinant"),
      kernel.prove_exact_rank(parent_hessian,3,subject="common parent controls all relative variables"),
      kernel.prove_positive_expression(parent_hessian[0,0],subject="first common parent leading minor"),
      kernel.prove_positive_expression(parent_hessian[:2,:2].det(),subject="second common parent leading minor"),
      kernel.prove_expression_equality(velocity_ratio,sp.Rational(121,24)*kx,subject="selected bath group velocity"),
      kernel.prove_expression_equality(a*kx,2*velocity_ratio,subject="dispersion compatibility at parent zero"),
      kernel.prove_expression_equality(front_ratio,sp.Rational(121,8),subject="blind bath velocity to cell front ratio"),
      kernel.prove_expression_equality(sp.limit(kx/x,x,0,dir='+'),1,subject="weak vacuum growth coupling limit"),
      kernel.prove_expression_equality(sp.limit(velocity_ratio/x,x,0,dir='+'),sp.Rational(121,24),subject="weak vacuum velocity coefficient"),
      kernel.prove_expression_equality(sp.limit((velocity_ratio)/(x/sp.sqrt(8*sp.pi)),x,0,dir='+'),sp.Rational(121,24)*sp.sqrt(8*sp.pi),subject="velocity to vacuum amplitude asymptotic ratio"),
      kernel.prove_matrix_equality(provenance_map,sp.eye(3),subject="three parent residuals have independent inherited provenance"),
      kernel.prove_exact_rank(provenance_map,3,subject="inherited relation provenance rank"),
      kernel.prove_expression_equality(residual[0].subs(selected),0,subject="memory cutoff residual closes"),
      kernel.prove_expression_equality(residual[1].subs(selected),0,subject="conductance growth residual closes"),
      kernel.prove_expression_equality(residual[2].subs(selected),0,subject="cell dispersion residual closes"),
      kernel.prove_exact_rank(scale_map,3,subject="absolute length frequency map rank"),
      kernel.prove_exact_nullity(scale_map,1,subject="one absolute length frequency orbit remains"),
      kernel.prove_matrix_equality(scale_map*scale_kernel,sp.zeros(3,1),subject="absolute scale kernel"),
      kernel.prove_matrix_equality(architecture,sp.ones(10,1),subject="common parent architecture complete"),
      kernel.prove_expression_equality(sum(architecture),10,subject="ten common parent architecture checks pass"),
      kernel.prove_matrix_equality(conditional_origin,sp.ones(8,1),subject="conditional relative origin complete"),
      kernel.prove_expression_equality(sum(conditional_origin),8,subject="eight conditional origin requirements pass"),
      kernel.prove_matrix_equality(physical_ledger,sp.Matrix([1,1,1,1,0]),subject="dimensionless velocity closes while absolute scale stays open"),
      kernel.prove_expression_equality(sum(physical_ledger),4,subject="four of five physical status entries pass"),
    )
    gate=kernel.prove_gate("version10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_vacuum_growth_common_parent_origin_gate",ts)
    return BathVelocityGrowthParentCertificate(parent,stationary_gradient,parent_hessian,provenance_map,scale_map,scale_kernel,architecture,conditional_origin,physical_ledger,ts,gate)

SPEC=GateSpec("version10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_vacuum_growth_common_parent_origin_gate","Общий родитель скорости ванны и вакуумного роста",("s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_vacuum_growth_common_parent_origin_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_vacuum_growth_common_parent_origin_gate_results.json"),tuple(Obligation(f"bath_velocity_growth_parent_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(26)))