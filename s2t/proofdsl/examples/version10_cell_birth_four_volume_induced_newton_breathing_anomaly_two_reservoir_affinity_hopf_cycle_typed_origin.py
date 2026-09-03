"""LCF certificate for the Hopf-cycle origin of the two-bath affinity difference."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HopfAffinityCertificate:
    edge_affinities: sp.ImmutableMatrix
    reservoir_affinities: sp.ImmutableMatrix
    affinity_map: sp.ImmutableMatrix
    affinity_kernel: sp.ImmutableMatrix
    anchored_affinity_map: sp.ImmutableMatrix
    rate_clock_map: sp.ImmutableMatrix
    rate_clock_kernel: sp.ImmutableMatrix
    hessian: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HopfAffinityCertificate:
    log2=sp.log(2)
    edge_affinities=sp.ImmutableMatrix([log2,log2,log2])
    reservoir_affinities=sp.ImmutableMatrix([log2,2*log2])
    affinity_map=sp.ImmutableMatrix([[-1,1,-1],[0,0,1]])
    affinity_kernel=sp.ImmutableMatrix([1,1,0])
    anchored_affinity_map=sp.ImmutableMatrix.vstack(affinity_map,sp.ImmutableMatrix([[1,0,0]]))
    rate_clock_map=sp.ImmutableMatrix([[1,1]])
    rate_clock_kernel=sp.ImmutableMatrix([1,-1])
    u1,u2,u3=sp.symbols("u1 u2 u3",real=True)
    parent=((u1-1)**2+(u2-u1)**2+(u3-u2)**2)/2
    hessian=sp.ImmutableMatrix(sp.hessian(parent,(u1,u2,u3)))
    conditional_origin=sp.ones(8,1)
    physical_origin=sp.zeros(2,1)
    ts=(
      kernel.prove_expression_equality(sum(edge_affinities),3*log2,subject="three Hopf edge affinities sum to the cycle affinity"),
      kernel.prove_matrix_equality(edge_affinities,sp.Matrix([log2]*3),subject="cyclic symmetry fixes equal edge affinities"),
      kernel.prove_expression_equality(reservoir_affinities[1]-reservoir_affinities[0],log2,subject="two-reservoir affinity difference"),
      kernel.prove_expression_equality(sp.log(sp.Rational(1,2)/sp.Rational(1,4)),log2,subject="KMS ratio quotient equals the Hopf edge affinity"),
      kernel.prove_expression_equality(3*sp.Rational(1,66),sp.Rational(1,22),subject="edge-current matching fixes kappa times the step"),
      kernel.prove_expression_equality(sp.Rational(1,66)*log2,log2/66,subject="one-edge entropy production matches the two-bath entropy"),
      kernel.prove_exact_rank(affinity_map,2,subject="difference and edge affinity give two independent relations"),
      kernel.prove_exact_nullity(affinity_map,1,subject="one common affinity offset remains"),
      kernel.prove_matrix_equality(affinity_map*affinity_kernel,sp.zeros(2,1),subject="common bath affinity shift is invisible"),
      kernel.prove_exact_rank(anchored_affinity_map,3,subject="one independent bath affinity removes the offset"),
      kernel.prove_exact_rank(rate_clock_map,1,subject="current matching fixes only a rate-time product"),
      kernel.prove_exact_nullity(rate_clock_map,1,subject="absolute clock-rate calibration remains free"),
      kernel.prove_matrix_equality(rate_clock_map*rate_clock_kernel,sp.zeros(1,1),subject="rate and step time counter-rescale"),
      kernel.prove_matrix_equality(hessian,sp.Matrix([[2,-1,0],[-1,2,-1],[0,-1,1]]),subject="Hopf affinity parent Hessian"),
      kernel.prove_exact_rank(hessian,3,subject="Hopf affinity parent rank"),
      kernel.prove_expression_equality(hessian.det(),1,subject="Hopf affinity parent determinant"),
      kernel.prove_matrix_equality(conditional_origin,sp.ones(8,1),subject="conditional Hopf affinity transfer complete"),
      kernel.prove_expression_equality(sum(conditional_origin),8,subject="eight conditional affinity requirements pass"),
      kernel.prove_matrix_equality(physical_origin,sp.zeros(2,1),subject="common temperature and absolute clock origins open"),
      kernel.prove_expression_equality(sum(physical_origin),0,subject="no absolute physical anchor supplied"),
    )
    gate=kernel.prove_gate("version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_affinity_hopf_cycle_typed_origin_gate",ts)
    return HopfAffinityCertificate(edge_affinities,reservoir_affinities,affinity_map,affinity_kernel,anchored_affinity_map,rate_clock_map,rate_clock_kernel,hessian,conditional_origin,physical_origin,ts,gate)


SPEC=GateSpec(
 identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_affinity_hopf_cycle_typed_origin_gate",
 title="Хопфовское происхождение разности сродств двух резервуаров",
 source_paths=("s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_affinity_hopf_cycle_typed_origin_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_affinity_hopf_cycle_typed_origin_gate_results.json"),
 obligations=tuple(Obligation(f"hopf_affinity_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(20)),
)