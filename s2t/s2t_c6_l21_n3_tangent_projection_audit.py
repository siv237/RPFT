import json
import math

import numpy as np
from pathlib import Path

DIM = 4
VOL_L21 = math.pi ** 2

# Polynomial helpers: monomial tuple -> coefficient.
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
        new = list(mon); new[idx] -= 1
        out[tuple(new)] = out.get(tuple(new), 0.0) + val * mon[idx]
    return {m: v for m, v in out.items() if abs(v) > 1e-12}

def lin_poly(coeffs):
    return {tuple(1 if i == j else 0 for i in range(DIM)): float(c) for j, c in enumerate(coeffs) if abs(c) > 1e-12}

def quad_form_poly(B):
    out = {}
    for i in range(DIM):
        for j in range(DIM):
            c = float(B[i, j])
            if abs(c) < 1e-12: continue
            mon = [0]*DIM; mon[i]+=1; mon[j]+=1
            out[tuple(mon)] = out.get(tuple(mon), 0.0) + c
    return {m:v for m,v in out.items() if abs(v)>1e-12}

def vector_lin(M):
    return [lin_poly(M[row, :]) for row in range(DIM)]

def vector_add(v, w, scale=1.0):
    return [add_poly(v[i], w[i], scale) for i in range(DIM)]

def vector_scale(v, scale):
    return [{m: scale*c for m,c in comp.items()} for comp in v]

def scalar_times_vector(s, v):
    return [mul_poly(s, comp) for comp in v]

def dot_x_vector(v):
    total = {}
    for i in range(DIM):
        total = add_poly(total, mul_poly(lin_poly([1 if k==i else 0 for k in range(DIM)]), v[i]))
    return total

def ambient_div(v):
    total = {}
    for i in range(DIM):
        total = add_poly(total, deriv_poly(v[i], i))
    return total

def sphere_expectation_monomial(mon):
    total = sum(mon)
    if any(k % 2 for k in mon): return 0.0
    if total == 0: return 1.0
    numerator = 1.0; half = total // 2
    for k in mon:
        a = k // 2; odd_df = 1
        for r in range(1, 2*a, 2): odd_df *= r
        numerator *= odd_df
    denom = 1.0
    for r in range(half): denom *= DIM + 2*r
    return numerator / denom

def integrate_poly_l21(p):
    return VOL_L21 * sum(c * sphere_expectation_monomial(m) for m,c in p.items())

def inner_vector_integral(v, w):
    total = {}
    for i in range(DIM): total = add_poly(total, mul_poly(v[i], w[i]))
    return integrate_poly_l21(total)

def norm_vector_l21(v):
    return inner_vector_integral(v, v)

def max_coeff(p):
    return max([0.0] + [abs(v) for v in p.values()])

def antisym_basis_4():
    labels=[]; basis=[]
    for a in range(4):
        for b in range(a+1,4):
            m=np.zeros((4,4)); m[a,b]=1; m[b,a]=-1
            labels.append(f'E{a}{b}'); basis.append(m)
    return labels,basis

labels,basis=antisym_basis_4()
A=np.diag([1.,-1.,0.,0.])
q=quad_form_poly(A)
x_vec=[lin_poly([1 if i==j else 0 for j in range(DIM)]) for i in range(DIM)]

raw_images=[]; tan_images=[]
for N in basis:
    Nx=vector_lin(N); NAx=vector_lin(N@A)
    C=N.T@A + A.T@N; Cx=vector_lin(C); f=quad_form_poly(C)
    V=vector_add(vector_scale(scalar_times_vector(q,Nx),-12.0), vector_scale(NAx,4.0))
    V=vector_add(V, vector_scale(Cx,-2.0))
    V=vector_add(V, vector_scale(scalar_times_vector(f,x_vec),2.0))
    normal_scalar=dot_x_vector(V)
    Vtan=vector_add(V, scalar_times_vector(normal_scalar, x_vec), scale=-1.0)  # since |x|=1 on S3
    raw_images.append(V); tan_images.append(Vtan)

raw_tangencies=[max_coeff(dot_x_vector(v)) for v in raw_images]
tan_tangencies=[max_coeff(dot_x_vector(v)) for v in tan_images]
tan_tangency_norms=[integrate_poly_l21(mul_poly(dot_x_vector(v), dot_x_vector(v))) for v in tan_images]
tan_divs=[max_coeff(ambient_div(v)) for v in tan_images]

G=np.zeros((6,6)); Gtan=np.zeros((6,6))
for i in range(6):
    for j in range(6):
        G[i,j]=inner_vector_integral(raw_images[i], raw_images[j])
        Gtan[i,j]=inner_vector_integral(tan_images[i], tan_images[j])

norm_sq = VOL_L21 * float(np.trace(basis[0].T @ basis[0])) / 4.0
Gnorm=(G+G.T)/(2*norm_sq); Gtnorm=(Gtan+Gtan.T)/(2*norm_sq)

results={
    "status":"n3_tangent_projection_removes_normal_component_on_sphere_but_not_coexact_gate",
    "source":"s2t_c6_l21_n3_coexact_gate_results.json",
    "projection":"V_tan = V - (x·V)x on |x|=1; polynomial x·V_tan may be proportional to 1-|x|^2 and is tested by sphere norm",
    "raw_tangency_max_coeff": max(raw_tangencies),
    "tangent_projected_tangency_max_coeff_ambient_polynomial": max(tan_tangencies),
    "tangent_projected_tangency_norm_on_sphere": max(tan_tangency_norms),
    "tangent_projected_ambient_divergence_max_coeff": max(tan_divs),
    "raw_gram_summary": {
        "trace": float(np.trace(Gnorm)),
        "rank": int(np.linalg.matrix_rank(Gnorm, tol=1e-12)),
        "eigenvalues": [float(x) for x in np.linalg.eigvalsh(Gnorm)],
    },
    "tangent_projected_gram_summary": {
        "trace": float(np.trace(Gtnorm)),
        "rank": int(np.linalg.matrix_rank(Gtnorm, tol=1e-12)),
        "eigenvalues": [float(x) for x in np.linalg.eigvalsh(Gtnorm)],
    },
    "interpretation":[
        {"claim":"normal component explains all cubic leakage","verdict":"fails","reason":"after tangent projection the Gram trace remains nonzero."},
        {"claim":"tangent projection is already coexact","verdict":"not_yet","reason":"ambient divergence of the tangent-projected representative is nonzero; intrinsic divergence/coexact projection must be computed."},
    ],
    "verdict":"The normal component is not the whole story: tangent projection removes x·V on the unit sphere and leaves a nonzero tangent cubic signal. However the tangent-projected ambient divergence is nonzero, so this is still not a completed coexact n=3 projection. Next step: compute intrinsic divergence/coexact projection on S3/RP3."
}
Path('s2t_c6_l21_n3_tangent_projection_results.json').write_text(json.dumps(results, indent=2, ensure_ascii=False)+'\n')
print(json.dumps({"status":results["status"],"raw_tangency":results["raw_tangency_max_coeff"],"tan_tangency_coeff":results["tangent_projected_tangency_max_coeff_ambient_polynomial"],"tan_tangency_sphere_norm":results["tangent_projected_tangency_norm_on_sphere"],"tan_div":results["tangent_projected_ambient_divergence_max_coeff"],"tan_trace":results["tangent_projected_gram_summary"]["trace"],"tan_eigs":results["tangent_projected_gram_summary"]["eigenvalues"]}, indent=2, ensure_ascii=False))