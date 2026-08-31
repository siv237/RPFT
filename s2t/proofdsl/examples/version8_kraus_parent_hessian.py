"""Exact parent-action Hessian certificate for the cross-sector Kraus bridge."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_gauge_twirl_kraus import (
    central_basis,
    cross_arrow_families,
    internal_control_arrows,
    kraus_generator,
)


@dataclass(frozen=True, slots=True)
class KrausParentHessianCertificate:
    cross_coefficient: sp.Expr
    cross_total_coefficient: sp.Expr
    gaussian_unit_rate: sp.Expr
    bridge_hessian: sp.ImmutableMatrix
    coefficient_theorem: Theorem
    control_theorem: Theorem
    hessian_theorem: Theorem
    bridge_signature_theorem: Theorem
    origin_signature_theorem: Theorem
    vacuum_signature_theorem: Theorem
    zero_energy_theorem: Theorem
    zero_gradient_theorem: Theorem
    zero_jump_weights_theorem: Theorem
    covariance_rate_theorem: Theorem
    gaussian_rate_theorem: Theorem


def _contrast() -> sp.ImmutableMatrix:
    quark, lepton = central_basis()
    value = (3 * quark - sp.sqrt(12) * lepton) / sp.sqrt(21)
    assert sp.simplify(sp.trace(value.H * value)) == 1
    return sp.ImmutableMatrix(value)


def _dirichlet_coefficient(arrow: sp.MatrixBase, index: int) -> sp.Expr:
    generator = kraus_generator(f"single_cross_{index}", (sp.ImmutableMatrix(arrow),))
    contrast = _contrast()
    return sp.simplify(-sp.trace(contrast.H * generator.act(contrast)))


def _baseline_hessians() -> tuple[sp.ImmutableMatrix, sp.ImmutableMatrix]:
    root_multiplicities = (3, 3, 1, 1, 1, 1, 1)
    origin = tuple(-4 * value for value in root_multiplicities)
    vacuum = tuple(8 * value for value in root_multiplicities)
    heavy = (sp.Rational(32, 5),) * 12 + (sp.Rational(18, 5),) * 8
    return sp.ImmutableMatrix(sp.diag(*(origin + heavy))), sp.ImmutableMatrix(
        sp.diag(*(vacuum + heavy))
    )


@lru_cache(maxsize=1)
def build_certificate() -> KrausParentHessianCertificate:
    qlyr, xldr = cross_arrow_families()
    cross = qlyr + xldr
    controls = internal_control_arrows()
    cross_coefficients = sp.ImmutableMatrix(
        [_dirichlet_coefficient(arrow, index) for index, arrow in enumerate(cross)]
    )
    control_coefficients = sp.ImmutableMatrix(
        [
            _dirichlet_coefficient(arrow, len(cross) + index)
            for index, arrow in enumerate(controls)
        ]
    )
    expected_cross = sp.ImmutableMatrix([sp.Rational(7, 36)] * 12)
    coefficient_theorem = kernel.prove_matrix_equality(
        cross_coefficients,
        expected_cross,
        subject="individual cross-arrow Dirichlet coefficients",
    )
    control_theorem = kernel.prove_matrix_equality(
        control_coefficients,
        sp.zeros(8, 1),
        subject="internal lepton Dirichlet controls",
    )

    coordinates = sp.symbols("z0:12", real=True)
    energy = sp.Rational(7, 36) * sum(item**2 for item in coordinates)
    field_hessian = sp.hessian(energy, coordinates)
    expected_field_hessian = sp.Rational(7, 18) * sp.eye(12)
    hessian_theorem = kernel.prove_matrix_equality(
        field_hessian,
        expected_field_hessian,
        subject="cross-arrow field Dirichlet Hessian",
    )
    zero_substitution = {item: 0 for item in coordinates}
    zero_energy = kernel.prove_expression_equality(
        energy.subs(zero_substitution),
        0,
        subject="tree-level bridge energy at the Tome VII vacuum",
    )
    zero_gradient = kernel.prove_matrix_equality(
        sp.ImmutableMatrix([sp.diff(energy, item) for item in coordinates]).subs(
            zero_substitution
        ),
        sp.zeros(12, 1),
        subject="cross-arrow stationarity at the Tome VII vacuum",
    )
    zero_jump_weights = kernel.prove_matrix_equality(
        sp.ImmutableMatrix([item**2 for item in coordinates]).subs(zero_substitution),
        sp.zeros(12, 1),
        subject="field-dependent Kraus weights at the Tome VII vacuum",
    )

    bridge_hessian = sp.ImmutableMatrix(
        sp.diag(*((0,) * 7 + (sp.Rational(7, 18),) * 12 + (0,) * 8))
    )
    bridge_signature = kernel.prove_diagonal_signature(
        bridge_hessian,
        (0, 15, 12),
        subject="27-dimensional bridge Hessian",
    )
    weight = sp.Symbol("lambda_bridge", nonnegative=True)
    origin, vacuum = _baseline_hessians()
    origin_signature = kernel.prove_diagonal_signature(
        origin + weight * bridge_hessian,
        (7, 0, 20),
        subject="Tome VII origin plus every nonnegative bridge weight",
    )
    vacuum_signature = kernel.prove_diagonal_signature(
        vacuum + weight * bridge_hessian,
        (0, 0, 27),
        subject="Tome VII target plus every nonnegative bridge weight",
    )

    covariance_q = sp.Symbol("c_Q", positive=True)
    covariance_x = sp.Symbol("c_X", positive=True)
    rate_from_directions = 6 * sp.Rational(7, 36) * (
        covariance_q + covariance_x
    )
    expected_rate = sp.Rational(7, 6) * (covariance_q + covariance_x)
    covariance_rate = kernel.prove_expression_equality(
        rate_from_directions,
        expected_rate,
        subject="two-family covariance-induced central rate",
    )
    gaussian_rate = 12 * sp.Rational(7, 36) / sp.Rational(32, 5)
    gaussian_theorem = kernel.prove_expression_equality(
        gaussian_rate,
        sp.Rational(35, 96),
        subject="unit-strength Gaussian heavy-Hessian probe",
    )

    return KrausParentHessianCertificate(
        cross_coefficient=sp.Rational(7, 36),
        cross_total_coefficient=sp.Rational(7, 3),
        gaussian_unit_rate=sp.Rational(35, 96),
        bridge_hessian=bridge_hessian,
        coefficient_theorem=coefficient_theorem,
        control_theorem=control_theorem,
        hessian_theorem=hessian_theorem,
        bridge_signature_theorem=bridge_signature,
        origin_signature_theorem=origin_signature,
        vacuum_signature_theorem=vacuum_signature,
        zero_energy_theorem=zero_energy,
        zero_gradient_theorem=zero_gradient,
        zero_jump_weights_theorem=zero_jump_weights,
        covariance_rate_theorem=covariance_rate,
        gaussian_rate_theorem=gaussian_theorem,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.cross_coefficient)
    print(certificate.origin_signature_theorem.proposition)