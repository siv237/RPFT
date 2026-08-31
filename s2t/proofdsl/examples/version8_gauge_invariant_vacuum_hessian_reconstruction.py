"""Exact horizontal quotient of the fixed-background vacuum Hessian."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_full_42_carrier_base_k_determinant_compatibility import (
    build_certificate as determinant_certificate,
)
from .version8_full_42_carrier_bv_vacuum_quotient import (
    build_certificate as bv_certificate,
)
from .version8_full_noise_trace_frame import build_certificate as frame_certificate


@dataclass(frozen=True, slots=True)
class GaugeInvariantVacuumHessianReconstructionCertificate:
    orbit_basis: sp.ImmutableMatrix
    orbit_metric: sp.ImmutableMatrix
    orbit_projector: sp.ImmutableMatrix
    horizontal_projector: sp.ImmutableMatrix
    quotient_hessian: sp.ImmutableMatrix
    horizontal_flat_direction: sp.ImmutableMatrix
    scalar_fourth_moment: sp.Expr
    bosonic_fourth_moment: sp.Expr
    full_quadratic_numerator: sp.Expr
    orbit_metric_theorem: Theorem
    projector_theorem: Theorem
    metric_orthogonality_theorem: Theorem
    horizontal_rank_theorem: Theorem
    goldstone_kernel_theorem: Theorem
    quotient_rank_theorem: Theorem
    quotient_nullity_theorem: Theorem
    kernel_decomposition_theorem: Theorem
    scalar_fourth_theorem: Theorem
    bosonic_fourth_theorem: Theorem
    full_numerator_theorem: Theorem
    nonlinear_parent_boundary_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> GaugeInvariantVacuumHessianReconstructionCertificate:
    determinant = determinant_certificate()
    bv = bv_certificate()
    transfer_metric = sp.ImmutableMatrix(frame_certificate().trace_metric[:30, :30])
    orbit_coordinates = sp.Matrix(bv.gauge_orbit_coordinates)
    _, pivot_columns = orbit_coordinates.rref()
    orbit_basis = sp.ImmutableMatrix(orbit_coordinates[:, list(pivot_columns)])
    orbit_metric = sp.ImmutableMatrix(orbit_basis.T * transfer_metric * orbit_basis)
    orbit_metric_theorem = kernel.prove_matrix_equality(
        orbit_metric,
        14 * sp.eye(3),
        subject="trace metric restricted to the broken gauge orbit",
    )

    orbit_projector = sp.ImmutableMatrix(
        orbit_basis * orbit_metric.inv() * orbit_basis.T * transfer_metric
    )
    horizontal_projector = sp.ImmutableMatrix(sp.eye(30) - orbit_projector)
    projector_theorem = kernel.prove_matrix_equality(
        orbit_projector * orbit_projector,
        orbit_projector,
        subject="trace-orthogonal projector onto the broken gauge orbit",
    )
    metric_orthogonality = kernel.prove_matrix_equality(
        orbit_projector.T * transfer_metric,
        transfer_metric * orbit_projector,
        subject="self-adjointness of the orbit projector in the trace metric",
    )
    horizontal_rank = kernel.prove_exact_rank(
        horizontal_projector,
        27,
        subject="horizontal transfer slice after the gauge quotient",
    )

    fixed_hessian = sp.Matrix(determinant.scalar_hessian)
    quotient_hessian = sp.ImmutableMatrix(
        horizontal_projector.T * fixed_hessian * horizontal_projector
    )
    goldstone_kernel = kernel.prove_matrix_equality(
        quotient_hessian * orbit_coordinates,
        sp.zeros(30, 12),
        subject="all broken gauge directions are zero modes of the quotient Hessian",
    )
    quotient_rank = kernel.prove_exact_rank(
        quotient_hessian,
        26,
        subject="rank of the reconstructed quadratic quotient Hessian",
    )
    quotient_nullity = kernel.prove_exact_nullity(
        quotient_hessian,
        4,
        subject="three Goldstone modes plus one horizontal flat mode",
    )

    horizontal_flat = sp.ImmutableMatrix(
        sp.Matrix([0, 6, 0, 0, 0, 0, 0, -1, 0, 1] + [0] * 20)
    )
    full_kernel_basis = sp.ImmutableMatrix(orbit_basis.row_join(horizontal_flat))
    kernel_decomposition = kernel.prove_linear_kernel(
        quotient_hessian,
        full_kernel_basis,
        subject="Goldstone orbit plus the unique horizontal scalar flat direction",
    )

    scalar_mass = sp.ImmutableMatrix(transfer_metric.inv() * quotient_hessian)
    scalar_fourth = sp.simplify(sp.trace(scalar_mass * scalar_mass))
    scalar_fourth_theorem = kernel.prove_expression_equality(
        scalar_fourth,
        sp.Rational(1118917, 882),
        subject="scalar fourth moment on the horizontal quotient",
    )
    gauge_fourth = sp.trace(sp.Matrix(determinant.gauge_mass_operator) ** 2)
    bosonic_fourth = sp.simplify(scalar_fourth + 3 * gauge_fourth)
    bosonic_fourth_theorem = kernel.prove_expression_equality(
        bosonic_fourth,
        sp.Rational(226371884, 159201),
        subject="quadratic BV bosonic fourth moment",
    )
    full_numerator = sp.simplify(bosonic_fourth - bv.physical_fermion_fourth_moment)
    full_numerator_theorem = kernel.prove_expression_equality(
        full_numerator,
        sp.Rational(211725392, 159201),
        subject="quadratic horizontal-quotient supertrace numerator",
    )
    nonlinear_parent_boundary = kernel.prove_gate(
        "quadratic_quotient_does_not_supply_a_nonlinear_gauge_invariant_parent",
        (kernel_decomposition, scalar_fourth_theorem, bosonic_fourth_theorem),
    )
    gate = kernel.prove_gate(
        "gauge_invariant_vacuum_hessian_reconstruction",
        (
            orbit_metric_theorem,
            projector_theorem,
            metric_orthogonality,
            horizontal_rank,
            goldstone_kernel,
            quotient_rank,
            quotient_nullity,
            kernel_decomposition,
            scalar_fourth_theorem,
            bosonic_fourth_theorem,
            full_numerator_theorem,
            nonlinear_parent_boundary,
        ),
    )
    return GaugeInvariantVacuumHessianReconstructionCertificate(
        orbit_basis=orbit_basis,
        orbit_metric=orbit_metric,
        orbit_projector=orbit_projector,
        horizontal_projector=horizontal_projector,
        quotient_hessian=quotient_hessian,
        horizontal_flat_direction=horizontal_flat,
        scalar_fourth_moment=scalar_fourth,
        bosonic_fourth_moment=bosonic_fourth,
        full_quadratic_numerator=full_numerator,
        orbit_metric_theorem=orbit_metric_theorem,
        projector_theorem=projector_theorem,
        metric_orthogonality_theorem=metric_orthogonality,
        horizontal_rank_theorem=horizontal_rank,
        goldstone_kernel_theorem=goldstone_kernel,
        quotient_rank_theorem=quotient_rank,
        quotient_nullity_theorem=quotient_nullity,
        kernel_decomposition_theorem=kernel_decomposition,
        scalar_fourth_theorem=scalar_fourth_theorem,
        bosonic_fourth_theorem=bosonic_fourth_theorem,
        full_numerator_theorem=full_numerator_theorem,
        nonlinear_parent_boundary_theorem=nonlinear_parent_boundary,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.orbit_metric)
    print(certificate.quotient_hessian.rank())
    print(certificate.full_quadratic_numerator)