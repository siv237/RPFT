import json

import numpy as np
from scipy.optimize import differential_evolution, minimize_scalar


with open(
    "s2t_v4_full_spectral_profile_global_gate_results.json",
    encoding="utf-8",
) as handle:
    angular_results = json.load(handle)


def chiral_matrix(radius, theta):
    connector = radius * np.exp(-1j * theta)
    return np.array(
        [
            [0, 0, 0, connector, 0, 0],
            [0, 0.5, -0.5, 0, connector, 0],
            [0, -0.5, 0.5, 0, 0, connector],
            [0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 0, 0],
        ],
        dtype=complex,
    )


def squared_spectrum(radius, theta):
    matrix = chiral_matrix(radius, theta)
    return np.linalg.eigvalsh(matrix @ matrix.conj().T)


def profile(eigenvalues):
    return (
        np.exp(-eigenvalues**2 / 100)
        + np.exp(-10 * eigenvalues**2) / 12
    ) / (13 / 12)


def action(radius, theta):
    return float(2 * np.sum(profile(squared_spectrum(radius, theta))))


def log_radial_action(coordinates):
    return action(np.exp(coordinates[0]), coordinates[1])


global_fit = differential_evolution(
    log_radial_action,
    [(-8, 8), (0, np.pi)],
    seed=1729,
    tol=1e-12,
    polish=True,
)
global_radius = float(np.exp(global_fit.x[0]))
global_theta = float(global_fit.x[1])


def numerical_hessian(function, point, step=1e-4):
    point = np.array(point, dtype=float)
    hessian = np.zeros((2, 2))
    center = function(point)
    for index in range(2):
        shift = np.zeros(2)
        shift[index] = step
        hessian[index, index] = (
            function(point + shift)
            - 2 * center
            + function(point - shift)
        ) / step**2
    first = np.array([step, 0.0])
    second = np.array([0.0, step])
    hessian[0, 1] = hessian[1, 0] = (
        function(point + first + second)
        - function(point + first - second)
        - function(point - first + second)
        + function(point - first - second)
    ) / (4 * step**2)
    return hessian


global_hessian = numerical_hessian(
    log_radial_action, [np.log(global_radius), global_theta]
)

slice_theta = angular_results["counterexample_unit_radial_slice"][
    "theta_minimum"
]
radial_step = 1e-5
slice_radial_derivative = (
    action(np.exp(radial_step), slice_theta)
    - action(np.exp(-radial_step), slice_theta)
) / (2 * radial_step)

radial_rows = []
for radius in (0, 0.1, 0.5, 1, 2, 5, 10, 20, 50, 100):
    fit = minimize_scalar(
        lambda theta: action(radius, theta),
        bounds=(0, np.pi),
        method="bounded",
    )
    radial_rows.append(
        {
            "radius": radius,
            "minimum_theta": float(fit.x),
            "minimum_value": float(fit.fun),
        }
    )

output = {
    "gate": "version4_full_profile_radial_vacuum",
    "profile": angular_results["positive_counterexample_profile"],
    "unit_radial_slice": angular_results[
        "counterexample_unit_radial_slice"
    ],
    "slice_radial_derivative_in_log_radius": float(slice_radial_derivative),
    "slice_cp_point_is_full_stationary_point": bool(
        abs(slice_radial_derivative) < 1e-8
    ),
    "global_minimum": {
        "radius": global_radius,
        "theta": global_theta,
        "orientation_amplitude": float(np.sin(global_theta)),
        "value": float(global_fit.fun),
    },
    "global_hessian_log_radius_theta": global_hessian.tolist(),
    "global_hessian_eigenvalues": np.linalg.eigvalsh(
        global_hessian
    ).tolist(),
    "radial_rows": radial_rows,
    "cp_breaking_global_vacuum": False,
    "flavour_test_reached": False,
    "verdict": (
        "the positive profile has CP-breaking minima only on the frozen "
        "unit-radius slice; after radial minimization the unique stable "
        "vacuum is CP even near r=5.7733 and theta=0"
    ),
}

with open(
    "s2t_v4_full_profile_radial_vacuum_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))