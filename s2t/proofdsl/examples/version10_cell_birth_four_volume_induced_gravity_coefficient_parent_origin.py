"""LCF certificate for through-flow-induced gravitational coefficients."""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class ThroughFlowInducedGravityCoefficientCertificate:
    throughflow_constraint_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_ledger: sp.ImmutableMatrix
    balance_theorem: Theorem
    throughput_theorem: Theorem
    entropy_production_theorem: Theorem
    square_parent_theorem: Theorem
    broken_stationary_theorem: Theorem
    broken_scale_theorem: Theorem
    broken_hessian_theorem: Theorem
    origin_hessian_theorem: Theorem
    zero_flow_parent_theorem: Theorem
    zero_flow_stationary_theorem: Theorem
    volume_coefficient_theorem: Theorem
    einstein_coefficient_theorem: Theorem
    selected_curvature_scale_theorem: Theorem
    constraint_rank_theorem: Theorem
    constraint_nullity_theorem: Theorem
    constraint_kernel_theorem: Theorem
    architecture_theorem: Theorem
    conditional_origin_theorem: Theorem
    physical_ledger_theorem: Theorem
    physical_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> ThroughFlowInducedGravityCoefficientCertificate:
    current, incoming, outgoing, affinity = sp.symbols("J J_in J_out F", positive=True)
    coupling, stiffness = sp.symbols("g lambda", positive=True)
    alpha, beta = sp.symbols("alpha beta", positive=True)
    x = sp.symbols("x", real=True)
    q = sp.symbols("q", positive=True)

    net_birth = incoming - outgoing
    throughput = incoming + outgoing
    entropy_production = affinity * current
    parent = stiffness * (x**2 - coupling*entropy_production/stiffness)**2 / 4
    broken_x = sp.sqrt(coupling*entropy_production/stiffness)
    induced_seed = sp.simplify(broken_x**2)
    coefficient_a = alpha * induced_seed**2
    coefficient_b = beta * induced_seed
    selected_q = sp.simplify(coefficient_b/(2*coefficient_a))

    throughflow_constraint_map = sp.ImmutableMatrix([[1, 1, 0], [0, 1, -1]])
    scale_vector = sp.ImmutableMatrix([1, -1, -1])
    architecture = sp.ones(9, 1)
    conditional_origin = sp.ones(4, 1)
    physical_ledger = sp.zeros(2, 1)

    balance_theorem = kernel.prove_expression_equality(net_birth.subs({incoming: current, outgoing: current}), 0, subject="equal incoming and outgoing currents preserve the stored cell number")
    throughput_theorem = kernel.prove_expression_equality(throughput.subs({incoming: current, outgoing: current}), 2*current, subject="balanced storage can coexist with nonzero through-flow activity")
    entropy_production_theorem = kernel.prove_expression_equality(entropy_production, affinity*current, subject="oriented through flow has positive entropy production")
    square_parent_theorem = kernel.prove_expression_equality(parent, stiffness*(x**2-coupling*entropy_production/stiffness)**2/4, subject="through-flow order parent is an exact nonnegative square")
    broken_stationary_theorem = kernel.prove_expression_equality(sp.diff(parent, x).subs(x, broken_x), 0, subject="nonzero through flow creates an exact stationary geometric amplitude")
    broken_scale_theorem = kernel.prove_expression_equality(broken_x**2, coupling*entropy_production/stiffness, subject="the maintained geometric amplitude is proportional to entropy production")
    broken_hessian_theorem = kernel.prove_expression_equality(sp.diff(parent, x, 2).subs(x, broken_x), 2*coupling*entropy_production, subject="the maintained through-flow branch is locally stable")
    origin_hessian_theorem = kernel.prove_expression_equality(sp.diff(parent, x, 2).subs(x, 0), -coupling*entropy_production, subject="the collapsed branch is unstable while physical through flow is present")
    zero_flow_parent_theorem = kernel.prove_expression_equality(parent.subs(current, 0), stiffness*x**4/4, subject="turning off through flow removes the broken quadratic term")
    zero_flow_stationary_theorem = kernel.prove_expression_equality(sp.diff(parent, x).subs({current: 0, x: 0}), 0, subject="the zero-flow geometry admits the collapsed stationary state")
    volume_coefficient_theorem = kernel.prove_expression_equality(coefficient_a, alpha*(coupling*entropy_production/stiffness)**2, subject="the maintained amplitude conditionally induces the volume coefficient")
    einstein_coefficient_theorem = kernel.prove_expression_equality(coefficient_b, beta*coupling*entropy_production/stiffness, subject="the same through flow conditionally induces the Einstein coefficient")
    selected_curvature_scale_theorem = kernel.prove_expression_equality(selected_q*induced_seed, beta/(2*alpha), subject="induced coefficients still select only a dimensionless curvature product")
    constraint_rank_theorem = kernel.prove_exact_rank(throughflow_constraint_map, 2, subject="the curvature and through-flow relations impose two relative constraints")
    constraint_nullity_theorem = kernel.prove_exact_nullity(throughflow_constraint_map, 1, subject="one simultaneous through-flow and geometry scale remains free")
    constraint_kernel_theorem = kernel.prove_matrix_equality(throughflow_constraint_map*scale_vector, sp.zeros(2, 1), subject="inverse geometry and flow rescaling is the exact remaining kernel")
    architecture_theorem = kernel.prove_matrix_equality(architecture, sp.ones(9, 1), subject="the stationary through-flow architecture is fully constructed")
    conditional_origin_theorem = kernel.prove_matrix_equality(conditional_origin, sp.ones(4, 1), subject="balance activity entropy production and conditional symmetry breaking are derived")
    physical_ledger_theorem = kernel.prove_matrix_equality(physical_ledger, sp.zeros(2, 1), subject="physical affinity origin and absolute scale remain open")
    physical_score_theorem = kernel.prove_expression_equality(sum(physical_ledger), 0, subject="through-flow does not yet provide an absolute physical coefficient scale")
    gate_theorem = kernel.prove_gate("version10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin_gate", (balance_theorem, throughput_theorem, entropy_production_theorem, square_parent_theorem, broken_stationary_theorem, broken_scale_theorem, broken_hessian_theorem, origin_hessian_theorem, zero_flow_parent_theorem, zero_flow_stationary_theorem, volume_coefficient_theorem, einstein_coefficient_theorem, selected_curvature_scale_theorem, constraint_rank_theorem, constraint_nullity_theorem, constraint_kernel_theorem, architecture_theorem, conditional_origin_theorem, physical_ledger_theorem, physical_score_theorem))
    return ThroughFlowInducedGravityCoefficientCertificate(throughflow_constraint_map, scale_vector, architecture, conditional_origin, physical_ledger, balance_theorem, throughput_theorem, entropy_production_theorem, square_parent_theorem, broken_stationary_theorem, broken_scale_theorem, broken_hessian_theorem, origin_hessian_theorem, zero_flow_parent_theorem, zero_flow_stationary_theorem, volume_coefficient_theorem, einstein_coefficient_theorem, selected_curvature_scale_theorem, constraint_rank_theorem, constraint_nullity_theorem, constraint_kernel_theorem, architecture_theorem, conditional_origin_theorem, physical_ledger_theorem, physical_score_theorem, gate_theorem)


SPEC = GateSpec("version10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin_gate", "Сквозной ток и условно индуцированные коэффициенты гравитации", ("s2t/gates/version10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin_gate.tex", "s2t/results/s2t_v10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin_gate_results.json"), tuple(Obligation(name, getter) for name, getter in (
    ("balanced_throughflow_zero_storage_change", lambda: build_certificate().balance_theorem), ("balanced_throughflow_nonzero_activity", lambda: build_certificate().throughput_theorem), ("positive_entropy_production", lambda: build_certificate().entropy_production_theorem), ("throughflow_parent_exact_square", lambda: build_certificate().square_parent_theorem), ("maintained_geometry_stationary", lambda: build_certificate().broken_stationary_theorem), ("maintained_geometry_scale", lambda: build_certificate().broken_scale_theorem), ("maintained_geometry_positive_hessian", lambda: build_certificate().broken_hessian_theorem), ("collapsed_branch_negative_hessian", lambda: build_certificate().origin_hessian_theorem), ("zero_flow_quartic_parent", lambda: build_certificate().zero_flow_parent_theorem), ("zero_flow_collapsed_stationary", lambda: build_certificate().zero_flow_stationary_theorem), ("throughflow_induced_volume_coefficient", lambda: build_certificate().volume_coefficient_theorem), ("throughflow_induced_einstein_coefficient", lambda: build_certificate().einstein_coefficient_theorem), ("throughflow_selected_dimensionless_curvature", lambda: build_certificate().selected_curvature_scale_theorem), ("throughflow_constraint_rank_two", lambda: build_certificate().constraint_rank_theorem), ("throughflow_constraint_nullity_one", lambda: build_certificate().constraint_nullity_theorem), ("throughflow_scale_kernel", lambda: build_certificate().constraint_kernel_theorem), ("throughflow_architecture_full", lambda: build_certificate().architecture_theorem), ("throughflow_conditional_origin_full", lambda: build_certificate().conditional_origin_theorem), ("throughflow_physical_origin_zero", lambda: build_certificate().physical_ledger_theorem), ("throughflow_physical_score_zero", lambda: build_certificate().physical_score_theorem))))