#!/usr/bin/env python3
"""Audit higher cycle characters and the single-holonomy mixing no-go."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v7_higher_cycle_character_mixing_freeze_gate_results.json"
)


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def random_unitary(rng: np.random.Generator, size: int = 3) -> np.ndarray:
    matrix = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    q, r = np.linalg.qr(matrix)
    phases = np.diag(r)
    phases = phases / np.abs(phases)
    return q @ np.diag(phases.conj())


def main() -> None:
    previous = load_result(
        "s2t_v7_cycle_holonomy_spectral_moment_scale_gate_results.json"
    )
    assert previous["verdict"]["status"] == (
        "positive_sixth_moment_holonomy_visibility_central_minimum_scale_no_go"
    )

    vertices = previous["graph"]["vertices"]
    baseline_edges = previous["graph"]["baseline_edges"]
    selected_edges = previous["graph"]["selected_edges"]
    full_edges = baseline_edges + selected_edges
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    holonomy_edge = "Q_L--Y_R"

    # Each matrix entry is a Laurent polynomial in the cycle phase z and a
    # polynomial in the common selected-edge radius r.  The key (p,m) means
    # r^p z^m.  Exact integer multiplication counts closed walks.
    adjacency_polynomial = [[[] for _ in vertices] for _ in vertices]
    for edge in full_edges:
        source, target = edge.split("--")
        radius_power = int(edge in selected_edges)
        winding = int(edge == holonomy_edge)
        adjacency_polynomial[vertex_index[source]][vertex_index[target]].append(
            (radius_power, winding, 1)
        )
        adjacency_polynomial[vertex_index[target]][vertex_index[source]].append(
            (radius_power, -winding, 1)
        )

    size = len(vertices)
    matrix = [[defaultdict(int) for _ in vertices] for _ in vertices]
    for index in range(size):
        matrix[index][index][(0, 0)] = 1

    trace_coefficients: dict[int, dict[tuple[int, int], int]] = {}
    for degree in range(1, 31):
        product = [[defaultdict(int) for _ in vertices] for _ in vertices]
        for first in range(size):
            for middle in range(size):
                if not matrix[first][middle]:
                    continue
                for second in range(size):
                    if not adjacency_polynomial[middle][second]:
                        continue
                    for (power, winding), coefficient in matrix[first][middle].items():
                        for edge_power, edge_winding, edge_coefficient in (
                            adjacency_polynomial[middle][second]
                        ):
                            product[first][second][
                                (power + edge_power, winding + edge_winding)
                            ] += coefficient * edge_coefficient
        matrix = product
        if degree % 2 == 0:
            trace = defaultdict(int)
            for index in range(size):
                for key, coefficient in matrix[index][index].items():
                    trace[key] += coefficient
            trace_coefficients[degree] = dict(trace)

    first_winding_degrees = {}
    for winding in range(1, 6):
        first = min(
            degree
            for degree, coefficients in trace_coefficients.items()
            if any(abs(key_winding) == winding for _, key_winding in coefficients)
        )
        first_winding_degrees[str(winding)] = first
        assert first == 6 * winding

    def harmonic_polynomial(degree: int, winding: int) -> dict[int, int]:
        # The +m and -m coefficients agree.  Their sum becomes
        # 2*c(r)*ReTr(W^m) on the three-family block graph.
        positive = {
            power: coefficient
            for (power, key_winding), coefficient in trace_coefficients[degree].items()
            if key_winding == winding
        }
        negative = {
            power: coefficient
            for (power, key_winding), coefficient in trace_coefficients[degree].items()
            if key_winding == -winding
        }
        assert positive == negative
        return {power: 2 * coefficient for power, coefficient in sorted(positive.items())}

    harmonics = {
        str(degree): {
            str(winding): harmonic_polynomial(degree, winding)
            for winding in range(1, degree // 6 + 1)
            if any(
                abs(key_winding) == winding
                for _, key_winding in trace_coefficients[degree]
            )
        }
        for degree in (6, 8, 10, 12, 18)
    }
    assert harmonics["6"]["1"] == {4: 12}
    assert harmonics["12"]["1"] == {4: 360, 6: 1560, 8: 3072, 10: 2592}
    assert harmonics["12"]["2"] == {8: 12}
    assert harmonics["18"]["3"] == {12: 12}

    def harmonic_value(degree: int, winding: int, radius: float) -> float:
        return sum(
            coefficient * radius**power
            for power, coefficient in harmonic_polynomial(degree, winding).items()
        )

    # Direct block-matrix checks for the first two higher characters.
    def adjacency(holonomy: np.ndarray, radius: float) -> np.ndarray:
        operator = np.zeros((3 * size, 3 * size), dtype=complex)
        identity = np.eye(3)
        for edge in full_edges:
            source, target = edge.split("--")
            block = holonomy if edge == holonomy_edge else identity
            if edge in selected_edges:
                block = radius * block
            first = slice(3 * vertex_index[source], 3 * vertex_index[source] + 3)
            second = slice(3 * vertex_index[target], 3 * vertex_index[target] + 3)
            operator[first, second] = block
            operator[second, first] = block.conj().T
        return operator

    rng = np.random.default_rng(20260827)
    identity = np.eye(3)
    maximum_higher_character_residual = 0.0
    maximum_higher_character_relative_residual = 0.0
    for _ in range(100):
        holonomy = random_unitary(rng)
        radius = float(rng.uniform(0.2, 1.8))
        operator = adjacency(holonomy, radius)
        reference = adjacency(identity, radius)
        for degree in (12, 18):
            predicted = 0.0
            for winding in range(1, degree // 6 + 1):
                coefficient = harmonic_value(degree, winding, radius)
                predicted += coefficient * (
                    np.trace(np.linalg.matrix_power(holonomy, winding)).real - 3.0
                )
            direct = (
                np.trace(np.linalg.matrix_power(operator, degree)).real
                - np.trace(np.linalg.matrix_power(reference, degree)).real
            )
            maximum_higher_character_residual = max(
                maximum_higher_character_residual, abs(float(direct - predicted))
            )
            maximum_higher_character_relative_residual = max(
                maximum_higher_character_relative_residual,
                abs(float(direct - predicted))
                / max(1.0, abs(float(direct)), abs(float(predicted))),
            )
    assert maximum_higher_character_residual < 1.0e-4
    assert maximum_higher_character_relative_residual < 1.0e-11

    # Every individual even moment tested through degree 30 is minimized at
    # theta=pi on a broad radial grid.  This is a finite audit, not an all-order
    # theorem.  It rules out the nearest higher-moment loophole.
    angles = np.linspace(0.0, np.pi, 20001)
    radii = np.geomspace(0.05, 20.0, 61)
    maximum_minimum_displacement = 0.0
    tested_moment_minima = {}
    for degree in range(6, 31, 2):
        minima = []
        for radius in radii:
            potential = np.zeros_like(angles)
            for winding in range(1, degree // 6 + 1):
                coefficient = harmonic_value(degree, winding, float(radius))
                potential += coefficient * np.cos(winding * angles)
            minimum_angle = float(angles[int(np.argmin(potential))])
            minima.append(minimum_angle)
            maximum_minimum_displacement = max(
                maximum_minimum_displacement, abs(np.pi - minimum_angle)
            )
        tested_moment_minima[str(degree)] = {
            "all_tested_radii_minimize_at_pi": bool(
                max(abs(np.pi - angle) for angle in minima) < 1.0e-12
            )
        }
    assert maximum_minimum_displacement < 1.0e-12

    # At r=1 the first two harmonics of Tr D^12 are 7584 and 12.  A tuned
    # combination c6 TrD6+c12 TrD12 has
    # v(theta)=a cos(theta)+b cos(2 theta).  An interior minimum requires
    # b>0 and |a|<4b, hence -636<c6/c12<-628.  The graph does not derive this
    # profile ratio.
    a12 = sum(harmonics["12"]["1"].values())
    b12 = sum(harmonics["12"]["2"].values())
    assert a12 == 7584 and b12 == 12
    tuned_ratio_interval = (-636.0, -628.0)

    result = {
        "gate": "version7_higher_cycle_character_mixing_freeze_gate",
        "exact_walk_character_structure": {
            "first_winding_degrees": first_winding_degrees,
            "selected_harmonic_coefficients_by_radius_power": harmonics,
            "maximum_direct_block_matrix_residual": maximum_higher_character_residual,
            "maximum_direct_block_matrix_relative_residual": maximum_higher_character_relative_residual,
            "single_holonomy_class_function": True,
            "depends_on_eigenphases_not_eigenvectors": True,
        },
        "individual_higher_moment_test": {
            "degrees": list(range(6, 31, 2)),
            "radius_interval": [float(radii[0]), float(radii[-1])],
            "radius_samples": len(radii),
            "angle_samples": len(angles),
            "minima": tested_moment_minima,
            "maximum_displacement_from_pi": maximum_minimum_displacement,
            "all_tested_individual_moments_select_minus_identity": True,
            "all_order_theorem_claimed": False,
        },
        "first_tunable_noncentral_loophole": {
            "potential": "a*ReTr(W)+b*ReTr(W^2)",
            "scalar_stationarity": "sin(theta)*(a+4*b*cos(theta))=0",
            "interior_minimum_condition": "b>0 and abs(a)<4*b",
            "at_r_equal_1": {
                "TrD6_chi1_coefficient": 12,
                "TrD12_chi1_coefficient": a12,
                "TrD12_chi2_coefficient": b12,
                "required_c6_over_c12_interval": list(tuned_ratio_interval),
            },
            "ratio_derived_by_H15": False,
            "noncentral_eigenphase_requires_profile_tuning": True,
        },
        "verdict": {
            "status": "higher_cycle_characters_visible_single_holonomy_mixing_freeze",
            "higher_characters_exist": True,
            "nearest_individual_moment_loophole_closed": True,
            "single_conjugacy_class_can_select_CKM_eigenvectors": False,
            "parameter_free_noncentral_minimum_obtained": False,
            "family_mixing_branch_frozen_in_current_single_cycle_parent": True,
            "complete_physical_parent_obtained": False,
            "next_gate": "return to the scale problem and test whether a profile-independent dynamical level can be derived from the Hodge parent; reopen mixing only after a second noncommuting family tensor is independently derived",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()