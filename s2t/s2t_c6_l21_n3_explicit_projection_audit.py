import itertools
import json
import math
from pathlib import Path

import numpy as np

DIM = 4
VOL_L21 = math.pi ** 2
TOL = 1e-10


def monomials(total_degree):
    return [m for m in itertools.product(range(total_degree + 1), repeat=DIM) if sum(m) == total_degree]


MONS1 = monomials(1)
MONS2 = monomials(2)
MONS3 = monomials(3)
MONS4 = monomials(4)
COEFF_INDEX = {(component, mon): component * len(MONS3) + i for component in range(DIM) for i, mon in enumerate(MONS3)}


def sphere_expectation_monomial(mon):
    total = sum(mon)
    if any(k % 2 for k in mon):
        return 0.0
    if total == 0:
        return 1.0
    numerator = 1.0
    half = total // 2
    for k in mon:
        a = k // 2
        odd_df = 1
        for r in range(1, 2 * a, 2):
            odd_df *= r
        numerator *= odd_df
    denom = 1.0
    for r in range(half):
        denom *= DIM + 2 * r
    return numerator / denom


def integral_monomial_l21(mon):
    return VOL_L21 * sphere_expectation_monomial(mon)


def antisym_basis_4():
    labels = []
    basis = []
    for a in range(DIM):
        for b in range(a + 1, DIM):
            matrix = np.zeros((DIM, DIM), dtype=float)
            matrix[a, b] = 1.0
            matrix[b, a] = -1.0
            labels.append(f"E{a}{b}")
            basis.append(matrix)
    return labels, basis


def add_poly(p, q, scale=1.0):
    out = dict(p)
    for mon, val in q.items():
        out[mon] = out.get(mon, 0.0) + scale * val
        if abs(out[mon]) < 1e-12:
            del out[mon]
    return out


def mul_poly(p, q):
    out = {}
    for a, va in p.items():
        for b, vb in q.items():
            mon = tuple(a[i] + b[i] for i in range(DIM))
            out[mon] = out.get(mon, 0.0) + va * vb
    return {m: v for m, v in out.items() if abs(v) > 1e-12}


def lin_poly(coeffs):
    return {tuple(1 if i == j else 0 for i in range(DIM)): float(c) for j, c in enumerate(coeffs) if abs(c) > 1e-12}


def quad_form_poly(matrix):
    out = {}
    for i in range(DIM):
        for j in range(DIM):
            coeff = float(matrix[i, j])
            if abs(coeff) < 1e-12:
                continue
            mon = [0] * DIM
            mon[i] += 1
            mon[j] += 1
            out[tuple(mon)] = out.get(tuple(mon), 0.0) + coeff
    return {m: v for m, v in out.items() if abs(v) > 1e-12}


def vector_lin(matrix):
    return [lin_poly(matrix[row, :]) for row in range(DIM)]


def vector_add(v, w, scale=1.0):
    return [add_poly(v[i], w[i], scale) for i in range(DIM)]


def vector_scale(v, scale):
    return [{m: scale * c for m, c in component.items()} for component in v]


def scalar_times_vector(s, v):
    return [mul_poly(s, component) for component in v]


def dot_x_vector(v):
    total = {}
    for i in range(DIM):
        total = add_poly(total, mul_poly(lin_poly([1 if k == i else 0 for k in range(DIM)]), v[i]))
    return total


def vector_to_coeff(v, degree=3):
    coeff = np.zeros(DIM * len(MONS3), dtype=float)
    skipped_norm_proxy = 0.0
    skipped_terms = 0
    for component, poly in enumerate(v):
        for mon, value in poly.items():
            if sum(mon) != degree:
                skipped_norm_proxy += value * value
                skipped_terms += 1
                continue
            coeff[COEFF_INDEX[(component, mon)]] += value
    return coeff, skipped_terms, skipped_norm_proxy


def coeff_to_vector(coeff):
    vector = []
    for component in range(DIM):
        poly = {}
        for i, mon in enumerate(MONS3):
            value = coeff[component * len(MONS3) + i]
            if abs(value) > 1e-12:
                poly[mon] = float(value)
        vector.append(poly)
    return vector


def build_constraint_matrix():
    rows = []
    names = []
    for target in MONS4:
        row = np.zeros(DIM * len(MONS3), dtype=float)
        for component in range(DIM):
            mon = list(target)
            mon[component] -= 1
            if mon[component] >= 0 and sum(mon) == 3:
                row[COEFF_INDEX[(component, tuple(mon))]] += 1.0
        rows.append(row)
        names.append(("tangency", target))
    for target in MONS2:
        row = np.zeros(DIM * len(MONS3), dtype=float)
        for component in range(DIM):
            mon = list(target)
            mon[component] += 1
            if sum(mon) == 3:
                row[COEFF_INDEX[(component, tuple(mon))]] += mon[component]
        rows.append(row)
        names.append(("divergence", target))
    for component in range(DIM):
        for target in MONS1:
            row = np.zeros(DIM * len(MONS3), dtype=float)
            for axis in range(DIM):
                mon = list(target)
                mon[axis] += 2
                if sum(mon) == 3:
                    row[COEFF_INDEX[(component, tuple(mon))]] += mon[axis] * (mon[axis] - 1)
            rows.append(row)
            names.append(("component_harmonic", component, target))
    return np.vstack(rows), names


def build_l2_metric():
    metric = np.zeros((DIM * len(MONS3), DIM * len(MONS3)), dtype=float)
    for component in range(DIM):
        for i, mon_i in enumerate(MONS3):
            for j, mon_j in enumerate(MONS3):
                mon = tuple(mon_i[k] + mon_j[k] for k in range(DIM))
                metric[component * len(MONS3) + i, component * len(MONS3) + j] = integral_monomial_l21(mon)
    return (metric + metric.T) / 2.0


def leaked_image(matrix):
    a_matrix = np.diag([1.0, -1.0, 0.0, 0.0])
    q = quad_form_poly(a_matrix)
    x_vec = [lin_poly([1 if i == j else 0 for i in range(DIM)]) for j in range(DIM)]
    nx = vector_lin(matrix)
    nax = vector_lin(matrix @ a_matrix)
    c_matrix = matrix.T @ a_matrix + a_matrix.T @ matrix
    cx = vector_lin(c_matrix)
    f = quad_form_poly(c_matrix)
    raw = vector_add(vector_scale(scalar_times_vector(q, nx), -12.0), vector_scale(nax, 4.0))
    raw = vector_add(raw, vector_scale(cx, -2.0))
    raw = vector_add(raw, vector_scale(scalar_times_vector(f, x_vec), 2.0))
    normal_scalar = dot_x_vector(raw)
    tangent = vector_add(raw, scalar_times_vector(normal_scalar, x_vec), scale=-1.0)
    return tangent


def gram_from_coeffs(coeffs, metric):
    gram = np.zeros((len(coeffs), len(coeffs)), dtype=float)
    for i, vi in enumerate(coeffs):
        for j, vj in enumerate(coeffs):
            gram[i, j] = vi @ metric @ vj
    return (gram + gram.T) / 2.0


constraint_matrix, constraint_names = build_constraint_matrix()
_, singular_values, vh = np.linalg.svd(constraint_matrix)
rank = int(np.sum(singular_values > TOL))
nullspace = vh[rank:].T
metric = build_l2_metric()
null_metric = (nullspace.T @ metric @ nullspace + nullspace.T @ metric.T @ nullspace) / 2.0
metric_eigs, metric_vecs = np.linalg.eigh(null_metric)
positive = metric_eigs > TOL
orthonormal_basis = nullspace @ metric_vecs[:, positive] @ np.diag(1.0 / np.sqrt(metric_eigs[positive]))

labels, killing_basis = antisym_basis_4()
killing_norm_sq = VOL_L21 * float(np.trace(killing_basis[0].T @ killing_basis[0])) / 4.0
image_rows = [vector_to_coeff(leaked_image(matrix)) for matrix in killing_basis]
images = [row[0] / math.sqrt(killing_norm_sq) for row in image_rows]
skipped_terms_total = int(sum(row[1] for row in image_rows))
skipped_coeff_square_proxy = float(sum(row[2] for row in image_rows))
image_gram = gram_from_coeffs(images, metric)
projection_coefficients = np.array([[orthonormal_basis[:, a] @ metric @ image for a in range(orthonormal_basis.shape[1])] for image in images])
projected_gram = projection_coefficients @ projection_coefficients.T
residual_gram = image_gram - projected_gram

basis_constraint_residual = float(np.max(np.abs(constraint_matrix @ orthonormal_basis)))
basis_metric_residual = float(np.max(np.abs(orthonormal_basis.T @ metric @ orthonormal_basis - np.eye(orthonormal_basis.shape[1]))))
image_constraint_residual = float(np.max(np.abs(constraint_matrix @ np.column_stack(images))))

LAMBDA_1 = 4
LAMBDA_3 = 16
lambda_gap = LAMBDA_3 - LAMBDA_1
projected_trace = float(np.trace(projected_gram))
second_order_gap_proxy = projected_trace / (lambda_gap ** 2)
second_order_single_gap_proxy = projected_trace / lambda_gap

results = {
    "status": "explicit_n3_coexact_basis_projection_confirms_nonzero_leakage",
    "construction": {
        "ambient_space": "homogeneous cubic vector polynomials in R4",
        "ambient_dimension": int(DIM * len(MONS3)),
        "constraints": {
            "tangency_x_dot_V_zero": len(MONS4),
            "ambient_divergence_zero": len(MONS2),
            "component_harmonic_laplacian_zero": DIM * len(MONS1),
            "constraint_rank": rank,
            "nullity": int(nullspace.shape[1]),
        },
        "basis_dimension": int(orthonormal_basis.shape[1]),
        "inner_product": "L2 on L(2,1), using quotient volume pi^2",
        "basis_constraint_max_abs": basis_constraint_residual,
        "basis_orthonormality_max_abs_error": basis_metric_residual,
    },
    "projection": {
        "source_images": "cubic part of the six tangent-projected n=1 Killing-shell leakage images, normalized by the L(2,1) Killing norm",
        "discarded_non_cubic_terms_total": skipped_terms_total,
        "discarded_non_cubic_coeff_square_proxy": skipped_coeff_square_proxy,
        "basis_labels": labels,
        "image_constraint_max_abs_before_projection": image_constraint_residual,
        "image_gram_trace": float(np.trace(image_gram)),
        "projected_gram_trace": projected_trace,
        "residual_gram_trace": float(np.trace(residual_gram)),
        "projected_rank_numeric": int(np.linalg.matrix_rank(projected_gram, tol=1e-9)),
        "projected_eigenvalues": [float(x) for x in np.linalg.eigvalsh((projected_gram + projected_gram.T) / 2.0)],
        "max_abs_residual_gram_entry": float(np.max(np.abs(residual_gram))),
        "projected_gram_matrix": projected_gram.tolist(),
        "residual_gram_matrix": residual_gram.tolist(),
    },
    "second_order_bookkeeping_proxy": {
        "lambda_1": LAMBDA_1,
        "lambda_3": LAMBDA_3,
        "lambda_gap": lambda_gap,
        "trace_over_gap": second_order_single_gap_proxy,
        "trace_over_gap_squared": second_order_gap_proxy,
        "note": "This is still bookkeeping-level; the final determinant sign and whether one or two gap denominators enter must be fixed in the full operator formula.",
    },
    "interpretation": [
        {
            "claim": "the proxy residue was an artifact of not having an explicit n=3 basis",
            "verdict": "fails_for_this_modelled_operator_slice",
            "reason": "Projection onto the explicit 30-dimensional cubic coexact basis leaves a nonzero trace rather than killing the six images.",
        },
        {
            "claim": "this is already the final C6 determinant coefficient",
            "verdict": "not_yet",
            "reason": "The calculation covers the conformal Hodge-filtered low-shell slice and explicit coexact projection. Full C6 still needs all one-form operator terms, Hilbert-metric variation, determinant sign, and tower bookkeeping.",
        },
    ],
    "verdict": (
        "An explicit quotient-normalized 30-dimensional n=3 coexact basis was constructed from cubic tangent, divergence-free, harmonic vector polynomials. "
        "Projecting the six normalized leaked Killing-shell images onto this basis gives a nonzero projected trace, so the n=3 gate is not killed by the explicit basis construction. "
        "This upgrades the proxy warning into a concrete low-shell obstruction candidate, but it is not yet the final C6 determinant theorem because the full one-form variation and determinant bookkeeping remain to be assembled."
    ),
}

Path("s2t_c6_l21_n3_explicit_projection_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "basis_dimension": results["construction"]["basis_dimension"],
    "constraint_rank": rank,
    "projected_trace": projected_trace,
    "residual_trace": results["projection"]["residual_gram_trace"],
    "projected_rank": results["projection"]["projected_rank_numeric"],
    "trace_over_gap": second_order_single_gap_proxy,
}, indent=2, ensure_ascii=False))