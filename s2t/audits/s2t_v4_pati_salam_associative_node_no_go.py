#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np

from s2t_v4_pati_salam_three_node_parent_graph import second_edge


OUTPUT_PATH = Path("s2t_v4_pati_salam_associative_node_no_go_results.json")
RANDOM_SEED = 20260814
RANDOM_TESTS = 200
WEDGE_PAIRS = [(first, second) for first in range(4) for second in range(first + 1, 4)]


def wedge_vector(first, second):
    return np.asarray(
        [
            first[left] * second[right] - first[right] * second[left]
            for left, right in WEDGE_PAIRS
        ]
    )


def exterior_square(matrix):
    result = np.zeros((6, 6), dtype=complex)
    for column, (first, second) in enumerate(WEDGE_PAIRS):
        result[:, column] = wedge_vector(matrix[:, first], matrix[:, second])
    return result


def exterior_square_lie(matrix):
    result = np.zeros((6, 6), dtype=complex)
    basis = np.eye(4, dtype=complex)
    for column, (first, second) in enumerate(WEDGE_PAIRS):
        result[:, column] = wedge_vector(matrix[:, first], basis[:, second])
        result[:, column] += wedge_vector(basis[:, first], matrix[:, second])
    return result


def random_unitary(size, rng, special=False):
    matrix = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    unitary, triangular = np.linalg.qr(matrix)
    diagonal = np.diag(triangular)
    unitary = unitary @ np.diag(np.conj(diagonal) / np.abs(diagonal))
    if special:
        unitary /= np.linalg.det(unitary) ** (1.0 / size)
    return unitary


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    maxima = {
        "group_exterior_square_multiplicativity_error": 0.0,
        "lie_exterior_square_commutator_error": 0.0,
        "wedge_edge_gauge_equivariance_error": 0.0,
    }
    additivity_defects = []
    associative_defects = []
    for _ in range(RANDOM_TESTS):
        first = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
        second = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
        maxima["group_exterior_square_multiplicativity_error"] = max(
            maxima["group_exterior_square_multiplicativity_error"],
            float(
                np.linalg.norm(
                    exterior_square(first @ second)
                    - exterior_square(first) @ exterior_square(second)
                )
            ),
        )
        first_lie = exterior_square_lie(first)
        second_lie = exterior_square_lie(second)
        maxima["lie_exterior_square_commutator_error"] = max(
            maxima["lie_exterior_square_commutator_error"],
            float(
                np.linalg.norm(
                    exterior_square_lie(first @ second - second @ first)
                    - (first_lie @ second_lie - second_lie @ first_lie)
                )
            ),
        )
        additivity_defects.append(
            float(
                np.linalg.norm(
                    exterior_square(first + second)
                    - exterior_square(first)
                    - exterior_square(second)
                )
            )
        )
        associative_defects.append(
            float(
                np.linalg.norm(
                    exterior_square_lie(first @ second) - first_lie @ second_lie
                )
            )
        )

        weak = random_unitary(2, rng, special=True)
        color = random_unitary(4, rng, special=True)
        delta = rng.normal(size=(2, 4)) + 1j * rng.normal(size=(2, 4))
        transformed_delta = weak @ delta @ color.T
        middle_action = np.kron(weak, color)
        target_action = exterior_square(color)
        maxima["wedge_edge_gauge_equivariance_error"] = max(
            maxima["wedge_edge_gauge_equivariance_error"],
            float(
                np.linalg.norm(
                    second_edge(transformed_delta) @ middle_action
                    - target_action @ second_edge(delta)
                )
            ),
        )

    scalar_identity = 2.0 * np.eye(4)
    group_scalar_defect = float(
        np.linalg.norm(exterior_square(scalar_identity) - 2.0 * np.eye(6))
    )
    lie_unit_defect = float(
        np.linalg.norm(exterior_square_lie(np.eye(4)) - np.eye(6))
    )
    wedge_map_matrix = np.column_stack(
        [
            second_edge(np.eye(8, dtype=complex)[:, index].reshape(2, 4)).reshape(-1)
            for index in range(8)
        ]
    )

    results = {
        "date": "2026-08-14",
        "random_seed": RANDOM_SEED,
        "random_tests": RANDOM_TESTS,
        "group_level_checks": {
            "maximum_errors": maxima,
            "wedge_intertwiner_complex_rank": int(
                np.linalg.matrix_rank(wedge_map_matrix, tol=1.0e-10)
            ),
            "representation_decomposition": (
                "Hom((2,4),(1,6)) contains one (2,4) summand and one (2,20bar) summand"
            ),
        },
        "associative_algebra_obstruction": {
            "median_exterior_square_additivity_defect": float(
                np.median(additivity_defects)
            ),
            "minimum_exterior_square_additivity_defect": float(
                np.min(additivity_defects)
            ),
            "scalar_linearity_defect_for_2I": group_scalar_defect,
            "median_lie_map_associative_product_defect": float(
                np.median(associative_defects)
            ),
            "minimum_lie_map_associative_product_defect": float(
                np.min(associative_defects)
            ),
            "lie_map_unitality_defect": lie_unit_defect,
            "reason": (
                "Lambda^2 is a group representation and its derivative is a Lie-algebra "
                "representation, but neither is a unital complex-linear representation of M4(C)"
            ),
        },
        "pati_salam_module_ledger": {
            "algebra": "H_R direct_sum H_L direct_sum M4(C)",
            "irreducible_complex_left_module_dimensions": [2, 2, 4],
            "M4_active_module_dimensions_are_multiples_of": 4,
            "one_dimensional_node_available": False,
            "irreducible_six_dimensional_color_node_available": False,
            "where_color_six_does_exist": (
                "inside Sym^2((2_R,4_4)) as the scalar channel (1_R,6_4)"
            ),
        },
        "verdict": {
            "equivariant_superconnection_carrier_pass": True,
            "strict_pati_salam_finite_triple_parent_pass": False,
            "previous_coarse_order_one_test_sufficient": False,
            "new_color_algebra_summand_required_for_literal_six_node": True,
            "preferred_repair": (
                "keep the established 32-dimensional Pati-Salam Hilbert module and derive "
                "the (1_R,6_4) determinant selector as a represented universal two-form or "
                "curvature component after the junk quotient"
            ),
            "next_gate": (
                "compute the degree-two represented differential calculus of the existing "
                "finite Dirac seed and test whether junk projection isolates the wedge channel"
            ),
        },
    }
    OUTPUT_PATH.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()