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
with open(
    "s2t_v4_variational_family_state_gate_results.json",
    encoding="utf-8",
) as handle:
    variational_results = json.load(handle)


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
    return np.array(
        sp.simplify(triplet_basis.T * matrix * triplet_basis),
        dtype=complex,
    )


def independent(matrices, tolerance=1e-8):
    basis = []
    for matrix in matrices:
        previous = (
            np.column_stack([item.reshape(-1) for item in basis])
            if basis
            else np.zeros((9, 0), dtype=complex)
        )
        augmented = np.column_stack([previous, matrix.reshape(-1)])
        if np.linalg.matrix_rank(augmented, tol=tolerance) > len(basis):
            basis.append(matrix)
    return basis


def algebra_closure(generators):
    basis = independent(generators)
    while True:
        enlarged = independent(
            basis + [left @ right for left in basis for right in basis]
        )
        if len(enlarged) == len(basis):
            return basis
        basis = enlarged


def family_one_forms(algebra_basis, edge):
    return independent(
        [
            left @ (edge @ right - right @ edge)
            for left in algebra_basis
            for right in algebra_basis
        ]
    )


def belongs_to_span(basis, matrix, tolerance=1e-8):
    span = (
        np.column_stack([item.reshape(-1) for item in basis])
        if basis
        else np.zeros((9, 0), dtype=complex)
    )
    augmented = np.column_stack([span, matrix.reshape(-1)])
    return bool(
        np.linalg.matrix_rank(augmented, tol=tolerance)
        == np.linalg.matrix_rank(span, tol=tolerance)
    )


operators = [
    restrict(permutation_matrix(row["permutations"][0]))
    for row in square_results["selected_operators"]
]
operator_up = operators[0]
operator_down = operators[2]

identity = np.eye(3, dtype=complex)
translation_p = np.diag([-1, 1, -1]).astype(complex)
translation_q = np.diag([1, -1, -1]).astype(complex)
shear = restrict(
    permutation_matrix(rank_one_results["shear_permutation"])
)
projector_odd = (identity - shear) / 2
ground_vector = np.array(
    variational_results["ground_data"]["4"]["B_plus"]["ground_vector"],
    dtype=float,
)
ground_state = np.outer(ground_vector, ground_vector).astype(complex)

matrix_units = []
for row in range(3):
    for column in range(3):
        matrix = np.zeros((3, 3), dtype=complex)
        matrix[row, column] = 1
        matrix_units.append(matrix)

algebras = {
    "coarse_C": [identity],
    "state_C2": algebra_closure([identity, ground_state]),
    "residual_family": algebra_closure(
        [identity, translation_p, translation_q, shear]
    ),
    "full_M3": matrix_units,
    "generated_selected_data": algebra_closure(
        [identity, projector_odd, ground_state, operator_up, operator_down]
    ),
}


rows = []
for algebra_name, algebra_basis in algebras.items():
    row = {
        "algebra": algebra_name,
        "algebra_dimension": len(algebra_basis),
        "edges": {},
    }
    for edge_name, edge in (
        ("up", operator_up),
        ("down", operator_down),
    ):
        one_forms = family_one_forms(algebra_basis, edge)
        target = 1j * (ground_state @ edge + edge @ ground_state)
        row["edges"][edge_name] = {
            "one_form_dimension": len(one_forms),
            "contains_state_anticommutator_correction": belongs_to_span(
                one_forms, target
            ),
        }
    rows.append(row)


row_by_name = {row["algebra"]: row for row in rows}
result = {
    "gate": "version4_inner_fluctuation_yukawa",
    "local_family_one_form_definition": "Omega_H^1(A)=span{a[H,b]}",
    "rows": rows,
    "dimension_sequence_up": [
        row_by_name[name]["edges"]["up"]["one_form_dimension"]
        for name in ("coarse_C", "state_C2", "residual_family", "full_M3")
    ],
    "dimension_sequence_down": [
        row_by_name[name]["edges"]["down"]["one_form_dimension"]
        for name in ("coarse_C", "state_C2", "residual_family", "full_M3")
    ],
    "target_first_appears_in_full_M3": all(
        not row_by_name[name]["edges"][edge][
            "contains_state_anticommutator_correction"
        ]
        for name in ("coarse_C", "state_C2", "residual_family")
        for edge in ("up", "down")
    )
    and all(
        row_by_name["full_M3"]["edges"][edge][
            "contains_state_anticommutator_correction"
        ]
        for edge in ("up", "down")
    ),
    "selected_data_generate_full_M3": bool(
        len(algebras["generated_selected_data"]) == 9
    ),
    "coarse_failure": (
        "family multiplicity algebra cannot create a rho-dependent correction"
    ),
    "full_failure": (
        "the first algebra large enough to contain the CP-capable correction "
        "also restores the full arbitrary M3 family one-form space"
    ),
    "unique_inner_fluctuation_map_derived": False,
    "status": (
        "inner-fluctuation dichotomy: small family algebras exclude the "
        "CP-capable map, while full M3 includes it non-uniquely"
    ),
}

assert result["dimension_sequence_up"] == [0, 2, 8, 9]
assert result["dimension_sequence_down"] == [0, 2, 8, 9]
assert result["target_first_appears_in_full_M3"]
assert result["selected_data_generate_full_M3"]

with open(
    "s2t_v4_inner_fluctuation_yukawa_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))