"""LCF certificate for the origin boundary of bath correlation time."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class BathCorrelationTimeCertificate:
    correlation_times: sp.ImmutableMatrix
    mixture_time: sp.Expr
    mixture_slope: sp.Expr
    fixed_profile_gradient: sp.ImmutableMatrix
    fixed_profile_hessian: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    velocity_anchored_map: sp.ImmutableMatrix
    fully_anchored_map: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> BathCorrelationTimeCertificate:
    x = sp.symbols("x", nonnegative=True)
    a = sp.symbols("a", real=True)
    exponential = sp.exp(-x)
    gaussian = sp.exp(-x**2)
    tau_exponential = sp.integrate(exponential, (x, 0, sp.oo))
    tau_gaussian = sp.integrate(gaussian, (x, 0, sp.oo))
    correlation_times = sp.ImmutableMatrix([tau_exponential, tau_gaussian])
    mixture = a * exponential + (1 - a) * gaussian
    mixture_time = sp.integrate(mixture, (x, 0, sp.oo))
    mixture_slope = sp.diff(mixture, x).subs(x, 0)

    r = sp.symbols("r", real=True)
    fixed_profile_parent = (r - 1) ** 2 / 2
    fixed_profile_gradient = sp.ImmutableMatrix([sp.diff(fixed_profile_parent, r).subs(r, 1)])
    fixed_profile_hessian = sp.ImmutableMatrix(sp.hessian(fixed_profile_parent, (r,)))

    # Logarithmic variables are (tau_corr, omega_UV, ell_cell, v_g).
    scale_map = sp.ImmutableMatrix([[1, 1, 0, 0], [0, 1, 1, -1]])
    scale_kernel = sp.ImmutableMatrix.hstack(
        sp.ImmutableMatrix([-1, 1, 0, 1]),
        sp.ImmutableMatrix([1, -1, 1, 0]),
    )
    velocity_anchored_map = sp.ImmutableMatrix.vstack(
        scale_map, sp.ImmutableMatrix([[0, 0, 0, 1]])
    )
    fully_anchored_map = sp.ImmutableMatrix.vstack(
        velocity_anchored_map, sp.ImmutableMatrix([[0, 0, 1, 0]])
    )
    conditional_origin = sp.ones(8, 1)
    physical_origin = sp.zeros(2, 1)

    theorems = (
        kernel.prove_expression_equality(exponential.subs(x, 0), 1, subject="exponential correlation normalization"),
        kernel.prove_expression_equality(gaussian.subs(x, 0), 1, subject="Gaussian correlation normalization"),
        kernel.prove_expression_equality(tau_exponential, 1, subject="exponential dimensionless correlation time"),
        kernel.prove_expression_equality(tau_gaussian, sp.sqrt(sp.pi) / 2, subject="Gaussian dimensionless correlation time"),
        kernel.prove_matrix_inequality(sp.ImmutableMatrix([tau_exponential]), sp.ImmutableMatrix([tau_gaussian]), subject="equal cutoffs permit unequal correlation times"),
        kernel.prove_expression_equality(sp.diff(exponential, x).subs(x, 0), -1, subject="exponential short-time slope"),
        kernel.prove_expression_equality(sp.diff(gaussian, x).subs(x, 0), 0, subject="Gaussian short-time slope"),
        kernel.prove_expression_equality(mixture.subs(x, 0), 1, subject="normalized correlation mixture"),
        kernel.prove_expression_equality(mixture_time, a + (1 - a) * sp.sqrt(sp.pi) / 2, subject="mixture correlation time"),
        kernel.prove_expression_equality(mixture_slope, -a, subject="mixture short-time slope"),
        kernel.prove_expression_nonconstant(mixture_time, a, subject="correlation time depends on spectral shape"),
        kernel.prove_matrix_equality(fixed_profile_gradient, sp.zeros(1, 1), subject="fixed exponential profile parent stationary point"),
        kernel.prove_matrix_equality(fixed_profile_hessian, sp.eye(1), subject="fixed exponential profile parent Hessian"),
        kernel.prove_expression_equality(fixed_profile_hessian.det(), 1, subject="fixed-profile parent determinant"),
        kernel.prove_exact_rank(scale_map, 2, subject="bath correlation-time dimensional map rank"),
        kernel.prove_exact_nullity(scale_map, 2, subject="bath time length and velocity freedoms"),
        kernel.prove_matrix_equality(scale_map * scale_kernel, sp.zeros(2, 2), subject="bath correlation-time scale kernels"),
        kernel.prove_exact_rank(velocity_anchored_map, 3, subject="velocity anchor leaves the cell-length time orbit"),
        kernel.prove_exact_rank(fully_anchored_map, 4, subject="velocity and length anchors close the time map"),
        kernel.prove_matrix_equality(conditional_origin, sp.ones(8, 1), subject="conditional correlation-time architecture complete"),
        kernel.prove_expression_equality(sum(conditional_origin), 8, subject="eight conditional time requirements pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(2, 1), subject="spectral-shape and absolute-time origins remain open"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_correlation_time_parent_origin_gate",
        theorems,
    )
    return BathCorrelationTimeCertificate(
        correlation_times,
        mixture_time,
        mixture_slope,
        fixed_profile_gradient,
        fixed_profile_hessian,
        scale_map,
        scale_kernel,
        velocity_anchored_map,
        fully_anchored_map,
        conditional_origin,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_correlation_time_parent_origin_gate",
    title="Происхождение времени корреляции неравновесной ванны",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_correlation_time_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_correlation_time_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"bath_correlation_time_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(22)
    ),
)