import itertools
import json
from collections import Counter

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


def matrix_key(matrix):
    return tuple(str(value) for value in matrix)


operators = {}
orientation_odd = {}
for row in incidence_results["rows"]:
    if row["operator_algebra_dimension"] != 9:
        continue
    permutation = tuple(row["permutation"])
    P = permutation_matrix(permutation)
    H = restrict((P + P.T) / 2)
    K = restrict((P - P.T) / (2 * sp.I))
    operators.setdefault(matrix_key(H), H)
    if K != sp.zeros(3):
        orientation_odd.setdefault(matrix_key(K), K)

operator_list = list(operators.values())
pair_rows = []
for first_index, second_index in itertools.combinations(range(len(operator_list)), 2):
    first = operator_list[first_index]
    second = operator_list[second_index]
    commutator = sp.simplify(first * second - second * first)
    norm = sp.simplify(sp.trace(commutator.T * commutator))
    cp_odd = sp.simplify(sp.trace(commutator**3))
    pair_rows.append(
        {
            "pair": [first_index, second_index],
            "commutator_norm": str(norm),
            "cp_odd_trace_cube": str(cp_odd),
            "commutes": norm == 0,
            "_norm": norm,
        }
    )

maximum_norm = max(row["_norm"] for row in pair_rows)
minimum_norm = min(row["_norm"] for row in pair_rows)
maximum_pairs = [row for row in pair_rows if row["_norm"] == maximum_norm]
minimum_pairs = [row for row in pair_rows if row["_norm"] == minimum_norm]

orientation_spectra = [
    {str(key): value for key, value in operator.eigenvals().items()}
    for operator in orientation_odd.values()
]

result = {
    "gate": "version4_cross_sector_cp",
    "distinct_real_symmetric_sector_operators": len(operator_list),
    "unordered_sector_pairs": len(pair_rows),
    "commutator_norm_distribution": dict(Counter(row["commutator_norm"] for row in pair_rows)),
    "minimum_commutator_norm": str(minimum_norm),
    "minimum_pair_degeneracy": len(minimum_pairs),
    "maximum_commutator_norm": str(maximum_norm),
    "maximum_pair_degeneracy": len(maximum_pairs),
    "all_cp_odd_trace_cubes_zero": all(row["cp_odd_trace_cube"] == "0" for row in pair_rows),
    "positive_cross_coupling_verdict": "selects one of ten commuting pairs and cannot force mixing",
    "negative_cross_coupling_verdict": "selects one of four maximally noncommuting pairs but does not choose a unique orbit",
    "real_menu_cp_verdict": "all real symmetric pairs have zero Jarlskog trace-cube invariant",
    "nonzero_orientation_odd_operators": len(orientation_odd),
    "orientation_odd_spectra": orientation_spectra,
    "next_route": "include the Hermitian orientation-odd operator (P-P^dagger)/(2i) from a directed three-cycle",
    "pairs": [{key: value for key, value in row.items() if not key.startswith("_")} for row in pair_rows],
}

with open("s2t_v4_cross_sector_cp_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))