#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np

from s2t_v4_pati_salam_first_order_kernel import (
    algebra_representation,
    dirac_from_channels,
    opposite_representation,
)


OUTPUT_PATH = Path("s2t_v4_pati_salam_generalized_inner_fluctuation_results.json")
RANDOM_SEED = 20260813
SAMPLE_COUNT = 600
UNITARY_TEST_COUNT = 20
TOLERANCE = 1.0e-9


def algebra_star(element):
    return tuple(matrix.conj().T for matrix in element)


def identity_element():
    return np.eye(2), np.eye(2), np.eye(4)


def random_quaternion_unitary(rng):
    coordinates = rng.normal(size=4)
    coordinates /= np.linalg.norm(coordinates)
    alpha = coordinates[0] + 1j * coordinates[1]
    beta = coordinates[2] + 1j * coordinates[3]
    return np.array(
        [[alpha, beta], [-np.conj(beta), np.conj(alpha)]], dtype=complex
    )


def random_unitary(size, rng):
    matrix = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    unitary, triangular = np.linalg.qr(matrix)
    diagonal = np.diag(triangular)
    return unitary @ np.diag(np.conj(diagonal) / np.abs(diagonal))


def random_algebra_unitary(rng):
    return (
        random_quaternion_unitary(rng),
        random_quaternion_unitary(rng),
        random_unitary(4, rng),
    )


def physical_seed():
    lepton_projector = np.diag([1.0, 0.0, 0.0, 0.0])
    quark_projector = np.eye(4) - lepton_projector
    lepton_yukawa = np.diag([0.7, 0.2])
    quark_yukawa = np.diag([1.1, 0.4])
    yukawa = np.kron(lepton_yukawa, lepton_projector)
    yukawa += np.kron(quark_yukawa, quark_projector)
    majorana_right = np.zeros((8, 8), dtype=complex)
    majorana_right[0, 0] = 0.9
    return dirac_from_channels(yukawa, majorana_right, None), yukawa, majorana_right


def generalized_fluctuation(dirac, terms):
    linear = np.zeros_like(dirac)
    opposite_linear = np.zeros_like(dirac)
    represented = []
    for coefficient, element in terms:
        element_star = algebra_star(element)
        represented.append(
            (
                coefficient,
                algebra_representation(element),
                algebra_representation(element_star),
                opposite_representation(element),
                opposite_representation(element_star),
            )
        )
    for coefficient, left, right, opposite_left, opposite_right in represented:
        linear += coefficient * left @ (dirac @ right - right @ dirac)
        opposite_linear += coefficient * opposite_left @ (
            dirac @ opposite_right - opposite_right @ dirac
        )
    quadratic = np.zeros_like(dirac)
    for coefficient_j, _, _, opposite_left_j, opposite_right_j in represented:
        for coefficient_k, left_k, right_k, _, _ in represented:
            commutator = dirac @ right_k - right_k @ dirac
            double_commutator = (
                commutator @ opposite_right_j - opposite_right_j @ commutator
            )
            quadratic += (
                coefficient_j
                * coefficient_k
                * opposite_left_j
                @ left_k
                @ double_commutator
            )
    fluctuated = dirac + linear + opposite_linear + quadratic
    return fluctuated, linear, opposite_linear, quadratic


def real_vector(matrix):
    return np.concatenate((matrix.real.ravel(), matrix.imag.ravel()))


def real_span_rank(vectors):
    matrix = np.asarray(vectors)
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    threshold = max(TOLERANCE, singular_values[0] * 1.0e-10)
    return int(np.sum(singular_values > threshold))


def weak_color_reshuffle(yukawa):
    tensor = yukawa.reshape(2, 4, 2, 4)
    return np.transpose(tensor, (0, 2, 1, 3)).reshape(4, 16)


def crossed_majorana_reshuffle(majorana):
    tensor = majorana.reshape(2, 4, 2, 4)
    return np.transpose(tensor, (0, 3, 2, 1)).reshape(8, 8)


def tilde_matrix(matrix):
    epsilon = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    return epsilon @ matrix.conj() @ np.linalg.inv(epsilon)


def tilde_subspace_error(reshuffled):
    left_vectors, _, _ = np.linalg.svd(reshuffled, full_matrices=False)
    basis = left_vectors[:, :2]
    projector = basis @ basis.conj().T
    complement = np.eye(4) - projector
    errors = []
    for column in range(2):
        transformed = tilde_matrix(basis[:, column].reshape(2, 2)).reshape(4)
        errors.append(np.linalg.norm(complement @ transformed))
    return max(errors)


def valid_affine_terms(rng, random_term_count=3):
    coefficients = rng.normal(size=random_term_count)
    coefficients = np.concatenate((coefficients, [1.0 - np.sum(coefficients)]))
    elements = [random_algebra_unitary(rng) for _ in range(random_term_count)]
    elements.append(identity_element())
    return list(zip(coefficients, elements))


def normalization_error(terms):
    accumulated = [np.zeros((2, 2), complex), np.zeros((2, 2), complex), np.zeros((4, 4), complex)]
    for coefficient, element in terms:
        for index, matrix in enumerate(element):
            accumulated[index] += coefficient * matrix @ matrix.conj().T
    identities = [np.eye(2), np.eye(2), np.eye(4)]
    return max(np.linalg.norm(value - identity) for value, identity in zip(accumulated, identities))


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    dirac, seed_yukawa, seed_majorana = physical_seed()
    spans = {
        "total_yukawa": [],
        "total_majorana_right": [],
        "total_majorana_left": [],
        "linear_yukawa": [],
        "linear_majorana_right": [],
        "quadratic_yukawa": [],
        "quadratic_majorana_right": [],
    }
    maxima = {
        "pert_normalization_error": 0.0,
        "self_adjointness_error": 0.0,
        "dirac_block_reconstruction_error": 0.0,
        "majorana_symmetry_error": 0.0,
        "left_majorana_norm": 0.0,
        "yukawa_third_singular_ratio": 0.0,
        "majorana_second_singular_ratio": 0.0,
        "majorana_reshuffle_symmetry_error": 0.0,
        "tilde_subspace_error": 0.0,
    }
    observed_yukawa_reshuffle_ranks = set()
    observed_majorana_reshuffle_ranks = set()

    for _ in range(SAMPLE_COUNT):
        terms = valid_affine_terms(rng)
        fluctuated, linear, _, quadratic = generalized_fluctuation(dirac, terms)
        yukawa = fluctuated[:8, 8:16]
        majorana_right = fluctuated[:8, 16:24]
        majorana_left = fluctuated[8:16, 24:32]
        spans["total_yukawa"].append(real_vector(yukawa - seed_yukawa))
        spans["total_majorana_right"].append(
            real_vector(majorana_right - seed_majorana)
        )
        spans["total_majorana_left"].append(real_vector(majorana_left))
        spans["linear_yukawa"].append(real_vector(linear[:8, 8:16]))
        spans["linear_majorana_right"].append(real_vector(linear[:8, 16:24]))
        spans["quadratic_yukawa"].append(real_vector(quadratic[:8, 8:16]))
        spans["quadratic_majorana_right"].append(
            real_vector(quadratic[:8, 16:24])
        )

        reconstructed = dirac_from_channels(yukawa, majorana_right, majorana_left)
        maxima["pert_normalization_error"] = max(
            maxima["pert_normalization_error"], normalization_error(terms)
        )
        maxima["self_adjointness_error"] = max(
            maxima["self_adjointness_error"],
            float(np.linalg.norm(fluctuated - fluctuated.conj().T)),
        )
        maxima["dirac_block_reconstruction_error"] = max(
            maxima["dirac_block_reconstruction_error"],
            float(np.linalg.norm(fluctuated - reconstructed)),
        )
        maxima["majorana_symmetry_error"] = max(
            maxima["majorana_symmetry_error"],
            float(np.linalg.norm(majorana_right - majorana_right.T)),
        )
        maxima["left_majorana_norm"] = max(
            maxima["left_majorana_norm"], float(np.linalg.norm(majorana_left))
        )

        yukawa_reshuffled = weak_color_reshuffle(yukawa)
        yukawa_singular = np.linalg.svd(yukawa_reshuffled, compute_uv=False)
        observed_yukawa_reshuffle_ranks.add(
            int(np.linalg.matrix_rank(yukawa_reshuffled, tol=TOLERANCE))
        )
        maxima["yukawa_third_singular_ratio"] = max(
            maxima["yukawa_third_singular_ratio"],
            float(yukawa_singular[2] / yukawa_singular[0]),
        )
        maxima["tilde_subspace_error"] = max(
            maxima["tilde_subspace_error"], tilde_subspace_error(yukawa_reshuffled)
        )

        majorana_reshuffled = crossed_majorana_reshuffle(majorana_right)
        majorana_singular = np.linalg.svd(majorana_reshuffled, compute_uv=False)
        observed_majorana_reshuffle_ranks.add(
            int(np.linalg.matrix_rank(majorana_reshuffled, tol=TOLERANCE))
        )
        maxima["majorana_second_singular_ratio"] = max(
            maxima["majorana_second_singular_ratio"],
            float(majorana_singular[1] / majorana_singular[0]),
        )
        maxima["majorana_reshuffle_symmetry_error"] = max(
            maxima["majorana_reshuffle_symmetry_error"],
            float(np.linalg.norm(majorana_reshuffled - majorana_reshuffled.T)),
        )

    unitary_errors = []
    omitted_quadratic_errors = []
    quadratic_norms = []
    for _ in range(UNITARY_TEST_COUNT):
        element = random_algebra_unitary(rng)
        fluctuated, linear, opposite_linear, quadratic = generalized_fluctuation(
            dirac, [(1.0, element)]
        )
        gauge_unitary = algebra_representation(element) @ opposite_representation(element)
        gauge_conjugate = gauge_unitary @ dirac @ gauge_unitary.conj().T
        unitary_errors.append(float(np.linalg.norm(fluctuated - gauge_conjugate)))
        omitted_quadratic_errors.append(
            float(np.linalg.norm(dirac + linear + opposite_linear - gauge_conjugate))
        )
        quadratic_norms.append(float(np.linalg.norm(quadratic)))

    results = {
        "random_seed": RANDOM_SEED,
        "sample_count": SAMPLE_COUNT,
        "unitary_test_count": UNITARY_TEST_COUNT,
        "seed": {
            "lepton_yukawa_diagonal": [0.7, 0.2],
            "quark_yukawa_diagonal": [1.1, 0.4],
            "right_neutrino_majorana": 0.9,
        },
        "real_sample_span_ranks": {
            name: real_span_rank(vectors) for name, vectors in spans.items()
        },
        "single_configuration_constraints": {
            "yukawa_weak_color_reshuffle_ranks": sorted(
                observed_yukawa_reshuffle_ranks
            ),
            "majorana_crossed_reshuffle_ranks": sorted(
                observed_majorana_reshuffle_ranks
            ),
            **maxima,
        },
        "unitary_orbit_test": {
            "maximum_full_formula_error": max(unitary_errors),
            "minimum_error_without_quadratic_term": min(omitted_quadratic_errors),
            "maximum_relative_difference_omission_vs_quadratic_norm": max(
                abs(error - norm) / norm
                for error, norm in zip(omitted_quadratic_errors, quadratic_norms)
            ),
        },
        "interpretation": {
            "linear_yukawa_rank_8": "bidoublet phi sector",
            "linear_majorana_rank_16": "Delta(2_R,4) sector",
            "rank_2_yukawa_reshuffle": "phi and tilde(phi) composite form",
            "rank_1_crossed_majorana_reshuffle": "H_(aI,bJ)=k Delta_(aJ) Delta_(bI)",
            "warning": "sample-span ranks are ambient linear spans, not manifold dimensions",
        },
    }
    OUTPUT_PATH.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()