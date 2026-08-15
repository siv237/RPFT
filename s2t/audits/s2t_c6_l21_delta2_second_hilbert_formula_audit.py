import json
from pathlib import Path

ambient = json.loads(Path("s2t_c6_l21_delta2_ambient_path_formula_results.json").read_text())
hilbert1 = json.loads(Path("s2t_c6_l21_hilbert_variation_formula_results.json").read_text())
decomp = json.loads(Path("s2t_c6_l21_delta2_operator_decomposition_results.json").read_text())

results = {
    "status": "delta2_second_hilbert_formula_skeleton_fixed_basis_expansion_missing",
    "inputs": [
        "s2t_c6_l21_delta2_ambient_path_formula_results.json",
        "s2t_c6_l21_hilbert_variation_formula_results.json",
        "s2t_c6_l21_delta2_operator_decomposition_results.json",
    ],
    "operator_convention": {
        "inner_product": "<alpha,beta>_g = integral g^{ab} alpha_a beta_b dvol_g",
        "this_block_only": "second-order Hilbert metric, volume, and basis/orthonormalization corrections to determinant matrix traces",
        "not_included_here": [
            "principal/operator second-symbol terms",
            "connection/Ricci/projector operator terms",
            "local counterterm classifier",
        ],
    },
    "ambient_metric_path": ambient["selected_path"],
    "metric_derivatives": ambient["metric_derivatives"],
    "first_hilbert_reference": hilbert1["hilbert_variation_formula"],
    "second_hilbert_skeleton": {
        "fixed_component_inner_product_second_variation": [
            "second variation of g^{ab} alpha_a beta_b",
            "cross term from first variation of g^{ab} and first variation of dvol_g",
            "second variation of dvol_g from h_A, h_B, and k_AB",
        ],
        "volume_form_formula_slots": {
            "first": "partial_A dvol = 1/2 tr(h_A) dvol",
            "mixed_second": "partial_AB dvol = [1/2 tr(k_AB) + 1/4 tr(h_A)tr(h_B) - 1/2 tr(h_A h_B)] dvol, with background index raising",
        },
        "basis_variation_slots": [
            "orthonormal basis derivative needed to keep <e_i(eps),e_j(eps)>_eps=delta_ij",
            "second derivative / Gram-Schmidt correction for diagonal trace consistency",
            "possible eigenbasis rotation inside degenerate n=1 and n=3 shells",
            "self-adjoint representation of the reduced operator in the varied Hilbert metric",
        ],
        "warning": "This audit fixes the required Hilbert/basis slots; it does not choose a basis transport rule or evaluate any Gram correction.",
    },
    "determinant_trace_role": {
        "why_it_matters": "A fixed-metric Gram trace is not the final determinant coefficient if the Hilbert metric and orthonormal basis move with epsilon.",
        "required_consistency": "Operator second-variation traces and trace-square terms must be represented in the same quotient-normalized varied Hilbert space.",
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
            "meaning": "Second Hilbert/volume/basis correction slots are now identified.",
        },
        {
            "test": "basis_transport_chosen",
            "status": "not_yet",
            "meaning": "No canonical orthonormal-basis transport or gauge has been selected.",
        },
        {
            "test": "second_Gram_correction_evaluated",
            "status": "not_yet",
            "meaning": "No diagonal C_delta2 trace correction from Hilbert/basis variation has been computed.",
        },
        {
            "test": "self_adjointness_verified",
            "status": "not_yet",
            "meaning": "The final reduced operator has not been checked in the second-order varied Hilbert metric.",
        },
    ],
    "plain_language": "The fifth gear is the ruler changing for the second time. We know which marks on the ruler can stretch, but we have not recalibrated the ruler yet.",
    "verdict": "The second Hilbert/basis subblock is now fixed at skeleton level. It contains second variation of the one-form inner product, volume-form second variation, basis transport/Gram-Schmidt corrections, degenerate-shell rotations, and self-adjoint representation of the reduced operator. This is not yet a basis convention or finite trace computation; diagonal C_delta2 corrections remain open.",
}

Path("s2t_c6_l21_delta2_second_hilbert_formula_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "formula_skeleton_written": True,
    "basis_transport_chosen": False,
    "second_Gram_correction_evaluated": False,
    "self_adjointness_verified": False,
}, indent=2, ensure_ascii=False))