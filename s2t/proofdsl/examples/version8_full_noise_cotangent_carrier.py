"""Exact typed admission test for the full mixed-real noise cotangent carrier."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_full_primitive import build_certificate as full_qms_certificate
from .version8_metric_dual_environment_parent_action import (
    build_certificate as parent_origin_certificate,
)


@dataclass(frozen=True, slots=True)
class FullNoiseCotangentCarrierCertificate:
    mixed_real_dimension: int
    naive_uniform_complex_real_dimension: int
    current_jump_dimension: int
    missing_real_directions: int
    full_qms_theorem: Theorem
    mixed_dimension_theorem: Theorem
    naive_complexification_no_go_theorem: Theorem
    current_deficit_theorem: Theorem
    parent_origin_boundary_theorem: Theorem
    admission_gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FullNoiseCotangentCarrierCertificate:
    full_qms = full_qms_certificate()
    parent_origin = parent_origin_certificate()
    mixed_dimension = kernel.prove_mixed_real_cotangent_carrier_dimension(
        transfer_complex_dimension=15,
        gauge_hermitian_dimension=12,
        field_real_dimension=42,
        current_jump_dimension=full_qms.jump_count,
        subject="full transfer-complex plus Hermitian-gauge cotangent carrier",
        premises=(full_qms.gksl_theorem, parent_origin.parent_origin_no_go_theorem),
    )
    naive_no_go = kernel.prove_matrix_inequality(
        sp.Matrix([[54]]),
        sp.Matrix([[42]]),
        subject="uniform complexification overcounts the Hermitian gauge carrier",
    )
    deficit = kernel.prove_expression_equality(
        42 - full_qms.jump_count,
        17,
        subject="missing real directions of the current 25-jump QMS",
    )
    admission = kernel.prove_gate(
        "full_noise_cotangent_carrier_admission",
        (
            full_qms.gksl_theorem,
            mixed_dimension,
            naive_no_go,
            deficit,
            parent_origin.parent_origin_no_go_theorem,
        ),
    )
    return FullNoiseCotangentCarrierCertificate(
        mixed_real_dimension=42,
        naive_uniform_complex_real_dimension=54,
        current_jump_dimension=full_qms.jump_count,
        missing_real_directions=17,
        full_qms_theorem=full_qms.gksl_theorem,
        mixed_dimension_theorem=mixed_dimension,
        naive_complexification_no_go_theorem=naive_no_go,
        current_deficit_theorem=deficit,
        parent_origin_boundary_theorem=parent_origin.parent_origin_no_go_theorem,
        admission_gate_theorem=admission,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.mixed_dimension_theorem.proposition)