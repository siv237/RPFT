"""Exact dimensionless-time and collision-limit certificate for Tome VIII."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_gauge_twirl_kraus import (
    cross_arrow_families,
    kraus_generator,
)
from .version8_stinespring import build_certificate as build_stinespring_certificate


@dataclass(frozen=True, slots=True)
class NoiseClockCertificate:
    spectrum: tuple[tuple[sp.Expr, int], ...]
    kernel_dimension: int
    unit_gap: sp.Expr
    maximum_decay: sp.Expr
    dissipative_projector_norm_squared: sp.Expr
    gksl_theorem: Theorem
    spectrum_theorem: Theorem
    semigroup_theorem: Theorem
    rate_scaling_theorem: Theorem
    uniform_modular_theorem: Theorem
    central_modular_theorem: Theorem
    dissipative_motion_theorem: Theorem
    collision_limit_theorem: Theorem


def _corner_basis() -> tuple[sp.ImmutableMatrix, ...]:
    basis = []
    for start, dimension in ((0, 11), (11, 10)):
        for row in range(dimension):
            for column in range(dimension):
                unit = sp.zeros(21)
                unit[start + row, start + column] = 1
                basis.append(sp.ImmutableMatrix(unit))
    return tuple(basis)


def _corner_coordinates(matrix: sp.MatrixBase) -> sp.ImmutableMatrix:
    entries = []
    for start, dimension in ((0, 11), (11, 10)):
        for row in range(dimension):
            for column in range(dimension):
                entries.append(matrix[start + row, start + column])
    return sp.ImmutableMatrix(entries)


def _corner_superoperator(generator) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix.hstack(
        *[_corner_coordinates(generator.act(unit)) for unit in _corner_basis()]
    )


def _sector_projectors() -> tuple[sp.ImmutableMatrix, sp.ImmutableMatrix]:
    quark_source = sp.diag(*([1] * 6 + [0] * 5))
    quark_target = sp.diag(*([1] * 6 + [0] * 4))
    quark = sp.ImmutableMatrix(sp.diag(quark_source, quark_target))
    return quark, sp.ImmutableMatrix(sp.eye(21) - quark)


@lru_cache(maxsize=1)
def build_certificate() -> NoiseClockCertificate:
    qlyr, xldr = cross_arrow_families()
    generator = kraus_generator("cross_noise_clock", qlyr + xldr)
    superoperator = _corner_superoperator(generator)
    decay = -superoperator
    expected = {
        sp.Integer(0): 46,
        sp.Rational(1, 2): 48,
        sp.Integer(1): 62,
        sp.Rational(3, 2): 20,
        sp.Integer(2): 8,
        sp.Rational(5, 2): 12,
        sp.Integer(3): 8,
        sp.Rational(7, 2): 12,
        sp.Integer(4): 4,
        sp.Integer(8): 1,
    }
    spectrum_theorem = kernel.prove_exact_spectrum(
        decay, expected, subject="cross-arrow decay spectrum on the endpoint algebra"
    )
    u = sp.Symbol("u", nonnegative=True)
    semigroup = kernel.prove_matrix_exponential_semigroup(
        superoperator, u, subject="dimensionless cross-arrow Lindblad flow"
    )
    kappa = sp.Symbol("kappa", positive=True)
    scaling = kernel.prove_positive_scalar_kernel_invariance(
        superoperator,
        kappa,
        subject="positive physical-rate rescaling of the cross generator",
        premises=(spectrum_theorem,),
    )

    quark, lepton = _sector_projectors()
    uniform_modular_hamiltonian = sp.log(21) * sp.eye(21)
    uniform_modular = kernel.prove_matrix_equality(
        uniform_modular_hamiltonian * quark - quark * uniform_modular_hamiltonian,
        sp.zeros(21),
        subject="uniform-state modular action on the quark projector",
    )
    a = sp.Symbol("a", positive=True)
    b = sp.Symbol("b", positive=True)
    central_modular_hamiltonian = -sp.log(a / 12) * quark - sp.log(b / 9) * lepton
    central_modular = kernel.prove_matrix_equality(
        sp.Matrix.hstack(
            central_modular_hamiltonian * quark - quark * central_modular_hamiltonian,
            central_modular_hamiltonian * lepton - lepton * central_modular_hamiltonian,
        ),
        sp.zeros(21, 42),
        subject="all faithful central modular flows fix both sector populations",
    )
    motion = generator.act(quark)
    norm_squared = sp.simplify(sp.trace(motion.H * motion))
    dissipative_motion = kernel.prove_expression_equality(
        norm_squared,
        sp.Integer(72),
        subject="cross dissipation moves the quark population projector",
    )

    stinespring = build_stinespring_certificate()
    collision_limit = kernel.prove_finite_dimensional_collision_limit(
        stinespring.tangent_theorem,
        stinespring.step_window_theorem,
        subject="fresh-ancilla weak-collision approximation of exp(u L_cross)",
    )
    spectrum = tuple(sorted(expected.items(), key=lambda item: sp.default_sort_key(item[0])))
    return NoiseClockCertificate(
        spectrum=spectrum,
        kernel_dimension=46,
        unit_gap=sp.Rational(1, 2),
        maximum_decay=sp.Integer(8),
        dissipative_projector_norm_squared=norm_squared,
        gksl_theorem=generator.theorem,
        spectrum_theorem=spectrum_theorem,
        semigroup_theorem=semigroup,
        rate_scaling_theorem=scaling,
        uniform_modular_theorem=uniform_modular,
        central_modular_theorem=central_modular,
        dissipative_motion_theorem=dissipative_motion,
        collision_limit_theorem=collision_limit,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.spectrum)
    print(certificate.collision_limit_theorem.proposition)