import json

import sympy as sp


with open("s2t_v4_incidence_operator_menu_gate_results.json", encoding="utf-8") as handle:
    incidence_results = json.load(handle)

points = [(0, 0), (0, 1), (1, 0), (1, 1)]
point_index = {point: index for index, point in enumerate(points)}


def affine_permutation(matrix, shift):
    return tuple(
        point_index[
            (
                (matrix[0][0] * point[0] + matrix[0][1] * point[1] + shift[0]) % 2,
                (matrix[1][0] * point[0] + matrix[1][1] * point[1] + shift[1]) % 2,
            )
        ]
        for point in points
    )


def permutation_matrix(permutation):
    matrix = sp.zeros(4)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1
    return matrix


triplet_basis = sp.Matrix.hstack(
    sp.Matrix([1, 1, -1, -1]) / 2,
    sp.Matrix([1, -1, 1, -1]) / 2,
    sp.Matrix([1, -1, -1, 1]) / 2,
)


def restrict(matrix):
    return sp.simplify(triplet_basis.T * matrix * triplet_basis)


identity2 = ((1, 0), (0, 1))
shear2 = ((1, 0), (1, 1))
T_p = restrict(permutation_matrix(affine_permutation(identity2, (1, 0))))
T_q = restrict(permutation_matrix(affine_permutation(identity2, (0, 1))))
S = restrict(permutation_matrix(affine_permutation(shear2, (0, 0))))
P_minus = (sp.eye(3) - S) / 2


def commutator_norm(operator, reference):
    commutator = operator * reference - reference * operator
    return sp.simplify(sp.trace(commutator.T * commutator))


def matrix_key(matrix):
    return tuple(str(value) for value in matrix)


operators = {}
for row in incidence_results["rows"]:
    if row["operator_algebra_dimension"] != 9:
        continue
    permutation = tuple(row["permutation"])
    P = permutation_matrix(permutation)
    H = restrict((P + P.T) / 2)
    operators.setdefault(matrix_key(H), {"matrix": H, "permutations": [], "cycle_types": set()})
    operators[matrix_key(H)]["permutations"].append(list(permutation))
    operators[matrix_key(H)]["cycle_types"].add(row["cycle_type"])

rows = []
for item in operators.values():
    H = item["matrix"]
    scores = {
        "translation_p": commutator_norm(H, T_p),
        "translation_q": commutator_norm(H, T_q),
        "shear": commutator_norm(H, S),
        "rank_one": commutator_norm(H, P_minus),
    }
    metric_score = sp.simplify(
        scores["translation_p"]
        + sp.Rational(1, 4) * scores["translation_q"]
        + sp.Rational(1, 5) * scores["shear"]
    )
    rows.append(
        {
            "matrix": str(H),
            "permutations": item["permutations"],
            "cycle_types": sorted(item["cycle_types"]),
            "scores": {key: str(value) for key, value in scores.items()},
            "metric_weighted_score": str(metric_score),
            "_metric_score_exact": metric_score,
            "_matrix": H,
        }
    )

minimum_score = min(row["_metric_score_exact"] for row in rows)
minima = [row for row in rows if row["_metric_score_exact"] == minimum_score]
minima_commutators = []
for first_index in range(len(minima)):
    for second_index in range(first_index + 1, len(minima)):
        commutator = sp.simplify(minima[first_index]["_matrix"] * minima[second_index]["_matrix"] - minima[second_index]["_matrix"] * minima[first_index]["_matrix"])
        minima_commutators.append(
            {
                "pair": [first_index, second_index],
                "commutator": str(commutator),
                "vanishes": commutator == sp.zeros(3),
            }
        )

score_classes = {}
for row in rows:
    key = tuple(row["scores"].values())
    score_classes.setdefault(str(key), 0)
    score_classes[str(key)] += 1

serializable_rows = []
for row in rows:
    serializable_rows.append({key: value for key, value in row.items() if not key.startswith("_")})

result = {
    "gate": "version4_quadratic_parent_selector",
    "raw_successful_permutation_directions": incidence_results["successful_full_M3_count"],
    "distinct_hermitian_full_M3_operators": len(rows),
    "quadratic_score_classes": score_classes,
    "any_singleton_score_class": any(count == 1 for count in score_classes.values()),
    "metric_weights": {"translation_p": "1", "translation_q": "1/4", "shear": "1/5"},
    "metric_minimum_score": str(minimum_score),
    "metric_minimum_degeneracy": len(minima),
    "metric_minima": [{key: value for key, value in row.items() if not key.startswith("_")} for row in minima],
    "metric_minima_commutators": minima_commutators,
    "all_metric_minima_commute": all(item["vanishes"] for item in minima_commutators),
    "selector_status": "quadratic commutator data do not select a unique incidence operator",
    "mixing_status": "assigning the two metric minima to different sectors still gives a common eigenbasis",
    "rows": serializable_rows,
}

with open("s2t_v4_quadratic_parent_selector_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))