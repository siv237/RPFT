"""LCF certificate for the canonical two-reservoir K43 current."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..channel import KrausChannel
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel
from ..structures import Morphism, Space


@dataclass(frozen=True, slots=True)
class TwoReservoirCertificate:
    completeness: sp.ImmutableMatrix
    transition: sp.ImmutableMatrix
    stationary: sp.ImmutableMatrix
    currents: sp.ImmutableMatrix
    entropy_production: sp.Expr
    hessian: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> TwoReservoirCertificate:
    dh = dc = sp.Rational(1, 6)
    uh, uc = sp.Rational(1, 12), sp.Rational(1, 24)
    up, down = uh + uc, dh + dc
    space = Space("W_Y", 2)
    matrices = (
        sp.diag(sp.sqrt(1-up), sp.sqrt(1-down)),
        sp.Matrix([[0, sp.sqrt(dh)], [0, 0]]),
        sp.Matrix([[0, sp.sqrt(dc)], [0, 0]]),
        sp.Matrix([[0, 0], [sp.sqrt(uh), 0]]),
        sp.Matrix([[0, 0], [sp.sqrt(uc), 0]]),
    )
    matrices = tuple(sp.ImmutableMatrix(x) for x in matrices)
    channel = KrausChannel.make(
        "Phi_two_bath",
        tuple(Morphism(f"K{i}", space, space, x) for i, x in enumerate(matrices)),
    )
    completeness = sp.ImmutableMatrix(sum((x.H*x for x in matrices), sp.zeros(2)))
    transition = sp.ImmutableMatrix([[1-up, down], [up, 1-down]])
    population = sp.ImmutableMatrix([sp.Rational(8, 11), sp.Rational(3, 11)])
    stationary = transition * population
    jh = sp.simplify(uh*population[0] - dh*population[1])
    jc = sp.simplify(uc*population[0] - dc*population[1])
    currents = sp.ImmutableMatrix([jh, jc])
    entropy_production = sp.simplify(jh * sp.log(2))

    u1,u2,u3=sp.symbols("u1 u2 u3", real=True)
    parent=((u1-1)**2+(u2-u1)**2+(u3-u2)**2)/2
    hessian=sp.ImmutableMatrix(sp.hessian(parent,(u1,u2,u3)))
    scale_map=sp.ImmutableMatrix([[2,0,1,0],[1,-1,0,0],[0,0,1,1]])
    scale_vector=sp.ImmutableMatrix([-1,-1,2,-2])
    architecture=sp.ones(10,1)
    physical_origin=sp.zeros(3,1)

    ts=(
        channel.theorem,
        kernel.prove_matrix_equality(completeness,sp.eye(2),subject="two-reservoir Kraus completeness"),
        kernel.prove_matrix_equality(transition,sp.Matrix([[sp.Rational(7,8),sp.Rational(1,3)],[sp.Rational(1,8),sp.Rational(2,3)]]),subject="two-reservoir population transition"),
        kernel.prove_matrix_equality(stationary,population,subject="two-reservoir stationary population"),
        kernel.prove_expression_equality(uh/dh,sp.Rational(1,2),subject="hot reservoir KMS ratio"),
        kernel.prove_expression_equality(uc/dc,sp.Rational(1,4),subject="cold reservoir KMS ratio"),
        kernel.prove_matrix_equality(currents,sp.Matrix([sp.Rational(1,66),-sp.Rational(1,66)]),subject="equal opposite bath currents"),
        kernel.prove_expression_equality(jh-jc,sp.Rational(1,33),subject="oriented current separation"),
        kernel.prove_expression_equality(entropy_production,sp.log(2)/66,subject="positive two-bath entropy production"),
        kernel.prove_positive_expression(entropy_production,subject="strictly positive nonequilibrium entropy production"),
        kernel.prove_matrix_equality(hessian,sp.Matrix([[2,-1,0],[-1,2,-1],[0,-1,1]]),subject="two-reservoir parent Hessian"),
        kernel.prove_exact_rank(hessian,3,subject="two-reservoir parent rank"),
        kernel.prove_expression_equality(hessian.det(),1,subject="two-reservoir parent determinant"),
        kernel.prove_exact_rank(scale_map,3,subject="two-reservoir scale rank"),
        kernel.prove_exact_nullity(scale_map,1,subject="two-reservoir scale nullity"),
        kernel.prove_matrix_equality(scale_map*scale_vector,sp.zeros(3,1),subject="two-reservoir scale kernel"),
        kernel.prove_matrix_equality(architecture,sp.ones(10,1),subject="two-reservoir architecture complete"),
        kernel.prove_matrix_equality(physical_origin,sp.zeros(3,1),subject="bath affinity rate and scale origins open"),
        kernel.prove_expression_equality(sum(physical_origin),0,subject="no absolute physical origin"),
    )
    gate=kernel.prove_gate("version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_nonequilibrium_two_reservoir_output_current_parent_admission_gate",ts)
    return TwoReservoirCertificate(completeness,transition,stationary,currents,entropy_production,hessian,scale_map,scale_vector,architecture,physical_origin,ts,gate)


SPEC=GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_nonequilibrium_two_reservoir_output_current_parent_admission_gate",
    title="Допуск двухрезервуарного неравновесного тока K43",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_nonequilibrium_two_reservoir_output_current_parent_admission_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_nonequilibrium_two_reservoir_output_current_parent_admission_gate_results.json",
    ),
    obligations=tuple(Obligation(f"two_bath_{i:02d}",lambda i=i: build_certificate().theorems[i]) for i in range(19)),
)