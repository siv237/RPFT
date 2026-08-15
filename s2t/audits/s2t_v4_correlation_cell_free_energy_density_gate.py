import json
import math

import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp


PI = math.pi


def moments_s4(radius_ratio):
    cutoff = max(100, math.ceil(radius_ratio * math.sqrt(100.0)))
    ell = np.arange(cutoff + 1, dtype=float)
    degeneracy = (ell + 1.0) * (ell + 2.0) * (2.0 * ell + 3.0) / 6.0
    mu = ell * (ell + 3.0)
    log_weight = np.log(degeneracy) - mu / radius_ratio**2
    log_partition = float(logsumexp(log_weight))
    probability = np.exp(log_weight - log_partition)
    mean = float(np.sum(probability * mu))
    second = float(np.sum(probability * mu**2))
    return log_partition, mean, second - mean**2


def moments_s2xs2(radius_ratio):
    cutoff = max(100, math.ceil(radius_ratio * math.sqrt(100.0)))
    ell = np.arange(cutoff + 1, dtype=float)
    degeneracy = 2.0 * ell + 1.0
    mu = ell * (ell + 1.0)
    log_weight = np.log(degeneracy) - mu / radius_ratio**2
    log_partition_s2 = float(logsumexp(log_weight))
    probability = np.exp(log_weight - log_partition_s2)
    mean_s2 = float(np.sum(probability * mu))
    second_s2 = float(np.sum(probability * mu**2))
    variance_s2 = second_s2 - mean_s2**2
    return 2.0 * log_partition_s2, 2.0 * mean_s2, 2.0 * variance_s2


def audit_candidate(name, volume_coefficient, moments):
    def density(radius_ratio):
        log_partition, _, _ = moments(radius_ratio)
        return -log_partition / (volume_coefficient * radius_ratio**4)

    def derivative(radius_ratio):
        log_partition, mean, _ = moments(radius_ratio)
        return (4.0 * log_partition - 2.0 * mean / radius_ratio**2) / (
            volume_coefficient * radius_ratio**5
        )

    root = brentq(derivative, 0.5, 2.0, xtol=1.0e-14)
    log_partition, mean, variance = moments(root)
    hessian = 4.0 * (3.0 * mean * root**2 - variance) / (
        volume_coefficient * root**10
    )
    return {
        "name": name,
        "radius_over_sigma": root,
        "dimensionless_density": density(root),
        "log_partition": log_partition,
        "mean_dimensionless_eigenvalue": mean,
        "variance_dimensionless_eigenvalue": variance,
        "hessian": hessian,
        "stationarity_residual": mean / root**2 - 2.0 * log_partition,
        "scalar_curvature_times_sigma_squared": (
            12.0 / root**2 if name == "S4" else 4.0 / root**2
        ),
    }


candidates = [
    audit_candidate("S4", 8.0 * PI**2 / 3.0, moments_s4),
    audit_candidate("S2xS2", 16.0 * PI**2, moments_s2xs2),
]

result = {
    "gate": "version4_correlation_cell_free_energy_density",
    "date": "2026-08-11",
    "functional": "tau^3 F/V=-tau^2 log(Z)/V",
    "dimensionless_radius": "r=a/sqrt(tau)=a/sigma",
    "stationarity_condition": "<mu>/r^2=2 log Z",
    "equation_of_state_at_stationarity": "p=-epsilon",
    "candidates": candidates,
    "winner": min(candidates, key=lambda candidate: candidate["dimensionless_density"])["name"],
    "status": "conditional_scale_ratio_selection",
    "remaining_scale": "sigma_absolute_value",
}

with open("s2t_v4_correlation_cell_free_energy_density_gate_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, indent=2))