import json
from pathlib import Path

sprint = json.loads(Path("s2t_c6_timeboxed_operator_sprint_results.json").read_text())
connection2 = json.loads(Path("s2t_c6_l21_delta2_second_connection_formula_results.json").read_text())
ambient = json.loads(Path("s2t_c6_l21_delta2_ambient_path_formula_results.json").read_text())
c11 = json.loads(Path("s2t_c6_l21_delta2_c11_setup_results.json").read_text())

results = {
    "status": "delta2_Gamma_AB_expansion_formula_fixed_C11_insertion_rule_still_missing",
    "inputs": [
        "s2t_c6_timeboxed_operator_sprint_results.json",
        "s2t_c6_l21_delta2_second_connection_formula_results.json",
        "s2t_c6_l21_delta2_ambient_path_formula_results.json",
        "s2t_c6_l21_delta2_c11_setup_results.json",
    ],
    "convention": {
        "background_connection": "Use the round L(2,1) background covariant derivative nabla to write the Levi-Civita connection difference tensor.",
        "metric_path": ambient["selected_path"],
        "metric_derivative_names": {
            "h_A_ij": "partial_A g_ij",
            "k_AB_ij": "partial_A partial_B g_ij",
            "m_A^kl": "partial_A g^{kl} = -h_A^{kl}",
        },
        "why_background_nabla": "It avoids double-counting covariant-derivative variation; connection variation appears in the rough-Laplacian operator slots, not inside this Gamma difference formula.",
    },
    "definitions": {
        "C_A_ijl": "nabla_i h^A_jl + nabla_j h^A_il - nabla_l h^A_ij",
        "C_B_ijl": "nabla_i h^B_jl + nabla_j h^B_il - nabla_l h^B_ij",
        "C_AB_ijl": "nabla_i k^AB_jl + nabla_j k^AB_il - nabla_l k^AB_ij",
        "first_connection": "Gamma_A^k_ij = 1/2 g^{kl} C_A_ijl",
    },
    "expanded_formula": {
        "mixed_second_connection": "Gamma_AB^k_ij = 1/2 [ g^{kl} C_AB_ijl + m_A^{kl} C_B_ijl + m_B^{kl} C_A_ijl ]",
        "same_direction_AA": "Gamma_AA^k_ij = 1/2 [ g^{kl} C_AA_ijl + 2 m_A^{kl} C_A_ijl ]",
        "ambient_path_insertions": {
            "h_A": ambient["metric_derivatives"]["first_derivative_same_A"],
            "k_AB": ambient["metric_derivatives"]["mixed_second_derivative_A_B"],
            "same_A_k_AA": ambient["metric_derivatives"]["second_derivative_same_A"],
        },
        "not_included_here": [
            "products Gamma_A Gamma_B inside second variation of two covariant derivatives",
            "inverse-metric/principal second-symbol block already fixed separately",
            "Ricci, projector, Hilbert/basis, and local counterterm pieces",
        ],
    },
    "rough_laplacian_connection_slots_next": [
        {
            "slot": "single_Gamma_AB_derivative",
            "schematic": "-g^{ij}[ -nabla_i(Gamma_AB^d_jc alpha_d) - Gamma_AB^d_ij nabla_d alpha_c - Gamma_AB^d_ic nabla_j alpha_d ] with index placement checked",
            "status": "not_expanded_to_matrix",
        },
        {
            "slot": "Gamma_A_Gamma_B_products",
            "schematic": "terms from applying delta_A nabla and delta_B nabla in both orders to the one-form second covariant derivative",
            "status": "not_expanded_to_matrix",
        },
        {
            "slot": "inverse_metric_first_connection_cross",
            "schematic": "-m_A^{ij} connection_B_terms - m_B^{ij} connection_A_terms in the rough Laplacian",
            "status": "not_expanded_to_matrix",
        },
    ],
    "C11_relevance": {
        "target": c11["target_block"],
        "what_is_now_ready": "Gamma_AB tensor formula has fixed signs and slots in a background-nabla convention.",
        "what_is_not_ready": "The full rough-Laplacian connection operator and its 6x6 C11 matrix entries are not evaluated.",
        "next_matrix_enabling_step": "expand the three rough_laplacian_connection_slots_next against n=1 Killing one-forms and classify which integrals reduce to existing q_A overlaps.",
    },
    "pass_fail": [
        {
            "test": "Gamma_AB_formula_written",
            "status": "pass",
            "meaning": "The mixed second connection difference tensor is now explicit in one convention.",
        },
        {
            "test": "rough_laplacian_connection_operator_expanded",
            "status": "not_yet",
            "meaning": "Gamma_AB must still be inserted into -g^{ij} nabla_i nabla_j acting on one-forms.",
        },
        {
            "test": "C11_connection_matrix_evaluated",
            "status": "not_yet",
            "meaning": "No C_conn2[1,1] entries or traces have been computed.",
        },
    ],
    "plain_language": "One gear tooth is cut: we now know the second-connection tensor itself. But it still has to be mounted inside the Laplacian before it can turn the C11 box.",
    "verdict": "The timeboxed C6 sprint has produced its first operator content: an explicit background-covariant formula for delta2 Gamma_AB on the locked ambient path. This is progress beyond a label. It does not yet evaluate C_delta2[1,1]; the next required step is inserting Gamma_AB, Gamma_A Gamma_B products, and inverse-metric/first-connection crosses into the rough one-form Laplacian and then reducing the result against the six n=1 Killing states.",
}

Path("s2t_c6_l21_delta2_gamma_expansion_formula_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "Gamma_AB_formula_written": True,
    "rough_laplacian_connection_operator_expanded": False,
    "C11_connection_matrix_evaluated": False,
}, indent=2, ensure_ascii=False))