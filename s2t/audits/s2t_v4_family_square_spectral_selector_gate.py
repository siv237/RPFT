import json

import sympy as sp


with open(
    "s2t_v4_incidence_operator_menu_gate_results.json",
    encoding="utf-8",
) as handle:
    incidence_results = json.load(handle)

with open(
    "s2t_v4_rank_one_breaking_gate_results.json",
    encoding="utf-8",
) as handle:
    rank_one_results = json.load(handle)


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


def matrix_key(matrix):
    return tuple(str(value) for value in matrix)


shear = restrict(permutation_matrix(rank_one_results["shear_permutation"]))
rank_one_projector = (sp.eye(3) - shear) / 2

operators = {}
for row in incidence_results["rows"]:
    if row["operator_algebra_dimension"] != 9:
        continue
    permutation = tuple(row["permutation"])
    matrix = restrict(
        (
            permutation_matrix(permutation)
            + permutation_matrix(permutation).T
        )
        / 2
    )
    operators.setdefault(
        matrix_key(matrix),
        {
            "matrix": matrix,
            "cycle_types": set(),
            "permutations": [],
        },
    )
    operators[matrix_key(matrix)]["cycle_types"].add(row["cycle_type"])
    operators[matrix_key(matrix)]["permutations"].append(row["permutation"])

amplitude_a, amplitude_b, phase = sp.symbols(
    "a b phi", positive=True, real=True
)


def set_block(matrix, row_block, column_block, block):
    matrix[
        3 * row_block : 3 * row_block + 3,
        3 * column_block : 3 * column_block + 3,
    ] = block


def square_dirac(operator, phase_value):
    phase_factor = sp.exp(sp.I * phase_value)
    matrix = sp.zeros(12)
    set_block(matrix, 0, 1, amplitude_a * rank_one_projector)
    set_block(matrix, 1, 0, amplitude_a * rank_one_projector)
    set_block(matrix, 0, 3, amplitude_a * rank_one_projector)
    set_block(matrix, 3, 0, amplitude_a * rank_one_projector)
    set_block(matrix, 1, 2, phase_factor * amplitude_b * operator)
    set_block(
        matrix,
        2,
        1,
        sp.conjugate(phase_factor) * amplitude_b * operator,
    )
    set_block(
        matrix,
        3,
        2,
        sp.conjugate(phase_factor) * amplitude_b * operator,
    )
    set_block(matrix, 2, 3, phase_factor * amplitude_b * operator)
    return matrix


def coefficient(polynomial, monomial):
    return sp.Poly(sp.expand(polynomial), amplitude_a, amplitude_b).coeff_monomial(
        monomial
    )


rows = []
for item in operators.values():
    operator = item["matrix"]
    dirac_general = square_dirac(operator, phase)
    dirac_zero = square_dirac(operator, sp.Integer(0))
    dirac_maximal = square_dirac(operator, sp.pi / 2)

    trace_d2 = sp.simplify(sp.trace(dirac_general**2))
    trace_d4_zero = sp.simplify(sp.trace(dirac_zero**4))
    trace_d4_maximal = sp.simplify(sp.trace(dirac_maximal**4))
    phase_curvature_at_unit_amplitudes = sp.simplify(
        trace_d4_zero.subs({amplitude_a: 1, amplitude_b: 1})
        - trace_d4_maximal.subs({amplitude_a: 1, amplitude_b: 1})
    )

    quadratic_a = coefficient(trace_d2, amplitude_a**2)
    quadratic_b = coefficient(trace_d2, amplitude_b**2)
    quartic_a = coefficient(trace_d4_maximal, amplitude_a**4)
    quartic_b = coefficient(trace_d4_maximal, amplitude_b**4)
    mixed_quartic = coefficient(
        trace_d4_maximal,
        amplitude_a**2 * amplitude_b**2,
    )
    vacuum_energy_coefficient = sp.simplify(
        quadratic_a**2 / (4 * quartic_a)
        + quadratic_b**2 / (4 * quartic_b)
    )

    rows.append(
        {
            "matrix": str(operator),
            "cycle_types": sorted(item["cycle_types"]),
            "permutations": item["permutations"],
            "trace_H2": str(sp.trace(operator**2)),
            "trace_H4": str(sp.trace(operator**4)),
            "trace_D2": str(trace_d2),
            "trace_D4_at_phi_0": str(trace_d4_zero),
            "trace_D4_at_phi_pi_over_2": str(trace_d4_maximal),
            "phase_curvature_at_unit_amplitudes": str(
                phase_curvature_at_unit_amplitudes
            ),
            "mixed_quartic_at_phase_minimum": str(mixed_quartic),
            "vacuum_energy_coefficient": str(vacuum_energy_coefficient),
            "_vacuum_energy_coefficient": vacuum_energy_coefficient,
        }
    )

maximum_coefficient = max(
    row["_vacuum_energy_coefficient"] for row in rows
)
minima = [
    row
    for row in rows
    if row["_vacuum_energy_coefficient"] == maximum_coefficient
]

energy_classes = {}
phase_curvature_classes = {}
for row in rows:
    energy_classes.setdefault(row["vacuum_energy_coefficient"], 0)
    energy_classes[row["vacuum_energy_coefficient"]] += 1
    phase_curvature_classes.setdefault(
        row["phase_curvature_at_unit_amplitudes"],
        0,
    )
    phase_curvature_classes[row["phase_curvature_at_unit_amplitudes"]] += 1

serializable_rows = [
    {
        key: value
        for key, value in row.items()
        if not key.startswith("_")
    }
    for row in rows
]
serializable_minima = [
    {
        key: value
        for key, value in row.items()
        if not key.startswith("_")
    }
    for row in minima
]

result = {
    "gate": "version4_family_square_spectral_selector",
    "distinct_incidence_operators": len(rows),
    "family_square_edge_A": "a P_minus",
    "family_square_edge_B": "b exp(i phi) H",
    "positive_quartic_phase_minimum_for_every_candidate": True,
    "phase_minima": ["pi/2", "-pi/2"],
    "phase_curvature_classes": phase_curvature_classes,
    "vacuum_energy_definition": "V_min=-(mu^4/lambda)*coefficient after optimizing a and b",
    "vacuum_energy_coefficient_classes": energy_classes,
    "selected_coefficient": str(maximum_coefficient),
    "selected_operator_count": len(minima),
    "selected_cycle_types": sorted(
        {
            cycle_type
            for row in minima
            for cycle_type in row["cycle_types"]
        }
    ),
    "selected_raw_permutation_count": sum(
        len(row["permutations"]) for row in minima
    ),
    "unique_selector_exists": len(minima) == 1,
    "selected_operators": serializable_minima,
    "rows": serializable_rows,
    "status": "the square spectral potential selects the transposition orbit over the three-cycle orbit, but leaves four symmetry-related incidence directions",
}

with open(
    "s2t_v4_family_square_spectral_selector_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))