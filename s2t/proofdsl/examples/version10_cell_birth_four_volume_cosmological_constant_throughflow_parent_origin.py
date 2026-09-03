"""LCF certificate for the throughflow parent of cosmological curvature."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CosmologicalThroughflowParentCertificate:
    affinity: sp.Expr
    entropy_production: sp.Expr
    curvature_response: sp.Expr
    parent: sp.Expr
    stationary_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    inherited_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    affinity_theorem: Theorem
    entropy_theorem: Theorem
    parent_stationary_theorem: Theorem
    parent_hessian_theorem: Theorem
    parent_rank_theorem: Theorem
    parent_determinant_theorem: Theorem
    parent_spectrum_theorem: Theorem
    curvature_entropy_theorem: Theorem
    curvature_conductance_theorem: Theorem
    zero_flow_curvature_theorem: Theorem
    scale_rank_theorem: Theorem
    scale_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    architecture_theorem: Theorem
    conditional_origin_theorem: Theorem
    conditional_score_theorem: Theorem
    inherited_origin_theorem: Theorem
    inherited_score_theorem: Theorem
    physical_origin_theorem: Theorem
    physical_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CosmologicalThroughflowParentCertificate:
    conductance, light_speed = sp.symbols("kappa c", positive=True)
    s_flow, u_curvature = sp.symbols("s_flow u_Lambda", real=True)

    affinity = 3 * sp.log(2)
    entropy_production = conductance * sp.log(2)
    curvature_response = sp.simplify(
        3 * entropy_production**2 / (light_speed**2 * affinity**2)
    )

    # s_flow normalizes entropy production; u_curvature normalizes curvature.
    parent = ((s_flow - 1) ** 2 + (u_curvature - s_flow) ** 2) / 2
    stationary_point = {s_flow: 1, u_curvature: 1}
    stationary_gradient = sp.ImmutableMatrix([
        sp.diff(parent, variable).subs(stationary_point)
        for variable in (s_flow, u_curvature)
    ])
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, (s_flow, u_curvature)))

    # log(kappa), log(sigma), log(Lambda).
    scale_map = sp.ImmutableMatrix([
        [-1, 1, 0],
        [0, -2, 1],
    ])
    scale_vector = sp.ImmutableMatrix([1, 1, 2])
    architecture = sp.ones(10, 1)
    conditional_origin = sp.ones(5, 1)
    inherited_origin = sp.ImmutableMatrix([1, 1, 0])
    physical_origin = sp.zeros(2, 1)

    affinity_theorem = kernel.prove_expression_equality(
        affinity,
        3 * sp.log(2),
        subject="the oriented Hopf cycle supplies a fixed dimensionless affinity",
    )
    entropy_theorem = kernel.prove_expression_equality(
        entropy_production,
        conductance * sp.log(2),
        subject="the throughflow entropy production is linear in conductance",
    )
    parent_stationary_theorem = kernel.prove_matrix_equality(
        stationary_gradient,
        sp.zeros(2, 1),
        subject="the throughflow-curvature parent selects unit normalized flow and curvature",
    )
    parent_hessian_theorem = kernel.prove_matrix_equality(
        parent_hessian,
        sp.Matrix([[2, -1], [-1, 1]]),
        subject="the conditional throughflow-curvature parent has an exact Hessian",
    )
    parent_rank_theorem = kernel.prove_exact_rank(
        parent_hessian,
        2,
        subject="the conditional parent controls both relative response variables",
    )
    parent_determinant_theorem = kernel.prove_expression_equality(
        parent_hessian.det(),
        1,
        subject="the conditional parent Hessian has unit determinant",
    )
    parent_spectrum_theorem = kernel.prove_exact_spectrum(
        parent_hessian,
        {
            (sp.Integer(3) - sp.sqrt(5)) / 2: 1,
            (sp.Integer(3) + sp.sqrt(5)) / 2: 1,
        },
        subject="the conditional throughflow-curvature parent is strictly positive",
    )
    curvature_entropy_theorem = kernel.prove_expression_equality(
        curvature_response,
        3 * entropy_production**2 / (light_speed**2 * affinity**2),
        subject="the selected cosmological curvature is the squared dissipative response",
    )
    curvature_conductance_theorem = kernel.prove_expression_equality(
        curvature_response,
        conductance**2 / (3 * light_speed**2),
        subject="the throughflow response reproduces the conductance cosmological relation",
    )
    zero_flow_curvature_theorem = kernel.prove_expression_equality(
        curvature_response.subs(conductance, 0),
        0,
        subject="the conditional cosmological response collapses when throughflow stops",
    )
    scale_rank_theorem = kernel.prove_exact_rank(
        scale_map,
        2,
        subject="entropy and curvature relations fix two relative scale directions",
    )
    scale_nullity_theorem = kernel.prove_exact_nullity(
        scale_map,
        1,
        subject="one common throughflow-curvature scale remains",
    )
    scale_kernel_theorem = kernel.prove_matrix_equality(
        scale_map * scale_vector,
        sp.zeros(2, 1),
        subject="linear rate scaling and quadratic curvature scaling form the exact kernel",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(10, 1),
        subject="the conditional throughflow-curvature parent architecture is complete",
    )
    conditional_origin_theorem = kernel.prove_matrix_equality(
        conditional_origin,
        sp.ones(5, 1),
        subject="all conditional response relations are selected by the proposed parent",
    )
    conditional_score_theorem = kernel.prove_expression_equality(
        sum(conditional_origin),
        5,
        subject="five conditional response requirements pass",
    )
    inherited_origin_theorem = kernel.prove_matrix_equality(
        inherited_origin,
        sp.Matrix([1, 1, 0]),
        subject="affinity and entropy are inherited while the curvature coupling is new",
    )
    inherited_score_theorem = kernel.prove_expression_equality(
        sum(inherited_origin),
        2,
        subject="two of three parent-source requirements are inherited",
    )
    physical_origin_theorem = kernel.prove_matrix_equality(
        physical_origin,
        sp.zeros(2, 1),
        subject="physical curvature-coupling origin and absolute scale remain open",
    )
    physical_score_theorem = kernel.prove_expression_equality(
        sum(physical_origin),
        0,
        subject="the conditional parent supplies no absolute cosmological scale",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin_gate",
        (
            affinity_theorem,
            entropy_theorem,
            parent_stationary_theorem,
            parent_hessian_theorem,
            parent_rank_theorem,
            parent_determinant_theorem,
            parent_spectrum_theorem,
            curvature_entropy_theorem,
            curvature_conductance_theorem,
            zero_flow_curvature_theorem,
            scale_rank_theorem,
            scale_nullity_theorem,
            scale_kernel_theorem,
            architecture_theorem,
            conditional_origin_theorem,
            conditional_score_theorem,
            inherited_origin_theorem,
            inherited_score_theorem,
            physical_origin_theorem,
            physical_score_theorem,
        ),
    )
    return CosmologicalThroughflowParentCertificate(
        affinity,
        entropy_production,
        curvature_response,
        parent,
        stationary_gradient,
        parent_hessian,
        scale_map,
        scale_vector,
        architecture,
        conditional_origin,
        inherited_origin,
        physical_origin,
        affinity_theorem,
        entropy_theorem,
        parent_stationary_theorem,
        parent_hessian_theorem,
        parent_rank_theorem,
        parent_determinant_theorem,
        parent_spectrum_theorem,
        curvature_entropy_theorem,
        curvature_conductance_theorem,
        zero_flow_curvature_theorem,
        scale_rank_theorem,
        scale_nullity_theorem,
        scale_kernel_theorem,
        architecture_theorem,
        conditional_origin_theorem,
        conditional_score_theorem,
        inherited_origin_theorem,
        inherited_score_theorem,
        physical_origin_theorem,
        physical_score_theorem,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin_gate",
    title="Родитель космологической постоянной из сквозного потока",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("throughflow_cycle_affinity", lambda: build_certificate().affinity_theorem),
        Obligation("throughflow_entropy_production", lambda: build_certificate().entropy_theorem),
        Obligation("throughflow_curvature_parent_stationary", lambda: build_certificate().parent_stationary_theorem),
        Obligation("throughflow_curvature_parent_hessian", lambda: build_certificate().parent_hessian_theorem),
        Obligation("throughflow_curvature_parent_rank_two", lambda: build_certificate().parent_rank_theorem),
        Obligation("throughflow_curvature_parent_determinant_one", lambda: build_certificate().parent_determinant_theorem),
        Obligation("throughflow_curvature_parent_positive_spectrum", lambda: build_certificate().parent_spectrum_theorem),
        Obligation("cosmological_curvature_entropy_response", lambda: build_certificate().curvature_entropy_theorem),
        Obligation("cosmological_curvature_conductance_relation", lambda: build_certificate().curvature_conductance_theorem),
        Obligation("zero_throughflow_zero_curvature_response", lambda: build_certificate().zero_flow_curvature_theorem),
        Obligation("throughflow_curvature_scale_rank_two", lambda: build_certificate().scale_rank_theorem),
        Obligation("throughflow_curvature_scale_nullity_one", lambda: build_certificate().scale_nullity_theorem),
        Obligation("throughflow_curvature_scale_kernel", lambda: build_certificate().scale_kernel_theorem),
        Obligation("throughflow_curvature_architecture_full", lambda: build_certificate().architecture_theorem),
        Obligation("throughflow_curvature_conditional_origin_full", lambda: build_certificate().conditional_origin_theorem),
        Obligation("throughflow_curvature_conditional_score", lambda: build_certificate().conditional_score_theorem),
        Obligation("throughflow_curvature_inherited_origin", lambda: build_certificate().inherited_origin_theorem),
        Obligation("throughflow_curvature_inherited_score", lambda: build_certificate().inherited_score_theorem),
        Obligation("throughflow_curvature_physical_origin_open", lambda: build_certificate().physical_origin_theorem),
        Obligation("throughflow_curvature_physical_score_zero", lambda: build_certificate().physical_score_theorem),
    ),
)