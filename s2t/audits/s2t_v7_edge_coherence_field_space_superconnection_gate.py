#!/usr/bin/env python3
"""Audit the field-space superconnection carrier of edge coherence."""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v7_edge_coherence_field_space_superconnection_gate_results.json"
)
RNG = np.random.default_rng(20260827)


def wedge_matrix(matrix: np.ndarray) -> np.ndarray:
    """Matrix of the second exterior power in lexicographic wedge bases."""
    row_pairs = list(combinations(range(matrix.shape[0]), 2))
    col_pairs = list(combinations(range(matrix.shape[1]), 2))
    result = np.zeros((len(row_pairs), len(col_pairs)), dtype=complex)
    for i, rows in enumerate(row_pairs):
        for j, cols in enumerate(col_pairs):
            result[i, j] = np.linalg.det(matrix[np.ix_(rows, cols)])
    return result


def c_matrix(field: np.ndarray) -> np.ndarray:
    """Matrix of one half of the derivative of B -> Lambda^2 B."""
    result = np.zeros((3, 6), dtype=complex)
    for output, (first, second) in enumerate(combinations(range(3), 2)):
        result[output, first] = 0.5 * field[1, second]
        result[output, second] = -0.5 * field[1, first]
        result[output, 3 + first] = -0.5 * field[0, second]
        result[output, 3 + second] = 0.5 * field[0, first]
    return result


def finite_dirac(field: np.ndarray) -> np.ndarray:
    edge_a = field.reshape(-1, 1)
    edge_c = c_matrix(field)
    operator = np.zeros((10, 10), dtype=complex)
    operator[1:7, 0:1] = edge_a
    operator[0:1, 1:7] = edge_a.conj().T
    operator[7:10, 1:7] = edge_c
    operator[1:7, 7:10] = edge_c.conj().T
    return operator


def oriented_differential(field: np.ndarray) -> np.ndarray:
    result = np.zeros((10, 10), dtype=complex)
    result[1:7, 0] = field.reshape(-1)
    result[7:10, 1:7] = c_matrix(field)
    return result


def random_complex(shape: tuple[int, ...]) -> np.ndarray:
    return RNG.normal(size=shape) + 1j * RNG.normal(size=shape)


def random_unitary(size: int) -> np.ndarray:
    q, r = np.linalg.qr(random_complex((size, size)))
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
    return q @ np.diag(phases.conj())


def invariants(field: np.ndarray) -> tuple[float, float]:
    gram = field @ field.conj().T
    return float(np.trace(gram).real), float(np.linalg.det(gram).real)


def spectral_action(field: np.ndarray, mu: float) -> float:
    operator = finite_dirac(field)
    return float(
        (4.0 / 9.0)
        * (
            np.trace(np.linalg.matrix_power(operator, 4)).real
            - mu * np.trace(operator @ operator).real
            + mu**2
        )
    )


def main() -> None:
    previous = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v7_edge_coherence_bimodule_admission_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert previous["verdict"]["status"] == (
        "closed_on_unchanged_physical_bimodule_carrier"
    )

    maxima = {
        "polarization": 0.0,
        "oriented_curvature": 0.0,
        "curvature_norm": 0.0,
        "second_trace": 0.0,
        "fourth_trace": 0.0,
        "action": 0.0,
        "block_covariance_wedge": 0.0,
        "block_covariance_derivative": 0.0,
        "real_half_trace_second": 0.0,
        "real_half_trace_fourth": 0.0,
    }

    trials = 250
    for _ in range(trials):
        field = random_complex((2, 3))
        direction = random_complex((2, 3))
        edge_c = c_matrix(field)
        wedge = wedge_matrix(field).reshape(-1)
        polarized = edge_c @ field.reshape(-1)
        maxima["polarization"] = max(
            maxima["polarization"], float(np.max(np.abs(polarized - wedge)))
        )

        differential = oriented_differential(field)
        square = differential @ differential
        expected_square = np.zeros_like(square)
        expected_square[7:10, 0] = wedge
        maxima["oriented_curvature"] = max(
            maxima["oriented_curvature"],
            float(np.max(np.abs(square - expected_square))),
        )

        total, determinant = invariants(field)
        maxima["curvature_norm"] = max(
            maxima["curvature_norm"],
            abs(float(np.vdot(wedge, wedge).real) - determinant),
        )

        operator = finite_dirac(field)
        trace_two = float(np.trace(operator @ operator).real)
        trace_four = float(np.trace(np.linalg.matrix_power(operator, 4)).real)
        maxima["second_trace"] = max(
            maxima["second_trace"], abs(trace_two - 3.0 * total)
        )
        maxima["fourth_trace"] = max(
            maxima["fourth_trace"],
            abs(trace_four - (9.0 / 4.0) * total**2 - (15.0 / 4.0) * determinant),
        )
        mu = float(RNG.uniform(0.2, 8.0))
        reduced = (total - 2.0 * mu / 3.0) ** 2 + (5.0 / 3.0) * determinant
        maxima["action"] = max(
            maxima["action"], abs(spectral_action(field, mu) - reduced)
        )

        # Maximal basis group that preserves the actual isotypic channel
        # split: U(2)_copy x U(2)_{eX} x U(1)_Y.  No U(3) gauge symmetry is
        # asserted.
        left = random_unitary(2)
        channel_pair = random_unitary(2)
        phase = np.exp(1j * RNG.uniform(-np.pi, np.pi))
        right = np.zeros((3, 3), dtype=complex)
        right[:2, :2] = channel_pair
        right[2, 2] = phase
        transformed_field = left @ field @ right.conj().T
        transformed_direction = left @ direction @ right.conj().T
        exterior_left = wedge_matrix(left)
        exterior_right = wedge_matrix(right)
        expected_wedge = exterior_left @ wedge_matrix(field) @ exterior_right.conj().T
        maxima["block_covariance_wedge"] = max(
            maxima["block_covariance_wedge"],
            float(np.max(np.abs(wedge_matrix(transformed_field) - expected_wedge))),
        )
        actual_derivative = (
            c_matrix(transformed_field) @ transformed_direction.reshape(-1)
        ).reshape(1, 3)
        expected_derivative = (
            exterior_left
            @ (c_matrix(field) @ direction.reshape(-1)).reshape(1, 3)
            @ exterior_right.conj().T
        )
        maxima["block_covariance_derivative"] = max(
            maxima["block_covariance_derivative"],
            float(np.max(np.abs(actual_derivative - expected_derivative))),
        )

        real_double = np.block(
            [
                [operator, np.zeros_like(operator)],
                [np.zeros_like(operator), operator.conj()],
            ]
        )
        maxima["real_half_trace_second"] = max(
            maxima["real_half_trace_second"],
            abs(0.5 * np.trace(real_double @ real_double).real - trace_two),
        )
        maxima["real_half_trace_fourth"] = max(
            maxima["real_half_trace_fourth"],
            abs(
                0.5 * np.trace(np.linalg.matrix_power(real_double, 4)).real
                - trace_four
            ),
        )

    # The finite trace metric supplies the principal kinetic metric of the
    # product superconnection.  It must be exactly 3 times the flat metric on
    # the twelve real components of B.
    real_basis = []
    for row in range(2):
        for col in range(3):
            for phase in (1.0, 1.0j):
                basis = np.zeros((2, 3), dtype=complex)
                basis[row, col] = phase
                real_basis.append(basis)
    kinetic_gram = np.zeros((12, 12))
    for i, first in enumerate(real_basis):
        first_operator = finite_dirac(first)
        for j, second in enumerate(real_basis):
            second_operator = finite_dirac(second)
            kinetic_gram[i, j] = np.trace(first_operator @ second_operator).real
    kinetic_eigenvalues = np.linalg.eigvalsh(kinetic_gram)
    kinetic_residual = float(np.max(np.abs(kinetic_gram - 3.0 * np.eye(12))))

    rank_one_field = (
        random_complex((2, 1)) @ random_complex((1, 3))
    )
    rank_two_field = random_complex((2, 3))
    rank_one_differential = oriented_differential(rank_one_field)
    rank_one_curvature = float(
        np.linalg.norm(rank_one_differential @ rank_one_differential)
    )
    rank_one_wedge_norm = float(np.linalg.norm(wedge_matrix(rank_one_field)))
    rank_two_wedge_norm = float(np.linalg.norm(wedge_matrix(rank_two_field)))

    tolerance = 2.0e-7
    assert max(maxima.values()) < tolerance
    assert kinetic_residual < tolerance
    assert np.min(kinetic_eigenvalues) > 0.0
    assert rank_one_wedge_norm < tolerance
    assert rank_two_wedge_norm > 1.0e-3

    result = {
        "gate": "version7_edge_coherence_field_space_superconnection_gate",
        "carrier": {
            "graded_dimensions": [1, 6, 3],
            "degree_zero": "trivial line",
            "degree_one": "Hom(W,V), the six-dimensional arrow-amplitude bundle",
            "degree_two": "Hom(Lambda^2 W,Lambda^2 V), the three-dimensional composite-minor bundle",
            "physical_fermion_vertices_added": 0,
            "independent_gauge_connections_added": 0,
            "connection_rule": "connections on degree one and two are induced functorially from endpoint bundles V and W",
        },
        "oriented_superconnection": {
            "d_squared": "Lambda^2 B in Hom(H0,H2)",
            "curvature_norm_squared": "det(B B*)",
            "rank_one_wedge_norm": rank_one_wedge_norm,
            "rank_two_control_wedge_norm": rank_two_wedge_norm,
            "rank_one_curvature_array_power_diagnostic": rank_one_curvature,
            "interpretation": "curved complex off vacuum, genuine complex on the rank-at-most-one locus",
        },
        "hermitian_finite_part": {
            "operator": "D_B=d_B+d_B*",
            "trace_D2": "3 T",
            "trace_D4": "(9/4) T^2 + (15/4) det(B B*)",
            "spectral_action": "(T-2 mu/3)^2 + (5/3) det(B B*)",
        },
        "kinetic_metric": {
            "identity": "Tr(delta D_B delta D_B)=3 Tr(delta B delta B*)",
            "real_dimension": 12,
            "eigenvalues": [float(value) for value in kinetic_eigenvalues],
            "max_residual_from_3I": kinetic_residual,
            "positive": True,
        },
        "covariance": {
            "tested_group": "U(2)_copy x U(2)_{eX} x U(1)_Y",
            "reason_for_block_group": "the third channel has a different bimodule type from e_R and X_R",
            "full_U3_channel_symmetry_used_as_physical_gauge_group": False,
            "actual_physical_gauge_group_is_a_subgroup": True,
        },
        "placement_in_full_strict_graph": {
            "coherence_block_edges_total": 6,
            "baseline_edges_inside_block": 1,
            "new_edges_inside_block": 5,
            "selected_new_edges_inside_block": 2,
            "unwanted_new_edges_inside_block": 3,
            "new_edges_outside_block": 6,
            "selected_new_edges_outside_block": 4,
            "unwanted_new_edges_outside_block": 2,
            "interpretation": "the coherence block is a maximal twin biclique, not the desired six-edge extension",
        },
        "real_completion": {
            "construction": "conjugate associated bundle with anti-linear exchange",
            "physical_half_trace_preserves_finite_coefficients": True,
        },
        "numerical_audit": {
            "seed": 20260827,
            "trials": trials,
            "tolerance": tolerance,
            "maximum_residuals": maxima,
        },
        "verdict": {
            "status": "positive_auxiliary_field_space_superconnection_carrier",
            "physical_finite_triple_embedding_required": False,
            "new_physical_particles_required": False,
            "new_independent_gauge_field_required": False,
            "absolute_spacetime_heat_kernel_normalization_closed": False,
            "full_eleven_edge_competition_closed": False,
            "next_gate": "test the exact support and flat-direction competition between the coherence biclique and all eleven new strict edges without a manual projector",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()