"""LCF certificate for the origin audit of KMS auxiliary fermion parity."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSAuxiliaryFermionStatisticsOriginCertificate:
    type_grading: sp.ImmutableMatrix
    candidate_gradings: tuple[sp.ImmutableMatrix, ...]
    target_grading: sp.ImmutableMatrix
    closest_defect: sp.ImmutableMatrix
    type_spectrum_theorem: Theorem
    plus_plus_spectrum_theorem: Theorem
    plus_minus_spectrum_theorem: Theorem
    minus_plus_spectrum_theorem: Theorem
    minus_minus_spectrum_theorem: Theorem
    mixed_swap_breaking_theorem: Theorem
    equal_swap_covariance_theorem: Theorem
    closest_defect_rank_theorem: Theorem
    target_involution_theorem: Theorem
    paired_jacobian_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSAuxiliaryFermionStatisticsOriginCertificate:
    type_grading = sp.ImmutableMatrix(sp.diag(1, -1, 1, 1, 1))

    def package_grading(theta_sign: int, kappa_sign: int) -> sp.ImmutableMatrix:
        return sp.ImmutableMatrix(sp.diag(
            theta_sign * type_grading,
            kappa_sign * type_grading,
        ))

    plus_plus = package_grading(1, 1)
    plus_minus = package_grading(1, -1)
    minus_plus = package_grading(-1, 1)
    minus_minus = package_grading(-1, -1)
    candidate_gradings = (plus_plus, plus_minus, minus_plus, minus_minus)
    target_grading = sp.ImmutableMatrix(-sp.eye(10))
    closest_defect = sp.ImmutableMatrix(target_grading - minus_minus)

    package_swap = sp.ImmutableMatrix(sp.Matrix.vstack(
        sp.Matrix.hstack(sp.zeros(5), sp.eye(5)),
        sp.Matrix.hstack(sp.eye(5), sp.zeros(5)),
    ))

    scales = sp.symbols("s_0:10", positive=True)
    basis_change = sp.diag(*scales)
    dual_change = sp.diag(*(1 / scale for scale in scales))

    type_spectrum_theorem = kernel.prove_exact_spectrum(
        type_grading,
        {sp.Integer(-1): 1, sp.Integer(1): 4},
        subject="physical channel grading has one odd and four even types",
    )
    plus_plus_spectrum_theorem = kernel.prove_exact_spectrum(
        plus_plus,
        {sp.Integer(-1): 2, sp.Integer(1): 8},
        subject="even even package parity leaves only two odd directions",
    )
    plus_minus_spectrum_theorem = kernel.prove_exact_spectrum(
        plus_minus,
        {sp.Integer(-1): 5, sp.Integer(1): 5},
        subject="even odd package parity gives five odd directions",
    )
    minus_plus_spectrum_theorem = kernel.prove_exact_spectrum(
        minus_plus,
        {sp.Integer(-1): 5, sp.Integer(1): 5},
        subject="odd even package parity gives five odd directions",
    )
    minus_minus_spectrum_theorem = kernel.prove_exact_spectrum(
        minus_minus,
        {sp.Integer(-1): 8, sp.Integer(1): 2},
        subject="odd odd package parity still leaves two even directions",
    )
    mixed_swap_breaking_theorem = kernel.prove_matrix_inequality(
        package_swap * plus_minus,
        plus_minus * package_swap,
        subject="mixed package parity breaks theta kappa exchange covariance",
    )
    equal_swap_covariance_theorem = kernel.prove_matrix_equality(
        package_swap * minus_minus,
        minus_minus * package_swap,
        subject="equal package parity preserves theta kappa exchange covariance",
    )
    closest_defect_rank_theorem = kernel.prove_exact_rank(
        closest_defect,
        2,
        subject="closest inherited grading misses two antisymmetric channel copies",
    )
    target_involution_theorem = kernel.prove_matrix_equality(
        target_grading**2,
        sp.eye(10),
        subject="externally seeded all odd grading is a valid involution",
    )
    paired_jacobian_theorem = kernel.prove_expression_equality(
        basis_change.det() * dual_change.det(),
        1,
        subject="paired psi dual psi Berezin density cancels basis Jacobians",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_logdet_auxiliary_fermion_"
        "statistics_parent_origin_gate",
        (
            type_spectrum_theorem,
            plus_plus_spectrum_theorem,
            plus_minus_spectrum_theorem,
            minus_plus_spectrum_theorem,
            minus_minus_spectrum_theorem,
            mixed_swap_breaking_theorem,
            equal_swap_covariance_theorem,
            closest_defect_rank_theorem,
            target_involution_theorem,
            paired_jacobian_theorem,
        ),
    )
    return KMSAuxiliaryFermionStatisticsOriginCertificate(
        type_grading=type_grading,
        candidate_gradings=candidate_gradings,
        target_grading=target_grading,
        closest_defect=closest_defect,
        type_spectrum_theorem=type_spectrum_theorem,
        plus_plus_spectrum_theorem=plus_plus_spectrum_theorem,
        plus_minus_spectrum_theorem=plus_minus_spectrum_theorem,
        minus_plus_spectrum_theorem=minus_plus_spectrum_theorem,
        minus_minus_spectrum_theorem=minus_minus_spectrum_theorem,
        mixed_swap_breaking_theorem=mixed_swap_breaking_theorem,
        equal_swap_covariance_theorem=equal_swap_covariance_theorem,
        closest_defect_rank_theorem=closest_defect_rank_theorem,
        target_involution_theorem=target_involution_theorem,
        paired_jacobian_theorem=paired_jacobian_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version9_endpoint_creation_kms_logdet_auxiliary_fermion_"
        "statistics_parent_origin_gate"
    ),
    title="Parent-origin нечётной статистики auxiliary KMS fermion module",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_logdet_auxiliary_fermion_"
        "statistics_parent_origin_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_auxiliary_fermion_"
        "statistics_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("physical_type_grading_spectrum", lambda: build_certificate().type_spectrum_theorem),
        Obligation("package_parity_plus_plus", lambda: build_certificate().plus_plus_spectrum_theorem),
        Obligation("package_parity_plus_minus", lambda: build_certificate().plus_minus_spectrum_theorem),
        Obligation("package_parity_minus_plus", lambda: build_certificate().minus_plus_spectrum_theorem),
        Obligation("package_parity_minus_minus", lambda: build_certificate().minus_minus_spectrum_theorem),
        Obligation("mixed_package_swap_breaking", lambda: build_certificate().mixed_swap_breaking_theorem),
        Obligation("equal_package_swap_covariance", lambda: build_certificate().equal_swap_covariance_theorem),
        Obligation("closest_grading_defect_rank_two", lambda: build_certificate().closest_defect_rank_theorem),
        Obligation("conditional_all_odd_involution", lambda: build_certificate().target_involution_theorem),
        Obligation("paired_berezin_jacobian_cancellation", lambda: build_certificate().paired_jacobian_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)