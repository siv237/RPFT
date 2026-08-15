import json
import math


S4_RADIUS_OVER_SIGMA = 1.3513921956865422
S4_LOG_PARTITION = 0.482205579996784
RP3_RADIUS_OVER_SIGMA = 1.9976083272693532
RP3_DENSITY = -0.010439954564981247
RP3_HESSIAN = 0.018660172218233947

rp3_volume_over_sigma_cubed = math.pi**2 * RP3_RADIUS_OVER_SIGMA**3
rp3_systole_over_sigma = math.pi * RP3_RADIUS_OVER_SIGMA

joint_samples = []
volume_s4_unit = 8.0 * math.pi**2 / 3.0
volume_rp3_unit = math.pi**2
rp3_log_partitions = {
    2.0: 0.8243015696244396,
    1.0: 0.0030146160703438457,
    0.5: 1.1397748994184095e-13,
    0.25: 2.3149884353781623e-55,
    0.1: 0.0,
}
for radius, log_partition in rp3_log_partitions.items():
    density = -(S4_LOG_PARTITION + log_partition) / (
        volume_s4_unit
        * volume_rp3_unit
        * S4_RADIUS_OVER_SIGMA**4
        * radius**3
    )
    joint_samples.append({"rp3_radius_over_sigma": radius, "joint_density": density})

result = {
    "gate": "version4_s4_rp3_hybrid_experiment",
    "date": "2026-08-11",
    "separate_rp3_scalar_density": {
        "radius_over_sigma": RP3_RADIUS_OVER_SIGMA,
        "density": RP3_DENSITY,
        "hessian": RP3_HESSIAN,
        "volume_over_sigma_cubed": rp3_volume_over_sigma_cubed,
        "systole_over_sigma": rp3_systole_over_sigma,
        "relative_radius_error_from_2": RP3_RADIUS_OVER_SIGMA / 2.0 - 1.0,
        "relative_volume_error_from_8pi2": rp3_volume_over_sigma_cubed / (8.0 * math.pi**2) - 1.0,
    },
    "kk_thresholds_over_correlation_cutoff": {
        "trivial_scalar_first_nonzero": math.sqrt(8.0) / RP3_RADIUS_OVER_SIGMA,
        "twisted_scalar_first_nonzero": math.sqrt(3.0) / RP3_RADIUS_OVER_SIGMA,
    },
    "joint_product_density": {
        "formula": "-(log Z_S4+log Z_RP3)/(v4 v3 r^4 s^3)",
        "samples": joint_samples,
        "limit_s_to_zero": "minus_infinity",
        "bounded_below": False,
    },
    "discrete_branch_sum": {
        "radius_over_sigma": 1.34900141462449,
        "density": -0.026153398325769996,
        "interpretation": "requires_a_spin_or_flat_character_sum_measure",
    },
    "verdict": "full_metric_K_baggage_cannot_be_inherited_without_product_instability_or_KK_content",
    "surviving_topological_core": ["pi1_RP3_equals_Z2", "torsion_holonomy", "linking_form"],
    "reopened_relative_measure_audit": {
        "connected_minimum": {
            "radius_base_over_sigma": 1.2258613343809333,
            "radius_circle_over_sigma": 1.1066331548520218,
            "hessian_eigenvalues": [0.0121002994, 0.0313148605],
        },
        "mutual_information_minimum": {
            "radius_base_over_sigma": 1.0324676288709487,
            "radius_circle_over_sigma": 0.9771570860359303,
            "hessian_eigenvalues": [0.0199410474, 0.0800801892],
        },
        "gibbs_parent_sign": "F_BC=F_B+F_C+T*I",
        "bundle_free_energy_minus_product_at_information_minimum": 0.36892276634420196,
        "verdict": "relative_minima_exist_but_additive_Gibbs_parent_has_wrong_sign",
    },
}

with open("s2t_v4_s4_rp3_hybrid_experiment_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, indent=2))