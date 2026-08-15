#!/usr/bin/env python3
import itertools
import json
import math
from pathlib import Path

import numpy as np

from s2t_family_minimal_operator_menu_exhaustive_audit import (
    jarlskog,
    operator_norm,
)
from s2t_shared_holonomy_two_sector_audit import (
    affine_permutation,
    permutation_matrix,
    restrict,
    triplet_basis,
)


def physical_diagonalization(yukawa):
    squared_mass = yukawa @ yukawa.conj().T
    eigenvalues, eigenvectors = np.linalg.eigh(squared_mass)
    minimum_gap = float(np.min(np.abs(np.diff(eigenvalues))))
    return eigenvalues, eigenvectors, minimum_gap


def chiral_dirac(yukawa):
    zero = np.zeros_like(yukawa)
    return np.block([[zero, yukawa], [yukawa.conj().T, zero]])


def matrix_key(matrix):
    return tuple(
        np.round(
            np.concatenate([matrix.real.ravel(), matrix.imag.ravel()]),
            12,
        )
    )


def operator_menu():
    continuous = json.loads(
        Path("s2t_continuous_wilson_gap_action_results.json").read_text(
            encoding="utf-8"
        )
    )
    axes = [
        np.array(axis, dtype=float)
        for axis in continuous["factor_axis_selector"]["summary"][
            "inverse_length"
        ]["selected_axes"]
    ]
    identity2 = np.eye(2, dtype=int)
    shear2 = np.array([[1, 0], [1, 1]], dtype=int)
    translation_x = affine_permutation(identity2, (1, 0))
    translation_y = affine_permutation(identity2, (0, 1))
    shear = affine_permutation(shear2, (0, 0))
    basis = triplet_basis()
    restricted_x = restrict(permutation_matrix(translation_x), basis)
    restricted_y = restrict(permutation_matrix(translation_y), basis)
    restricted_shear = restrict(permutation_matrix(shear), basis)
    target_cosine = (26.0 - 9.0 * math.sqrt(15.0)) / 11.0
    incidences = [
        target_cosine * np.eye(3)
        + (1.0 - target_cosine) * np.outer(axis, axis)
        for axis in axes
    ]
    commutators = [
        1j * (restricted_shear @ incidence - incidence @ restricted_shear)
        for incidence in incidences
    ]
    kernels = {
        "inverse_length": (1.0 / math.pi, 1.0 / (2.0 * math.pi)),
        "inverse_square": (1.0 / math.pi**2, 1.0 / (4.0 * math.pi**2)),
        "tunneling": (math.exp(-math.pi), math.exp(-2.0 * math.pi)),
    }
    return {
        "restricted_x": restricted_x,
        "restricted_y": restricted_y,
        "restricted_shear": restricted_shear,
        "incidences": incidences,
        "commutators": commutators,
        "kernels": kernels,
    }


def scan_menu(menu):
    coefficients = list(itertools.product([-1, 0, 1], repeat=3))
    rows = []
    maximum_grading_error = 0.0
    maximum_selfadjoint_error = 0.0
    grading = np.diag([-1.0] * 3 + [1.0] * 3)
    for scheme in ["raw", "spectral", "frobenius"]:
        shear = operator_norm(menu["restricted_shear"], scheme)
        incidences = [
            operator_norm(matrix, scheme) for matrix in menu["incidences"]
        ]
        commutators = [
            operator_norm(matrix, scheme) for matrix in menu["commutators"]
        ]
        for kernel_name, (weight3, weight1) in menu["kernels"].items():
            level = weight3 * (np.eye(3) - menu["restricted_x"]) + weight1 * (
                np.eye(3) - menu["restricted_y"]
            )
            candidates = []
            for axis in range(2):
                primitives = [shear, incidences[axis], commutators[axis]]
                for coefficient_tuple in coefficients:
                    yukawa = level.astype(complex)
                    for coefficient, primitive in zip(
                        coefficient_tuple, primitives
                    ):
                        yukawa = yukawa + coefficient * primitive
                    squared_masses, vectors, minimum_gap = (
                        physical_diagonalization(yukawa)
                    )
                    dirac = chiral_dirac(yukawa)
                    maximum_grading_error = max(
                        maximum_grading_error,
                        float(np.linalg.norm(grading @ dirac + dirac @ grading)),
                    )
                    maximum_selfadjoint_error = max(
                        maximum_selfadjoint_error,
                        float(np.linalg.norm(dirac - dirac.conj().T)),
                    )
                    candidates.append(
                        {
                            "axis": axis,
                            "coefficients": coefficient_tuple,
                            "yukawa": yukawa,
                            "squared_masses": squared_masses,
                            "vectors": vectors,
                            "minimum_squared_mass_gap": minimum_gap,
                        }
                    )

            valid = [
                row
                for row in candidates
                if row["minimum_squared_mass_gap"] > 1e-9
            ]
            full_mixing_pairs = 0
            cp_pairs = 0
            same_coefficients_cp = 0
            commutator_free_cp = 0
            signatures = set()
            maximum_abs_j = 0.0
            minimum_support = None
            for upper in valid:
                for lower in valid:
                    mixing = upper["vectors"].conj().T @ lower["vectors"]
                    full_mixing = bool(np.all(np.abs(mixing) > 1e-7))
                    abs_j = abs(jarlskog(mixing))
                    cp = full_mixing and abs_j > 1e-9
                    full_mixing_pairs += int(full_mixing)
                    cp_pairs += int(cp)
                    same_coefficients_cp += int(
                        cp and upper["coefficients"] == lower["coefficients"]
                    )
                    both_commutators_zero = (
                        upper["coefficients"][2] == 0
                        and lower["coefficients"][2] == 0
                    )
                    commutator_free_cp += int(cp and both_commutators_zero)
                    if cp:
                        support = sum(
                            coefficient != 0
                            for coefficient in (
                                upper["coefficients"] + lower["coefficients"]
                            )
                        )
                        minimum_support = (
                            support
                            if minimum_support is None
                            else min(minimum_support, support)
                        )
                        maximum_abs_j = max(maximum_abs_j, abs_j)
                        signatures.add(
                            tuple(np.round(np.abs(mixing).ravel(), 6))
                            + (round(abs_j, 8),)
                        )
            rows.append(
                {
                    "normalization": scheme,
                    "kernel": kernel_name,
                    "sector_candidates_before_deduplication": len(candidates),
                    "unique_yukawa_blocks": len(
                        {matrix_key(row["yukawa"]) for row in candidates}
                    ),
                    "squared_mass_nondegenerate_candidates": len(valid),
                    "squared_mass_degenerate_candidates": len(candidates)
                    - len(valid),
                    "ordered_physical_sector_pairs": len(valid) ** 2,
                    "full_mixing_pairs": full_mixing_pairs,
                    "nonzero_CP_pairs": cp_pairs,
                    "same_coefficient_CP_pairs": same_coefficients_cp,
                    "commutator_free_CP_pairs": commutator_free_cp,
                    "unique_absolute_CP_signatures": len(signatures),
                    "minimum_nonzero_coefficient_support_for_CP": minimum_support,
                    "maximum_abs_J": maximum_abs_j,
                }
            )
    return rows, maximum_grading_error, maximum_selfadjoint_error


def independent_svd_check(menu):
    weight3, weight1 = menu["kernels"]["inverse_length"]
    level = weight3 * (np.eye(3) - menu["restricted_x"]) + weight1 * (
        np.eye(3) - menu["restricted_y"]
    )
    yukawa = (
        level.astype(complex)
        + menu["restricted_shear"]
        + menu["incidences"][0]
        + menu["commutators"][0]
    )
    squared_masses, eigenvectors, _ = physical_diagonalization(yukawa)
    left_vectors, singular_values, _ = np.linalg.svd(yukawa)
    order = np.argsort(singular_values)
    absolute_overlap = np.abs(
        eigenvectors.conj().T @ left_vectors[:, order]
    )
    return {
        "squared_mass_error": float(
            np.max(np.abs(squared_masses - np.square(singular_values[order])))
        ),
        "left_singular_vector_overlap_error": float(
            np.max(np.abs(absolute_overlap - np.eye(3)))
        ),
    }


def primitive_span_rank(menu):
    primitives = [
        menu["restricted_shear"],
        *menu["incidences"],
        *menu["commutators"],
    ]
    vectors = [
        np.concatenate([matrix.real.ravel(), matrix.imag.ravel()])
        for matrix in primitives
    ]
    return int(np.linalg.matrix_rank(np.stack(vectors), tol=1e-10))


def main():
    menu = operator_menu()
    rows, grading_error, selfadjoint_error = scan_menu(menu)
    svd_check = independent_svd_check(menu)
    representative = next(
        row
        for row in rows
        if row["normalization"] == "raw"
        and row["kernel"] == "inverse_length"
    )
    span_rank = primitive_span_rank(menu)
    previous = json.loads(
        Path("s2t_family_minimal_operator_menu_exhaustive_results.json").read_text(
            encoding="utf-8"
        )
    )["representative_raw_result"]
    results = {
        "status": "chiral_doubling_repairs_the_grading_but_does_not_select_Yukawa_blocks_and_the_physical_menu_remains_highly_underdetermined",
        "date": "2026-08-06",
        "blind_protocol": {
            "observed_quark_masses_loaded": False,
            "observed_CKM_loaded": False,
            "input_menu": "the previously declared L, S, A_n and i[S,A_n] operators",
            "coefficient_menu": "(a,b,d) in {-1,0,1}^3 independently per sector",
        },
        "chiral_embedding_gate": {
            "family_space": "V3_left direct_sum V3_right",
            "grading": "Gamma=diag(-I3,+I3)",
            "Dirac_operator": "D(Y)=[[0,Y],[Y^dagger,0]]",
            "Dirac_square": "D(Y)^2=diag(Y Y^dagger,Y^dagger Y)",
            "maximum_grading_anticommutator_error": grading_error,
            "maximum_selfadjoint_error": selfadjoint_error,
            "finding": (
                "The chiral doubling is a valid odd self-adjoint embedding for every complex "
                "3x3 Yukawa block Y; grading alone imposes no family texture."
            ),
        },
        "physical_readout_correction": {
            "left_squared_mass_operator": "H=Y Y^dagger",
            "independent_SVD_check": svd_check,
            "previous_menu_diagonalized_Hermitian_M_directly": True,
            "finding": (
                "The physical rescan orders states by squared singular values; all declared "
                "menu candidates remain nondegenerate in squared mass."
            ),
        },
        "discrete_menu_scan": {
            "rows": rows,
            "representative_raw_inverse_length": representative,
            "previous_direct_matrix_result": {
                "ordered_sector_pairs": previous["ordered_sector_pairs"],
                "nonzero_CP_pairs": previous["nonzero_CP_pairs"],
                "unique_absolute_CP_signatures": previous[
                    "unique_absolute_CP_signatures"
                ],
            },
        },
        "selector_gate": {
            "primitive_real_linear_span_rank": span_rank,
            "general_complex_Y_real_dimension": 18,
            "two_sector_general_real_dimension_before_basis_quotients": 36,
            "same_sector_block_consequence": "Y_u=Y_d gives identity CKM",
            "finding": (
                "Chiral doubling supplies the correct left-right architecture but neither "
                "chooses distinct up/down blocks nor fixes their discrete coefficients, "
                "normalization or CP orientation."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "The canonical affine triplet is preserved and the finite Dirac operator is "
                "strictly odd without adding or eliminating a fourth family mode."
            ),
            "negative": (
                "Every complex 3x3 Yukawa matrix is compatible with the grading. Restricting "
                "to the existing discrete menu still leaves many physical CP candidates, so "
                "the construction repairs consistency but adds no selector."
            ),
            "next_gate": (
                "Specify the represented finite algebra, real structure and first-order "
                "condition, then classify which Yukawa blocks survive. Without those data, "
                "the doubled-triplet route is a kinematic container rather than a prediction."
            ),
        },
    }
    assert grading_error < 1e-12
    assert selfadjoint_error < 1e-12
    assert svd_check["squared_mass_error"] < 1e-12
    assert svd_check["left_singular_vector_overlap_error"] < 1e-12
    assert representative["nonzero_CP_pairs"] > 100
    assert representative["same_coefficient_CP_pairs"] == 0
    assert representative["commutator_free_CP_pairs"] == 0
    Path("s2t_chiral_doubled_triplet_yukawa_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "primitive_span_rank": span_rank,
                "physical_candidates": representative[
                    "squared_mass_nondegenerate_candidates"
                ],
                "physical_CP_pairs": representative["nonzero_CP_pairs"],
                "physical_CP_signatures": representative[
                    "unique_absolute_CP_signatures"
                ],
                "next_gate": results["scientific_verdict"]["next_gate"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()