"""Exact 42-jump GKSL assembly and fixed-algebra certificate."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from ..lindblad import LindbladGenerator
from ..structures import Morphism, Space
from .version8_full_noise_trace_frame import build_certificate as frame_certificate
from .version8_full_noise_trace_frame import full_noise_frame
from .version8_full_primitive import _jumps as primitive_jumps
from .version8_full_primitive import build_certificate as primitive_certificate


@dataclass(frozen=True, slots=True)
class FullNoiseGKSLCertificate:
    jump_count: int
    base_jump_count: int
    added_jump_count: int
    gksl_theorem: Theorem
    trace_theorem: Theorem
    unital_theorem: Theorem
    endpoint_theorem: Theorem
    scalar_fixed_theorem: Theorem
    trace_dual_span_theorem: Theorem
    full_gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FullNoiseGKSLCertificate:
    frame = full_noise_frame()
    endpoint = Space("E_s+E_t", 21)
    zero = Morphism("H_0_full_42", endpoint, endpoint, sp.zeros(21))
    jumps = tuple(
        Morphism(f"F_full_{index}", endpoint, endpoint, matrix)
        for index, matrix in enumerate(frame)
    )
    generator = LindbladGenerator.make(
        "full_42_jump_QMS", zero, jumps, [sp.Integer(1)] * len(jumps)
    )
    trace = kernel.prove_generator_trace_preserving(generator)
    unital = kernel.prove_generator_unital(generator)
    endpoint_theorem = kernel.prove_block_subalgebra_invariant(
        generator, (11, 10), subject="42-jump endpoint observable algebra"
    )
    primitive = primitive_certificate()
    scalar_fixed = kernel.prove_scalar_fixed_algebra_under_frame_extension(
        primitive.scalar_fixed_theorem,
        primitive_jumps(),
        frame,
        subject="full 42-jump frame retains the scalar fixed algebra",
    )
    trace_frame = frame_certificate()
    trace_dual_span = kernel.prove_matrix_equality(
        trace_frame.trace_metric * trace_frame.dual_rate_metric,
        sp.eye(42),
        subject="trace-dual whitening is invertible on the full jump span",
    )
    gate = kernel.prove_gate(
        "full_42_jump_gksl",
        (
            generator.theorem,
            trace,
            unital,
            endpoint_theorem,
            scalar_fixed,
            trace_dual_span,
        ),
    )
    return FullNoiseGKSLCertificate(
        jump_count=42,
        base_jump_count=25,
        added_jump_count=17,
        gksl_theorem=generator.theorem,
        trace_theorem=trace,
        unital_theorem=unital,
        endpoint_theorem=endpoint_theorem,
        scalar_fixed_theorem=scalar_fixed,
        trace_dual_span_theorem=trace_dual_span,
        full_gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.scalar_fixed_theorem.proposition)