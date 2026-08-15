import json
import math
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np

VOL_L21 = math.pi ** 2
DIM = 4
LAMBDA_1 = 4.0
LAMBDA_3 = 16.0


def antisym_basis_4():
    basis = []
    labels = []
    for a in range(4):
        for b in range(a + 1, 4):
            m = np.zeros((4, 4), dtype=float)
            m[a, b] = 1.0
            m[b, a] = -1.0
            basis.append(m)
            labels.append(f"E{a}{b}")
    return labels, basis


def add_poly(p, q, scale=1.0):
    out = dict(p)
    for mon, val in q.items():
        out[mon] = out.get(mon, 0.0) + scale * val
        if abs(out[mon]) < 1e-14:
            del out[mon]
    return out


def mul_poly(p, q):
    out = {}
    for a, va in p.items():
        for b, vb in q.items():
            mon = tuple(a[i] + b[i] for i in range(DIM))
            out[mon] = out.get(mon, 0.0) + va * vb
    return {m: v for m, v in out.items() if abs(v) > 1e-14}


def lin_poly(coeffs):
    return {tuple(1 if i == j else 0 for i in range(DIM)): float(c) for j, c in enumerate(coeffs) if abs(c) > 1e-14}


def quad_form_poly(B):
    out = {}
    for i in range(DIM):
        for j in range(DIM):
            coeff = float(B[i, j])
            if abs(coeff) < 1e-14:
                continue
            mon = [0] * DIM
            mon[i] += 1
            mon[j] += 1
            out[tuple(mon)] = out.get(tuple(mon), 0.0) + coeff
    return {m: v for m, v in out.items() if abs(v) > 1e-14}


def vector_lin(M):
    return [lin_poly(M[row, :]) for row in range(DIM)]


def vector_add(v, w, scale=1.0):
    return [add_poly(v[i], w[i], scale) for i in range(DIM)]


def vector_scale(v, scale):
    return [{m: scale * c for m, c in comp.items()} for comp in v]


def scalar_times_vector(s, v):
    return [mul_poly(s, comp) for comp in v]


def sphere_expectation_monomial(mon):
    total = sum(mon)
    if any(k % 2 for k in mon):
        return 0.0
    if total == 0:
        return 1.0
    # For S^{d-1}: E[x_1^{2a1}...] = prod((2ai-1)!!)/d(d+2)...(d+2A-2).
    numerator = 1.0
    A = total // 2
    for k in mon:
        a = k // 2
        odd_df = 1
        for r in range(1, 2 * a, 2):
            odd_df *= r
        numerator *= odd_df
    denom = 1.0
    for r in range(A):
        denom *= DIM + 2 * r
    return numerator / denom


def integrate_poly_l21(p):
    return VOL_L21 * sum(coeff * sphere_expectation_monomial(mon) for mon, coeff in p.items())


def inner_vector_integral(v, w):
    total = {}
    for i in range(DIM):
        total = add_poly(total, mul_poly(v[i], w[i]))
    return integrate_poly_l21(total)


labels, basis = antisym_basis_4()
A = np.diag([1.0, -1.0, 0.0, 0.0])
q = quad_form_poly(A)
x_vec = [lin_poly([1 if i == j else 0 for j in range(DIM)]) for i in range(DIM)]

images = []
for N in basis:
    Nx = vector_lin(N)
    NAx = vector_lin(N @ A)
    C = N.T @ A + A.T @ N
    Cx = vector_lin(C)
    f = quad_form_poly(C)
    # Full conformal Hodge variation image on a Killing one-form after n=1 cancellation:
    # V_N = -12 q N x +4 N A x -2 C x + 2 f x.
    V = vector_add(vector_scale(scalar_times_vector(q, Nx), -12.0), vector_scale(NAx, 4.0))
    V = vector_add(V, vector_scale(Cx, -2.0))
    V = vector_add(V, vector_scale(scalar_times_vector(f, x_vec), 2.0))
    images.append(V)

G = np.zeros((6, 6), dtype=float)
for i, Vi in enumerate(images):
    for j, Vj in enumerate(images):
        G[i, j] = inner_vector_integral(Vi, Vj)

norm_sq = VOL_L21 * float(np.trace(basis[0].T @ basis[0])) / 4.0
G_normalized = G / norm_sq
sym = (G_normalized + G_normalized.T) / 2.0

# Projection back to n=1 should vanish; verify against Killing basis.
proj = np.zeros((6, 6), dtype=float)
for i, M in enumerate(basis):
    Mx = vector_lin(M)
    for j, Vj in enumerate(images):
        proj[i, j] = inner_vector_integral(Mx, Vj) / norm_sq

# If the image is entirely in the n=3 shell, second-order mixing scale from n=1 to n=3 has denominator lambda1-lambda3.
trace_image_norm = float(np.trace(sym))
second_order_proxy = trace_image_norm / ((LAMBDA_3 - LAMBDA_1) ** 2)
weighted_by_lambda1 = trace_image_norm / (LAMBDA_1 ** 2)

results = {
    "status": "n1_conformal_hodge_diagonal_cancellation_leaks_to_cubic_shell",
    "formula_for_image": "V_N = -12 q N x +4 N A x -2 C_N x + 2 f_N x, C_N=N^T A + A^T N, f_N=x^T C_N x",
    "basis_labels": labels,
    "tested_deformation": "A=diag(1,-1,0,0)",
    "normalization": {"killing_norm_sq_on_L21": norm_sq},
    "n1_projection_summary": {
        "max_abs_entry": float(np.max(np.abs(proj))),
        "frobenius_norm": float(np.linalg.norm(proj, ord="fro")),
    },
    "image_gram_summary": {
        "rank_numeric": int(np.linalg.matrix_rank(sym, tol=1e-12)),
        "trace_image_norm": trace_image_norm,
        "max_abs_entry": float(np.max(np.abs(sym))),
        "frobenius_norm": float(np.linalg.norm(sym, ord="fro")),
        "eigenvalues": [float(x) for x in np.linalg.eigvalsh(sym)],
        "weighted_by_lambda1_trace_norm": weighted_by_lambda1,
        "second_order_denominator_proxy_lambda3_minus_lambda1": second_order_proxy,
    },
    "matrices": {
        "n1_projection_matrix": proj.tolist(),
        "normalized_image_gram_matrix": sym.tolist(),
    },
    "interpretation": [
        {
            "claim": "the n=1 diagonal cancellation means the perturbation vanishes",
            "verdict": "fails",
            "reason": "The n=1 projection is zero, but the cubic image has nonzero norm; the operator sends the Killing shell into higher shell content.",
        },
        {
            "claim": "this proves a determinant obstruction",
            "verdict": "not_yet",
            "reason": "The image is represented as cubic tangent polynomials; it still needs projection onto the orthonormal coexact n=3 eigenspace and denominator/sign bookkeeping in the full second-order trace.",
        },
    ],
    "next_required_audit": {
        "name": "n1_to_n3_coexact_projection",
        "needed": "construct or numerically orthonormalize the coexact n=3 basis and project the cubic images onto it",
        "pass_condition_for_zero_route": "projected n=3 component vanishes or cancels against projection/Hilbert terms",
        "failure_condition": "nonzero finite 1<->3 trace-square remains outside the existing pi^-4/P02 residue",
    },
    "verdict": (
        "The conformal Hodge variation cancels inside the n=1 diagonal block, but it does not vanish as an operator on Killing forms. "
        "Its n=1 projection is zero to roundoff while its cubic tangent-polynomial image has nonzero normalized Gram trace. "
        "Thus the next decisive C6 test is the actual coexact n=3 projection and second-order 1<->3 trace contribution."
    ),
}

Path("s2t_c6_l21_n1_to_n3_leakage_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "n1_projection_max_abs": results["n1_projection_summary"]["max_abs_entry"],
    "image_rank": results["image_gram_summary"]["rank_numeric"],
    "trace_image_norm": trace_image_norm,
    "eigenvalues": results["image_gram_summary"]["eigenvalues"],
}, indent=2, ensure_ascii=False))