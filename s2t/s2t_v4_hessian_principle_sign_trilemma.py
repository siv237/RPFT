import json

import sympy as sp


c = sp.symbols("c", real=True)
t = 1 - c
inverse_square_trace = sp.Rational(1, 45)
inverse_fourth_trace = sp.Rational(1, 4725)
incidence_norm_squared = 2 * t

gaussian_logdet_quadratic = sp.simplify(
    -sp.Rational(1, 2) * incidence_norm_squared * inverse_square_trace
)
gaussian_logdet_quartic = sp.simplify(
    -sp.Rational(1, 4) * incidence_norm_squared**2 * inverse_fourth_trace
)
gaussian_kl_quadratic = -gaussian_logdet_quadratic
static_susceptibility = -gaussian_logdet_quadratic
target = -(1 - c) / 45

result = {
    "gate": "version4_hessian_principle_sign_trilemma",
    "date": "2026-08-13",
    "target": str(target),
    "Gaussian_logdet": {
        "quadratic_coefficient": str(gaussian_logdet_quadratic),
        "target_sign_match": sp.simplify(gaussian_logdet_quadratic - target) == 0,
        "quartic_residual": str(gaussian_logdet_quartic),
        "exact_full_action_match": False,
    },
    "Gaussian_KL_Fisher": {
        "quadratic_coefficient": str(gaussian_kl_quadratic),
        "Wilson_domain": "c=cos(theta) in [-1,1]",
        "positive_on_Wilson_domain": True,
        "target_sign_match": sp.simplify(gaussian_kl_quadratic - target) == 0,
    },
    "trilemma": [
        "KL/Fisher geometry is canonical and quadratic but has the opposite positive sign",
        "Gaussian logdet has the required negative quadratic sign but its full action has nonzero higher powers",
        "declaring only the negative Hessian fundamental is an extra non-metric parent axiom",
    ],
    "literature_correction": {
        "free_energy_Hessian": str(gaussian_logdet_quadratic),
        "static_susceptibility_minus_free_energy_Hessian": str(static_susceptibility),
        "higher_terms_change_second_derivative_at_zero": False,
        "interpretation": (
            "the negative free-energy Hessian is a standard signed response; its "
            "negative is the positive susceptibility or information metric"
        ),
    },
    "verdict": "exact_two_point_response_pass_parent_action_identification_open",
    "reopening": (
        "derive an independently required signed susceptibility functional or an infinite "
        "graded cancellation that removes all higher powers without reversing the linear sign"
    ),
}

assert gaussian_logdet_quadratic == target
assert gaussian_kl_quadratic == -target
assert sp.simplify(gaussian_logdet_quartic + (1 - c) ** 2 / 4725) == 0
assert gaussian_kl_quadratic == (1 - c) / 45
assert static_susceptibility == (1 - c) / 45
assert not result["Gaussian_KL_Fisher"]["target_sign_match"]

with open(
    "s2t_v4_hessian_principle_sign_trilemma_results.json",
    "w",
    encoding="utf-8",
) as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, ensure_ascii=False, indent=2))