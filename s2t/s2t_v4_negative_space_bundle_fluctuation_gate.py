import json
import math

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import logsumexp


PI = math.pi
VOLUME_COEFFICIENT = 2.0 * PI**3


def log_sector_sums(radius_base, radius_circle):
    ell_cutoff = max(100, math.ceil(radius_base * math.sqrt(100.0)))
    mode_cutoff = max(100, math.ceil(radius_circle * math.sqrt(100.0)))

    ell = np.arange(ell_cutoff + 1, dtype=int)
    mode = np.arange(-mode_cutoff, mode_cutoff + 1, dtype=int)
    log_degeneracy = 2.0 * np.log(ell + 1.0)
    base_energy = ell * (ell + 2.0) / radius_base**2
    circle_energy = mode**2 / radius_circle**2

    log_even_base = float(logsumexp(log_degeneracy[ell % 2 == 0] - base_energy[ell % 2 == 0]))
    log_odd_base = float(logsumexp(log_degeneracy[ell % 2 == 1] - base_energy[ell % 2 == 1]))
    log_all_circle = float(logsumexp(-circle_energy))
    log_even_circle = float(logsumexp(-circle_energy[mode % 2 == 0]))
    log_odd_circle = float(logsumexp(-circle_energy[mode % 2 != 0]))

    log_trivial_product = log_even_base + log_all_circle
    log_nontrivial_bundle = float(
        logsumexp(
            [
                log_even_base + log_even_circle,
                log_odd_base + log_odd_circle,
            ]
        )
    )
    return log_trivial_product, log_nontrivial_bundle


def density(radius_base, radius_circle, branch):
    log_partition = log_sector_sums(radius_base, radius_circle)[branch]
    return -log_partition / (
        VOLUME_COEFFICIENT * radius_base**3 * radius_circle
    )


def equal_scale_minimum(branch):
    result = minimize_scalar(
        lambda log_radius: density(math.exp(log_radius), math.exp(log_radius), branch),
        bounds=(math.log(0.1), math.log(5.0)),
        method="bounded",
        options={"xatol": 1.0e-14},
    )
    radius = math.exp(result.x)
    return {"radius_over_sigma": radius, "density": result.fun}


boundary_samples = []
for radius_base in [0.5, 0.25, 0.1, 0.05]:
    boundary_samples.append(
        {
            "base_radius_over_sigma": radius_base,
            "circle_radius_over_sigma_trivial": 1.53362628,
            "trivial_density": density(radius_base, 1.53362628, 0),
            "circle_radius_over_sigma_nontrivial": 3.06725256,
            "nontrivial_density": density(radius_base, 3.06725256, 1),
        }
    )


result = {
    "gate": "version4_negative_space_bundle_fluctuation",
    "date": "2026-08-11",
    "forgotten_bundle": {
        "base": "RP3",
        "classification": "H2(RP3;Z)=Z2",
        "total_space_model": "(S3 x S1)/[(x,theta)~(-x,theta+pi)]",
        "scalar_selection_rule": "ell_plus_m_even",
        "volume": "2*pi^3*R3^3*R1",
        "trivial_product_rule": "ell_even_with_all_m",
        "equal_scale_minima": {
            "trivial_product": equal_scale_minimum(0),
            "nontrivial_bundle": equal_scale_minimum(1),
        },
        "boundary_samples": boundary_samples,
        "analytic_boundary": {
            "limit": "R3_to_zero_at_fixed_R1",
            "trivial_log_partition": "log(sum_m exp(-m^2/R1^2)) > 0",
            "nontrivial_log_partition": "log(sum_n exp(-(2n)^2/R1^2)) > 0",
            "density_limit": "minus_infinity",
        },
        "verdict": "nontrivial_bundle_couples_parity_and_momentum_but_does_not_stabilize_the_scalar_correlation_density",
    },
    "negative_space_map": {
        "fixed_product_no_go": "does_not_cover_nonproduct_bundles_or_warped_metrics",
        "bundle_test_here": "closes_the_homogeneous_flat_connection_scalar_density_branch",
        "warped_metrics": "still_underdetermined_without_a_parent_cross_term",
        "scalar_carrier_tests": "do_not_cover_the_full_standard_model_fluctuation_action",
        "general_single_vertex_no_go": "explicitly_unproved_in_existing_audit",
    },
    "highest_value_omission": {
        "name": "full_field_carrier_fluctuation_determinant",
        "required_ledger": [
            "three_physical_scalar_operators",
            "massive_vector_plus_gauge_ghost_complex",
            "two_Dirac_pair_operators",
            "zero_modes_and_curvature_endomorphisms",
            "one_common_counterterm_and_measure_scheme",
        ],
        "warning": "a_signed_supertrace_is_not_a_positive_density_state_and_cannot_be_inserted_into_the_scalar_entropy_gate",
        "next_exact_test": "compare_renormalized_Gamma_fluc_on_S4_and_S2xS2_at_fixed_volume_then_compute_the_joint_geometry_Hessian",
    },
}

with open("s2t_v4_negative_space_bundle_fluctuation_gate_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps({
    "equal_scale_minima": result["forgotten_bundle"]["equal_scale_minima"],
    "last_boundary_sample": boundary_samples[-1],
    "highest_value_omission": result["highest_value_omission"]["name"],
}, ensure_ascii=False, indent=2))