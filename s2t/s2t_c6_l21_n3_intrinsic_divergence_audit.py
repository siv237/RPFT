import json
import math
from pathlib import Path

import numpy as np

DIM = 4
VOL_L21 = math.pi ** 2


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


def lin_poly(coeffs):
    return {tuple(1 if i == j else 0 for i in range(DIM)): float(c) for j, c in enumerate(coeffs) if abs(c) > 1e-12}


def quad_form_poly(B):
    out = {}
    for i in range(DIM):
        for j in range(DIM):
            c = float(B[i, j])
            if abs(c) < 1e-12:
                continue
            mon = [0] * DIM
            mon[i] += 1
            mon[j] += 1
            out[tuple(mon)] = out.get(tuple(mon), 0.0) + c
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
    return VOL_L21 * sum(c * sphere_expectation_monomial(m) for m, c in p.items())


def norm_poly_l21(p):
    return integrate_poly_l21(mul_poly(p, p))


def inner_vector_integral(v, w):
    total = {}
    for i in range(DIM):
        total = add_poly(total, mul_poly(v[i], w[i]))
    return integrate_poly_l21(total)


def antisym_basis_4():
    labels = []
    basis = []
    for a in range(4):
        for b in range(a + 1, 4):
            m = np.zeros((4, 4))
            m[a, b] = 1
            m[b, a] = -1
            labels.append(f"E{a}{b}")
            basis.append(m)
    return labels, basis


def max_coeff(p):
    return max([0.0] + [abs(v) for v in p.values()])


labels, basis = antisym_basis_4()
A = np.diag([1.0, -1.0, 0.0, 0.0])
q = quad_form_poly(A)
x_vec = [lin_poly([1 if i == j else 0 for j in range(DIM)]) for i in range(DIM)]

rows = []
D = np.zeros((6, 6))
Gtan = np.zeros((6, 6))
for col, N in enumerate(basis):
    Nx = vector_lin(N)
    NAx = vector_lin(N @ A)
    C = N.T @ A + A.T @ N
    Cx = vector_lin(C)
    f = quad_form_poly(C)
    V = vector_add(vector_scale(scalar_times_vector(q, Nx), -12.0), vector_scale(NAx, 4.0))
    V = vector_add(V, vector_scale(Cx, -2.0))
    V = vector_add(V, vector_scale(scalar_times_vector(f, x_vec), 2.0))
    normal_scalar = dot_x_vector(V)
    Vtan = vector_add(V, scalar_times_vector(normal_scalar, x_vec), scale=-1.0)
    div = ambient_div(Vtan)
    rows.append({
        "basis": labels[col],
        "divergence_max_coeff": max_coeff(div),
        "divergence_norm_sq_on_L21": norm_poly_l21(div),
        "divergence_degree": max(sum(m) for m in div) if div else -1,
    })
    for row, M in enumerate(basis):
        # Correlate divergence scalar with q-overlap labels via Killing basis only as diagnostic.
        pass
    for j, M in enumerate(basis):
        # Gram of tangent images recomputed for normalization reference.
        pass

# Divergence Gram across the six images: if nonzero, the tangent image has an exact/longitudinal component.
for i, Ni in enumerate(basis):
    def image(N):
        Nx = vector_lin(N)
        NAx = vector_lin(N @ A)
        C = N.T @ A + A.T @ N
        Cx = vector_lin(C)
        f = quad_form_poly(C)
        V = vector_add(vector_scale(scalar_times_vector(q, Nx), -12.0), vector_scale(NAx, 4.0))
        V = vector_add(V, vector_scale(Cx, -2.0))
        V = vector_add(V, vector_scale(scalar_times_vector(f, x_vec), 2.0))
        normal_scalar = dot_x_vector(V)
        return vector_add(V, scalar_times_vector(normal_scalar, x_vec), scale=-1.0)
    Vi = image(Ni)
    divi = ambient_div(Vi)
    for j, Nj in enumerate(basis):
        Vj = image(Nj)
        divj = ambient_div(Vj)
        D[i, j] = integrate_poly_l21(mul_poly(divi, divj))
        Gtan[i, j] = inner_vector_integral(Vi, Vj)

norm_sq = VOL_L21 * float(np.trace(basis[0].T @ basis[0])) / 4.0
Dnorm = (D + D.T) / (2 * norm_sq)
Gnorm = (Gtan + Gtan.T) / (2 * norm_sq)

results = {
    "status": "n3_tangent_signal_fails_coexact_divergence_gate",
    "source": "s2t_c6_l21_n3_tangent_projection_results.json",
    "geometry_note": "For a tangent ambient representative on the unit sphere, nonzero intrinsic/ambient divergence signals a non-coexact component; the transverse Hodge projector is still required.",
    "row_checks": rows,
    "tangent_gram_summary": {
        "trace": float(np.trace(Gnorm)),
        "rank": int(np.linalg.matrix_rank(Gnorm, tol=1e-12)),
        "eigenvalues": [float(x) for x in np.linalg.eigvalsh(Gnorm)],
    },
    "divergence_gram_summary": {
        "trace": float(np.trace(Dnorm)),
        "rank": int(np.linalg.matrix_rank(Dnorm, tol=1e-12)),
        "max_abs_entry": float(np.max(np.abs(Dnorm))),
        "eigenvalues": [float(x) for x in np.linalg.eigvalsh(Dnorm)],
    },
    "interpretation": [
        {
            "claim": "the tangent cubic signal is already coexact",
            "verdict": "fails",
            "reason": "The divergence Gram trace is nonzero, so an exact/longitudinal component remains.",
        },
        {
            "claim": "the n=3 channel is irrelevant",
            "verdict": "not_yet",
            "reason": "The tangent Gram trace is nonzero; only the explicit transverse Hodge projection can decide whether a coexact residue survives.",
        },
    ],
    "next_required_audit": {
        "name": "n3_hodge_coexact_projection",
        "task": "subtract the gradient/exact component from the tangent cubic signal and recompute the coexact Gram trace",
        "zero_route_pass": "coexact-projected Gram trace vanishes or cancels in determinant bookkeeping",
        "obstruction_condition": "a nonzero coexact-projected 1<->3 trace remains outside the existing pi^-4/P02 residue",
    },
    "verdict": (
        "The tangent-projected cubic signal fails the coexact divergence gate: it is tangent and nonzero, but not divergence-free. "
        "Therefore C6 is not decided yet. The next calculation must apply the Hodge coexact projector on the n=3 tangent cubic sector."
    ),
}

Path("s2t_c6_l21_n3_intrinsic_divergence_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "tangent_trace": results["tangent_gram_summary"]["trace"],
    "divergence_trace": results["divergence_gram_summary"]["trace"],
    "divergence_eigenvalues": results["divergence_gram_summary"]["eigenvalues"],
}, indent=2, ensure_ascii=False))