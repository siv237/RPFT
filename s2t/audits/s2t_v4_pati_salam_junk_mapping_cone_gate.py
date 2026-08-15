#!/usr/bin/env python3
import json
from itertools import product
from pathlib import Path

import numpy as np


TOLERANCE = 1.0e-10
RANDOM_SEED = 20260814
RANDOM_TESTS = 300


def matrix_unit(size, row, column):
    matrix = np.zeros((size, size), dtype=complex)
    matrix[row, column] = 1.0
    return matrix


def commutator(left, right):
    return left @ right - right @ left


def matrix_rank(matrix):
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return int(np.sum(singular_values > TOLERANCE))


def orthonormal_span(matrix):
    left_vectors, singular_values, _ = np.linalg.svd(matrix, full_matrices=False)
    return left_vectors[:, singular_values > TOLERANCE]


def universal_calculus_audit(first_weight, second_weight):
    size = 3
    dirac = np.zeros((size, size), dtype=complex)
    dirac[0, 1] = first_weight
    dirac[1, 0] = np.conjugate(first_weight)
    dirac[1, 2] = second_weight
    dirac[2, 1] = np.conjugate(second_weight)
    idempotents = [matrix_unit(size, index, index) for index in range(size)]

    represented_one = []
    differentials_of_one = []
    for first, second in product(range(size), repeat=2):
        represented_one.append(
            idempotents[first] @ commutator(dirac, idempotents[second])
        )
        differentials_of_one.append(
            commutator(dirac, idempotents[first])
            @ commutator(dirac, idempotents[second])
        )

    represented_one_matrix = np.stack(
        [matrix.reshape(-1) for matrix in represented_one], axis=1
    )
    _, singular_values, right_vectors = np.linalg.svd(
        represented_one_matrix, full_matrices=True
    )
    one_rank = int(np.sum(singular_values > TOLERANCE))
    one_kernel = right_vectors[one_rank:].conjugate().T
    junk_columns = []
    for kernel_index in range(one_kernel.shape[1]):
        junk_matrix = sum(
            one_kernel[generator_index, kernel_index]
            * differentials_of_one[generator_index]
            for generator_index in range(len(differentials_of_one))
        )
        junk_columns.append(junk_matrix.reshape(-1))
    junk_matrix = np.stack(junk_columns, axis=1)
    junk_basis = orthonormal_span(junk_matrix)

    represented_two = []
    for first, second, third in product(range(size), repeat=3):
        represented_two.append(
            idempotents[first]
            @ commutator(dirac, idempotents[second])
            @ commutator(dirac, idempotents[third])
        )
    represented_two_matrix = np.stack(
        [matrix.reshape(-1) for matrix in represented_two], axis=1
    )
    represented_two_basis = orthonormal_span(represented_two_matrix)

    endpoint_forward = matrix_unit(size, 0, 2).reshape(-1)
    endpoint_backward = matrix_unit(size, 2, 0).reshape(-1)
    forward_junk_residual = np.linalg.norm(
        endpoint_forward - junk_basis @ (junk_basis.conjugate().T @ endpoint_forward)
    )
    backward_junk_residual = np.linalg.norm(
        endpoint_backward - junk_basis @ (junk_basis.conjugate().T @ endpoint_backward)
    )
    junk_outside_twoforms = np.linalg.norm(
        junk_basis
        - represented_two_basis
        @ (represented_two_basis.conjugate().T @ junk_basis)
    )

    return {
        "represented_one_rank": one_rank,
        "one_form_kernel_dimension": int(one_kernel.shape[1]),
        "represented_two_rank": matrix_rank(represented_two_matrix),
        "degree_two_junk_rank": matrix_rank(junk_matrix),
        "quotient_rank": matrix_rank(represented_two_matrix)
        - matrix_rank(junk_matrix),
        "endpoint_forward_residual_outside_junk": float(forward_junk_residual),
        "endpoint_backward_residual_outside_junk": float(backward_junk_residual),
        "junk_outside_represented_twoforms": float(junk_outside_twoforms),
    }


def build_dirac(delta, normalization):
    epsilon = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    first_edge = delta
    second_edge = normalization * delta.T @ epsilon
    dirac = np.zeros((10, 10), dtype=complex)
    dirac[0:4, 4:6] = first_edge.conjugate().T
    dirac[4:6, 0:4] = first_edge
    dirac[4:6, 6:10] = second_edge.conjugate().T
    dirac[6:10, 4:6] = second_edge
    return dirac, first_edge, second_edge


def graph_coordinate():
    laplacian = np.array(
        [[1.0, -1.0, 0.0], [-1.0, 2.0, -1.0], [0.0, -1.0, 1.0]]
    )
    reflection = np.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
    eigenvalues, eigenvectors = np.linalg.eigh(laplacian)
    odd_candidates = []
    for index, eigenvalue in enumerate(eigenvalues):
        vector = eigenvectors[:, index]
        reflection_parity = float(np.real(vector @ (reflection @ vector)))
        if reflection_parity < -1.0 + TOLERANCE:
            odd_candidates.append((float(eigenvalue), vector))
    odd_eigenvalue, odd_vector = min(odd_candidates, key=lambda item: item[0])
    coordinate = odd_vector / ((odd_vector[2] - odd_vector[0]) / 2.0)
    if coordinate[2] < coordinate[0]:
        coordinate = -coordinate
    return laplacian, reflection, odd_eigenvalue, coordinate


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    junk_controls = [
        universal_calculus_audit(1.0, 1.0),
        universal_calculus_audit(0.7 + 0.2j, 1.3 - 0.4j),
        universal_calculus_audit(1.8 - 0.6j, 0.5 + 0.9j),
    ]

    laplacian, reflection, odd_eigenvalue, coordinate = graph_coordinate()
    node_coordinate = np.diag(
        np.concatenate(
            [
                np.full(4, coordinate[0]),
                np.full(2, coordinate[1]),
                np.full(4, coordinate[2]),
            ]
        )
    ).astype(complex)

    maximum_errors = {
        "graph_eigenvector_error": float(
            np.linalg.norm(laplacian @ coordinate - odd_eigenvalue * coordinate)
        ),
        "graph_reflection_odd_error": float(
            np.linalg.norm(reflection @ coordinate + coordinate)
        ),
        "edge_isometry_error": 0.0,
        "mapping_cone_endpoint_projection_error": 0.0,
        "determinant_selector_error": 0.0,
        "raw_trace_rank_blind_error": 0.0,
        "ko6_physical_half_error": 0.0,
    }

    for _ in range(RANDOM_TESTS):
        delta = rng.normal(size=(2, 4)) + 1j * rng.normal(size=(2, 4))
        dirac, first_edge, second_edge = build_dirac(delta, 1.0)
        curvature = dirac @ dirac
        relative_curvature = 0.5 * commutator(node_coordinate, curvature)
        endpoint_curvature = np.zeros_like(curvature)
        endpoint_curvature[0:4, 6:10] = curvature[0:4, 6:10]
        endpoint_curvature[6:10, 0:4] = curvature[6:10, 0:4]
        gram = delta @ delta.conjugate().T
        determinant = float(np.real(np.linalg.det(gram)))
        relative_norm = float(
            np.real(np.trace(relative_curvature.conjugate().T @ relative_curvature))
        )
        endpoint_norm = float(
            np.real(np.trace(endpoint_curvature.conjugate().T @ endpoint_curvature))
        )
        raw_trace_four = float(np.real(np.trace(curvature @ curvature)))
        rho = float(np.real(np.trace(gram)))

        maximum_errors["edge_isometry_error"] = max(
            maximum_errors["edge_isometry_error"],
            abs(
                np.linalg.norm(first_edge, "fro") ** 2
                - np.linalg.norm(second_edge, "fro") ** 2
            ),
        )
        maximum_errors["mapping_cone_endpoint_projection_error"] = max(
            maximum_errors["mapping_cone_endpoint_projection_error"],
            abs(relative_norm - endpoint_norm),
        )
        maximum_errors["determinant_selector_error"] = max(
            maximum_errors["determinant_selector_error"],
            abs(relative_norm - 4.0 * determinant),
        )
        maximum_errors["raw_trace_rank_blind_error"] = max(
            maximum_errors["raw_trace_rank_blind_error"],
            abs(raw_trace_four - 4.0 * rho**2),
        )
        doubled_relative_norm = 2.0 * relative_norm
        maximum_errors["ko6_physical_half_error"] = max(
            maximum_errors["ko6_physical_half_error"],
            abs(0.5 * doubled_relative_norm - 4.0 * determinant),
        )

    results = {
        "date": "2026-08-14",
        "random_seed": RANDOM_SEED,
        "random_tests": RANDOM_TESTS,
        "ordinary_connes_calculus_control": {
            "algebra": "C^3 on the three-node path 0-1-2",
            "controls": junk_controls,
            "stable_result": (
                "The endpoint matrix units E_02 and E_20 lie in d(ker pi_1). "
                "The degree-two junk quotient removes rather than selects the length-two endpoint path."
            ),
            "ordinary_junk_selector_pass": False,
        },
        "canonical_graph_coordinate": {
            "path_laplacian": laplacian.tolist(),
            "reflection": reflection.tolist(),
            "lowest_nonzero_reflection_odd_eigenvalue": odd_eigenvalue,
            "endpoint_gap_normalized_coordinate": coordinate.tolist(),
            "uniqueness": "unique up to sign; the normalized commutator is sign-independent at norm level",
        },
        "mapping_cone_relative_derivation": {
            "definition": "delta_h(F)=(1/2)[h,F] with h=(-1,0,1)",
            "effect": "kills diagonal backtracking curvature and retains exactly the 0-2 plus 2-0 endpoint curvature",
            "identity": "||delta_h(D_Delta^2)||_HS^2=4 det(Delta Delta^dagger) at c=1",
            "gauge_covariance": "h acts on node position and commutes with block-diagonal Pati-Salam gauge transformations",
            "continuous_weight_added": False,
        },
        "normalization": {
            "edge_relation": "B_Delta=Delta^T epsilon_2",
            "isometry": "transpose and the unitary SU(2) symplectic form preserve the Frobenius norm",
            "reality_interpretation": "endpoint reflection exchanges 4bar and 4 while pseudoreality exchanges the two edge realizations",
            "consequence": "reflection/reality-invariant single trace-Hodge metric fixes |c|=1; endpoint rephasing fixes c=1",
        },
        "maximum_errors": maximum_errors,
        "verdict": {
            "ordinary_junk_route": "failed",
            "canonical_c_equals_one": "passed inside the reflection/reality-invariant trace-Hodge metric",
            "mapping_cone_projector": "derived from the unique reflection-odd graph coordinate",
            "relative_curvature_selector": "passed",
            "ordinary_spectral_action": "still rank-blind",
            "physical_closure": "conditional",
            "remaining_gate": (
                "derive why the bosonic parent action uses the relative mapping-cone norm "
                "||delta_h(F)||^2 rather than the full ungraded curvature norm, and audit the resulting physical state/gauge ledger"
            ),
        },
    }

    assert all(
        control["endpoint_forward_residual_outside_junk"] < TOLERANCE
        and control["endpoint_backward_residual_outside_junk"] < TOLERANCE
        for control in junk_controls
    )
    assert max(maximum_errors.values()) < 1.0e-9

    Path("s2t_v4_pati_salam_junk_mapping_cone_gate_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()