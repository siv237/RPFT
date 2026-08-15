import json
import math

import numpy as np
from scipy.special import logsumexp


TAU = 1.0


def spectral_data(radius, tail=60.0):
    cutoff = max(80, math.ceil(radius * math.sqrt(tail / TAU)))
    ell = np.arange(cutoff + 1, dtype=float)
    degeneracy = (ell + 1.0) * (ell + 2.0) * (2.0 * ell + 3.0) / 6.0
    mu = ell * (ell + 3.0)
    log_weight = np.log(degeneracy) - TAU * mu / radius**2
    log_partition = float(logsumexp(log_weight))
    probability = np.exp(log_weight - log_partition)
    mean_mu = float(np.sum(probability * mu))
    return log_partition, mean_mu


def row(radius):
    log_partition, mean_mu = spectral_data(radius)
    partition = math.exp(log_partition)
    gibbs_free_energy = -log_partition / TAU
    gibbs_derivative = -2.0 * mean_mu / radius**3
    heat_trace_derivative = partition * 2.0 * TAU * mean_mu / radius**3
    return {
        "radius": radius,
        "partition": partition,
        "gibbs_free_energy": gibbs_free_energy,
        "gibbs_derivative": gibbs_derivative,
        "positive_heat_spectral_action": partition,
        "spectral_action_derivative": heat_trace_derivative,
    }


radii = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0]
samples = [row(radius) for radius in radii]

result = {
    "gate": "version4_s4_radius_boundary_no_go",
    "date": "2026-08-11",
    "tau": TAU,
    "gibbs_identity": "dF_da=-2<mu>/a^3<0",
    "positive_cutoff_identity": "dS_f_da=sum d_l f'(y_l)(-2y_l/a)>=0 for f'<=0",
    "samples": samples,
    "gibbs_nonnegative_derivative_points": sum(sample["gibbs_derivative"] >= 0.0 for sample in samples),
    "spectral_nonpositive_derivative_points": sum(sample["spectral_action_derivative"] <= 0.0 for sample in samples),
    "verdict": "no_finite_radius_stationary_point_from_either_functional",
    "boundary_limits": {
        "gibbs_minimum": "a_to_infinity_decompactification",
        "positive_spectral_action_minimum": "a_to_zero_collapse",
    },
    "reopening_condition": "derived_constraint_or_relative_weight_not_fitted_to_observables",
}

with open("s2t_v4_s4_radius_boundary_no_go_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, indent=2))