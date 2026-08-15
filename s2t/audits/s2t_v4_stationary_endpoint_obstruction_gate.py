import json


with open(
    "s2t_v4_radial_pfaffian_hessian_gate_results.json",
    encoding="utf-8",
) as handle:
    radial_results = json.load(handle)

bare_quartic_normalization = 1.0
critical_lambda = radial_results["critical_lambda"]
unit_curvature = radial_results["unit_lambda_angular_curvature"]

output = {
    "gate": "version4_stationary_endpoint_obstruction",
    "cross_tome_input": {
        "bare_quartic_over_kinetic_ratio": bare_quartic_normalization,
        "source": "version3_compact_a2_a4_moment_gate",
        "normalization_dictionary_derived": False,
    },
    "critical_lambda": critical_lambda,
    "quartic_to_critical_ratio": {
        branch: bare_quartic_normalization / threshold
        for branch, threshold in critical_lambda.items()
    },
    "unit_lambda_angular_curvature": unit_curvature,
    "identity_dictionary_stationary_cp_odd_branch_exists": False,
    "absolute_stationary_obstruction_proved": False,
    "minimal_missing_structure": (
        "an independently derived CP-odd radial-orientation invariant or a "
        "cross-tome mechanism changing the normalized quartic coefficient"
    ),
    "verdict": (
        "the identity normalization dictionary gives a large stationary "
        "obstruction, but the physical cross-tome comparison is conditional "
        "until the heat-kernel to spectral-trace coefficient is derived"
    ),
}

with open(
    "s2t_v4_stationary_endpoint_obstruction_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))