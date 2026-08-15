import json

import sympy as sp


sigma, theta = sp.symbols("sigma theta", real=True)
radius = sp.exp(sigma)

determinant = (
    sp.Rational(1, 2)
    * radius**2
    * (2 * radius + sp.exp(sp.I * theta))
    * sp.exp(-3 * sp.I * theta)
)
log_determinant = (
    2 * sigma
    + sp.log(2 * radius + sp.exp(sp.I * theta))
    - 3 * sp.I * theta
    - sp.log(2)
)


def imaginary_derivative(expression, *variables):
    derivative = sp.diff(expression, *variables).subs({sigma: 0, theta: 0})
    return sp.simplify(sp.im(sp.expand_complex(derivative)))


reduced_phase_gradient = {
    "sigma": str(imaginary_derivative(log_determinant, sigma)),
    "theta": str(imaginary_derivative(log_determinant, theta)),
}
reduced_phase_mixed_hessian = imaginary_derivative(
    log_determinant, sigma, theta
)

imaginary_determinant = sp.simplify(sp.im(sp.expand_complex(determinant)))
imaginary_determinant_mixed_hessian = sp.simplify(
    sp.diff(imaginary_determinant, sigma, theta).subs(
        {sigma: 0, theta: 0}
    )
)

output = {
    "gate": "version4_cp_odd_mixed_invariant",
    "reduced_chiral_determinant": str(determinant),
    "polynomial_trace_classification": {
        "odd_traces": "zero by bipartite chirality",
        "graded_even_traces": (
            "zero because MM^dagger and M^dagger M are isospectral"
        ),
        "ungraded_even_traces": (
            "real and CP even under theta -> -theta"
        ),
        "mixed_radial_orientation_hessian": 0,
    },
    "reduced_pfaffian_phase": {
        "local_log_section": str(log_determinant),
        "gradient_at_unit_vacuum": reduced_phase_gradient,
        "mixed_hessian_sigma_theta": str(reduced_phase_mixed_hessian),
        "nonzero_mixed_hessian": bool(reduced_phase_mixed_hessian != 0),
        "basis_independent": False,
        "globally_single_valued": False,
    },
    "imaginary_determinant_candidate": {
        "expression": str(imaginary_determinant),
        "mixed_hessian_sigma_theta": str(
            imaginary_determinant_mixed_hessian
        ),
        "basis_independent": False,
    },
    "full_ko6_measure": {
        "pfaffian": "|Pf_red|^2",
        "phase": 0,
        "mixed_hessian_sigma_theta": 0,
        "reality_pairing_cancels_candidate": True,
    },
    "order_one_status": (
        "the reduced phase uses an allowed Dirac block, but promoting it to "
        "an action term requires an oriented determinant line not supplied "
        "by the current real spectral triple"
    ),
    "unique_local_candidate": "Im log Pf_red",
    "candidate_survives_current_axioms": False,
    "minimal_extension": (
        "a chiral bulk/boundary determinant-line orientation or another "
        "independently derived pseudoscalar coefficient"
    ),
    "verdict": (
        "all polynomial spectral invariants have zero mixed Hessian; the "
        "only local nonzero candidate is the reduced Pfaffian phase with "
        "mixed Hessian -2/9, but J pairing cancels it and the determinant "
        "line is trivial in the current vectorlike model"
    ),
}

with open(
    "s2t_v4_cp_odd_mixed_invariant_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))