import json
import sympy as sp

with open("s2t_v4_family_square_spectral_selector_gate_results.json", encoding="utf-8") as handle:
    square_results = json.load(handle)
with open("s2t_v4_rank_one_breaking_gate_results.json", encoding="utf-8") as handle:
    rank_one_results = json.load(handle)

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

def set_block(matrix, row_block, column_block, block):
    matrix[3 * row_block:3 * row_block + 3, 3 * column_block:3 * column_block + 3] = block

operators = [
    restrict(permutation_matrix(row["permutations"][0]))
    for row in square_results["selected_operators"]
]
shear = restrict(permutation_matrix(rank_one_results["shear_permutation"]))
projector_odd = (sp.eye(3) - shear) / 2
projector_even = sp.eye(3) - projector_odd

def branch_dirac(first, second, connector_sign):
    matrix = sp.zeros(12)
    edges = [
        (0, 1, projector_odd),
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

def represent_family(matrix):
    return sp.diag(matrix, matrix, matrix, matrix)

def moment(weight, dirac):
    return sp.simplify(sp.trace(weight * dirac**4))

represented_odd = represent_family(projector_odd)
represented_even = represent_family(projector_even)
represented_shear = represent_family(shear)
moments = {
    "full": {"B_minus": sp.trace(branch_minus**4), "B_plus": sp.trace(branch_plus**4)},
    "odd_corner": {"B_minus": moment(represented_odd, branch_minus), "B_plus": moment(represented_odd, branch_plus)},
    "even_corner": {"B_minus": moment(represented_even, branch_minus), "B_plus": moment(represented_even, branch_plus)},
    "normalized_even_corner": {
        "B_minus": moment(represented_even, branch_minus) / projector_even.trace(),
        "B_plus": moment(represented_even, branch_plus) / projector_even.trace(),
    },
    "shear_weight": {"B_minus": moment(represented_shear, branch_minus), "B_plus": moment(represented_shear, branch_plus)},
}

def selected_branch(values):
    if values["B_minus"] < values["B_plus"]:
        return "B_minus"
    if values["B_plus"] < values["B_minus"]:
        return "B_plus"
    return "degenerate"

generic_matrix = sp.Matrix(3, 3, sp.symbols("x0:9"))
odd_expectation = projector_odd * generic_matrix * projector_odd
even_expectation = projector_even * generic_matrix * projector_even
k, mass_squared, coupling_squared, eigenvalue = sp.symbols("k M2 g2 lambda", real=True)
vectorlike_eigenvalue = mass_squared + coupling_squared * (k * eigenvalue) ** 2

result = {
    "gate": "version4_conditional_weight_origin",
    "odd_projector_rank": projector_odd.rank(),
    "even_projector_rank": projector_even.rank(),
    "odd_corner_expectation_idempotent": projector_odd * odd_expectation * projector_odd == odd_expectation,
    "even_corner_expectation_idempotent": projector_even * even_expectation * projector_even == even_expectation,
    "fourth_moments": {
        name: {branch: str(value) for branch, value in values.items()}
        for name, values in moments.items()
    },
    "branch_selected_by_weight": {name: selected_branch(values) for name, values in moments.items()},
    "full_trace_is_sum_of_corners": all(
        moments["full"][branch] == moments["odd_corner"][branch] + moments["even_corner"][branch]
        for branch in ("B_minus", "B_plus")
    ),
    "corner_choices_select_opposite_branches": selected_branch(moments["odd_corner"]) != selected_branch(moments["even_corner"]),
    "conditional_expectation_derives_state_after_corner_is_chosen": True,
    "conditional_expectation_selects_corner": False,
    "canonical_weight_selector_unique": False,
    "vectorlike_orientation_eigenvalue": str(vectorlike_eigenvalue),
    "vectorlike_even_determinant_independent_of_k_sign": sp.simplify(
        vectorlike_eigenvalue.subs(k, -1) - vectorlike_eigenvalue.subs(k, 1)
    ) == 0,
    "status": "odd and even corners select opposite branches; vectorlike loops are orientation-even, so a variational state-selection principle is required",
}

with open("s2t_v4_conditional_weight_origin_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)
print(json.dumps(result, ensure_ascii=False, indent=2))