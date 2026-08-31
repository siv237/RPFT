"""Exact field-to-noise block embedding and pullback trace metric."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_full_noise_trace_frame import (
    build_certificate as trace_frame_certificate,
    full_noise_frame,
)
from .version8_gauge_twirl_kraus import _endpoint_gauge_generators
from .version8_metric_dual_environment_parent_action import (
    build_certificate as parent_origin_certificate,
)


TRANSFER_REAL_DIMENSION = 30
GAUGE_REAL_DIMENSION = 12
FULL_REAL_DIMENSION = 42
SOURCE_DIMENSION = 11


@dataclass(frozen=True, slots=True)
class FieldToNoiseMapCertificate:
    map_matrix: sp.ImmutableMatrix
    pullback_metric: sp.ImmutableMatrix
    pullback_dual: sp.ImmutableMatrix
    gauge_action_count: int
    intertwining_check_count: int
    map_rank_theorem: Theorem
    block_embedding_theorem: Theorem
    gauge_intertwining_theorem: Theorem
    sector_preservation_theorem: Theorem
    pullback_metric_theorem: Theorem
    pullback_dual_theorem: Theorem
    sector_rescaling_theorem: Theorem
    dynamical_boundary_theorem: Theorem
    gate_theorem: Theorem


def _field_action(generator: sp.MatrixBase, field: sp.MatrixBase) -> sp.ImmutableMatrix:
    source = generator[:SOURCE_DIMENSION, :SOURCE_DIMENSION]
    target = generator[SOURCE_DIMENSION:, SOURCE_DIMENSION:]
    if field[:SOURCE_DIMENSION, SOURCE_DIMENSION:] != sp.zeros(11, 10):
        arrow = field[SOURCE_DIMENSION:, :SOURCE_DIMENSION]
        transformed = sp.I * (target * arrow - arrow * source)
        result = sp.zeros(21)
        result[:SOURCE_DIMENSION, SOURCE_DIMENSION:] = transformed.H
        result[SOURCE_DIMENSION:, :SOURCE_DIMENSION] = transformed
        return sp.ImmutableMatrix(result)
    source_field = field[:SOURCE_DIMENSION, :SOURCE_DIMENSION]
    target_field = field[SOURCE_DIMENSION:, SOURCE_DIMENSION:]
    return sp.ImmutableMatrix(
        sp.diag(
            sp.I * (source * source_field - source_field * source),
            sp.I * (target * target_field - target_field * target),
        )
    )


@lru_cache(maxsize=1)
def build_certificate() -> FieldToNoiseMapCertificate:
    frame_certificate = trace_frame_certificate()
    parent_origin = parent_origin_certificate()
    frame = tuple(full_noise_frame())
    generators = tuple(_endpoint_gauge_generators())
    metric = sp.ImmutableMatrix(frame_certificate.trace_metric)
    map_matrix = sp.ImmutableMatrix(sp.eye(FULL_REAL_DIMENSION))

    ambient_columns = sp.Matrix.hstack(
        *(sp.Matrix(list(operator)) for operator in frame)
    )
    map_rank = kernel.prove_exact_rank(
        ambient_columns,
        FULL_REAL_DIMENSION,
        subject="block embedding of the complete field carrier into observables",
    )
    block_embedding = kernel.prove_matrix_equality(
        map_matrix,
        sp.eye(FULL_REAL_DIMENSION),
        subject="canonical coordinates of the field-to-noise block embedding",
    )

    nonzero_intertwining_entries = 0
    nonzero_sector_leakage_entries = 0
    for generator in generators:
        for index, field in enumerate(frame):
            field_side = _field_action(generator, field)
            noise_side = sp.ImmutableMatrix(
                sp.I * (generator * field - field * generator)
            )
            nonzero_intertwining_entries += sum(
                1
                for entry in field_side - noise_side
                if sp.simplify(entry) != 0
            )
            if index < TRANSFER_REAL_DIMENSION:
                forbidden = sp.diag(
                    field_side[:SOURCE_DIMENSION, :SOURCE_DIMENSION],
                    field_side[SOURCE_DIMENSION:, SOURCE_DIMENSION:],
                )
            else:
                forbidden = sp.zeros(21)
                forbidden[:SOURCE_DIMENSION, SOURCE_DIMENSION:] = field_side[
                    :SOURCE_DIMENSION, SOURCE_DIMENSION:
                ]
                forbidden[SOURCE_DIMENSION:, :SOURCE_DIMENSION] = field_side[
                    SOURCE_DIMENSION:, :SOURCE_DIMENSION
                ]
            nonzero_sector_leakage_entries += sum(
                1 for entry in forbidden if sp.simplify(entry) != 0
            )
    gauge_intertwining = kernel.prove_expression_equality(
        nonzero_intertwining_entries,
        0,
        subject="exact gauge intertwining of field and noise actions",
    )
    sector_preservation = kernel.prove_expression_equality(
        nonzero_sector_leakage_entries,
        0,
        subject="separate gauge invariance of transfer and gauge sectors",
    )

    pullback_metric = sp.ImmutableMatrix(map_matrix.H * metric * map_matrix)
    pullback_metric_theorem = kernel.prove_matrix_equality(
        pullback_metric,
        metric,
        subject="finite-trace metric pulled back to the complete field carrier",
    )
    pullback_dual = sp.ImmutableMatrix(pullback_metric.inv())
    pullback_dual_theorem = kernel.prove_matrix_equality(
        pullback_dual,
        frame_certificate.dual_rate_metric,
        subject="inverse pulled-back trace metric",
    )

    scale_transfer, scale_gauge = sp.symbols(
        "s_transfer s_gauge", nonzero=True, real=True
    )
    rescaling = sp.diag(
        *([scale_transfer] * TRANSFER_REAL_DIMENSION),
        *([scale_gauge] * GAUGE_REAL_DIMENSION),
    )
    rescaled_pullback = sp.ImmutableMatrix(rescaling.H * metric * rescaling)
    expected_rescaled = sp.ImmutableMatrix(
        sp.diag(
            scale_transfer**2 * metric[:30, :30],
            scale_gauge**2 * metric[30:, 30:],
        )
    )
    sector_rescaling = kernel.prove_matrix_equality(
        rescaled_pullback,
        expected_rescaled,
        subject="two-sector equivariant normalization freedom of the abstract carrier",
    )
    dynamical_boundary = parent_origin.parent_origin_no_go_theorem
    gate = kernel.prove_gate(
        "field_to_noise_chain_map_pullback_metric",
        (
            map_rank,
            block_embedding,
            gauge_intertwining,
            sector_preservation,
            pullback_metric_theorem,
            pullback_dual_theorem,
            sector_rescaling,
            dynamical_boundary,
        ),
    )
    return FieldToNoiseMapCertificate(
        map_matrix=map_matrix,
        pullback_metric=pullback_metric,
        pullback_dual=pullback_dual,
        gauge_action_count=len(generators),
        intertwining_check_count=len(generators) * len(frame),
        map_rank_theorem=map_rank,
        block_embedding_theorem=block_embedding,
        gauge_intertwining_theorem=gauge_intertwining,
        sector_preservation_theorem=sector_preservation,
        pullback_metric_theorem=pullback_metric_theorem,
        pullback_dual_theorem=pullback_dual_theorem,
        sector_rescaling_theorem=sector_rescaling,
        dynamical_boundary_theorem=dynamical_boundary,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.map_rank_theorem.proposition)
    print(certificate.gauge_intertwining_theorem.proposition)