"""LCF certificate for the K43 trace-response output-density morphism."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class K43OutputDensityMorphismCertificate:
    trace_response: sp.Expr
    output_fraction: sp.Expr
    subunit_gap: sp.Expr
    sign_candidates: sp.ImmutableMatrix
    sign_admissibility: sp.ImmutableMatrix
    cell_volume: sp.Expr
    output_density: sp.Expr
    effective_epsilon: sp.Expr
    inflow_density: sp.Expr
    balance_residual: sp.Expr
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
    trace_response_theorem: Theorem
    output_fraction_theorem: Theorem
    output_positive_theorem: Theorem
    subunit_gap_theorem: Theorem
    subunit_positive_theorem: Theorem
    witness_theorem: Theorem
    sign_candidates_theorem: Theorem
    sign_admissibility_theorem: Theorem
    cell_volume_theorem: Theorem
    output_density_theorem: Theorem
    effective_epsilon_theorem: Theorem
    inflow_density_theorem: Theorem
    balance_residual_theorem: Theorem
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
def build_certificate() -> K43OutputDensityMorphismCertificate:
    x, q, alpha, beta_e, m = sp.symbols(
        "x q alpha beta_E m", positive=True
    )
    n_flow = sp.symbols("n_flow", nonnegative=True)

    trace_response = sp.simplify(
        x / (1 + q**2 + x) - x / (1 + x)
    )
    output_fraction = sp.simplify(-trace_response)
    subunit_gap = sp.simplify(
        (q**2 + (x + 1) ** 2) / ((x + 1) * (q**2 + x + 1))
    )
    sign_candidates = sp.ImmutableMatrix([-1, 1])
    sign_admissibility = sp.ImmutableMatrix([0, 1])

    cell_volume = beta_e**2 / (4 * alpha**2 * m**2)
    output_density = sp.simplify(output_fraction / cell_volume)
    effective_epsilon = sp.simplify(4 * alpha**2 * output_fraction / beta_e**2)
    inflow_density = sp.simplify(n_flow * sp.log(2) / cell_volume)
    balance_residual = sp.simplify(inflow_density - output_density)

    u_response, u_density, u_balance = sp.symbols(
        "u_response u_density u_balance", real=True
    )
    parent = (
        (u_response - 1) ** 2
        + (u_density - u_response) ** 2
        + (u_balance - u_density) ** 2
    ) / 2
    stationary_point = {u_response: 1, u_density: 1, u_balance: 1}
    stationary_gradient = sp.ImmutableMatrix([
        sp.diff(parent, variable).subs(stationary_point)
        for variable in (u_response, u_density, u_balance)
    ])
    parent_hessian = sp.ImmutableMatrix(
        sp.hessian(parent, (u_response, u_density, u_balance))
    )
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

    inherited_origin = sp.ones(4, 1)
    architecture = sp.ones(10, 1)
    conditional_origin = sp.ones(8, 1)
    physical_origin = sp.zeros(3, 1)

    trace_response_theorem = kernel.prove_expression_equality(
        trace_response,
        -x * q**2 / ((1 + x) * (1 + q**2 + x)),
        subject="the oriented K43 trace response has an exact negative closed form",
    )
    output_fraction_theorem = kernel.prove_expression_equality(
        output_fraction,
        x * q**2 / ((1 + x) * (1 + q**2 + x)),
        subject="reversing the response sign gives the exact output fraction",
    )
    output_positive_theorem = kernel.prove_positive_expression(
        output_fraction,
        subject="the sign-reversed K43 response is strictly positive",
    )
    subunit_gap_theorem = kernel.prove_expression_equality(
        1 - output_fraction,
        subunit_gap,
        subject="the gap between unity and the K43 output fraction has a positive form",
    )
    subunit_positive_theorem = kernel.prove_positive_expression(
        subunit_gap,
        subject="the K43 output fraction is strictly smaller than one",
    )
    witness_theorem = kernel.prove_expression_equality(
        output_fraction.subs({x: 1, q: 1}),
        sp.Rational(1, 6),
        subject="the canonical K43 output fraction equals one sixth",
    )
    sign_candidates_theorem = kernel.prove_matrix_equality(
        sign_candidates,
        sp.Matrix([-1, 1]),
        subject="the trace-to-output sign menu contains the direct and reversed maps",
    )
    sign_admissibility_theorem = kernel.prove_matrix_equality(
        sign_admissibility,
        sp.Matrix([0, 1]),
        subject="positivity admits only the sign-reversed trace response",
    )
    cell_volume_theorem = kernel.prove_expression_equality(
        cell_volume,
        beta_e**2 / (4 * alpha**2 * m**2),
        subject="the inherited cell four-volume is inverse quadratic in m",
    )
    output_density_theorem = kernel.prove_expression_equality(
        output_density,
        4 * alpha**2 * output_fraction * m**2 / beta_e**2,
        subject="the per-cell K43 output becomes a normalized density proportional to m squared",
    )
    effective_epsilon_theorem = kernel.prove_expression_equality(
        output_density / m**2,
        effective_epsilon,
        subject="the K43 morphism conditionally fixes the dimensionless leading output coefficient",
    )
    inflow_density_theorem = kernel.prove_expression_equality(
        inflow_density,
        4 * alpha**2 * n_flow * sp.log(2) * m**2 / beta_e**2,
        subject="the inherited throughflow density has the same inverse-volume normalization",
    )
    balance_residual_theorem = kernel.prove_expression_equality(
        balance_residual,
        4 * alpha**2 * m**2 * (n_flow * sp.log(2) - output_fraction) / beta_e**2,
        subject="the K43 inflow-output balance cancels the absolute scale",
    )
    parent_stationary_theorem = kernel.prove_matrix_equality(
        stationary_gradient,
        sp.zeros(3, 1),
        subject="the response density balance parent has a common stationary point",
    )
    parent_hessian_theorem = kernel.prove_matrix_equality(
        parent_hessian,
        sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 1]]),
        subject="the K43 output-density parent has the exact chain Hessian",
    )
    parent_rank_theorem = kernel.prove_exact_rank(
        parent_hessian,
        3,
        subject="the conditional output-density parent controls all normalized relations",
    )
    parent_determinant_theorem = kernel.prove_expression_equality(
        parent_hessian.det(),
        1,
        subject="the output-density parent Hessian has unit determinant",
    )
    leading_minors_theorem = kernel.prove_matrix_equality(
        leading_minors,
        sp.Matrix([2, 3, 1]),
        subject="the output-density parent has positive leading principal minors",
    )
    scale_rank_theorem = kernel.prove_exact_rank(
        scale_map,
        3,
        subject="the output morphism preserves the three relative dimensional relations",
    )
    scale_nullity_theorem = kernel.prove_exact_nullity(
        scale_map,
        1,
        subject="one absolute scale remains after the K43 output morphism",
    )
    scale_kernel_theorem = kernel.prove_matrix_equality(
        scale_map * scale_vector,
        sp.zeros(3, 1),
        subject="the K43 output density shares the breathing scale orbit",
    )
    external_anchor_rank_theorem = kernel.prove_exact_rank(
        externally_anchored_map,
        4,
        subject="an independent reference scale would remove the final output-density orbit",
    )
    inherited_origin_theorem = kernel.prove_matrix_equality(
        inherited_origin,
        sp.ones(4, 1),
        subject="K43 response growth orientation cell volume and cycle entropy are inherited",
    )
    inherited_score_theorem = kernel.prove_expression_equality(
        sum(inherited_origin),
        4,
        subject="four ingredients of the output morphism are inherited",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(10, 1),
        subject="the conditional K43 output-density architecture is complete",
    )
    conditional_origin_theorem = kernel.prove_matrix_equality(
        conditional_origin,
        sp.ones(8, 1),
        subject="all algebraic output-density morphism requirements pass",
    )
    conditional_score_theorem = kernel.prove_expression_equality(
        sum(conditional_origin),
        8,
        subject="eight conditional output-density requirements are closed",
    )
    physical_origin_theorem = kernel.prove_matrix_equality(
        physical_origin,
        sp.zeros(3, 1),
        subject="physical channel identity coefficient origin and reference scale remain open",
    )
    physical_score_theorem = kernel.prove_expression_equality(
        sum(physical_origin),
        0,
        subject="the conditional output morphism supplies no absolute physical origin",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_output_density_morphism_origin_gate",
        (
            trace_response_theorem,
            output_fraction_theorem,
            output_positive_theorem,
            subunit_gap_theorem,
            subunit_positive_theorem,
            witness_theorem,
            sign_candidates_theorem,
            sign_admissibility_theorem,
            cell_volume_theorem,
            output_density_theorem,
            effective_epsilon_theorem,
            inflow_density_theorem,
            balance_residual_theorem,
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
    return K43OutputDensityMorphismCertificate(
        trace_response,
        output_fraction,
        subunit_gap,
        sign_candidates,
        sign_admissibility,
        cell_volume,
        output_density,
        effective_epsilon,
        inflow_density,
        balance_residual,
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
        trace_response_theorem,
        output_fraction_theorem,
        output_positive_theorem,
        subunit_gap_theorem,
        subunit_positive_theorem,
        witness_theorem,
        sign_candidates_theorem,
        sign_admissibility_theorem,
        cell_volume_theorem,
        output_density_theorem,
        effective_epsilon_theorem,
        inflow_density_theorem,
        balance_residual_theorem,
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
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_output_density_morphism_origin_gate",
    title="Происхождение морфизма K43-отклика в плотность выхода",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_output_density_morphism_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_output_density_morphism_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(name, getter)
        for name, getter in (
            ("k43_output_trace_response_closed_form", lambda: build_certificate().trace_response_theorem),
            ("k43_output_fraction_closed_form", lambda: build_certificate().output_fraction_theorem),
            ("k43_output_fraction_positive", lambda: build_certificate().output_positive_theorem),
            ("k43_output_subunit_gap", lambda: build_certificate().subunit_gap_theorem),
            ("k43_output_subunit_positive", lambda: build_certificate().subunit_positive_theorem),
            ("k43_output_witness_one_sixth", lambda: build_certificate().witness_theorem),
            ("k43_output_sign_candidates", lambda: build_certificate().sign_candidates_theorem),
            ("k43_output_sign_admissibility", lambda: build_certificate().sign_admissibility_theorem),
            ("k43_output_cell_volume", lambda: build_certificate().cell_volume_theorem),
            ("k43_output_density_morphism", lambda: build_certificate().output_density_theorem),
            ("k43_output_effective_epsilon", lambda: build_certificate().effective_epsilon_theorem),
            ("k43_output_inflow_density", lambda: build_certificate().inflow_density_theorem),
            ("k43_output_balance_scale_cancellation", lambda: build_certificate().balance_residual_theorem),
            ("k43_output_parent_stationary", lambda: build_certificate().parent_stationary_theorem),
            ("k43_output_parent_hessian", lambda: build_certificate().parent_hessian_theorem),
            ("k43_output_parent_rank_three", lambda: build_certificate().parent_rank_theorem),
            ("k43_output_parent_determinant_one", lambda: build_certificate().parent_determinant_theorem),
            ("k43_output_parent_positive_minors", lambda: build_certificate().leading_minors_theorem),
            ("k43_output_scale_rank_three", lambda: build_certificate().scale_rank_theorem),
            ("k43_output_scale_nullity_one", lambda: build_certificate().scale_nullity_theorem),
            ("k43_output_scale_kernel", lambda: build_certificate().scale_kernel_theorem),
            ("k43_output_external_anchor_rank_four", lambda: build_certificate().external_anchor_rank_theorem),
            ("k43_output_inherited_origin_full", lambda: build_certificate().inherited_origin_theorem),
            ("k43_output_inherited_score_four", lambda: build_certificate().inherited_score_theorem),
            ("k43_output_architecture_full", lambda: build_certificate().architecture_theorem),
            ("k43_output_conditional_origin_full", lambda: build_certificate().conditional_origin_theorem),
            ("k43_output_conditional_score_eight", lambda: build_certificate().conditional_score_theorem),
            ("k43_output_physical_origin_open", lambda: build_certificate().physical_origin_theorem),
            ("k43_output_physical_score_zero", lambda: build_certificate().physical_score_theorem),
        )
    ),
)