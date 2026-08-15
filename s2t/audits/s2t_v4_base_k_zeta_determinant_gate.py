import json
import math


scalar_modes = 3
scalar_mass_squared_ratio = 4
dirac_pairs = 2
dirac_weight_per_pair = -4
fermion_mass_squared_ratio = 1
vector_polarizations = 3
vector_mass_squared_ratio = 3

scalar_numerator = scalar_modes * scalar_mass_squared_ratio**2
fermion_numerator = (
    dirac_pairs * dirac_weight_per_pair * fermion_mass_squared_ratio**2
)
vector_numerator = vector_polarizations * vector_mass_squared_ratio**2
total_numerator = scalar_numerator + fermion_numerator + vector_numerator
coleman_weinberg_coefficient = total_numerator / (64 * math.pi**2)

betti_numbers_k = [1, 1, 0, 1, 1]
harmonic_gauge_mismatch = betti_numbers_k[1] - betti_numbers_k[0]

result = {
    "date": "2026-08-11",
    "version": "S2T-IV",
    "status": "base_K_operator_determinant_assembled_vacuum_not_parameter_free",
    "background": {
        "K": "RP3_R x S1_R",
        "dimension": 4,
        "scalar_curvature": "6/R^2",
        "betti_numbers": betti_numbers_k,
    },
    "field_ledger": {
        "real_scalars": {
            "multiplicity": scalar_modes,
            "operator": "Delta_0 + 4 chi^2",
            "flat_supertrace_numerator": scalar_numerator,
        },
        "relative_U1_BV_block": {
            "operator_combination": "1/2 logdet(Delta_1+3 chi^2) - 1/2 logdet(Delta_0+3 chi^2)",
            "physical_polarizations": vector_polarizations,
            "flat_supertrace_numerator": vector_numerator,
        },
        "dirac_pairs": {
            "multiplicity": dirac_pairs,
            "squared_operator": "D_K^2 + chi^2",
            "flat_supertrace_numerator": fermion_numerator,
        },
    },
    "gauge_topology": {
        "b0": betti_numbers_k[0],
        "b1": betti_numbers_k[1],
        "b1_minus_b0": harmonic_gauge_mismatch,
        "massive_harmonic_factor": "(b1-b0) log(3 chi^2)",
        "harmonic_factor_cancels": harmonic_gauge_mismatch == 0,
        "reduced_gauge_determinant": "1/2 logdet on non-harmonic coexact one-forms of Delta_1+3 chi^2",
    },
    "flat_limit_control": {
        "scalar_numerator": scalar_numerator,
        "fermion_numerator": fermion_numerator,
        "vector_numerator": vector_numerator,
        "total_numerator": total_numerator,
        "B0": coleman_weinberg_coefficient,
        "expected_total_numerator": 67,
        "passes": total_numerator == 67,
    },
    "zeta_definition": {
        "logdet_mu": "-zeta_P_prime(0)-zeta_P(0) log(mu^2)",
        "scale_derivative": "d logdet_mu / d log(mu) = -2 zeta_P(0)",
        "four_dimensional_local_terms": [
            "R_K^2",
            "R_K chi^2",
            "chi^4",
        ],
    },
    "renormalization_test": {
        "allowed_finite_counterterms": "lambda_0 R_K^2 + lambda_2 R_K chi^2 + lambda_4 chi^4",
        "arbitrary_stationary_point_formula": "lambda_2=-(F'(chi_*)+4 lambda_4 chi_*^3)/(2 R_K chi_*)",
        "scale_shift": "mu -> exp(t) mu is compensated in the flat quartic part by lambda_4 -> lambda_4 + 2 B0 t",
        "parameter_free_vacuum": False,
    },
    "verdict": {
        "operator_complex_closed": True,
        "gauge_zero_mode_bookkeeping_closed": True,
        "full_nonlocal_determinant_defined_after_discrete_spin_flat_choice": True,
        "finite_local_parts_fixed_by_spectrum": False,
        "absolute_vacuum_predicted": False,
        "next_allowed_step": "declare renormalization conditions before numerical zeta evaluation, then test only scheme-independent or blind dimensionless outputs",
    },
}

with open("s2t_v4_base_k_zeta_determinant_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result["flat_limit_control"], ensure_ascii=False, indent=2))