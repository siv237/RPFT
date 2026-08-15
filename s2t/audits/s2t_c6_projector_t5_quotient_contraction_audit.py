import itertools
import json
import math
from pathlib import Path

import numpy as np


DIM = 4
VOL_L21 = math.pi**2
LAMBDA_4 = 24.0
TOL = 1e-10


def monomials(total_degree):
    return [
        monomial
        for monomial in itertools.product(range(total_degree + 1), repeat=DIM)
        if sum(monomial) == total_degree
    ]


MONS1 = monomials(1)
MONS2 = monomials(2)
MONS3 = monomials(3)
MONS4 = monomials(4)
MONS6 = monomials(6)


def sphere_expectation_monomial(monomial):
    total = sum(monomial)
    if any(power % 2 for power in monomial):
        return 0.0
    if total == 0:
        return 1.0
    numerator = 1.0
    for power in monomial:
        half_power = power // 2
        for odd in range(1, 2 * half_power, 2):
            numerator *= odd
    denominator = 1.0
    for offset in range(total // 2):
        denominator *= DIM + 2 * offset
    return numerator / denominator


def integrate_monomial_l21(monomial):
    return VOL_L21 * sphere_expectation_monomial(monomial)


def add_poly(left, right, scale=1.0):
    output = dict(left)
    for monomial, coefficient in right.items():
        output[monomial] = output.get(monomial, 0.0) + scale * coefficient
        if abs(output[monomial]) < 1e-13:
            del output[monomial]
    return output


def scale_poly(poly, scale):
    return {monomial: scale * coefficient for monomial, coefficient in poly.items()}


def multiply_poly(left, right):
    output = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(
                monomial_left[axis] + monomial_right[axis] for axis in range(DIM)
            )
            output[monomial] = output.get(monomial, 0.0) + coefficient_left * coefficient_right
    return {monomial: coefficient for monomial, coefficient in output.items() if abs(coefficient) > 1e-13}


def derivative_poly(poly, axis):
    output = {}
    for monomial, coefficient in poly.items():
        power = monomial[axis]
        if power == 0:
            continue
        derived = list(monomial)
        derived[axis] -= 1
        derived = tuple(derived)
        output[derived] = output.get(derived, 0.0) + coefficient * power
    return output


def laplacian_poly(poly):
    output = {}
    for axis in range(DIM):
        output = add_poly(output, derivative_poly(derivative_poly(poly, axis), axis))
    return output


def integrate_poly_l21(poly):
    return sum(
        coefficient * integrate_monomial_l21(monomial)
        for monomial, coefficient in poly.items()
    )


def inner_poly(left, right):
    return integrate_poly_l21(multiply_poly(left, right))


def inner_vector(left, right):
    return sum(inner_poly(left[axis], right[axis]) for axis in range(DIM))


def coefficient_vector_to_poly(coefficients, monomial_basis):
    return {
        monomial: float(coefficient)
        for monomial, coefficient in zip(monomial_basis, coefficients)
        if abs(coefficient) > 1e-13
    }


def scalar_metric(monomial_basis):
    metric = np.zeros((len(monomial_basis), len(monomial_basis)), dtype=float)
    for row, monomial_row in enumerate(monomial_basis):
        for column, monomial_column in enumerate(monomial_basis):
            product = tuple(
                monomial_row[axis] + monomial_column[axis] for axis in range(DIM)
            )
            metric[row, column] = integrate_monomial_l21(product)
    return (metric + metric.T) / 2.0


def orthonormal_nullspace(constraint_matrix, metric):
    _, singular_values, right_vectors = np.linalg.svd(constraint_matrix)
    rank = int(np.sum(singular_values > TOL))
    nullspace = right_vectors[rank:].T
    restricted_metric = (nullspace.T @ metric @ nullspace + nullspace.T @ metric.T @ nullspace) / 2.0
    eigenvalues, eigenvectors = np.linalg.eigh(restricted_metric)
    positive = eigenvalues > TOL
    basis = nullspace @ eigenvectors[:, positive] @ np.diag(1.0 / np.sqrt(eigenvalues[positive]))
    return rank, basis


def scalar_harmonic_basis_degree4():
    monomial_index_2 = {monomial: index for index, monomial in enumerate(MONS2)}
    constraints = np.zeros((len(MONS2), len(MONS4)), dtype=float)
    for column, monomial in enumerate(MONS4):
        for axis in range(DIM):
            power = monomial[axis]
            if power < 2:
                continue
            target = list(monomial)
            target[axis] -= 2
            constraints[monomial_index_2[tuple(target)], column] += power * (power - 1)
    metric = scalar_metric(MONS4)
    rank, basis = orthonormal_nullspace(constraints, metric)
    return constraints, metric, rank, basis


def vector_coefficient_index(component, monomial):
    return component * len(MONS3) + MONS3.index(monomial)


def n3_constraint_matrix():
    rows = []
    for target in MONS4:
        row = np.zeros(DIM * len(MONS3), dtype=float)
        for component in range(DIM):
            source = list(target)
            source[component] -= 1
            if source[component] >= 0:
                row[vector_coefficient_index(component, tuple(source))] += 1.0
        rows.append(row)
    for target in MONS2:
        row = np.zeros(DIM * len(MONS3), dtype=float)
        for component in range(DIM):
            source = list(target)
            source[component] += 1
            row[vector_coefficient_index(component, tuple(source))] += source[component]
        rows.append(row)
    for component in range(DIM):
        for target in MONS1:
            row = np.zeros(DIM * len(MONS3), dtype=float)
            for axis in range(DIM):
                source = list(target)
                source[axis] += 2
                row[vector_coefficient_index(component, tuple(source))] += source[axis] * (source[axis] - 1)
            rows.append(row)
    return np.vstack(rows)


def n3_vector_metric():
    metric = np.zeros((DIM * len(MONS3), DIM * len(MONS3)), dtype=float)
    for component in range(DIM):
        offset = component * len(MONS3)
        block = scalar_metric(MONS3)
        metric[offset : offset + len(MONS3), offset : offset + len(MONS3)] = block
    return metric


def vector_coefficients_to_poly(coefficients):
    output = []
    for component in range(DIM):
        start = component * len(MONS3)
        stop = start + len(MONS3)
        output.append(coefficient_vector_to_poly(coefficients[start:stop], MONS3))
    return output


def antisymmetric_killing_basis():
    labels = []
    vectors = []
    for first in range(DIM):
        for second in range(first + 1, DIM):
            matrix = np.zeros((DIM, DIM), dtype=float)
            matrix[first, second] = 1.0
            matrix[second, first] = -1.0
            vector = []
            for component in range(DIM):
                poly = {}
                for axis in range(DIM):
                    coefficient = matrix[component, axis]
                    if coefficient:
                        monomial = tuple(1 if index == axis else 0 for index in range(DIM))
                        poly[monomial] = coefficient
                vector.append(poly)
            norm = math.sqrt(inner_vector(vector, vector))
            labels.append(f"E{first}{second}")
            vectors.append([scale_poly(component, 1.0 / norm) for component in vector])
    return labels, vectors


def gradient_poly(poly):
    return [derivative_poly(poly, axis) for axis in range(DIM)]


def harmonic_projection_degree4(poly):
    radius_squared = {
        tuple(2 if axis == component else 0 for axis in range(DIM)): 1.0
        for component in range(DIM)
    }
    laplacian = laplacian_poly(poly)
    laplacian_squared = laplacian_poly(laplacian)
    projected = add_poly(poly, multiply_poly(radius_squared, laplacian), scale=-1.0 / 16.0)
    projected = add_poly(
        projected,
        multiply_poly(multiply_poly(radius_squared, radius_squared), laplacian_squared),
        scale=1.0 / 384.0,
    )
    return projected


scalar_constraints, scalar_metric_4, scalar_rank, scalar_basis = scalar_harmonic_basis_degree4()
n3_constraints = n3_constraint_matrix()
n3_metric = n3_vector_metric()
n3_rank, n3_basis = orthonormal_nullspace(n3_constraints, n3_metric)

scalar_polys = [coefficient_vector_to_poly(scalar_basis[:, index], MONS4) for index in range(scalar_basis.shape[1])]
n3_vectors = [vector_coefficients_to_poly(n3_basis[:, index]) for index in range(n3_basis.shape[1])]
n1_labels, n1_vectors = antisymmetric_killing_basis()

one_form_labels = [f"n1_{label}" for label in n1_labels] + [f"n3_B{index:02d}" for index in range(len(n3_vectors))]
one_form_vectors = n1_vectors + n3_vectors
scalar_labels = [f"ell4_Y{index:02d}" for index in range(len(scalar_polys))]

raw_table = np.zeros((len(one_form_vectors), len(scalar_polys)), dtype=float)
for row, one_form in enumerate(one_form_vectors):
    for column, scalar in enumerate(scalar_polys):
        d_green_scalar = [scale_poly(component, 1.0 / LAMBDA_4) for component in gradient_poly(scalar)]
        raw_table[row, column] = inner_vector(one_form, d_green_scalar)

display_table = np.where(np.abs(raw_table) < 1e-11, 0.0, raw_table)

q = {(2, 0, 0, 0): 1.0, (0, 2, 0, 0): -1.0}
t1_harmonic = harmonic_projection_degree4(scale_poly(multiply_poly(q, q), 20.0))
t3_seed = {(4, 0, 0, 0): -172.0, (0, 4, 0, 0): 172.0}
t3_harmonic = harmonic_projection_degree4(t3_seed)


def witness_summary(harmonic):
    d_green = [scale_poly(component, 1.0 / LAMBDA_4) for component in gradient_poly(harmonic)]
    contractions = np.array([inner_vector(one_form, d_green) for one_form in one_form_vectors])
    return {
        "harmonic_laplacian_max_abs_coefficient": max(
            [abs(value) for value in laplacian_poly(harmonic).values()] or [0.0]
        ),
        "scalar_norm_squared": inner_poly(harmonic, harmonic),
        "dG_one_form_norm_squared": inner_vector(d_green, d_green),
        "max_abs_low_coexact_contraction": float(np.max(np.abs(contractions))),
        "low_coexact_contractions": [0.0 if abs(value) < 1e-11 else float(value) for value in contractions],
    }


t1_summary = witness_summary(t1_harmonic)
t3_summary = witness_summary(t3_harmonic)

results = {
    "status": "T5_direct_dG_ell4_leakage_is_orthogonal_to_low_coexact_quotient",
    "question": "Does ell=4 scalar leakage from T1/T3 survive after the outer dG term is paired with quotient-normalized n=1/n=3 coexact one-forms?",
    "conventions": {
        "space": "L(2,1)=RP3 with quotient volume pi^2",
        "scalar_shell": "complete ell=4 harmonic shell inherited from even S3 harmonics",
        "scalar_shell_dimension": int(scalar_basis.shape[1]),
        "scalar_eigenvalue": LAMBDA_4,
        "green_action": "G Y_4 = Y_4/24",
        "one_form_rows": "six normalized n=1 Killing forms plus thirty normalized n=3 coexact cubic vector harmonics",
        "structural_identity": "<beta_coex,dG phi>=<delta beta_coex,G phi>=0",
    },
    "basis_checks": {
        "scalar_laplacian_constraint_rank": scalar_rank,
        "scalar_harmonic_dimension": int(scalar_basis.shape[1]),
        "scalar_constraint_max_abs": float(np.max(np.abs(scalar_constraints @ scalar_basis))),
        "scalar_orthonormality_max_abs_error": float(
            np.max(np.abs(scalar_basis.T @ scalar_metric_4 @ scalar_basis - np.eye(scalar_basis.shape[1])))
        ),
        "n3_constraint_rank": n3_rank,
        "n3_coexact_dimension": int(n3_basis.shape[1]),
        "n3_constraint_max_abs": float(np.max(np.abs(n3_constraints @ n3_basis))),
        "n3_orthonormality_max_abs_error": float(
            np.max(np.abs(n3_basis.T @ n3_metric @ n3_basis - np.eye(n3_basis.shape[1])))
        ),
    },
    "T5_table": {
        "shape": [int(raw_table.shape[0]), int(raw_table.shape[1])],
        "row_labels": one_form_labels,
        "column_labels": scalar_labels,
        "raw_max_abs_entry": float(np.max(np.abs(raw_table))),
        "raw_frobenius_norm": float(np.linalg.norm(raw_table, ord="fro")),
        "numeric_rank_at_1e_10": int(np.linalg.matrix_rank(raw_table, tol=1e-10)),
        "thresholded_entries": display_table.tolist(),
    },
    "witness_channels": {
        "T1_ell4_harmonic": t1_summary,
        "T3_ell4_harmonic": t3_summary,
    },
    "decision": {
        "direct_T1_T3_outer_dG_quotient_contraction": "zero_by_exact_coexact_orthogonality",
        "rank10_rescue_effect": "the specific ell4 leakage in Pi_AB does not survive direct projection onto the background n1/n3 coexact quotient",
        "full_projector_block": "still_open",
        "remaining_terms": [
            "Pi Delta1_A Pi_B and A<->B, where the varied one-form operator acts on an exact dG D_B input before the final coexact projection",
            "Hilbert/basis transport and self-adjoint representation in the varied inner product",
            "possible T4 or higher-shell channels inside cross terms rather than the pure outer-dG Pi_AB channel",
        ],
    },
    "verdict": (
        "The complete 36x25 quotient-contraction table vanishes to numerical precision. "
        "The result is structural: every T1/T3 ell=4 scalar contribution entering through the outer dG in Pi_AB is an exact one-form, so its pairing with any quotient-normalized coexact n=1 or n=3 state is zero. "
        "This closes the direct T5 channel and removes the previously identified T1/T3 higher-shell leakage from the pure Pi_AB matrix element. "
        "It does not yet close the full projector contribution, because cross terms in which Delta1_A acts on Pi_B before the final coexact projection can still be nonzero."
    ),
}

Path("s2t_c6_projector_t5_quotient_contraction_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)

print(
    json.dumps(
        {
            "status": results["status"],
            "table_shape": results["T5_table"]["shape"],
            "raw_max_abs_entry": results["T5_table"]["raw_max_abs_entry"],
            "numeric_rank": results["T5_table"]["numeric_rank_at_1e_10"],
            "T1_max_abs_contraction": t1_summary["max_abs_low_coexact_contraction"],
            "T3_max_abs_contraction": t3_summary["max_abs_low_coexact_contraction"],
            "full_projector_block": results["decision"]["full_projector_block"],
        },
        indent=2,
        ensure_ascii=False,
    )
)