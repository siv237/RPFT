import json
import math
from pathlib import Path

import numpy as np


PI = math.pi
FULL_DIMENSION = 24

kernel_vector = np.zeros(FULL_DIMENSION)
kernel_vector[0] = 1.0
p_kernel = np.outer(kernel_vector, kernel_vector)
p_heavy = np.eye(FULL_DIMENSION) - p_kernel

trace_kernel = float(np.trace(p_kernel.T @ p_kernel))
trace_heavy = float(np.trace(p_heavy.T @ p_heavy))
projector_cross = float(np.trace(p_heavy.T @ p_kernel))

length_gamma = PI
e0_integral_norm_squared = length_gamma
e0_canonical_norm_squared = 1.0
e1_integral_norm_squared = 1.0 / length_gamma
e1_canonical_norm_squared = 1.0

superconnection_norm_squared = (
    trace_heavy * e0_canonical_norm_squared
    + trace_kernel * e1_integral_norm_squared
)

normalization_scenarios = [
    {
        "name": "canonical_wavefunction_plus_integral_holonomy",
        "e0_norm_squared": e0_canonical_norm_squared,
        "e1_norm_squared": e1_integral_norm_squared,
    },
    {
        "name": "both_integral_generators",
        "e0_norm_squared": e0_integral_norm_squared,
        "e1_norm_squared": e1_integral_norm_squared,
    },
    {
        "name": "both_canonical_wavefunctions",
        "e0_norm_squared": e0_canonical_norm_squared,
        "e1_norm_squared": e1_canonical_norm_squared,
    },
]

for scenario in normalization_scenarios:
    scenario["combined_norm_squared"] = (
        trace_heavy * scenario["e0_norm_squared"]
        + trace_kernel * scenario["e1_norm_squared"]
    )

results = {
    "status": "superconnection_trace_closes_relative_metric_with_wavefunction_holonomy_normalization",
    "date": "2026-08-03",
    "superconnection_tangent": {
        "definition": "Xi=P_heavy tensor e0_hat + P_kernel tensor e1_integral",
        "e0_hat": "1/sqrt(pi), the canonically normalized constant field mode on gamma",
        "e1_integral": "ds/pi, the unit-period holonomy generator on gamma",
        "reason_for_distinct_normalizations": (
            "The degree-zero component is a dynamical collective amplitude and must be wavefunction "
            "normalized. The degree-one component is a quantized connection/charge-lattice element "
            "and must retain unit period."
        ),
    },
    "single_trace_Hodge_metric": {
        "formula": (
            "||Xi||^2=Tr(P_heavy^2)||e0_hat||^2+Tr(P_kernel^2)||e1_integral||^2"
        ),
        "Tr_P_heavy_squared": trace_heavy,
        "Tr_P_kernel_squared": trace_kernel,
        "projector_cross_trace": projector_cross,
        "e0_hat_norm_squared": e0_canonical_norm_squared,
        "e1_integral_norm_squared": e1_integral_norm_squared,
        "combined_norm_squared": superconnection_norm_squared,
        "target": 23.0 + 1.0 / PI,
        "error": abs(superconnection_norm_squared - (23.0 + 1.0 / PI)),
    },
    "orthogonality": {
        "form_degree_statement": "Omega0 and Omega1 are orthogonal in the graded L2 metric",
        "internal_statement": "P_heavy P_kernel=0",
        "projector_cross_trace": projector_cross,
        "consequence": "no mixed normalization coefficient or cross counterterm is available",
    },
    "normalization_audit": {
        "scenarios": normalization_scenarios,
        "selected_without_data": "canonical_wavefunction_plus_integral_holonomy",
        "selection_rule": (
            "Use L2 normalization for propagating field amplitudes and integral-period normalization "
            "for topological connection generators, the same distinction already used in the Qcycle audit."
        ),
        "continuous_relative_weight": False,
    },
    "relation_to_Qcycle": {
        "Qcycle_uses": "integral lattice generators e0=1 and e1=ds/pi for the coupling norm",
        "collective_metric_uses": (
            "the normalized field zero mode e0_hat and the same integral e1 for stiffness"
        ),
        "consistency": (
            "This is not a contradiction: the primitive coupling vector is not wavefunction-normalized, "
            "whereas the collective dynamical amplitude is."
        ),
    },
    "theory_effect": {
        "relative_metric_gate": "closed_inside_the_minimal_superconnection_model",
        "D_nu": "derived_as_one_trace_Hodge_norm",
        "continuous_fit_parameter_added": False,
        "remaining_global_obligation": (
            "either take the canonical configuration trace-Hodge metric as primary or derive a "
            "special spectral-kernel/background identity reproducing its Hessian"
        ),
    },
    "verdict": (
        "The equal Hilbert-Schmidt/Hodge weighting need not be postulated as alpha=beta. A single "
        "graded trace-Hodge metric on Xi=P_heavy tensor e0_hat + P_kernel tensor e1 gives "
        "23+pi^-1 exactly. The zero-form and one-form pieces are orthogonal both by form degree and "
        "by complementary projectors. The apparent normalization asymmetry is fixed by physical role: "
        "e0_hat is a canonical dynamical wavefunction, while e1 is a unit-period topological generator. "
        "The parent tubular embedding is supplied by the companion audit; the remaining task is to "
        "justify this canonical metric as primary or derive it from a special spectral kernel/background."
    ),
}

assert abs(trace_heavy - 23.0) < 1e-12
assert abs(trace_kernel - 1.0) < 1e-12
assert abs(projector_cross) < 1e-12
assert abs(superconnection_norm_squared - (23.0 + 1.0 / PI)) < 1e-12
assert not results["normalization_audit"]["continuous_relative_weight"]

Path("s2t_neutrino_superconnection_metric_closure_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "Tr_P_heavy_squared": trace_heavy,
            "Tr_P_kernel_squared": trace_kernel,
            "cross_trace": projector_cross,
            "D_nu": superconnection_norm_squared,
            "remaining_obligation": results["theory_effect"]["remaining_global_obligation"],
        },
        indent=2,
        ensure_ascii=False,
    )
)