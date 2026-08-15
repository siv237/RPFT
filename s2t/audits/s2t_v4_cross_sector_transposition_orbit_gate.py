import itertools
import json

import numpy as np
import sympy as sp


with open(
    "s2t_v4_family_square_spectral_selector_gate_results.json",
    encoding="utf-8",
) as handle:
    square_results = json.load(handle)

with open(
    "s2t_v4_rank_one_breaking_gate_results.json",
    encoding="utf-8",
) as handle:
    rank_one_results = json.load(handle)


points = [(0, 0), (0, 1), (1, 0), (1, 1)]
point_index = {point: index for index, point in enumerate(points)}
triplet_basis = sp.Matrix.hstack(
    sp.Matrix([1, 1, -1, -1]) / 2,
    sp.Matrix([1, -1, 1, -1]) / 2,
    sp.Matrix([1, -1, -1, 1]) / 2,
)


def affine_permutation(matrix, shift):
    return tuple(
        point_index[
            (
                (
                    matrix[0][0] * point[0]
                    + matrix[0][1] * point[1]
                    + shift[0]
                )
                % 2,
                (
                    matrix[1][0] * point[0]
                    + matrix[1][1] * point[1]
                    + shift[1]
                )
                % 2,
            )
        ]
        for point in points
    )


def compose(first, second):
    return tuple(first[second[index]] for index in range(4))


def generated_group(generators):
    identity = tuple(range(4))
    group = {identity}
    frontier = [identity]
    while frontier:
        element = frontier.pop()
        for generator in generators:
            for product in (
                compose(element, generator),
                compose(generator, element),
            ):
                if product not in group:
                    group.add(product)
                    frontier.append(product)
    return group


def permutation_matrix(permutation):
    matrix = sp.zeros(4)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1
    return matrix


def restrict(matrix):
    return sp.simplify(triplet_basis.T * matrix * triplet_basis)


operators = [
    restrict(permutation_matrix(row["permutations"][0]))
    for row in square_results["selected_operators"]
]

shear_permutation = tuple(rank_one_results["shear_permutation"])
shear = restrict(permutation_matrix(shear_permutation))
rank_one_projector = (sp.eye(3) - shear) / 2

identity2 = ((1, 0), (0, 1))
shear2 = ((1, 0), (1, 1))
translation_p = affine_permutation(identity2, (1, 0))
translation_q = affine_permutation(identity2, (0, 1))
residual_group = generated_group(
    [translation_p, translation_q, shear_permutation]
)
projector_stabilizer = [
    element
    for element in residual_group
    if sp.simplify(
        restrict(permutation_matrix(element))
        * rank_one_projector
        * restrict(permutation_matrix(element)).T
        - rank_one_projector
    )
    == sp.zeros(3)
]

operator_actions = []
for element in projector_stabilizer:
    unitary = restrict(permutation_matrix(element))
    action = []
    for operator in operators:
        transformed = sp.simplify(unitary * operator * unitary.T)
        action.append(
            next(
                index
                for index, candidate in enumerate(operators)
                if transformed == candidate
            )
        )
    operator_actions.append(action)

remaining_pairs = set(itertools.permutations(range(len(operators)), 2))
pair_orbits = []
while remaining_pairs:
    seed = next(iter(remaining_pairs))
    orbit = {
        (action[seed[0]], action[seed[1]])
        for action in operator_actions
    }
    pair_orbits.append(sorted(orbit))
    remaining_pairs -= orbit


def pair_invariants(first, second):
    operator_u = operators[first]
    operator_d = operators[second]
    commutator = operator_u * operator_d - operator_d * operator_u
    cross_word = sp.simplify(
        sp.trace(rank_one_projector * operator_u * operator_d)
    )
    return {
        "trace_Hu_Hd": str(sp.trace(operator_u * operator_d)),
        "commutator_norm_squared": str(
            sp.trace(commutator.T * commutator)
        ),
        "cross_word_Tr_P_Hu_Hd": str(cross_word),
        "commuting": commutator == sp.zeros(3),
    }


def minimal_readout(first, second):
    operator_u = operators[first]
    operator_d = operators[second]
    yukawa_u = rank_one_projector + sp.I * operator_u
    yukawa_d = rank_one_projector + sp.I * operator_d
    mass_u = sp.simplify(yukawa_u * yukawa_u.conjugate().T)
    mass_d = sp.simplify(yukawa_d * yukawa_d.conjugate().T)
    commutator = sp.simplify(mass_u * mass_d - mass_d * mass_u)
    cp_trace = sp.simplify(sp.trace(commutator**3))

    eigenvalues_u, eigenvectors_u = np.linalg.eigh(
        np.array(mass_u, dtype=complex)
    )
    eigenvalues_d, eigenvectors_d = np.linalg.eigh(
        np.array(mass_d, dtype=complex)
    )
    mixing = np.abs(eigenvectors_u.conj().T @ eigenvectors_d)
    return {
        "mass_squared_eigenvalues_u": [
            round(float(value), 12) for value in eigenvalues_u
        ],
        "mass_squared_eigenvalues_d": [
            round(float(value), 12) for value in eigenvalues_d
        ],
        "absolute_mixing_matrix": [
            [round(float(value), 12) for value in row]
            for row in mixing
        ],
        "maximum_off_diagonal_entry": max(
            mixing[row, column]
            for row in range(3)
            for column in range(3)
            if row != column
        ),
        "cp_trace_commutator_cube": str(cp_trace),
        "physical_cp_nonzero": cp_trace != 0,
    }


orbit_rows = []
for orbit in pair_orbits:
    representative = orbit[0]
    invariants = pair_invariants(*representative)
    orbit_rows.append(
        {
            "ordered_pairs": [list(pair) for pair in orbit],
            "orbit_size": len(orbit),
            "representative": list(representative),
            "invariants": invariants,
            "minimal_readout": minimal_readout(*representative),
        }
    )

orbit_rows.sort(
    key=lambda row: sp.Rational(
        row["invariants"]["cross_word_Tr_P_Hu_Hd"]
    )
)

result = {
    "gate": "version4_cross_sector_transposition_orbit",
    "selected_single_sector_operator_count": len(operators),
    "projector_stabilizer_order": len(projector_stabilizer),
    "ordered_distinct_pair_count": len(operators) * (len(operators) - 1),
    "relative_pair_orbit_count": len(orbit_rows),
    "all_pair_orbits_have_size_four": all(
        row["orbit_size"] == 4 for row in orbit_rows
    ),
    "cross_word_values": [
        row["invariants"]["cross_word_Tr_P_Hu_Hd"]
        for row in orbit_rows
    ],
    "cross_word_distinguishes_all_relative_orbits": len(
        {
            row["invariants"]["cross_word_Tr_P_Hu_Hd"]
            for row in orbit_rows
        }
    )
    == len(orbit_rows),
    "separate_square_action_contains_cross_word": False,
    "linear_cross_word_selector_requires_new_coefficient": True,
    "all_minimal_readout_cp_invariants_vanish": all(
        not row["minimal_readout"]["physical_cp_nonzero"]
        for row in orbit_rows
    ),
    "minimum_class_maximum_off_diagonal_entry": min(
        row["minimal_readout"]["maximum_off_diagonal_entry"]
        for row in orbit_rows
    ),
    "relative_orbits": orbit_rows,
    "status": "one cross word classifies the three physical relative transposition orbits, but its coefficient is absent from the separate square action and the unit-amplitude readout remains CP-zero with large mixing",
}

with open(
    "s2t_v4_cross_sector_transposition_orbit_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))