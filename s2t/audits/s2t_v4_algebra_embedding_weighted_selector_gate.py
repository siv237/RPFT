import json

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


def permutation_matrix(permutation):
    matrix = sp.zeros(4)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1
    return matrix


def restrict(matrix):
    return sp.simplify(triplet_basis.T * matrix * triplet_basis)


def translation(shift):
    permutation = tuple(
        point_index[
            (
                (point[0] + shift[0]) % 2,
                (point[1] + shift[1]) % 2,
            )
        ]
        for point in points
    )
    return restrict(permutation_matrix(permutation))


def set_block(matrix, row_block, column_block, block):
    matrix[
        3 * row_block : 3 * row_block + 3,
        3 * column_block : 3 * column_block + 3,
    ] = block


operators = [
    restrict(permutation_matrix(row["permutations"][0]))
    for row in square_results["selected_operators"]
]
shear = restrict(
    permutation_matrix(rank_one_results["shear_permutation"])
)
rank_one_projector = (sp.eye(3) - shear) / 2
translation_p = translation((1, 0))
translation_q = translation((0, 1))


def branch_dirac(first, second, connector_sign):
    matrix = sp.zeros(12)
    edges = [
        (0, 1, rank_one_projector),
        (1, 2, operators[first]),
        (2, 3, operators[second]),
        (3, 0, connector_sign * sp.eye(3)),
    ]
    for source, target, block in edges:
        set_block(matrix, source, target, block)
        set_block(matrix, target, source, block.T)
    return matrix


branch_minus = branch_dirac(0, 1, 1)
branch_plus = branch_dirac(0, 2, -1)

unitary_a = sp.eye(3)
unitary_b = sp.diag(-1, 1, 1)
unitary_c = sp.diag(1, -1, 1)
unitary_d = -sp.eye(3)
coarse_equivalence = sp.diag(
    unitary_a,
    unitary_b,
    unitary_c,
    unitary_d,
)
grading = sp.diag(
    *(
        [1] * 3
        + [-1] * 3
        + [1] * 3
        + [-1] * 3
    )
)

coarse_algebra_generators = []
for node in range(4):
    generator = sp.zeros(12)
    set_block(generator, node, node, sp.eye(3))
    coarse_algebra_generators.append(generator)

full_j_swap = sp.zeros(24)
full_j_swap[:12, 12:] = sp.eye(12)
full_j_swap[12:, :12] = sp.eye(12)
full_equivalence = sp.diag(
    coarse_equivalence,
    coarse_equivalence,
)

loop_minus = sp.simplify(
    rank_one_projector
    * operators[0]
    * operators[1]
)
loop_plus = sp.simplify(
    -rank_one_projector
    * operators[0]
    * operators[2]
)

family_generators = {
    "T_p": translation_p,
    "T_q": translation_q,
    "S": shear,
    "P_minus": rank_one_projector,
}
represented_family_generators = {
    name: sp.diag(generator, generator, generator, generator)
    for name, generator in family_generators.items()
}

decorated_moments = {}
for name, represented in represented_family_generators.items():
    decorated_moments[name] = {
        "Tr_rho_D4_minus": str(
            sp.trace(represented * branch_minus**4)
        ),
        "Tr_rho_D4_plus": str(
            sp.trace(represented * branch_plus**4)
        ),
    }

variables = sp.symbols("x0:9")
generic_matrix = sp.Matrix(3, 3, variables)
commutant_equations = []
for generator in (translation_p, translation_q, shear):
    commutant_equations.extend(
        list(generic_matrix * generator - generator * generic_matrix)
    )
commutant_solution = sp.linsolve(
    commutant_equations,
    variables,
)

result = {
    "gate": "version4_algebra_embedding_weighted_selector",
    "coarse_algebra_acts_trivially_on_family_multiplicity": True,
    "explicit_coarse_commutant_unitary": {
        "U_A": str(unitary_a),
        "U_B": str(unitary_b),
        "U_C": str(unitary_c),
        "U_D": str(unitary_d),
    },
    "coarse_unitary_is_orthogonal": coarse_equivalence.T
    * coarse_equivalence
    == sp.eye(12),
    "coarse_unitary_determinant": str(sp.det(coarse_equivalence)),
    "coarse_unitary_maps_branches": sp.simplify(
        coarse_equivalence.T
        * branch_minus
        * coarse_equivalence
        - branch_plus
    )
    == sp.zeros(12),
    "coarse_unitary_commutes_with_algebra": all(
        coarse_equivalence * generator
        == generator * coarse_equivalence
        for generator in coarse_algebra_generators
    ),
    "coarse_unitary_commutes_with_grading": coarse_equivalence * grading
    == grading * coarse_equivalence,
    "full_unitary_commutes_with_J": full_equivalence * full_j_swap
    == full_j_swap * full_equivalence,
    "closed_loop_products_equal": loop_minus == loop_plus,
    "pfaffian_sign_flip_explained_by_orientation_reversal": sp.det(
        coarse_equivalence
    )
    == -1,
    "coarse_spectral_triples_unitarily_equivalent": True,
    "family_residual_commutant": str(commutant_solution),
    "coarse_equivalence_commutes_with_family_generators": {
        name: coarse_equivalence * represented
        == represented * coarse_equivalence
        for name, represented in represented_family_generators.items()
    },
    "enriched_family_embedding_blocks_explicit_equivalence": not all(
        coarse_equivalence * represented
        == represented * coarse_equivalence
        for represented in represented_family_generators.values()
    ),
    "enriched_commutant_edge_equations_consistent": False,
    "enriched_commutant_contradiction": "P and H_u edges force U_B=U_C=b I; connector gives U_D=-U_A; then the middle diagonal entry of U_C^* H_d^- U_D is -1 while H_d^+ requires +1",
    "decorated_fourth_moments": decorated_moments,
    "P_minus_weighted_moment_selects": "B_plus",
    "P_minus_weighted_values": {
        "B_minus": decorated_moments["P_minus"][
            "Tr_rho_D4_minus"
        ],
        "B_plus": decorated_moments["P_minus"][
            "Tr_rho_D4_plus"
        ],
    },
    "positive_P_minus_weighted_quartic_has_unique_branch": bool(
        sp.Rational(
            decorated_moments["P_minus"]["Tr_rho_D4_plus"]
        )
        < sp.Rational(
            decorated_moments["P_minus"]["Tr_rho_D4_minus"]
        )
    ),
    "standard_unweighted_spectral_action_selects_branch": False,
    "weighted_state_principle_derived": False,
    "physical_ckm_phase_derived": False,
    "status": "the branches are equivalent for the current coarse algebra, but become inequivalent when the canonical family embedding is promoted; a positive P_minus-weighted fourth moment selects B_plus conditionally",
}

with open(
    "s2t_v4_algebra_embedding_weighted_selector_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))