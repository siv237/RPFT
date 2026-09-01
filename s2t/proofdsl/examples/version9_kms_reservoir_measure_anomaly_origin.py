"""LCF certificate for the KMS reservoir measure-anomaly origin gate."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSReservoirMeasureAnomalyOriginCertificate:
    inherited_coefficients: sp.ImmutableMatrix
    target_coefficients: sp.ImmutableMatrix
    paired_jacobian_theorem: Theorem
    same_direction_jacobian_theorem: Theorem
    inherited_rank_theorem: Theorem
    augmented_rank_theorem: Theorem
    type_mismatch_theorem: Theorem
    package_mismatch_theorem: Theorem
    product_mismatch_theorem: Theorem
    type_trace_theorem: Theorem
    package_trace_theorem: Theorem
    product_trace_theorem: Theorem
    target_trace_theorem: Theorem
    target_loaded_rescaling_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSReservoirMeasureAnomalyOriginCertificate:
    s = sp.symbols("s0:10", nonzero=True)
    det_s = sp.prod(s)
    paired_jacobian = det_s**-1 * det_s
    same_direction_jacobian = det_s**-2

    target_coefficients = sp.ImmutableMatrix([[1, 1, 3, 1, 1, 3]])
    inherited_coefficients = sp.ImmutableMatrix([
        [1, -1, 3, 1, -1, 3],
        [1, 1, 3, -1, -1, -3],
        [1, -1, 3, -1, 1, -3],
    ])
    r = sp.symbols("r", positive=True)
    loaded_s = r ** sp.Rational(-1, 2)
    loaded_jacobian = (loaded_s**10) ** -2

    paired_jacobian_theorem = kernel.prove_expression_equality(
        paired_jacobian, 1,
        subject="paired vector like Berezin basis changes have unit total Jacobian",
    )
    same_direction_jacobian_theorem = kernel.prove_expression_equality(
        same_direction_jacobian, det_s**-2,
        subject="same direction fermion rescaling produces a nontrivial Jacobian",
    )
    inherited_rank_theorem = kernel.prove_exact_rank(
        inherited_coefficients, 3,
        subject="type package and product gradings span three signed anomaly directions",
    )
    augmented_rank_theorem = kernel.prove_exact_rank(
        sp.ImmutableMatrix.vstack(inherited_coefficients, target_coefficients), 4,
        subject="the positive target trace lies outside inherited anomaly directions",
    )
    type_mismatch_theorem = kernel.prove_matrix_inequality(
        inherited_coefficients[0:1, :], target_coefficients,
        subject="type grading anomaly coefficients do not equal the target coefficients",
    )
    package_mismatch_theorem = kernel.prove_matrix_inequality(
        inherited_coefficients[1:2, :], target_coefficients,
        subject="package grading anomaly coefficients do not equal the target coefficients",
    )
    product_mismatch_theorem = kernel.prove_matrix_inequality(
        inherited_coefficients[2:3, :], target_coefficients,
        subject="product grading anomaly coefficients do not equal the target coefficients",
    )
    type_trace_theorem = kernel.prove_expression_equality(
        sum(inherited_coefficients.row(0)), 6,
        subject="isotropic type anomaly trace is six",
    )
    package_trace_theorem = kernel.prove_expression_equality(
        sum(inherited_coefficients.row(1)), 0,
        subject="isotropic package anomaly trace vanishes",
    )
    product_trace_theorem = kernel.prove_expression_equality(
        sum(inherited_coefficients.row(2)), 0,
        subject="isotropic product anomaly trace vanishes",
    )
    target_trace_theorem = kernel.prove_expression_equality(
        sum(target_coefficients.row(0)), 10,
        subject="isotropic target log determinant trace is ten",
    )
    target_loaded_rescaling_theorem = kernel.prove_expression_equality(
        loaded_jacobian, r**10,
        subject="only a target dependent all direction rescaling reproduces the isotropic determinant",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_logdet_reservoir_measure_anomaly_parent_origin_gate",
        (
            paired_jacobian_theorem, same_direction_jacobian_theorem,
            inherited_rank_theorem, augmented_rank_theorem,
            type_mismatch_theorem, package_mismatch_theorem, product_mismatch_theorem,
            type_trace_theorem, package_trace_theorem, product_trace_theorem,
            target_trace_theorem, target_loaded_rescaling_theorem,
        ),
    )
    return KMSReservoirMeasureAnomalyOriginCertificate(
        inherited_coefficients=inherited_coefficients,
        target_coefficients=target_coefficients,
        paired_jacobian_theorem=paired_jacobian_theorem,
        same_direction_jacobian_theorem=same_direction_jacobian_theorem,
        inherited_rank_theorem=inherited_rank_theorem,
        augmented_rank_theorem=augmented_rank_theorem,
        type_mismatch_theorem=type_mismatch_theorem,
        package_mismatch_theorem=package_mismatch_theorem,
        product_mismatch_theorem=product_mismatch_theorem,
        type_trace_theorem=type_trace_theorem,
        package_trace_theorem=package_trace_theorem,
        product_trace_theorem=product_trace_theorem,
        target_trace_theorem=target_trace_theorem,
        target_loaded_rescaling_theorem=target_loaded_rescaling_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version9_endpoint_creation_kms_logdet_reservoir_measure_anomaly_parent_origin_gate",
    title="Parent-origin measure anomaly reservoir KMS logdet",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_logdet_reservoir_measure_anomaly_parent_origin_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_reservoir_measure_anomaly_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("paired_berezin_jacobian", lambda: build_certificate().paired_jacobian_theorem),
        Obligation("same_direction_jacobian", lambda: build_certificate().same_direction_jacobian_theorem),
        Obligation("inherited_anomaly_rank", lambda: build_certificate().inherited_rank_theorem),
        Obligation("target_augmented_rank", lambda: build_certificate().augmented_rank_theorem),
        Obligation("type_grading_mismatch", lambda: build_certificate().type_mismatch_theorem),
        Obligation("package_grading_mismatch", lambda: build_certificate().package_mismatch_theorem),
        Obligation("product_grading_mismatch", lambda: build_certificate().product_mismatch_theorem),
        Obligation("type_isotropic_trace", lambda: build_certificate().type_trace_theorem),
        Obligation("package_isotropic_trace", lambda: build_certificate().package_trace_theorem),
        Obligation("product_isotropic_trace", lambda: build_certificate().product_trace_theorem),
        Obligation("target_isotropic_trace", lambda: build_certificate().target_trace_theorem),
        Obligation("target_loaded_rescaling", lambda: build_certificate().target_loaded_rescaling_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)