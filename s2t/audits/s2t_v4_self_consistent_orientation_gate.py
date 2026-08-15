import json

import numpy as np
import sympy as sp
from scipy.linalg import eigvalsh
from scipy.optimize import minimize_scalar


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
    "s2t_v4_affine_modular_temperature_gate_results.json",
    encoding="utf-8",
) as handle:
    affine_results = json.load(handle)


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


def effective_free_energy(order_parameter, stiffness=1.0):
    matter_term = np.mean(
        [
            log_trace_exponential_negative(
                values["energy"] - order_parameter * values["orientation"]
            )
            for values in constraints.values()
        ]
    )
    return order_parameter**2 / (2 * stiffness) - matter_term


scan_grid = np.linspace(-8, 8, 16001)
scan_values = np.array([effective_free_energy(value) for value in scan_grid])
best_indices = np.argsort(scan_values)[:20]
fits = []
for index in best_indices:
    center = scan_grid[index]
    fit = minimize_scalar(
        effective_free_energy,
        bounds=(max(-8, center - 0.02), min(8, center + 0.02)),
        method="bounded",
    )
    fits.append((float(fit.fun), float(fit.x)))
fits.sort()
minimum_value, minimum_order_parameter = fits[0]

step = 1e-4
curvature_at_zero = (
    effective_free_energy(step)
    - 2 * effective_free_energy(0)
    + effective_free_energy(-step)
) / step**2
orientation_susceptibility = 1 - curvature_at_zero
critical_stiffness = 1 / orientation_susceptibility

evenness_residual = max(
    abs(effective_free_energy(value) - effective_free_energy(-value))
    for value in np.linspace(0, 8, 1001)
)

output = {
    "gate": "version4_self_consistent_orientation",
    "free_energy": "Phi_g(alpha)=alpha^2/(2g)-1/4 sum_s log Tr exp[-(Z4_s-alpha K_s)]",
    "canonical_stiffness": 1.0,
    "minimum_order_parameter": minimum_order_parameter,
    "minimum_value": minimum_value,
    "curvature_at_zero": curvature_at_zero,
    "orientation_susceptibility": orientation_susceptibility,
    "critical_stiffness": critical_stiffness,
    "evenness_residual": evenness_residual,
    "unique_zero_minimum_on_scan": abs(minimum_order_parameter) < 1e-6,
    "fallback_affine_branch": {
        "best": affine_results["best"],
        "normalized_masses": affine_results["normalized_masses"],
        "ckm_angles": affine_results["ckm_angles"],
        "jarlskog_absolute": affine_results["jarlskog_absolute"],
    },
    "verdict": "canonical self-consistent orientation field remains uncondensed; nonzero CP requires a derived stiffness above the critical value",
}

with open(
    "s2t_v4_self_consistent_orientation_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))