import json

import numpy as np
import sympy as sp


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

dirac_fourth = dirac_plus**4
node_blocks = [
    np.array(
        dirac_fourth[
            3 * node : 3 * node + 3,
            3 * node : 3 * node + 3,
        ],
        dtype=float,
    )
    for node in range(4)
]


g1_squared, g2_squared, g3_squared = sp.symbols(
    "g1_squared g2_squared g3_squared", positive=True
)
casimir_symbolic = {
    "u": (
        sp.Rational(4, 3) * g3_squared
        + sp.Rational(3, 4) * g2_squared
        + sp.Rational(1, 60) * g1_squared,
        sp.Rational(4, 3) * g3_squared
        + sp.Rational(4, 15) * g1_squared,
    ),
    "d": (
        sp.Rational(4, 3) * g3_squared
        + sp.Rational(3, 4) * g2_squared
        + sp.Rational(1, 60) * g1_squared,
        sp.Rational(4, 3) * g3_squared
        + sp.Rational(1, 15) * g1_squared,
    ),
    "nu": (
        sp.Rational(3, 4) * g2_squared
        + sp.Rational(3, 20) * g1_squared,
        sp.Integer(0),
    ),
    "e": (
        sp.Rational(3, 4) * g2_squared
        + sp.Rational(3, 20) * g1_squared,
        sp.Rational(3, 5) * g1_squared,
    ),
}

d_left, d_right = casimir_symbolic["d"]
e_left, e_right = casimir_symbolic["e"]
down_electron_split_polynomial = sp.factor(
    d_right * e_left - e_right * d_left
)

couplings = gauge_results["couplings_at_MZ"]
substitution = {
    g1_squared: couplings["g1"] ** 2,
    g2_squared: couplings["g2"] ** 2,
    g3_squared: couplings["g3"] ** 2,
}


def state_projection(state, matrix):
    complement = np.eye(3) - state
    return matrix - complement @ matrix @ complement


def sector_data(sector, left_weight, right_weight):
    reduced_operator = (
        left_weight * (node_blocks[0] + node_blocks[3])
        + right_weight * (node_blocks[1] + node_blocks[2])
    )
    reduced_eigenvalues, reduced_eigenvectors = np.linalg.eigh(
        reduced_operator
    )
    ground_vector = reduced_eigenvectors[:, 0]
    state = np.outer(ground_vector, ground_vector)
    incidence = (
        operator_up if sector in ("u", "nu") else operator_down
    )
    yukawa = projector_odd + 1j * state_projection(state, incidence)
    mass = yukawa @ yukawa.conj().T
    mass_eigenvalues, mass_eigenvectors = np.linalg.eigh(mass)
    masses = np.sqrt(np.maximum(mass_eigenvalues, 0))
    return {
        "left_weight": float(left_weight),
        "right_weight": float(right_weight),
        "right_to_left_ratio": float(right_weight / left_weight),
        "ground_vector": [round(float(value), 12) for value in ground_vector],
        "normalized_masses": [
            round(float(value / masses[-1]), 12) for value in masses
        ],
        "_mass": mass,
        "_mass_eigenvectors": mass_eigenvectors,
    }


sectors = {}
for sector, (left_symbolic, right_symbolic) in casimir_symbolic.items():
    sectors[sector] = sector_data(
        sector,
        float(left_symbolic.subs(substitution)),
        float(right_symbolic.subs(substitution)),
    )


def pair_readout(first, second):
    first_data = sectors[first]
    second_data = sectors[second]
    mixing = (
        first_data["_mass_eigenvectors"].conj().T
        @ second_data["_mass_eigenvectors"]
    )
    commutator = (
        first_data["_mass"] @ second_data["_mass"]
        - second_data["_mass"] @ first_data["_mass"]
    )
    cp_trace = np.trace(commutator @ commutator @ commutator)
    return {
        "absolute_mixing_matrix": [
            [round(float(value), 12) for value in row]
            for row in np.abs(mixing)
        ],
        "maximum_off_diagonal_entry": float(
            max(
                np.abs(mixing[row, column])
                for row in range(3)
                for column in range(3)
                if row != column
            )
        ),
        "cp_invariant_im_Tr_commutator_cube": float(cp_trace.imag),
    }


serializable_sectors = {
    sector: {
        key: value
        for key, value in data.items()
        if not key.startswith("_")
    }
    for sector, data in sectors.items()
}
ground_vectors = [
    np.array(sectors[sector]["ground_vector"]) for sector in ("u", "d", "nu", "e")
]
distinct_ground_state_count = 0
representatives = []
for vector in ground_vectors:
    if not any(
        min(np.linalg.norm(vector - item), np.linalg.norm(vector + item)) < 1e-8
        for item in representatives
    ):
        representatives.append(vector)
        distinct_ground_state_count += 1

result = {
    "gate": "version4_gauge_casimir_family_split",
    "weight_definition": "C_s=g3^2 C3+g2^2 C2+g1^2 T1^2",
    "gut_normalized_hypercharge": True,
    "casimir_weights_symbolic": {
        sector: [str(left), str(right)]
        for sector, (left, right) in casimir_symbolic.items()
    },
    "down_electron_ratio_split_polynomial": str(
        down_electron_split_polynomial
    ),
    "down_electron_degenerate_at_equal_couplings": bool(
        down_electron_split_polynomial.subs(
            {g2_squared: g1_squared, g3_squared: g1_squared}
        )
        == 0
    ),
    "coupling_source": "frozen MZ gauge-train ledger",
    "couplings": {
        key: couplings[key] for key in ("g1", "g2", "g3")
    },
    "sectors": serializable_sectors,
    "distinct_ground_state_count": distinct_ground_state_count,
    "quark_readout": pair_readout("u", "d"),
    "lepton_readout": pair_readout("nu", "e"),
    "four_sector_structural_split": bool(distinct_ground_state_count == 4),
    "quark_small_mixing_pass": bool(
        pair_readout("u", "d")["maximum_off_diagonal_entry"] < 0.3
    ),
    "blind_status": (
        "not blind: the four-way split uses measured low-scale gauge "
        "couplings and the quark mixing ledger fails"
    ),
    "status": (
        "RG-separated gauge Casimirs generate four distinct family anchors "
        "without flavour coefficients, but equal spectral couplings restore "
        "d/e degeneracy and the resulting quark readout is not viable"
    ),
}

assert result["down_electron_degenerate_at_equal_couplings"]
assert result["four_sector_structural_split"]
assert not result["quark_small_mixing_pass"]

with open(
    "s2t_v4_gauge_casimir_family_split_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))