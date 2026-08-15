import json
from pathlib import Path

ambient = json.loads(Path("s2t_c6_l21_delta2_ambient_path_formula_results.json").read_text())
ricci1 = json.loads(Path("s2t_c6_l21_ricci_variation_formula_results.json").read_text())
decomp = json.loads(Path("s2t_c6_l21_delta2_operator_decomposition_results.json").read_text())

results = {
    "status": "delta2_second_ricci_formula_skeleton_fixed_delta2Ricci_expansion_missing",
    "inputs": [
        "s2t_c6_l21_delta2_ambient_path_formula_results.json",
        "s2t_c6_l21_ricci_variation_formula_results.json",
        "s2t_c6_l21_delta2_operator_decomposition_results.json",
    ],
    "operator_convention": {
        "laplacian": "Delta_1 alpha = -nabla^2 alpha + Ric(alpha)",
        "this_block_only": "second variation of the Ricci/curvature endomorphism part of the one-form Weitzenbock operator",
        "not_included_here": [
            "principal second-symbol block",
            "rough-laplacian connection second-variation block",
            "coexact projector second variation",
            "Hilbert/basis second variation",
            "local counterterm classifier",
        ],
    },
    "ambient_metric_path": ambient["selected_path"],
    "metric_derivatives": ambient["metric_derivatives"],
    "first_ricci_reference": ricci1["ricci_variation_formula"],
    "ricci_second_variation_skeleton": {
        "curvature_part": "delta2_AB Ric_ij from variation_B[delta_A Ric_ij], including delta2 Gamma derivatives and delta Gamma_A delta Gamma_B curvature products",
        "operator_index_part": "delta2_AB(Ric_i^j alpha_j) includes delta2 Ric_i^j alpha_j plus all index-raising products from partial_A g^{-1}, partial_B g^{-1}, and partial_AB g^{-1}",
        "expanded_obligation": [
            "covariant Ricci second variation: partial_AB Ric_ij in one ambient-path convention",
            "mixed-index conversion: partial_AB(g^{jk} Ric_ik)",
            "products (partial_A g^{-1})(partial_B Ric) and (partial_B g^{-1})(partial_A Ric)",
            "background-curvature index term (partial_AB g^{-1}) Ric_background",
            "symmetrization in A,B and sign convention matching Delta_1=-nabla^2+Ric",
        ],
        "warning": "This audit fixes the Ricci second-variation slots and signs to track, not the fully expanded delta2 Ricci tensor on S3/RP3.",
    },
    "constant_curvature_context": {
        "background": "unit S3/RP3 has Ric_ij=2 g_ij in dimension 3",
        "why_not_drop": "Even on a constant-curvature background, metric variation changes Ric and the mixed Ric_i^j endomorphism; this block can contribute finite low-shell data.",
        "conformal_slice_reference": "For h=2qg, first variation used delta Ric_ab=-nabla_a nabla_b q-g_ab nabla^2 q plus index raising -4q alpha_a, but the ambient theorem path is raw pullback unless a slice theorem is supplied.",
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
            "meaning": "The second Ricci/curvature slots are now identified and separated from principal/connection blocks.",
        },
        {
            "test": "delta2Ricci_fully_expanded",
            "status": "not_yet",
            "meaning": "The complete ambient-path tensor expression for delta2 Ricci_AB is still missing.",
        },
        {
            "test": "diagonal_matrix_traces_evaluated",
            "status": "not_yet",
            "meaning": "No diagonal C_delta2 traces have been computed from the Ricci block.",
        },
    ],
    "plain_language": "The third gear is curvature. RP3 is curved, so this gear cannot be thrown away. We have marked its slot, but the actual curved gear is not cut yet.",
    "verdict": "The second Ricci/curvature subblock is now fixed at skeleton level. It consists of delta2 Ricci_AB, mixed-index raising terms, products of first inverse-metric and first Ricci variations, and background-curvature terms from partial_AB g^{-1}. This is not yet the full delta2 Ricci tensor or a finite trace computation; diagonal C_delta2 traces remain open.",
}

Path("s2t_c6_l21_delta2_second_ricci_formula_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "formula_skeleton_written": True,
    "delta2Ricci_fully_expanded": False,
    "matrix_traces_evaluated": False,
}, indent=2, ensure_ascii=False))