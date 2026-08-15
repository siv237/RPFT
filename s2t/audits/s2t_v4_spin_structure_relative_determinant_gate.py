import json
import math


def mode_log_ratio(rho, beta):
    exponential = math.exp(-2.0 * math.pi * rho)
    numerator = (
        1.0
        - 2.0 * math.cos(2.0 * math.pi * beta) * exponential
        + exponential**2
    )
    denominator = (1.0 - exponential) ** 2
    return math.log(numerator / denominator)


def fermion_relative_action(beta, chi_r3=1.0, radius_ratio=1.0, cutoff=80):
    total = 0.0
    for shell in range(cutoff + 1):
        eigenvalue_r3 = shell + 1.5
        multiplicity = (shell + 1) * (shell + 2)
        rho = radius_ratio * math.sqrt(eigenvalue_r3**2 + chi_r3**2)
        total += multiplicity * mode_log_ratio(rho, beta)

    # The RP3 shell multiplicity is for a complex rank-two 3D spinor.
    # Product Clifford doubling and the two physical Dirac pairs give -2.
    return -2.0 * total


def derivative(beta, chi_r3=1.0, radius_ratio=1.0, step=1e-5):
    upper = fermion_relative_action(beta + step, chi_r3, radius_ratio)
    lower = fermion_relative_action(beta - step, chi_r3, radius_ratio)
    return (upper - lower) / (2.0 * step)


def curvature(beta, chi_r3=1.0, radius_ratio=1.0, step=1e-4):
    upper = fermion_relative_action(beta + step, chi_r3, radius_ratio)
    center = fermion_relative_action(beta, chi_r3, radius_ratio)
    lower = fermion_relative_action(beta - step, chi_r3, radius_ratio)
    return (upper - 2.0 * center + lower) / step**2


beta_grid = [0.0, 0.125, 0.25, 0.375, 0.5]
mass_grid = [0.0, 0.5, 1.0, 2.0, 4.0]
radius_grid = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]

beta_sweep = [
    {
        "beta": beta,
        "relative_action": fermion_relative_action(beta),
    }
    for beta in beta_grid
]

mass_sweep = [
    {
        "chi_R3": mass,
        "periodic_action": fermion_relative_action(0.0, mass),
        "antiperiodic_action": fermion_relative_action(0.5, mass),
    }
    for mass in mass_grid
]

radius_sweep = [
    {
        "R1_over_R3": ratio,
        "antiperiodic_action": fermion_relative_action(
            0.5, chi_r3=1.0, radius_ratio=ratio
        ),
    }
    for ratio in radius_grid
]

convergence = [
    {
        "cutoff": cutoff,
        "antiperiodic_action": fermion_relative_action(0.5, cutoff=cutoff),
    }
    for cutoff in [5, 10, 20, 40, 80]
]

stationary = [
    {
        "beta": beta,
        "first_derivative": derivative(beta),
        "second_derivative": curvature(beta),
    }
    for beta in [0.0, 0.5]
]

reflection_errors = []
periodicity_errors = []
for beta in [0.1, 0.2, 0.3, 0.4]:
    value = fermion_relative_action(beta)
    reflection_errors.append(
        abs(value - fermion_relative_action(1.0 - beta))
    )
    periodicity_errors.append(
        abs(value - fermion_relative_action(1.0 + beta))
    )

result = {
    "date": "2026-08-11",
    "version": "S2T-IV",
    "status": "scheme_independent_S1_spin_selection_conditional_on_spin_sum",
    "RP3_spin_gate": {
        "tau_plus_absolute_spectrum": "abs(lambda_k)=k+3/2, d_k=(k+1)(k+2)",
        "tau_minus_relation": "positive and negative signed branches exchanged",
        "squared_spectra_equal": True,
        "vectorlike_modulus_distinguishes_tau_plus_tau_minus": False,
        "eta_values": [-0.25, 0.25],
        "eta_phase_survives_two_Dirac_pairing": False,
    },
    "S1_relative_determinant": {
        "mode_formula": "I_rho(beta)=log[(cosh(2 pi rho)-cos(2 pi beta))/(cosh(2 pi rho)-1)]",
        "rho_k": "(R1/R3)*sqrt((k+3/2)^2+(chi R3)^2)",
        "shell_multiplicity": "(k+1)(k+2)",
        "two_Dirac_pair_action": "Delta Gamma_f=-2 sum_k d_k I_rho_k(beta)",
        "analytic_sign": "I_rho(beta)>=0; it is maximal at beta=1/2, so Delta Gamma_f is minimized at beta=1/2",
    },
    "unit_radius_unit_mass_beta_sweep": beta_sweep,
    "mass_sweep_R1_over_R3_1": mass_sweep,
    "radius_sweep_chi_R3_1": radius_sweep,
    "stationary_tests": stationary,
    "convergence": convergence,
    "checks": {
        "cutoff_40_to_80_error": abs(
            convergence[-1]["antiperiodic_action"]
            - convergence[-2]["antiperiodic_action"]
        ),
        "max_reflection_error": max(reflection_errors),
        "max_periodicity_error": max(periodicity_errors),
        "periodic_value_zero": abs(beta_sweep[0]["relative_action"]),
        "antiperiodic_lower_than_periodic_for_mass_sweep": all(
            row["antiperiodic_action"] < row["periodic_action"]
            for row in mass_sweep
        ),
        "beta_half_is_local_minimum": stationary[1]["second_derivative"] > 0,
        "beta_zero_is_local_maximum": stationary[0]["second_derivative"] < 0,
    },
    "interpretation": {
        "scheme_independence": "Local heat-kernel coefficients are beta-independent, so the branch difference cancels lambda_0, lambda_2, lambda_4 and mu.",
        "selection_scope": "If the functional integral sums the two S1 spin structures with equal prior weight, the antiperiodic branch has lower fermionic effective action for every finite chi and radius.",
        "superselection_warning": "If the spin structure is fixed as external background data, the determinant compares branches but does not dynamically change the chosen topology.",
        "remaining_degeneracy": "The two RP3 spin structures remain exactly degenerate in the vectorlike determinant modulus.",
    },
    "verdict": {
        "S1_antiperiodic_branch_selected_conditionally": True,
        "RP3_spin_branch_selected": False,
        "absolute_vacuum_scale_fixed": False,
        "new_continuous_parameter_used": False,
    },
}

assert result["checks"]["cutoff_40_to_80_error"] < 1e-14
assert result["checks"]["max_reflection_error"] < 1e-14
assert result["checks"]["max_periodicity_error"] < 1e-14
assert result["checks"]["periodic_value_zero"] < 1e-14
assert result["checks"]["antiperiodic_lower_than_periodic_for_mass_sweep"]
assert result["checks"]["beta_half_is_local_minimum"]
assert result["checks"]["beta_zero_is_local_maximum"]

with open(
    "s2t_v4_spin_structure_relative_determinant_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps({"beta_sweep": beta_sweep, "checks": result["checks"]}, indent=2))