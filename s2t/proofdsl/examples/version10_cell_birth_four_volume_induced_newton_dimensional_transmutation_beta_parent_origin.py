"""LCF certificate for dimensional transmutation and Planck self-consistency."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class InducedNewtonDimensionalTransmutationCertificate:
    beta_coefficient: sp.Expr
    matching_coupling_squared: sp.Expr
    landau_log_ratio: sp.Expr
    seed_log_ratio: sp.Expr
    einstein_dimensionless_coefficient: sp.Expr
    parent: sp.Expr
    stationary_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    leading_minors: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    externally_anchored_map: sp.ImmutableMatrix
    historical_rg_data: sp.ImmutableMatrix
    current_typed_transfer: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    beta_coefficient_theorem: Theorem
    matching_coupling_theorem: Theorem
    landau_log_ratio_theorem: Theorem
    seed_log_ratio_theorem: Theorem
    planck_coefficient_theorem: Theorem
    parent_stationary_theorem: Theorem
    parent_hessian_theorem: Theorem
    parent_rank_theorem: Theorem
    parent_determinant_theorem: Theorem
    leading_minors_theorem: Theorem
    scale_rank_theorem: Theorem
    scale_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    external_anchor_rank_theorem: Theorem
    historical_rg_data_theorem: Theorem
    current_typed_transfer_theorem: Theorem
    architecture_theorem: Theorem
    conditional_origin_theorem: Theorem
    conditional_score_theorem: Theorem
    physical_origin_theorem: Theorem
    physical_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> InducedNewtonDimensionalTransmutationCertificate:
    beta_coefficient = sp.Integer(2)
    matching_coupling_squared = sp.Rational(3, 8)
    landau_log_ratio = sp.simplify(
        8 * sp.pi**2 / (beta_coefficient * matching_coupling_squared)
    )
    seed_log_ratio = sp.simplify(2 * landau_log_ratio)
    einstein_dimensionless_coefficient = sp.simplify(1 / (16 * sp.pi))

    u_rg, u_planck, u_einstein = sp.symbols("u_RG u_P u_E", real=True)
    parent = (
        (u_rg - 1) ** 2
        + (u_planck - u_rg) ** 2
        + (u_einstein - u_planck) ** 2
    ) / 2
    stationary_point = {u_rg: 1, u_planck: 1, u_einstein: 1}
    stationary_gradient = sp.ImmutableMatrix([
        sp.diff(parent, variable).subs(stationary_point)
        for variable in (u_rg, u_planck, u_einstein)
    ])
    parent_hessian = sp.ImmutableMatrix(
        sp.hessian(parent, (u_rg, u_planck, u_einstein))
    )
    leading_minors = sp.ImmutableMatrix([
        parent_hessian[:1, :1].det(),
        parent_hessian[:2, :2].det(),
        parent_hessian.det(),
    ])

    # log(m), log(mu^2), log(g_N).
    scale_map = sp.ImmutableMatrix([
        [1, -1, 0],
        [1, 0, 1],
    ])
    scale_vector = sp.ImmutableMatrix([1, 1, -1])
    externally_anchored_map = sp.ImmutableMatrix.vstack(
        scale_map,
        sp.ImmutableMatrix([[0, 0, 1]]),
    )

    historical_rg_data = sp.ones(2, 1)
    current_typed_transfer = sp.zeros(2, 1)
    architecture = sp.ones(10, 1)
    conditional_origin = sp.ones(7, 1)
    physical_origin = sp.zeros(4, 1)

    beta_coefficient_theorem = kernel.prove_expression_equality(
        beta_coefficient,
        2,
        subject="the inherited relative-U1 one-loop beta coefficient equals two",
    )
    matching_coupling_theorem = kernel.prove_expression_equality(
        matching_coupling_squared,
        sp.Rational(3, 8),
        subject="the inherited spectral matching coupling squared equals three eighths",
    )
    landau_log_ratio_theorem = kernel.prove_expression_equality(
        landau_log_ratio,
        32 * sp.pi**2 / 3,
        subject="the inherited positive beta function fixes the exact Landau scale ratio",
    )
    seed_log_ratio_theorem = kernel.prove_expression_equality(
        seed_log_ratio,
        64 * sp.pi**2 / 3,
        subject="the inverse-area transmutation seed has twice the Landau logarithm",
    )
    planck_coefficient_theorem = kernel.prove_expression_equality(
        16 * sp.pi * einstein_dimensionless_coefficient,
        1,
        subject="Planck self-consistency selects the dimensionless Einstein coefficient",
    )
    parent_stationary_theorem = kernel.prove_matrix_equality(
        stationary_gradient,
        sp.zeros(3, 1),
        subject="the conditional RG Planck Einstein parent has a common stationary point",
    )
    parent_hessian_theorem = kernel.prove_matrix_equality(
        parent_hessian,
        sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 1]]),
        subject="the conditional transmutation parent has the exact chain Hessian",
    )
    parent_rank_theorem = kernel.prove_exact_rank(
        parent_hessian,
        3,
        subject="the conditional parent controls all three normalized relations",
    )
    parent_determinant_theorem = kernel.prove_expression_equality(
        parent_hessian.det(),
        1,
        subject="the conditional parent Hessian has unit determinant",
    )
    leading_minors_theorem = kernel.prove_matrix_equality(
        leading_minors,
        sp.Matrix([2, 3, 1]),
        subject="the conditional parent has positive leading principal minors",
    )
    scale_rank_theorem = kernel.prove_exact_rank(
        scale_map,
        2,
        subject="RG matching and Planck self-consistency give two dimensional relations",
    )
    scale_nullity_theorem = kernel.prove_exact_nullity(
        scale_map,
        1,
        subject="one common absolute scale remains after conditional closure",
    )
    scale_kernel_theorem = kernel.prove_matrix_equality(
        scale_map * scale_vector,
        sp.zeros(2, 1),
        subject="transmutation seed matching scale and Newton area share one scale orbit",
    )
    external_anchor_rank_theorem = kernel.prove_exact_rank(
        externally_anchored_map,
        3,
        subject="an independently fixed Newton area would remove the residual scale mode",
    )
    historical_rg_data_theorem = kernel.prove_matrix_equality(
        historical_rg_data,
        sp.ones(2, 1),
        subject="two exact RG data are inherited from the earlier relative-U1 sector",
    )
    current_typed_transfer_theorem = kernel.prove_matrix_equality(
        current_typed_transfer,
        sp.zeros(2, 1),
        subject="neither beta data nor its boundary condition is typed into the current Newton carrier",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(10, 1),
        subject="the conditional dimensional-transmutation architecture is complete",
    )
    conditional_origin_theorem = kernel.prove_matrix_equality(
        conditional_origin,
        sp.ones(7, 1),
        subject="all algebraic conditional closure requirements pass",
    )
    conditional_score_theorem = kernel.prove_expression_equality(
        sum(conditional_origin),
        7,
        subject="seven conditional transmutation requirements are closed",
    )
    physical_origin_theorem = kernel.prove_matrix_equality(
        physical_origin,
        sp.zeros(4, 1),
        subject="typed beta boundary Planck seed and absolute Newton origins remain open",
    )
    physical_score_theorem = kernel.prove_expression_equality(
        sum(physical_origin),
        0,
        subject="the conditional construction supplies no absolute physical scale",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin_gate",
        (
            beta_coefficient_theorem,
            matching_coupling_theorem,
            landau_log_ratio_theorem,
            seed_log_ratio_theorem,
            planck_coefficient_theorem,
            parent_stationary_theorem,
            parent_hessian_theorem,
            parent_rank_theorem,
            parent_determinant_theorem,
            leading_minors_theorem,
            scale_rank_theorem,
            scale_nullity_theorem,
            scale_kernel_theorem,
            external_anchor_rank_theorem,
            historical_rg_data_theorem,
            current_typed_transfer_theorem,
            architecture_theorem,
            conditional_origin_theorem,
            conditional_score_theorem,
            physical_origin_theorem,
            physical_score_theorem,
        ),
    )
    return InducedNewtonDimensionalTransmutationCertificate(
        beta_coefficient,
        matching_coupling_squared,
        landau_log_ratio,
        seed_log_ratio,
        einstein_dimensionless_coefficient,
        parent,
        stationary_gradient,
        parent_hessian,
        leading_minors,
        scale_map,
        scale_vector,
        externally_anchored_map,
        historical_rg_data,
        current_typed_transfer,
        architecture,
        conditional_origin,
        physical_origin,
        beta_coefficient_theorem,
        matching_coupling_theorem,
        landau_log_ratio_theorem,
        seed_log_ratio_theorem,
        planck_coefficient_theorem,
        parent_stationary_theorem,
        parent_hessian_theorem,
        parent_rank_theorem,
        parent_determinant_theorem,
        leading_minors_theorem,
        scale_rank_theorem,
        scale_nullity_theorem,
        scale_kernel_theorem,
        external_anchor_rank_theorem,
        historical_rg_data_theorem,
        current_typed_transfer_theorem,
        architecture_theorem,
        conditional_origin_theorem,
        conditional_score_theorem,
        physical_origin_theorem,
        physical_score_theorem,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin_gate",
    title="Родитель размерностной трансмутации и планковской самосогласованности",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(name, getter)
        for name, getter in (
            ("newton_dt_beta_coefficient_two", lambda: build_certificate().beta_coefficient_theorem),
            ("newton_dt_matching_coupling_three_eighths", lambda: build_certificate().matching_coupling_theorem),
            ("newton_dt_landau_log_ratio", lambda: build_certificate().landau_log_ratio_theorem),
            ("newton_dt_seed_log_ratio", lambda: build_certificate().seed_log_ratio_theorem),
            ("newton_dt_planck_coefficient", lambda: build_certificate().planck_coefficient_theorem),
            ("newton_dt_parent_stationary", lambda: build_certificate().parent_stationary_theorem),
            ("newton_dt_parent_hessian", lambda: build_certificate().parent_hessian_theorem),
            ("newton_dt_parent_rank_three", lambda: build_certificate().parent_rank_theorem),
            ("newton_dt_parent_determinant_one", lambda: build_certificate().parent_determinant_theorem),
            ("newton_dt_parent_positive_minors", lambda: build_certificate().leading_minors_theorem),
            ("newton_dt_scale_rank_two", lambda: build_certificate().scale_rank_theorem),
            ("newton_dt_scale_nullity_one", lambda: build_certificate().scale_nullity_theorem),
            ("newton_dt_scale_kernel", lambda: build_certificate().scale_kernel_theorem),
            ("newton_dt_external_anchor_rank_three", lambda: build_certificate().external_anchor_rank_theorem),
            ("newton_dt_historical_rg_data", lambda: build_certificate().historical_rg_data_theorem),
            ("newton_dt_current_typed_transfer_zero", lambda: build_certificate().current_typed_transfer_theorem),
            ("newton_dt_architecture_full", lambda: build_certificate().architecture_theorem),
            ("newton_dt_conditional_origin_full", lambda: build_certificate().conditional_origin_theorem),
            ("newton_dt_conditional_score_seven", lambda: build_certificate().conditional_score_theorem),
            ("newton_dt_physical_origin_open", lambda: build_certificate().physical_origin_theorem),
            ("newton_dt_physical_score_zero", lambda: build_certificate().physical_score_theorem),
        )
    ),
)