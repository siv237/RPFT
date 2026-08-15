import json
import math


def mode_ratio(rho):
    return 2.0 * math.log(1.0 / math.tanh(math.pi * rho))


def relative_action_and_derivative(chi_r3, radius_ratio=1.0, cutoff=80):
    action_sum = 0.0
    derivative_sum = 0.0
    for shell in range(cutoff + 1):
        eigenvalue = shell + 1.5
        multiplicity = (shell + 1) * (shell + 2)
        norm = math.sqrt(eigenvalue**2 + chi_r3**2)
        rho = radius_ratio * norm
        action_sum += multiplicity * mode_ratio(rho)
        if chi_r3 > 0:
            derivative_sum += (
                multiplicity
                * radius_ratio
                * chi_r3
                / norm
                / math.sinh(2.0 * math.pi * rho)
            )

    action = -2.0 * action_sum
    derivative = 8.0 * math.pi * derivative_sum
    return action, derivative


mass_grid = [0.0, 0.1, 0.5, 1.0, 2.0, 4.0, 8.0]
mass_sweep = []
for mass in mass_grid:
    action, derivative = relative_action_and_derivative(mass)
    mass_sweep.append(
        {
            "chi_R3": mass,
            "Delta_Gamma_AP_minus_P": action,
            "derivative_wrt_chi_R3": derivative,
        }
    )

convergence = []
for cutoff in [5, 10, 20, 40, 80]:
    action, derivative = relative_action_and_derivative(1.0, cutoff=cutoff)
    convergence.append(
        {
            "cutoff": cutoff,
            "action_at_chi_R3_1": action,
            "derivative_at_chi_R3_1": derivative,
        }
    )

result = {
    "date": "2026-08-11",
    "version": "S2T-IV",
    "status": "spin_branch_ratio_has_no_nonzero_mass_stationary_point",
    "gauge_mass_objection": {
        "physical_quotient_scalars": 3,
        "goldstone_is_counted_among_physical_scalars": False,
        "goldstone_location": "separate gauge-orbit direction in the R_xi BV complex",
        "vector_mass_origin": "trace kinetic term of charged x,z vacuum with m_A^2/chi^2=8g^2=3",
        "stueckelberg_input_required": False,
        "objection_valid": False,
    },
    "relative_determinant": {
        "variables": "x=chi R3, r=R1/R3",
        "action": "Delta Gamma_AP-P=-2 sum_k d_k I(r sqrt((k+3/2)^2+x^2))",
        "mode_function": "I(rho)=2 log coth(pi rho)>0",
        "analytic_derivative": "d_x Delta Gamma=8 pi r x sum_k d_k/[sqrt((k+3/2)^2+x^2) sinh(2 pi r sqrt((k+3/2)^2+x^2))]",
        "derivative_sign_for_x_positive": "strictly positive",
        "only_stationary_point_on_nonnegative_domain": "x=0 boundary",
        "limit_x_to_infinity": 0,
    },
    "mass_sweep_unit_radius_ratio": mass_sweep,
    "convergence_at_chi_R3_1": convergence,
    "checks": {
        "all_positive_mass_derivatives_positive": all(
            row["derivative_wrt_chi_R3"] > 0
            for row in mass_sweep
            if row["chi_R3"] > 0
        ),
        "action_monotone_increasing": all(
            mass_sweep[index]["Delta_Gamma_AP_minus_P"]
            < mass_sweep[index + 1]["Delta_Gamma_AP_minus_P"]
            for index in range(len(mass_sweep) - 1)
        ),
        "cutoff_40_to_80_action_error": abs(
            convergence[-1]["action_at_chi_R3_1"]
            - convergence[-2]["action_at_chi_R3_1"]
        ),
        "cutoff_40_to_80_derivative_error": abs(
            convergence[-1]["derivative_at_chi_R3_1"]
            - convergence[-2]["derivative_at_chi_R3_1"]
        ),
    },
    "verdict": {
        "local_counterterms_cancel_in_branch_difference": True,
        "nontrivial_chi_dependence": True,
        "nonzero_stationary_chi_exists": False,
        "scheme_independent_scale_ratio_fixed": False,
        "last_no_new_physics_route_closed": True,
        "minimal_fixed_K_parent_exhausted": True,
    },
}

assert result["checks"]["all_positive_mass_derivatives_positive"]
assert result["checks"]["action_monotone_increasing"]
assert result["checks"]["cutoff_40_to_80_action_error"] < 1e-14
assert result["checks"]["cutoff_40_to_80_derivative_error"] < 1e-14

with open(
    "s2t_v4_spin_branch_mass_stationarity_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps({"mass_sweep": mass_sweep, "verdict": result["verdict"]}, indent=2))