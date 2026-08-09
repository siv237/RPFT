import json
import math
import numpy as np

R3 = 1.0
R1 = 1.0
N_MAX = 80
M_MAX = 80

vals = []
mult = []
for n in range(N_MAX + 1):
    lam_s3 = n * (n + 2) / R3**2
    g = (n + 1) ** 2
    for m in range(-M_MAX, M_MAX + 1):
        lam = lam_s3 + (m / R1) ** 2
        vals.append(lam)
        mult.append(g)

vals = np.array(vals, dtype=float)
mult = np.array(mult, dtype=float)

def heat_trace(t: float) -> float:
    return float(np.sum(mult * np.exp(-t * vals)))

ts = np.array([0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06], dtype=float)
scaled = np.array([(4 * np.pi * t) ** 2 * heat_trace(float(t)) for t in ts], dtype=float)
A = np.vstack([np.ones_like(ts), ts, ts**2]).T
coef, *_ = np.linalg.lstsq(A, scaled, rcond=None)
a0_fit, a2_fit, a4_fit = [float(x) for x in coef]

results = {
    "manifold": "S^3 x S^1",
    "operator": "scalar Laplacian heat trace",
    "radii": {"R3": R3, "R1": R1},
    "truncation": {"n_max": N_MAX, "m_max": M_MAX},
    "fit_window": ts.tolist(),
    "a0_fit": a0_fit,
    "a2_fit": a2_fit,
    "a4_fit": a4_fit,
    "a0_expected": 4 * math.pi**3,
    "a2_expected": 4 * math.pi**3,
    "a2_over_4pi_fit": a2_fit / (4 * math.pi),
    "a2_over_4pi_expected": math.pi**2,
    "systole_s1": 2 * math.pi * R1,
    "pi_proxy_from_systole": (2 * math.pi * R1) / 2,
    "scaled_trace_data": [
        {"t": float(t), "scaled_trace": float(y)} for t, y in zip(ts, scaled)
    ],
}

with open('spectral_bridge_results.json', 'w', encoding='utf-8') as handle:
    json.dump(results, handle, ensure_ascii=False, indent=2)

print(json.dumps(results, ensure_ascii=False, indent=2))