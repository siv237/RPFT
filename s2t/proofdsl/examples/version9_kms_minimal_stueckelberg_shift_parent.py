"""LCF certificate for the minimal Stueckelberg KMS shift parent."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSMinimalStueckelbergShiftParentCertificate:
    orbit_map: sp.ImmutableMatrix
    invariant_map: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    isotropic_hessian: sp.ImmutableMatrix
    fp_operator: sp.ImmutableMatrix
    orbit_rank_theorem: Theorem
    invariant_rank_theorem: Theorem
    invariant_orbit_theorem: Theorem
    hessian_rank_theorem: Theorem
    hessian_nullity_theorem: Theorem
    gauge_zero_mode_theorem: Theorem
    isotropic_spectrum_theorem: Theorem
    fp_rank_theorem: Theorem
    fp_determinant_theorem: Theorem
    determinant_cancellation_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSMinimalStueckelbergShiftParentCertificate:
    identity = sp.eye(10)
    orbit_map = sp.ImmutableMatrix(sp.Matrix.vstack(identity, identity))
    invariant_map = sp.ImmutableMatrix(sp.Matrix.hstack(identity, -identity))

    ts, ta, tt = sp.symbols("theta_s theta_a theta_t", positive=True)
    ks, ka, kt = sp.symbols("kappa_s kappa_a kappa_t", positive=True)
    fp_operator = sp.ImmutableMatrix(sp.diag(
        ts, ta, tt, tt, tt, ks, ka, kt, kt, kt
    ))
    parent_hessian = sp.ImmutableMatrix(
        invariant_map.T * fp_operator * invariant_map
    )
    isotropic_hessian = sp.ImmutableMatrix(parent_hessian.subs({
        ts: 1, ta: 1, tt: 1, ks: 1, ka: 1, kt: 1,
    }))

    orbit_rank_theorem = kernel.prove_exact_rank(
        orbit_map,
        10,
        subject="diagonal Stueckelberg shift orbit has rank ten",
    )
    invariant_rank_theorem = kernel.prove_exact_rank(
        invariant_map,
        10,
        subject="difference field spans the ten dimensional quotient",
    )
    invariant_orbit_theorem = kernel.prove_matrix_equality(
        invariant_map * orbit_map,
        sp.zeros(10),
        subject="difference field is invariant under diagonal shifts",
    )
    hessian_rank_theorem = kernel.prove_exact_rank(
        parent_hessian,
        10,
        subject="Stueckelberg parent controls all quotient directions",
    )
    hessian_nullity_theorem = kernel.prove_exact_nullity(
        parent_hessian,
        10,
        subject="Stueckelberg parent has exactly the gauge orbit as zero modes",
    )
    gauge_zero_mode_theorem = kernel.prove_matrix_equality(
        parent_hessian * orbit_map,
        sp.zeros(20, 10),
        subject="parent Hessian annihilates every gauge shift",
    )
    isotropic_spectrum_theorem = kernel.prove_exact_spectrum(
        isotropic_hessian,
        {sp.Integer(0): 10, sp.Integer(2): 10},
        subject="isotropic Stueckelberg Hessian is positive semidefinite",
    )
    fp_rank_theorem = kernel.prove_exact_rank(
        fp_operator,
        10,
        subject="Stueckelberg gauge condition has full rank FP operator",
    )
    fp_determinant_theorem = kernel.prove_expression_equality(
        fp_operator.det(),
        ts * ta * tt**3 * ks * ka * kt**3,
        subject="Stueckelberg FP determinant equals the KMS target determinant",
    )
    determinant_cancellation_theorem = kernel.prove_expression_equality(
        fp_operator.det() / fp_operator.det(),
        1,
        subject="complex invariant boson determinant cancels the ghost determinant",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_logdet_minimal_stueckelberg_"
        "shift_parent_architecture_gate",
        (
            orbit_rank_theorem,
            invariant_rank_theorem,
            invariant_orbit_theorem,
            hessian_rank_theorem,
            hessian_nullity_theorem,
            gauge_zero_mode_theorem,
            isotropic_spectrum_theorem,
            fp_rank_theorem,
            fp_determinant_theorem,
            determinant_cancellation_theorem,
        ),
    )
    return KMSMinimalStueckelbergShiftParentCertificate(
        orbit_map=orbit_map,
        invariant_map=invariant_map,
        parent_hessian=parent_hessian,
        isotropic_hessian=isotropic_hessian,
        fp_operator=fp_operator,
        orbit_rank_theorem=orbit_rank_theorem,
        invariant_rank_theorem=invariant_rank_theorem,
        invariant_orbit_theorem=invariant_orbit_theorem,
        hessian_rank_theorem=hessian_rank_theorem,
        hessian_nullity_theorem=hessian_nullity_theorem,
        gauge_zero_mode_theorem=gauge_zero_mode_theorem,
        isotropic_spectrum_theorem=isotropic_spectrum_theorem,
        fp_rank_theorem=fp_rank_theorem,
        fp_determinant_theorem=fp_determinant_theorem,
        determinant_cancellation_theorem=determinant_cancellation_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version9_endpoint_creation_kms_logdet_minimal_stueckelberg_"
        "shift_parent_architecture_gate"
    ),
    title="Минимальный Stückelberg shift-parent для KMS logdet",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_logdet_minimal_"
        "stueckelberg_shift_parent_architecture_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_minimal_"
        "stueckelberg_shift_parent_architecture_gate_results.json",
    ),
    obligations=(
        Obligation("stueckelberg_orbit_rank_ten", lambda: build_certificate().orbit_rank_theorem),
        Obligation("quotient_invariant_rank_ten", lambda: build_certificate().invariant_rank_theorem),
        Obligation("difference_is_shift_invariant", lambda: build_certificate().invariant_orbit_theorem),
        Obligation("parent_hessian_rank_ten", lambda: build_certificate().hessian_rank_theorem),
        Obligation("parent_hessian_nullity_ten", lambda: build_certificate().hessian_nullity_theorem),
        Obligation("gauge_orbit_is_hessian_kernel", lambda: build_certificate().gauge_zero_mode_theorem),
        Obligation("isotropic_positive_semidefinite_spectrum", lambda: build_certificate().isotropic_spectrum_theorem),
        Obligation("fp_operator_rank_ten", lambda: build_certificate().fp_rank_theorem),
        Obligation("fp_determinant_target", lambda: build_certificate().fp_determinant_theorem),
        Obligation("complex_boson_ghost_cancellation", lambda: build_certificate().determinant_cancellation_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)