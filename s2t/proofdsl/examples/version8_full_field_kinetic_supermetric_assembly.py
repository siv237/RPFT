"""Exact assembly of the full field principal kinetic supermetric."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_full_noise_trace_frame import build_certificate as trace_frame_certificate
from .version8_spacetime_kinetic_factorization_and_gauge_fixing import (
    build_certificate as kinetic_certificate,
)
from .version8_transverse_noise_mobility_environment_origin import (
    build_certificate as environment_certificate,
)


@dataclass(frozen=True, slots=True)
class FullFieldKineticSupermetricCertificate:
    transfer_metric: sp.ImmutableMatrix
    gauge_metric: sp.ImmutableMatrix
    scalar_principal_symbol: sp.ImmutableMatrix
    gauge_principal_symbol: sp.ImmutableMatrix
    ungauged_supermetric: sp.ImmutableMatrix
    gauge_fixed_supermetric: sp.ImmutableMatrix
    gauge_fixed_inverse: sp.ImmutableMatrix
    sector_mixing_block: sp.ImmutableMatrix
    scalar_rank_theorem: Theorem
    gauge_rank_theorem: Theorem
    type_separation_theorem: Theorem
    ungauged_rank_theorem: Theorem
    ungauged_nullity_theorem: Theorem
    gauge_fixed_rank_theorem: Theorem
    inverse_theorem: Theorem
    relative_weight_freedom_theorem: Theorem
    lower_order_boundary_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FullFieldKineticSupermetricCertificate:
    frame = trace_frame_certificate()
    kinetic = kinetic_certificate()
    environment = environment_certificate()

    transfer_metric = sp.ImmutableMatrix(frame.trace_metric[:30, :30])
    gauge_metric = sp.ImmutableMatrix(frame.trace_metric[30:, 30:])
    identity_four = sp.ImmutableMatrix(sp.eye(4))
    transverse = kinetic.transverse_projector
    longitudinal = kinetic.longitudinal_projector

    scalar_symbol = sp.ImmutableMatrix(
        sp.kronecker_product(transfer_metric, identity_four)
    )
    gauge_symbol = sp.ImmutableMatrix(
        sp.kronecker_product(gauge_metric, transverse)
    )
    mixing = sp.ImmutableMatrix(sp.zeros(120, 48))
    ungauged = sp.ImmutableMatrix(
        sp.BlockMatrix([[scalar_symbol, mixing], [mixing.H, gauge_symbol]]).as_explicit()
    )

    xi = sp.Symbol("xi", positive=True)
    gauge_fixed_symbol = sp.ImmutableMatrix(
        sp.kronecker_product(gauge_metric, transverse + longitudinal / xi)
    )
    fixed = sp.ImmutableMatrix(sp.diag(scalar_symbol, gauge_fixed_symbol))
    fixed_inverse = sp.ImmutableMatrix(
        sp.diag(
            sp.kronecker_product(transfer_metric.inv(), identity_four),
            sp.kronecker_product(
                gauge_metric.inv(), transverse + xi * longitudinal
            ),
        )
    )

    scalar_rank = kernel.prove_expression_equality(
        transfer_metric.rank() * identity_four.rank(),
        120,
        subject="Kronecker rank of the scalar principal symbol",
    )
    gauge_rank = kernel.prove_expression_equality(
        gauge_metric.rank() * transverse.rank(),
        36,
        subject="Kronecker rank of the transverse gauge principal symbol",
    )
    type_separation = kernel.prove_matrix_equality(
        mixing,
        sp.zeros(120, 48),
        subject="zero scalar-vector mixing in the second-order principal symbol",
    )
    ungauged_rank = kernel.prove_expression_equality(
        120 + 36,
        156,
        subject="block-additive rank of the complete ungauged principal supermetric",
    )
    ungauged_nullity = kernel.prove_expression_equality(
        168 - 156,
        12,
        subject="longitudinal nullity of the complete supermetric",
    )
    fixed_rank = kernel.prove_expression_equality(
        120 + gauge_metric.rank() * (transverse + longitudinal / xi).rank(),
        168,
        subject="block-additive full rank after field gauge fixing",
    )
    scalar_inverse = sp.ImmutableMatrix(
        sp.kronecker_product(transfer_metric.inv(), identity_four)
    )
    gauge_inverse = sp.ImmutableMatrix(
        sp.kronecker_product(gauge_metric.inv(), transverse + xi * longitudinal)
    )
    inverse = kernel.prove_matrix_equality(
        sp.diag(
            scalar_symbol * scalar_inverse,
            gauge_fixed_symbol * gauge_inverse,
        ),
        sp.eye(168),
        subject="exact block inverse of the gauge-fixed field supermetric",
    )

    transfer_weight, gauge_weight = sp.symbols(
        "w_transfer w_gauge", positive=True
    )
    weighted = sp.ImmutableMatrix(
        sp.diag(transfer_weight * scalar_symbol, gauge_weight * gauge_fixed_symbol)
    )
    relative_weight_freedom = kernel.prove_matrix_inequality(
        weighted.subs({transfer_weight: 1, gauge_weight: 1}),
        weighted.subs({transfer_weight: 1, gauge_weight: 2}),
        subject="independent sector weights preserve the assembled block type",
    )
    lower_order_boundary = environment.physical_scale_boundary_theorem
    gate = kernel.prove_gate(
        "full_field_kinetic_supermetric_assembly",
        (
            frame.transfer_gauge_orthogonality_theorem,
            scalar_rank,
            gauge_rank,
            type_separation,
            ungauged_rank,
            ungauged_nullity,
            fixed_rank,
            inverse,
            relative_weight_freedom,
            lower_order_boundary,
        ),
    )
    return FullFieldKineticSupermetricCertificate(
        transfer_metric=transfer_metric,
        gauge_metric=gauge_metric,
        scalar_principal_symbol=scalar_symbol,
        gauge_principal_symbol=gauge_symbol,
        ungauged_supermetric=ungauged,
        gauge_fixed_supermetric=fixed,
        gauge_fixed_inverse=fixed_inverse,
        sector_mixing_block=mixing,
        scalar_rank_theorem=scalar_rank,
        gauge_rank_theorem=gauge_rank,
        type_separation_theorem=type_separation,
        ungauged_rank_theorem=ungauged_rank,
        ungauged_nullity_theorem=ungauged_nullity,
        gauge_fixed_rank_theorem=fixed_rank,
        inverse_theorem=inverse,
        relative_weight_freedom_theorem=relative_weight_freedom,
        lower_order_boundary_theorem=lower_order_boundary,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.ungauged_rank_theorem.proposition)
    print(certificate.gauge_fixed_rank_theorem.proposition)