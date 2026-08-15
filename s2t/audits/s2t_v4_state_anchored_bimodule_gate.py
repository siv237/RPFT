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
        dtype=float,
    )


operators = [
    restrict(permutation_matrix(row["permutations"][0]))
    for row in square_results["selected_operators"]
]
operator_up = operators[0]
operator_down = operators[2]
shear = restrict(
    permutation_matrix(rank_one_results["shear_permutation"])
)
projector_odd = (np.eye(3) - shear) / 2
ground_vector = np.array(
    variational_results["ground_data"]["4"]["B_plus"]["ground_vector"],
    dtype=float,
)
state = np.outer(ground_vector, ground_vector)
complement = np.eye(3) - state


def state_projection(matrix):
    return matrix - complement @ matrix @ complement


matrix_units = []
for row in range(3):
    for column in range(3):
        matrix = np.zeros((3, 3))
        matrix[row, column] = 1
        matrix_units.append(matrix)

projected_units = [state_projection(matrix) for matrix in matrix_units]
superoperator = np.column_stack(
    [matrix.reshape(-1) for matrix in projected_units]
)

idempotence_error = max(
    np.linalg.norm(state_projection(state_projection(matrix)) - state_projection(matrix))
    for matrix in matrix_units
)
self_adjointness_error = np.linalg.norm(superoperator - superoperator.T)
star_closure_error = max(
    np.linalg.norm(
        state_projection(matrix).conj().T
        - state_projection(matrix.conj().T)
    )
    for matrix in matrix_units
)

state_algebra = [state, complement]
bimodule_error = 0.0
for left in state_algebra:
    for right in state_algebra:
        for matrix in projected_units:
            candidate = left @ matrix @ right
            bimodule_error = max(
                bimodule_error,
                np.linalg.norm(state_projection(candidate) - candidate),
            )

rng = np.random.default_rng(20260811)
orthogonal, _ = np.linalg.qr(rng.normal(size=(3, 3)))
transformed_state = orthogonal @ state @ orthogonal.T
transformed_complement = np.eye(3) - transformed_state


def transformed_projection(matrix):
    return matrix - transformed_complement @ matrix @ transformed_complement


covariance_error = max(
    np.linalg.norm(
        transformed_projection(orthogonal @ matrix @ orthogonal.T)
        - orthogonal @ state_projection(matrix) @ orthogonal.T
    )
    for matrix in matrix_units
)


def readout(operator_up, operator_down):
    yukawa_up = projector_odd + 1j * state_projection(operator_up)
    yukawa_down = projector_odd + 1j * state_projection(operator_down)
    mass_up = yukawa_up @ yukawa_up.conj().T
    mass_down = yukawa_down @ yukawa_down.conj().T
    eigenvalues_up, eigenvectors_up = np.linalg.eigh(mass_up)
    eigenvalues_down, eigenvectors_down = np.linalg.eigh(mass_down)
    mixing = eigenvectors_up.conj().T @ eigenvectors_down
    commutator = mass_up @ mass_down - mass_down @ mass_up
    cp_trace = np.trace(commutator @ commutator @ commutator)
    masses_up = np.sqrt(np.maximum(eigenvalues_up, 0))
    masses_down = np.sqrt(np.maximum(eigenvalues_down, 0))
    return {
        "mass_squared_eigenvalues_up": [
            round(float(value), 12) for value in eigenvalues_up
        ],
        "mass_squared_eigenvalues_down": [
            round(float(value), 12) for value in eigenvalues_down
        ],
        "normalized_masses_up": [
            round(float(value / masses_up[-1]), 12)
            for value in masses_up
        ],
        "normalized_masses_down": [
            round(float(value / masses_down[-1]), 12)
            for value in masses_down
        ],
        "absolute_mixing_matrix": [
            [round(float(value), 12) for value in row]
            for row in np.abs(mixing)
        ],
        "cp_invariant_im_Tr_commutator_cube": float(cp_trace.imag),
        "cp_nonzero": bool(abs(cp_trace.imag) > 1e-8),
    }


readout_data = readout(operator_up, operator_down)
result = {
    "gate": "version4_state_anchored_bimodule",
    "module": "M_rho=rho M3 + M3 rho={X:(1-rho)X(1-rho)=0}",
    "module_dimension": int(np.linalg.matrix_rank(superoperator, tol=1e-8)),
    "kernel_dimension": 9 - int(np.linalg.matrix_rank(superoperator, tol=1e-8)),
    "orthogonal_projection": "Pi_rho(X)=X-(1-rho)X(1-rho)",
    "projection_equals": "rho X + X rho - rho X rho",
    "idempotence_error": float(idempotence_error),
    "hilbert_schmidt_self_adjointness_error": float(self_adjointness_error),
    "star_closure_error": float(star_closure_error),
    "state_algebra_bimodule_error": float(bimodule_error),
    "basis_covariance_error": float(covariance_error),
    "continuous_coefficient_required": False,
    "support_axiom": "every subleading connector touches the selected state at at least one endpoint",
    "readout": readout_data,
    "conditional_operator_map": "Y_s=P_minus+i Pi_rho(H_s)",
    "conditional_pass": bool(readout_data["cp_nonzero"]),
    "remaining_four_sector_obstruction": True,
    "status": (
        "a canonical five-dimensional state-anchored bimodule and its unique "
        "Hilbert-Schmidt projection select a CP-nonzero map conditionally on "
        "the support axiom"
    ),
}

assert result["module_dimension"] == 5
assert result["kernel_dimension"] == 4
assert result["idempotence_error"] < 1e-9
assert result["hilbert_schmidt_self_adjointness_error"] < 1e-9
assert result["star_closure_error"] < 1e-9
assert result["state_algebra_bimodule_error"] < 1e-9
assert result["basis_covariance_error"] < 1e-9
assert result["conditional_pass"]

with open(
    "s2t_v4_state_anchored_bimodule_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))