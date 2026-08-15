#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np

from s2t_v4_pati_salam_finite_dirac_block import ko6_operators
from s2t_v4_pati_salam_first_order_kernel import (
    algebra_representation,
    reconstruct_dirac,
    sm_analytic_kernel,
)
from s2t_v4_pati_salam_generalized_inner_fluctuation import (
    crossed_majorana_reshuffle,
    generalized_fluctuation,
    physical_seed,
    random_algebra_unitary,
    valid_affine_terms,
)
from s2t_v4_pati_salam_wedge_channel_compatibility import (
    direct_channel,
    wedge_channel,
)


OUTPUT_PATH = Path("s2t_v4_pati_salam_twoform_a2_trilemma_results.json")
RANDOM_SEED = 20260814
TWO_FORM_TESTS = 200
PHYSICAL_SEED_TESTS = 200
GENERIC_SEED_TESTS = 800
TOLERANCE = 1.0e-9


def represented_commutator(dirac, element):
    representation = algebra_representation(element)
    return dirac @ representation - representation @ dirac


def represented_two_form(dirac, left, first, second):
    return (
        algebra_representation(left)
        @ represented_commutator(dirac, first)
        @ represented_commutator(dirac, second)
    )


def real_vector(matrix):
    return np.concatenate((matrix.real.ravel(), matrix.imag.ravel()))


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    physical_dirac, _, _ = physical_seed()
    _, grading = ko6_operators(8)

    two_form_even_error = 0.0
    wedge_odd_error = 0.0
    wedge_two_form_overlap = 0.0
    for _ in range(TWO_FORM_TESTS):
        left = random_algebra_unitary(rng)
        first = random_algebra_unitary(rng)
        second = random_algebra_unitary(rng)
        two_form = represented_two_form(physical_dirac, left, first, second)
        two_form_even_error = max(
            two_form_even_error,
            float(np.linalg.norm(grading @ two_form - two_form @ grading)),
        )
        delta = rng.normal(size=(2, 4)) + 1j * rng.normal(size=(2, 4))
        wedge_dirac = reconstruct_dirac(np.zeros(272))
        wedge_dirac[:8, 16:24] = wedge_channel(delta)
        wedge_dirac[16:24, :8] = wedge_channel(delta).conj().T
        wedge_odd_error = max(
            wedge_odd_error,
            float(np.linalg.norm(grading @ wedge_dirac + wedge_dirac @ grading)),
        )
        wedge_two_form_overlap = max(
            wedge_two_form_overlap,
            abs(complex(np.vdot(wedge_dirac, two_form))),
        )

    physical_crossed_ratio = 0.0
    physical_crossed_ranks = set()
    for _ in range(PHYSICAL_SEED_TESTS):
        quadratic = generalized_fluctuation(
            physical_dirac, valid_affine_terms(rng)
        )[3]
        majorana = quadratic[:8, 16:24]
        reshuffled = crossed_majorana_reshuffle(majorana)
        singular_values = np.linalg.svd(reshuffled, compute_uv=False)
        if singular_values[0] > TOLERANCE:
            physical_crossed_ratio = max(
                physical_crossed_ratio,
                float(singular_values[1] / singular_values[0]),
            )
            physical_crossed_ranks.add(
                int(np.linalg.matrix_rank(reshuffled, tol=TOLERANCE))
            )

    majorana_seed_basis = sm_analytic_kernel()[:, -16:]
    generic_vectors = []
    generic_symmetry_error = 0.0
    generic_ordinary_ranks = set()
    generic_crossed_ranks = set()
    for _ in range(GENERIC_SEED_TESTS):
        coefficients = rng.normal(size=16)
        generic_dirac = reconstruct_dirac(majorana_seed_basis @ coefficients)
        quadratic = generalized_fluctuation(
            generic_dirac, valid_affine_terms(rng)
        )[3]
        majorana = quadratic[:8, 16:24]
        generic_vectors.append(real_vector(majorana))
        generic_symmetry_error = max(
            generic_symmetry_error,
            float(np.linalg.norm(majorana - majorana.T)),
        )
        generic_ordinary_ranks.add(
            int(np.linalg.matrix_rank(majorana, tol=TOLERANCE))
        )
        generic_crossed_ranks.add(
            int(
                np.linalg.matrix_rank(
                    crossed_majorana_reshuffle(majorana), tol=TOLERANCE
                )
            )
        )

    generic_matrix = np.asarray(generic_vectors)
    _, singular_values, right_vectors = np.linalg.svd(
        generic_matrix, full_matrices=False
    )
    threshold = singular_values[0] * 1.0e-10
    generic_span_rank = int(np.sum(singular_values > threshold))
    generic_basis = right_vectors[:generic_span_rank].T

    target_delta = rng.normal(size=(2, 4)) + 1j * rng.normal(size=(2, 4))
    targets = {
        "direct": direct_channel(target_delta),
        "wedge": wedge_channel(target_delta),
    }
    projection_errors = {}
    for name, target in targets.items():
        target_vector = real_vector(target)
        projected = generic_basis @ (generic_basis.T @ target_vector)
        projection_errors[name] = float(
            np.linalg.norm(target_vector - projected) / np.linalg.norm(target_vector)
        )

    results = {
        "date": "2026-08-14",
        "random_seed": RANDOM_SEED,
        "ordinary_two_forms": {
            "tests": TWO_FORM_TESTS,
            "maximum_even_grading_error": two_form_even_error,
            "maximum_wedge_odd_grading_error": wedge_odd_error,
            "maximum_frobenius_overlap_with_odd_wedge_block": wedge_two_form_overlap,
            "junk_quotient_parity_statement": (
                "degree-two junk is a subspace of the even represented two-forms, "
                "so quotienting cannot create the odd Majorana wedge block"
            ),
        },
        "physical_seed_A2": {
            "tests": PHYSICAL_SEED_TESTS,
            "observed_crossed_reshuffle_ranks": sorted(physical_crossed_ranks),
            "maximum_second_to_first_crossed_singular_ratio": physical_crossed_ratio,
            "interpretation": "the physical Standard-Model seed produces only the crossed rank-one orbit",
        },
        "generic_SM_kernel_seed_A2": {
            "tests": GENERIC_SEED_TESTS,
            "seed_real_dimension": 16,
            "quadratic_majorana_real_span_rank": generic_span_rank,
            "full_complex_symmetric_channel_real_dimension": 72,
            "smallest_retained_singular_value": float(
                singular_values[generic_span_rank - 1]
            ),
            "largest_discarded_singular_value": float(
                singular_values[generic_span_rank]
            ),
            "retained_to_discarded_singular_gap": float(
                singular_values[generic_span_rank - 1]
                / singular_values[generic_span_rank]
            ),
            "maximum_symmetry_error": generic_symmetry_error,
            "observed_ordinary_matrix_ranks": sorted(generic_ordinary_ranks),
            "observed_crossed_reshuffle_ranks": sorted(generic_crossed_ranks),
            "relative_projection_errors": projection_errors,
            "interpretation": (
                "the generic allowed seed spans the entire symmetric Majorana channel; "
                "direct and wedge targets are available only together with all competitors"
            ),
        },
        "verdict": {
            "ordinary_two_form_wedge_block_pass": False,
            "physical_seed_direct_path_pass": False,
            "generic_seed_predictive_selector_pass": False,
            "trilemma": [
                "ordinary two-forms have the wrong grading parity for the wedge Majorana block",
                "the physical seed gives only the crossed rank-one path",
                "the generic allowed seed spans all 72 real symmetric Majorana directions",
            ],
            "not_excluded": (
                "an even gauge-singlet curvature functional may still encode the determinant "
                "after the full degree-two junk quotient"
            ),
            "next_gate": (
                "compute only the even singlet sector of the represented two-form quotient; "
                "if it cannot distinguish rank, test a valid vectorlike fundamental-module extension"
            ),
        },
    }
    OUTPUT_PATH.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()