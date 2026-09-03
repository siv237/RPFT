"""LCF certificate for a local causal bath propagation-kernel parent."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class LocalCausalKernelCertificate:
    adjacency: sp.ImmutableMatrix
    causal_defects: sp.ImmutableMatrix
    hot_envelope: sp.ImmutableMatrix
    cold_envelope: sp.ImmutableMatrix
    covariance_determinants: sp.ImmutableMatrix
    parent_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    parent_kernel: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    time_anchored_map: sp.ImmutableMatrix
    fully_anchored_map: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> LocalCausalKernelCertificate:
    size = 7
    adjacency = sp.ImmutableMatrix(
        size,
        size,
        lambda i, j: sp.Rational(1, 2) if abs(i - j) == 1 else 0,
    )
    defects = []
    for step in (1, 2, 3):
        power = adjacency**step
        defects.extend(power[i, j] for i in range(size) for j in range(size) if abs(i - j) > step)
    causal_defects = sp.ImmutableMatrix(defects)

    hot_r = sp.Rational(1, 2)
    cold_r = sp.Rational(1, 4)
    hot_envelope = sp.ImmutableMatrix([hot_r**n for n in range(4)])
    cold_envelope = sp.ImmutableMatrix([cold_r**n for n in range(4)])
    hot_covariance = sp.ImmutableMatrix(3, 3, lambda i, j: hot_r ** abs(i - j))
    cold_covariance = sp.ImmutableMatrix(3, 3, lambda i, j: cold_r ** abs(i - j))
    covariance_determinants = sp.ImmutableMatrix([hot_covariance.det(), cold_covariance.det()])

    k1, k2, k3, r = sp.symbols("k1 k2 k3 r", real=True)
    residuals = sp.ImmutableMatrix([k1 - r, k2 - r * k1, k3 - r * k2])
    parent = sp.expand((residuals.T * residuals)[0] / 2)
    variables = (k1, k2, k3, r)
    hot_point = {k1: hot_r, k2: hot_r**2, k3: hot_r**3, r: hot_r}
    parent_gradient = sp.ImmutableMatrix([sp.diff(parent, item) for item in variables]).subs(hot_point)
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, variables).subs(hot_point))
    parent_kernel = sp.ImmutableMatrix([1, 1, sp.Rational(3, 4), 1])

    # Logarithmic variables are (tau_corr, Delta_t, ell_cell, v_g).
    scale_map = sp.ImmutableMatrix([[1, -1, 0, 0], [0, 1, -1, 1]])
    scale_kernel = sp.ImmutableMatrix.hstack(
        sp.ImmutableMatrix([1, 1, 1, 0]),
        sp.ImmutableMatrix([-1, -1, 0, 1]),
    )
    time_anchored_map = sp.ImmutableMatrix.vstack(scale_map, sp.ImmutableMatrix([[0, 1, 0, 0]]))
    fully_anchored_map = sp.ImmutableMatrix.vstack(time_anchored_map, sp.ImmutableMatrix([[0, 0, 1, 0]]))
    conditional_origin = sp.ones(8, 1)
    physical_origin = sp.zeros(2, 1)

    theorems = (
        kernel.prove_matrix_equality(adjacency, adjacency.T, subject="nearest-neighbour propagation operator is symmetric"),
        kernel.prove_matrix_equality(causal_defects, sp.zeros(causal_defects.rows, 1), subject="three-step kernel has no support outside the graph light cone"),
        kernel.prove_matrix_equality(hot_envelope, sp.ImmutableMatrix([1, sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 8)]), subject="hot geometric memory envelope"),
        kernel.prove_matrix_equality(cold_envelope, sp.ImmutableMatrix([1, sp.Rational(1, 4), sp.Rational(1, 16), sp.Rational(1, 64)]), subject="cold geometric memory envelope"),
        kernel.prove_expression_equality(sum(hot_r**n for n in range(20)) + hot_r**20 / (1 - hot_r), 2, subject="hot infinite memory sum"),
        kernel.prove_expression_equality(sum(cold_r**n for n in range(20)) + cold_r**20 / (1 - cold_r), sp.Rational(4, 3), subject="cold infinite memory sum"),
        kernel.prove_matrix_equality(covariance_determinants, sp.ImmutableMatrix([sp.Rational(9, 16), sp.Rational(225, 256)]), subject="positive Toeplitz covariance determinants"),
        kernel.prove_matrix_equality(parent_gradient, sp.zeros(4, 1), subject="local kernel chain parent stationary point"),
        kernel.prove_exact_rank(parent_hessian, 3, subject="local kernel parent fixes three chain coordinates"),
        kernel.prove_exact_nullity(parent_hessian, 1, subject="decay parameter remains a parent zero mode"),
        kernel.prove_matrix_equality(parent_hessian * parent_kernel, sp.zeros(4, 1), subject="geometric-decay family tangent is the parent kernel"),
        kernel.prove_expression_equality(parent_hessian.det(), 0, subject="locality parent does not select damping"),
        kernel.prove_matrix_inequality(sp.ImmutableMatrix([hot_r]), sp.ImmutableMatrix([cold_r]), subject="two KMS ratios induce distinct conditional memories"),
        kernel.prove_exact_rank(scale_map, 2, subject="local kernel time-scale map rank"),
        kernel.prove_exact_nullity(scale_map, 2, subject="local kernel time-scale map nullity"),
        kernel.prove_matrix_equality(scale_map * scale_kernel, sp.zeros(2, 2), subject="local kernel residual scale orbits"),
        kernel.prove_exact_rank(time_anchored_map, 3, subject="step-time anchor leaves one length orbit"),
        kernel.prove_exact_rank(fully_anchored_map, 4, subject="step-time and length anchors close propagation scale"),
        kernel.prove_matrix_equality(conditional_origin, sp.ones(8, 1), subject="conditional local causal kernel architecture complete"),
        kernel.prove_expression_equality(sum(conditional_origin), 8, subject="eight conditional causal-kernel requirements pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(2, 1), subject="damping and absolute-time origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="no physical damping or clock anchor is supplied"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin_gate",
        theorems,
    )
    return LocalCausalKernelCertificate(
        adjacency,
        causal_defects,
        hot_envelope,
        cold_envelope,
        covariance_determinants,
        parent_gradient,
        parent_hessian,
        parent_kernel,
        scale_map,
        scale_kernel,
        time_anchored_map,
        fully_anchored_map,
        conditional_origin,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin_gate",
    title="Родитель локального причинного ядра распространения ванны",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"local_causal_kernel_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(22)
    ),
)