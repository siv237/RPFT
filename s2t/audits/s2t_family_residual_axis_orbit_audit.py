#!/usr/bin/env python3
import itertools
import json
from pathlib import Path

import numpy as np

from s2t_shared_holonomy_two_sector_audit import (
    affine_permutation,
    permutation_matrix,
    restrict,
    triplet_basis,
)


def compose(first, second):
    return tuple(first[second[index]] for index in range(len(first)))


def inverse(permutation):
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def conjugate(group_element, permutation):
    return compose(compose(group_element, permutation), inverse(group_element))


def main():
    continuous = json.loads(
        Path("s2t_continuous_wilson_gap_action_results.json").read_text(
            encoding="utf-8"
        )
    )
    selected_axes = [
        np.array(axis, dtype=float)
        for axis in continuous["factor_axis_selector"]["summary"][
            "inverse_length"
        ]["selected_axes"]
    ]

    identity2 = np.eye(2, dtype=int)
    translation_x = affine_permutation(identity2, (1, 0))
    translation_y = affine_permutation(identity2, (0, 1))
    basis = triplet_basis()
    restricted_x = restrict(permutation_matrix(translation_x), basis)
    restricted_y = restrict(permutation_matrix(translation_y), basis)

    residual_group = []
    for permutation in itertools.permutations(range(4)):
        restricted = restrict(permutation_matrix(permutation), basis)
        if np.allclose(
            restricted @ restricted_x @ restricted.T, restricted_x, atol=1e-12
        ) and np.allclose(
            restricted @ restricted_y @ restricted.T, restricted_y, atol=1e-12
        ):
            residual_group.append(
                {
                    "permutation": permutation,
                    "restricted_matrix": restricted,
                    "restricted_determinant": float(np.linalg.det(restricted)),
                }
            )

    source_transpositions = [(0, 2, 1, 3), (3, 1, 2, 0)]
    source_pairs = [(1, 2), (0, 3)]

    axis_projectors = [np.outer(axis, axis) for axis in selected_axes]
    orbit_maps = []
    for row in residual_group:
        restricted = row["restricted_matrix"]
        image_indices = []
        for projector in axis_projectors:
            image = restricted @ projector @ restricted.T
            matches = [
                index
                for index, target in enumerate(axis_projectors)
                if np.allclose(image, target, atol=1e-12)
            ]
            image_indices.append(matches[0] if matches else None)
        orbit_maps.append(
            {
                "permutation": list(row["permutation"]),
                "restricted_determinant": row["restricted_determinant"],
                "axis_projector_map": image_indices,
            }
        )

    swapping_elements = [
        row for row in orbit_maps if row["axis_projector_map"] == [1, 0]
    ]
    stabilizing_elements = [
        row for row in orbit_maps if row["axis_projector_map"] == [0, 1]
    ]

    conjugation_rows = []
    for row in residual_group:
        permutation = row["permutation"]
        conjugation_rows.append(
            {
                "group_element": list(permutation),
                "transposition_images": [
                    list(conjugate(permutation, source))
                    for source in source_transpositions
                ],
            }
        )

    axis_dot = float(selected_axes[0] @ selected_axes[1])
    projective_orbit_size = 2
    stabilizer_size = len(residual_group) // projective_orbit_size

    results = {
        "status": "two_factor_selected_axes_form_one_exact_residual_symmetry_orbit",
        "date": "2026-08-06",
        "selected_axes": {
            "triplet_coordinates": [axis.tolist() for axis in selected_axes],
            "four_state_pair_directions": [list(pair) for pair in source_pairs],
            "source_transpositions": [list(item) for item in source_transpositions],
            "absolute_inner_product": abs(axis_dot),
            "orthogonal": abs(axis_dot) < 1e-12,
        },
        "residual_factor_symmetry": {
            "definition": (
                "permutations whose triplet action fixes T_RP3 and T_S1 separately"
            ),
            "order": len(residual_group),
            "elements": [list(row["permutation"]) for row in residual_group],
            "is_translation_Klein_four_group": len(residual_group) == 4,
            "factor_exchange_excluded": (
                "RP3 and S1 are inequivalent factors and their weights differ, so only the "
                "pointwise centralizer, not the setwise factor swap, is admissible."
            ),
        },
        "orbit_test": {
            "maps": orbit_maps,
            "swapping_elements": swapping_elements,
            "stabilizing_elements": stabilizing_elements,
            "projective_orbit_size": projective_orbit_size,
            "projective_stabilizer_size": stabilizer_size,
            "same_orbit": bool(swapping_elements),
            "explicit_swap": list(translation_x),
            "conjugation_check": conjugation_rows,
        },
        "selector_consequence": {
            "factor_cost_degeneracy_is_accidental": False,
            "finding": (
                "Every factor operator built from T_RP3 and T_S1 is invariant under the "
                "residual Klein group. The two minima are therefore exact symmetry images, "
                "not two unrelated candidates."
            ),
            "intrinsic_invariant_can_distinguish_axes": False,
            "reason": (
                "Any scalar invariant of the unbroken factor geometry is constant on a group "
                "orbit. Selecting one representative requires spontaneous or explicit breaking."
            ),
        },
        "two_sector_gate": {
            "single_sector_choice": (
                "The apparent 2-to-1 selector problem is solved after quotienting by the "
                "residual symmetry: there is one projective orbit."
            ),
            "remaining_relative_choices": [
                "aligned representatives for up and down sectors",
                "orthogonal representatives for up and down sectors",
            ],
            "relative_invariant": "absolute inner product is respectively 1 or 0",
            "next_test": (
                "Build up/down operators with the same derived coefficients and determine "
                "whether the aligned and crossed orbit classes give a nondegenerate, "
                "parameter-free mixing matrix."
            ),
        },
    }

    assert len(residual_group) == 4
    assert abs(axis_dot) < 1e-12
    assert len(swapping_elements) == 2
    assert len(stabilizing_elements) == 2
    assert any(
        row["permutation"] == list(translation_x) for row in swapping_elements
    )
    assert conjugate(translation_x, source_transpositions[0]) == source_transpositions[1]

    Path("s2t_family_residual_axis_orbit_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "residual_group_order": len(residual_group),
                "axes_orthogonal": results["selected_axes"]["orthogonal"],
                "same_projective_orbit": results["orbit_test"]["same_orbit"],
                "orbit_size": projective_orbit_size,
                "stabilizer_size": stabilizer_size,
                "explicit_swap": list(translation_x),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()