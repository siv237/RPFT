import json
from pathlib import Path

ambient = json.loads(Path("s2t_c6_l21_delta2_ambient_path_formula_results.json").read_text())
projector1 = json.loads(Path("s2t_c6_l21_projector_variation_formula_results.json").read_text())
decomp = json.loads(Path("s2t_c6_l21_delta2_operator_decomposition_results.json").read_text())

results = {
    "status": "delta2_second_projector_formula_skeleton_fixed_delta2Pi_expansion_missing",
    "inputs": [
        "s2t_c6_l21_delta2_ambient_path_formula_results.json",
        "s2t_c6_l21_projector_variation_formula_results.json",
        "s2t_c6_l21_delta2_operator_decomposition_results.json",
    ],
    "operator_convention": {
        "projector": "Pi_coex = I - d Delta_0^{-1} delta on non-harmonic one-forms, b1(L(2,1))=0",
        "reduced_operator": "L_phys = Pi_coex Delta_1 Pi_coex restricted to the moving coexact slice",
        "this_block_only": "second variation caused by the moving coexact projector and side-projector/reduction terms",
        "not_included_here": [
            "principal second-symbol block",
            "rough-laplacian second-connection block",
            "Ricci/curvature second block",
            "Hilbert/basis second variation",
            "local counterterm classifier",
        ],
    },
    "ambient_metric_path": ambient["selected_path"],
    "first_projector_reference": projector1["projector_variation_formula"],
    "second_projector_skeleton": {
        "inverse_scalar_laplacian_second_variation": "delta2(Delta_0^{-1}) = Delta_0^{-1}(delta_A Delta_0)Delta_0^{-1}(delta_B Delta_0)Delta_0^{-1} + A<->B - Delta_0^{-1}(delta2_AB Delta_0)Delta_0^{-1}",
        "codifferential_second_variation": "delta2_AB delta_g must be derived from the ambient metric path and Hodge-star/volume variation",
        "projector_second_variation": "delta2_AB Pi = -d[ delta2(Delta_0^{-1}) delta + delta_A(Delta_0^{-1}) delta_B delta + delta_B(Delta_0^{-1}) delta_A delta + Delta_0^{-1} delta2_AB delta ]",
        "warning": "Formula is schematic on det-prime scalar modes; zero-mode/gauge-volume conventions must match the physical quotient scheme.",
    },
    "reduced_operator_second_variation_skeleton": {
        "delta2_L_phys": [
            "Pi delta2Delta_1 Pi",
            "(delta2 Pi) Delta_1 Pi + Pi Delta_1 (delta2 Pi)",
            "(delta Pi_A) Delta_1 (delta Pi_B) + (delta Pi_B) Delta_1 (delta Pi_A)",
            "(delta Pi_A)(delta_B Delta_1)Pi + (delta Pi_B)(delta_A Delta_1)Pi",
            "Pi(delta_A Delta_1)(delta Pi_B) + Pi(delta_B Delta_1)(delta Pi_A)",
        ],
        "self_adjointness_obligation": "The sum must be symmetric/self-adjoint in the varied quotient Hilbert metric before determinant traces are trusted.",
        "coexact_input_warning": "Terms that vanish on initially coexact input may reappear after delta Delta_1 or a side projector acts; do not drop side terms prematurely.",
    },
    "matrix_task": {
        "required_targets": decomp["target_operator"]["finite_trace_targets"],
        "required_pairs": decomp["finite_block_counts"]["symmetric_deformation_pairs_A_B"],
        "required_raw_diagonal_entries": decomp["finite_block_counts"]["required_diagonal_entries_all_pairs"],
        "status": "not_evaluated",
    },
    "pass_fail": [
        {
            "test": "formula_skeleton_written",
            "status": "pass",
            "meaning": "Second projector and reduced-operator side terms are now identified.",
        },
        {
            "test": "delta2Pi_fully_expanded",
            "status": "not_yet",
            "meaning": "The complete ambient-path expression for delta2 Pi_coex is still missing.",
        },
        {
            "test": "self_adjointness_verified",
            "status": "not_yet",
            "meaning": "The reduced second-order operator has not been checked in the varied Hilbert metric.",
        },
        {
            "test": "diagonal_matrix_traces_evaluated",
            "status": "not_yet",
            "meaning": "No diagonal C_delta2 traces have been computed from projector terms.",
        },
    ],
    "plain_language": "The fourth gear is the moving doorway at second order. We now know every hinge that can move twice or cross-move with the operator, but no hinge has been measured yet.",
    "verdict": "The second coexact-projector subblock is now fixed at skeleton level. It consists of delta2 Pi_coex, inverse scalar-Laplacian second variation, codifferential second variation, side-projector terms, and cross terms with first operator variations. This is not yet a full delta2 Pi formula or a finite trace computation; self-adjointness and diagonal C_delta2 traces remain open.",
}

Path("s2t_c6_l21_delta2_second_projector_formula_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "formula_skeleton_written": True,
    "delta2Pi_fully_expanded": False,
    "self_adjointness_verified": False,
    "matrix_traces_evaluated": False,
}, indent=2, ensure_ascii=False))