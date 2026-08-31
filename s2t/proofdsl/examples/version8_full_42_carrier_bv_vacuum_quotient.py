"""Exact BV/Goldstone audit and fermion multiplicity on the full carrier."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_fixed_algebra import physical_incidence
from .version8_full_42_carrier_base_k_determinant_compatibility import (
    build_certificate as determinant_certificate,
)
from .version8_full_field_kinetic_relative_weight_parent_origin import (
    build_certificate as kinetic_weight_certificate,
)
from .version8_full_noise_trace_frame import (
    build_certificate as frame_certificate,
    full_noise_frame,
)


@dataclass(frozen=True, slots=True)
class Full42CarrierBvVacuumQuotientCertificate:
    internal_grading: sp.ImmutableMatrix
    physical_chiral_projector: sp.ImmutableMatrix
    gauge_orbit_coordinates: sp.ImmutableMatrix
    orbit_hessian_restriction: sp.ImmutableMatrix
    physical_fermion_fourth_moment: sp.Expr
    fixed_background_candidate_numerator: sp.Expr
    grading_theorem: Theorem
    projector_theorem: Theorem
    projector_rank_theorem: Theorem
    fermion_multiplicity_theorem: Theorem
    gauge_orbit_rank_theorem: Theorem
    orbit_hessian_rank_theorem: Theorem
    orbit_hessian_trace_theorem: Theorem
    goldstone_no_go_theorem: Theorem
    candidate_numerator_theorem: Theorem
    physical_ledger_boundary_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> Full42CarrierBvVacuumQuotientCertificate:
    determinant = determinant_certificate()
    frame_data = frame_certificate()
    frame = full_noise_frame()
    incidence = sp.ImmutableMatrix(physical_incidence())

    vacuum = sp.zeros(21)
    vacuum[:11, 11:] = incidence.H
    vacuum[11:, :11] = incidence
    internal_grading = sp.ImmutableMatrix(sp.diag(*([1] * 11 + [-1] * 10)))
    grading = kernel.prove_matrix_equality(
        internal_grading * vacuum + vacuum * internal_grading,
        sp.zeros(21),
        subject="odd finite incidence anticommutes with the internal grading",
    )

    gamma_five = kinetic_weight_certificate().gamma_five
    total_grading = sp.kronecker_product(gamma_five, internal_grading)
    physical_projector = sp.ImmutableMatrix((sp.eye(84) + total_grading) / 2)
    projector = kernel.prove_matrix_equality(
        physical_projector * physical_projector,
        physical_projector,
        subject="total-even chiral projector on spinors times the finite carrier",
    )
    projector_rank = kernel.prove_exact_rank(
        physical_projector,
        42,
        subject="rank of the physical chiral fermion projector",
    )
    mass_four = sp.kronecker_product(sp.eye(4), vacuum**4)
    physical_fermion_fourth = sp.simplify(sp.trace(physical_projector * mass_four))
    fermion_multiplicity = kernel.prove_expression_equality(
        physical_fermion_fourth,
        92,
        subject="physical chiral fermion fourth moment",
    )

    transfer_frame = frame[:30]
    gauge_frame = frame[30:]
    transfer_metric = sp.ImmutableMatrix(frame_data.trace_metric[:30, :30])
    inverse_metric = transfer_metric.inv()
    orbit_columns = []
    for generator in gauge_frame:
        variation = sp.I * (generator * vacuum - vacuum * generator)
        covector = sp.Matrix(
            [sp.simplify(sp.trace(direction.H * variation)) for direction in transfer_frame]
        )
        orbit_columns.append(inverse_metric * covector)
    orbit_coordinates = sp.ImmutableMatrix(sp.Matrix.hstack(*orbit_columns))
    orbit_rank = kernel.prove_exact_rank(
        orbit_coordinates,
        3,
        subject="broken gauge orbit inside the full transfer carrier",
    )

    scalar_hessian = sp.Matrix(determinant.scalar_hessian)
    orbit_restriction = sp.ImmutableMatrix(
        sp.simplify(orbit_coordinates.T * scalar_hessian * orbit_coordinates)
    )
    orbit_hessian_rank = kernel.prove_exact_rank(
        orbit_restriction,
        3,
        subject="fixed-background scalar Hessian restricted to the broken gauge orbit",
    )
    orbit_hessian_trace = kernel.prove_expression_equality(
        sp.trace(orbit_restriction),
        34,
        subject="trace of the scalar Hessian on the broken gauge orbit",
    )
    goldstone_no_go = kernel.prove_matrix_inequality(
        orbit_restriction,
        sp.zeros(12),
        subject="fixed-background Gram Hessian fails the Goldstone kernel condition",
    )

    candidate_numerator = sp.simplify(
        determinant.bosonic_fourth_moment - physical_fermion_fourth
    )
    candidate = kernel.prove_expression_equality(
        candidate_numerator,
        sp.Rational(4360268, 3249),
        subject="algebraic full numerator before the BV Goldstone repair",
    )
    physical_boundary = kernel.prove_gate(
        "physical_bv_ledger_requires_gauge_invariant_vacuum_hessian",
        (orbit_rank, orbit_hessian_rank, goldstone_no_go),
    )
    gate = kernel.prove_gate(
        "full_42_carrier_bv_vacuum_quotient",
        (
            grading,
            projector,
            projector_rank,
            fermion_multiplicity,
            orbit_rank,
            orbit_hessian_rank,
            orbit_hessian_trace,
            goldstone_no_go,
            candidate,
            physical_boundary,
        ),
    )
    return Full42CarrierBvVacuumQuotientCertificate(
        internal_grading=internal_grading,
        physical_chiral_projector=physical_projector,
        gauge_orbit_coordinates=orbit_coordinates,
        orbit_hessian_restriction=orbit_restriction,
        physical_fermion_fourth_moment=physical_fermion_fourth,
        fixed_background_candidate_numerator=candidate_numerator,
        grading_theorem=grading,
        projector_theorem=projector,
        projector_rank_theorem=projector_rank,
        fermion_multiplicity_theorem=fermion_multiplicity,
        gauge_orbit_rank_theorem=orbit_rank,
        orbit_hessian_rank_theorem=orbit_hessian_rank,
        orbit_hessian_trace_theorem=orbit_hessian_trace,
        goldstone_no_go_theorem=goldstone_no_go,
        candidate_numerator_theorem=candidate,
        physical_ledger_boundary_theorem=physical_boundary,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.physical_fermion_fourth_moment)
    print(certificate.orbit_hessian_restriction.rank())
    print(certificate.fixed_background_candidate_numerator)