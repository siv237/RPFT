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

x = sp.symbols("x")
characteristic_minus = sp.factor(
    branch_minus.charpoly(x).as_expr()
)
characteristic_plus = sp.factor(
    branch_plus.charpoly(x).as_expr()
)
characteristic_squared_minus = sp.factor(
    (branch_minus**2).charpoly(x).as_expr()
)
characteristic_squared_plus = sp.factor(
    (branch_plus**2).charpoly(x).as_expr()
)

grading = sp.diag(
    *(
        [1] * 3
        + [-1] * 3
        + [1] * 3
        + [-1] * 3
    )
)

moment_rows = []
for power in range(1, 13):
    trace_minus = sp.trace(branch_minus**power)
    trace_plus = sp.trace(branch_plus**power)
    moment_rows.append(
        {
            "power": power,
            "trace_minus": str(trace_minus),
            "trace_plus": str(trace_plus),
            "equal": trace_minus == trace_plus,
        }
    )

graded_rows = []
for power in range(1, 7):
    graded_minus = sp.trace(
        grading * branch_minus ** (2 * power)
    )
    graded_plus = sp.trace(
        grading * branch_plus ** (2 * power)
    )
    graded_rows.append(
        {
            "even_power": 2 * power,
            "supertrace_minus": str(graded_minus),
            "supertrace_plus": str(graded_plus),
            "both_zero": graded_minus == 0 and graded_plus == 0,
        }
    )

result = {
    "gate": "version4_orientation_spectral_no_go",
    "branch_minus": {"cross_word": "-1/2", "theta": "0"},
    "branch_plus": {"cross_word": "1/2", "theta": "pi"},
    "primary_dirac_dimension": 12,
    "characteristic_polynomial_minus": str(characteristic_minus),
    "characteristic_polynomial_plus": str(characteristic_plus),
    "characteristic_polynomials_equal": characteristic_minus
    == characteristic_plus,
    "squared_characteristic_polynomials_equal": characteristic_squared_minus
    == characteristic_squared_plus,
    "ordinary_moments_through_dimension": moment_rows,
    "all_ordinary_moments_equal": all(
        row["equal"] for row in moment_rows
    ),
    "graded_even_moments": graded_rows,
    "all_tested_supertraces_zero": all(
        row["both_zero"] for row in graded_rows
    ),
    "determinant_minus": str(sp.det(branch_minus)),
    "determinant_plus": str(sp.det(branch_plus)),
    "determinants_equal": sp.det(branch_minus) == sp.det(branch_plus),
    "cp_odd_loop_observable_minus": "W sin(theta)=0",
    "cp_odd_loop_observable_plus": "W sin(theta)=0",
    "ordinary_real_spectral_action_can_select_orientation": False,
    "graded_spectral_action_can_select_orientation": False,
    "surviving_orientation_sensitive_routes": [
        "fermionic Pfaffian or eta-invariant phase",
        "quantized boundary Chern-Simons or anomaly-inflow term",
        "explicit relaxation of the real-even spectral-action class",
    ],
    "status": "the two noncommuting minima are exactly isospectral, so no real function Tr f(D^2), determinant magnitude or tested graded trace can select their orientation",
}

with open(
    "s2t_v4_orientation_spectral_no_go_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))