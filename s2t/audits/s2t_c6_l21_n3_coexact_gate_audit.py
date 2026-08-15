import json
import math
from pathlib import Path

import numpy as np

DIM = 4
VOL_L21 = math.pi ** 2


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


def deriv_poly(p, idx):
    out = {}
    for mon, val in p.items():
        if mon[idx] == 0:
            continue
        new = list(mon)
        new[idx] -= 1
        out[tuple(new)] = out.get(tuple(new), 0.0) + val * mon[idx]
    return {m: v for m, v in out.items() if abs(v) > 1e-12}


def lap_poly(p):
    out = {}
    for i in range(DIM):
        out = add_poly(out, deriv_poly(deriv_poly(p, i), i))
    return out


def lin_poly(coeffs):
    return {tuple(1 if i == j else 0 for i in range(DIM)): float(c) for j, c in enumerate(coeffs) if abs(c) > 1e-12}


def quad_form_poly(B):
    out = {}
    for i in range(DIM):
        for j in range(DIM):
            coeff = float(B[i, j])
            if abs(coeff) < 1e-12:
                continue
            mon = [0] * DIM
            mon[i] += 1
            mon[j] += 1
            out[tuple(mon)] = out.get(tuple(mon), 0.0) + coeff
    return {m: v for m, v in out.items() if abs(v) > 1e-12}


def vector_lin(M):
    return [lin_poly(M[row, :]) for row in range(DIM)]


def vector_add(v, w, scale=1.0):
    return [add_poly(v[i], w[i], scale) for i in range(DIM)]


def vector_scale(v, scale):
    return [{m: scale * c for m, c in comp.items()} for comp in v]


def scalar_times_vector(s, v):
    return [mul_poly(s, comp) for comp in v]


def dot_x_vector(v):
    total = {}
    for i in range(DIM):
        total = add_poly(total, mul_poly(lin_poly([1 if k == i else 0 for k in range(DIM)]), v[i]))
    return total


def ambient_div(v):
    total = {}
    for i in range(DIM):
        total = add_poly(total, deriv_poly(v[i], i))
    return total


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


def integrate_poly_l21(p):
    return VOL_L21 * sum(coeff * sphere_expectation_monomial(mon) for mon, coeff in p.items())


def norm_poly_l21(p):
    return integrate_poly_l21(mul_poly(p, p))


def norm_vector_l21(v):
    total = {}
    for comp in v:
        total = add_poly(total, mul_poly(comp, comp))
    return integrate_poly_l21(total)


def max_coeff(p):
    return max([0.0] + [abs(v) for v in p.values()])


labels, basis = antisym_basis_4()
A = np.diag([1.0, -1.0, 0.0, 0.0])
q = quad_form_poly(A)
x_vec = [lin_poly([1 if i == j else 0 for j in range(DIM)]) for i in range(DIM)]

rows = []
for label, N in zip(labels, basis):
    Nx = vector_lin(N)
    NAx = vector_lin(N @ A)
    C = N.T @ A + A.T @ N
    Cx = vector_lin(C)
    f = quad_form_poly(C)
    V = vector_add(vector_scale(scalar_times_vector(q, Nx), -12.0), vector_scale(NAx, 4.0))
    V = vector_add(V, vector_scale(Cx, -2.0))
    V = vector_add(V, vector_scale(scalar_times_vector(f, x_vec), 2.0))

    tangent = dot_x_vector(V)
    div = ambient_div(V)
    comp_laps = [lap_poly(comp) for comp in V]
    rows.append({
        "basis": label,
        "norm_sq": norm_vector_l21(V),
        "tangency_max_coeff": max_coeff(tangent),
        "divergence_max_coeff": max_coeff(div),
        "divergence_norm_sq": norm_poly_l21(div),
        "component_laplacian_max_coeff": max(max_coeff(p) for p in comp_laps),
        "max_polynomial_degree": max(sum(mon) for comp in V for mon in comp),
    })

results = {
    "status": "n3_leakage_raw_image_requires_tangent_projection_before_coexact_claim",
    "source": "s2t_c6_l21_n1_to_n3_leakage_results.json",
    "tested_deformation": "A=diag(1,-1,0,0)",
    "gate_meaning": {
        "tangency": "x·V is tested before intrinsic tangent projection. Nonzero tangency means the ambient polynomial representative contains a normal component.",
        "coexactness": "ambient divergence of the raw representative is tested, but it is not sufficient when the tangency gate fails.",
        "degree": "max polynomial degree is cubic, matching the next allowed odd shell after n=1.",
    },
    "row_checks": rows,
    "summary": {
        "max_tangency_coeff": max(row["tangency_max_coeff"] for row in rows),
        "max_divergence_coeff": max(row["divergence_max_coeff"] for row in rows),
        "max_divergence_norm_sq": max(row["divergence_norm_sq"] for row in rows),
        "max_component_laplacian_coeff": max(row["component_laplacian_max_coeff"] for row in rows),
        "min_norm_sq": min(row["norm_sq"] for row in rows),
        "max_norm_sq": max(row["norm_sq"] for row in rows),
        "max_polynomial_degree": max(row["max_polynomial_degree"] for row in rows),
    },
    "interpretation": [
        {
            "claim": "the cubic leakage is already proven coexact",
            "verdict": "fails",
            "reason": "The raw ambient representative has a nonzero normal component, so an intrinsic tangent projection is mandatory before a coexact claim.",
        },
        {
            "claim": "the n=3 determinant contribution is now fully known",
            "verdict": "not_yet",
            "reason": "The raw leakage norm is nonzero, but the intrinsic tangent projection, coexact projection, and second-order denominator/sign trace still need to be assembled explicitly.",
        },
    ],
    "verdict": (
        "The cubic leakage from the n=1 Killing shell is nonzero, but the raw ambient representative fails the tangency gate because x·V is not zero. "
        "Therefore it cannot yet be called a coexact n=3 contribution. The next step is to form the intrinsic tangent projection, then test co-closedness and spectral n=3 projection."
    ),
}

Path("s2t_c6_l21_n3_coexact_gate_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "summary": results["summary"],
}, indent=2, ensure_ascii=False))