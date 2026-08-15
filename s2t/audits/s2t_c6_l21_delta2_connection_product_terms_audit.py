import json
from pathlib import Path

insertion = json.loads(Path("s2t_c6_l21_delta2_connection_laplacian_insertion_results.json").read_text())
gamma = json.loads(Path("s2t_c6_l21_delta2_gamma_expansion_formula_results.json").read_text())
c11 = json.loads(Path("s2t_c6_l21_delta2_c11_setup_results.json").read_text())

results = {
    "status": "delta2_connection_product_terms_expansion_family_fixed_integrals_missing",
    "inputs": [
        "s2t_c6_l21_delta2_connection_laplacian_insertion_results.json",
        "s2t_c6_l21_delta2_gamma_expansion_formula_results.json",
        "s2t_c6_l21_delta2_c11_setup_results.json",
    ],
    "operator_convention": insertion["operator_convention"],
    "product_term_source": {
        "first_connection_template": insertion["first_connection_insertion_template"],
        "product_slot": next(row for row in insertion["mixed_second_connection_insertion_slots"] if row["slot"] == "Gamma_A_Gamma_B_products"),
        "first_connection_formula": gamma["definitions"]["first_connection"],
    },
    "expanded_product_families": [
        {
            "family": "derivative_index_products",
            "schematic_terms": [
                "+ Gamma_A^p_ij Gamma_B^d_pc alpha_d + A<->B",
                "+ Gamma_A^p_ii_like acting on the first derivative index of T_B, with contraction by g^{ij}; keep explicit indices before simplifying",
            ],
            "meaning": "When D_A acts on the derivative indices of T_B, connection factors multiply Gamma_B alpha or Gamma_B nabla alpha terms.",
            "status": "family_fixed_exact_index_cleanup_pending",
        },
        {
            "family": "one_form_component_products",
            "schematic_terms": [
                "+ Gamma_A^p_ic Gamma_B^d_jp alpha_d + A<->B",
                "+ Gamma_A^p_jc Gamma_B^d_ip alpha_d + A<->B",
            ],
            "meaning": "The variation of the one-form component connection index produces Gamma_A Gamma_B alpha contractions.",
            "status": "family_fixed_exact_index_cleanup_pending",
        },
        {
            "family": "mixed_gradient_products",
            "schematic_terms": [
                "+ Gamma_A Gamma_B nabla alpha terms from D_A acting on nabla alpha inside T_B, plus A<->B",
                "+ Gamma_A nabla(Gamma_B) alpha and Gamma_B nabla(Gamma_A) alpha terms only if not already assigned to single Gamma_AB derivative bookkeeping",
            ],
            "meaning": "These terms decide whether product pieces reduce to existing Killing derivative identities or require new tensor integrals.",
            "status": "family_fixed_derivative_assignment_pending",
        },
    ],
    "double_counting_guardrails": [
        "Do not include principal second-symbol terms; those are already in delta2_principal_AB.",
        "Do not include single Gamma_AB derivative terms; those belong to L_conn2_single_AB.",
        "Do not include metric-cross terms; those belong to L_conn2_metric_cross_AB.",
        "Symmetrize A,B exactly once; do not add an extra factor of two after summing A<->B.",
    ],
    "C11_reduction_plan": {
        "target": c11["target_block"],
        "matrix_template": insertion["C11_insertion_rule_progress"]["matrix_element_template"],
        "basis": c11["locked_conventions"]["basis_labels_expected"],
        "normalization": c11["locked_conventions"]["normalization_rule"],
        "next_reduction_tests": [
            "replace alpha by each Killing one-form E_rs and use nabla_i E_j antisymmetry identities",
            "classify terms as q_A q_B overlaps, grad q_A grad q_B overlaps, Hessian/q mixed overlaps, or genuinely new tensor integrals",
            "check whether trace direction and traceless P02 directions decouple as expected",
            "build symbolic/index table before numerical integration over 55 symmetric A,B pairs",
        ],
    },
    "pass_fail": [
        {
            "test": "product_families_named",
            "status": "pass",
            "meaning": "Gamma_A Gamma_B product contribution is split into derivative-index, one-form-component, and mixed-gradient families.",
        },
        {
            "test": "exact_index_table_completed",
            "status": "not_yet",
            "meaning": "The family-level expressions still need exact index cleanup before integration.",
        },
        {
            "test": "C11_product_integrals_evaluated",
            "status": "not_yet",
            "meaning": "No C11 product-term matrix entries have been computed.",
        },
    ],
    "plain_language": "The dirty double-gear piece is now sorted into three bins. We still have to count the teeth in each bin before multiplying against the six C11 basis vectors.",
    "verdict": "The Gamma_A Gamma_B product part of the second-connection sprint is now organized into concrete term families with double-counting guardrails. This advances the rough-Laplacian insertion toward a C11 reduction plan, but it is still not a matrix computation: exact index cleanup and integrals against the six n=1 Killing states remain open.",
}

Path("s2t_c6_l21_delta2_connection_product_terms_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "product_families_named": True,
    "exact_index_table_completed": False,
    "C11_product_integrals_evaluated": False,
}, indent=2, ensure_ascii=False))