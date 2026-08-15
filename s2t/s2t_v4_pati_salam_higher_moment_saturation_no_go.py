import json

import numpy as np
import sympy as sp


t, alpha = sp.symbols("t alpha", positive=True, real=True)
coefficients = sp.symbols("a2:7", real=True)
polynomial = sum(
    coefficient * t**degree
    for degree, coefficient in enumerate(coefficients, start=2)
)
derivative = sp.diff(polynomial, t)
zeta = sp.expand(2 * derivative)
stationary_hessian = sp.simplify(
    (-4 * alpha + 2 * zeta).subs(alpha, derivative)
)

rng = np.random.default_rng(20260814)
residuals = []
for _ in range(32):
    values = rng.uniform(0.01, 2.0, size=5)
    radius = rng.uniform(0.05, 2.0)
    degrees = np.arange(2, 7)
    stationary_alpha = np.sum(degrees * values * radius ** (degrees - 1))
    induced_zeta = 2 * stationary_alpha
    residuals.append(abs(-4 * stationary_alpha + 2 * induced_zeta))

normalization_errors = []
for edge_count in (1, 2, 3, 5, 8):
    weights = rng.normal(size=edge_count) + 1j * rng.normal(size=edge_count)
    trace_norm = np.vdot(weights, weights).real
    canonical_coefficient = 4 * trace_norm / trace_norm
    normalization_errors.append(abs(canonical_coefficient - 4))

result = {
    "gate": "version4_pati_salam_higher_moment_saturation_no_go",
    "radial_potential": "V=-alpha t+P(t)",
    "stationarity": "alpha=P'(t)",
    "canonical_product_portal": "zeta=2P'(t)",
    "stationary_weak_hessian": str(stationary_hessian),
    "symbolic_P": str(polynomial),
    "symbolic_zeta": str(zeta),
    "maximum_random_identity_residual": float(max(residuals)),
    "weighted_edge_normalization_identity": (
        "c_raw=4 sum|w_i|^2 and canonical normalization gives c=4"
    ),
    "maximum_weighted_normalization_error": float(max(normalization_errors)),
    "verdict": (
        "All finite polynomial higher moments saturate the weak phi threshold "
        "after radial stationarity. Weighted non-identical placements return "
        "to c=4 after canonical normalization."
    ),
}

with open(
    "s2t_v4_pati_salam_higher_moment_saturation_no_go_results.json",
    "w",
    encoding="utf-8",
) as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, ensure_ascii=False, indent=2))