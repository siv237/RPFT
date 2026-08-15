import contextlib
import io
import json
import runpy

import numpy as np
from scipy.optimize import minimize_scalar


namespace_output = io.StringIO()
with contextlib.redirect_stdout(namespace_output):
    linear_namespace = runpy.run_path(
        "s2t_v4_gram_eigenvector_endpoint_gate.py"
    )

projector_odd = linear_namespace["projector_odd"]
mass_targets = linear_namespace["mass_targets"]
ckm_target = linear_namespace["ckm_target"]
ckm_jarlskog_target = linear_namespace["ckm_jarlskog_target"]
spectral_masses = linear_namespace["spectral_masses"]
gram_eigenvalues = linear_namespace["gram_eigenvalues"]
gram_eigenvectors = linear_namespace["gram_eigenvectors"]
eigenmode_operators = linear_namespace["eigenmode_operators"]
oriented_cycle = linear_namespace["oriented_cycle"]


def bounded_transform(operator):
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    bounded_eigenvalues = eigenvalues / np.sqrt(1 + eigenvalues**2)
    return (eigenvectors * bounded_eigenvalues) @ eigenvectors.T


bounded_mode_operators = {
    sector: [bounded_transform(operator) for operator in operators]
    for sector, operators in eigenmode_operators.items()
}
bounded_mode_spectra = {
    sector: [np.linalg.eigvalsh(operator).tolist() for operator in operators]
    for sector, operators in bounded_mode_operators.items()
}


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
    for sector, modes in bounded_mode_operators.items():
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
    "gate": "version4_bounded_gram_endpoint",
    "bounded_transform": "b(Q)=Q(1+Q^2)^(-1/2)",
    "gram_eigenvalues": gram_eigenvalues.tolist(),
    "canonically_oriented_eigenvectors": gram_eigenvectors.tolist(),
    "spectral_masses": spectral_masses.tolist(),
    "bounded_mode_spectra": bounded_mode_spectra,
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
    "s2t_v4_bounded_gram_endpoint_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))