import json
import math


RADIUS_OVER_SIGMA = 1.3513921956865422
CURVATURE_TIMES_SIGMA_SQUARED = 6.570802791491215
GAUSSIAN_F2 = 1.0

sigma_over_planck_length = math.sqrt(GAUSSIAN_F2 / (12.0 * math.pi))
radius_over_planck_length = RADIUS_OVER_SIGMA * sigma_over_planck_length
curvature_times_planck_length_squared = (
    CURVATURE_TIMES_SIGMA_SQUARED / sigma_over_planck_length**2
)

validity_targets = {}
for target in [1.0, 0.1, 0.01]:
    cutoff_ratio = math.sqrt(CURVATURE_TIMES_SIGMA_SQUARED / target)
    validity_targets[str(target)] = {
        "required_Lambda_EFT_times_sigma": cutoff_ratio,
        "required_radius_times_Lambda_EFT": RADIUS_OVER_SIGMA * cutoff_ratio,
    }

result = {
    "gate": "version4_absolute_scale_eft_validity",
    "date": "2026-08-11",
    "gravitational_matching": "1/(8 pi G)=f2 Lambda^2/(96 pi^2)",
    "sigma_squared": "G f2/(12 pi)",
    "gaussian_profile": {"f2": GAUSSIAN_F2},
    "gaussian_absolute_ratios": {
        "sigma_over_planck_length": sigma_over_planck_length,
        "radius_over_planck_length": radius_over_planck_length,
        "curvature_times_planck_length_squared": curvature_times_planck_length_squared,
    },
    "same_scale_validity": {
        "radius_times_Lambda": RADIUS_OVER_SIGMA,
        "curvature_over_Lambda_squared": CURVATURE_TIMES_SIGMA_SQUARED,
        "sqrt_curvature_over_Lambda": math.sqrt(CURVATURE_TIMES_SIGMA_SQUARED),
        "valid": False,
    },
    "moment_independence": "R/Lambda^2=R sigma^2 is independent of f2 when Lambda=1/sigma",
    "diagnostic_separation_targets": validity_targets,
    "verdict": "absolute_matching_not_self_consistent_with_local_heat_kernel_expansion",
    "reopening_routes": [
        "derive_Lambda_EFT_over_Lambda_correlation_hierarchy",
        "use_exact_nonlocal_spectral_action_without_local_truncation",
    ],
}

with open("s2t_v4_absolute_scale_eft_validity_gate_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, indent=2))