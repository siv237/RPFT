import json
from pathlib import Path

hodge = json.loads(Path("s2t_c6_l21_n3_hodge_projection_results.json").read_text())
principal = json.loads(Path("s2t_c6_l21_n1_principal_symbol_results.json").read_text())

coexact_trace = hodge["trace_bookkeeping"]["coexact_trace_proxy"]
second_proxy = hodge["second_order_proxy"]["coexact_trace_over_denominator_squared"]
principal_trace_square = principal["principal_trace_square"]

# Known internal rank-10 compression scale from earlier C6 path: P02 rank 10 enters as the desired finite rank,
# while this n=1<->3 proxy is an additional low-shell off-diagonal trace candidate.
RANK_P02 = 10
ratio_to_rank10 = coexact_trace / RANK_P02
ratio_to_principal_warning = coexact_trace / principal_trace_square
ratio_second_to_principal = second_proxy / principal_trace_square

results = {
    "status": "n3_proxy_obstruction_scale_large_relative_to_rank10_route",
    "sources": [
        "s2t_c6_l21_n3_hodge_projection_results.json",
        "s2t_c6_l21_n1_principal_symbol_results.json",
    ],
    "scale_comparison": {
        "coexact_trace_proxy_n1_to_n3": coexact_trace,
        "second_order_denominator_proxy": second_proxy,
        "p02_rank_target": RANK_P02,
        "ratio_coexact_trace_to_rank10": ratio_to_rank10,
        "n1_principal_warning_trace_square": principal_trace_square,
        "ratio_coexact_trace_to_n1_principal_warning": ratio_to_principal_warning,
        "ratio_second_order_proxy_to_n1_principal_warning": ratio_second_to_principal,
    },
    "interpretation": [
        {
            "claim": "the n=1<->3 proxy can be ignored as a tiny leakage",
            "verdict": "fails",
            "reason": "The coexact trace proxy is 64, which is 6.4 times the rank-10 P02 count and much larger than the n=1 principal warning trace-square.",
        },
        {
            "claim": "the proxy alone proves final C6 failure",
            "verdict": "not_yet",
            "reason": "The explicit orthonormal n=3 coexact projection and determinant sign/normalization are still missing; this is a scale warning, not the final theorem.",
        },
    ],
    "next_required_audit": {
        "name": "explicit_n3_coexact_basis_or_no_go_downgrade",
        "task": "confirm whether the trace-level residue 64 survives in an explicit coexact n=3 basis",
        "pass_for_rescue": "show exact cancellation with projection/Hilbert terms or absorption into the existing pi^-4/P02 residue without a tunable coefficient",
        "fail_for_rescue": "nonzero explicit residue remains as an independent low-shell finite determinant contribution",
    },
    "verdict": (
        "The proxy residue is not small in the internal C6 bookkeeping. A coexact trace proxy of 64 is 6.4 times the rank-10 P02 route and gives a second-order denominator proxy 4/9. "
        "Therefore, if explicit n=3 projection confirms it, C6 cannot remain a clean rank-10 absorption theorem without a new cancellation or paired sector."
    ),
}

Path("s2t_c6_l21_n3_proxy_obstruction_scale_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "coexact_trace_proxy": coexact_trace,
    "second_order_proxy": second_proxy,
    "ratio_to_rank10": ratio_to_rank10,
}, indent=2, ensure_ascii=False))