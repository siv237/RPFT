"""Exact certificate for the microscopic repeated-interaction Hamiltonian."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from ..structures import Morphism, Space
from .version8_gauge_twirl_kraus import (
    _endpoint_gauge_generators,
    build_certificate as build_gauge_certificate,
    cross_arrow_families,
    kraus_generator,
)
from .version8_noise_clock import build_certificate as build_noise_clock_certificate


SYSTEM_DIMENSION = 21
JUMP_DIMENSION = 12
ENVIRONMENT_DIMENSION = 13
AMBIENT_DIMENSION = SYSTEM_DIMENSION * ENVIRONMENT_DIMENSION


@dataclass(frozen=True, slots=True)
class MicroscopicInteractionHamiltonianCertificate:
    system_dimension: int
    environment_dimension: int
    ambient_dimension: int
    jump_dimension: int
    full_commutant_dimension: int
    symmetric_rate_metric_dimension: int
    finite_step_witness: tuple[int, int]
    typed_theorem: Theorem
    hermiticity_theorem: Theorem
    vacuum_second_moment_theorem: Theorem
    tangent_theorem: Theorem
    covariance_theorem: Theorem
    coupling_commutant_theorem: Theorem
    finite_step_no_go_theorem: Theorem
    scale_no_go_theorem: Theorem
    collision_limit_theorem: Theorem


def _jumps() -> tuple[sp.ImmutableMatrix, ...]:
    qlyr, xldr = cross_arrow_families()
    generator = kraus_generator("microscopic_cross_frame", qlyr + xldr)
    return tuple(jump.matrix for jump in generator.jumps)


def _jump_sum(jumps: tuple[sp.ImmutableMatrix, ...]) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(
        sum((jump.H * jump for jump in jumps), sp.zeros(SYSTEM_DIMENSION))
    )


def _star_hamiltonian(jumps: tuple[sp.ImmutableMatrix, ...]) -> sp.ImmutableMatrix:
    vacuum_to_jumps = sp.Matrix.vstack(*jumps)
    return sp.ImmutableMatrix(
        sp.Matrix.vstack(
            sp.Matrix.hstack(sp.zeros(SYSTEM_DIMENSION), vacuum_to_jumps.H),
            sp.Matrix.hstack(
                vacuum_to_jumps,
                sp.zeros(SYSTEM_DIMENSION * JUMP_DIMENSION),
            ),
        )
    )


def _corner_basis() -> tuple[tuple[int, int, sp.ImmutableMatrix], ...]:
    basis = []
    for start, dimension in ((0, 11), (11, 10)):
        for row in range(dimension):
            for column in range(dimension):
                unit = sp.zeros(SYSTEM_DIMENSION)
                unit[start + row, start + column] = 1
                basis.append((start + row, start + column, sp.ImmutableMatrix(unit)))
    return tuple(basis)


def _second_order_coefficients(
    observable: sp.MatrixBase,
    jumps: tuple[sp.ImmutableMatrix, ...],
    gram: sp.ImmutableMatrix,
) -> tuple[sp.ImmutableMatrix, sp.ImmutableMatrix]:
    jump_image = sum(
        (jump * observable * jump for jump in jumps),
        sp.zeros(SYSTEM_DIMENSION),
    )
    gram_squared = gram * gram
    star = (
        gram * observable * gram / 4
        + (gram_squared * observable + observable * gram_squared) / 24
        - (gram * jump_image + jump_image * gram) / 6
    )
    exact_kraus = (
        gram * observable * gram / 4
        - (gram_squared * observable + observable * gram_squared) / 8
    )
    return sp.ImmutableMatrix(star), sp.ImmutableMatrix(exact_kraus)


@lru_cache(maxsize=1)
def build_certificate() -> MicroscopicInteractionHamiltonianCertificate:
    jumps = _jumps()
    gram = _jump_sum(jumps)
    hamiltonian_matrix = _star_hamiltonian(jumps)
    ambient = Space("H_system tensor K_env", AMBIENT_DIMENSION)
    hamiltonian = Morphism(
        "H_int_star", ambient, ambient, hamiltonian_matrix
    )
    typed = kernel.prove_well_typed_morphism(hamiltonian)
    hermiticity = kernel.prove_matrix_equality(
        hamiltonian_matrix,
        hamiltonian_matrix.H,
        subject="Hermiticity of the vacuum-to-cross star interaction",
    )

    vacuum_to_jumps = sp.Matrix.vstack(*jumps)
    vacuum_second_moment = kernel.prove_matrix_equality(
        vacuum_to_jumps.H * vacuum_to_jumps,
        gram,
        subject="vacuum second moment of the star interaction",
    )

    step = sp.Symbol("h", nonnegative=True)
    no_jump_tangent = sp.eye(SYSTEM_DIMENSION) - step * gram / 2
    unitary_jump_tangents = tuple(-sp.I * jump for jump in jumps)
    tangent = kernel.prove_kraus_family_tangent(
        no_jump_tangent,
        unitary_jump_tangents,
        step,
        subject="weak repeated-interaction tangent equals cross-arrow GKSL",
        premises=(hermiticity, vacuum_second_moment),
    )

    gauge = build_gauge_certificate()
    covariance = kernel.prove_orthogonal_star_interaction_covariance(
        gauge.gauge_covariance_theorem,
        hermiticity,
        environment_dimension=ENVIRONMENT_DIMENSION,
        subject="gauge-invariant contraction of the cross frame with its environment dual",
    )
    coupling_commutant = kernel.prove_orthogonal_frame_commutant_dimensions(
        jumps,
        _endpoint_gauge_generators(),
        expected_full_dimension=8,
        expected_symmetric_dimension=4,
        subject="gauge-compatible couplings of the two equivalent cross families",
    )

    witness = None
    star_second = None
    kraus_second = None
    for row, column, observable in _corner_basis():
        star_candidate, kraus_candidate = _second_order_coefficients(
            observable, jumps, gram
        )
        if star_candidate != kraus_candidate:
            witness = (row, column)
            star_second = star_candidate
            kraus_second = kraus_candidate
            break
    assert witness is not None and star_second is not None and kraus_second is not None
    finite_step_no_go = kernel.prove_matrix_inequality(
        star_second,
        kraus_second,
        subject="second-order star-unitary channel differs from the exact finite Kraus step",
    )

    coupling_scale = sp.Symbol("g", positive=True)
    scale_no_go = kernel.prove_expression_nonconstant(
        coupling_scale**2,
        coupling_scale,
        subject="macroscopic GKSL rate retains the microscopic coupling scale",
    )
    collision_limit = build_noise_clock_certificate().collision_limit_theorem

    return MicroscopicInteractionHamiltonianCertificate(
        system_dimension=SYSTEM_DIMENSION,
        environment_dimension=ENVIRONMENT_DIMENSION,
        ambient_dimension=AMBIENT_DIMENSION,
        jump_dimension=JUMP_DIMENSION,
        full_commutant_dimension=8,
        symmetric_rate_metric_dimension=4,
        finite_step_witness=witness,
        typed_theorem=typed,
        hermiticity_theorem=hermiticity,
        vacuum_second_moment_theorem=vacuum_second_moment,
        tangent_theorem=tangent,
        covariance_theorem=covariance,
        coupling_commutant_theorem=coupling_commutant,
        finite_step_no_go_theorem=finite_step_no_go,
        scale_no_go_theorem=scale_no_go,
        collision_limit_theorem=collision_limit,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.coupling_commutant_theorem.proposition)
    print(certificate.finite_step_witness)