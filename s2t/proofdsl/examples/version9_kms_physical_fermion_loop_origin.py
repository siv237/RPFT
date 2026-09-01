"""LCF certificate for the physical KMS fermion-loop origin audit."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSPhysicalFermionLoopOriginCertificate:
    target_projector: sp.ImmutableMatrix
    gap_operator: sp.ImmutableMatrix
    conductance_operator: sp.ImmutableMatrix
    doubled_operator: sp.ImmutableMatrix
    real_lift: sp.ImmutableMatrix
    real_pairing_witness: sp.ImmutableMatrix
    composite_kernel: sp.ImmutableMatrix
    target_rank_theorem: Theorem
    gap_determinant_theorem: Theorem
    conductance_determinant_theorem: Theorem
    single_linear_degree_theorem: Theorem
    target_degree_theorem: Theorem
    real_lift_determinant_theorem: Theorem
    real_pairing_mismatch_theorem: Theorem
    doubled_determinant_theorem: Theorem
    doubled_rank_theorem: Theorem
    composite_determinant_theorem: Theorem
    composite_nonlinearity_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSPhysicalFermionLoopOriginCertificate:
    target_projector = sp.ImmutableMatrix(sp.diag(0, 1, 1, 1, 1, 1))

    ts, ta, tt = sp.symbols("theta_s theta_a theta_t", positive=True)
    ks, ka, kt = sp.symbols("kappa_s kappa_a kappa_t", positive=True)
    gap_operator = sp.ImmutableMatrix(sp.diag(ts, ta, tt, tt, tt))
    conductance_operator = sp.ImmutableMatrix(sp.diag(ks, ka, kt, kt, kt))
    doubled_operator = sp.ImmutableMatrix(sp.diag(gap_operator, conductance_operator))
    composite_kernel = sp.ImmutableMatrix(gap_operator * conductance_operator)

    zero = sp.zeros(5)
    real_lift = sp.ImmutableMatrix(sp.Matrix.vstack(
        sp.Matrix.hstack(zero, gap_operator),
        sp.Matrix.hstack(-gap_operator, zero),
    ))

    gap_witness = sp.diag(1, 2, 3, 3, 3)
    conductance_witness = sp.diag(2, 1, 2, 2, 2)
    real_pairing_witness = sp.ImmutableMatrix(sp.diag(gap_witness, conductance_witness))
    real_swap = sp.Matrix.vstack(
        sp.Matrix.hstack(sp.zeros(5), sp.eye(5)),
        sp.Matrix.hstack(sp.eye(5), sp.zeros(5)),
    )
    real_pairing_commutator = sp.ImmutableMatrix(
        real_swap * real_pairing_witness - real_pairing_witness * real_swap
    )

    gap_det = ts * ta * tt**3
    conductance_det = ks * ka * kt**3
    scale = sp.symbols("lambda", positive=True)
    single_linear_kernel = gap_operator + conductance_operator

    target_rank_theorem = kernel.prove_exact_rank(
        target_projector,
        5,
        subject="physical creation cell contains one five dimensional target multiplet",
    )
    gap_determinant_theorem = kernel.prove_expression_equality(
        gap_operator.det(),
        gap_det,
        subject="one physical type multiplet carries one gap determinant",
    )
    conductance_determinant_theorem = kernel.prove_expression_equality(
        conductance_operator.det(),
        conductance_det,
        subject="one conductance type operator also has determinant degree five",
    )
    single_linear_degree_theorem = kernel.prove_expression_equality(
        (scale * single_linear_kernel).det(),
        scale**5 * single_linear_kernel.det(),
        subject="one homogeneous linear five channel kernel has common scaling degree five",
    )
    target_degree_theorem = kernel.prove_expression_equality(
        (scale * gap_operator).det() * (scale * conductance_operator).det(),
        scale**10 * gap_det * conductance_det,
        subject="the two package target has common scaling degree ten",
    )
    real_lift_determinant_theorem = kernel.prove_expression_equality(
        real_lift.det(),
        gap_det**2,
        subject="KO Real doubling squares one determinant before Pfaffian half counting",
    )
    real_pairing_mismatch_theorem = kernel.prove_exact_rank(
        real_pairing_commutator,
        10,
        subject="independent gap and conductance blocks violate exchange Real pairing",
    )
    doubled_determinant_theorem = kernel.prove_expression_equality(
        doubled_operator.det(),
        gap_det * conductance_det,
        subject="two independent fermion multiplets reproduce the target determinant",
    )
    doubled_rank_theorem = kernel.prove_exact_rank(
        doubled_operator,
        10,
        subject="the block linear target needs ten nondegenerate fermion directions",
    )
    composite_determinant_theorem = kernel.prove_expression_equality(
        composite_kernel.det(),
        gap_det * conductance_det,
        subject="a multiplicative five channel kernel algebraically reproduces the target",
    )
    composite_nonlinearity_theorem = kernel.prove_expression_equality(
        sp.diff(composite_kernel[0, 0], ts, ks),
        1,
        subject="the multiplicative kernel contains an explicit mixed package coupling",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_logdet_physical_fermion_loop_"
        "parent_origin_gate",
        (
            target_rank_theorem,
            gap_determinant_theorem,
            conductance_determinant_theorem,
            single_linear_degree_theorem,
            target_degree_theorem,
            real_lift_determinant_theorem,
            real_pairing_mismatch_theorem,
            doubled_determinant_theorem,
            doubled_rank_theorem,
            composite_determinant_theorem,
            composite_nonlinearity_theorem,
        ),
    )
    return KMSPhysicalFermionLoopOriginCertificate(
        target_projector=target_projector,
        gap_operator=gap_operator,
        conductance_operator=conductance_operator,
        doubled_operator=doubled_operator,
        real_lift=real_lift,
        real_pairing_witness=real_pairing_witness,
        composite_kernel=composite_kernel,
        target_rank_theorem=target_rank_theorem,
        gap_determinant_theorem=gap_determinant_theorem,
        conductance_determinant_theorem=conductance_determinant_theorem,
        single_linear_degree_theorem=single_linear_degree_theorem,
        target_degree_theorem=target_degree_theorem,
        real_lift_determinant_theorem=real_lift_determinant_theorem,
        real_pairing_mismatch_theorem=real_pairing_mismatch_theorem,
        doubled_determinant_theorem=doubled_determinant_theorem,
        doubled_rank_theorem=doubled_rank_theorem,
        composite_determinant_theorem=composite_determinant_theorem,
        composite_nonlinearity_theorem=composite_nonlinearity_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version9_endpoint_creation_kms_logdet_physical_fermion_loop_"
        "parent_origin_gate"
    ),
    title="Parent-origin physical fermion loop для KMS logdet",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_logdet_physical_"
        "fermion_loop_parent_origin_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_physical_"
        "fermion_loop_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("physical_target_rank_five", lambda: build_certificate().target_rank_theorem),
        Obligation("gap_type_determinant", lambda: build_certificate().gap_determinant_theorem),
        Obligation("conductance_type_determinant", lambda: build_certificate().conductance_determinant_theorem),
        Obligation("single_linear_kernel_degree_five", lambda: build_certificate().single_linear_degree_theorem),
        Obligation("two_package_target_degree_ten", lambda: build_certificate().target_degree_theorem),
        Obligation("real_lift_determinant_square", lambda: build_certificate().real_lift_determinant_theorem),
        Obligation("independent_packages_break_real_pairing", lambda: build_certificate().real_pairing_mismatch_theorem),
        Obligation("doubled_fermion_determinant_target", lambda: build_certificate().doubled_determinant_theorem),
        Obligation("doubled_fermion_rank_ten", lambda: build_certificate().doubled_rank_theorem),
        Obligation("composite_kernel_determinant_target", lambda: build_certificate().composite_determinant_theorem),
        Obligation("composite_kernel_is_mixed", lambda: build_certificate().composite_nonlinearity_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)