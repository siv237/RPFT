import json
from pathlib import Path

projection = json.loads(Path("s2t_c6_l21_n3_explicit_projection_results.json").read_text())
proxy = json.loads(Path("s2t_c6_l21_n3_proxy_obstruction_scale_results.json").read_text())
full_gate = json.loads(Path("s2t_c6_l21_full_operator_rescue_gate_results.json").read_text())

trace = projection["projection"]["projected_gram_trace"]
rank = projection["projection"]["projected_rank_numeric"]
eigs = projection["projection"]["projected_eigenvalues"]
lambda_gap = projection["second_order_bookkeeping_proxy"]["lambda_gap"]
trace_over_gap = projection["second_order_bookkeeping_proxy"]["trace_over_gap"]
trace_over_gap_squared = projection["second_order_bookkeeping_proxy"]["trace_over_gap_squared"]
proxy_trace = proxy["scale_comparison"]["coexact_trace_proxy_n1_to_n3"]
rank10 = 10.0
rank10_over_24 = rank10 / 24.0
n_need_gap = 0.0099700224

results = {
    "status": "explicit_n3_obstruction_scale_large_not_small_scheme_gap",
    "inputs": [
        "s2t_c6_l21_n3_explicit_projection_results.json",
        "s2t_c6_l21_n3_proxy_obstruction_scale_results.json",
        "s2t_c6_l21_full_operator_rescue_gate_results.json",
    ],
    "scale_data": {
        "projected_trace": trace,
        "projected_rank": rank,
        "projected_eigenvalues": eigs,
        "lambda_gap": lambda_gap,
        "trace_over_gap": trace_over_gap,
        "trace_over_gap_squared": trace_over_gap_squared,
        "rank10_count": rank10,
        "rank10_over_24_scale": rank10_over_24,
        "N_need_minus_10_gap": n_need_gap,
    },
    "comparisons": {
        "trace_to_rank10_ratio": trace / rank10,
        "trace_to_proxy64_ratio": trace / proxy_trace,
        "trace_over_gap_squared_to_rank10_over24_ratio": trace_over_gap_squared / rank10_over_24,
        "trace_over_gap_squared_to_Nneed_gap_ratio": trace_over_gap_squared / n_need_gap,
        "trace_over_gap_to_rank10_ratio": trace_over_gap / rank10,
    },
    "interpretation": [
        {
            "claim": "the explicit n=3 projection is a tiny correction comparable to N_need-10",
            "verdict": "fails_at_bookkeeping_scale",
            "reason": "Even the conservative trace/gap^2 proxy is about 0.5556, roughly 55.7 times the N_need-10 gap.",
        },
        {
            "claim": "the explicit n=3 projection is smaller than the earlier proxy and therefore harmless",
            "verdict": "fails",
            "reason": "The explicit trace is 80, larger than the earlier Hodge proxy trace 64 by a factor 1.25 in this modeled slice.",
        },
        {
            "claim": "the scale audit alone proves final C6 failure",
            "verdict": "not_yet",
            "reason": "The full one-form operator may still cancel or absorb the low-shell block; this audit only rules out treating it as a small gap-sized correction.",
        },
    ],
    "plain_language": (
        "The third-floor signal is not a tiny scratch. Even with a conservative denominator-squared bookkeeping proxy, it is much bigger than the small N_need-10 gap. "
        "So C6 needs a real cancellation, not a rounding explanation."
    ),
    "verdict": (
        "The explicit n=3 projected obstruction is large in the current low-shell bookkeeping. Its trace is 80, eight times the rank-10 count and 1.25 times the earlier proxy trace 64. "
        "The trace/(lambda3-lambda1)^2 proxy is about 0.5556, far larger than the N_need-10 gap. Therefore the nonzero n=3 block cannot be dismissed as a small scheme residue; only full-operator cancellation or a derived no-fit absorption identity can rescue C6."
    ),
}

Path("s2t_c6_l21_n3_obstruction_scale_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "trace_to_rank10_ratio": results["comparisons"]["trace_to_rank10_ratio"],
    "trace_over_gap_squared": trace_over_gap_squared,
    "gap_ratio": results["comparisons"]["trace_over_gap_squared_to_Nneed_gap_ratio"],
}, indent=2, ensure_ascii=False))