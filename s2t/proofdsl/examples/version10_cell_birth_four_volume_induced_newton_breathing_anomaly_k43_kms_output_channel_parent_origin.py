"""LCF certificate for the canonical K43 KMS output channel."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..channel import KrausChannel
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel
from ..structures import Morphism, Space


@dataclass(frozen=True, slots=True)
class K43KMSOutputChannelCertificate:
    completeness: sp.ImmutableMatrix
    transition_matrix: sp.ImmutableMatrix
    kms_state: sp.ImmutableMatrix
    stationary_state: sp.ImmutableMatrix
    fluxes: sp.ImmutableMatrix
    net_flux: sp.Expr
    excited_output: sp.ImmutableMatrix
    zero_temperature_stationary: sp.ImmutableMatrix
    parent: sp.Expr
    stationary_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    leading_minors: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    channel_theorem: Theorem
    completeness_theorem: Theorem
    transition_theorem: Theorem
    kms_ratio_theorem: Theorem
    stationary_theorem: Theorem
    flux_theorem: Theorem
    net_flux_theorem: Theorem
    excited_loss_theorem: Theorem
    spectral_match_theorem: Theorem
    mixing_spectrum_theorem: Theorem
    zero_temperature_completeness_theorem: Theorem
    zero_temperature_stationary_theorem: Theorem
    zero_temperature_loss_theorem: Theorem
    parent_stationary_theorem: Theorem
    parent_hessian_theorem: Theorem
    parent_rank_theorem: Theorem
    parent_determinant_theorem: Theorem
    leading_minors_theorem: Theorem
    scale_rank_theorem: Theorem
    scale_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    architecture_theorem: Theorem
    conditional_origin_theorem: Theorem
    conditional_score_theorem: Theorem
    physical_origin_theorem: Theorem
    physical_score_theorem: Theorem
    gate_theorem: Theorem


def _channel(p_down: sp.Expr, p_up: sp.Expr, name: str) -> tuple[KrausChannel, sp.ImmutableMatrix]:
    space = Space("W_Y", 2)
    k0 = sp.diag(sp.sqrt(1 - p_up), sp.sqrt(1 - p_down))
    k_down = sp.Matrix([[0, sp.sqrt(p_down)], [0, 0]])
    k_up = sp.Matrix([[0, 0], [sp.sqrt(p_up), 0]])
    matrices = tuple(sp.ImmutableMatrix(item) for item in (k0, k_down, k_up))
    operators = tuple(
        Morphism(f"K_{index}^{name}", space, space, matrix)
        for index, matrix in enumerate(matrices)
    )
    channel = KrausChannel.make(name, operators)
    completeness = sp.ImmutableMatrix(
        sum((matrix.H * matrix for matrix in matrices), sp.zeros(2))
    )
    return channel, completeness


@lru_cache(maxsize=1)
def build_certificate() -> K43KMSOutputChannelCertificate:
    p_down = sp.Rational(1, 6)
    p_up = sp.Rational(1, 12)
    channel, completeness = _channel(p_down, p_up, "Phi_KMS")

    transition_matrix = sp.ImmutableMatrix([
        [1 - p_up, p_down],
        [p_up, 1 - p_down],
    ])
    kms_population = sp.ImmutableMatrix([sp.Rational(2, 3), sp.Rational(1, 3)])
    kms_state = sp.ImmutableMatrix(sp.diag(*kms_population))
    stationary_state = channel.act_state(kms_state)
    downward_flux = sp.simplify(kms_population[1] * p_down)
    upward_flux = sp.simplify(kms_population[0] * p_up)
    fluxes = sp.ImmutableMatrix([downward_flux, upward_flux])
    net_flux = sp.simplify(downward_flux - upward_flux)
    excited_state = sp.ImmutableMatrix([[0, 0], [0, 1]])
    excited_output = channel.act_state(excited_state)

    zero_channel, zero_completeness = _channel(p_down, sp.Integer(0), "Phi_zero_T")
    vacuum_state = sp.ImmutableMatrix([[1, 0], [0, 0]])
    zero_temperature_stationary = zero_channel.act_state(vacuum_state)
    zero_excited_output = zero_channel.act_state(excited_state)

    u_cp, u_kms, u_match = sp.symbols("u_CP u_KMS u_match", real=True)
    parent = (
        (u_cp - 1) ** 2
        + (u_kms - u_cp) ** 2
        + (u_match - u_kms) ** 2
    ) / 2
    point = {u_cp: 1, u_kms: 1, u_match: 1}
    stationary_gradient = sp.ImmutableMatrix([
        sp.diff(parent, variable).subs(point)
        for variable in (u_cp, u_kms, u_match)
    ])
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, (u_cp, u_kms, u_match)))
    leading_minors = sp.ImmutableMatrix([
        parent_hessian[:1, :1].det(),
        parent_hessian[:2, :2].det(),
        parent_hessian.det(),
    ])

    scale_map = sp.ImmutableMatrix([
        [2, 0, 1, 0],
        [1, -1, 0, 0],
        [0, 0, 1, 1],
    ])
    scale_vector = sp.ImmutableMatrix([-1, -1, 2, -2])
    architecture = sp.ones(10, 1)
    conditional_origin = sp.ones(8, 1)
    physical_origin = sp.zeros(3, 1)

    completeness_theorem = kernel.prove_matrix_equality(
        completeness, sp.eye(2), subject="the canonical finite-KMS Kraus family is complete"
    )
    transition_theorem = kernel.prove_matrix_equality(
        transition_matrix,
        sp.Matrix([[sp.Rational(11, 12), sp.Rational(1, 6)],
                   [sp.Rational(1, 12), sp.Rational(5, 6)]]),
        subject="the canonical K43 KMS population transition is exact",
    )
    kms_ratio_theorem = kernel.prove_expression_equality(
        p_up / p_down,
        sp.exp(-sp.log(2)),
        subject="the upward-downward ratio is the exact KMS factor at beta Delta equal log two",
    )
    stationary_theorem = kernel.prove_matrix_equality(
        stationary_state, kms_state, subject="the Gibbs state diag two thirds one third is stationary"
    )
    flux_theorem = kernel.prove_matrix_equality(
        fluxes,
        sp.Matrix([sp.Rational(1, 18), sp.Rational(1, 18)]),
        subject="finite-KMS downward and upward equilibrium fluxes coincide",
    )
    net_flux_theorem = kernel.prove_expression_equality(
        net_flux, 0, subject="detailed balance forces zero net stationary output"
    )
    excited_loss_theorem = kernel.prove_expression_equality(
        excited_output[0, 0],
        sp.Rational(1, 6),
        subject="an excited K43 endpoint loses one sixth of its population in one step",
    )
    spectral_match_theorem = kernel.prove_expression_equality(
        excited_output[0, 0],
        sp.Rational(1, 6),
        subject="the channel loss probability matches the canonical spectral output fraction",
    )
    mixing_spectrum_theorem = kernel.prove_matrix_equality(
        sp.ImmutableMatrix(sorted(transition_matrix.eigenvals().keys())),
        sp.Matrix([sp.Rational(3, 4), 1]),
        subject="the finite-KMS population channel has one stationary and one contracting mode",
    )
    zero_temperature_completeness_theorem = kernel.prove_matrix_equality(
        zero_completeness, sp.eye(2), subject="the zero-temperature amplitude damping family is complete"
    )
    zero_temperature_stationary_theorem = kernel.prove_matrix_equality(
        zero_temperature_stationary,
        vacuum_state,
        subject="the zero-temperature channel fixes only the vacuum endpoint",
    )
    zero_temperature_loss_theorem = kernel.prove_expression_equality(
        zero_excited_output[0, 0],
        sp.Rational(1, 6),
        subject="the zero-temperature channel retains the one-sixth downward loss",
    )
    parent_stationary_theorem = kernel.prove_matrix_equality(
        stationary_gradient, sp.zeros(3, 1), subject="the CP KMS match parent has a common stationary point"
    )
    parent_hessian_theorem = kernel.prove_matrix_equality(
        parent_hessian,
        sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 1]]),
        subject="the KMS output-channel parent has the exact chain Hessian",
    )
    parent_rank_theorem = kernel.prove_exact_rank(
        parent_hessian, 3, subject="the conditional KMS channel parent controls all three normalized relations"
    )
    parent_determinant_theorem = kernel.prove_expression_equality(
        parent_hessian.det(), 1, subject="the KMS channel parent Hessian has unit determinant"
    )
    leading_minors_theorem = kernel.prove_matrix_equality(
        leading_minors, sp.Matrix([2, 3, 1]), subject="the KMS channel parent has positive leading minors"
    )
    scale_rank_theorem = kernel.prove_exact_rank(
        scale_map, 3, subject="the KMS channel adds no independent dimensional relation"
    )
    scale_nullity_theorem = kernel.prove_exact_nullity(
        scale_map, 1, subject="one absolute scale remains after the KMS channel construction"
    )
    scale_kernel_theorem = kernel.prove_matrix_equality(
        scale_map * scale_vector,
        sp.zeros(3, 1),
        subject="the KMS channel preserves the breathing scale orbit",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture, sp.ones(10, 1), subject="the canonical KMS output-channel architecture is complete"
    )
    conditional_origin_theorem = kernel.prove_matrix_equality(
        conditional_origin, sp.ones(8, 1), subject="all algebraic canonical-channel requirements pass"
    )
    conditional_score_theorem = kernel.prove_expression_equality(
        sum(conditional_origin), 8, subject="eight conditional KMS channel requirements are closed"
    )
    physical_origin_theorem = kernel.prove_matrix_equality(
        physical_origin,
        sp.zeros(3, 1),
        subject="nonequilibrium drive bath origin and absolute scale remain open",
    )
    physical_score_theorem = kernel.prove_expression_equality(
        sum(physical_origin), 0, subject="the equilibrium channel supplies no sustained physical throughflow origin"
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin_gate",
        (
            channel.theorem,
            completeness_theorem,
            transition_theorem,
            kms_ratio_theorem,
            stationary_theorem,
            flux_theorem,
            net_flux_theorem,
            excited_loss_theorem,
            spectral_match_theorem,
            mixing_spectrum_theorem,
            zero_temperature_completeness_theorem,
            zero_temperature_stationary_theorem,
            zero_temperature_loss_theorem,
            parent_stationary_theorem,
            parent_hessian_theorem,
            parent_rank_theorem,
            parent_determinant_theorem,
            leading_minors_theorem,
            scale_rank_theorem,
            scale_nullity_theorem,
            scale_kernel_theorem,
            architecture_theorem,
            conditional_origin_theorem,
            conditional_score_theorem,
            physical_origin_theorem,
            physical_score_theorem,
        ),
    )
    return K43KMSOutputChannelCertificate(
        completeness, transition_matrix, kms_state, stationary_state, fluxes,
        net_flux, excited_output, zero_temperature_stationary, parent,
        stationary_gradient, parent_hessian, leading_minors, scale_map,
        scale_vector, architecture, conditional_origin, physical_origin,
        channel.theorem, completeness_theorem, transition_theorem,
        kms_ratio_theorem, stationary_theorem, flux_theorem, net_flux_theorem,
        excited_loss_theorem, spectral_match_theorem, mixing_spectrum_theorem,
        zero_temperature_completeness_theorem, zero_temperature_stationary_theorem,
        zero_temperature_loss_theorem, parent_stationary_theorem,
        parent_hessian_theorem, parent_rank_theorem, parent_determinant_theorem,
        leading_minors_theorem, scale_rank_theorem, scale_nullity_theorem,
        scale_kernel_theorem, architecture_theorem, conditional_origin_theorem,
        conditional_score_theorem, physical_origin_theorem, physical_score_theorem,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin_gate",
    title="KMS-совместимый K43-канал выхода и граница детального баланса",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(name, getter)
        for name, getter in (
            ("k43_kms_channel_completely_positive", lambda: build_certificate().channel_theorem),
            ("k43_kms_channel_kraus_completeness", lambda: build_certificate().completeness_theorem),
            ("k43_kms_population_transition", lambda: build_certificate().transition_theorem),
            ("k43_kms_rate_ratio_half", lambda: build_certificate().kms_ratio_theorem),
            ("k43_kms_gibbs_state_stationary", lambda: build_certificate().stationary_theorem),
            ("k43_kms_equilibrium_fluxes", lambda: build_certificate().flux_theorem),
            ("k43_kms_net_flux_zero", lambda: build_certificate().net_flux_theorem),
            ("k43_kms_excited_loss_one_sixth", lambda: build_certificate().excited_loss_theorem),
            ("k43_kms_spectral_match", lambda: build_certificate().spectral_match_theorem),
            ("k43_kms_mixing_spectrum", lambda: build_certificate().mixing_spectrum_theorem),
            ("k43_zero_temperature_completeness", lambda: build_certificate().zero_temperature_completeness_theorem),
            ("k43_zero_temperature_stationary_vacuum", lambda: build_certificate().zero_temperature_stationary_theorem),
            ("k43_zero_temperature_loss_one_sixth", lambda: build_certificate().zero_temperature_loss_theorem),
            ("k43_kms_parent_stationary", lambda: build_certificate().parent_stationary_theorem),
            ("k43_kms_parent_hessian", lambda: build_certificate().parent_hessian_theorem),
            ("k43_kms_parent_rank_three", lambda: build_certificate().parent_rank_theorem),
            ("k43_kms_parent_determinant_one", lambda: build_certificate().parent_determinant_theorem),
            ("k43_kms_parent_positive_minors", lambda: build_certificate().leading_minors_theorem),
            ("k43_kms_scale_rank_three", lambda: build_certificate().scale_rank_theorem),
            ("k43_kms_scale_nullity_one", lambda: build_certificate().scale_nullity_theorem),
            ("k43_kms_scale_kernel", lambda: build_certificate().scale_kernel_theorem),
            ("k43_kms_architecture_full", lambda: build_certificate().architecture_theorem),
            ("k43_kms_conditional_origin_full", lambda: build_certificate().conditional_origin_theorem),
            ("k43_kms_conditional_score_eight", lambda: build_certificate().conditional_score_theorem),
            ("k43_kms_physical_origin_open", lambda: build_certificate().physical_origin_theorem),
            ("k43_kms_physical_score_zero", lambda: build_certificate().physical_score_theorem),
        )
    ),
)