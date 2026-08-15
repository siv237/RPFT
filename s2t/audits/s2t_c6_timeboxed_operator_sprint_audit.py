import json
from pathlib import Path

direction = json.loads(Path("s2t_direction_reaudit_20260714_results.json").read_text())
c11 = json.loads(Path("s2t_c6_l21_delta2_c11_setup_results.json").read_text())
connection2 = json.loads(Path("s2t_c6_l21_delta2_second_connection_formula_results.json").read_text())
principal2 = json.loads(Path("s2t_c6_l21_delta2_principal_second_symbol_formula_results.json").read_text())
ambient = json.loads(Path("s2t_c6_l21_delta2_ambient_path_formula_results.json").read_text())

results = {
    "status": "C6_timeboxed_operator_sprint_defined_second_connection_first",
    "inputs": [
        "s2t_direction_reaudit_20260714_results.json",
        "s2t_c6_l21_delta2_c11_setup_results.json",
        "s2t_c6_l21_delta2_second_connection_formula_results.json",
        "s2t_c6_l21_delta2_principal_second_symbol_formula_results.json",
        "s2t_c6_l21_delta2_ambient_path_formula_results.json",
    ],
    "sprint_policy": {
        "why_timeboxed": direction["decision"]["why"],
        "not_allowed": [
            "add more C6 labels without matrix-enabling formulas",
            "change the ambient path after seeing numbers",
            "use local counterterms to erase finite low-shell data after the fact",
            "count off-diagonal archive blocks as direct delta2 trace data",
        ],
        "success_definition": "produce one operator expansion that can be inserted into C_delta2[1,1], or prove same-scheme locality/compensation for that piece",
        "fallback_trigger": "if the next concrete operator expansion still cannot feed C11/C33 or locality/compensation, shift effort to external determinant gate and neutrino overlap lemma",
    },
    "chosen_first_target": {
        "target": "delta2_second_connection_AB",
        "source_status": connection2["status"],
        "reason": [
            "principal second-symbol is already formula-fixed, so the next missing rough-Laplacian piece is connection2",
            "connection2 contributes before Ricci/projector/Hilbert bookkeeping in the operator assembly",
            "it is shared by C_delta2[1,1] and C_delta2[3,3] and can expose whether cancellation is plausible",
            "it is concrete enough to produce tensor slots rather than another high-level roadmap label",
        ],
        "primary_matrix_target": c11["target_block"],
    },
    "required_deliverables": [
        {
            "deliverable": "explicit delta2 Gamma_AB slots on ambient path",
            "must_include": [
                "k_AB contribution from second metric derivative",
                "inverse-metric variation times first connection variation",
                "covariant derivative variation acting on h_A/h_B",
                "delta Gamma_A delta Gamma_B products with symmetrization in A,B",
            ],
            "done_when": "each slot has sign convention and index placement compatible with Delta_1 alpha = -g^{ij} nabla_i nabla_j alpha + Ric(alpha)",
        },
        {
            "deliverable": "C11 insertion rule for connection2",
            "must_include": [
                "six n=1 Killing basis labels E01..E23",
                "quotient-orthonormal inner product with no cover factor",
                "which pieces can be evaluated by existing q_A overlap identities and which need new integrals",
            ],
            "done_when": "the result can create a C_conn2[1,1] matrix task or a proof that the piece is local/zero/compensated",
        },
        {
            "deliverable": "go/no-go note after the sprint",
            "must_include": [
                "does connection2 plausibly cancel principal2 in C11?",
                "does it introduce new n=3-sized leakage?",
                "does it force fallback to external/neutrino tracks?",
            ],
            "done_when": "the next decision is compute C11 contribution, continue to Ricci2, or trigger fallback",
        },
    ],
    "known_starting_point": {
        "principal2_status": principal2["status"],
        "connection2_status": connection2["status"],
        "ambient_path": ambient["selected_path"]["path_id"],
        "C11_raw_entries": c11["target_block"]["raw_entries_all_pairs"],
        "C11_values_evaluated": False,
    },
    "plain_language": "The next dig is not a new tunnel map. It is one tool: expand the second-connection gear enough that it can touch the small C11 box.",
    "verdict": "The C6 timeboxed sprint is now defined. Continue C6 only by expanding the second-connection part delta2 Gamma_AB on the locked ambient path toward a real C_delta2[1,1] insertion rule. This is the first computation-facing target after principal2. If this sprint cannot produce matrix-enabling content, locality/compensation, or a clear next computation, the direction audit requires shifting effort toward the external determinant gate and neutrino overlap lemma rather than adding more C6 scoping layers.",
}

Path("s2t_c6_timeboxed_operator_sprint_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "chosen_first_target": results["chosen_first_target"]["target"],
    "primary_matrix_target": results["chosen_first_target"]["primary_matrix_target"]["name"],
    "C11_raw_entries": results["known_starting_point"]["C11_raw_entries"],
    "fallback_if_no_matrix_enabling_content": True,
}, indent=2, ensure_ascii=False))