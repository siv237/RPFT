import json
import math
from pathlib import Path

import sympy as sp


MAX_POLYNOMIAL_DEGREE = 8
BACKGROUND_POINTS = [0.25, 0.5, 1.0, 2.0, 4.0]
POSITIVE_HEAT_MIXTURES = [
    [(1.0, 1.0)],
    [(0.5, 0.5), (0.5, 2.0)],
    [(0.2, 0.25), (0.3, 1.0), (0.5, 4.0)],
]


def heat_mixture_mismatch(x_value, mixture):
    return sum(
        weight
        * rate
        * (
            1.0
            - math.exp(-rate * x_value)
            + 2.0 * rate * x_value * math.exp(-rate * x_value)
        )
        for weight, rate in mixture
    )


x = sp.symbols("x", positive=True)
coefficients = sp.symbols(f"a0:{MAX_POLYNOMIAL_DEGREE + 1}")
polynomial = sum(
    coefficients[index] * x**index for index in range(MAX_POLYNOMIAL_DEGREE + 1)
)
first_derivative = sp.diff(polynomial, x)
second_derivative = sp.diff(first_derivative, x)
equal_weight_identity = sp.expand(
    first_derivative.subs(x, 0) - first_derivative - 2 * x * second_derivative
)
identity_equations = sp.Poly(equal_weight_identity, x).all_coeffs()
identity_solution = sp.solve(identity_equations, coefficients[2:], dict=True)

y = sp.Function("y")
c = sp.symbols("c")
ode = sp.Eq(y(x) + 2 * x * sp.diff(y(x), x), c)
ode_solution = sp.dsolve(ode)

heat_rows = []
for mixture in POSITIVE_HEAT_MIXTURES:
    mismatches = [
        heat_mixture_mismatch(point, mixture) for point in BACKGROUND_POINTS
    ]
    heat_rows.append(
        {
            "mixture": [
                {"weight": weight, "rate": rate} for weight, rate in mixture
            ],
            "background_points": BACKGROUND_POINTS,
            "heavy_minus_kernel_half_weight": mismatches,
            "strictly_positive_for_tested_positive_backgrounds": all(
                mismatch > 0.0 for mismatch in mismatches
            ),
        }
    )

fixed_background_dimension = MAX_POLYNOMIAL_DEGREE
fixed_background_constraint_rank = 1
fixed_background_solution_dimension = (
    fixed_background_dimension - fixed_background_constraint_rank
)

results = {
    "status": "canonical_metric_is_unique_smooth_background_independent_hessian_positive_heat_kernels_fail",
    "date": "2026-08-04",
    "reduced_hessian": {
        "functional": "S_f(a)=Tr f((D0+a deltaA)^2)",
        "kernel_line_weight": "w0=2 f'(0)",
        "massive_heavy_weight": "wM=2 f'(M^2)+4 M^2 f''(M^2)",
        "equal_weight_condition": "f'(0)=f'(x)+2x f''(x), x=M^2",
    },
    "background_independent_identity": {
        "ode_for_y_equal_fprime": str(ode),
        "general_ode_solution": str(ode_solution),
        "smooth_at_zero_consequence": (
            "the x^(-1/2) branch is excluded, so f'(x) is constant"
        ),
        "unique_smooth_kernel_class": "f(x)=A+B x",
        "polynomial_degree_tested": MAX_POLYNOMIAL_DEGREE,
        "symbolic_identity_solution": [
            {str(key): str(value) for key, value in row.items()}
            for row in identity_solution
        ],
    },
    "positive_heat_kernel_gate": {
        "class": (
            "f(x)=integral exp(-t x) dmu(t), with nonzero positive measure on t>0"
        ),
        "mismatch_formula": (
            "wM-w0=2 integral t[1-exp(-tx)+2tx exp(-tx)] dmu(t)>0 for x>0"
        ),
        "tested_mixtures": heat_rows,
        "verdict": (
            "no nonconstant positive heat-kernel mixture gives equal weights at nonzero background"
        ),
    },
    "single_background_warning": {
        "statement": (
            "At one preselected M, equality is one scalar constraint and admits infinitely many "
            "non-affine kernels. Choosing one after seeing D_nu is not a derivation."
        ),
        "polynomial_coefficient_dimension_excluding_constant": fixed_background_dimension,
        "constraint_rank": fixed_background_constraint_rank,
        "remaining_solution_dimension": fixed_background_solution_dimension,
    },
    "theory_effect": {
        "generic_bosonic_spectral_action_route": (
            "closed_negatively_for_positive_heat_kernels"
        ),
        "background_independent_smooth_route": "forces_affine_kernel",
        "canonical_configuration_metric": (
            "may be adopted as a primary kinetic postulate, but is not derived from a generic cutoff kernel"
        ),
        "neutrino_denominator": (
            "theorem only inside the declared affine/canonical configuration-metric model; otherwise conditional"
        ),
    },
    "verdict": (
        "The equal heavy/kernel metric is not a generic spectral-action consequence. Requiring it "
        "smoothly for arbitrary nonzero heavy background uniquely selects an affine f, equivalent "
        "to the canonical quadratic configuration metric. Standard positive heat-kernel mixtures "
        "miss equality with a strict sign. A non-affine kernel can be tuned at one chosen mass, but "
        "that is a codimension-one choice and cannot count as a no-fit derivation."
    ),
}

assert identity_solution == [
    {coefficient: 0 for coefficient in coefficients[2:]}
]
assert all(
    row["strictly_positive_for_tested_positive_backgrounds"] for row in heat_rows
)

Path("s2t_neutrino_spectral_metric_uniqueness_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "unique_smooth_kernel_class": results["background_independent_identity"][
                "unique_smooth_kernel_class"
            ],
            "positive_heat_mixture_pass_count": sum(
                not row["strictly_positive_for_tested_positive_backgrounds"]
                for row in heat_rows
            ),
            "single_background_remaining_polynomial_dimension": (
                fixed_background_solution_dimension
            ),
        },
        indent=2,
        ensure_ascii=False,
    )
)