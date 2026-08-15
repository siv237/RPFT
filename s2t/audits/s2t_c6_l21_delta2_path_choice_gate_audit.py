import json
from pathlib import Path

finite_spec = json.loads(Path("s2t_c6_l21_delta2_finite_block_spec_results.json").read_text())
gate = json.loads(Path("s2t_c6_l21_delta2_delta_gate_results.json").read_text())

allowed_paths = [
    {
        "path_id": "ambient_linear_embedding_strain",
        "definition": "Use the same ambient map x -> (I + eps A)x, followed by the already declared normalization/projection convention to L(2,1).",
        "status": "preferred_if_consistent_with_first_strain_audits",
        "risk": "Second metric derivative is induced by the normalization/projection step and must be written explicitly, not set to zero by fiat.",
    },
    {
        "path_id": "metric_geodesic_path",
        "definition": "Use a fixed Riemannian metric-space path g(eps) with g'(0)=h_A and a declared g''(0), for example an exponential/geodesic convention.",
        "status": "allowed_only_if_declared_before_C_delta2_values",
        "risk": "May differ from the ambient-strain path; any difference must be treated as scheme data, not as a fitted knob.",
    },
    {
        "path_id": "pure_conformal_test_path",
        "definition": "Use g(eps)=exp(2 eps q_A) g for the conformal slice when the audit is explicitly labelled as a slice test, not the full ambient theorem.",
        "status": "diagnostic_only_unless_slice_theorem_is_proven",
        "risk": "Cannot by itself prove the full P02/ambient C6 claim because traceless non-conformal pieces are omitted.",
    },
]

forbidden_moves = [
    "choosing g''(0) after seeing whether C_delta2 cancels trace 80",
    "setting delta2 Delta to zero while keeping nonlinear metric normalization effects elsewhere",
    "mixing the conformal test path for delta2 with the ambient path for trace-square without a bridge lemma",
    "using a finite local counterterm whose coefficient is selected after comparing with alpha",
]

results = {
    "status": "delta2_path_choice_gate_fixed_scheme_must_precede_matrix",
    "inputs": [
        "s2t_c6_l21_delta2_delta_gate_results.json",
        "s2t_c6_l21_delta2_finite_block_spec_results.json",
    ],
    "problem": {
        "why_path_matters": "delta^2 Delta depends on the second derivative of the operator along a chosen one-parameter metric/embedding path, not only on the tangent h_A.",
        "determinant_role": gate["determinant_identity"]["second_variation"],
        "finite_fallback_size": finite_spec["counts"],
    },
    "allowed_paths": allowed_paths,
    "required_before_computation": [
        "select exactly one path_id for the finite C_delta2 theorem route",
        "write g'(0), g''(0), delta Delta, and delta2 Delta in the same convention",
        "state whether the calculation is full ambient P02 or only conformal-slice diagnostic",
        "state the subtraction/local-counterterm convention before computing finite traces",
        "use the same quotient-normalized bases and Hilbert convention as the trace-square audits",
    ],
    "forbidden_moves": forbidden_moves,
    "current_status": {
        "path_choice_fixed": False,
        "C_delta2_matrix_evaluated": False,
        "locality_or_compensation_proven": False,
        "master_matrix_should_upgrade": False,
    },
    "pass_fail": [
        {
            "test": "path_declared_before_numbers",
            "status": "not_yet",
            "meaning": "No finite C_delta2 number should be interpreted until the path convention is fixed.",
        },
        {
            "test": "same_scheme_as_trace_square",
            "status": "not_yet",
            "meaning": "The delta2 block still needs a bridge to the first-strain trace-square scheme.",
        },
        {
            "test": "conformal_slice_labelled",
            "status": "required_if_used",
            "meaning": "A conformal calculation is allowed as a diagnostic, but cannot be sold as the full ambient theorem without a slice theorem.",
        },
    ],
    "plain_language": "Before measuring the fifth extinguisher, choose the track it rolls on. If we choose the track after seeing the fire, it is a hidden fit.",
    "verdict": "The delta2 path-choice gate is now explicit. C_delta2 cannot be used for C6 cancellation until the second-variation path is fixed before the finite matrix computation. The preferred route is the same ambient linear embedding strain used by the first-strain audits, with its induced second metric/operator derivative written explicitly; conformal-path calculations remain diagnostic unless a slice theorem is supplied.",
}

Path("s2t_c6_l21_delta2_path_choice_gate_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "path_choice_fixed": False,
    "allowed_paths": [path["path_id"] for path in allowed_paths],
    "master_matrix_should_upgrade": False,
}, indent=2, ensure_ascii=False))