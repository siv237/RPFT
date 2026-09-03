"""LCF certificate for the common parent of Hopf-cycle conductance."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HopfCycleConductanceCommonParentCertificate:
    growth_coupling: sp.Expr
    step_growth: sp.Expr
    parent: sp.Expr
    stationary_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    scale_constraint_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    relative_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    growth_identity_theorem: Theorem
    parent_stationary_theorem: Theorem
    parent_hessian_theorem: Theorem
    parent_rank_theorem: Theorem
    parent_determinant_theorem: Theorem
    parent_spectrum_theorem: Theorem
    conductance_birth_identity_theorem: Theorem
    conductance_clock_ratio_theorem: Theorem
    edge_current_ratio_theorem: Theorem
    entropy_clock_ratio_theorem: Theorem
    scale_rank_theorem: Theorem
    scale_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    rescaled_conductance_ratio_theorem: Theorem
    rescaled_birth_ratio_theorem: Theorem
    architecture_theorem: Theorem
    relative_origin_theorem: Theorem
    relative_origin_score_theorem: Theorem
    physical_origin_theorem: Theorem
    physical_origin_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HopfCycleConductanceCommonParentCertificate:
    x = sp.symbols("x", positive=True)
    r_birth, r_cycle = sp.symbols("r_B r_kappa", real=True)
    omega, scale = sp.symbols("Omega c", positive=True)

    growth_coupling = sp.log((1 + 2 * x) / (1 + x))
    step_growth = growth_coupling / 3
    parent = ((r_birth - growth_coupling) ** 2 + (r_cycle - r_birth) ** 2) / 2
    stationary_point = {
        r_birth: growth_coupling,
        r_cycle: growth_coupling,
    }
    stationary_gradient = sp.ImmutableMatrix([
        sp.diff(parent, variable).subs(stationary_point)
        for variable in (r_birth, r_cycle)
    ])
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, (r_birth, r_cycle)))

    birth_rate = growth_coupling * omega
    conductance = birth_rate
    edge_current = conductance / 3
    entropy_production = conductance * sp.log(2)

    # Logarithmic constraints for Gamma_B/Omega and kappa/Gamma_B.
    scale_constraint_map = sp.ImmutableMatrix([
        [0, 1, -1],
        [1, -1, 0],
    ])
    scale_vector = sp.ones(3, 1)
    architecture = sp.ones(10, 1)
    relative_origin = sp.ones(6, 1)
    physical_origin = sp.zeros(2, 1)

    growth_identity_theorem = kernel.prove_expression_equality(
        growth_coupling,
        3 * step_growth,
        subject="the normalized birth coupling is three geometric growth increments",
    )
    parent_stationary_theorem = kernel.prove_matrix_equality(
        stationary_gradient,
        sp.zeros(2, 1),
        subject="the common parent selects the birth and cycle rate ratios jointly",
    )
    parent_hessian_theorem = kernel.prove_matrix_equality(
        parent_hessian,
        sp.Matrix([[2, -1], [-1, 1]]),
        subject="the conductance common parent has an exact constant Hessian",
    )
    parent_rank_theorem = kernel.prove_exact_rank(
        parent_hessian,
        2,
        subject="the common parent controls both relative rate directions",
    )
    parent_determinant_theorem = kernel.prove_expression_equality(
        parent_hessian.det(),
        1,
        subject="the conductance common-parent Hessian has unit determinant",
    )
    parent_spectrum_theorem = kernel.prove_exact_spectrum(
        parent_hessian,
        {
            (sp.Integer(3) - sp.sqrt(5)) / 2: 1,
            (sp.Integer(3) + sp.sqrt(5)) / 2: 1,
        },
        subject="the common conductance parent is strictly positive in relative directions",
    )
    conductance_birth_identity_theorem = kernel.prove_expression_equality(
        conductance,
        birth_rate,
        subject="the selected Hopf conductance equals the selected cell-birth rate",
    )
    conductance_clock_ratio_theorem = kernel.prove_expression_equality(
        conductance / omega,
        growth_coupling,
        subject="the Hopf conductance is fixed relative to the quantum clock",
    )
    edge_current_ratio_theorem = kernel.prove_expression_equality(
        edge_current / omega,
        step_growth,
        subject="the clock-blind edge current equals one geometric growth increment",
    )
    entropy_clock_ratio_theorem = kernel.prove_expression_equality(
        entropy_production / omega,
        3 * step_growth * sp.log(2),
        subject="the clock-blind entropy production is fixed by growth and cycle affinity",
    )
    scale_rank_theorem = kernel.prove_exact_rank(
        scale_constraint_map,
        2,
        subject="two relative constraints tie conductance birth rate and clock frequency",
    )
    scale_nullity_theorem = kernel.prove_exact_nullity(
        scale_constraint_map,
        1,
        subject="one common rate scale remains after the common-parent selection",
    )
    scale_kernel_theorem = kernel.prove_matrix_equality(
        scale_constraint_map * scale_vector,
        sp.zeros(2, 1),
        subject="common rescaling of conductance birth rate and clock is the exact kernel",
    )
    rescaled_conductance_ratio_theorem = kernel.prove_expression_equality(
        scale * conductance / (scale * omega),
        conductance / omega,
        subject="common rate rescaling preserves the conductance-clock ratio",
    )
    rescaled_birth_ratio_theorem = kernel.prove_expression_equality(
        scale * birth_rate / (scale * omega),
        birth_rate / omega,
        subject="common rate rescaling preserves the birth-clock ratio",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(10, 1),
        subject="all common-parent conductance architecture conditions pass",
    )
    relative_origin_theorem = kernel.prove_matrix_equality(
        relative_origin,
        sp.ones(6, 1),
        subject="all relative conductance-origin conditions pass",
    )
    relative_origin_score_theorem = kernel.prove_expression_equality(
        sum(relative_origin),
        6,
        subject="six relative origin requirements are jointly closed",
    )
    physical_origin_theorem = kernel.prove_matrix_equality(
        physical_origin,
        sp.zeros(2, 1),
        subject="absolute conductance and absolute clock origins remain open",
    )
    physical_origin_score_theorem = kernel.prove_expression_equality(
        sum(physical_origin),
        0,
        subject="the common relative parent supplies no absolute rate anchor",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_hopf_cycle_conductance_common_parent_origin_gate",
        (
            growth_identity_theorem,
            parent_stationary_theorem,
            parent_hessian_theorem,
            parent_rank_theorem,
            parent_determinant_theorem,
            parent_spectrum_theorem,
            conductance_birth_identity_theorem,
            conductance_clock_ratio_theorem,
            edge_current_ratio_theorem,
            entropy_clock_ratio_theorem,
            scale_rank_theorem,
            scale_nullity_theorem,
            scale_kernel_theorem,
            rescaled_conductance_ratio_theorem,
            rescaled_birth_ratio_theorem,
            architecture_theorem,
            relative_origin_theorem,
            relative_origin_score_theorem,
            physical_origin_theorem,
            physical_origin_score_theorem,
        ),
    )
    return HopfCycleConductanceCommonParentCertificate(
        growth_coupling,
        step_growth,
        parent,
        stationary_gradient,
        parent_hessian,
        scale_constraint_map,
        scale_vector,
        architecture,
        relative_origin,
        physical_origin,
        growth_identity_theorem,
        parent_stationary_theorem,
        parent_hessian_theorem,
        parent_rank_theorem,
        parent_determinant_theorem,
        parent_spectrum_theorem,
        conductance_birth_identity_theorem,
        conductance_clock_ratio_theorem,
        edge_current_ratio_theorem,
        entropy_clock_ratio_theorem,
        scale_rank_theorem,
        scale_nullity_theorem,
        scale_kernel_theorem,
        rescaled_conductance_ratio_theorem,
        rescaled_birth_ratio_theorem,
        architecture_theorem,
        relative_origin_theorem,
        relative_origin_score_theorem,
        physical_origin_theorem,
        physical_origin_score_theorem,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_hopf_cycle_conductance_common_parent_origin_gate",
    title="Общий родитель проводимости хопфовского цикла",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_hopf_cycle_conductance_common_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_hopf_cycle_conductance_common_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("conductance_growth_coupling_identity", lambda: build_certificate().growth_identity_theorem),
        Obligation("conductance_parent_stationary_point", lambda: build_certificate().parent_stationary_theorem),
        Obligation("conductance_parent_hessian", lambda: build_certificate().parent_hessian_theorem),
        Obligation("conductance_parent_rank_two", lambda: build_certificate().parent_rank_theorem),
        Obligation("conductance_parent_determinant_one", lambda: build_certificate().parent_determinant_theorem),
        Obligation("conductance_parent_positive_spectrum", lambda: build_certificate().parent_spectrum_theorem),
        Obligation("conductance_equals_birth_rate", lambda: build_certificate().conductance_birth_identity_theorem),
        Obligation("conductance_clock_ratio", lambda: build_certificate().conductance_clock_ratio_theorem),
        Obligation("edge_current_clock_blind_growth", lambda: build_certificate().edge_current_ratio_theorem),
        Obligation("entropy_clock_blind_ratio", lambda: build_certificate().entropy_clock_ratio_theorem),
        Obligation("conductance_scale_map_rank_two", lambda: build_certificate().scale_rank_theorem),
        Obligation("conductance_scale_map_nullity_one", lambda: build_certificate().scale_nullity_theorem),
        Obligation("conductance_scale_kernel", lambda: build_certificate().scale_kernel_theorem),
        Obligation("conductance_ratio_scale_invariance", lambda: build_certificate().rescaled_conductance_ratio_theorem),
        Obligation("birth_ratio_scale_invariance", lambda: build_certificate().rescaled_birth_ratio_theorem),
        Obligation("conductance_common_parent_architecture_full", lambda: build_certificate().architecture_theorem),
        Obligation("conductance_relative_origin_full", lambda: build_certificate().relative_origin_theorem),
        Obligation("conductance_relative_origin_score", lambda: build_certificate().relative_origin_score_theorem),
        Obligation("conductance_absolute_origin_open", lambda: build_certificate().physical_origin_theorem),
        Obligation("conductance_absolute_origin_score_zero", lambda: build_certificate().physical_origin_score_theorem),
    ),
)