import json

import numpy as np
import sympy as sp
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
    "s2t_v4_spectral_gauge_normalization_gate_results.json",
    encoding="utf-8",
) as handle:
    gauge_results = json.load(handle)


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
operator_up = np.array(operators[0], dtype=float)
operator_down = np.array(operators[2], dtype=float)
shear = restrict(
    permutation_matrix(rank_one_results["shear_permutation"])
)
projector_odd = np.array((sp.eye(3) - shear) / 2, dtype=float)

dirac_plus = sp.zeros(12)
for source, target, block in (
    (0, 1, sp.Matrix(projector_odd)),
    (1, 2, operators[0]),
    (2, 3, operators[2]),
    (3, 0, -sp.eye(3)),
):
    set_block(dirac_plus, source, target, block)
    set_block(dirac_plus, target, source, block.T)

node_blocks = {}
for power in (2, 4):
    powered = dirac_plus**power
    node_blocks[power] = [
        np.array(
            powered[
                3 * node : 3 * node + 3,
                3 * node : 3 * node + 3,
            ],
            dtype=float,
        )
        for node in range(4)
    ]

couplings = gauge_results["couplings_at_MZ"]
g1_squared = couplings["g1"] ** 2
g2_squared = couplings["g2"] ** 2
g3_squared = couplings["g3"] ** 2
weights = {
    "u": (
        4 / 3 * g3_squared + 3 / 4 * g2_squared + 1 / 60 * g1_squared,
        4 / 3 * g3_squared + 4 / 15 * g1_squared,
    ),
    "d": (
        4 / 3 * g3_squared + 3 / 4 * g2_squared + 1 / 60 * g1_squared,
        4 / 3 * g3_squared + 1 / 15 * g1_squared,
    ),
    "nu": (
        3 / 4 * g2_squared + 3 / 20 * g1_squared,
        0.0,
    ),
    "e": (
        3 / 4 * g2_squared + 3 / 20 * g1_squared,
        3 / 5 * g1_squared,
    ),
}


def reduced_operator(sector, power):
    left_weight, right_weight = weights[sector]
    blocks = node_blocks[power]
    return (
        left_weight * (blocks[0] + blocks[3])
        + right_weight * (blocks[1] + blocks[2])
    )


reduced = {
    (sector, power): reduced_operator(sector, power)
    for sector in weights
    for power in (2, 4)
}


def state_projection(state, matrix):
    complement = np.eye(3) - state
    return matrix - complement @ matrix @ complement


def sector_data(sector, ratio):
    family_operator = reduced[sector, 4] - ratio * reduced[sector, 2]
    _, family_eigenvectors = np.linalg.eigh(family_operator)
    ground_vector = family_eigenvectors[:, 0]
    state = np.outer(ground_vector, ground_vector)
    incidence = (
        operator_up if sector in ("u", "nu") else operator_down
    )
    yukawa = projector_odd + 1j * state_projection(state, incidence)
    mass = yukawa @ yukawa.conj().T
    mass_eigenvalues, mass_eigenvectors = np.linalg.eigh(mass)
    masses = np.sqrt(np.maximum(mass_eigenvalues, 0))
    return {
        "normalized_masses": masses / masses[-1],
        "mass": mass,
        "mass_eigenvectors": mass_eigenvectors,
    }


def all_data(ratio):
    return {sector: sector_data(sector, ratio) for sector in weights}


mass_targets = {
    "u": np.array([1.2521739130434784e-5, 0.0073623188405797105, 1.0]),
    "d": np.array([0.0011172248803827751, 0.022344497607655507, 1.0]),
}
ckm_target = np.array([0.22501, 0.04183, 0.003732])
ckm_jarlskog_target = 3.12e-5


def mass_log_rms(ratio):
    data = all_data(float(ratio))
    prediction = np.concatenate(
        [data["u"]["normalized_masses"][:2], data["d"]["normalized_masses"][:2]]
    )
    target = np.concatenate(
        [mass_targets["u"][:2], mass_targets["d"][:2]]
    )
    if np.any(prediction <= 0):
        return 1e9
    return float(np.sqrt(np.mean(np.log(prediction / target) ** 2)))


linear_grid = np.linspace(0, 100, 10001)
log_grid = np.logspace(-5, 6, 5000)
scan_grid = np.unique(np.concatenate([linear_grid, log_grid]))
scan_values = np.array([mass_log_rms(value) for value in scan_grid])
best_indices = np.argsort(scan_values)[:30]
best_fit = None
for index in best_indices:
    center = scan_grid[index]
    width = max(0.02, center * 0.01)
    fit = minimize_scalar(
        mass_log_rms,
        bounds=(max(0, center - width), center + width),
        method="bounded",
        options={"xatol": 1e-12},
    )
    if best_fit is None or fit.fun < best_fit.fun:
        best_fit = fit

trained_ratio = float(best_fit.x)
trained_data = all_data(trained_ratio)


def mixing_readout(first, second):
    first_data = trained_data[first]
    second_data = trained_data[second]
    mixing = (
        first_data["mass_eigenvectors"].conj().T
        @ second_data["mass_eigenvectors"]
    )
    absolute_mixing = np.abs(mixing)
    sin13 = absolute_mixing[0, 2]
    cos13 = np.sqrt(1 - sin13**2)
    angles = np.array(
        [absolute_mixing[0, 1] / cos13, absolute_mixing[1, 2] / cos13, sin13]
    )
    jarlskog = np.imag(
        mixing[0, 0]
        * mixing[1, 1]
        * np.conj(mixing[0, 1])
        * np.conj(mixing[1, 0])
    )
    return absolute_mixing, angles, float(jarlskog)


quark_mixing, quark_angles, quark_jarlskog = mixing_readout("u", "d")
lepton_mixing, _, lepton_jarlskog = mixing_readout("nu", "e")
mass_predictions = {
    sector: [
        round(float(value), 12)
        for value in trained_data[sector]["normalized_masses"]
    ]
    for sector in weights
}
mass_multiplicative_errors = np.concatenate(
    [
        np.maximum(
            trained_data[sector]["normalized_masses"][:2]
            / mass_targets[sector][:2],
            mass_targets[sector][:2]
            / trained_data[sector]["normalized_masses"][:2],
        )
        for sector in ("u", "d")
    ]
)


def simultaneous_factor_score(ratio):
    data = all_data(float(ratio))
    if any(
        np.any(data[sector]["normalized_masses"][:2] <= 0)
        for sector in ("u", "d")
    ):
        return float("inf")
    mass_errors = np.concatenate(
        [
            np.maximum(
                data[sector]["normalized_masses"][:2]
                / mass_targets[sector][:2],
                mass_targets[sector][:2]
                / data[sector]["normalized_masses"][:2],
            )
            for sector in ("u", "d")
        ]
    )
    mixing = (
        data["u"]["mass_eigenvectors"].conj().T
        @ data["d"]["mass_eigenvectors"]
    )
    absolute_mixing = np.abs(mixing)
    sin13 = absolute_mixing[0, 2]
    cos13 = np.sqrt(max(1 - sin13**2, 1e-30))
    angles = np.array(
        [absolute_mixing[0, 1] / cos13, absolute_mixing[1, 2] / cos13, sin13]
    )
    angle_errors = np.maximum(angles / ckm_target, ckm_target / angles)
    return float(max(np.max(mass_errors), np.max(angle_errors)))


simultaneous_scores = np.array(
    [simultaneous_factor_score(value) for value in scan_grid]
)
simultaneous_index = int(np.argmin(simultaneous_scores))

result = {
    "gate": "version4_one_ratio_family_functional",
    "functional": "R_s(t)=R4_s-t R2_s",
    "shared_continuous_parameter_count": 1,
    "train_data": "four light up/down mass ratios only",
    "blind_data": "three CKM angles and Jarlskog invariant",
    "mass_targets": {
        sector: values.tolist() for sector, values in mass_targets.items()
    },
    "trained_ratio": trained_ratio,
    "mass_log_rms": float(best_fit.fun),
    "mass_predictions": mass_predictions,
    "mass_multiplicative_errors": [
        float(value) for value in mass_multiplicative_errors
    ],
    "maximum_mass_multiplicative_error": float(
        np.max(mass_multiplicative_errors)
    ),
    "quark_absolute_mixing": [
        [round(float(value), 12) for value in row] for row in quark_mixing
    ],
    "quark_angles": [float(value) for value in quark_angles],
    "ckm_target_angles": ckm_target.tolist(),
    "quark_angle_ratios": [
        float(value) for value in quark_angles / ckm_target
    ],
    "quark_jarlskog": quark_jarlskog,
    "ckm_target_jarlskog": ckm_jarlskog_target,
    "absolute_jarlskog_ratio": float(
        abs(quark_jarlskog) / ckm_jarlskog_target
    ),
    "lepton_absolute_mixing": [
        [round(float(value), 12) for value in row] for row in lepton_mixing
    ],
    "lepton_jarlskog": lepton_jarlskog,
    "scan_domain": "hybrid linear/log grid on [0,10^6]",
    "best_simultaneous_factor_score": float(
        simultaneous_scores[simultaneous_index]
    ),
    "best_simultaneous_ratio": float(scan_grid[simultaneous_index]),
    "factor_ten_simultaneous_candidate_exists": bool(
        np.any(simultaneous_scores <= 10)
    ),
    "mass_train_pass": bool(np.max(mass_multiplicative_errors) <= 5),
    "ckm_blind_pass": bool(
        np.all(np.maximum(quark_angles / ckm_target, ckm_target / quark_angles) <= 5)
        and 0.2 <= abs(quark_jarlskog) / ckm_jarlskog_target <= 5
    ),
    "status": (
        "a single shared quadratic/quartic ratio creates a sharp hierarchy "
        "near t=4, but mass-only training misses the middle generations and "
        "fails the blind CKM hierarchy"
    ),
}

assert not result["mass_train_pass"]
assert not result["ckm_blind_pass"]
assert not result["factor_ten_simultaneous_candidate_exists"]

with open(
    "s2t_v4_one_ratio_family_functional_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))