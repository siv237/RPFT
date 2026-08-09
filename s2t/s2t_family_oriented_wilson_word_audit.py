#!/usr/bin/env python3
import itertools
import json
import math
from pathlib import Path

import numpy as np

from s2t_continuous_wilson_gap_action_audit import rodrigues
from s2t_shared_holonomy_two_sector_audit import (
    affine_permutation,
    permutation_matrix,
    restrict,
    triplet_basis,
)


def reduced_words(maximum_length):
    words = []
    for length in range(1, maximum_length + 1):
        for letters in itertools.product("QRr", repeat=length):
            if any(
                (left == right == "Q")
                or (left, right) in {("R", "r"), ("r", "R")}
                for left, right in zip(letters, letters[1:])
            ):
                continue
            words.append("".join(letters))
    return words


def evaluate_word(word, proper_shear, rotation):
    generators = {"Q": proper_shear, "R": rotation, "r": rotation.T}
    result = np.eye(3)
    for letter in word:
        result = result @ generators[letter]
    return result


def principal_so3_generator(rotation):
    cosine = float(np.clip((np.trace(rotation) - 1.0) / 2.0, -1.0, 1.0))
    angle = math.acos(cosine)
    if angle < 1e-10:
        return np.zeros((3, 3), dtype=complex), angle, False
    if abs(math.pi - angle) < 1e-7:
        return None, angle, True
    logarithm = angle * (rotation - rotation.T) / (2.0 * math.sin(angle))
    return -1j * logarithm, angle, False


def diagonalizer(matrix, direct_yukawa=False):
    hermitian = matrix @ matrix.T if direct_yukawa else matrix
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    minimum_gap = float(np.min(np.abs(np.diff(eigenvalues))))
    return eigenvectors, minimum_gap


def jarlskog(matrix):
    return float(
        np.imag(
            matrix[0, 0]
            * matrix[1, 1]
            * np.conj(matrix[0, 1])
            * np.conj(matrix[1, 0])
        )
    )


def scan_pairs(candidates, factor_operator, reading, normalization="raw"):
    matrices = []
    for candidate in candidates:
        if reading == "direct_real":
            matrix = factor_operator + candidate["unitary"]
            direct = True
        elif reading == "cosine":
            matrix = factor_operator + (
                candidate["unitary"] + candidate["unitary"].T
            ) / 2.0
            direct = False
        elif reading == "principal_log":
            if candidate["branch_ambiguous"]:
                continue
            generator = candidate["generator"].copy()
            if normalization == "spectral":
                norm = np.linalg.norm(generator, 2)
                generator = generator / norm if norm > 1e-14 else generator
            elif normalization == "per_edge":
                generator = generator / len(candidate["word"])
            elif normalization != "raw":
                raise ValueError(normalization)
            matrix = factor_operator + generator
            direct = False
        else:
            raise ValueError(reading)

        eigenvectors, gap = diagonalizer(matrix, direct_yukawa=direct)
        if gap > 1e-8:
            matrices.append({**candidate, "eigenvectors": eigenvectors})

    full_mixing = 0
    nonzero_cp = 0
    unique_cp_signatures = set()
    minimum_total_word_length = None
    same_word_cp = 0
    maximum_abs_j = 0.0

    for upper in matrices:
        for lower in matrices:
            mixing = upper["eigenvectors"].conj().T @ lower["eigenvectors"]
            full = bool(np.all(np.abs(mixing) > 1e-7))
            abs_j = abs(jarlskog(mixing))
            cp = full and abs_j > 1e-9
            full_mixing += int(full)
            nonzero_cp += int(cp)
            same_word_cp += int(cp and upper["word"] == lower["word"])
            if cp:
                total_length = len(upper["word"]) + len(lower["word"])
                minimum_total_word_length = (
                    total_length
                    if minimum_total_word_length is None
                    else min(minimum_total_word_length, total_length)
                )
                maximum_abs_j = max(maximum_abs_j, abs_j)
                signature = tuple(np.round(np.abs(mixing).ravel(), 6)) + (
                    round(abs_j, 8),
                )
                unique_cp_signatures.add(signature)

    return {
        "sector_operators": len(matrices),
        "ordered_pairs": len(matrices) ** 2,
        "full_mixing_pairs": full_mixing,
        "nonzero_CP_pairs": nonzero_cp,
        "unique_absolute_CP_signatures": len(unique_cp_signatures),
        "minimum_total_word_length_for_CP": minimum_total_word_length,
        "same_word_CP_pairs": same_word_cp,
        "maximum_abs_J": maximum_abs_j,
    }


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
    proper_shear = -restricted_shear

    target_cosine = (26.0 - 9.0 * math.sqrt(15.0)) / 11.0
    target_sine = math.sqrt(1.0 - target_cosine**2)
    rotations = [
        rodrigues(axis, target_cosine, target_sine) for axis in axes
    ]
    factor_operator = (1.0 / math.pi) * (np.eye(3) - restricted_x) + (
        1.0 / (2.0 * math.pi)
    ) * (np.eye(3) - restricted_y)

    cumulative_rows = []
    candidates_by_length = {}
    for maximum_length in range(1, 6):
        candidates = []
        for axis_index, rotation in enumerate(rotations):
            for word in reduced_words(maximum_length):
                unitary = evaluate_word(word, proper_shear, rotation)
                generator, angle, branch_ambiguous = principal_so3_generator(unitary)
                candidates.append(
                    {
                        "axis": axis_index,
                        "word": word,
                        "unitary": unitary,
                        "generator": generator,
                        "angle": angle,
                        "branch_ambiguous": branch_ambiguous,
                    }
                )
        candidates_by_length[maximum_length] = candidates

        real_result = scan_pairs(candidates, factor_operator, "direct_real")
        cosine_result = scan_pairs(candidates, factor_operator, "cosine")
        log_result = scan_pairs(
            candidates, factor_operator, "principal_log", normalization="raw"
        )
        cumulative_rows.append(
            {
                "maximum_word_length": maximum_length,
                "formal_axis_words": len(candidates),
                "branch_ambiguous_words": sum(
                    candidate["branch_ambiguous"] for candidate in candidates
                ),
                "direct_real_readout": real_result,
                "cosine_readout": cosine_result,
                "principal_log_readout": log_result,
            }
        )

    normalization_rows = []
    length_four_candidates = candidates_by_length[4]
    for normalization in ["raw", "spectral", "per_edge"]:
        normalization_rows.append(
            {
                "normalization": normalization,
                **scan_pairs(
                    length_four_candidates,
                    factor_operator,
                    "principal_log",
                    normalization=normalization,
                ),
            }
        )

    length_two = next(
        row for row in cumulative_rows if row["maximum_word_length"] == 2
    )
    length_four = next(
        row for row in cumulative_rows if row["maximum_word_length"] == 4
    )

    results = {
        "status": "path_ordering_creates_CP_only_through_a_multivalued_log_readout_and_does_not_select_a_unique_word",
        "date": "2026-08-06",
        "blind_protocol": {
            "observed_CKM_or_masses_loaded": False,
            "alphabet": {
                "Q": "properized shear rotation -S",
                "R": "Wilson rotation R_n(theta_star)",
                "r": "inverse Wilson rotation R_n(theta_star)^(-1)",
            },
            "word_reduction": "QQ, Rr and rR immediate cancellations removed",
            "maximum_lengths": [1, 2, 3, 4, 5],
        },
        "geometric_gate": {
            "fundamental_group": "pi1(RP3 times S1)=Z2 times Z is abelian",
            "consequence": (
                "Noncommuting Q and R cannot be two flat fundamental-loop holonomies. The "
                "word construction requires a new non-flat connection, an edge graph or a "
                "defect with specified path ordering."
            ),
            "path_graph_declared": False,
        },
        "readout_gate": {
            "direct_real": (
                "Y=L+U is real; diagonalizing YY^T gives an orthogonal mixing matrix and CP=0."
            ),
            "cosine": (
                "M=L+(U+U^T)/2 is real symmetric and gives CP=0."
            ),
            "principal_log": (
                "M=L-i Log(U) is Hermitian and can give CP, but requires a branch of the "
                "matrix logarithm and a normalization relative to L."
            ),
        },
        "cumulative_scan": cumulative_rows,
        "normalization_scan_at_length_four": normalization_rows,
        "shortest_CP_gate": {
            "maximum_length_one_CP_pairs": cumulative_rows[0][
                "principal_log_readout"
            ]["nonzero_CP_pairs"],
            "maximum_length_two_CP_pairs": length_two["principal_log_readout"][
                "nonzero_CP_pairs"
            ],
            "minimum_total_word_length": length_two["principal_log_readout"][
                "minimum_total_word_length_for_CP"
            ],
            "finding": (
                "CP first appears for a pair with total word length three, for example a "
                "one-edge R sector against a two-edge QR sector."
            ),
        },
        "selector_gate": {
            "length_two_unique_CP_signatures": length_two[
                "principal_log_readout"
            ]["unique_absolute_CP_signatures"],
            "length_four_unique_CP_signatures": length_four[
                "principal_log_readout"
            ]["unique_absolute_CP_signatures"],
            "growth": "40 at length <=2, 252 at <=3, 1598 at <=4, 7080 at <=5",
            "finding": (
                "Increasing the allowed path length rapidly increases, rather than reduces, "
                "the number of blind CP candidates. No intrinsic shortest-word selector is present."
            ),
        },
        "branch_and_orientation_gate": {
            "pi_rotation_issue": (
                "Words with eigenangle pi have a non-unique principal generator axis and were "
                "excluded from the logarithmic scan."
            ),
            "inverse_word": (
                "Reversing orientation sends the generator approximately to its negative and "
                "produces CP-conjugate choices unless an oriented parent structure is declared."
            ),
            "properization": (
                "The reflection S was replaced by the proper rotation Q=-S; this signed "
                "representation choice must itself follow from the boundary theory."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "Path ordering can generate a fixed noncommutative complex operator without "
                "introducing continuous coefficients, and CP appears already at total path "
                "length three in the logarithmic readout."
            ),
            "negative": (
                "Real readouts give CP=0, while the logarithmic readout introduces branch, "
                "normalization, path-graph and orientation choices and yields rapidly growing "
                "candidate multiplicity."
            ),
            "status": "mechanism_exists_but_path_and_readout_selector_fail",
            "next_gate": (
                "Specify a concrete oriented edge complex or non-flat boundary connection that "
                "allows exactly one shortest word per quark sector and fixes the logarithm branch."
            ),
        },
    }

    assert abs(np.linalg.det(proper_shear) - 1.0) < 1e-12
    assert np.linalg.norm(proper_shear @ proper_shear - np.eye(3)) < 1e-12
    assert all(
        row["direct_real_readout"]["nonzero_CP_pairs"] == 0
        and row["cosine_readout"]["nonzero_CP_pairs"] == 0
        for row in cumulative_rows
    )
    assert cumulative_rows[0]["principal_log_readout"]["nonzero_CP_pairs"] == 0
    assert length_two["principal_log_readout"]["nonzero_CP_pairs"] == 160
    assert length_two["principal_log_readout"]["unique_absolute_CP_signatures"] == 40
    assert length_four["principal_log_readout"]["unique_absolute_CP_signatures"] == 1598

    Path("s2t_family_oriented_wilson_word_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "real_readout_CP": 0,
                "cosine_readout_CP": 0,
                "length_two_log_CP_pairs": length_two[
                    "principal_log_readout"
                ]["nonzero_CP_pairs"],
                "length_four_log_unique_CP": length_four[
                    "principal_log_readout"
                ]["unique_absolute_CP_signatures"],
                "minimum_total_word_length_for_CP": length_two[
                    "principal_log_readout"
                ]["minimum_total_word_length_for_CP"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()