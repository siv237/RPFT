import json
import math
import numpy as np

N_MAX = 120
M_MAX = 120
BASELINE_WINDOW = [0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06]
ALPHAS = [0.0, 0.125, 0.25, 0.375, 0.5]


def build_spectrum(R3: float, R1: float, alpha: float):
    vals = []
    mult = []
    for n in range(N_MAX + 1):
        lam_s3 = ((n + 1.5) / R3) ** 2
        g = 2 * (n + 1) * (n + 2)
        for m in range(-M_MAX, M_MAX + 1):
            lam_s1 = ((m + alpha) / R1) ** 2
            vals.append(lam_s3 + lam_s1)
            mult.append(g)
    return np.array(vals, dtype=float), np.array(mult, dtype=float)


def heat_trace(vals, mult, t: float) -> float:
    return float(np.sum(mult * np.exp(-t * vals)))


def fit_coefficients(R3: float, R1: float, alpha: float, ts):
    vals, mult = build_spectrum(R3, R1, alpha)
    ts = np.array(ts, dtype=float)
    scaled = np.array([(4 * math.pi * t) ** 2 * heat_trace(vals, mult, float(t)) for t in ts], dtype=float)
    A = np.vstack([np.ones_like(ts), ts, ts**2]).T
    coef, *_ = np.linalg.lstsq(A, scaled, rcond=None)
    a0_fit, a2_fit, a4_fit = [float(x) for x in coef]
    a0_expected = 8 * math.pi**3 * (R3**3) * R1
    a2_expected = -4 * math.pi**3 * R3 * R1
    theta = 2 * math.pi * alpha
    gap = alpha / R1
    return {
        'alpha': alpha,
        'theta': theta,
        'theta_over_pi': theta / math.pi,
        'spin_structure_label': 'periodic' if alpha == 0.0 else ('antiperiodic' if alpha == 0.5 else 'twisted'),
        'a0_fit': a0_fit,
        'a2_fit': a2_fit,
        'a4_fit': a4_fit,
        'a0_expected': a0_expected,
        'a2_expected': a2_expected,
        'a0_rel_err': abs(a0_fit - a0_expected) / abs(a0_expected),
        'a2_rel_err': abs(a2_fit - a2_expected) / abs(a2_expected),
        'a2_over_4pi_fit': a2_fit / (4 * math.pi),
        'a2_over_4pi_expected': -math.pi**2 * R3 * R1,
        'wilson_phase': theta,
        'wilson_phase_over_pi': theta / math.pi,
        'circle_gap': gap,
        'circle_gap_times_pi': gap * math.pi,
    }


rows = [fit_coefficients(1.0, 1.0, alpha, BASELINE_WINDOW) for alpha in ALPHAS]

periodic = rows[0]
antiperiodic = rows[-1]
results = {
    'operator': 'Dirac-type squared spin/holonomy audit on S^3 x S^1',
    'truncation': {'n_max': N_MAX, 'm_max': M_MAX},
    'fit_window': BASELINE_WINDOW,
    'alpha_sweep': rows,
    'invariance_summary': {
        'max_a0_rel_err': max(row['a0_rel_err'] for row in rows),
        'max_a2_rel_err': max(row['a2_rel_err'] for row in rows),
        'a0_fit_spread': max(row['a0_fit'] for row in rows) - min(row['a0_fit'] for row in rows),
        'a2_fit_spread': max(row['a2_fit'] for row in rows) - min(row['a2_fit'] for row in rows),
    },
    'pi_sector_summary': {
        'periodic_theta': periodic['theta'],
        'antiperiodic_theta': antiperiodic['theta'],
        'antiperiodic_theta_equals_pi': abs(antiperiodic['theta'] - math.pi),
        'periodic_gap': periodic['circle_gap'],
        'antiperiodic_gap': antiperiodic['circle_gap'],
    },
}

with open('dirac_spin_holonomy_results.json', 'w', encoding='utf-8') as handle:
    json.dump(results, handle, ensure_ascii=False, indent=2)

print(json.dumps(results, ensure_ascii=False, indent=2))