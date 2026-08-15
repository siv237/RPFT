import itertools
import json
from collections import Counter
from pathlib import Path

import sympy as sp


DIM = 4
x = sp.Matrix(sp.symbols("x0:4", real=True))
I4 = sp.eye(DIM)
P = I4 - x * x.T


def strain_basis():
    labels = []
    matrices = []
    for index in range(DIM):
        matrix = sp.zeros(DIM)
        matrix[index, index] = 1
        labels.append(f"D{index}{index}")
        matrices.append(matrix)
    for first in range(DIM):
        for second in range(first + 1, DIM):
            matrix = sp.zeros(DIM)
            matrix[first, second] = 1
            matrix[second, first] = 1
            labels.append(f"S{first}{second}")
            matrices.append(matrix)
    return labels, matrices


def killing_basis():
    labels = []
    matrices = []
    for first in range(DIM):
        for second in range(first + 1, DIM):
            matrix = sp.zeros(DIM)
            matrix[first, second] = 1
            matrix[second, first] = -1
            labels.append(f"E{first}{second}")
            matrices.append(matrix)
    return labels, matrices


def sphere_expectation_monomial(powers):
    total = sum(powers)
    if any(power % 2 for power in powers):
        return sp.Integer(0)
    if total == 0:
        return sp.Integer(1)
    numerator = sp.Integer(1)
    for power in powers:
        half = power // 2
        numerator *= sp.factorial2(2 * half - 1) if half else 1
    denominator = sp.Integer(1)
    for offset in range(total // 2):
        denominator *= DIM + 2 * offset
    return sp.Rational(numerator, denominator)


def sphere_expectation(poly):
    expanded = sp.Poly(sp.expand(poly), *x)
    total = sp.Integer(0)
    for powers, coefficient in expanded.terms():
        total += coefficient * sphere_expectation_monomial(powers)
    return sp.simplify(total)


def matrix_trace(matrix):
    return sum(matrix[index, index] for index in range(matrix.rows))


def ricci_mixed_second(A, B):
    U = -2 * A
    V = -2 * B
    W = 3 * (A * B + B * A)

    u = sp.expand((x.T * U * x)[0])
    v = sp.expand((x.T * V * x)[0])
    w = sp.expand((x.T * W * x)[0])

    y_e = U * x
    y_f = V * x
    y_ef = W * x

    Y0 = x * x.T
    Ye = y_e * x.T + x * y_e.T
    Yf = y_f * x.T + x * y_f.T
    Yef = y_ef * x.T + x * y_ef.T + y_e * y_f.T + y_f * y_e.T

    Q0 = P
    Qe = U - Ye + u * Y0
    Qf = V - Yf + v * Y0
    Qef = W - (
        Yef - u * Yf - v * Ye + (2 * u * v - w) * Y0
    )

    inv_s_e = -u / 2
    inv_s_f = -v / 2
    inv_s_ef = -w / 2 + sp.Rational(3, 4) * u * v

    S0 = Q0
    Se = Qe + inv_s_e * Q0
    Sf = Qf + inv_s_f * Q0
    Sef = Qef + inv_s_e * Qf + inv_s_f * Qe + inv_s_ef * Q0

    H0 = sp.Integer(3)
    He = matrix_trace(Se)
    Hf = matrix_trace(Sf)
    Hef = matrix_trace(Sef)

    ricci_ef = (
        H0 * Sef
        + He * Sf
        + Hf * Se
        + Hef * S0
        - S0 * Sef
        - Sef * S0
        - Se * Sf
        - Sf * Se
    )
    return ricci_ef.applyfunc(sp.expand)


def normalized_killing_matrix(ricci_second, killing_matrices):
    matrix = sp.zeros(len(killing_matrices))
    killing_vectors = [rotation * x for rotation in killing_matrices]
    for row, left in enumerate(killing_vectors):
        for column, right in enumerate(killing_vectors):
            integrand = (left.T * ricci_second * right)[0]
            matrix[row, column] = sp.simplify(2 * sphere_expectation(integrand))
    return matrix


def parse_sparse_pair(pair, rotation_labels):
    matrix = sp.zeros(len(rotation_labels))
    index = {label: position for position, label in enumerate(rotation_labels)}
    for entry in pair["nonzero_entries"]:
        matrix[index[entry["row"]], index[entry["col"]]] = sp.Rational(
            entry["value"]
        )
    return matrix


def sparse_entries(matrix, rotation_labels):
    entries = []
    for row in range(matrix.rows):
        for column in range(matrix.cols):
            value = sp.simplify(matrix[row, column])
            if value != 0:
                entries.append(
                    {
                        "row": rotation_labels[row],
                        "col": rotation_labels[column],
                        "value": str(value),
                    }
                )
    return entries


strain_labels, strains = strain_basis()
rotation_labels, rotations = killing_basis()
pair_indices = list(itertools.combinations_with_replacement(range(len(strains)), 2))

principal_connection = json.loads(
    Path("s2t_c6_l21_delta2_principal_plus_connection_C11_table_data.json").read_text()
)
pc_lookup = {
    (pair["A"], pair["B"]): parse_sparse_pair(pair, rotation_labels)
    for pair in principal_connection["pairs"]
}

ricci_pairs = []
combined_pairs = []
ricci_rank_distribution = Counter()
combined_rank_distribution = Counter()
ricci_zero_pairs = []
combined_zero_pairs = []
max_asymmetry = 0.0

for first, second in pair_indices:
    label_a = strain_labels[first]
    label_b = strain_labels[second]
    ricci_second = ricci_mixed_second(strains[first], strains[second])
    ricci_matrix = normalized_killing_matrix(ricci_second, rotations)
    asymmetry = max(
        [float(abs(sp.N(value))) for value in (ricci_matrix - ricci_matrix.T)]
        or [0.0]
    )
    max_asymmetry = max(max_asymmetry, asymmetry)
    ricci_rank = int(ricci_matrix.rank())
    ricci_rank_distribution[ricci_rank] += 1
    if ricci_rank == 0:
        ricci_zero_pairs.append(f"{label_a},{label_b}")
    ricci_pairs.append(
        {
            "A": label_a,
            "B": label_b,
            "rank": ricci_rank,
            "nonzero_entries": sparse_entries(ricci_matrix, rotation_labels),
        }
    )

    combined = pc_lookup[(label_a, label_b)] + ricci_matrix
    combined_rank = int(combined.rank())
    combined_rank_distribution[combined_rank] += 1
    if combined_rank == 0:
        combined_zero_pairs.append(f"{label_a},{label_b}")
    combined_pairs.append(
        {
            "A": label_a,
            "B": label_b,
            "rank": combined_rank,
            "nonzero_entries": sparse_entries(combined, rotation_labels),
            "principal_connection_rank": int(pc_lookup[(label_a, label_b)].rank()),
            "ricci_rank": ricci_rank,
        }
    )

trace_second = ricci_mixed_second(I4, I4)
trace_control_matrix = normalized_killing_matrix(trace_second, rotations)
trace_control = trace_control_matrix - 12 * sp.eye(len(rotations))
trace_control_max = max(
    [float(abs(sp.N(value))) for value in trace_control] or [0.0]
)

ricci_data = {
    "status": "delta2_Ricci_C11_Gauss_table_computed",
    "rot_labels": rotation_labels,
    "strain_labels_raw_trace_basis": strain_labels,
    "formula": "For y=Mx ellipsoid, S=(x^T C^-1 x)^(-1/2)[C^-1-C^-1 x x^T C^-1/(x^T C^-1 x)], Ric#=tr(S)S-S^2; take mixed AB coefficient and integrate against normalized Killing forms",
    "symmetric_pair_count": len(pair_indices),
    "rank_distribution": {str(rank): count for rank, count in sorted(ricci_rank_distribution.items())},
    "zero_pairs": ricci_zero_pairs,
    "all_pairs_nonzero": not ricci_zero_pairs,
    "max_matrix_asymmetry_numeric": float(max_asymmetry),
    "trace_scaling_control_max_abs": float(trace_control_max),
    "pairs": ricci_pairs,
}

combined_data = {
    "status": "principal_connection_plus_Ricci_C11_table_computed",
    "inputs": [
        "s2t_c6_l21_delta2_principal_plus_connection_C11_table_data.json",
        "s2t_c6_l21_delta2_ricci_C11_gauss_table_data.json",
    ],
    "rot_labels": rotation_labels,
    "strain_labels_raw_trace_basis": strain_labels,
    "formula": "C_principal_connection_Ricci=C_principal_connection+C_Ricci2",
    "symmetric_pair_count": len(pair_indices),
    "rank_distribution": {str(rank): count for rank, count in sorted(combined_rank_distribution.items())},
    "zero_pairs": combined_zero_pairs,
    "all_pairs_nonzero": not combined_zero_pairs,
    "pairs": combined_pairs,
}

results = {
    "status": "delta2_Ricci_C11_computed_and_combined_with_principal_connection",
    "geometry": {
        "method": "Gauss equation for the linear ellipsoid F(x)=Mx in R4",
        "background_control": "Ric#=2I on unit S3/RP3",
        "trace_scaling_control": "A=B=I gives delta2 Ric#=12I on tangent forms",
        "trace_scaling_control_max_abs": float(trace_control_max),
    },
    "ricci_table": {
        "pair_count": len(pair_indices),
        "rank_distribution": ricci_data["rank_distribution"],
        "zero_pairs": ricci_zero_pairs,
        "all_pairs_nonzero": not ricci_zero_pairs,
        "max_matrix_asymmetry_numeric": float(max_asymmetry),
    },
    "combined_table": {
        "rank_distribution": combined_data["rank_distribution"],
        "zero_pairs": combined_zero_pairs,
        "all_pairs_nonzero": not combined_zero_pairs,
    },
    "decision": {
        "Ricci_internal_status": "computed_full_C11_table",
        "principal_connection_cancellation_by_Ricci": "yes_only_if_combined_zero_pairs_exist_else_no",
        "actual_combined_zero_pair_count": len(combined_zero_pairs),
        "next_required_object": "inspect combined ranks/entries and add any remaining genuine local or Maxwell-ghost same-scheme L_AB terms",
    },
    "verdict": (
        "The mixed second Ricci endomorphism has been computed from the exact Gauss shape-operator formula for the linearly deformed sphere and integrated against the six quotient-normalized Killing forms. "
        "The resulting 55-pair C11 table is then added to the existing principal+connection table. "
        "The trace-scaling control A=B=I reproduces delta2 Ric#=12I. "
        "The combined rank and zero-pair data decide whether curvature can cancel the previously nonzero C11 block."
    ),
}

Path("s2t_c6_l21_delta2_ricci_C11_gauss_table_data.json").write_text(
    json.dumps(ricci_data, indent=2, ensure_ascii=False) + "\n"
)
Path("s2t_c6_l21_delta2_principal_connection_ricci_C11_table_data.json").write_text(
    json.dumps(combined_data, indent=2, ensure_ascii=False) + "\n"
)
Path("s2t_c6_l21_delta2_ricci_C11_gauss_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)

print(
    json.dumps(
        {
            "status": results["status"],
            "trace_control_max_abs": float(trace_control_max),
            "ricci_rank_distribution": ricci_data["rank_distribution"],
            "ricci_zero_pairs": ricci_zero_pairs,
            "combined_rank_distribution": combined_data["rank_distribution"],
            "combined_zero_pairs": combined_zero_pairs,
        },
        indent=2,
        ensure_ascii=False,
    )
)