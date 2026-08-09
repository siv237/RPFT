import json
import math
import numpy as np

N_MAX = 120
M_MAX = 120
TS = [0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06]
R3 = 1.0
R1 = 1.0
ALPHA = 0.5
BETAS = [0.0, 0.125, 0.25, 0.375, 0.5]
CHARGES = [-1.0, 1.0]


def build_gauge_holonomy_spectrum(R3: float, R1: float, alpha: float, beta: float):
    vals = []
    mult = []
    for n in range(N_MAX + 1):
        lam_s3 = ((n + 1.5) / R3) ** 2
        g = 2 * (n + 1) * (n + 2)
        for q in CHARGES:
            shift = alpha + q * beta
            for m in range(-M_MAX, M_MAX + 1):
                lam_s1 = ((m + shift) / R1) ** 2
                vals.append(lam_s3 + lam_s1)
                mult.append(g)
    return np.array(vals, dtype=float), np.array(mult, dtype=float)


def heat_trace(vals, mult, t: float) -> float:
    return float(np.sum(mult * np.exp(-t * vals)))


def nearest_distance_to_integer(x: float) -> float:
    return min(abs(x - round(x)), abs((x % 1.0) - round(x % 1.0)))


def circle_gap(alpha: float, beta: float, R1: float):
    gaps = []
    for q in CHARGES:
        shift = alpha + q * beta
        frac = shift - round(shift)
        gaps.append(abs(frac) / R1)
    return min(gaps)


def fit_row(beta: float):
    vals, mult = build_gauge_holonomy_spectrum(R3, R1, ALPHA, beta)
    ts = np.array(TS, dtype=float)
    scaled = np.array([(4 * math.pi * t) ** 2 * heat_trace(vals, mult, float(t)) for t in ts], dtype=float)
    A = np.vstack([np.ones_like(ts), ts, ts**2]).T
    coef, *_ = np.linalg.lstsq(A, scaled, rcond=None)
    a0_fit, a2_fit, a4_fit = [float(x) for x in coef]
    a0_expected = 16 * math.pi**3 * R3**3 * R1
    a2_expected = -8 * math.pi**3 * R3 * R1
    theta_plus = 2 * math.pi * (ALPHA + beta)
    theta_minus = 2 * math.pi * (ALPHA - beta)
    return {
        "alpha": ALPHA,
        "beta": beta,
        "theta_plus_over_pi": theta_plus / math.pi,
        "theta_minus_over_pi": theta_minus / math.pi,
        "a0_fit": a0_fit,
        "a2_fit": a2_fit,
        "a4_fit": a4_fit,
        "a0_expected": a0_expected,
        "a2_expected": a2_expected,
        "a0_rel_err": abs(a0_fit - a0_expected) / abs(a0_expected),
        "a2_rel_err": abs(a2_fit - a2_expected) / abs(a2_expected),
        "a2_over_4pi_fit": a2_fit / (4 * math.pi),
        "a2_over_4pi_expected": -2 * math.pi**2,
        "effective_circle_gap": circle_gap(ALPHA, beta, R1),
    }


rows = [fit_row(beta) for beta in BETAS]
results = {
    "operator": "Dirac-type with U(1)-like gauge holonomy doublet on S^3 x S^1",
    "parameters": {
        "R3": R3,
        "R1": R1,
        "alpha": ALPHA,
        "charges": CHARGES,
        "betas": BETAS,
        "n_max": N_MAX,
        "m_max": M_MAX,
        "fit_window": TS,
    },
    "beta_sweep": rows,
    "invariance_summary": {
        "max_a0_rel_err": max(r["a0_rel_err"] for r in rows),
        "max_a2_rel_err": max(r["a2_rel_err"] for r in rows),
        "a0_fit_spread": max(r["a0_fit"] for r in rows) - min(r["a0_fit"] for r in rows),
        "a2_fit_spread": max(r["a2_fit"] for r in rows) - min(r["a2_fit"] for r in rows),
        "gap_min": min(r["effective_circle_gap"] for r in rows),
        "gap_max": max(r["effective_circle_gap"] for r in rows),
    },
}

with open('gauge_holonomy_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(json.dumps(results, ensure_ascii=False, indent=2))