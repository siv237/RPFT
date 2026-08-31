"""Exact bosonic base-K ledger on the full 42-real field carrier."""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..kernel import Theorem, kernel
from .version8_fixed_algebra import physical_incidence
from .version8_full_noise_trace_frame import build_certificate as frame_certificate, full_noise_frame


@dataclass(frozen=True, slots=True)
class Full42CarrierBaseKCompatibilityCertificate:
    scalar_hessian: sp.ImmutableMatrix
    gauge_mass_gram: sp.ImmutableMatrix
    scalar_mass_operator: sp.ImmutableMatrix
    gauge_mass_operator: sp.ImmutableMatrix
    bosonic_fourth_moment: sp.Expr
    finite_fermion_fourth_moment: sp.Expr
    scalar_rank_theorem: Theorem
    scalar_nullity_theorem: Theorem
    gauge_rank_theorem: Theorem
    gauge_nullity_theorem: Theorem
    scalar_fourth_theorem: Theorem
    gauge_fourth_theorem: Theorem
    bosonic_ledger_theorem: Theorem
    fermion_moment_theorem: Theorem
    full_ledger_boundary_theorem: Theorem
    gate_theorem: Theorem


def _real(value: sp.Expr) -> sp.Expr:
    return sp.simplify((value + sp.conjugate(value)) / 2)


@lru_cache(maxsize=1)
def build_certificate() -> Full42CarrierBaseKCompatibilityCertificate:
    frame_data = frame_certificate()
    frame = full_noise_frame()
    incidence = sp.ImmutableMatrix(physical_incidence())
    transfer = tuple(item[11:, :11] for item in frame[:30])

    def left_variation(direction: sp.MatrixBase) -> sp.MatrixBase:
        return direction * incidence.H + incidence * direction.H

    def right_variation(direction: sp.MatrixBase) -> sp.MatrixBase:
        return direction.H * incidence + incidence.H * direction

    scalar_hessian = sp.ImmutableMatrix(
        [
            [
                sp.simplify(
                    2
                    * _real(
                        sp.trace(left_variation(first).H * left_variation(second))
                        + sp.trace(right_variation(first).H * right_variation(second))
                    )
                )
                for second in transfer
            ]
            for first in transfer
        ]
    )

    vacuum = sp.zeros(21)
    vacuum[:11, 11:] = incidence.H
    vacuum[11:, :11] = incidence
    gauge_variations = tuple(sp.I * (generator * vacuum - vacuum * generator) for generator in frame[30:])
    gauge_gram = sp.ImmutableMatrix(
        [[sp.simplify(sp.trace(first.H * second)) for second in gauge_variations] for first in gauge_variations]
    )

    transfer_metric = sp.ImmutableMatrix(frame_data.trace_metric[:30, :30])
    gauge_metric = sp.ImmutableMatrix(frame_data.trace_metric[30:, 30:])
    scalar_mass = sp.ImmutableMatrix(transfer_metric.inv() * scalar_hessian)
    gauge_mass = sp.ImmutableMatrix(3 * gauge_metric.inv() * gauge_gram)
    scalar_fourth = sp.simplify(sp.trace(scalar_mass * scalar_mass))
    gauge_fourth = sp.simplify(sp.trace(gauge_mass * gauge_mass))
    bosonic_fourth = sp.simplify(scalar_fourth + 3 * gauge_fourth)
    fermion_fourth = sp.simplify(sp.trace(vacuum**4))

    scalar_rank = kernel.prove_exact_rank(scalar_hessian, 28, subject="vacuum Gram Hessian rank on the full transfer carrier")
    scalar_nullity = kernel.prove_exact_nullity(scalar_hessian, 2, subject="vacuum Gram Hessian nullity")
    gauge_rank = kernel.prove_exact_rank(gauge_gram, 3, subject="broken gauge rank of the incidence vacuum")
    gauge_nullity = kernel.prove_exact_nullity(gauge_gram, 9, subject="unbroken gauge nullity of the incidence vacuum")
    scalar_fourth_theorem = kernel.prove_expression_equality(scalar_fourth, sp.Rational(23053, 18), subject="normalized scalar fourth mass moment")
    gauge_fourth_theorem = kernel.prove_expression_equality(gauge_fourth, sp.Rational(36897, 722), subject="normalized gauge fourth mass moment")
    bosonic_ledger = kernel.prove_expression_equality(bosonic_fourth, sp.Rational(4659176, 3249), subject="full-carrier bosonic Coleman-Weinberg numerator")
    fermion_moment = kernel.prove_expression_equality(fermion_fourth, 46, subject="raw finite incidence fourth moment")
    multiplicity = sp.Symbol("nu_f", positive=True)
    full_one = bosonic_fourth - 2 * fermion_fourth
    full_two = bosonic_fourth - 4 * fermion_fourth
    full_boundary = kernel.prove_matrix_inequality(sp.Matrix([[full_one]]), sp.Matrix([[full_two]]), subject="full supertrace depends on the unresolved fermion multiplicity")
    gate = kernel.prove_gate(
        "full_42_carrier_base_k_determinant_compatibility",
        (scalar_rank, scalar_nullity, gauge_rank, gauge_nullity, scalar_fourth_theorem, gauge_fourth_theorem, bosonic_ledger, fermion_moment, full_boundary),
    )
    return Full42CarrierBaseKCompatibilityCertificate(
        scalar_hessian=scalar_hessian, gauge_mass_gram=gauge_gram,
        scalar_mass_operator=scalar_mass, gauge_mass_operator=gauge_mass,
        bosonic_fourth_moment=bosonic_fourth, finite_fermion_fourth_moment=fermion_fourth,
        scalar_rank_theorem=scalar_rank, scalar_nullity_theorem=scalar_nullity,
        gauge_rank_theorem=gauge_rank, gauge_nullity_theorem=gauge_nullity,
        scalar_fourth_theorem=scalar_fourth_theorem, gauge_fourth_theorem=gauge_fourth_theorem,
        bosonic_ledger_theorem=bosonic_ledger, fermion_moment_theorem=fermion_moment,
        full_ledger_boundary_theorem=full_boundary, gate_theorem=gate,
    )