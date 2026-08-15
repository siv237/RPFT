import json
import math

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import logsumexp


PI = math.pi
RADIUS_S4 = (3.0 / (8.0 * PI**2)) ** 0.25
RADIUS_S2 = (1.0 / (16.0 * PI**2)) ** 0.25


def log_heat_trace_s4(tau):
    cutoff = max(80, math.ceil(math.sqrt(60.0 * RADIUS_S4**2 / tau)))
    ell = np.arange(cutoff + 1, dtype=float)
    log_degeneracy = np.log((ell + 1.0) * (ell + 2.0) * (2.0 * ell + 3.0) / 6.0)
    eigenvalue = ell * (ell + 3.0) / RADIUS_S4**2
    return float(logsumexp(log_degeneracy - tau * eigenvalue))


def log_heat_trace_s2(tau):
    cutoff = max(80, math.ceil(math.sqrt(60.0 * RADIUS_S2**2 / tau)))
    ell = np.arange(cutoff + 1, dtype=float)
    log_degeneracy = np.log(2.0 * ell + 1.0)
    eigenvalue = ell * (ell + 1.0) / RADIUS_S2**2
    return float(logsumexp(log_degeneracy - tau * eigenvalue))


def renyi2_s4(tau):
    return 2.0 * log_heat_trace_s4(tau) - log_heat_trace_s4(2.0 * tau)


def renyi2_s2xs2(tau):
    return 2.0 * (2.0 * log_heat_trace_s2(tau) - log_heat_trace_s2(2.0 * tau))


def delta_renyi2(tau):
    return renyi2_s4(tau) - renyi2_s2xs2(tau)


grid = np.logspace(-5.0, math.log10(2.0), 3001)
delta_grid = np.array([delta_renyi2(tau) for tau in grid])
maximum = minimize_scalar(
    lambda log_tau: -delta_renyi2(math.exp(log_tau)),
    bounds=(math.log(1.0e-5), math.log(2.0)),
    method="bounded",
    options={"xatol": 1.0e-13},
)

sample_taus = [1.0e-5, 1.0e-4, 1.0e-3, 1.0e-2, 0.05, 0.1, math.exp(maximum.x), 0.2, 0.5, 1.0, 2.0]
samples = []
for tau in sample_taus:
    samples.append(
        {
            "tau": tau,
            "renyi2_s4": renyi2_s4(tau),
            "renyi2_s2xs2": renyi2_s2xs2(tau),
            "delta": delta_renyi2(tau),
        }
    )

result = {
    "gate": "version4_s4_s2xs2_correlation_purity",
    "date": "2026-08-11",
    "normalization": "unit_four_volume",
    "radii": {"s4": RADIUS_S4, "s2_factor": RADIUS_S2},
    "scalar_curvatures": {
        "s4": 12.0 / RADIUS_S4**2,
        "s2xs2": 4.0 / RADIUS_S2**2,
    },
    "first_positive_eigenvalues": {
        "s4": {"lambda": 4.0 / RADIUS_S4**2, "degeneracy": 5},
        "s2xs2": {"lambda": 2.0 / RADIUS_S2**2, "degeneracy": 6},
    },
    "small_tau_delta_coefficient": 16.0 * PI**2 / 15.0,
    "grid": {
        "tau_min": float(grid[0]),
        "tau_max": float(grid[-1]),
        "points": int(grid.size),
        "minimum_delta": float(delta_grid.min()),
        "minimum_tau": float(grid[delta_grid.argmin()]),
        "crossings_found": int(np.count_nonzero(delta_grid <= 0.0)),
    },
    "maximum": {"tau": math.exp(maximum.x), "delta": -maximum.fun},
    "samples": samples,
    "verdict": "S4_has_larger_Renyi2_entropy_on_the_audited_profile",
    "interpretive_status": "ordering_not_dynamic_selection",
}

with open("s2t_v4_s4_s2xs2_correlation_purity_gate_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result["grid"], indent=2))
print(json.dumps(result["maximum"], indent=2))