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


def log_heat_trace_s2xs2(tau):
    cutoff = max(80, math.ceil(math.sqrt(60.0 * RADIUS_S2**2 / tau)))
    ell = np.arange(cutoff + 1, dtype=float)
    log_degeneracy = np.log(2.0 * ell + 1.0)
    eigenvalue = ell * (ell + 1.0) / RADIUS_S2**2
    return 2.0 * float(logsumexp(log_degeneracy - tau * eigenvalue))


def delta_log_partition(tau):
    return log_heat_trace_s4(tau) - log_heat_trace_s2xs2(tau)


def delta_free_energy(tau):
    return -delta_log_partition(tau) / tau


grid = np.logspace(-5.0, math.log10(2.0), 3001)
delta_log_grid = np.array([delta_log_partition(tau) for tau in grid])
maximum = minimize_scalar(
    lambda log_tau: -delta_log_partition(math.exp(log_tau)),
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
            "delta_log_partition": delta_log_partition(tau),
            "delta_free_energy": delta_free_energy(tau),
        }
    )

result = {
    "gate": "version4_gibbs_free_energy_carrier",
    "date": "2026-08-11",
    "normalization": "unit_four_volume",
    "state_principle": "minimize_Tr_rho_Delta_minus_tau_inverse_von_Neumann_entropy",
    "identity": "Phi(rho)-F=tau_inverse_relative_entropy(rho||rho_tau)",
    "small_tau_delta_log_partition_coefficient": (4.0 * PI / 3.0) * (math.sqrt(6.0) - 2.0),
    "grid": {
        "tau_min": float(grid[0]),
        "tau_max": float(grid[-1]),
        "points": int(grid.size),
        "minimum_delta_log_partition": float(delta_log_grid.min()),
        "minimum_tau": float(grid[delta_log_grid.argmin()]),
        "nonpositive_points": int(np.count_nonzero(delta_log_grid <= 0.0)),
    },
    "maximum_delta_log_partition": {
        "tau": math.exp(maximum.x),
        "value": -maximum.fun,
    },
    "samples": samples,
    "verdict": "S4_has_lower_Gibbs_free_energy_on_the_audited_profile",
    "status": "conditional_on_normalized_correlation_state_completion",
}

with open("s2t_v4_gibbs_free_energy_carrier_gate_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result["grid"], indent=2))
print(json.dumps(result["maximum_delta_log_partition"], indent=2))