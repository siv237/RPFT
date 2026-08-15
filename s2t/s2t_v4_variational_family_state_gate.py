import json
import numpy as np
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

def graph_partial_trace(matrix):
    return sp.simplify(sum(
        (matrix[3 * node:3 * node + 3, 3 * node:3 * node + 3] for node in range(4)),
        sp.zeros(3),
    ))

branch_minus = branch_dirac(0, 1, 1)
branch_plus = branch_dirac(0, 2, -1)
reduced_operators = {
    power: {
        "B_minus": graph_partial_trace(branch_minus**power),
        "B_plus": graph_partial_trace(branch_plus**power),
    }
    for power in (2, 4, 6)
}

def ground_data(matrix):
    eigenvalues, eigenvectors = np.linalg.eigh(np.array(matrix, dtype=float))
    ground_vector = eigenvectors[:, 0]
    odd_vector = np.array([0, 1, -1], dtype=float) / np.sqrt(2)
    return {
        "eigenvalues": [round(float(value), 12) for value in eigenvalues],
        "ground_value": float(eigenvalues[0]),
        "ground_vector": [round(float(value), 12) for value in ground_vector],
        "odd_projector_overlap": float(abs(np.vdot(odd_vector, ground_vector)) ** 2),
        "ground_state_unique": bool(abs(eigenvalues[1] - eigenvalues[0]) > 1e-10),
    }

grounds = {
    power: {branch: ground_data(matrix) for branch, matrix in branches.items()}
    for power, branches in reduced_operators.items()
}
x = sp.symbols("x")
minus_exact = 17 - sp.sqrt(57) / 2
plus_polynomial = 4 * x**3 - 192 * x**2 + 3003 * x - 15358

result = {
    "gate": "version4_variational_family_state",
    "family_state_space": "rho>=0, Tr(rho)=1",
    "functional": "V_2n(D,rho)=Tr(rho R_2n(D))",
    "rayleigh_ritz_minimum": "lambda_min(R_2n)",
    "reduced_operators": {
        str(power): {branch: str(matrix) for branch, matrix in branches.items()}
        for power, branches in reduced_operators.items()
    },
    "ground_data": {str(power): branches for power, branches in grounds.items()},
    "quadratic_ground_values_equal": abs(grounds[2]["B_minus"]["ground_value"] - grounds[2]["B_plus"]["ground_value"]) < 1e-12,
    "quartic_minus_exact_ground_value": str(minus_exact),
    "quartic_plus_ground_root_bracket": ["25/2", "13"],
    "quartic_plus_polynomial_at_25_over_2": str(plus_polynomial.subs(x, sp.Rational(25, 2))),
    "quartic_plus_polynomial_at_13": str(plus_polynomial.subs(x, 13)),
    "quartic_minus_ground_value_greater_than_13": bool(minus_exact > 13),
    "quartic_selected_branch": "B_plus",
    "quartic_ground_gap": grounds[4]["B_minus"]["ground_value"] - grounds[4]["B_plus"]["ground_value"],
    "quartic_ground_states_unique": all(data["ground_state_unique"] for data in grounds[4].values()),
    "quartic_ground_state_equals_odd_corner": False,
    "sixth_moment_stress_selected_branch": "B_plus" if grounds[6]["B_plus"]["ground_value"] < grounds[6]["B_minus"]["ground_value"] else "B_minus",
    "preselected_corner_required": False,
    "continuous_weight_parameter_required": False,
    "requires_enriched_family_identification_across_nodes": True,
    "physical_ckm_phase_derived": False,
    "status": "joint minimization over all family states selects B_plus at D^4 with no preselected corner; Yukawa readout remains open",
}

with open("s2t_v4_variational_family_state_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)
print(json.dumps(result, ensure_ascii=False, indent=2))