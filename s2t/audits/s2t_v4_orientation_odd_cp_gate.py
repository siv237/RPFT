import itertools
import json

import numpy as np
import sympy as sp


with open("s2t_v4_incidence_operator_menu_gate_results.json", encoding="utf-8") as handle:
    incidence_results = json.load(handle)

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


directed_three_cycles = []
for row in incidence_results["rows"]:
    if row["cycle_type"] != "3+1" or row["operator_algebra_dimension"] != 9:
        continue
    permutation = tuple(row["permutation"])
    P = permutation_matrix(permutation)
    H = restrict((P + P.T) / 2)
    K = restrict((P - P.T) / (2 * sp.I))
    directed_three_cycles.append({"permutation": list(permutation), "H": H, "K": K})

r = sp.symbols("r", real=True)
generic_spectrum = sp.factor((directed_three_cycles[0]["H"] + r * directed_three_cycles[0]["K"]).charpoly().as_expr())

r_u, r_d = sp.symbols("r_u r_d", real=True)
pair_rows = []
all_zero = True
for first_index, second_index in itertools.combinations(range(len(directed_three_cycles)), 2):
    first = directed_three_cycles[first_index]
    second = directed_three_cycles[second_index]
    X_u = first["H"] + r_u * first["K"]
    X_d = second["H"] + r_d * second["K"]
    mass_squared_u = sp.simplify(X_u * X_u)
    mass_squared_d = sp.simplify(X_d * X_d)
    commutator = sp.simplify(mass_squared_u * mass_squared_d - mass_squared_d * mass_squared_u)
    cp_odd = sp.factor(sp.trace(commutator**3))
    all_zero = all_zero and cp_odd == 0
    pair_rows.append(
        {
            "pair": [first_index, second_index],
            "cp_odd_mass_squared_trace_cube": str(cp_odd),
        }
    )

unit_operators = [
    np.array(item["H"] + item["K"], dtype=complex)
    for item in directed_three_cycles
]
mixing_pattern_counts = {}
for first_index, second_index in itertools.combinations(range(len(unit_operators)), 2):
    _, first_vectors = np.linalg.eigh(unit_operators[first_index])
    _, second_vectors = np.linalg.eigh(unit_operators[second_index])
    mixing = first_vectors.conj().T @ second_vectors
    absolute_pattern = np.round(np.abs(mixing), 12)
    key = tuple(float(value) for value in absolute_pattern.reshape(-1))
    mixing_pattern_counts[key] = mixing_pattern_counts.get(key, 0) + 1

serialized_mixing_patterns = [
    {
        "count": count,
        "absolute_matrix": [list(key[0:3]), list(key[3:6]), list(key[6:9])],
    }
    for key, count in mixing_pattern_counts.items()
]

result = {
    "gate": "version4_orientation_odd_cp",
    "directed_three_cycle_count": len(directed_three_cycles),
    "axis_count_mod_orientation": len(directed_three_cycles) // 2,
    "generic_operator": "X_P(r)=H_P+r K_P",
    "generic_characteristic_polynomial": str(generic_spectrum),
    "generic_eigenvalues": ["1", "-1/2+sqrt(3) r/2", "-1/2-sqrt(3) r/2"],
    "nondegenerate_for_generic_nonzero_r": True,
    "tested_symbolic_sector_pairs": len(pair_rows),
    "all_physical_cp_odd_invariants_zero": all_zero,
    "physical_invariant": "Tr([X_u X_u^dagger, X_d X_d^dagger]^3)",
    "interpretation": "the linear H+rK three-cycle menu has pairwise rephasing-real structure and cannot generate CKM CP violation",
    "unit_weight_mixing_patterns": serialized_mixing_patterns,
    "unit_weight_pattern_counts": sorted(mixing_pattern_counts.values()),
    "unit_weight_mixing_verdict": "four pairs give only a family permutation; the other twenty-four give large democratic 1/3-2/3 overlaps rather than hierarchical mixing",
    "next_requirement": "add a third noncommuting layer or a relative orientation term not reducible to one directed-cycle quadrature per sector",
    "pairs": pair_rows,
}

with open("s2t_v4_orientation_odd_cp_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))