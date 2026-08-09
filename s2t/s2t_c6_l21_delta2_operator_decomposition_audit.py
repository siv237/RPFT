import json
from pathlib import Path

ambient_path = json.loads(Path("s2t_c6_l21_delta2_ambient_path_formula_results.json").read_text())
finite_spec = json.loads(Path("s2t_c6_l21_delta2_finite_block_spec_results.json").read_text())
checklist = json.loads(Path("s2t_c6_l21_full_operator_checklist_results.json").read_text())

operator_decomposition = [
    {
        "block": "principal_second_symbol",
        "schematic_role": "second variation of the inverse metric contraction in -g^{ij} nabla_i nabla_j alpha",
        "depends_on": ["g'_A", "g''_{A,B}", "first connection terms through covariant second derivatives"],
        "required_output": "diagonal shell trace contribution to C_delta2[1,1] and C_delta2[3,3]",
        "status": "not_derived",
    },
    {
        "block": "second_connection_terms",
        "schematic_role": "terms containing delta2 Gamma and products delta Gamma_A delta Gamma_B inside the rough one-form Laplacian",
        "depends_on": ["g'_A", "g''_{A,B}", "first and second derivatives of the ambient strain"],
        "required_output": "operator formula before coexact projection plus diagonal matrix traces",
        "status": "not_derived",
    },
    {
        "block": "second_ricci_curvature_terms",
        "schematic_role": "second variation of Ric(alpha) and index raising/lowering in Delta_1=-nabla^2+Ric",
        "depends_on": ["delta Ric_A", "delta2 Ric_AB", "metric index variation"],
        "required_output": "curvature part of C_delta2 diagonal shell traces",
        "status": "not_derived",
    },
    {
        "block": "coexact_projector_second_variation",
        "schematic_role": "second-order change of Pi_coex Delta Pi_coex and cross terms from delta Pi_A delta Delta_B",
        "depends_on": ["Pi=I-d Delta0^-1 delta", "delta Pi_A", "delta2 Pi_AB"],
        "required_output": "reduced coexact operator on moving transverse slice",
        "status": "not_derived",
    },
    {
        "block": "hilbert_basis_second_variation",
        "schematic_role": "second-order Hilbert metric, volume, and orthonormal basis corrections entering determinant matrix traces",
        "depends_on": ["delta <.,.>", "delta2 <.,.>", "basis renormalization convention"],
        "required_output": "self-adjoint diagonal trace in the varied quotient-normalized Hilbert space",
        "status": "not_derived",
    },
    {
        "block": "local_counterterm_classifier",
        "schematic_role": "separate UV/local heat-kernel contributions from finite low-shell spectral data before any subtraction",
        "depends_on": ["chosen subtraction scheme", "finite low-shell projection"],
        "required_output": "proof local-only or finite residual table",
        "status": "not_done",
    },
]

results = {
    "status": "delta2_operator_decomposition_fixed_all_subblocks_missing",
    "inputs": [
        "s2t_c6_l21_delta2_ambient_path_formula_results.json",
        "s2t_c6_l21_delta2_finite_block_spec_results.json",
        "s2t_c6_l21_full_operator_checklist_results.json",
    ],
    "selected_path_summary": ambient_path["selected_path"],
    "metric_derivatives": ambient_path["metric_derivatives"],
    "target_operator": {
        "object": "delta2 Delta_1,coex[A,B] on L(2,1) under the ambient pullback path",
        "trace_role": "1/2 Tr(Delta^-1 delta2 Delta) in the coexact bosonic determinant before subtraction choices",
        "finite_trace_targets": ["C_delta2[1,1]", "C_delta2[3,3]"],
    },
    "operator_decomposition": operator_decomposition,
    "finite_block_counts": finite_spec["counts"],
    "full_operator_context_status": checklist["status"],
    "minimal_pass_condition": {
        "formula_level": "all six subblocks above must be written in one convention with signs",
        "matrix_level": "diagonal n=1 and n=3 traces over the 55 symmetric deformation pairs must be evaluated or proven local/zero",
        "scheme_level": "local subtraction and quotient Hilbert convention must be fixed before comparing with alpha",
    },
    "current_status": {
        "ambient_path_formula_fixed": True,
        "delta2_operator_formula_complete": False,
        "delta2_matrix_traces_evaluated": False,
        "C6_status_upgrade_allowed": False,
    },
    "plain_language": "We have named the machine parts for the fifth extinguisher. None of the parts has been machined yet, so it cannot put out the trace-80 fire today.",
    "verdict": "The delta2 operator task is now decomposed into six mandatory subblocks: principal second-symbol, second connection, second Ricci/curvature, second coexact-projector, second Hilbert/basis variation, and local-counterterm classification. This is progress in scoping, not a C6 proof. The actual delta2 Delta_1,coex formula and diagonal C_delta2 traces remain missing.",
}

Path("s2t_c6_l21_delta2_operator_decomposition_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "subblocks": len(operator_decomposition),
    "ambient_path_formula_fixed": True,
    "delta2_operator_formula_complete": False,
    "delta2_matrix_traces_evaluated": False,
}, indent=2, ensure_ascii=False))