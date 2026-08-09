#!/usr/bin/env python3
import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np


POINTS = [(0, 0), (1, 0), (0, 1), (1, 1)]
POINT_INDEX = {point: index for index, point in enumerate(POINTS)}


def compose(first, second):
    return tuple(first[second[index]] for index in range(len(first)))


def inverse(permutation):
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def generated_group(generators):
    identity = tuple(range(len(generators[0])))
    group = {identity}
    frontier = [identity]
    while frontier:
        element = frontier.pop()
        for generator in generators:
            for product in [compose(element, generator), compose(generator, element)]:
                if product not in group:
                    group.add(product)
                    frontier.append(product)
    return sorted(group)


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


def triplet_basis():
    uniform = np.ones(4) / 2.0
    projector = np.eye(4) - np.outer(uniform, uniform)
    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    return eigenvectors[:, eigenvalues > 0.5]


def restrict(matrix, basis):
    return basis.T @ matrix @ basis


def algebra_dimension(generators):
    dimension = generators[0].shape[0]
    basis = []

    def add(matrix):
        old_dimension = len(basis)
        trial = basis + [matrix]
        rank = np.linalg.matrix_rank(
            np.stack([item.reshape(-1) for item in trial]), tol=1e-10
        )
        if rank > old_dimension:
            basis.append(matrix)
            return True
        return False

    add(np.eye(dimension))
    for generator in generators:
        add(generator)
    changed = True
    while changed:
        changed = False
        old_basis = list(basis)
        for matrix in old_basis:
            for generator in generators:
                changed = add(matrix @ generator) or changed
    return len(basis)


def commutant_dimension(generators):
    dimension = generators[0].shape[0]
    equations = [
        np.kron(generator.T, np.eye(dimension))
        - np.kron(np.eye(dimension), generator)
        for generator in generators
    ]
    rank = np.linalg.matrix_rank(np.vstack(equations), tol=1e-10)
    return int(dimension * dimension - rank)


def cycle_type(permutation):
    seen = set()
    lengths = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return "+".join(map(str, sorted(lengths, reverse=True)))


def conjugacy_orbits(elements, acting_group):
    remaining = set(elements)
    orbits = []
    while remaining:
        seed = next(iter(remaining))
        orbit = {
            compose(compose(group_element, seed), inverse(group_element))
            for group_element in acting_group
        }
        orbit &= set(elements)
        orbits.append(sorted(orbit))
        remaining -= orbit
    return orbits


def main():
    identity2 = np.eye(2, dtype=int)
    shear2 = np.array([[1, 0], [1, 1]], dtype=int)
    translation_x = affine_permutation(identity2, (1, 0))
    translation_y = affine_permutation(identity2, (0, 1))
    shear = affine_permutation(shear2, (0, 0))
    current_group = generated_group([translation_x, translation_y, shear])

    affine_group = sorted(
        {
            affine_permutation(matrix, translation)
            for matrix in invertible_matrices_f2()
            for translation in POINTS
        }
    )
    outside = [element for element in affine_group if element not in current_group]
    basis = triplet_basis()
    current_hermitian = [
        restrict(permutation_matrix(element), basis)
        for element in [translation_x, translation_y, shear]
    ]

    candidate_rows = []
    for candidate in outside:
        candidate_matrix = permutation_matrix(candidate)
        hermitian_incidence = 0.5 * (candidate_matrix + candidate_matrix.T)
        restricted_candidate = restrict(hermitian_incidence, basis)
        generators = current_hermitian + [restricted_candidate]
        orbit_average = sum(
            permutation_matrix(group_element)
            @ hermitian_incidence
            @ permutation_matrix(group_element).T
            for group_element in current_group
        ) / len(current_group)
        averaged_generators = current_hermitian + [restrict(orbit_average, basis)]
        candidate_rows.append(
            {
                "permutation": list(candidate),
                "cycle_type": cycle_type(candidate),
                "generated_group_order": len(
                    generated_group([translation_x, translation_y, shear, candidate])
                ),
                "operator_algebra_dimension": algebra_dimension(generators),
                "operator_commutant_dimension": commutant_dimension(generators),
                "averaged_algebra_dimension": algebra_dimension(averaged_generators),
                "averaged_commutant_dimension": commutant_dimension(
                    averaged_generators
                ),
            }
        )

    full_m3_candidates = [
        row for row in candidate_rows if row["operator_algebra_dimension"] == 9
    ]
    orbits = conjugacy_orbits(outside, current_group)
    orbit_summary = [
        {
            "size": len(orbit),
            "cycle_types": dict(Counter(cycle_type(item) for item in orbit)),
        }
        for orbit in orbits
    ]

    results = {
        "status": "one_extra_affine_incidence_can_generate_full_M3_but_geometry_does_not_select_it_and_symmetry_average_removes_the_gain",
        "date": "2026-08-05",
        "groups": {
            "current_translation_shear_group_order": len(current_group),
            "full_affine_group_order": len(affine_group),
            "outside_candidate_count": len(outside),
            "outside_D8_conjugacy_orbits": orbit_summary,
        },
        "current_family_algebra": {
            "dimension": algebra_dimension(current_hermitian),
            "commutant_dimension": commutant_dimension(current_hermitian),
            "interpretation": "the current D8-type geometry leaves a reducible 1+2 family algebra",
        },
        "single_extra_operator_scan": {
            "candidate_count": len(candidate_rows),
            "full_M3_candidate_count": len(full_m3_candidates),
            "cycle_type_counts": dict(Counter(row["cycle_type"] for row in candidate_rows)),
            "rows": candidate_rows,
            "finding": (
                "Every affine permutation outside the current D8 subgroup enlarges the generated "
                "permutation group to S4. Its Hermitian incidence part is sufficient to make the "
                "triplet operator algebra irreducible and, in the successful cases, equal to M3."
            ),
        },
        "selector_gate": {
            "geometric_selector_exists": False,
            "reason": (
                "The RP3 and S1 factors are inequivalent, so the missing affine transformations "
                "are abstract relabelings rather than diffeomorphism-induced symmetries. The "
                "current D8 action partitions the candidates into multiple nontrivial orbits."
            ),
            "symmetry_averaging_result": (
                "Averaging any candidate over the current geometric group returns it to the "
                "D8 commutant and restores the reducible 1+2 algebra."
            ),
        },
        "action_gate": {
            "fixed_coefficient_from_incidence": "an unweighted chosen edge can be normalized to one",
            "remaining_choices": [
                "which outside affine incidence operator is physical",
                "its relative coefficient against the existing factor Laplacian",
                "which SU5 Yukawa sector receives which incidence combination",
            ],
            "consequence": (
                "Full mixing algebra is easy once one explicitly breaks the current geometry, "
                "but the parent action does not choose the breaking direction or sector map."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "There is no algebraic obstruction to a three-dimensional full mixing algebra: "
                "one extra affine incidence operator can supply it."
            ),
            "no_go": (
                "Within the declared carrier geometry the required operator is unselected. "
                "Restoring symmetry removes it, while choosing it by CKM data is forbidden."
            ),
            "next_condition": (
                "A successful 1+3 rescue must derive one specific outside-D8 incidence direction "
                "from new prior geometry, a boundary condition or a discrete Dirac complex."
            ),
        },
    }

    assert len(current_group) == 8
    assert len(affine_group) == 24
    assert len(outside) == 16
    assert algebra_dimension(current_hermitian) == 5
    assert commutant_dimension(current_hermitian) == 2
    assert all(row["generated_group_order"] == 24 for row in candidate_rows)
    assert len(full_m3_candidates) > 0
    assert all(row["averaged_commutant_dimension"] >= 2 for row in candidate_rows)

    Path("s2t_family_affine_incidence_exhaustive_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "outside_candidates": len(outside),
                "full_M3_candidates": len(full_m3_candidates),
                "D8_conjugacy_orbits": orbit_summary,
                "current_algebra_dimension": algebra_dimension(current_hermitian),
                "current_commutant_dimension": commutant_dimension(current_hermitian),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()