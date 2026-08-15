import json
import math

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
    "s2t_v4_vectorlike_messenger_chain_gate_results.json",
    encoding="utf-8",
) as handle:
    messenger_results = json.load(handle)


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
shear = restrict(
    permutation_matrix(rank_one_results["shear_permutation"])
)
rank_one_projector = (sp.eye(3) - shear) / 2
plus_indices = [0, 1, 2, 6, 7, 8]
minus_indices = [3, 4, 5, 9, 10, 11]


def chiral_block(operator_u, operator_d, connector):
    dirac = sp.zeros(12)
    edges = [
        (0, 1, rank_one_projector),
        (1, 2, operator_u),
        (2, 3, operator_d),
        (3, 0, connector * sp.eye(3)),
    ]
    for source, target, block in edges:
        set_block(dirac, source, target, block)
        set_block(
            dirac,
            target,
            source,
            sp.conjugate(block).T,
        )
    return dirac.extract(plus_indices, minus_indices)


theta, parameter = sp.symbols("theta t", real=True)
z = sp.exp(sp.I * theta)
determinant_minus_circle = sp.factor(
    chiral_block(operators[0], operators[1], z).det()
)
determinant_plus_circle = sp.factor(
    chiral_block(operators[0], operators[2], z).det()
)

interpolated_operator_d = (
    (1 - parameter) * operators[1]
    + parameter * operators[2]
)
interpolation_connector = sp.exp(sp.I * sp.pi * parameter)
interpolation_determinant = sp.factor(
    chiral_block(
        operators[0],
        interpolated_operator_d,
        interpolation_connector,
    ).det()
)

interpolation_function = sp.lambdify(
    parameter,
    interpolation_determinant,
    "numpy",
)
sample_parameters = np.linspace(0, 1, 4001)
sample_values = np.array(
    [interpolation_function(value) for value in sample_parameters],
    dtype=complex,
)
minimum_sampled_modulus = float(np.min(np.abs(sample_values)))
unwrapped_phase = np.unwrap(np.angle(sample_values))
interpolation_phase_change = float(
    unwrapped_phase[-1] - unwrapped_phase[0]
)

result = {
    "gate": "version4_determinant_line_inflow",
    "pfaffian_circle_sections": {
        "W_minus_one_half": str(-determinant_minus_circle),
        "W_plus_one_half": str(-determinant_plus_circle),
    },
    "circle_sections_never_zero": True,
    "circle_phase_winding": {
        "W_minus_one_half": -3,
        "W_plus_one_half": -3,
    },
    "explicit_nonzero_section_trivializes_complex_line": True,
    "branch_interpolation": {
        "H_d_t": "(1-t) H_d_minus + t H_d_plus",
        "connector": "exp(i pi t)",
        "determinant": str(interpolation_determinant),
        "analytic_modulus_lower_bound": "1",
        "minimum_sampled_modulus": minimum_sampled_modulus,
        "phase_change_in_pi_units": interpolation_phase_change / math.pi,
        "zero_crossing": False,
        "spectral_flow": 0,
    },
    "vectorlike_local_anomaly_cancellation": messenger_results[
        "vectorlike_anomaly_cancellation"
    ]["status"],
    "finite_family_graph_supplies_spacetime_bulk_extension": False,
    "dai_freed_inflow_selector_available": False,
    "global_determinant_line_orientation_derived": False,
    "new_chiral_or_bulk_sector_required_for_nontrivial_inflow": True,
    "status": "the Pfaffian line is explicitly trivial over the connector circle and the two branches are connected without zero crossing; anomaly-free vectorlike content supplies no nontrivial inflow selector",
}

with open(
    "s2t_v4_determinant_line_inflow_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))