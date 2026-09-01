"""LCF certificate for the origin audit of the KMS BRST shift symmetry."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSBRSTShiftSymmetryOriginCertificate:
    required_shift_map: sp.ImmutableMatrix
    kms_parameter_tangent: sp.ImmutableMatrix
    normalized_shape_tangent: sp.ImmutableMatrix
    phase_laplacian: sp.ImmutableMatrix
    trivial_parent_hessian: sp.ImmutableMatrix
    positive_parent_hessian: sp.ImmutableMatrix
    required_rank_theorem: Theorem
    parameter_rank_theorem: Theorem
    parameter_cokernel_theorem: Theorem
    shape_rank_theorem: Theorem
    phase_nullity_theorem: Theorem
    type_orbit_theorem: Theorem
    transport_tangent_theorem: Theorem
    trivial_hessian_theorem: Theorem
    positive_hessian_theorem: Theorem
    translation_breaking_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSBRSTShiftSymmetryOriginCertificate:
    required_shift_map = sp.ImmutableMatrix(sp.eye(10))
    kms_parameter_tangent = sp.ImmutableMatrix([
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1],
    ])
    normalized_shape_tangent = sp.ImmutableMatrix([
        [4, -1, 0, 0],
        [-1, 4, 0, 0],
        [-1, -1, 0, 0],
        [-1, -1, 0, 0],
        [-1, -1, 0, 0],
        [0, 0, 4, -1],
        [0, 0, -1, 4],
        [0, 0, -1, -1],
        [0, 0, -1, -1],
        [0, 0, -1, -1],
    ])
    phase_laplacian = sp.ImmutableMatrix([
        [1, -1, 0],
        [-1, 2, -1],
        [0, -1, 1],
    ])
    type_orbit = sp.ImmutableMatrix(sp.zeros(10, 2))
    transport_tangent = sp.ImmutableMatrix(sp.zeros(10, 1))
    trivial_parent_hessian = sp.ImmutableMatrix(sp.zeros(10))

    ds = sp.symbols("d_0:10", positive=True)
    positive_parent_hessian = sp.ImmutableMatrix(sp.diag(*ds))

    required_rank_theorem = kernel.prove_exact_rank(
        required_shift_map,
        10,
        subject="BRST translation orbit must span all ten auxiliary directions",
    )
    parameter_rank_theorem = kernel.prove_exact_rank(
        kms_parameter_tangent,
        6,
        subject="all KMS type parameters span only six diagonal directions",
    )
    parameter_cokernel_theorem = kernel.prove_exact_nullity(
        kms_parameter_tangent.T,
        4,
        subject="KMS parameter tangent has four dimensional cokernel",
    )
    shape_rank_theorem = kernel.prove_exact_rank(
        normalized_shape_tangent,
        4,
        subject="normalized KMS shapes span four relative directions",
    )
    phase_nullity_theorem = kernel.prove_exact_nullity(
        phase_laplacian,
        1,
        subject="endpoint phase graph supplies only one zero mode",
    )
    type_orbit_theorem = kernel.prove_exact_rank(
        type_orbit,
        0,
        subject="type conjugations fix scalar isotypic KMS blocks",
    )
    transport_tangent_theorem = kernel.prove_exact_rank(
        transport_tangent,
        0,
        subject="discrete transport orientation has no continuous translation tangent",
    )
    trivial_hessian_theorem = kernel.prove_exact_rank(
        trivial_parent_hessian,
        0,
        subject="zero action spectator extension has a ten dimensional flat orbit",
    )
    positive_hessian_theorem = kernel.prove_exact_rank(
        positive_parent_hessian,
        10,
        subject="any positive auxiliary quadratic parent removes all shift directions",
    )
    translation_breaking_theorem = kernel.prove_matrix_inequality(
        positive_parent_hessian * required_shift_map,
        sp.zeros(10),
        subject="positive auxiliary parent is not invariant under full translations",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_logdet_brst_shift_symmetry_"
        "parent_origin_gate",
        (
            required_rank_theorem,
            parameter_rank_theorem,
            parameter_cokernel_theorem,
            shape_rank_theorem,
            phase_nullity_theorem,
            type_orbit_theorem,
            transport_tangent_theorem,
            trivial_hessian_theorem,
            positive_hessian_theorem,
            translation_breaking_theorem,
        ),
    )
    return KMSBRSTShiftSymmetryOriginCertificate(
        required_shift_map=required_shift_map,
        kms_parameter_tangent=kms_parameter_tangent,
        normalized_shape_tangent=normalized_shape_tangent,
        phase_laplacian=phase_laplacian,
        trivial_parent_hessian=trivial_parent_hessian,
        positive_parent_hessian=positive_parent_hessian,
        required_rank_theorem=required_rank_theorem,
        parameter_rank_theorem=parameter_rank_theorem,
        parameter_cokernel_theorem=parameter_cokernel_theorem,
        shape_rank_theorem=shape_rank_theorem,
        phase_nullity_theorem=phase_nullity_theorem,
        type_orbit_theorem=type_orbit_theorem,
        transport_tangent_theorem=transport_tangent_theorem,
        trivial_hessian_theorem=trivial_hessian_theorem,
        positive_hessian_theorem=positive_hessian_theorem,
        translation_breaking_theorem=translation_breaking_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version9_endpoint_creation_kms_logdet_brst_shift_symmetry_"
        "parent_origin_gate"
    ),
    title="Parent-origin десятипараметрической BRST shift-symmetry",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_logdet_brst_shift_"
        "symmetry_parent_origin_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_brst_shift_"
        "symmetry_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("required_shift_rank_ten", lambda: build_certificate().required_rank_theorem),
        Obligation("kms_parameter_rank_six", lambda: build_certificate().parameter_rank_theorem),
        Obligation("kms_parameter_cokernel_four", lambda: build_certificate().parameter_cokernel_theorem),
        Obligation("normalized_shape_rank_four", lambda: build_certificate().shape_rank_theorem),
        Obligation("endpoint_phase_nullity_one", lambda: build_certificate().phase_nullity_theorem),
        Obligation("type_conjugation_orbit_rank_zero", lambda: build_certificate().type_orbit_theorem),
        Obligation("transport_tangent_rank_zero", lambda: build_certificate().transport_tangent_theorem),
        Obligation("trivial_spectator_hessian_rank_zero", lambda: build_certificate().trivial_hessian_theorem),
        Obligation("positive_auxiliary_hessian_rank_ten", lambda: build_certificate().positive_hessian_theorem),
        Obligation("positive_parent_breaks_translation", lambda: build_certificate().translation_breaking_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)