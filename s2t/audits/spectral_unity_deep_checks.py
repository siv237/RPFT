import json
import math
import numpy as np

N_MAX = 100
M_MAX = 100


def build_spectrum(R3: float, R1: float):
    vals = []
    mult = []
    for n in range(N_MAX + 1):
        lam_s3 = n * (n + 2) / (R3 ** 2)
        g = (n + 1) ** 2
        for m in range(-M_MAX, M_MAX + 1):
            lam = lam_s3 + (m / R1) ** 2
            vals.append(lam)
            mult.append(g)
    return np.array(vals, dtype=float), np.array(mult, dtype=float)


def heat_trace(vals, mult, t: float) -> float:
    return float(np.sum(mult * np.exp(-t * vals)))


def fit_heat_coefficients(R3: float, R1: float, ts):
    vals, mult = build_spectrum(R3, R1)
    ts = np.array(ts, dtype=float)
    scaled = np.array([(4 * math.pi * t) ** 2 * heat_trace(vals, mult, float(t)) for t in ts], dtype=float)
    A = np.vstack([np.ones_like(ts), ts, ts ** 2]).T
    coef, *_ = np.linalg.lstsq(A, scaled, rcond=None)
    a0_fit, a2_fit, a4_fit = [float(x) for x in coef]
    a0_expected = 4 * math.pi ** 3 * (R3 ** 3) * R1
    a2_expected = 4 * math.pi ** 3 * R3 * R1
    return {
        "radii": {"R3": R3, "R1": R1},
        "fit_window": ts.tolist(),
        "a0_fit": a0_fit,
        "a2_fit": a2_fit,
        "a4_fit": a4_fit,
        "a0_expected": a0_expected,
        "a2_expected": a2_expected,
        "a0_rel_err": abs(a0_fit - a0_expected) / a0_expected,
        "a2_rel_err": abs(a2_fit - a2_expected) / a2_expected,
        "a2_over_4pi_fit": a2_fit / (4 * math.pi),
        "a2_over_4pi_expected": math.pi ** 2 * R3 * R1,
        "pi_proxy_from_systole": math.pi * R1,
        "scaled_trace_data": [
            {"t": float(t), "scaled_trace": float(y)} for t, y in zip(ts, scaled)
        ],
    }


def spectral_action(vals, mult, Lambda: float, kind: str, param: float) -> float:
    x = vals / (Lambda ** 2)
    if kind == "exp":
        f = np.exp(-param * x)
    elif kind == "cauchy":
        f = (1.0 + x) ** (-param)
    else:
        raise ValueError(kind)
    return float(np.sum(mult * f))


def kernel_family_checks(R3: float, R1: float):
    vals, mult = build_spectrum(R3, R1)
    kernels = [
        {"kind": "exp", "param": 1.0, "label": "exp(-x)"},
        {"kind": "exp", "param": 2.0, "label": "exp(-2x)"},
        {"kind": "cauchy", "param": 3.0, "label": "(1+x)^(-3)"},
        {"kind": "cauchy", "param": 4.0, "label": "(1+x)^(-4)"},
    ]
    lambdas = [6.0, 8.0, 10.0, 12.0]
    rows = []
    for kernel in kernels:
        values = []
        for Lambda in lambdas:
            action = spectral_action(vals, mult, Lambda, kernel["kind"], kernel["param"])
            volume_normalized = action / (Lambda ** 4 * (R3 ** 3) * R1)
            values.append({
                "Lambda": Lambda,
                "action": action,
                "volume_normalized": volume_normalized,
            })
        rows.append({
            "kernel": kernel,
            "values": values,
            "spread_volume_normalized": max(v["volume_normalized"] for v in values) - min(v["volume_normalized"] for v in values),
        })
    return rows


baseline_window = [0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06]
window_checks = {
    "narrow": [0.02, 0.025, 0.03, 0.035, 0.04],
    "baseline": baseline_window,
    "wide": [0.04, 0.05, 0.06, 0.07, 0.08],
}

radius_grid = [
    (1.0, 1.0),
    (1.2, 1.0),
    (1.0, 1.3),
    (1.5, 0.8),
    (0.8, 1.5),
]

results = {
    "operator": "scalar Laplacian heat-trace deep unity audit",
    "truncation": {"n_max": N_MAX, "m_max": M_MAX},
    "window_stability": {
        name: fit_heat_coefficients(1.0, 1.0, ts) for name, ts in window_checks.items()
    },
    "radius_sweep": [fit_heat_coefficients(R3, R1, baseline_window) for R3, R1 in radius_grid],
    "kernel_family": kernel_family_checks(1.0, 1.0),
}

with open('spectral_unity_deep_results.json', 'w', encoding='utf-8') as handle:
    json.dump(results, handle, ensure_ascii=False, indent=2)

print(json.dumps(results, ensure_ascii=False, indent=2))