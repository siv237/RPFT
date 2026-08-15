import itertools
import json
from collections import Counter

import sympy as sp


points = [(0, 0), (0, 1), (1, 0), (1, 1)]
point_index = {point: index for index, point in enumerate(points)}


def det_mod2(matrix):
    return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 2


def affine_permutation(matrix, shift):
    return tuple(
        point_index[
            (
                (matrix[0][0] * point[0] + matrix[0][1] * point[1] + shift[0]) % 2,
                (matrix[1][0] * point[0] + matrix[1][1] * point[1] + shift[1]) % 2,
            )
        ]
        for point in points
    )


def compose(first, second):
    return tuple(first[second[index]] for index in range(4))


def inverse(permutation):
    result = [0] * 4
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def generated_group(generators):
    identity = tuple(range(4))
    group = {identity}
    frontier = [identity]
    while frontier:
        element = frontier.pop()
        for generator in generators:
            for product in (compose(element, generator), compose(generator, element)):
                if product not in group:
                    group.add(product)
                    frontier.append(product)
    return group


def permutation_matrix(permutation):
    matrix = sp.zeros(4)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1
    return matrix


def cycle_type(permutation):
    seen = set()
    lengths = []
    for start in range(4):
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


triplet_basis = sp.Matrix.hstack(
    sp.Matrix([1, 1, -1, -1]) / 2,
    sp.Matrix([1, -1, 1, -1]) / 2,
    sp.Matrix([1, -1, -1, 1]) / 2,
)


def restrict(matrix):
    return sp.simplify(triplet_basis.T * matrix * triplet_basis)


def algebra_dimension(generators):
    basis = []

    def add(matrix):
        vectors = [sp.Matrix(item).reshape(9, 1) for item in basis]
        old_rank = sp.Matrix.hstack(*vectors).rank() if vectors else 0
        new_rank = sp.Matrix.hstack(*(vectors + [sp.Matrix(matrix).reshape(9, 1)])).rank()
        if new_rank > old_rank:
            basis.append(matrix)
            return True
        return False

    add(sp.eye(3))
    for generator in generators:
        add(generator)
    changed = True
    while changed:
        changed = False
        for matrix in list(basis):
            for generator in generators:
                changed = add(sp.simplify(matrix * generator)) or changed
    return len(basis)


def commutant_dimension(generators):
    variables = sp.symbols("x0:9")
    X = sp.Matrix(3, 3, variables)
    equations = []
    for generator in generators:
        equations.extend(list(X * generator - generator * X))
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    return 9 - coefficient_matrix.rank()


identity2 = ((1, 0), (0, 1))
shear2 = ((1, 0), (1, 1))
translation_p = affine_permutation(identity2, (1, 0))
translation_q = affine_permutation(identity2, (0, 1))
shear = affine_permutation(shear2, (0, 0))
residual_group = generated_group([translation_p, translation_q, shear])

affine_group = {
    affine_permutation(matrix, shift)
    for entries in itertools.product(range(2), repeat=4)
    for matrix in [((entries[0], entries[1]), (entries[2], entries[3]))]
    if det_mod2(matrix) == 1
    for shift in points
}

base_generators = [restrict(permutation_matrix(item)) for item in (translation_p, translation_q, shear)]
outside = sorted(affine_group - residual_group)

rows = []
for candidate in outside:
    P = permutation_matrix(candidate)
    incidence = (P + P.T) / 2
    candidate_generators = base_generators + [restrict(incidence)]
    orbit_average = sum(
        (
            permutation_matrix(group_element)
            * incidence
            * permutation_matrix(group_element).T
            for group_element in residual_group
        ),
        sp.zeros(4),
    ) / len(residual_group)
    averaged_generators = base_generators + [restrict(orbit_average)]
    rows.append(
        {
            "permutation": list(candidate),
            "cycle_type": cycle_type(candidate),
            "generated_group_order": len(generated_group([translation_p, translation_q, shear, candidate])),
            "operator_algebra_dimension": algebra_dimension(candidate_generators),
            "operator_commutant_dimension": commutant_dimension(candidate_generators),
            "averaged_algebra_dimension": algebra_dimension(averaged_generators),
            "averaged_commutant_dimension": commutant_dimension(averaged_generators),
        }
    )

successful = [row for row in rows if row["operator_algebra_dimension"] == 9]
failed = [row for row in rows if row["operator_algebra_dimension"] != 9]

remaining = set(outside)
orbits = []
while remaining:
    seed = next(iter(remaining))
    orbit = {
        compose(compose(group_element, seed), inverse(group_element))
        for group_element in residual_group
    } & set(outside)
    orbits.append(
        {
            "size": len(orbit),
            "cycle_types": dict(Counter(cycle_type(item) for item in orbit)),
        }
    )
    remaining -= orbit

result = {
    "gate": "version4_incidence_operator_menu",
    "affine_group_order": len(affine_group),
    "residual_group_order": len(residual_group),
    "residual_triplet_algebra_dimension": algebra_dimension(base_generators),
    "residual_triplet_commutant_dimension": commutant_dimension(base_generators),
    "outside_candidate_count": len(outside),
    "successful_full_M3_count": len(successful),
    "failed_reducible_count": len(failed),
    "cycle_type_counts": dict(Counter(row["cycle_type"] for row in rows)),
    "successful_cycle_type_counts": dict(Counter(row["cycle_type"] for row in successful)),
    "failed_cycle_type_counts": dict(Counter(row["cycle_type"] for row in failed)),
    "residual_conjugacy_orbits": orbits,
    "all_successful_generate_S4": all(row["generated_group_order"] == 24 for row in successful),
    "all_orbit_averages_restore_reducible_algebra": all(row["averaged_algebra_dimension"] == 5 for row in rows),
    "rows": rows,
    "selector_exists": False,
    "selector_obstruction": "twelve Hermitian incidence directions generate M3, but the frozen geometry selects neither an orbit element nor its sector assignment",
}

with open("s2t_v4_incidence_operator_menu_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))