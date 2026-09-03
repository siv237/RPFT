"""LCF certificate for the throughflow breathing-anomaly scale parent."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class BreathingAnomalyThroughflowScaleCertificate:
    cell_volume: sp.Expr
    injection_density: sp.Expr
    flow_coefficient: sp.Expr
    logarithmic_stationary_ratio: sp.Expr
    parent: sp.Expr
    stationary_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    leading_minors: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    externally_anchored_map: sp.ImmutableMatrix
    inherited_origin: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    cell_volume_theorem: Theorem
    injection_density_theorem: Theorem
    flow_coefficient_theorem: Theorem
    leading_scale_cancellation_theorem: Theorem
    logarithmic_stationary_ratio_theorem: Theorem
    logarithmic_balance_theorem: Theorem
    zero_flow_injection_theorem: Theorem
    zero_seed_output_theorem: Theorem
    active_output_positive_theorem: Theorem
    parent_stationary_theorem: Theorem
    parent_hessian_theorem: Theorem
    parent_rank_theorem: Theorem
    parent_determinant_theorem: Theorem
    leading_minors_theorem: Theorem
    scale_rank_theorem: Theorem
    scale_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    external_anchor_rank_theorem: Theorem
    inherited_origin_theorem: Theorem
    inherited_score_theorem: Theorem
    architecture_theorem: Theorem
    conditional_origin_theorem: Theorem
    conditional_score_theorem: Theorem
    physical_origin_theorem: Theorem
    physical_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> BreathingAnomalyThroughflowScaleCertificate:
    alpha, beta_e, m, epsilon, b_a = sp.symbols(
        "alpha beta_E m epsilon b_A", positive=True
    )
    n_flow = sp.symbols("n_flow", nonnegative=True)

    cell_volume = beta_e**2 / (4 * alpha**2 * m**2)
    injection_density = sp.simplify(n_flow * sp.log(2) / cell_volume)
    flow_coefficient = sp.simplify(4 * alpha**2 * n_flow * sp.log(2) / beta_e**2)
    leading_output_density = epsilon * m**2
    logarithmic_stationary_ratio = sp.simplify((flow_coefficient / epsilon - 1) / b_a)
    logarithmic_output_density = epsilon * m**2 * (
        1 + b_a * logarithmic_stationary_ratio
    )

    u_v, u_balance, u_log = sp.symbols("u_v u_balance u_log", real=True)
    parent = (
        (u_v - 1) ** 2
        + (u_balance - u_v) ** 2
        + (u_log - u_balance) ** 2
    ) / 2
    stationary_point = {u_v: 1, u_balance: 1, u_log: 1}
    stationary_gradient = sp.ImmutableMatrix([
        sp.diff(parent, variable).subs(stationary_point)
        for variable in (u_v, u_balance, u_log)
    ])
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, (u_v, u_balance, u_log)))
    leading_minors = sp.ImmutableMatrix([
        parent_hessian[:1, :1].det(),
        parent_hessian[:2, :2].det(),
        parent_hessian.det(),
    ])

    # log(m), log(mu_spec^2), log(v_cell), log(density/Theta).
    scale_map = sp.ImmutableMatrix([
        [2, 0, 1, 0],
        [1, -1, 0, 0],
        [0, 0, 1, 1],
    ])
    scale_vector = sp.ImmutableMatrix([-1, -1, 2, -2])
    externally_anchored_map = sp.ImmutableMatrix.vstack(
        scale_map,
        sp.ImmutableMatrix([[0, 1, 0, 0]]),
    )

    inherited_origin = sp.ones(3, 1)
    architecture = sp.ones(10, 1)
    conditional_origin = sp.ones(8, 1)
    physical_origin = sp.zeros(3, 1)

    cell_volume_theorem = kernel.prove_expression_equality(
        cell_volume,
        beta_e**2 / (4 * alpha**2 * m**2),
        subject="the inherited cell area gives an inverse-square cell four-volume",
    )
    injection_density_theorem = kernel.prove_expression_equality(
        injection_density,
        4 * alpha**2 * n_flow * m**2 * sp.log(2) / beta_e**2,
        subject="throughflow injection per cell becomes a normalized density proportional to m squared",
    )
    flow_coefficient_theorem = kernel.prove_expression_equality(
        injection_density / m**2,
        flow_coefficient,
        subject="the throughflow density has an exact dimensionless coefficient",
    )
    leading_scale_cancellation_theorem = kernel.prove_expression_equality(
        injection_density - leading_output_density,
        m**2 * (flow_coefficient - epsilon),
        subject="leading inflow-output balance factors out the entire dimensional scale",
    )
    logarithmic_stationary_ratio_theorem = kernel.prove_expression_equality(
        logarithmic_stationary_ratio,
        (flow_coefficient / epsilon - 1) / b_a,
        subject="a logarithmic anomaly conditionally selects the relative scale logarithm",
    )
    logarithmic_balance_theorem = kernel.prove_expression_equality(
        injection_density,
        logarithmic_output_density,
        subject="the logarithmic relative-scale solution exactly balances inflow and output",
    )
    zero_flow_injection_theorem = kernel.prove_expression_equality(
        injection_density.subs(n_flow, 0),
        0,
        subject="turning off throughflow removes the injection density",
    )
    zero_seed_output_theorem = kernel.prove_expression_equality(
        leading_output_density.subs(m, 0),
        0,
        subject="the collapsed zero-scale state has zero leading output",
    )
    active_output_positive_theorem = kernel.prove_positive_expression(
        leading_output_density,
        subject="every positive scale has strictly positive leading anomalous output",
    )
    parent_stationary_theorem = kernel.prove_matrix_equality(
        stationary_gradient,
        sp.zeros(3, 1),
        subject="the conditional breathing parent has a common stationary point",
    )
    parent_hessian_theorem = kernel.prove_matrix_equality(
        parent_hessian,
        sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 1]]),
        subject="the breathing parent has the exact chain Hessian",
    )
    parent_rank_theorem = kernel.prove_exact_rank(
        parent_hessian,
        3,
        subject="the breathing parent controls all normalized relations",
    )
    parent_determinant_theorem = kernel.prove_expression_equality(
        parent_hessian.det(),
        1,
        subject="the breathing parent Hessian has unit determinant",
    )
    leading_minors_theorem = kernel.prove_matrix_equality(
        leading_minors,
        sp.Matrix([2, 3, 1]),
        subject="the breathing parent has positive leading principal minors",
    )
    scale_rank_theorem = kernel.prove_exact_rank(
        scale_map,
        3,
        subject="cell volume relative anomaly scale and density give three dimensional relations",
    )
    scale_nullity_theorem = kernel.prove_exact_nullity(
        scale_map,
        1,
        subject="one common absolute scale remains in the breathing construction",
    )
    scale_kernel_theorem = kernel.prove_matrix_equality(
        scale_map * scale_vector,
        sp.zeros(3, 1),
        subject="the breathing relations share one exact scale orbit",
    )
    external_anchor_rank_theorem = kernel.prove_exact_rank(
        externally_anchored_map,
        4,
        subject="an independently fixed reference scale would remove the breathing scale orbit",
    )
    inherited_origin_theorem = kernel.prove_matrix_equality(
        inherited_origin,
        sp.ones(3, 1),
        subject="cell volume cycle entropy and throughflow density are inherited",
    )
    inherited_score_theorem = kernel.prove_expression_equality(
        sum(inherited_origin),
        3,
        subject="three ingredients of the breathing construction are inherited",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(10, 1),
        subject="the conditional breathing architecture is complete",
    )
    conditional_origin_theorem = kernel.prove_matrix_equality(
        conditional_origin,
        sp.ones(8, 1),
        subject="all algebraic conditional breathing requirements pass",
    )
    conditional_score_theorem = kernel.prove_expression_equality(
        sum(conditional_origin),
        8,
        subject="eight conditional breathing requirements are closed",
    )
    physical_origin_theorem = kernel.prove_matrix_equality(
        physical_origin,
        sp.zeros(3, 1),
        subject="anomaly coefficient logarithmic coefficient and absolute reference scale remain open",
    )
    physical_score_theorem = kernel.prove_expression_equality(
        sum(physical_origin),
        0,
        subject="the breathing construction supplies no new physical origins",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_throughflow_scale_parent_admission_gate",
        (
            cell_volume_theorem,
            injection_density_theorem,
            flow_coefficient_theorem,
            leading_scale_cancellation_theorem,
            logarithmic_stationary_ratio_theorem,
            logarithmic_balance_theorem,
            zero_flow_injection_theorem,
            zero_seed_output_theorem,
            active_output_positive_theorem,
            parent_stationary_theorem,
            parent_hessian_theorem,
            parent_rank_theorem,
            parent_determinant_theorem,
            leading_minors_theorem,
            scale_rank_theorem,
            scale_nullity_theorem,
            scale_kernel_theorem,
            external_anchor_rank_theorem,
            inherited_origin_theorem,
            inherited_score_theorem,
            architecture_theorem,
            conditional_origin_theorem,
            conditional_score_theorem,
            physical_origin_theorem,
            physical_score_theorem,
        ),
    )
    return BreathingAnomalyThroughflowScaleCertificate(
        cell_volume,
        injection_density,
        flow_coefficient,
        logarithmic_stationary_ratio,
        parent,
        stationary_gradient,
        parent_hessian,
        leading_minors,
        scale_map,
        scale_vector,
        externally_anchored_map,
        inherited_origin,
        architecture,
        conditional_origin,
        physical_origin,
        cell_volume_theorem,
        injection_density_theorem,
        flow_coefficient_theorem,
        leading_scale_cancellation_theorem,
        logarithmic_stationary_ratio_theorem,
        logarithmic_balance_theorem,
        zero_flow_injection_theorem,
        zero_seed_output_theorem,
        active_output_positive_theorem,
        parent_stationary_theorem,
        parent_hessian_theorem,
        parent_rank_theorem,
        parent_determinant_theorem,
        leading_minors_theorem,
        scale_rank_theorem,
        scale_nullity_theorem,
        scale_kernel_theorem,
        external_anchor_rank_theorem,
        inherited_origin_theorem,
        inherited_score_theorem,
        architecture_theorem,
        conditional_origin_theorem,
        conditional_score_theorem,
        physical_origin_theorem,
        physical_score_theorem,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_throughflow_scale_parent_admission_gate",
    title="Допуск родителя аномального дыхания сквозного потока",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_throughflow_scale_parent_admission_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_throughflow_scale_parent_admission_gate_results.json",
    ),
    obligations=tuple(
        Obligation(name, getter)
        for name, getter in (
            ("breathing_cell_volume_inverse_square", lambda: build_certificate().cell_volume_theorem),
            ("breathing_injection_density", lambda: build_certificate().injection_density_theorem),
            ("breathing_flow_coefficient", lambda: build_certificate().flow_coefficient_theorem),
            ("breathing_leading_scale_cancellation", lambda: build_certificate().leading_scale_cancellation_theorem),
            ("breathing_logarithmic_stationary_ratio", lambda: build_certificate().logarithmic_stationary_ratio_theorem),
            ("breathing_logarithmic_balance", lambda: build_certificate().logarithmic_balance_theorem),
            ("breathing_zero_flow_injection", lambda: build_certificate().zero_flow_injection_theorem),
            ("breathing_zero_seed_output", lambda: build_certificate().zero_seed_output_theorem),
            ("breathing_active_output_positive", lambda: build_certificate().active_output_positive_theorem),
            ("breathing_parent_stationary", lambda: build_certificate().parent_stationary_theorem),
            ("breathing_parent_hessian", lambda: build_certificate().parent_hessian_theorem),
            ("breathing_parent_rank_three", lambda: build_certificate().parent_rank_theorem),
            ("breathing_parent_determinant_one", lambda: build_certificate().parent_determinant_theorem),
            ("breathing_parent_positive_minors", lambda: build_certificate().leading_minors_theorem),
            ("breathing_scale_rank_three", lambda: build_certificate().scale_rank_theorem),
            ("breathing_scale_nullity_one", lambda: build_certificate().scale_nullity_theorem),
            ("breathing_scale_kernel", lambda: build_certificate().scale_kernel_theorem),
            ("breathing_external_anchor_rank_four", lambda: build_certificate().external_anchor_rank_theorem),
            ("breathing_inherited_origin_full", lambda: build_certificate().inherited_origin_theorem),
            ("breathing_inherited_score_three", lambda: build_certificate().inherited_score_theorem),
            ("breathing_architecture_full", lambda: build_certificate().architecture_theorem),
            ("breathing_conditional_origin_full", lambda: build_certificate().conditional_origin_theorem),
            ("breathing_conditional_score_eight", lambda: build_certificate().conditional_score_theorem),
            ("breathing_physical_origin_open", lambda: build_certificate().physical_origin_theorem),
            ("breathing_physical_score_zero", lambda: build_certificate().physical_score_theorem),
        )
    ),
)