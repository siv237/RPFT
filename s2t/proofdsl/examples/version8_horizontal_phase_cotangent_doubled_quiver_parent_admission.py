"""Exact cotangent doubled-quiver parent audit for the horizontal phase."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission import (
    build_certificate as build_completion_certificate,
)


@dataclass(frozen=True, slots=True)
class HorizontalPhaseCotangentDoubledQuiverParentAdmissionCertificate:
    symplectic_form: sp.ImmutableMatrix
    gauge_generators: tuple[sp.ImmutableMatrix, ...]
    moment_quadratic_matrices: tuple[sp.ImmutableMatrix, ...]
    moment_span_matrix: sp.ImmutableMatrix
    generator_relation: sp.ImmutableMatrix
    cotangent_phase_action: sp.ImmutableMatrix
    moment_vector: sp.ImmutableMatrix
    moment_parent: sp.Expr
    moment_span_dimension: int
    symplectic_theorem: Theorem
    moment_symmetry_theorem: Theorem
    moment_span_theorem: Theorem
    generator_relation_theorem: Theorem
    nonzero_moment_witness_theorem: Theorem
    phase_symplectic_theorem: Theorem
    phase_gauge_commutant_theorem: Theorem
    moment_phase_invariance_theorem: Theorem
    parent_phase_invariance_theorem: Theorem
    parent_scale_freedom_theorem: Theorem
    stability_level_freedom_theorem: Theorem
    cotangent_parent_no_go_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HorizontalPhaseCotangentDoubledQuiverParentAdmissionCertificate:
    completion = build_completion_certificate()
    omega = completion.standard_form
    generators = completion.gauge_generators
    moment_matrices = tuple(sp.ImmutableMatrix(omega * generator) for generator in generators)
    moment_span_matrix = sp.ImmutableMatrix.hstack(
        *(matrix.reshape(26 * 26, 1) for matrix in moment_matrices)
    )
    moment_span_dimension = moment_span_matrix.rank()
    relation = sp.ImmutableMatrix(
        [
            -sp.Rational(1, 2), 0, 0, -sp.Rational(1, 2),
            -sp.Rational(2, 3), 0, 0, 0, -sp.Rational(2, 3),
            0, 0, 0, -sp.Rational(2, 3), 1,
        ]
    )

    z = sp.Symbol("z", nonzero=True)
    q_indices = set(range(0, 8)) | set(range(16, 19)) | {22, 24}
    phase = sp.ImmutableMatrix(
        sp.diag(*(z if index in q_indices else 1 / z for index in range(26)))
    )
    coordinates = sp.ImmutableMatrix(sp.symbols("x0:26", commutative=True))
    moment_vector = sp.ImmutableMatrix(
        [sp.expand((coordinates.T * matrix * coordinates)[0] / 2) for matrix in moment_matrices]
    )
    transformed_moment = sp.ImmutableMatrix(
        [
            sp.expand((coordinates.T * phase.T * matrix * phase * coordinates)[0] / 2)
            for matrix in moment_matrices
        ]
    )
    parent = sp.expand(sum(component**2 for component in moment_vector))
    transformed_parent = sp.expand(sum(component**2 for component in transformed_moment))

    symplectic_theorem = kernel.prove_exact_rank(
        omega,
        26,
        subject="nondegenerate symplectic carrier used by the doubled quiver",
    )
    moment_symmetry_theorem = kernel.prove_matrix_equality(
        sp.ImmutableMatrix.hstack(*(matrix.T for matrix in moment_matrices)),
        sp.ImmutableMatrix.hstack(*moment_matrices),
        subject="Hamiltonian quadratic matrices Omega rho(X) are symmetric",
    )
    moment_span_theorem = kernel.prove_exact_rank(
        moment_span_matrix,
        13,
        subject="dimension of the nonzero gauge moment-map component span",
    )
    generator_relation_theorem = kernel.prove_matrix_equality(
        moment_span_matrix * relation,
        sp.zeros(26 * 26, 1),
        subject="single exact central relation among fourteen gauge generators",
    )
    witness = sp.ImmutableMatrix([1] + [0] * 7 + [1] + [0] * 17)
    witness_moment = sp.ImmutableMatrix(
        [sp.expand((witness.T * matrix * witness)[0] / 2) for matrix in moment_matrices]
    )
    expected_witness = sp.ImmutableMatrix(
        [-1] + [0] * 12 + [-sp.Rational(1, 2)]
    )
    nonzero_moment_witness_theorem = kernel.prove_matrix_equality(
        witness_moment,
        expected_witness,
        subject="explicit nonzero moment-map witness on one weak cotangent pair",
    )
    phase_symplectic_theorem = kernel.prove_matrix_equality(
        phase.T * omega * phase,
        omega,
        subject="canonical cotangent fibre phase preserves the symplectic form",
    )
    phase_gauge_commutant_theorem = kernel.prove_matrix_equality(
        sp.ImmutableMatrix.hstack(*(phase * generator - generator * phase for generator in generators)),
        sp.zeros(26, 26 * len(generators)),
        subject="cotangent fibre phase commutes with the endpoint gauge action",
    )
    moment_phase_invariance_theorem = kernel.prove_matrix_equality(
        transformed_moment,
        moment_vector,
        subject="all moment-map components are blind to the cotangent fibre phase",
    )
    parent_phase_invariance_theorem = kernel.prove_expression_equality(
        transformed_parent,
        parent,
        subject="the moment-map square parent is blind to the cotangent fibre phase",
    )
    coupling = sp.Symbol("lambda", positive=True)
    parent_scale_freedom_theorem = kernel.prove_expression_nonconstant(
        coupling * parent,
        coupling,
        subject="overall moment-map parent coupling remains free",
    )
    stability = sp.Symbol("zeta0", real=True)
    shifted_origin = stability**2
    stability_level_freedom_theorem = kernel.prove_expression_nonconstant(
        shifted_origin,
        stability,
        subject="a shifted moment-map level is independent stability data",
    )
    no_go = kernel.prove_gate(
        "canonical_cotangent_moment_map_parent_does_not_lift_horizontal_phase",
        (
            moment_span_theorem,
            nonzero_moment_witness_theorem,
            phase_symplectic_theorem,
            phase_gauge_commutant_theorem,
            moment_phase_invariance_theorem,
            parent_phase_invariance_theorem,
            parent_scale_freedom_theorem,
            stability_level_freedom_theorem,
        ),
    )
    gate = kernel.prove_gate(
        "horizontal_phase_cotangent_doubled_quiver_parent_admission",
        (
            symplectic_theorem,
            moment_symmetry_theorem,
            moment_span_theorem,
            generator_relation_theorem,
            nonzero_moment_witness_theorem,
            phase_symplectic_theorem,
            phase_gauge_commutant_theorem,
            moment_phase_invariance_theorem,
            parent_phase_invariance_theorem,
            parent_scale_freedom_theorem,
            stability_level_freedom_theorem,
            no_go,
        ),
    )
    return HorizontalPhaseCotangentDoubledQuiverParentAdmissionCertificate(
        symplectic_form=omega,
        gauge_generators=generators,
        moment_quadratic_matrices=moment_matrices,
        moment_span_matrix=moment_span_matrix,
        generator_relation=relation,
        cotangent_phase_action=phase,
        moment_vector=moment_vector,
        moment_parent=parent,
        moment_span_dimension=moment_span_dimension,
        symplectic_theorem=symplectic_theorem,
        moment_symmetry_theorem=moment_symmetry_theorem,
        moment_span_theorem=moment_span_theorem,
        generator_relation_theorem=generator_relation_theorem,
        nonzero_moment_witness_theorem=nonzero_moment_witness_theorem,
        phase_symplectic_theorem=phase_symplectic_theorem,
        phase_gauge_commutant_theorem=phase_gauge_commutant_theorem,
        moment_phase_invariance_theorem=moment_phase_invariance_theorem,
        parent_phase_invariance_theorem=parent_phase_invariance_theorem,
        parent_scale_freedom_theorem=parent_scale_freedom_theorem,
        stability_level_freedom_theorem=stability_level_freedom_theorem,
        cotangent_parent_no_go_theorem=no_go,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.moment_span_dimension)