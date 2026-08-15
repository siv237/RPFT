import itertools
import json

import numpy as np
import sympy as sp
from scipy.linalg import expm
from scipy.optimize import differential_evolution


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
    return np.array(triplet_basis.T * matrix * triplet_basis, dtype=float)


def set_block(matrix, row_block, column_block, block):
    matrix[
        3 * row_block : 3 * row_block + 3,
        3 * column_block : 3 * column_block + 3,
    ] = block


edge_operators = {}
for row in square_results["selected_operators"]:
    permutation = row["permutations"][0]
    moved = [index for index, target in enumerate(permutation) if index != target]
    first, second = points[moved[0]], points[moved[1]]
    lepton = first if first[0] == 0 else second
    quark = second if second[0] == 1 else first
    edge_operators[(lepton[1], quark[1])] = restrict(
        permutation_matrix(permutation)
    )

shear = restrict(permutation_matrix(rank_one_results["shear_permutation"]))
projector_odd = (np.eye(3) - shear) / 2

dirac_plus = np.zeros((12, 12), dtype=complex)
for source, target, block in (
    (0, 1, projector_odd),
    (1, 2, edge_operators[(1, 1)]),
    (2, 3, edge_operators[(0, 0)]),
    (3, 0, -np.eye(3)),
):
    set_block(dirac_plus, source, target, block)
    set_block(dirac_plus, target, source, block.T)

dirac_fourth = np.linalg.matrix_power(dirac_plus, 4)
node_blocks = [
    dirac_fourth[3 * node : 3 * node + 3, 3 * node : 3 * node + 3].real
    for node in range(4)
]
left_moment = node_blocks[0] + node_blocks[3]
right_moment = node_blocks[1] + node_blocks[2]

casimir_endpoints = {
    "u": (21 / 10, 8 / 5),
    "d": (21 / 10, 7 / 5),
    "nu": (9 / 10, 0),
    "e": (9 / 10, 3 / 5),
}
mass_targets = {
    "u": np.array([1.2521739130434784e-5, 0.0073623188405797105, 1.0]),
    "d": np.array([0.0011172248803827751, 0.022344497607655507, 1.0]),
}
ckm_target = np.array([0.22501, 0.04183, 0.003732])
ckm_jarlskog_target = 3.12e-5

standardized_operators = {}
spectral_standard_deviations = {}
gibbs_states = {}
state_square_roots = {}
state_eigenvalues = {}
for sector, (left_casimir, right_casimir) in casimir_endpoints.items():
    parent = left_casimir * left_moment + right_casimir * right_moment
    mean = np.trace(parent) / 3
    centered = parent - mean * np.eye(3)
    standard_deviation = np.sqrt(np.trace(centered @ centered) / 3)
    standardized = centered / standard_deviation
    state = expm(-standardized)
    state /= np.trace(state)
    eigenvalues, eigenvectors = np.linalg.eigh(state)
    standardized_operators[sector] = standardized
    spectral_standard_deviations[sector] = float(standard_deviation)
    gibbs_states[sector] = state
    state_square_roots[sector] = (
        eigenvectors * np.sqrt(eigenvalues)
    ) @ eigenvectors.T
    state_eigenvalues[sector] = eigenvalues.tolist()


def signed_sector_pairs(sign_bits):
    edge_order = [(0, 0), (0, 1), (1, 0), (1, 1)]
    signed = {
        edge: sign_bits[index] * edge_operators[edge]
        for index, edge in enumerate(edge_order)
    }
    return {
        "e": (signed[(0, 0)], signed[(0, 1)]),
        "nu": (signed[(1, 0)], signed[(1, 1)]),
        "d": (signed[(0, 0)], signed[(1, 0)]),
        "u": (signed[(0, 1)], signed[(1, 1)]),
    }


def endpoint_row(orientation, sector, first_edge, second_edge):
    state_root = state_square_roots[sector]
    if orientation == "left_gns":
        return np.hstack([state_root @ first_edge, state_root @ second_edge])
    if orientation == "right_gns":
        return np.hstack([first_edge @ state_root, second_edge @ state_root])
    if orientation == "kms_symmetric":
        return np.hstack(
            [
                state_root @ first_edge @ state_root,
                state_root @ second_edge @ state_root,
            ]
        )
    raise ValueError(orientation)


def candidate_data(orientation, messenger_ratio, sign_bits):
    identity = np.eye(3)
    heavy_block = np.block(
        [
            [messenger_ratio * identity, 1j * identity],
            [-1j * identity, messenger_ratio * identity],
        ]
    )
    propagator = np.linalg.inv(heavy_block)
    result = {}
    for sector, (first_edge, second_edge) in signed_sector_pairs(sign_bits).items():
        endpoints = endpoint_row(orientation, sector, first_edge, second_edge)
        yukawa = projector_odd - endpoints @ propagator @ endpoints.conj().T
        mass_squared = yukawa @ yukawa.conj().T
        eigenvalues, eigenvectors = np.linalg.eigh(mass_squared)
        masses = np.sqrt(np.maximum(eigenvalues, 0))
        result[sector] = {
            "normalized_masses": masses / masses[-1],
            "left_eigenvectors": eigenvectors,
        }
    return result


def mass_objective(log_gap, orientation, sign_bits):
    messenger_ratio = 1 + np.exp(float(log_gap))
    data = candidate_data(orientation, messenger_ratio, sign_bits)
    prediction = np.concatenate(
        [data["u"]["normalized_masses"][:2], data["d"]["normalized_masses"][:2]]
    )
    target = np.concatenate(
        [mass_targets["u"][:2], mass_targets["d"][:2]]
    )
    if np.any(prediction <= 0):
        return 1e9
    return float(np.sqrt(np.mean(np.log(prediction / target) ** 2)))


orientation_rows = []
for orientation in ("left_gns", "right_gns", "kms_symmetric"):
    sign_rows = []
    for sign_bits in itertools.product((-1, 1), repeat=4):
        fit = differential_evolution(
            lambda value: mass_objective(value[0], orientation, sign_bits),
            [(-10, 15)],
            seed=1729,
            tol=1e-11,
            polish=True,
        )
        sign_rows.append(
            {
                "sign_bits": list(sign_bits),
                "messenger_ratio": float(1 + np.exp(fit.x[0])),
                "mass_log_rms": float(fit.fun),
            }
        )
    sign_rows.sort(key=lambda row: row["mass_log_rms"])
    orientation_rows.append({"orientation": orientation, **sign_rows[0]})

orientation_rows.sort(key=lambda row: row["mass_log_rms"])
best = orientation_rows[0]
best_data = candidate_data(
    best["orientation"], best["messenger_ratio"], best["sign_bits"]
)
ckm = best_data["u"]["left_eigenvectors"].conj().T @ best_data["d"][
    "left_eigenvectors"
]
ckm_absolute = np.abs(ckm)
ckm_angles = np.array([ckm_absolute[0, 1], ckm_absolute[1, 2], ckm_absolute[0, 2]])
jarlskog = abs(
    np.imag(
        ckm[0, 0]
        * ckm[1, 1]
        * np.conj(ckm[0, 1])
        * np.conj(ckm[1, 0])
    )
)

mass_errors = {}
for sector in ("u", "d"):
    ratios = best_data[sector]["normalized_masses"][:2] / mass_targets[sector][:2]
    mass_errors[sector] = np.maximum(ratios, 1 / ratios).tolist()

output = {
    "gate": "version4_affine_modular_temperature",
    "standardization": "Z_s=(R_s-Tr(R_s)I/3)/sqrt(Tr((R_s-Tr(R_s)I/3)^2)/3)",
    "variational_functional": "F_s(rho)=Tr(rho Z_s)+Tr(rho log rho)",
    "spectral_standard_deviations": spectral_standard_deviations,
    "state_eigenvalues": state_eigenvalues,
    "orientation_rows": orientation_rows,
    "best": best,
    "normalized_masses": {
        sector: best_data[sector]["normalized_masses"].tolist()
        for sector in ("u", "d", "e", "nu")
    },
    "mass_multiplicative_errors": mass_errors,
    "ckm_absolute": ckm_absolute.tolist(),
    "ckm_angles": ckm_angles.tolist(),
    "ckm_angle_ratios": (ckm_angles / ckm_target).tolist(),
    "jarlskog_absolute": jarlskog,
    "jarlskog_ratio": jarlskog / ckm_jarlskog_target,
    "affine_invariant": True,
    "mass_train_pass": False,
    "ckm_blind_pass": False,
    "verdict": "affine normalization derives the modular scale and improves hierarchy and Cabibbo mixing, but full flavour closure still fails",
}

with open(
    "s2t_v4_affine_modular_temperature_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))