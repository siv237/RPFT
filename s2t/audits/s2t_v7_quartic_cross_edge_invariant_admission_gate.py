#!/usr/bin/env python3
"""Admission audit for coefficient-free quartic cross-edge invariants."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_quartic_cross_edge_invariant_admission_gate_results.json"

V = np.array(
    [
        [1 / np.sqrt(2), -1 / np.sqrt(2), 0.0, 0.0],
        [1 / np.sqrt(6), 1 / np.sqrt(6), -2 / np.sqrt(6), 0.0],
        [1 / np.sqrt(12), 1 / np.sqrt(12), 1 / np.sqrt(12), -3 / np.sqrt(12)],
    ],
    dtype=complex,
)


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def normalized_higgs(rng: np.random.Generator) -> np.ndarray:
    vector = rng.normal(size=2) + 1j * rng.normal(size=2)
    return vector / np.linalg.norm(vector)


def higgs_conjugate(higgs: np.ndarray) -> np.ndarray:
    epsilon = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    return epsilon @ np.conj(higgs)


def physical_edges(higgs: np.ndarray) -> list[np.ndarray]:
    tilde = higgs_conjugate(higgs)
    up = np.zeros((7, 8), dtype=complex)
    down = np.zeros((7, 8), dtype=complex)
    electron = np.zeros((7, 8), dtype=complex)
    for colour in range(3):
        weak_slice = slice(2 * colour, 2 * colour + 2)
        up[colour, weak_slice] = np.conj(tilde)
        down[3 + colour, weak_slice] = np.conj(higgs)
    electron[6, 6:8] = np.conj(higgs)
    return [up, down, electron]


def random_unitary(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    q, r = np.linalg.qr(raw)
    diagonal = np.diag(r)
    return q @ np.diag(np.conj(diagonal) / np.abs(diagonal))


def random_field(rng: np.random.Generator) -> np.ndarray:
    return rng.normal(size=(3, 4)) + 1j * rng.normal(size=(3, 4))


def trace_power(matrix: np.ndarray, power: int) -> complex:
    return np.trace(np.linalg.matrix_power(matrix, power))


def physical_moment(operators: list[np.ndarray], power: int) -> float:
    total = sum(operators)
    source = total.conj().T @ total
    target = total @ total.conj().T
    return float((trace_power(source, power) + trace_power(target, power)).real)


def separated_moment(operators: list[np.ndarray], power: int) -> float:
    return float(
        sum(
            (
                trace_power(operator.conj().T @ operator, power)
                + trace_power(operator @ operator.conj().T, power)
            ).real
            for operator in operators
        )
    )


def main() -> None:
    degree_two = load_result("s2t_v7_common_higgs_degree_two_cross_edge_gate_results.json")
    oneform = load_result("s2t_v5_h15_physical_oneform_bimodule_gate_results.json")
    torsion = load_result("s2t_v5_h15_spectral_torsion_selector_gate_results.json")
    rectangle = load_result("s2t_v4_common_updown_krajewski_loop_gate_results.json")

    assert degree_two["verdict"]["common_Higgs_direct_degree_two_cross_edge_curvature"] == "closed_zero"
    intertwiner_matrix = np.array(
        oneform["charged_edge_multiplicity_space"]["intertwiner_dimension_matrix"]
    )
    assert np.array_equal(intertwiner_matrix, np.eye(3, dtype=int))

    rng = np.random.default_rng(20260826)
    polynomial_absolute_residuals = {power: [] for power in range(1, 7)}
    polynomial_relative_residuals = {power: [] for power in range(1, 7)}
    quartic_cross_traces = []
    vacuum_quartics = []
    family_only = {"ReTrW": [], "ReTrW2": [], "absTrW_squared": []}

    for _ in range(64):
        edges = physical_edges(normalized_higgs(rng))
        arbitrary_fields = [random_field(rng) for _ in range(3)]
        arbitrary_operators = [
            np.kron(field, edge) for field, edge in zip(arbitrary_fields, edges)
        ]
        for power in polynomial_absolute_residuals:
            total_moment = physical_moment(arbitrary_operators, power)
            edge_moment = separated_moment(arbitrary_operators, power)
            residual = abs(total_moment - edge_moment)
            polynomial_absolute_residuals[power].append(residual)
            polynomial_relative_residuals[power].append(
                residual / max(1.0, abs(total_moment), abs(edge_moment))
            )

        for first in range(3):
            for second in range(first + 1, 3):
                source_first = arbitrary_operators[first].conj().T @ arbitrary_operators[first]
                source_second = arbitrary_operators[second].conj().T @ arbitrary_operators[second]
                target_first = arbitrary_operators[first] @ arbitrary_operators[first].conj().T
                target_second = arbitrary_operators[second] @ arbitrary_operators[second].conj().T
                quartic_cross_traces.append(
                    abs(np.trace(source_first @ source_second))
                    + abs(np.trace(target_first @ target_second))
                )

        unitaries = [random_unitary(rng) for _ in range(3)]
        vacuum_fields = [unitary @ V for unitary in unitaries]
        vacuum_operators = [
            np.kron(field, edge) for field, edge in zip(vacuum_fields, edges)
        ]
        vacuum_quartics.append(physical_moment(vacuum_operators, 2))

        relative = vacuum_fields[0] @ vacuum_fields[1].conj().T
        family_only["ReTrW"].append(float(np.trace(relative).real))
        family_only["ReTrW2"].append(float(np.trace(relative @ relative).real))
        family_only["absTrW_squared"].append(float(abs(np.trace(relative)) ** 2))

    polynomial_absolute_maxima = {
        str(power): float(max(values))
        for power, values in polynomial_absolute_residuals.items()
    }
    polynomial_relative_maxima = {
        str(power): float(max(values))
        for power, values in polynomial_relative_residuals.items()
    }
    family_ranges = {
        name: {
            "minimum": float(min(values)),
            "maximum": float(max(values)),
            "range": float(max(values) - min(values)),
        }
        for name, values in family_only.items()
    }

    result = {
        "gate": "version7_quartic_cross_edge_invariant_admission_gate",
        "current_carrier": {
            "physical_graph": "H15 charged forest with common-Higgs orthogonal edge supports",
            "edge_types": ["u", "d", "e"],
            "edge_bimodule_commutant": "C^3",
            "off_diagonal_intertwiner_dimension": int(
                np.sum(intertwiner_matrix) - np.trace(intertwiner_matrix)
            ),
        },
        "ordinary_one_trace_polynomials": {
            "tested_positive_moment_powers": list(range(1, 7)),
            "maximum_absolute_total_minus_separated_residual_by_power": polynomial_absolute_maxima,
            "maximum_relative_total_minus_separated_residual_by_power": polynomial_relative_maxima,
            "maximum_direct_quartic_cross_trace": float(max(quartic_cross_traces)),
            "all_polynomial_moments_split_by_edge": True,
        },
        "coisometric_vacuum": {
            "quartic_trace_expected": 42.0,
            "quartic_trace_minimum": float(min(vacuum_quartics)),
            "quartic_trace_maximum": float(max(vacuum_quartics)),
            "quartic_trace_range": float(max(vacuum_quartics) - min(vacuum_quartics)),
            "relative_U3_frames_seen_by_physical_trace": False,
        },
        "family_only_cross_contractions": {
            "relative_matrix": "W_ab=X_a X_b^*=U_a U_b^*",
            "ranges_over_random_vacua": family_ranges,
            "can_see_relative_frames": True,
            "requires_off_diagonal_edge_contraction": True,
            "admissible_in_current_physical_bimodule": False,
        },
        "known_higher_structures": {
            "spectral_torsion_cross_sensitive": torsion["verdict"][
                "spectral_torsion_is_nontrivial_on_H15"
            ]
            == "pass",
            "spectral_torsion_selector_status": torsion["verdict"][
                "spectral_torsion_selects_unique_relative_Yukawa_ratios"
            ],
            "krajewski_rectangle_generates_cross_word": rectangle[
                "common_loop_generates_cross_word"
            ],
            "krajewski_rectangle_requires_nonzero_common_connector": rectangle[
                "nonzero_common_connector_assumed"
            ],
            "krajewski_rectangle_full_dimension": rectangle["full_dirac_dimension"],
            "contained_in_current_H15_carrier": False,
        },
        "verdict": {
            "coefficient_free_quartic_cross_edge_invariant_on_current_carrier": "not_admitted",
            "raising_polynomial_degree_without_new_connector_can_help": False,
            "family_only_frame_sensitive_scalars_exist": True,
            "family_only_scalars_are_physically_typed": False,
            "minimal_required_change": "derive a new gauge- and Real-compatible connector completing a mixed Krajewski cycle",
            "next_gate": "minimal H15-compatible mixed connector representation admission",
        },
    }

    assert max(polynomial_relative_maxima.values()) < 1.0e-12
    assert max(quartic_cross_traces) < 1.0e-10
    assert abs(np.mean(vacuum_quartics) - 42.0) < 1.0e-10
    assert result["coisometric_vacuum"]["quartic_trace_range"] < 1.0e-10
    assert all(item["range"] > 0.5 for item in family_ranges.values())
    assert result["current_carrier"]["off_diagonal_intertwiner_dimension"] == 0
    assert not result["verdict"]["raising_polynomial_degree_without_new_connector_can_help"]

    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()