#!/usr/bin/env python3
import itertools
import json
from pathlib import Path

import numpy as np


POINTS = [(0, 0), (1, 0), (0, 1), (1, 1)]
POINT_INDEX = {point: index for index, point in enumerate(POINTS)}


def permutation_matrix(permutation):
    matrix = np.zeros((4, 4), dtype=float)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def invertible_matrices_f2():
    matrices = []
    for entries in itertools.product([0, 1], repeat=4):
        matrix = np.array(entries, dtype=int).reshape(2, 2)
        if int(round(np.linalg.det(matrix))) % 2 == 1:
            matrices.append(matrix)
    return matrices


def affine_permutation(matrix, translation):
    permutation = []
    for point in POINTS:
        image = (
            int((matrix[0, 0] * point[0] + matrix[0, 1] * point[1] + translation[0]) % 2),
            int((matrix[1, 0] * point[0] + matrix[1, 1] * point[1] + translation[1]) % 2),
        )
        permutation.append(POINT_INDEX[image])
    return tuple(permutation)


def commutant_dimension(representations):
    dimension = representations[0].shape[0]
    equations = [
        np.kron(rep.T, np.eye(dimension)) - np.kron(np.eye(dimension), rep)
        for rep in representations
    ]
    rank = np.linalg.matrix_rank(np.vstack(equations), tol=1e-10)
    return int(dimension * dimension - rank)


def restrict_to_triplet(matrix):
    basis = np.array(
        [
            [1, -1, 0, 0],
            [1, 1, -2, 0],
            [1, 1, 1, -3],
        ],
        dtype=float,
    ).T
    q, _ = np.linalg.qr(basis)
    return q.T @ matrix @ q


def main():
    identity2 = np.eye(2, dtype=int)
    shear2 = np.array([[1, 0], [1, 1]], dtype=int)
    affine_group = sorted(
        {
            affine_permutation(matrix, translation)
            for matrix in invertible_matrices_f2()
            for translation in POINTS
        }
    )
    affine4 = [permutation_matrix(permutation) for permutation in affine_group]
    affine3 = [restrict_to_triplet(matrix) for matrix in affine4]

    translation_permutations = [
        affine_permutation(identity2, translation) for translation in POINTS
    ]
    translations4 = [permutation_matrix(p) for p in translation_permutations]
    translations3 = [restrict_to_triplet(matrix) for matrix in translations4]

    shear4 = permutation_matrix(affine_permutation(shear2, (0, 0)))
    shear3 = restrict_to_triplet(shear4)
    residual_group4 = []
    for translation in translations4:
        for power in [np.eye(4), shear4]:
            candidate = translation @ power
            if not any(np.allclose(candidate, old) for old in residual_group4):
                residual_group4.append(candidate)
    residual_group3 = [restrict_to_triplet(matrix) for matrix in residual_group4]

    # A basis-independent canonical noncommuting candidate from two already
    # declared geometric operators.
    translation_rp3_3 = translations3[POINTS.index((1, 0))]
    commutator = 0.5j * (
        translation_rp3_3 @ shear3 - shear3 @ translation_rp3_3
    )
    translation_average = sum(
        rep @ commutator @ rep.conj().T for rep in translations3
    ) / len(translations3)
    affine_average = sum(
        rep @ commutator @ rep.conj().T for rep in affine3
    ) / len(affine3)

    support = np.argwhere(np.abs(commutator) > 1e-10).tolist()
    isolated_index = sorted(
        set(range(3)) - {index for pair in support for index in pair}
    )

    # The SU5 holonomy is a spurion rather than an SU5-invariant tensor.
    parity5 = np.diag([1.0, 1.0, 1.0, -1.0, -1.0])
    broken_generator = np.zeros((5, 5))
    broken_generator[0, 3] = broken_generator[3, 0] = 1.0
    parity_commutator_norm = float(
        np.linalg.norm(parity5 @ broken_generator - broken_generator @ parity5)
    )

    # Schur counting for the physical family triplet tensored with the two
    # inequivalent SU5 matter irreps 10 and bar5.
    exact_parent_action_coefficients = 2
    exact_parent_relative_coefficients = exact_parent_action_coefficients - 1
    exact_yukawa_family_tensors = {
        "10_10_5H": "one AGL-invariant family bilinear times an independent up-type coupling",
        "10_bar5_bar5H": "one AGL-invariant family bilinear times an independent down-type coupling",
    }

    results = {
        "status": "canonical_commutator_exists_but_is_symmetry_odd_and_does_not_close_family_mixing",
        "date": "2026-08-05",
        "menu_symmetry": {
            "AGL_order": len(affine3),
            "AGL_triplet_commutant_dimension": commutant_dimension(affine3),
            "translation_group_order": len(translations3),
            "translation_triplet_commutant_dimension": commutant_dimension(translations3),
            "translation_plus_shear_order": len(residual_group3),
            "translation_plus_shear_commutant_dimension": commutant_dimension(
                residual_group3
            ),
            "consequence": (
                "Full affine invariance allows only a scalar on the family triplet. "
                "Translation invariance allows diagonal splitting but no mixing."
            ),
        },
        "canonical_noncommuting_candidate": {
            "definition": "K=(i/2)[T_RP3,S_shear]",
            "hermiticity_error": float(
                np.linalg.norm(commutator - commutator.conj().T)
            ),
            "eigenvalues": np.linalg.eigvalsh(commutator).tolist(),
            "rank": int(np.linalg.matrix_rank(commutator, tol=1e-10)),
            "nonzero_support": support,
            "isolated_family_direction": isolated_index,
            "translation_orbit_average_norm": float(
                np.linalg.norm(translation_average)
            ),
            "full_affine_orbit_average_norm": float(np.linalg.norm(affine_average)),
            "finding": (
                "K is a normalized Hermitian generator with no fitted coefficient, but it is "
                "odd under the unbroken translation symmetry. Symmetry averaging kills it exactly."
            ),
        },
        "SU5_controlled_insertion": {
            "candidate": "K tensor P_SU5",
            "P_SU5": "diag(1,1,1,-1,-1)",
            "commutator_with_broken_SU5_generator_norm": parity_commutator_norm,
            "finding": (
                "The controlled insertion is invariant only after SU5 is already reduced to "
                "S(U3 x U2). The holonomy supplies a legal spurion, but symmetry does not fix "
                "the coefficient multiplying K tensor P_SU5."
            ),
        },
        "action_coefficient_count": {
            "physical_SU5xAGL_quadratic_blocks": exact_parent_action_coefficients,
            "relative_coefficients_after_overall_scale": exact_parent_relative_coefficients,
            "reason": "10 and bar5 are inequivalent SU5 irreducible representations",
            "Yukawa_invariants": exact_yukawa_family_tensors,
            "consequence": (
                "The unique normalized trace fixes normalization of each written term; it does "
                "not choose the relative coefficients of distinct invariant action terms."
            ),
        },
        "mixing_gate": {
            "single_K_support": "one two-family plane",
            "single_K_prediction": (
                "After any diagonal factor kernel, one K insertion leaves one family direction "
                "exactly isolated and can generate at most one mixing angle."
            ),
            "full_CKM_requirement": (
                "At least two non-coplanar family-breaking spurions are required for three "
                "nonzero mixing angles and a physical CP phase."
            ),
            "coefficient_problem": (
                "The current parent symmetry neither selects those spurion directions nor fixes "
                "their relative amplitudes."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "A canonical noncommuting operator can be constructed algebraically as a "
                "commutator of existing menu transformations."
            ),
            "no_go": (
                "It is not an invariant consequence of the current parent action: its orbit "
                "average vanishes, its SU5-controlled version carries an independent coupling, "
                "and one insertion cannot produce the full CKM structure."
            ),
            "next_admissible_gate": (
                "Introduce no fitted coefficient. Search instead for an enlarged symmetry or a "
                "discrete Dirac/incidence operator whose square fixes at least two noncommuting "
                "family spurions and their relative normalization."
            ),
        },
    }

    assert len(affine3) == 24
    assert commutant_dimension(affine3) == 1
    assert commutant_dimension(translations3) == 3
    assert len(residual_group3) == 8
    assert commutant_dimension(residual_group3) == 2
    assert results["canonical_noncommuting_candidate"]["hermiticity_error"] < 1e-12
    assert results["canonical_noncommuting_candidate"]["rank"] == 2
    assert np.linalg.norm(translation_average) < 1e-12
    assert np.linalg.norm(affine_average) < 1e-12
    assert parity_commutator_norm > 1.0

    Path("s2t_parent_noncommuting_family_insertion_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "commutants": {
                    "AGL": results["menu_symmetry"]["AGL_triplet_commutant_dimension"],
                    "translations": results["menu_symmetry"]["translation_triplet_commutant_dimension"],
                    "translations_plus_shear": results["menu_symmetry"]["translation_plus_shear_commutant_dimension"],
                },
                "K_rank": results["canonical_noncommuting_candidate"]["rank"],
                "K_translation_average_norm": results["canonical_noncommuting_candidate"]["translation_orbit_average_norm"],
                "relative_action_coefficients": exact_parent_relative_coefficients,
                "single_K_mixing": "one_plane_only",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()