import contextlib
import io
import json
import runpy

import numpy as np
from scipy.optimize import minimize_scalar


namespace_output = io.StringIO()
with contextlib.redirect_stdout(namespace_output):
    affine_namespace = runpy.run_path(
        "s2t_v4_affine_modular_temperature_gate.py"
    )

projector_odd = affine_namespace["projector_odd"]
mass_targets = affine_namespace["mass_targets"]
ckm_target = affine_namespace["ckm_target"]
ckm_jarlskog_target = affine_namespace["ckm_jarlskog_target"]
dirac_plus = affine_namespace["dirac_plus"]
casimir_endpoints = affine_namespace["casimir_endpoints"]


def node_moments(power):
    moment = np.linalg.matrix_power(dirac_plus, power)
    return [
        moment[
            3 * node : 3 * node + 3,
            3 * node : 3 * node + 3,
        ].real
        for node in range(4)
    ]


def standardized_sector_moment(power, sector):
    blocks = node_moments(power)
    left_casimir, right_casimir = casimir_endpoints[sector]
    operator = left_casimir * (blocks[0] + blocks[3]) + right_casimir * (
        blocks[1] + blocks[2]
    )
    centered = operator - np.trace(operator) * np.eye(3) / 3
    norm = np.sqrt(np.trace(centered @ centered).real / 3)
    return centered / norm


moment_powers = (4, 6, 8)
standardized_moments = {
    sector: [
        standardized_sector_moment(power, sector) for power in moment_powers
    ]
    for sector in casimir_endpoints
}

moment_gram = sum(
    np.array(
        [
            [np.trace(first @ second).real / 3 for second in moments]
            for first in moments
        ]
    )
    for moments in standardized_moments.values()
) / len(standardized_moments)

gram_eigenvalues, gram_eigenvectors = np.linalg.eigh(moment_gram)
for mode in range(3):
    column = gram_eigenvectors[:, mode]
    pivot = int(np.argmax(np.abs(column)))
    if column[pivot] < 0:
        gram_eigenvectors[:, mode] *= -1

spectral_masses = np.sqrt(gram_eigenvalues / gram_eigenvalues[0])
eigenmode_operators = {}
sector_mode_norms = {}
for sector, moments in standardized_moments.items():
    modes = []
    norms = []
    for mode in range(3):
        operator = sum(
            gram_eigenvectors[index, mode] * moments[index]
            for index in range(3)
        ) / np.sqrt(gram_eigenvalues[mode])
        modes.append(operator)
        norms.append(float(np.trace(operator @ operator).real / 3))
    eigenmode_operators[sector] = modes
    sector_mode_norms[sector] = norms


oriented_cycle = np.array(
    [
        [0.0, 1.0, -1.0],
        [-1.0, 0.0, 1.0],
        [1.0, -1.0, 0.0],
    ]
)


def positivity_threshold(orientation_sign):
    inverse_root = np.diag(1 / np.sqrt(spectral_masses))
    normalized_cycle = (
        inverse_root
        @ (orientation_sign * 1j * oriented_cycle)
        @ inverse_root
    )
    return max(0.0, -float(np.linalg.eigvalsh(normalized_cycle)[0]))


def candidate_data(messenger_scale, orientation_sign):
    channel_block = messenger_scale * np.diag(spectral_masses) + (
        orientation_sign * 1j * oriented_cycle
    )
    propagator = np.kron(np.linalg.inv(channel_block), np.eye(3))
    result = {}
    for sector, modes in eigenmode_operators.items():
        endpoints = np.hstack(modes)
        yukawa = projector_odd - endpoints @ propagator @ endpoints.conj().T
        mass_squared = yukawa @ yukawa.conj().T
        eigenvalues, eigenvectors = np.linalg.eigh(mass_squared)
        masses = np.sqrt(np.maximum(eigenvalues, 0))
        result[sector] = {
            "normalized_masses": masses / masses[-1],
            "left_eigenvectors": eigenvectors,
        }
    return result


def mass_objective(log_gap, orientation_sign):
    messenger_scale = positivity_threshold(orientation_sign) + np.exp(
        float(log_gap)
    )
    data = candidate_data(messenger_scale, orientation_sign)
    prediction = np.concatenate(
        [data["u"]["normalized_masses"][:2], data["d"]["normalized_masses"][:2]]
    )
    target = np.concatenate([mass_targets["u"][:2], mass_targets["d"][:2]])
    if np.any(prediction <= 0):
        return 1e9
    return float(np.sqrt(np.mean(np.log(prediction / target) ** 2)))


orientation_rows = []
for orientation_sign in (-1, 1):
    fit = minimize_scalar(
        lambda log_gap: mass_objective(log_gap, orientation_sign),
        bounds=(-12, 20),
        method="bounded",
        options={"xatol": 1e-12},
    )
    orientation_rows.append(
        {
            "orientation_sign": orientation_sign,
            "messenger_scale": float(
                positivity_threshold(orientation_sign) + np.exp(float(fit.x))
            ),
            "mass_log_rms": float(fit.fun),
        }
    )

orientation_rows.sort(key=lambda row: row["mass_log_rms"])
best = orientation_rows[0]
best_data = candidate_data(best["messenger_scale"], best["orientation_sign"])
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
    "gate": "version4_gram_eigenvector_endpoint",
    "moment_powers": list(moment_powers),
    "moment_gram": moment_gram.tolist(),
    "gram_eigenvalues": gram_eigenvalues.tolist(),
    "canonically_oriented_eigenvectors": gram_eigenvectors.tolist(),
    "spectral_masses": spectral_masses.tolist(),
    "sector_mode_norms": sector_mode_norms,
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
    "s2t_v4_gram_eigenvector_endpoint_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))