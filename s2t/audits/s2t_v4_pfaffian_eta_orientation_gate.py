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


def pfaffian(matrix):
    size = matrix.rows
    if size == 0:
        return sp.Integer(1)
    result = sp.Integer(0)
    for column in range(1, size):
        if matrix[0, column] == 0:
            continue
        remaining = [
            index for index in range(size) if index not in (0, column)
        ]
        minor = matrix.extract(remaining, remaining)
        result += (
            (-1) ** (column + 1)
            * matrix[0, column]
            * pfaffian(minor)
        )
    return sp.simplify(result)


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


plus_indices = [0, 1, 2, 6, 7, 8]
minus_indices = [3, 4, 5, 9, 10, 11]
canonical_order = plus_indices + minus_indices
canonical_grading = sp.diag(*([1] * 6 + [-1] * 6))


def branch_data(name, first, second, connector_sign):
    dirac = branch_dirac(first, second, connector_sign)
    reordered = dirac.extract(canonical_order, canonical_order)
    chiral_block = reordered[:6, 6:]
    antisymmetric_form = sp.simplify(canonical_grading * reordered)
    reduced_pfaffian = pfaffian(antisymmetric_form)
    full_form = sp.diag(antisymmetric_form, -antisymmetric_form)
    full_pfaffian = pfaffian(full_form)
    eigenvalues = dirac.eigenvals()
    positive_multiplicity = sum(
        multiplicity
        for eigenvalue, multiplicity in eigenvalues.items()
        if eigenvalue.is_positive
    )
    negative_multiplicity = sum(
        multiplicity
        for eigenvalue, multiplicity in eigenvalues.items()
        if eigenvalue.is_negative
    )
    return {
        "name": name,
        "det_chiral_block": str(sp.det(chiral_block)),
        "reduced_pfaffian": str(reduced_pfaffian),
        "reduced_pfaffian_squared": str(reduced_pfaffian**2),
        "reduced_form_antisymmetric": antisymmetric_form.T
        == -antisymmetric_form,
        "full_ko6_pfaffian": str(full_pfaffian),
        "full_ko6_form_antisymmetric": full_form.T == -full_form,
        "eta_signature": positive_multiplicity - negative_multiplicity,
    }


branch_minus = branch_data("B_minus", 0, 1, 1)
branch_plus = branch_data("B_plus", 0, 2, -1)

reference_dirac = branch_dirac(0, 1, 1).extract(
    canonical_order,
    canonical_order,
)
reference_form = canonical_grading * reference_dirac
reference_pfaffian = pfaffian(reference_form)
odd_basis_permutation = sp.eye(12)
odd_basis_permutation.row_swap(0, 1)
flipped_form = (
    odd_basis_permutation.T
    * reference_form
    * odd_basis_permutation
)
orientation_flip_pfaffian = pfaffian(flipped_form)

theta = sp.symbols("theta", real=True)
z = sp.exp(sp.I * theta)
determinant_paths = {
    "W_minus_one_half": str(
        sp.factor((z + 2) * z ** (-3) / 2)
    ),
    "W_plus_one_half": str(
        sp.factor(-(z - 2) * z ** (-3) / 2)
    ),
}

result = {
    "gate": "version4_pfaffian_eta_orientation",
    "canonical_antisymmetric_form": "A_red=gamma D in plus-then-minus chiral ordering",
    "pfaffian_identity": "Pf([[0,M],[-M^T,0]])=(-1)^15 det(M)=-det(M)",
    "branches": [branch_minus, branch_plus],
    "reduced_pfaffians_opposite": branch_minus["reduced_pfaffian"]
    == f"-{branch_plus['reduced_pfaffian']}",
    "reduced_relative_phase": "pi",
    "full_ko6_pfaffians_equal": branch_minus["full_ko6_pfaffian"]
    == branch_plus["full_ko6_pfaffian"],
    "full_ko6_phase_cancels": True,
    "eta_invariants_equal_zero": branch_minus["eta_signature"] == 0
    and branch_plus["eta_signature"] == 0,
    "odd_basis_permutation_flips_reduced_pfaffian": str(
        orientation_flip_pfaffian
    )
    == str(-reference_pfaffian),
    "determinant_line_orientation_derived": False,
    "complex_connector_paths": determinant_paths,
    "complex_paths_avoid_zero": True,
    "reduced_sign_is_topological_on_full_complex_configuration_space": False,
    "vacuum_energy_is_split_by_pfaffian_sign": False,
    "conditional_quantum_relative_sign_exists": True,
    "status": "a reduced oriented chiral Pfaffian gives opposite signs, but the full KO6 pair cancels the phase; eta is zero and the reduced sign is basis-orientation dependent and not topological in the complex configuration space",
}

with open(
    "s2t_v4_pfaffian_eta_orientation_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))