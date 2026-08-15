import contextlib
import io
import itertools
import json
import runpy

import numpy as np
from scipy.optimize import minimize_scalar


namespace_output = io.StringIO()
with contextlib.redirect_stdout(namespace_output):
    affine_namespace = runpy.run_path(
        "s2t_v4_affine_modular_temperature_gate.py"
    )

edge_operators = affine_namespace["edge_operators"]
projector_odd = affine_namespace["projector_odd"]
state_square_roots = affine_namespace["state_square_roots"]
mass_targets = affine_namespace["mass_targets"]
ckm_target = affine_namespace["ckm_target"]
ckm_jarlskog_target = affine_namespace["ckm_jarlskog_target"]
dirac_plus = affine_namespace["dirac_plus"]
casimir_endpoints = affine_namespace["casimir_endpoints"]


def node_moments(power):
    dirac_moment = np.linalg.matrix_power(dirac_plus, power)
    return [
        dirac_moment[
            3 * node : 3 * node + 3,
            3 * node : 3 * node + 3,
        ].real
        for node in range(4)
    ]


def standardized_sector_moment(power, sector):
    blocks = node_moments(power)
    left_casimir, right_casimir = casimir_endpoints[sector]
    parent = left_casimir * (blocks[0] + blocks[3]) + right_casimir * (
        blocks[1] + blocks[2]
    )
    centered = parent - np.trace(parent) * np.eye(3) / 3
    norm = np.sqrt(np.trace(centered @ centered).real / 3)
    return centered / norm


moment_powers = (4, 6, 8)
standardized_moments = {
    sector: [
        standardized_sector_moment(power, sector) for power in moment_powers
    ]
    for sector in casimir_endpoints
}

sector_gram_matrices = {}
for sector, moments in standardized_moments.items():
    sector_gram_matrices[sector] = np.array(
        [
            [np.trace(first @ second).real / 3 for second in moments]
            for first in moments
        ]
    )

moment_gram = sum(sector_gram_matrices.values()) / len(sector_gram_matrices)
gram_eigenvalues, gram_eigenvectors = np.linalg.eigh(moment_gram)
spectral_masses = np.sqrt(gram_eigenvalues / gram_eigenvalues[0])


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


def normalized_commutator(first_edge, second_edge):
    commutator = (first_edge @ second_edge - second_edge @ first_edge) / (2j)
    norm = np.sqrt(np.trace(commutator @ commutator).real / 3)
    return commutator / norm


def endpoint_row(placement, sector, first_edge, second_edge):
    third_edge = normalized_commutator(first_edge, second_edge)
    state_root = state_square_roots[sector]
    channels = (first_edge, second_edge, third_edge)
    if placement == "left_gns":
        return np.hstack([state_root @ channel for channel in channels])
    if placement == "right_gns":
        return np.hstack([channel @ state_root for channel in channels])
    if placement == "kms_symmetric":
        return np.hstack(
            [state_root @ channel @ state_root for channel in channels]
        )
    raise ValueError(placement)


oriented_cycle = np.array(
    [
        [0.0, 1.0, -1.0],
        [-1.0, 0.0, 1.0],
        [1.0, -1.0, 0.0],
    ]
)


def positivity_threshold(channel_masses, orientation_sign):
    inverse_root = np.diag(1 / np.sqrt(channel_masses))
    normalized_cycle = (
        inverse_root
        @ (orientation_sign * 1j * oriented_cycle)
        @ inverse_root
    )
    return max(0.0, -float(np.linalg.eigvalsh(normalized_cycle)[0]))


def candidate_data(
    placement,
    messenger_scale,
    sign_bits,
    channel_masses,
    orientation_sign,
):
    channel_block = messenger_scale * np.diag(channel_masses) + (
        orientation_sign * 1j * oriented_cycle
    )
    propagator = np.kron(np.linalg.inv(channel_block), np.eye(3))
    result = {}
    for sector, (first_edge, second_edge) in signed_sector_pairs(sign_bits).items():
        endpoints = endpoint_row(placement, sector, first_edge, second_edge)
        yukawa = projector_odd - endpoints @ propagator @ endpoints.conj().T
        mass_squared = yukawa @ yukawa.conj().T
        eigenvalues, eigenvectors = np.linalg.eigh(mass_squared)
        masses = np.sqrt(np.maximum(eigenvalues, 0))
        result[sector] = {
            "normalized_masses": masses / masses[-1],
            "left_eigenvectors": eigenvectors,
        }
    return result


def mass_objective(
    log_gap,
    placement,
    sign_bits,
    channel_masses,
    orientation_sign,
):
    threshold = positivity_threshold(channel_masses, orientation_sign)
    messenger_scale = threshold + np.exp(float(log_gap))
    data = candidate_data(
        placement,
        messenger_scale,
        sign_bits,
        channel_masses,
        orientation_sign,
    )
    prediction = np.concatenate(
        [data["u"]["normalized_masses"][:2], data["d"]["normalized_masses"][:2]]
    )
    target = np.concatenate([mass_targets["u"][:2], mass_targets["d"][:2]])
    if np.any(prediction <= 0):
        return 1e9
    return float(np.sqrt(np.mean(np.log(prediction / target) ** 2)))


branch_rows = []
for assignment in itertools.permutations(spectral_masses):
    channel_masses = np.array(assignment)
    for placement in ("left_gns", "right_gns", "kms_symmetric"):
        for orientation_sign in (-1, 1):
            sign_rows = []
            for sign_bits in itertools.product((-1, 1), repeat=4):
                fit = minimize_scalar(
                    lambda log_gap: mass_objective(
                        log_gap,
                        placement,
                        sign_bits,
                        channel_masses,
                        orientation_sign,
                    ),
                    bounds=(-12, 18),
                    method="bounded",
                    options={"xatol": 1e-11},
                )
                threshold = positivity_threshold(
                    channel_masses, orientation_sign
                )
                sign_rows.append(
                    {
                        "sign_bits": list(sign_bits),
                        "messenger_scale": float(
                            threshold + np.exp(float(fit.x))
                        ),
                        "mass_log_rms": float(fit.fun),
                    }
                )
            sign_rows.sort(key=lambda row: row["mass_log_rms"])
            branch_rows.append(
                {
                    "channel_masses": channel_masses.tolist(),
                    "placement": placement,
                    "orientation_sign": orientation_sign,
                    **sign_rows[0],
                }
            )

branch_rows.sort(key=lambda row: row["mass_log_rms"])
best = branch_rows[0]
best_data = candidate_data(
    best["placement"],
    best["messenger_scale"],
    best["sign_bits"],
    np.array(best["channel_masses"]),
    best["orientation_sign"],
)
ckm = best_data["u"]["left_eigenvectors"].conj().T @ best_data["d"][
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
    ratios = best_data[sector]["normalized_masses"][:2] / mass_targets[sector][:2]
    mass_errors[sector] = np.maximum(ratios, 1 / ratios).tolist()

output = {
    "gate": "version4_three_moment_oriented_messenger",
    "moment_powers": list(moment_powers),
    "moment_gram": moment_gram.tolist(),
    "sector_gram_matrices": {
        sector: matrix.tolist()
        for sector, matrix in sector_gram_matrices.items()
    },
    "gram_eigenvalues": gram_eigenvalues.tolist(),
    "gram_eigenvectors": gram_eigenvectors.tolist(),
    "gram_rank": int(np.linalg.matrix_rank(moment_gram)),
    "gram_condition_number": float(
        gram_eigenvalues[-1] / gram_eigenvalues[0]
    ),
    "spectral_masses": spectral_masses.tolist(),
    "branch_rows": branch_rows,
    "best": best,
    "normalized_masses": {
        sector: best_data[sector]["normalized_masses"].tolist()
        for sector in ("u", "d", "e", "nu")
    },
    "mass_multiplicative_errors": mass_errors,
    "ckm_absolute": ckm_absolute.tolist(),
    "ckm_angles": ckm_angles.tolist(),
    "ckm_angle_ratios": (ckm_angles / ckm_target).tolist(),
    "jarlskog": float(jarlskog),
    "absolute_jarlskog_ratio": abs(jarlskog) / ckm_jarlskog_target,
    "mass_train_pass": bool(max(sum(mass_errors.values(), [])) < 2),
    "cabibbo_blind_pass": bool(
        abs(ckm_angles[0] / ckm_target[0] - 1) < 0.05
    ),
    "full_ckm_blind_pass": bool(
        np.max(np.maximum(ckm_angles / ckm_target, ckm_target / ckm_angles))
        < 2
    ),
}

with open(
    "s2t_v4_three_moment_oriented_messenger_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))