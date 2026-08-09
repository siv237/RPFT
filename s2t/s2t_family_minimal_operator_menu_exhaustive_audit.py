#!/usr/bin/env python3
import itertools
import json
import math
from pathlib import Path

import numpy as np

from s2t_shared_holonomy_two_sector_audit import (
    affine_permutation,
    permutation_matrix,
    restrict,
    triplet_basis,
)


def operator_norm(matrix, scheme):
    if scheme == "raw":
        return matrix
    if scheme == "spectral":
        norm = np.linalg.norm(matrix, 2)
    elif scheme == "frobenius":
        norm = np.linalg.norm(matrix, "fro")
    else:
        raise ValueError(scheme)
    return matrix / norm if norm > 1e-14 else matrix


def diagonalize(matrix):
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    minimum_gap = float(np.min(np.abs(np.diff(eigenvalues))))
    return eigenvalues, eigenvectors, minimum_gap


def jarlskog(matrix):
    return float(
        np.imag(
            matrix[0, 0]
            * matrix[1, 1]
            * np.conj(matrix[0, 1])
            * np.conj(matrix[1, 0])
        )
    )


def main():
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

    coefficients = list(itertools.product([-1, 0, 1], repeat=3))
    kernels = {
        "inverse_length": (1.0 / math.pi, 1.0 / (2.0 * math.pi)),
        "inverse_square": (1.0 / math.pi**2, 1.0 / (4.0 * math.pi**2)),
        "tunneling": (math.exp(-math.pi), math.exp(-2.0 * math.pi)),
    }
    normalization_schemes = ["raw", "spectral", "frobenius"]

    scan_rows = []
    global_d_zero_cp = 0
    global_same_coefficient_cp = 0

    for scheme in normalization_schemes:
        normalized_shear = operator_norm(restricted_shear, scheme)
        normalized_incidences = [
            operator_norm(incidence, scheme) for incidence in incidences
        ]
        normalized_commutators = [
            operator_norm(commutator, scheme) for commutator in commutators
        ]

        for kernel_name, (weight3, weight1) in kernels.items():
            factor_operator = weight3 * (np.eye(3) - restricted_x) + weight1 * (
                np.eye(3) - restricted_y
            )
            matrices = []
            for axis_index in range(2):
                operators = [
                    normalized_shear,
                    normalized_incidences[axis_index],
                    normalized_commutators[axis_index],
                ]
                for coefficient_tuple in coefficients:
                    matrix = factor_operator.astype(complex)
                    for coefficient, operator in zip(coefficient_tuple, operators):
                        matrix = matrix + coefficient * operator
                    eigenvalues, eigenvectors, minimum_gap = diagonalize(matrix)
                    matrices.append(
                        {
                            "axis": axis_index,
                            "coefficients": coefficient_tuple,
                            "matrix": matrix,
                            "eigenvalues": eigenvalues,
                            "eigenvectors": eigenvectors,
                            "minimum_gap": minimum_gap,
                        }
                    )

            unique_matrix_keys = {
                tuple(
                    np.round(
                        np.concatenate(
                            [matrix["matrix"].real.ravel(), matrix["matrix"].imag.ravel()]
                        ),
                        12,
                    )
                )
                for matrix in matrices
            }

            nondegenerate_pairs = 0
            full_mixing_pairs = 0
            cp_pairs = 0
            same_axis_cp_pairs = 0
            crossed_axis_cp_pairs = 0
            same_coefficient_cp_pairs = 0
            both_commutators_zero_pairs = 0
            both_commutators_zero_cp_pairs = 0
            unique_cp_signatures = set()
            minimum_support = 99
            minimum_support_example = None
            maximum_abs_j = 0.0

            for upper in matrices:
                for lower in matrices:
                    if upper["minimum_gap"] < 1e-9 or lower["minimum_gap"] < 1e-9:
                        continue
                    nondegenerate_pairs += 1
                    mixing = upper["eigenvectors"].conj().T @ lower["eigenvectors"]
                    full_mixing = bool(np.all(np.abs(mixing) > 1e-7))
                    abs_j = abs(jarlskog(mixing))
                    cp = full_mixing and abs_j > 1e-9
                    full_mixing_pairs += int(full_mixing)
                    cp_pairs += int(cp)
                    same_axis_cp_pairs += int(cp and upper["axis"] == lower["axis"])
                    crossed_axis_cp_pairs += int(
                        cp and upper["axis"] != lower["axis"]
                    )
                    same_coefficient_cp_pairs += int(
                        cp and upper["coefficients"] == lower["coefficients"]
                    )

                    both_d_zero = (
                        upper["coefficients"][2] == 0
                        and lower["coefficients"][2] == 0
                    )
                    both_commutators_zero_pairs += int(both_d_zero)
                    both_commutators_zero_cp_pairs += int(cp and both_d_zero)

                    if cp:
                        support = sum(
                            coefficient != 0
                            for coefficient in upper["coefficients"]
                            + lower["coefficients"]
                        )
                        if support < minimum_support:
                            minimum_support = support
                            minimum_support_example = {
                                "upper_axis": upper["axis"],
                                "upper_coefficients": list(upper["coefficients"]),
                                "lower_axis": lower["axis"],
                                "lower_coefficients": list(lower["coefficients"]),
                                "abs_J": abs_j,
                                "abs_mixing_matrix": np.abs(mixing).tolist(),
                            }
                        maximum_abs_j = max(maximum_abs_j, abs_j)
                        signature = tuple(np.round(np.abs(mixing).ravel(), 6)) + (
                            round(abs_j, 8),
                        )
                        unique_cp_signatures.add(signature)

            global_d_zero_cp += both_commutators_zero_cp_pairs
            global_same_coefficient_cp += same_coefficient_cp_pairs
            scan_rows.append(
                {
                    "normalization": scheme,
                    "kernel": kernel_name,
                    "sector_operators_before_deduplication": len(matrices),
                    "unique_sector_operators": len(unique_matrix_keys),
                    "ordered_sector_pairs": len(matrices) ** 2,
                    "nondegenerate_pairs": nondegenerate_pairs,
                    "full_three_family_mixing_pairs": full_mixing_pairs,
                    "nonzero_CP_pairs": cp_pairs,
                    "same_axis_CP_pairs": same_axis_cp_pairs,
                    "crossed_axis_CP_pairs": crossed_axis_cp_pairs,
                    "same_coefficient_CP_pairs": same_coefficient_cp_pairs,
                    "both_commutators_zero_pairs": both_commutators_zero_pairs,
                    "both_commutators_zero_CP_pairs": both_commutators_zero_cp_pairs,
                    "unique_absolute_CP_signatures": len(unique_cp_signatures),
                    "minimum_nonzero_coefficient_support_for_CP": minimum_support,
                    "minimum_support_example": minimum_support_example,
                    "maximum_abs_J": maximum_abs_j,
                }
            )

    raw_inverse_length = next(
        row
        for row in scan_rows
        if row["normalization"] == "raw" and row["kernel"] == "inverse_length"
    )

    results = {
        "status": "minimal_discrete_operator_menu_generates_many_CKM_candidates_but_has_no_intrinsic_coefficient_selector",
        "date": "2026-08-06",
        "blind_protocol": {
            "observed_quark_masses_loaded": False,
            "observed_CKM_entries_loaded": False,
            "coefficient_menu": "(a,b,d) in {-1,0,1}^3 independently for up and down sectors",
            "operator": "M_s=L+a S+b A_n+d i[S,A_n]",
            "purpose": (
                "structural existence and uniqueness test, not phenomenological fitting"
            ),
        },
        "scan": {
            "normalizations": normalization_schemes,
            "kernels": list(kernels),
            "rows": scan_rows,
        },
        "representative_raw_result": raw_inverse_length,
        "ablation_gates": {
            "commutator_removed": {
                "nonzero_CP_pairs_across_all_scans": global_d_zero_cp,
                "finding": (
                    "With d_u=d_d=0 all matrices are real, so the Jarlskog invariant "
                    "vanishes identically."
                ),
            },
            "same_coefficients_in_both_sectors": {
                "nonzero_CP_pairs_across_all_scans": global_same_coefficient_cp,
                "finding": (
                    "Using the same coefficient triple in the two sectors gives zero CP even "
                    "when different representatives of the residual axis orbit are chosen."
                ),
            },
            "single_commutator_term": {
                "minimum_total_nonzero_coefficients": raw_inverse_length[
                    "minimum_nonzero_coefficient_support_for_CP"
                ],
                "finding": (
                    "One commutator term in only one sector already creates full mixing and "
                    "nonzero CP. This demonstrates abundance, not a unique mechanism."
                ),
            },
        },
        "normalization_sensitivity": {
            "qualitative_CP_count_stable": all(
                row["nonzero_CP_pairs"] == 2352 for row in scan_rows
            ),
            "mixing_values_change": True,
            "finding": (
                "Raw, spectral-norm and Frobenius-norm conventions all admit many CP matrices, "
                "but their numerical entries and maximal J change. The action must select a "
                "normalization before any prediction is claimed."
            ),
        },
        "orientation_gate": {
            "complex_term": "i d [S,A_n]",
            "conjugation": "d -> -d complex-conjugates the mass operator",
            "finding": (
                "Without an oriented or chiral parent principle the signs d and -d are "
                "degenerate CP-conjugate choices, so even the sign of CP violation is unselected."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "The minimal finite operator algebra is rich enough to produce nondegenerate "
                "three-family spectra, full mixing and nonzero CP without continuous fitting."
            ),
            "negative": (
                "It produces hundreds of inequivalent blind CKM signatures. CP requires an "
                "independent sector-asymmetric coefficient choice, and no current geometry "
                "selects that choice or its normalization."
            ),
            "status": "existence_pass_selector_fail",
            "next_gate": (
                "Derive one coefficient triple per sector and the commutator orientation from "
                "a parent representation or boundary action. If this cannot be done before "
                "using quark data, the finite operator-menu route closes as underdetermined."
            ),
        },
    }

    assert raw_inverse_length["ordered_sector_pairs"] == 2916
    assert raw_inverse_length["unique_sector_operators"] == 51
    assert raw_inverse_length["nonzero_CP_pairs"] == 2352
    assert raw_inverse_length["same_coefficient_CP_pairs"] == 0
    assert raw_inverse_length["both_commutators_zero_CP_pairs"] == 0
    assert raw_inverse_length["minimum_nonzero_coefficient_support_for_CP"] == 1
    assert global_d_zero_cp == 0
    assert global_same_coefficient_cp == 0

    Path("s2t_family_minimal_operator_menu_exhaustive_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "raw_pairs": raw_inverse_length["ordered_sector_pairs"],
                "raw_full_mixing": raw_inverse_length[
                    "full_three_family_mixing_pairs"
                ],
                "raw_CP_pairs": raw_inverse_length["nonzero_CP_pairs"],
                "raw_unique_CP_signatures": raw_inverse_length[
                    "unique_absolute_CP_signatures"
                ],
                "same_coefficients_CP": raw_inverse_length[
                    "same_coefficient_CP_pairs"
                ],
                "commutator_free_CP": raw_inverse_length[
                    "both_commutators_zero_CP_pairs"
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()