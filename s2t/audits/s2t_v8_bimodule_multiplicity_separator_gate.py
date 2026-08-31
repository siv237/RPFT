#!/usr/bin/env python3
"""Close the transfer field under endpoint bimodule projectors and test its Hessian."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_bimodule_multiplicity_separator_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (  # noqa: E402
    physical_blocks,
    physical_hessians,
    signature,
)
from s2t_v8_canonical_noise_frame_common_trace_gate import (  # noqa: E402
    gauge_components,
)
from s2t_v8_kms_nontracial_relative_rate_selector_gate import (  # noqa: E402
    central_density,
)
from s2t_v8_noise_isotropy_symmetry_admission_gate import (  # noqa: E402
    lie_orbit_closure,
    orthonormal_map_span,
)


SOURCE_BLOCKS = (("QL", 0, 6), ("LL", 6, 8), ("XL", 8, 9), ("YL", 9, 11))
TARGET_BLOCKS = (
    ("uR", 0, 3),
    ("dR", 3, 6),
    ("eR", 6, 7),
    ("XR", 7, 8),
    ("YR", 8, 10),
)
INCIDENCE_SUPPORT = {
    ("uR", "QL"),
    ("dR", "QL"),
    ("eR", "LL"),
    ("eR", "XL"),
    ("XR", "XL"),
    ("YR", "LL"),
    ("YR", "YL"),
}
HEAVY_SUPPORT = {
    ("dR", "XL"),
    ("eR", "YL"),
    ("XR", "LL"),
    ("YR", "QL"),
}


def endpoint_projectors() -> list[tuple[str, str, np.ndarray, np.ndarray]]:
    result = []
    for target_name, target_start, target_stop in TARGET_BLOCKS:
        target = np.zeros((10, 10))
        target[target_start:target_stop, target_start:target_stop] = np.eye(
            target_stop - target_start
        )
        for source_name, source_start, source_stop in SOURCE_BLOCKS:
            source = np.zeros((11, 11))
            source[source_start:source_stop, source_start:source_stop] = np.eye(
                source_stop - source_start
            )
            result.append((target_name, source_name, target.copy(), source.copy()))
    return result


def close_under_blocks(
    frame: list[np.ndarray],
    projectors: list[tuple[str, str, np.ndarray, np.ndarray]],
) -> list[np.ndarray]:
    pieces = [
        target @ item @ source
        for item in frame
        for _, _, target, source in projectors
        if np.linalg.norm(target @ item @ source) > 1.0e-12
    ]
    return orthonormal_map_span(pieces)


def projection_residual(matrix: np.ndarray, frame: list[np.ndarray]) -> float:
    coefficients = np.array(
        [np.trace(item.conj().T @ matrix) for item in frame]
    )
    reconstructed = sum(
        (coefficients[index] * frame[index] for index in range(len(frame))),
        np.zeros_like(matrix),
    )
    return float(np.linalg.norm(matrix - reconstructed))


def realification(frame: list[np.ndarray]) -> list[np.ndarray]:
    return [direction for item in frame for direction in (item, 1j * item)]


def main() -> None:
    background, variations, _, _ = physical_blocks()
    _, gauge_sources, gauge_targets = gauge_components()
    projectors = endpoint_projectors()
    incidence_orbit, incidence_sequence = lie_orbit_closure(
        [background], gauge_sources, gauge_targets
    )
    incidence_frame = orthonormal_map_span(incidence_orbit)
    heavy_frame = orthonormal_map_span(variations[7:])
    old_transfer = orthonormal_map_span(incidence_frame + heavy_frame)
    assert incidence_sequence == [1, 4, 5, 5]
    assert len(old_transfer) == 15

    leakage_rows = []
    for target_name, source_name, target, source in projectors:
        residual = max(
            projection_residual(target @ item @ source, old_transfer)
            for item in old_transfer
        )
        if residual > 1.0e-12:
            leakage_rows.append(
                {
                    "target": target_name,
                    "source": source_name,
                    "maximum_residual": residual,
                }
            )
    assert leakage_rows

    incidence_closed = close_under_blocks(incidence_frame, projectors)
    heavy_closed = close_under_blocks(heavy_frame, projectors)
    bimodule_closed = orthonormal_map_span(incidence_closed + heavy_closed)
    assert len(incidence_closed) == 10
    assert len(heavy_closed) == 10
    assert len(bimodule_closed) == 20
    incidence_heavy_overlap = max(
        float(abs(np.trace(left.conj().T @ right)))
        for left in incidence_closed
        for right in heavy_closed
    )
    assert incidence_heavy_overlap < TOL

    gauge_closed_again, gauge_sequence = lie_orbit_closure(
        bimodule_closed, gauge_sources, gauge_targets
    )
    assert gauge_sequence == [20, 20]
    assert len(gauge_closed_again) == 20

    block_dimensions = []
    for target_name, source_name, target, source in projectors:
        pieces = [
            target @ item @ source
            for item in bimodule_closed
            if np.linalg.norm(target @ item @ source) > 1.0e-12
        ]
        if not pieces:
            continue
        dimension = len(orthonormal_map_span(pieces))
        block_dimensions.append(
            {
                "target": target_name,
                "source": source_name,
                "complex_dimension": dimension,
                "sector": (
                    "incidence"
                    if (target_name, source_name) in INCIDENCE_SUPPORT
                    else "heavy"
                ),
            }
        )
    assert sum(row["complex_dimension"] for row in block_dimensions) == 20
    assert {
        (row["target"], row["source"])
        for row in block_dimensions
        if row["sector"] == "incidence"
    } == INCIDENCE_SUPPORT
    assert {
        (row["target"], row["source"])
        for row in block_dimensions
        if row["sector"] == "heavy"
    } == HEAVY_SUPPORT

    def incidence_selector(field: np.ndarray) -> np.ndarray:
        return sum(
            (
                target @ field @ source
                for target_name, source_name, target, source in projectors
                if (target_name, source_name) in INCIDENCE_SUPPORT
            ),
            np.zeros_like(field),
        )

    incidence_selector_residual = max(
        max(
            float(np.linalg.norm(incidence_selector(item) - item))
            for item in incidence_closed
        ),
        max(
            float(np.linalg.norm(incidence_selector(item)))
            for item in heavy_closed
        ),
    )
    assert incidence_selector_residual < TOL

    common_trace_rows = []
    for ratio in (1.0, float(np.exp(-2.0)), 22.0 / 21.0, 21.0 / 22.0):
        source_density, target_density = central_density(ratio)
        component_weight = source_density + target_density
        common_trace_rows.append(
            {
                "target_to_source_density_ratio": ratio,
                "per_component_weight": component_weight,
                "incidence_total_weight": 10.0 * component_weight,
                "heavy_total_weight": 10.0 * component_weight,
                "incidence_to_heavy_total_weight_ratio": 1.0,
            }
        )

    full_real = realification(incidence_closed + heavy_closed)
    physical_origin, physical_vacuum = physical_hessians(background, full_real)
    incidence_projector_real = np.diag([1.0] * 20 + [0.0] * 20)
    edge_origin = (
        -4.0 * incidence_projector_real
        + 4.0 * (np.eye(40) - incidence_projector_real)
    )
    edge_vacuum = (
        8.0 * incidence_projector_real
        + 4.0 * (np.eye(40) - incidence_projector_real)
    )

    gamma_source = np.diag([1.0] * 6 + [-1.0] * 5)
    gamma_target = np.diag([1.0] * 6 + [-1.0] * 4)

    def order(field: np.ndarray) -> np.ndarray:
        return gamma_target @ field - field @ gamma_source

    left_gram = background @ background.conj().T
    right_gram = background.conj().T @ background

    def linearized_relative(variation: np.ndarray) -> np.ndarray:
        value = order(variation)
        return left_gram @ value - value @ right_gram

    isotypic_hessian = np.array(
        [
            [
                2.0
                * np.real(
                    np.vdot(
                        linearized_relative(left),
                        linearized_relative(right),
                    )
                )
                for right in full_real
            ]
            for left in full_real
        ]
    )
    assert int(np.linalg.matrix_rank(isotypic_hessian, tol=TOL)) == 12

    def heavy_minimum(beta: float) -> float:
        matrix = edge_origin + beta * physical_origin
        return float(eigvalsh(matrix[20:, 20:])[0])

    critical_beta = brentq(heavy_minimum, 0.0, 1.0)
    assert abs(critical_beta - 2.0 / 3.0) < TOL

    hessian_rows = []
    for beta in (0.0, 0.1, 0.25, 0.5, 2.0 / 3.0, 1.0, 2.0):
        origin_values = eigvalsh(edge_origin + beta * physical_origin)
        vacuum_values = eigvalsh(
            edge_vacuum + beta * physical_vacuum + isotypic_hessian
        )
        hessian_rows.append(
            {
                "relative_gram_weight_beta": beta,
                "origin_signature": signature(origin_values),
                "vacuum_signature": signature(vacuum_values),
                "origin_minimum_eigenvalue": float(origin_values[0]),
                "origin_maximum_eigenvalue": float(origin_values[-1]),
                "vacuum_minimum_eigenvalue": float(vacuum_values[0]),
            }
        )
    beta_half = next(
        row for row in hessian_rows if row["relative_gram_weight_beta"] == 0.5
    )
    assert beta_half["origin_signature"] == [20, 0, 20]
    assert beta_half["vacuum_signature"] == [0, 0, 40]
    assert next(
        row
        for row in hessian_rows
        if row["relative_gram_weight_beta"] == 2.0 / 3.0
    )["origin_signature"] == [20, 12, 8]
    assert next(
        row for row in hessian_rows if row["relative_gram_weight_beta"] == 1.0
    )["origin_signature"] != [20, 0, 20]

    result = {
        "date": "2026-08-29",
        "gate": "version8_bimodule_multiplicity_separator_gate",
        "old_transfer_failure": {
            "old_gauge_closed_complex_dimension": 15,
            "endpoint_block_projectors_with_leakage": leakage_rows,
            "maximum_endpoint_projection_leakage": max(
                row["maximum_residual"] for row in leakage_rows
            ),
            "old_transfer_is_endpoint_bimodule_closed": False,
        },
        "bimodule_closure": {
            "incidence_complex_dimension": 10,
            "heavy_complex_dimension": 10,
            "total_transfer_complex_dimension": 20,
            "total_transfer_real_dimension": 40,
            "gauge_connection_real_dimension": 12,
            "total_internal_field_real_dimension": 52,
            "new_transfer_complex_directions": 5,
            "new_endpoint_fermion_states": 0,
            "new_gauge_generators": 0,
            "gauge_closure_sequence": gauge_sequence,
            "incidence_heavy_overlap": incidence_heavy_overlap,
            "endpoint_block_dimensions": block_dimensions,
        },
        "structural_selector": {
            "incidence_support": sorted([list(item) for item in INCIDENCE_SUPPORT]),
            "heavy_support": sorted([list(item) for item in HEAVY_SUPPORT]),
            "incidence_support_reading": "three baseline H15 pairs plus four gauge-isotypic pairs",
            "selector_residual": incidence_selector_residual,
            "uses_vacuum_amplitudes": False,
            "uses_endpoint_bimodule_labels": True,
        },
        "common_trace_edge_metric": {
            "rows": common_trace_rows,
            "incidence_and_heavy_complex_dimensions_equal": True,
            "single_moment_level_gives_equal_edge_hessian_masses": True,
            "edge_origin_incidence_mass": -4.0,
            "edge_origin_heavy_mass": 4.0,
            "edge_vacuum_incidence_mass": 8.0,
            "edge_vacuum_heavy_mass": 4.0,
        },
        "full_transfer_hessian": {
            "critical_relative_gram_weight": critical_beta,
            "passing_window": "0 <= beta < 2/3",
            "scan": hessian_rows,
            "beta_half_origin_signature": beta_half["origin_signature"],
            "beta_half_vacuum_signature": beta_half["vacuum_signature"],
            "beta_half_vacuum_gap": beta_half["vacuum_minimum_eigenvalue"],
            "isotypic_vacuum_hessian_rank": int(
                np.linalg.matrix_rank(isotypic_hessian, tol=TOL)
            ),
        },
        "verdict": {
            "full_endpoint_bimodule_labels_split_incidence_and_heavy": True,
            "old_15_complex_transfer_module_is_sufficient": False,
            "minimal_bimodule_closed_transfer_dimension_complex": 20,
            "relative_edge_mass_equality_from_single_level": True,
            "qualitative_20_to_20_transition_obtained": True,
            "relative_gram_weight_beta_derived": False,
            "absolute_mass_scale_derived": False,
            "full_parent_action_obtained": False,
            "next_gate": "version8_bimodule_common_curvature_relative_weight_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()