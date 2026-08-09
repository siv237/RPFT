import json
from pathlib import Path

full_gate = json.loads(Path("s2t_c6_l21_full_operator_rescue_gate_results.json").read_text())
lap_var = json.loads(Path("s2t_c6_l21_laplacian_variation_results.json").read_text())
scale = json.loads(Path("s2t_c6_l21_n3_obstruction_scale_results.json").read_text())
projection = json.loads(Path("s2t_c6_l21_n3_explicit_projection_results.json").read_text())

trace = projection["projection"]["projected_gram_trace"]
rank = projection["projection"]["projected_rank_numeric"]
trace_over_gap_squared = projection["second_order_bookkeeping_proxy"]["trace_over_gap_squared"]
gap_ratio = scale["comparisons"]["trace_over_gap_squared_to_Nneed_gap_ratio"]

TERM_TO_OUTPUT = {
    "connection_variation_terms": {
        "required_output": "matrix block C_conn[1,3] in the explicit n=1 Killing basis and n=3 coexact basis",
        "zero_test": "Does C_principal + C_conn cancel in the six-dimensional image before Ricci/projector terms?",
    },
    "curvature_Ricci_variation": {
        "required_output": "matrix block C_Ric[1,3] including index-raising variation",
        "zero_test": "Does C_principal + C_conn + C_Ric reduce the projected rank or trace?",
    },
    "coexact_projector_variation": {
        "required_output": "variation of Pi_coex and the induced correction to the n=1<->n=3 block",
        "zero_test": "Does the moving transverse slice cancel the apparent fixed-slice projection?",
    },
    "Hilbert_inner_product_variation": {
        "required_output": "metric variation of matrix elements, volume density, one-form contraction, and normalization",
        "zero_test": "Does the varied Hilbert metric remove the trace-80 block without fitted normalization?",
    },
    "second_variation_delta2_Delta": {
        "required_output": "direct Tr(Delta^{-1} delta2 Delta) finite low-shell part or proof it is local/subtracted/cancelled",
        "zero_test": "Does the direct second-variation term cancel the trace-square contribution in the same scheme?",
    },
}

checklist = []
for item in full_gate["remaining_rescue_terms"]:
    term = item["term"]
    checklist.append({
        "term": term,
        "current_status": item["current_status"],
        "must_do": item["must_do"],
        "why_it_matters": item["why_it_matters"],
        **TERM_TO_OUTPUT[term],
        "pass_condition": "written formula plus evaluated low-shell contribution with fixed signs and quotient normalization",
        "fail_condition": "term omitted, only asserted verbally, or adjusted after seeing alpha target",
    })

results = {
    "status": "full_operator_rescue_checklist_fixed_after_large_n3_obstruction",
    "inputs": [
        "s2t_c6_l21_full_operator_rescue_gate_results.json",
        "s2t_c6_l21_laplacian_variation_results.json",
        "s2t_c6_l21_n3_obstruction_scale_results.json",
        "s2t_c6_l21_n3_explicit_projection_results.json",
    ],
    "obstruction_to_rescue": {
        "projected_trace": trace,
        "projected_rank": rank,
        "trace_over_gap_squared": trace_over_gap_squared,
        "ratio_to_Nneed_minus_10_gap": gap_ratio,
        "meaning": "The obstruction is too large for a rounding/scheme-gap story; the checklist must produce a real cancellation or no-fit absorption.",
    },
    "required_operator_checklist": checklist,
    "global_pass_conditions": [
        {
            "condition": "complete_operator_formula",
            "meaning": "All principal, connection, Ricci, projector, Hilbert-metric, and delta2 terms are present with signs.",
        },
        {
            "condition": "same_basis_same_normalization",
            "meaning": "All terms are evaluated in the same quotient-normalized n=1 and n=3 bases; no cover factor is inserted after the fact.",
        },
        {
            "condition": "trace80_cancelled_or_absorbed",
            "meaning": "The combined finite low-shell contribution either vanishes or is mapped to the existing pi^-4/P02 residue by a derived identity.",
        },
        {
            "condition": "no_hidden_finite_counterterm",
            "meaning": "No finite subtraction is chosen after seeing alpha or the trace-80 result.",
        },
    ],
    "global_fail_conditions": [
        {
            "condition": "any_required_term_missing",
            "effect": "C6 remains open; pi^-4 cannot be called mature determinant theorem.",
        },
        {
            "condition": "nonzero_independent_low_shell_trace_survives",
            "effect": "Clean rank-10 determinant theorem is blocked in the physical coexact quotient.",
        },
        {
            "condition": "rescue_requires_adjustable_finite_scheme",
            "effect": "Downgrade to phenomenological/structural compression under the no-hidden-parameter rule.",
        },
    ],
    "plain_language": (
        "The third-floor fire is real and not small. The checklist says exactly which five extinguishers must be used next. "
        "If any extinguisher is only waved at, not computed, C6 is not closed."
    ),
    "verdict": (
        "After the explicit nonzero n=3 projection and scale audit, the C6 rescue problem is reduced to a concrete full-operator checklist. "
        "Connection, Ricci, coexact-projector, Hilbert-metric, and direct delta2-Delta terms must be derived and evaluated in the same quotient-normalized low-shell bases. "
        "Only an explicit cancellation or a no-fit absorption identity can promote pi^-4 beyond structural compression."
    ),
}

Path("s2t_c6_l21_full_operator_checklist_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "required_terms": len(checklist),
    "projected_trace": trace,
    "gap_ratio": gap_ratio,
}, indent=2, ensure_ascii=False))