import itertools
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


points = [(0, 0), (0, 1), (1, 0), (1, 1)]
sector_name = {(0, 0): "e", (0, 1): "nu", (1, 0): "d", (1, 1): "u"}
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


edge_operators = {}
edge_rows = []
for row in square_results["selected_operators"]:
    permutation = row["permutations"][0]
    moved = [index for index, target in enumerate(permutation) if index != target]
    first, second = points[moved[0]], points[moved[1]]
    lepton = first if first[0] == 0 else second
    quark = second if second[0] == 1 else first
    edge_operators[(lepton[1], quark[1])] = np.array(
        restrict(permutation_matrix(permutation)), dtype=float
    )
    edge_rows.append(
        {
            "lepton_sector": sector_name[lepton],
            "quark_sector": sector_name[quark],
            "permutation": permutation,
        }
    )

shear = restrict(
    permutation_matrix(rank_one_results["shear_permutation"])
)
projector_odd = np.array((sp.eye(3) - shear) / 2, dtype=float)

base_operator_up = edge_operators[(1, 1)]
base_operator_down = edge_operators[(0, 0)]
dirac_plus = sp.zeros(12)
for source, target, block in (
    (0, 1, sp.Matrix(projector_odd)),
    (1, 2, sp.Matrix(base_operator_up)),
    (2, 3, sp.Matrix(base_operator_down)),
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


def incidence_operators(sign_bits):
    signs = np.array(sign_bits).reshape(2, 2)
    return {
        "e": -(
            signs[0, 0] * edge_operators[(0, 0)]
            + signs[0, 1] * edge_operators[(0, 1)]
        )
        / 2,
        "nu": -(
            signs[1, 0] * edge_operators[(1, 0)]
            + signs[1, 1] * edge_operators[(1, 1)]
        )
        / 2,
        "d": (
            signs[0, 0] * edge_operators[(0, 0)]
            + signs[1, 0] * edge_operators[(1, 0)]
        )
        / 2,
        "u": (
            signs[0, 1] * edge_operators[(0, 1)]
            + signs[1, 1] * edge_operators[(1, 1)]
        )
        / 2,
    }


def state_projection(state, matrix):
    complement = np.eye(3) - state
    return matrix - complement @ matrix @ complement


def candidate_data(ratio, sign_bits):
    incidence = incidence_operators(sign_bits)
    result = {}
    for sector in weights:
        family_operator = reduced[sector, 4] - ratio * reduced[sector, 2]
        _, family_eigenvectors = np.linalg.eigh(family_operator)
        ground_vector = family_eigenvectors[:, 0]
        state = np.outer(ground_vector, ground_vector)
        yukawa = projector_odd + 1j * state_projection(
            state, incidence[sector]
        )
        mass = yukawa @ yukawa.conj().T
        mass_eigenvalues, mass_eigenvectors = np.linalg.eigh(mass)
        masses = np.sqrt(np.maximum(mass_eigenvalues, 0))
        result[sector] = {
            "normalized_masses": masses / masses[-1],
            "mass_eigenvectors": mass_eigenvectors,
        }
    return result


mass_targets = {
    "u": np.array([1.2521739130434784e-5, 0.0073623188405797105, 1.0]),
    "d": np.array([0.0011172248803827751, 0.022344497607655507, 1.0]),
}
ckm_target = np.array([0.22501, 0.04183, 0.003732])
ckm_jarlskog_target = 3.12e-5


def mass_objective(ratio, sign_bits):
    data = candidate_data(float(ratio), sign_bits)
    prediction = np.concatenate(
        [data["u"]["normalized_masses"][:2], data["d"]["normalized_masses"][:2]]
    )
    target = np.concatenate(
        [mass_targets["u"][:2], mass_targets["d"][:2]]
    )
    if np.any(prediction <= 0):
        return 1e9
    return float(np.sqrt(np.mean(np.log(prediction / target) ** 2)))


scan_grid = np.unique(
    np.concatenate([np.linspace(0, 100, 5001), np.logspace(-5, 6, 2500)])
)
rows = []
for sign_bits in itertools.product((-1, 1), repeat=4):
    scan_values = np.array(
        [mass_objective(value, sign_bits) for value in scan_grid]
    )
    best_indices = np.argsort(scan_values)[:10]
    best_fit = None
    for index in best_indices:
        center = scan_grid[index]
        width = max(0.05, center * 0.02)
        fit = minimize_scalar(
            lambda ratio: mass_objective(ratio, sign_bits),
            bounds=(max(0, center - width), center + width),
            method="bounded",
        )
        if best_fit is None or fit.fun < best_fit.fun:
            best_fit = fit
    rows.append(
        {
            "sign_bits": sign_bits,
            "trained_ratio": float(best_fit.x),
            "mass_log_rms": float(best_fit.fun),
        }
    )

rows.sort(key=lambda row: row["mass_log_rms"])
selected = rows[0]
selected_data = candidate_data(
    selected["trained_ratio"], selected["sign_bits"]
)
prediction = np.concatenate(
    [
        selected_data["u"]["normalized_masses"][:2],
        selected_data["d"]["normalized_masses"][:2],
    ]
)
target = np.concatenate(
    [mass_targets["u"][:2], mass_targets["d"][:2]]
)
mass_errors = np.maximum(prediction / target, target / prediction)

mixing = (
    selected_data["u"]["mass_eigenvectors"].conj().T
    @ selected_data["d"]["mass_eigenvectors"]
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

result = {
    "gate": "version4_sector_torsor_incidence",
    "sector_torsor": {
        "e": [0, 0],
        "nu": [0, 1],
        "d": [1, 0],
        "u": [1, 1],
    },
    "selected_transposition_edges": edge_rows,
    "selected_graph_is_K22": bool(len(edge_rows) == 4),
    "incidence_sign_menu_size": 16,
    "degree_normalization": "1/2",
    "train_data": "four light quark mass ratios",
    "blind_data": "CKM angles and Jarlskog invariant",
    "selected_sign_bits": list(selected["sign_bits"]),
    "trained_ratio": selected["trained_ratio"],
    "mass_log_rms": selected["mass_log_rms"],
    "mass_predictions": prediction.tolist(),
    "mass_multiplicative_errors": mass_errors.tolist(),
    "maximum_mass_multiplicative_error": float(np.max(mass_errors)),
    "quark_absolute_mixing": [
        [round(float(value), 12) for value in row]
        for row in absolute_mixing
    ],
    "quark_angles": angles.tolist(),
    "quark_angle_ratios": (angles / ckm_target).tolist(),
    "quark_jarlskog": float(jarlskog),
    "absolute_jarlskog_ratio": float(
        abs(jarlskog) / ckm_jarlskog_target
    ),
    "mass_train_pass": bool(np.max(mass_errors) <= 5),
    "ckm_blind_pass": bool(
        np.all(np.maximum(angles / ckm_target, ckm_target / angles) <= 5)
        and 0.2 <= abs(jarlskog) / ckm_jarlskog_target <= 5
    ),
    "status": (
        "the four transposition minima form a canonical sector K2,2, but "
        "every mass-trained oriented-incidence branch fails hierarchy and "
        "the selected branch predicts order-one CKM mixing"
    ),
}

assert result["selected_graph_is_K22"]
assert not result["mass_train_pass"]
assert not result["ckm_blind_pass"]

with open(
    "s2t_v4_sector_torsor_incidence_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))