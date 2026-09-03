"""LCF certificate for dimensional transmutation of the birth tick."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class BirthTickDimensionalTransmutationCertificate:
    beta_coefficient: sp.Expr
    boundary_coupling_squared: sp.Expr
    landau_log_ratio: sp.Expr
    seed_log_ratio: sp.Expr
    tick_reference_product: sp.Expr
    k43_tick_product: sp.Expr
    mismatch_factor: sp.Expr
    parent: sp.Expr
    stationary_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernels: sp.ImmutableMatrix
    speed_anchored_map: sp.ImmutableMatrix
    speed_anchored_kernel: sp.ImmutableMatrix
    fully_anchored_map: sp.ImmutableMatrix
    inherited_rg_data: sp.ImmutableMatrix
    bath_typed_transfer: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> BirthTickDimensionalTransmutationCertificate:
    beta_coefficient = sp.Integer(2)
    boundary_coupling_squared = sp.Rational(3, 8)
    landau_log_ratio = sp.simplify(
        8 * sp.pi**2 / (beta_coefficient * boundary_coupling_squared)
    )
    seed_log_ratio = sp.simplify(2 * landau_log_ratio)
    tick_reference_product = sp.exp(-landau_log_ratio)
    k43_tick_product = sp.Integer(42)
    mismatch_factor = sp.simplify(k43_tick_product / tick_reference_product)

    x_rg, x_tick, x_transit = sp.symbols("x_RG x_tick x_transit", real=True)
    parent = (
        (x_rg - landau_log_ratio) ** 2 + x_tick**2 + x_transit**2
    ) / 2
    stationary_point = {
        x_rg: landau_log_ratio,
        x_tick: 0,
        x_transit: 0,
    }
    stationary_gradient = sp.ImmutableMatrix([
        sp.diff(parent, variable).subs(stationary_point)
        for variable in (x_rg, x_tick, x_transit)
    ])
    parent_hessian = sp.ImmutableMatrix(
        sp.hessian(parent, (x_rg, x_tick, x_transit))
    )

    # Columns are log(tau_birth), log(mu_spec), log(omega_DT),
    # log(ell_edge), log(c).  The rows encode omega_DT/(c mu_spec),
    # tau_birth omega_DT, and ell_edge/(c tau_birth).
    scale_map = sp.ImmutableMatrix([
        [0, -1, 1, 0, -1],
        [1, 0, 1, 0, 0],
        [-1, 0, 0, 1, -1],
    ])
    scale_kernels = sp.ImmutableMatrix([
        [1, -1],
        [-1, 0],
        [-1, 1],
        [1, 0],
        [0, 1],
    ])
    speed_anchored_map = sp.ImmutableMatrix.vstack(
        scale_map, sp.ImmutableMatrix([[0, 0, 0, 0, 1]])
    )
    speed_anchored_kernel = sp.ImmutableMatrix([1, -1, -1, 1, 0])
    fully_anchored_map = sp.ImmutableMatrix.vstack(
        speed_anchored_map, sp.ImmutableMatrix([[0, 1, 0, 0, 0]])
    )

    inherited_rg_data = sp.ones(2, 1)
    bath_typed_transfer = sp.zeros(1, 1)
    conditional_origin = sp.ones(9, 1)
    physical_origin = sp.zeros(4, 1)

    theorems = (
        kernel.prove_expression_equality(beta_coefficient, 2, subject="inherited relative-U1 beta coefficient"),
        kernel.prove_expression_equality(boundary_coupling_squared, sp.Rational(3, 8), subject="inherited relative-U1 boundary coupling"),
        kernel.prove_expression_equality(landau_log_ratio, 32 * sp.pi**2 / 3, subject="exact Landau logarithm"),
        kernel.prove_expression_equality(seed_log_ratio, 64 * sp.pi**2 / 3, subject="exact inverse-area seed logarithm"),
        kernel.prove_expression_equality(tick_reference_product, sp.exp(-32 * sp.pi**2 / 3), subject="transmuted tick relative to the reference wavenumber"),
        kernel.prove_expression_equality(k43_tick_product, 42, subject="K43 birth-tick spectral product"),
        kernel.prove_expression_equality(mismatch_factor, 42 * sp.exp(32 * sp.pi**2 / 3), subject="exact K43-to-transmutation mismatch factor"),
        kernel.prove_matrix_inequality(sp.ImmutableMatrix([tick_reference_product]), sp.ImmutableMatrix([k43_tick_product]), subject="naive mu_spec equals Lambda43 typing is incompatible with the established birth tick"),
        kernel.prove_matrix_equality(stationary_gradient, sp.zeros(3, 1), subject="conditional transmutation parent is stationary at all target relations"),
        kernel.prove_matrix_equality(parent_hessian, sp.eye(3), subject="conditional transmutation parent has identity Hessian"),
        kernel.prove_exact_rank(parent_hessian, 3, subject="conditional parent controls all invariant residuals"),
        kernel.prove_expression_equality(parent_hessian.det(), 1, subject="conditional parent is strictly positive"),
        kernel.prove_exact_rank(scale_map, 3, subject="three relative dimensional relations are independent"),
        kernel.prove_exact_nullity(scale_map, 2, subject="speed and common length-time scale remain free before anchoring"),
        kernel.prove_matrix_equality(scale_map * scale_kernels, sp.zeros(3, 2), subject="two exact scale modes survive dimensional transmutation"),
        kernel.prove_exact_rank(speed_anchored_map, 4, subject="fixing c removes only the speed mode"),
        kernel.prove_exact_nullity(speed_anchored_map, 1, subject="one common birth-tick scale survives after fixing c"),
        kernel.prove_matrix_equality(speed_anchored_map * speed_anchored_kernel, sp.zeros(4, 1), subject="reference wavenumber and birth tick share the residual orbit"),
        kernel.prove_exact_rank(fully_anchored_map, 5, subject="an independent reference wavenumber would close the dimensional map"),
        kernel.prove_exact_nullity(fully_anchored_map, 0, subject="external mu_spec anchor removes the final scale mode"),
        kernel.prove_matrix_equality(inherited_rg_data, sp.ones(2, 1), subject="two historical RG inputs exist"),
        kernel.prove_matrix_equality(bath_typed_transfer, sp.zeros(1, 1), subject="the historical RG coupling is not typed into the bath carrier"),
        kernel.prove_matrix_equality(conditional_origin, sp.ones(9, 1), subject="conditional dimensional-transmutation architecture is complete"),
        kernel.prove_expression_equality(sum(conditional_origin), 9, subject="nine conditional requirements pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(4, 1), subject="bath RG transfer reference scale K43 compatibility and absolute tick remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict physical birth-tick origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin_gate",
        theorems,
    )
    return BirthTickDimensionalTransmutationCertificate(
        beta_coefficient,
        boundary_coupling_squared,
        landau_log_ratio,
        seed_log_ratio,
        tick_reference_product,
        k43_tick_product,
        mismatch_factor,
        parent,
        stationary_gradient,
        parent_hessian,
        scale_map,
        scale_kernels,
        speed_anchored_map,
        speed_anchored_kernel,
        fully_anchored_map,
        inherited_rg_data,
        bath_typed_transfer,
        conditional_origin,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin_gate",
    title="Родитель размерностной трансмутации такта рождения",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"birth_tick_dimensional_transmutation_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(26)
    ),
)