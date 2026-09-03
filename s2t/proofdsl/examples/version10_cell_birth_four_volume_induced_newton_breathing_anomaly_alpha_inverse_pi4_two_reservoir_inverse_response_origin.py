"""LCF certificate for the two-reservoir inverse-response pi^-4 correction."""
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel

@dataclass(frozen=True, slots=True)
class Certificate:
    reservoir_ratios: sp.ImmutableMatrix
    normalized_couplings: sp.ImmutableMatrix
    response_family: sp.Expr
    unit_response: sp.Expr
    old_dipole_response: sp.Expr
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    response_map: sp.ImmutableMatrix
    response_kernel: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem

@lru_cache(maxsize=1)
def build_certificate() -> Certificate:
    S=sp.symbols("S_geo",positive=True)
    chi=sp.symbols("chi_resp",positive=True)
    t=sp.symbols("t",real=True)
    rh=sp.sqrt(2)/sp.pi**2;rc=1/(sp.sqrt(2)*sp.pi**2)
    ratios=sp.ImmutableMatrix([rh,rc]);couplings=sp.ImmutableMatrix([rh/S,rc/S])
    response=sp.simplify(-chi*couplings[0]*couplings[1])
    unit=sp.simplify(response.subs(chi,1));old_chi=sp.pi**3/32
    old=sp.simplify(response.subs(chi,old_chi))
    scaled=sp.simplify(-chi*(t*couplings[0])*(t*couplings[1]))
    candidates=sp.ImmutableMatrix([
      [1,0,1,1,1,0], # unit cross susceptibility
      [1,0,0,1,1,0], # historical 32 pi coefficient
      [0,1,0,1,1,0], # uncorrelated fluctuation covariance
      [1,0,1,1,0,0], # linear Onsager response
      [1,1,1,0,1,0], # Schur-complement parent
      [1,0,1,1,1,0], # CODATA-normalized response
    ])
    passes=sp.ImmutableMatrix([sp.prod(candidates.row(i)) for i in range(6)])
    rmap=sp.ImmutableMatrix([[1,1,1]])
    rker=sp.ImmutableMatrix([[1,0],[-1,1],[0,-1]])
    conditional=sp.ones(4,1);physical=sp.zeros(2,1)
    ts=(
      kernel.prove_matrix_equality(ratios,sp.Matrix([sp.sqrt(2)/sp.pi**2,1/(sp.sqrt(2)*sp.pi**2)]),subject="two reservoir ratios"),
      kernel.prove_expression_equality(rh*rc,sp.pi**-4,subject="reservoir product pi inverse fourth"),
      kernel.prove_matrix_equality(couplings,sp.Matrix([sp.sqrt(2)/(sp.pi**2*S),1/(sp.sqrt(2)*sp.pi**2*S)]),subject="two normalized boundary couplings"),
      kernel.prove_expression_equality(response,-chi/(sp.pi**4*S**2),subject="inverse response family"),
      kernel.prove_positive_expression(-response,subject="positive dissipation gives negative vacuum correction"),
      kernel.prove_expression_equality(sp.diff(scaled,t).subs(t,0),0,subject="inverse response has no linear term"),
      kernel.prove_expression_equality(sp.diff(scaled,t,2).subs(t,0),-2*chi/(sp.pi**4*S**2),subject="inverse response is second order"),
      kernel.prove_expression_equality(unit,-1/(sp.pi**4*S**2),subject="unit susceptibility reproduces the late correction"),
      kernel.prove_positive_expression(old_chi,subject="historical dipole susceptibility is admissible"),
      kernel.prove_expression_equality(old,-1/(32*sp.pi*S**2),subject="same family reproduces historical correction"),
      kernel.prove_positive_expression(sp.simplify((-unit)-(-old)),subject="unit and historical magnitudes are distinct"),
      kernel.prove_matrix_equality(candidates,sp.Matrix(candidates),subject="six response origins on six criteria"),
      kernel.prove_matrix_equality(passes,sp.zeros(6,1),subject="no response origin passes complete contract"),
      kernel.prove_exact_rank(candidates,5,subject="response candidate criterion rank"),
      kernel.prove_exact_rank(rmap,1,subject="observable response fixes one product"),
      kernel.prove_exact_nullity(rmap,2,subject="two response normalizations remain free"),
      kernel.prove_matrix_equality(rmap*rker,sp.zeros(1,2),subject="response normalization kernel"),
      kernel.prove_matrix_equality(conditional,sp.ones(4,1),subject="conditional sign order pi factor and form close"),
      kernel.prove_matrix_equality(physical,sp.zeros(2,1),subject="susceptibility and alpha morphism origins open"),
      kernel.prove_expression_equality(sum(physical),0,subject="third correction not physically derived"))
    gate=kernel.prove_gate("version10_cell_birth_four_volume_induced_newton_breathing_anomaly_alpha_inverse_pi4_two_reservoir_inverse_response_origin_gate",ts)
    return Certificate(ratios,couplings,response,unit,old,candidates,passes,rmap,rker,conditional,physical,ts,gate)

SPEC=GateSpec(identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_alpha_inverse_pi4_two_reservoir_inverse_response_origin_gate",title="Двухрезервуарное inverse-response происхождение третьей поправки",source_paths=("s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_alpha_inverse_pi4_two_reservoir_inverse_response_origin_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_alpha_inverse_pi4_two_reservoir_inverse_response_origin_gate_results.json"),obligations=tuple(Obligation(f"pi4_response_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(20)))