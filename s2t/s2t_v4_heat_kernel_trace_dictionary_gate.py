import json

import sympy as sp


pi = sp.pi
f0, gauge_squared, radius = sp.symbols(
    "f0 gauge_squared radius", positive=True
)

heat_kernel_prefactor = 1 / (4 * pi) ** 2
scalar_wavefunction = sp.simplify(2 * f0 * heat_kernel_prefactor)
raw_gauge_coefficient = sp.simplify(
    heat_kernel_prefactor * f0 * sp.Rational(4, 3)
)
f0_from_gauge_matching = sp.solve(
    sp.Eq(raw_gauge_coefficient, 1 / (4 * gauge_squared)),
    f0,
)[0]
canonical_quartic = sp.simplify(1 / scalar_wavefunction)
canonical_quartic_from_gauge = sp.simplify(
    canonical_quartic.subs(f0, f0_from_gauge_matching)
)

compact_volume = 2 * pi**3 * radius**4
dimensionless_zero_mode_quartic = sp.simplify(
    compact_volume * canonical_quartic_from_gauge / radius**4
)
matching_gauge_squared = sp.Rational(3, 8)

output = {
    "gate": "version4_heat_kernel_trace_dictionary",
    "heat_kernel_prefactor": str(heat_kernel_prefactor),
    "scalar_wavefunction_coefficient": str(scalar_wavefunction),
    "raw_gauge_coefficient": str(raw_gauge_coefficient),
    "f0_from_gauge_matching": str(f0_from_gauge_matching),
    "canonical_quartic": str(canonical_quartic),
    "canonical_quartic_from_gauge": str(
        canonical_quartic_from_gauge
    ),
    "matching_value": {
        "gauge_squared": str(matching_gauge_squared),
        "f0": str(
            sp.simplify(
                f0_from_gauge_matching.subs(
                    gauge_squared, matching_gauge_squared
                )
            )
        ),
        "canonical_4d_quartic": str(
            sp.simplify(
                canonical_quartic_from_gauge.subs(
                    gauge_squared, matching_gauge_squared
                )
            )
        ),
    },
    "compact_base_volume": str(compact_volume),
    "dimensionless_zero_mode_quartic": str(
        dimensionless_zero_mode_quartic
    ),
    "dimensionless_zero_mode_matching_value": str(
        sp.simplify(
            dimensionless_zero_mode_quartic.subs(
                gauge_squared, matching_gauge_squared
            )
        )
    ),
    "curvature_changes_quartic_dictionary": False,
    "curvature_changes_quadratic_term": True,
    "local_4d_dictionary": (
        "after canonical scalar normalization lambda_4D=(8/3)g^2=1"
    ),
    "integrated_base_k_dictionary": (
        "for phi_hat=R phi, lambda_0D=2*pi^3 at g^2=3/8"
    ),
    "radial_pfaffian_gate_uses_same_architecture": False,
    "architecture_gap": (
        "the radial gate adds a unit finite Pfaffian to a unit-normalized "
        "bosonic trace; neither the local 4D determinant density nor the "
        "integrated base-K zero-mode coefficient is retained"
    ),
    "physical_cross_tome_threshold_available": False,
    "verdict": (
        "the quartic convention dictionary is derivable, but it exposes an "
        "architecture mismatch rather than a free numerical factor: the "
        "radial-Pfaffian critical lambda is a normalized toy-action "
        "threshold and cannot be compared directly with the 4D heat-kernel "
        "coefficient"
    ),
}

with open(
    "s2t_v4_heat_kernel_trace_dictionary_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))