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
projector_odd = (sp.eye(3) - shear) / 2
operator_up = operators[0]
operator_down = operators[2]

dirac_plus = sp.zeros(12)
for source, target, block in (
    (0, 1, projector_odd),
    (1, 2, operator_up),
    (2, 3, operator_down),
    (3, 0, -sp.eye(3)),
):
    set_block(dirac_plus, source, target, block)
    set_block(dirac_plus, target, source, block.T)

dirac_fourth = dirac_plus**4
reduced_fourth = sp.zeros(3)
for node in range(4):
    reduced_fourth += dirac_fourth[
        3 * node : 3 * node + 3,
        3 * node : 3 * node + 3,
    ]

eigenvalues, eigenvectors = np.linalg.eigh(
    np.array(reduced_fourth, dtype=float)
)
ground_vector = eigenvectors[:, 0]
ground_state = np.outer(ground_vector, ground_vector)

projector_numeric = np.array(projector_odd, dtype=float)
operator_up_numeric = np.array(operator_up, dtype=float)
operator_down_numeric = np.array(operator_down, dtype=float)


def baseline_map(operator):
    return projector_numeric + 1j * operator


def state_anticommutator_map(operator):
    return projector_numeric + 1j * (
        ground_state @ operator + operator @ ground_state
    )


dirac_numeric = np.array(dirac_plus, dtype=float)
weight = np.kron(np.eye(4), ground_state)
quartic_derivative = np.zeros((12, 12))
for power in range(4):
    quartic_derivative += (
        np.linalg.matrix_power(dirac_numeric, 3 - power)
        @ weight
        @ np.linalg.matrix_power(dirac_numeric, power)
    )


def edge_gradient(source, target):
    forward = quartic_derivative[
        3 * source : 3 * source + 3,
        3 * target : 3 * target + 3,
    ]
    backward = quartic_derivative[
        3 * target : 3 * target + 3,
        3 * source : 3 * source + 3,
    ]
    return backward.T + forward


gradient_up = edge_gradient(1, 2)
gradient_down = edge_gradient(2, 3)


def readout(yukawa_up, yukawa_down):
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


readouts = {
    "baseline_P_plus_iH": readout(
        baseline_map(operator_up_numeric),
        baseline_map(operator_down_numeric),
    ),
    "state_anticommutator": readout(
        state_anticommutator_map(operator_up_numeric),
        state_anticommutator_map(operator_down_numeric),
    ),
    "quartic_cotangent_gradient": readout(
        gradient_up,
        gradient_down,
    ),
}

rng = np.random.default_rng(20260811)
orthogonal, _ = np.linalg.qr(rng.normal(size=(3, 3)))
transformed_projector = orthogonal @ projector_numeric @ orthogonal.T
transformed_state = orthogonal @ ground_state @ orthogonal.T


def covariance_error(map_name, operator):
    transformed_operator = orthogonal @ operator @ orthogonal.T
    if map_name == "baseline":
        direct = transformed_projector + 1j * transformed_operator
        original = baseline_map(operator)
    else:
        direct = transformed_projector + 1j * (
            transformed_state @ transformed_operator
            + transformed_operator @ transformed_state
        )
        original = state_anticommutator_map(operator)
    return float(np.linalg.norm(direct - orthogonal @ original @ orthogonal.T))


result = {
    "gate": "version4_yukawa_operator_map",
    "selected_geometry_branch": "B_plus",
    "ground_vector": [round(float(value), 12) for value in ground_vector],
    "projector_odd": str(projector_odd),
    "operator_up": str(operator_up),
    "operator_down": str(operator_down),
    "admissible_coefficient_free_maps": {
        "baseline": "Y(H)=P_minus+iH",
        "state_anticommutator": "Y(H)=P_minus+i{rho_star,H}",
        "quartic_cotangent": "Y_u=dV4/dH_u, Y_d=dV4/dH_d",
    },
    "basis_covariance_errors": {
        "baseline_up": covariance_error("baseline", operator_up_numeric),
        "baseline_down": covariance_error("baseline", operator_down_numeric),
        "state_up": covariance_error("state", operator_up_numeric),
        "state_down": covariance_error("state", operator_down_numeric),
    },
    "quartic_gradient_up": gradient_up.tolist(),
    "quartic_gradient_down": gradient_down.tolist(),
    "readouts": readouts,
    "same_data_give_cp_zero_and_cp_nonzero_maps": bool(
        not readouts["baseline_P_plus_iH"]["cp_nonzero"]
        and readouts["state_anticommutator"]["cp_nonzero"]
    ),
    "cotangent_map_is_real_and_cp_zero": bool(
        np.isrealobj(gradient_up)
        and np.isrealobj(gradient_down)
        and not readouts["quartic_cotangent_gradient"]["cp_nonzero"]
    ),
    "observed_edge_types_distinguished_by_family_data": False,
    "four_sector_dichotomy": (
        "a common map identifies normalized up with neutrino and down with "
        "charged-lepton textures; sector-specific maps introduce new input"
    ),
    "operator_map_uniquely_derived": False,
    "positive_result": (
        "the selected state supports a coefficient-free CP-nonzero polynomial "
        "map, so CP generation is algebraically possible"
    ),
    "status": (
        "existence pass but prediction no-go: the same selected geometry and "
        "state admit inequivalent covariant coefficient-free Yukawa maps"
    ),
}

assert max(result["basis_covariance_errors"].values()) < 1e-12
assert result["same_data_give_cp_zero_and_cp_nonzero_maps"]
assert result["cotangent_map_is_real_and_cp_zero"]

with open(
    "s2t_v4_yukawa_operator_map_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))