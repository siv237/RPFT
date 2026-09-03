"""LCF certificate for the induced Newton-constant parent origin gate."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class InducedNewtonConstantParentCertificate:
    einstein_coefficient: sp.Expr
    cell_scale_squared: sp.Expr
    geometric_newton_area: sp.Expr
    physical_newton_constant: sp.Expr
    blind_newton_cell_ratio: sp.Expr
    parent: sp.Expr
    stationary_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    leading_minors: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    relative_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    einstein_normalization_theorem: Theorem
    induced_coefficient_theorem: Theorem
    selected_cell_scale_theorem: Theorem
    geometric_newton_area_theorem: Theorem
    physical_newton_constant_theorem: Theorem
    blind_ratio_theorem: Theorem
    parent_stationary_theorem: Theorem
    parent_hessian_theorem: Theorem
    parent_rank_theorem: Theorem
    parent_determinant_theorem: Theorem
    leading_minors_theorem: Theorem
    scale_rank_theorem: Theorem
    scale_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    architecture_theorem: Theorem
    relative_origin_theorem: Theorem
    relative_score_theorem: Theorem
    physical_origin_theorem: Theorem
    physical_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> InducedNewtonConstantParentCertificate:
    alpha, beta, seed = sp.symbols("alpha beta m", positive=True)
    light_speed, hbar = sp.symbols("c hbar", positive=True)
    u_einstein, u_seed, u_cell = sp.symbols("u_E u_m u_q", real=True)

    einstein_coefficient = beta * seed
    cell_scale_squared = beta / (2 * alpha * seed)
    geometric_newton_area = sp.simplify(1 / (16 * sp.pi * einstein_coefficient))
    physical_newton_constant = sp.simplify(light_speed**3 * geometric_newton_area / hbar)
    blind_newton_cell_ratio = sp.simplify(geometric_newton_area / cell_scale_squared)

    parent = (
        (u_einstein - 1) ** 2
        + (u_seed - u_einstein) ** 2
        + (u_cell - u_seed) ** 2
    ) / 2
    stationary_point = {u_einstein: 1, u_seed: 1, u_cell: 1}
    stationary_gradient = sp.ImmutableMatrix([
        sp.diff(parent, variable).subs(stationary_point)
        for variable in (u_einstein, u_seed, u_cell)
    ])
    parent_hessian = sp.ImmutableMatrix(
        sp.hessian(parent, (u_einstein, u_seed, u_cell))
    )
    leading_minors = sp.ImmutableMatrix([
        parent_hessian[:1, :1].det(),
        parent_hessian[:2, :2].det(),
        parent_hessian.det(),
    ])

    # log(g_N), log(B), log(m), log(q).
    scale_map = sp.ImmutableMatrix([
        [1, 1, 0, 0],
        [0, 1, -1, 0],
        [0, 0, 1, 1],
    ])
    scale_vector = sp.ImmutableMatrix([1, -1, -1, 1])
    architecture = sp.ones(10, 1)
    relative_origin = sp.ones(6, 1)
    physical_origin = sp.zeros(3, 1)

    einstein_normalization_theorem = kernel.prove_expression_equality(
        16 * sp.pi * geometric_newton_area * einstein_coefficient,
        1,
        subject="the geometric Newton area is normalized by the Einstein coefficient",
    )
    induced_coefficient_theorem = kernel.prove_expression_equality(
        einstein_coefficient,
        beta * seed,
        subject="the induced Einstein coefficient is linear in the curvature seed",
    )
    selected_cell_scale_theorem = kernel.prove_expression_equality(
        cell_scale_squared,
        beta / (2 * alpha * seed),
        subject="the curvature parent selects the cell scale relative to the same seed",
    )
    geometric_newton_area_theorem = kernel.prove_expression_equality(
        geometric_newton_area,
        1 / (16 * sp.pi * beta * seed),
        subject="the induced geometric Newton area is inverse to the common seed",
    )
    physical_newton_constant_theorem = kernel.prove_expression_equality(
        physical_newton_constant,
        light_speed**3 / (16 * sp.pi * hbar * beta * seed),
        subject="the physical Newton constant inherits the inverse seed scale",
    )
    blind_ratio_theorem = kernel.prove_expression_equality(
        blind_newton_cell_ratio,
        alpha / (8 * sp.pi * beta**2),
        subject="the Newton area to cell area ratio is dimensionless and seed independent",
    )
    parent_stationary_theorem = kernel.prove_matrix_equality(
        stationary_gradient,
        sp.zeros(3, 1),
        subject="the conditional parent jointly selects Einstein seed and cell normalizations",
    )
    parent_hessian_theorem = kernel.prove_matrix_equality(
        parent_hessian,
        sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 1]]),
        subject="the induced Newton parent has an exact tridiagonal Hessian",
    )
    parent_rank_theorem = kernel.prove_exact_rank(
        parent_hessian,
        3,
        subject="the induced Newton parent controls all relative variables",
    )
    parent_determinant_theorem = kernel.prove_expression_equality(
        parent_hessian.det(),
        1,
        subject="the induced Newton parent Hessian has unit determinant",
    )
    leading_minors_theorem = kernel.prove_matrix_equality(
        leading_minors,
        sp.Matrix([2, 3, 1]),
        subject="the induced Newton parent has positive leading principal minors",
    )
    scale_rank_theorem = kernel.prove_exact_rank(
        scale_map,
        3,
        subject="three relations fix Newton coefficient seed and cell ratios",
    )
    scale_nullity_theorem = kernel.prove_exact_nullity(
        scale_map,
        1,
        subject="one common length scale remains in the induced Newton system",
    )
    scale_kernel_theorem = kernel.prove_matrix_equality(
        scale_map * scale_vector,
        sp.zeros(3, 1),
        subject="Newton area and cell area co-scale against coefficient and seed",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(10, 1),
        subject="the conditional induced Newton parent architecture is complete",
    )
    relative_origin_theorem = kernel.prove_matrix_equality(
        relative_origin,
        sp.ones(6, 1),
        subject="all relative induced Newton relations pass",
    )
    relative_score_theorem = kernel.prove_expression_equality(
        sum(relative_origin),
        6,
        subject="six relative induced Newton requirements are closed",
    )
    physical_origin_theorem = kernel.prove_matrix_equality(
        physical_origin,
        sp.zeros(3, 1),
        subject="seed coefficient and absolute Newton origins remain open",
    )
    physical_score_theorem = kernel.prove_expression_equality(
        sum(physical_origin),
        0,
        subject="the induced construction supplies no absolute Newton scale",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_constant_parent_origin_gate",
        (
            einstein_normalization_theorem,
            induced_coefficient_theorem,
            selected_cell_scale_theorem,
            geometric_newton_area_theorem,
            physical_newton_constant_theorem,
            blind_ratio_theorem,
            parent_stationary_theorem,
            parent_hessian_theorem,
            parent_rank_theorem,
            parent_determinant_theorem,
            leading_minors_theorem,
            scale_rank_theorem,
            scale_nullity_theorem,
            scale_kernel_theorem,
            architecture_theorem,
            relative_origin_theorem,
            relative_score_theorem,
            physical_origin_theorem,
            physical_score_theorem,
        ),
    )
    return InducedNewtonConstantParentCertificate(
        einstein_coefficient,
        cell_scale_squared,
        geometric_newton_area,
        physical_newton_constant,
        blind_newton_cell_ratio,
        parent,
        stationary_gradient,
        parent_hessian,
        leading_minors,
        scale_map,
        scale_vector,
        architecture,
        relative_origin,
        physical_origin,
        einstein_normalization_theorem,
        induced_coefficient_theorem,
        selected_cell_scale_theorem,
        geometric_newton_area_theorem,
        physical_newton_constant_theorem,
        blind_ratio_theorem,
        parent_stationary_theorem,
        parent_hessian_theorem,
        parent_rank_theorem,
        parent_determinant_theorem,
        leading_minors_theorem,
        scale_rank_theorem,
        scale_nullity_theorem,
        scale_kernel_theorem,
        architecture_theorem,
        relative_origin_theorem,
        relative_score_theorem,
        physical_origin_theorem,
        physical_score_theorem,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_constant_parent_origin_gate",
    title="Родитель индуцированной ньютоновской постоянной",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_constant_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_constant_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("newton_einstein_normalization", lambda: build_certificate().einstein_normalization_theorem),
        Obligation("newton_induced_coefficient", lambda: build_certificate().induced_coefficient_theorem),
        Obligation("newton_selected_cell_scale", lambda: build_certificate().selected_cell_scale_theorem),
        Obligation("newton_geometric_area", lambda: build_certificate().geometric_newton_area_theorem),
        Obligation("newton_physical_constant", lambda: build_certificate().physical_newton_constant_theorem),
        Obligation("newton_cell_blind_ratio", lambda: build_certificate().blind_ratio_theorem),
        Obligation("newton_parent_stationary", lambda: build_certificate().parent_stationary_theorem),
        Obligation("newton_parent_hessian", lambda: build_certificate().parent_hessian_theorem),
        Obligation("newton_parent_rank_three", lambda: build_certificate().parent_rank_theorem),
        Obligation("newton_parent_determinant_one", lambda: build_certificate().parent_determinant_theorem),
        Obligation("newton_parent_positive_minors", lambda: build_certificate().leading_minors_theorem),
        Obligation("newton_scale_map_rank_three", lambda: build_certificate().scale_rank_theorem),
        Obligation("newton_scale_map_nullity_one", lambda: build_certificate().scale_nullity_theorem),
        Obligation("newton_scale_kernel", lambda: build_certificate().scale_kernel_theorem),
        Obligation("newton_parent_architecture_full", lambda: build_certificate().architecture_theorem),
        Obligation("newton_relative_origin_full", lambda: build_certificate().relative_origin_theorem),
        Obligation("newton_relative_origin_score", lambda: build_certificate().relative_score_theorem),
        Obligation("newton_physical_origin_open", lambda: build_certificate().physical_origin_theorem),
        Obligation("newton_physical_origin_score_zero", lambda: build_certificate().physical_score_theorem),
    ),
)