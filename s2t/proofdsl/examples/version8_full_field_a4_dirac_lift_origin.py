"""Exact nonuniqueness of the spacetime product-Dirac lift."""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..kernel import Theorem, kernel
from .version8_full_noise_trace_frame import full_noise_frame
from .version8_full_field_kinetic_relative_weight_parent_origin import build_certificate as weight_certificate


@dataclass(frozen=True, slots=True)
class FullFieldA4DiracLiftOriginCertificate:
    external_symbol_one: sp.ImmutableMatrix
    external_symbol_two: sp.ImmutableMatrix
    internal_check_count: int
    chirality_theorem: Theorem
    internal_calculus_theorem: Theorem
    first_symbol_theorem: Theorem
    second_symbol_theorem: Theorem
    symbol_scale_theorem: Theorem
    relative_weight_stability_theorem: Theorem
    lift_no_go_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FullFieldA4DiracLiftOriginCertificate:
    weight = weight_certificate()
    gamma_one = weight.gamma_matrices[0]
    gamma_five = weight.gamma_five
    identity_internal = sp.eye(21)
    frame = full_noise_frame()

    chirality = kernel.prove_matrix_equality(
        gamma_one * gamma_five + gamma_five * gamma_one,
        sp.zeros(4),
        subject="external Dirac symbol is odd for the common chirality",
    )
    commuting_defects = sum(
        sum(1 for entry in identity_internal * item - item * identity_internal if entry != 0)
        for item in frame
    )
    internal_calculus = kernel.prove_expression_equality(
        commuting_defects,
        0,
        subject="all 42 internal commutators are unchanged by external Dirac rescaling",
    )

    symbol_one = sp.ImmutableMatrix(gamma_one)
    symbol_two = sp.ImmutableMatrix(2 * gamma_one)
    first_symbol = kernel.prove_matrix_equality(
        symbol_one**2, sp.eye(4), subject="unit external principal symbol square"
    )
    second_symbol = kernel.prove_matrix_equality(
        symbol_two**2, 4 * sp.eye(4), subject="rescaled external principal symbol square"
    )
    symbol_scale = kernel.prove_matrix_inequality(
        symbol_one**2,
        symbol_two**2,
        subject="finite internal data do not select the external metric scale",
    )
    relative_stability = weight.relative_weight_theorem
    lift_no_go = kernel.prove_gate(
        "finite_parent_product_dirac_lift_no_go",
        (chirality, internal_calculus, first_symbol, second_symbol, symbol_scale),
    )
    gate = kernel.prove_gate(
        "full_field_a4_dirac_lift_origin",
        (
            chirality,
            internal_calculus,
            first_symbol,
            second_symbol,
            symbol_scale,
            relative_stability,
            lift_no_go,
        ),
    )
    return FullFieldA4DiracLiftOriginCertificate(
        external_symbol_one=symbol_one,
        external_symbol_two=symbol_two,
        internal_check_count=len(frame),
        chirality_theorem=chirality,
        internal_calculus_theorem=internal_calculus,
        first_symbol_theorem=first_symbol,
        second_symbol_theorem=second_symbol,
        symbol_scale_theorem=symbol_scale,
        relative_weight_stability_theorem=relative_stability,
        lift_no_go_theorem=lift_no_go,
        gate_theorem=gate,
    )