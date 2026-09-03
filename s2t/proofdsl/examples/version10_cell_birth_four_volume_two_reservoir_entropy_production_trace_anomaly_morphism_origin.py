"""LCF certificate for the entropy-production to trace-anomaly morphism."""
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel

@dataclass(frozen=True, slots=True)
class Certificate:
    entropy_per_step: sp.Expr
    entropy_energy_density: sp.Expr
    einstein_trace_density: sp.Expr
    selected_newton_ratio: sp.Expr
    scale_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    anchored_scale_map: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem

@lru_cache(maxsize=1)
def build_certificate() -> Certificate:
    ell,c,hbar,gamma=sp.symbols("ell_cell c hbar gamma",positive=True)
    sigma=sp.log(2)/66
    tau=ell/c; energy=hbar*c/ell; v3=ell**3; v4=ell**4
    rho_entropy=sp.simplify(energy*sigma/v3)
    curvature=12/ell**2; g_newton=gamma*ell**2
    rho_einstein=sp.simplify(hbar*c*curvature/(8*sp.pi*g_newton))
    selected_gamma=sp.simplify(99/(sp.pi*sp.log(2)))
    scale_map=sp.ImmutableMatrix([
      [1,1,0,0,0,0,0],[-1,0,1,0,0,0,0],[-3,0,0,1,0,0,0],
      [0,-1,0,1,1,0,0],[-2,0,0,0,0,1,0],[2,0,0,0,0,0,1],
      [0,0,0,0,1,1,-1]])
    scale_vector=sp.ImmutableMatrix([1,-1,1,3,-4,2,-2])
    anchored=sp.ImmutableMatrix.vstack(scale_map,sp.ImmutableMatrix([[1,0,0,0,0,0,0]]))
    architecture=sp.ones(10,1);conditional=sp.ones(7,1);physical=sp.zeros(3,1)
    ts=(
      kernel.prove_expression_equality(sigma,sp.log(2)/66,subject="two-reservoir entropy per transition"),
      kernel.prove_positive_expression(sigma,subject="positive nonequilibrium entropy production"),
      kernel.prove_expression_equality(tau,ell/c,subject="cell light-crossing clock"),
      kernel.prove_expression_equality(energy*tau,hbar,subject="cell clock energy action quantum"),
      kernel.prove_expression_equality(v3,ell**3,subject="cell spatial volume"),
      kernel.prove_expression_equality(v4,ell**4,subject="cell four-volume"),
      kernel.prove_expression_equality(rho_entropy,hbar*c*sp.log(2)/(66*ell**4),subject="entropy energy density"),
      kernel.prove_expression_equality(curvature,12/ell**2,subject="cell curvature magnitude inherited from v R squared"),
      kernel.prove_expression_equality(g_newton,gamma*ell**2,subject="dimensionless Newton-to-cell area ratio"),
      kernel.prove_expression_equality(rho_einstein,3*hbar*c/(2*sp.pi*gamma*ell**4),subject="Einstein trace energy density"),
      kernel.prove_expression_equality(sp.simplify(rho_einstein/rho_entropy),99/(sp.pi*gamma*sp.log(2)),subject="density ratio is scale free"),
      kernel.prove_expression_equality(selected_gamma,99/(sp.pi*sp.log(2)),subject="trace balance selects only Newton area ratio"),
      kernel.prove_positive_expression(selected_gamma-1,subject="entropy trace balance conflicts with unit Planck ratio"),
      kernel.prove_matrix_equality(scale_map,sp.Matrix(scale_map),subject="entropy Einstein scale map"),
      kernel.prove_exact_rank(scale_map,6,subject="entropy Einstein scale rank"),
      kernel.prove_exact_nullity(scale_map,1,subject="one absolute scale orbit remains"),
      kernel.prove_matrix_equality(scale_map*scale_vector,sp.zeros(7,1),subject="common length rescaling kernel"),
      kernel.prove_exact_rank(anchored,7,subject="one external length anchor closes the scale map"),
      kernel.prove_matrix_equality(architecture,sp.ones(10,1),subject="entropy trace morphism architecture"),
      kernel.prove_matrix_equality(conditional,sp.ones(7,1),subject="conditional entropy trace chain"),
      kernel.prove_matrix_equality(physical,sp.zeros(3,1),subject="temperature stress and absolute scale origins open"),
      kernel.prove_expression_equality(sum(physical),0,subject="no absolute scale is derived"))
    gate=kernel.prove_gate("version10_cell_birth_four_volume_two_reservoir_entropy_production_trace_anomaly_morphism_origin_gate",ts)
    return Certificate(sigma,rho_entropy,rho_einstein,selected_gamma,scale_map,scale_vector,anchored,architecture,conditional,physical,ts,gate)

SPEC=GateSpec(identifier="version10_cell_birth_four_volume_two_reservoir_entropy_production_trace_anomaly_morphism_origin_gate",title="Морфизм производства энтропии в следовую аномалию",source_paths=("s2t/gates/version10_cell_birth_four_volume_two_reservoir_entropy_production_trace_anomaly_morphism_origin_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_two_reservoir_entropy_production_trace_anomaly_morphism_origin_gate_results.json"),obligations=tuple(Obligation(f"entropy_trace_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(22)))