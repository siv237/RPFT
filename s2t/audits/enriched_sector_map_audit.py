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
MU_HEAVY_VALUES = [0.0, 0.3, 0.6, 0.9]


def build_spectrum(beta: float, mu_heavy: float):
    sectors = [
        {"name": "q+_light", "q": 1.0, "mu": 0.0, "weight": 1.0},
        {"name": "q-_light", "q": -1.0, "mu": 0.0, "weight": 1.0},
        {"name": "q+_heavy", "q": 1.0, "mu": mu_heavy, "weight": 1.0},
        {"name": "q-_heavy", "q": -1.0, "mu": mu_heavy, "weight": 1.0},
    ]
    vals, mult = [], []
    for sector in sectors:
        shift = ALPHA + sector["q"] * beta
        for n in range(N_MAX + 1):
            lam_s3 = ((n + 1.5) / R3) ** 2
            g = 2 * (n + 1) * (n + 2) * sector["weight"]
            for m in range(-M_MAX, M_MAX + 1):
                lam_s1 = ((m + shift) / R1) ** 2
                vals.append(lam_s3 + lam_s1 + sector["mu"] ** 2)
                mult.append(g)
    return np.array(vals, dtype=float), np.array(mult, dtype=float)


def heat_trace(vals, mult, t: float) -> float:
    return float(np.sum(mult * np.exp(-t * vals)))


def fit_coeffs(beta: float, mu_heavy: float):
    vals, mult = build_spectrum(beta, mu_heavy)
    ts = np.array(TS, dtype=float)
    scaled = np.array([(4 * math.pi * t) ** 2 * heat_trace(vals, mult, float(t)) for t in ts], dtype=float)
    A = np.vstack([np.ones_like(ts), ts, ts**2]).T
    coef, *_ = np.linalg.lstsq(A, scaled, rcond=None)
    a0_fit, a2_fit, a4_fit = [float(x) for x in coef]
    multiplicity_factor = 4.0
    a0_expected = multiplicity_factor * 8 * math.pi**3
    curvature_part = multiplicity_factor * (-4 * math.pi**3)
    mass_loading = -8 * math.pi**3 * (2 * mu_heavy**2)
    a2_model = curvature_part + mass_loading
    return {
        "beta": beta,
        "mu_heavy": mu_heavy,
        "a0_fit": a0_fit,
        "a2_fit": a2_fit,
        "a4_fit": a4_fit,
        "a0_expected": a0_expected,
        "a2_model": a2_model,
        "a0_rel_err": abs(a0_fit - a0_expected) / abs(a0_expected),
        "a2_rel_err": abs(a2_fit - a2_model) / max(1.0, abs(a2_model)),
        "a2_over_4pi_fit": a2_fit / (4 * math.pi),
        "theta_plus_over_pi": 2 * (ALPHA + beta),
        "theta_minus_over_pi": 2 * (ALPHA - beta),
    }

rows = [fit_coeffs(beta, mu) for mu in MU_HEAVY_VALUES for beta in BETAS]
mu_trend = []
for mu in MU_HEAVY_VALUES:
    subset = [r for r in rows if r['mu_heavy'] == mu]
    mu_trend.append({
        'mu_heavy': mu,
        'mean_a2_fit': sum(r['a2_fit'] for r in subset) / len(subset),
        'mean_a2_over_4pi_fit': sum(r['a2_over_4pi_fit'] for r in subset) / len(subset),
    })
beta_trend = []
for beta in BETAS:
    subset = [r for r in rows if r['beta'] == beta]
    beta_trend.append({
        'beta': beta,
        'theta_plus_over_pi': 2 * (ALPHA + beta),
        'theta_minus_over_pi': 2 * (ALPHA - beta),
        'mean_a2_fit': sum(r['a2_fit'] for r in subset) / len(subset),
    })
results = {
    'operator': 'Enriched sector map audit',
    'geometry': {'R3': R3, 'R1': R1},
    'alpha': ALPHA,
    'betas': BETAS,
    'mu_heavy_values': MU_HEAVY_VALUES,
    'rows': rows,
    'mu_trend': mu_trend,
    'beta_trend': beta_trend,
    'max_a0_rel_err': max(r['a0_rel_err'] for r in rows),
    'max_a2_rel_err': max(r['a2_rel_err'] for r in rows),
}
with open('enriched_sector_map_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(json.dumps(results, ensure_ascii=False, indent=2))