import itertools
import json

import numpy as np
import sympy as sp
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


def candidate_data(messenger_ratio, sign_bits):
    result = {}
    for sector, (first_edge, second_edge) in signed_sector_pairs(sign_bits).items():
        left_casimir, right_casimir = casimir_endpoints[sector]
        determinant = (
            (messenger_ratio + left_casimir)
            * (messenger_ratio + right_casimir)
            - 1
        )
        schur_term = (
            (messenger_ratio + right_casimir) * (first_edge @ first_edge)
            + (messenger_ratio + left_casimir) * (second_edge @ second_edge)
            + 1j * (second_edge @ first_edge - first_edge @ second_edge)
        ) / determinant
        yukawa = projector_odd - schur_term
        mass_squared = yukawa @ yukawa.conj().T
        eigenvalues, eigenvectors = np.linalg.eigh(mass_squared)
        masses = np.sqrt(np.maximum(eigenvalues, 0))
        result[sector] = {
            "normalized_masses": masses / masses[-1],
            "left_eigenvectors": eigenvectors,
        }
    return result


def mass_objective(log_ratio, sign_bits):
    messenger_ratio = np.exp(float(log_ratio))
    data = candidate_data(messenger_ratio, sign_bits)
    prediction = np.concatenate(
        [data["u"]["normalized_masses"][:2], data["d"]["normalized_masses"][:2]]
    )
    target = np.concatenate(
        [mass_targets["u"][:2], mass_targets["d"][:2]]
    )
    if np.any(prediction <= 0):
        return 1e9
    return float(np.sqrt(np.mean(np.log(prediction / target) ** 2)))


rows = []
for sign_bits in itertools.product((-1, 1), repeat=4):
    fit = differential_evolution(
        lambda value: mass_objective(value[0], sign_bits),
        [(-10, 15)],
        seed=1729,
        tol=1e-11,
        polish=True,
    )
    rows.append(
        {
            "sign_bits": list(sign_bits),
            "messenger_ratio": float(np.exp(fit.x[0])),
            "mass_log_rms": float(fit.fun),
        }
    )

rows.sort(key=lambda row: row["mass_log_rms"])
best = rows[0]
best_data = candidate_data(best["messenger_ratio"], best["sign_bits"])
up_vectors = best_data["u"]["left_eigenvectors"]
down_vectors = best_data["d"]["left_eigenvectors"]
ckm = up_vectors.conj().T @ down_vectors
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
    ratios = (
        best_data[sector]["normalized_masses"][:2]
        / mass_targets[sector][:2]
    )
    mass_errors[sector] = np.maximum(ratios, 1 / ratios).tolist()

output = {
    "gate": "version4_casimir_messenger_propagator",
    "casimir_endpoints": {
        sector: list(values) for sector, values in casimir_endpoints.items()
    },
    "menu_size": len(rows),
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
    "up_down_mass_difference_norm": float(
        np.linalg.norm(
            best_data["u"]["normalized_masses"]
            - best_data["d"]["normalized_masses"]
        )
    ),
    "verdict": "scalar representation Casimirs split sectors but are suppressed at the mass optimum",
}

with open(
    "s2t_v4_casimir_messenger_propagator_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))