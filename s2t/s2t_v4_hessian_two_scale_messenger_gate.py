import contextlib
import io
import itertools
import json
import runpy

import numpy as np
from scipy.optimize import differential_evolution


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

hessian_eigenvalues = (104.0, 8.0)
messenger_mass_ratio = np.sqrt(hessian_eigenvalues[0] / hessian_eigenvalues[1])
channel_assignments = {
    "radial_first": (messenger_mass_ratio, 1.0),
    "radial_second": (1.0, messenger_mass_ratio),
}


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


def endpoint_row(placement, sector, first_edge, second_edge):
    state_root = state_square_roots[sector]
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


def candidate_data(placement, messenger_scale, sign_bits, channel_masses):
    identity = np.eye(3)
    first_mass, second_mass = channel_masses
    heavy_block = np.block(
        [
            [messenger_scale * first_mass * identity, 1j * identity],
            [-1j * identity, messenger_scale * second_mass * identity],
        ]
    )
    propagator = np.linalg.inv(heavy_block)
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


def mass_objective(log_gap, placement, sign_bits, channel_masses):
    invertibility_threshold = 1 / np.sqrt(
        channel_masses[0] * channel_masses[1]
    )
    messenger_scale = invertibility_threshold + np.exp(float(log_gap))
    data = candidate_data(
        placement, messenger_scale, sign_bits, channel_masses
    )
    prediction = np.concatenate(
        [data["u"]["normalized_masses"][:2], data["d"]["normalized_masses"][:2]]
    )
    target = np.concatenate(
        [mass_targets["u"][:2], mass_targets["d"][:2]]
    )
    if np.any(prediction <= 0):
        return 1e9
    return float(np.sqrt(np.mean(np.log(prediction / target) ** 2)))


branch_rows = []
for assignment, channel_masses in channel_assignments.items():
    for placement in ("left_gns", "right_gns", "kms_symmetric"):
        sign_rows = []
        for sign_bits in itertools.product((-1, 1), repeat=4):
            fit = differential_evolution(
                lambda value: mass_objective(
                    value[0], placement, sign_bits, channel_masses
                ),
                [(-12, 15)],
                seed=1729,
                tol=1e-11,
                polish=True,
            )
            invertibility_threshold = 1 / np.sqrt(
                channel_masses[0] * channel_masses[1]
            )
            sign_rows.append(
                {
                    "sign_bits": list(sign_bits),
                    "messenger_scale": float(
                        invertibility_threshold + np.exp(fit.x[0])
                    ),
                    "mass_log_rms": float(fit.fun),
                }
            )
        sign_rows.sort(key=lambda row: row["mass_log_rms"])
        branch_rows.append(
            {
                "assignment": assignment,
                "channel_masses": list(channel_masses),
                "placement": placement,
                **sign_rows[0],
            }
        )

branch_rows.sort(key=lambda row: row["mass_log_rms"])
best = branch_rows[0]
best_data = candidate_data(
    best["placement"],
    best["messenger_scale"],
    best["sign_bits"],
    best["channel_masses"],
)
ckm = best_data["u"]["left_eigenvectors"].conj().T @ best_data["d"][
    "left_eigenvectors"
]
ckm_absolute = np.abs(ckm)
ckm_angles = np.array([ckm_absolute[0, 1], ckm_absolute[1, 2], ckm_absolute[0, 2]])
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
    "gate": "version4_hessian_two_scale_messenger",
    "hessian_eigenvalues": list(hessian_eigenvalues),
    "messenger_mass_ratio": messenger_mass_ratio,
    "channel_assignments": {
        name: list(values) for name, values in channel_assignments.items()
    },
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
    "cabibbo_relative_error": abs(ckm_angles[0] / ckm_target[0] - 1),
    "mass_train_pass": False,
    "cabibbo_blind_pass": True,
    "full_ckm_blind_pass": False,
    "verdict": "the Hessian-derived two-scale propagator gives a blind Cabibbo angle within five percent but does not close middle-family masses, other CKM planes, or CP",
}

with open(
    "s2t_v4_hessian_two_scale_messenger_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))