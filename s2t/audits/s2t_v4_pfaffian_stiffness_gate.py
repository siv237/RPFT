import itertools
import json

import numpy as np
import sympy as sp
from scipy.linalg import eigvalsh, expm
from scipy.optimize import differential_evolution, minimize_scalar


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


def standardize(matrix):
    centered = matrix - np.trace(matrix) * np.eye(3) / 3
    standard_deviation = np.sqrt(
        np.real(np.trace(centered.conj().T @ centered)) / 3
    )
    return centered / standard_deviation


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

node_blocks = {}
for power in (4, 6):
    powered = np.linalg.matrix_power(dirac_plus, power)
    node_blocks[power] = [
        powered[3 * node : 3 * node + 3, 3 * node : 3 * node + 3]
        for node in range(4)
    ]

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

constraints = {}
for sector, (left_casimir, right_casimir) in casimir_endpoints.items():
    standardized_moments = {}
    for power in (4, 6):
        left_moment = node_blocks[power][0] + node_blocks[power][3]
        right_moment = node_blocks[power][1] + node_blocks[power][2]
        sector_moment = left_casimir * left_moment + right_casimir * right_moment
        standardized_moments[power] = standardize(sector_moment)
    commutator = (
        standardized_moments[4] @ standardized_moments[6]
        - standardized_moments[6] @ standardized_moments[4]
    ) / (2j)
    constraints[sector] = {
        "energy": standardized_moments[4],
        "orientation": standardize(commutator),
    }


def log_trace_exponential_negative(matrix):
    eigenvalues = eigvalsh(matrix)
    minimum = np.min(eigenvalues)
    return float(-minimum + np.log(np.sum(np.exp(-(eigenvalues - minimum)))))


def pfaffian_action(theta, measure):
    exponent = -0.5 if measure == "reduced" else -1.0
    return exponent * np.log((5 + 4 * np.cos(theta)) / 9)


def effective_free_energy(theta, measure):
    orientation_amplitude = np.sin(theta)
    matter_term = np.mean(
        [
            log_trace_exponential_negative(
                values["energy"]
                - orientation_amplitude * values["orientation"]
            )
            for values in constraints.values()
        ]
    )
    return pfaffian_action(theta, measure) - matter_term


def measure_minimum(measure):
    fit = minimize_scalar(
        lambda theta: effective_free_energy(theta, measure),
        bounds=(0, np.pi),
        method="bounded",
        options={"xatol": 1e-13},
    )
    return {
        "theta": float(fit.x),
        "orientation_amplitude": float(np.sin(fit.x)),
        "free_energy": float(fit.fun),
        "free_energy_at_zero": float(effective_free_energy(0, measure)),
    }


def modular_roots(orientation_amplitude):
    roots = {}
    for sector, values in constraints.items():
        state = expm(
            -(
                values["energy"]
                - orientation_amplitude * values["orientation"]
            )
        )
        state /= np.trace(state)
        eigenvalues, eigenvectors = np.linalg.eigh(state)
        roots[sector] = (
            eigenvectors * np.sqrt(eigenvalues)
        ) @ eigenvectors.conj().T
    return roots


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


def endpoint_row(placement, state_root, first_edge, second_edge):
    if placement == "left_gns":
        return np.hstack([state_root @ first_edge, state_root @ second_edge])
    if placement == "right_gns":
        return np.hstack([first_edge @ state_root, second_edge @ state_root])
    if placement == "kms_symmetric":
        return np.hstack(
            [
                state_root @ first_edge @ state_root,
                state_root @ second_edge @ state_root,
            ]
        )
    raise ValueError(placement)


def candidate_data(placement, messenger_ratio, sign_bits, roots):
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
        endpoints = endpoint_row(placement, roots[sector], first_edge, second_edge)
        yukawa = projector_odd - endpoints @ propagator @ endpoints.conj().T
        mass_squared = yukawa @ yukawa.conj().T
        eigenvalues, eigenvectors = np.linalg.eigh(mass_squared)
        masses = np.sqrt(np.maximum(eigenvalues, 0))
        result[sector] = {
            "normalized_masses": masses / masses[-1],
            "left_eigenvectors": eigenvectors,
        }
    return result


def mass_objective(log_gap, placement, sign_bits, roots):
    messenger_ratio = 1 + np.exp(float(log_gap))
    data = candidate_data(placement, messenger_ratio, sign_bits, roots)
    prediction = np.concatenate(
        [data["u"]["normalized_masses"][:2], data["d"]["normalized_masses"][:2]]
    )
    target = np.concatenate(
        [mass_targets["u"][:2], mass_targets["d"][:2]]
    )
    if np.any(prediction <= 0):
        return 1e9
    return float(np.sqrt(np.mean(np.log(prediction / target) ** 2)))


measure_rows = []
for measure in ("reduced", "full_ko6"):
    minimum = measure_minimum("reduced" if measure == "reduced" else "full")
    branch_rows = []
    for orientation_sign in (-1, 1):
        roots = modular_roots(
            orientation_sign * minimum["orientation_amplitude"]
        )
        for placement in ("left_gns", "right_gns", "kms_symmetric"):
            sign_rows = []
            for sign_bits in itertools.product((-1, 1), repeat=4):
                fit = differential_evolution(
                    lambda value: mass_objective(
                        value[0], placement, sign_bits, roots
                    ),
                    [(-10, 15)],
                    seed=1729,
                    tol=1e-9,
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
            branch_rows.append(
                {
                    "orientation_sign": orientation_sign,
                    "placement": placement,
                    **sign_rows[0],
                }
            )
    branch_rows.sort(key=lambda row: row["mass_log_rms"])
    best = branch_rows[0]
    roots = modular_roots(
        best["orientation_sign"] * minimum["orientation_amplitude"]
    )
    data = candidate_data(
        best["placement"], best["messenger_ratio"], best["sign_bits"], roots
    )
    ckm = data["u"]["left_eigenvectors"].conj().T @ data["d"][
        "left_eigenvectors"
    ]
    ckm_absolute = np.abs(ckm)
    ckm_angles = np.array(
        [ckm_absolute[0, 1], ckm_absolute[1, 2], ckm_absolute[0, 2]]
    )
    jarlskog = np.imag(
        ckm[0, 0]
        * ckm[1, 1]
        * np.conj(ckm[0, 1])
        * np.conj(ckm[1, 0])
    )
    mass_errors = {}
    for sector in ("u", "d"):
        ratios = data[sector]["normalized_masses"][:2] / mass_targets[sector][:2]
        mass_errors[sector] = np.maximum(ratios, 1 / ratios).tolist()
    measure_rows.append(
        {
            "measure": measure,
            "pfaffian_curvature": 2 / 9 if measure == "reduced" else 4 / 9,
            "local_effective_g": 9 / 2 if measure == "reduced" else 9 / 4,
            "minimum": minimum,
            "best": best,
            "normalized_masses": {
                sector: data[sector]["normalized_masses"].tolist()
                for sector in ("u", "d", "e", "nu")
            },
            "mass_multiplicative_errors": mass_errors,
            "ckm_absolute": ckm_absolute.tolist(),
            "ckm_angles": ckm_angles.tolist(),
            "ckm_angle_ratios": (ckm_angles / ckm_target).tolist(),
            "jarlskog": float(jarlskog),
            "absolute_jarlskog_ratio": abs(jarlskog) / ckm_jarlskog_target,
        }
    )

output = {
    "gate": "version4_pfaffian_stiffness",
    "reduced_pfaffian_modulus_squared": "(5+4 cos theta)/4",
    "normalized_periodic_action": {
        "reduced": "-1/2 log((5+4 cos theta)/9)",
        "full_ko6": "-log((5+4 cos theta)/9)",
    },
    "critical_g": 1.4799586083653407,
    "measure_rows": measure_rows,
    "local_quadratic_extrapolation_allowed": False,
    "mass_train_pass": False,
    "ckm_blind_pass": False,
    "verdict": "Pfaffian curvature is supercritical and produces a periodic orientation minimum, but neither reduced nor full measure closes blind flavour",
}

with open(
    "s2t_v4_pfaffian_stiffness_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))