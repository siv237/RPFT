import json
from pathlib import Path

proxy = json.loads(Path("s2t_c6_l21_n3_proxy_obstruction_scale_results.json").read_text())
hodge = json.loads(Path("s2t_c6_l21_n3_hodge_projection_results.json").read_text())
low_shell = json.loads(Path("s2t_c6_l21_low_shell_block_spec_results.json").read_text())

D3 = 30
IMAGE_DIM = 6
COEXACT_PROXY_TRACE = hodge["trace_bookkeeping"]["coexact_trace_proxy"]
SECOND_ORDER_PROXY = hodge["second_order_proxy"]["coexact_trace_over_denominator_squared"]
RATIO_TO_RANK10 = proxy["scale_comparison"]["ratio_coexact_trace_to_rank10"]

basis_requirements = [
    {
        "requirement": "construct_n3_coexact_space",
        "needed": "an explicit 30-dimensional orthonormal coexact one-form basis on L(2,1), inherited from even RP3-compatible S3 vector harmonics",
        "why": "the proxy trace 64 must be tested against the real spectral Hilbert basis, not only against trace-level Hodge bookkeeping",
    },
    {
        "requirement": "project_six_images",
        "needed": "project the six Hodge-filtered images from the n=1 Killing basis into the n=3 coexact basis",
        "why": "the leakage image dimension is at most 6, but it lives inside a 30-dimensional shell",
    },
    {
        "requirement": "normalize_on_L21",
        "needed": "use quotient-normalized L(2,1) inner products, not raw S3 norms",
        "why": "earlier normalization audit showed cover factors cancel only after orthonormalization is done consistently",
    },
    {
        "requirement": "assemble_second_order_trace",
        "needed": "insert the denominator lambda_3-lambda_1=12 and determinant sign convention",
        "why": "a Gram trace is not yet the determinant contribution",
    },
]

pass_fail = [
    {
        "outcome": "explicit_trace_zero",
        "meaning": "the proxy was an artifact of incomplete projection; C6 diagonal rescue may extend to 1<->3",
        "effect_on_C6": "route_reopened",
    },
    {
        "outcome": "explicit_trace_equals_64_or_nonzero_same_scale",
        "meaning": "the proxy is confirmed as a real low-shell coexact residue",
        "effect_on_C6": "rank10_absorption_blocked_without_new_cancellation",
    },
    {
        "outcome": "explicit_trace_nonzero_but_absorbed_by_existing_pi4_residue",
        "meaning": "possible rescue only if the absorption identity is derived with no fitted coefficient",
        "effect_on_C6": "conditional_rescue",
    },
]

results = {
    "status": "explicit_n3_coexact_basis_is_now_the_blocking_gate",
    "sources": [
        "s2t_c6_l21_n3_hodge_projection_results.json",
        "s2t_c6_l21_n3_proxy_obstruction_scale_results.json",
        "s2t_c6_l21_low_shell_block_spec_results.json",
    ],
    "known_numbers": {
        "n3_coexact_degeneracy": D3,
        "leakage_image_dimension_bound": IMAGE_DIM,
        "coexact_trace_proxy": COEXACT_PROXY_TRACE,
        "second_order_proxy": SECOND_ORDER_PROXY,
        "ratio_to_rank10_route": RATIO_TO_RANK10,
    },
    "basis_requirements": basis_requirements,
    "pass_fail_outcomes": pass_fail,
    "forbidden_shortcuts": [
        "Do not claim C6 failure from proxy trace alone.",
        "Do not claim rank-10 rescue without projecting onto the 30-dimensional n=3 coexact shell.",
        "Do not hide a nonzero explicit trace in a finite counterterm chosen after seeing the alpha target.",
    ],
    "verdict": (
        "The C6 calculation has reached a hard gate: explicit n=3 coexact basis projection. "
        "The proxy residue 64 is too large to ignore, but it is not a theorem until the six leaked images are projected into the 30-dimensional quotient-normalized n=3 coexact shell. "
        "This gate decides whether C6 remains a possible rank-10 absorption theorem or must be downgraded without a new cancellation/paired sector."
    ),
}

Path("s2t_c6_l21_n3_explicit_basis_gate_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "n3_degeneracy": D3,
    "image_dim_bound": IMAGE_DIM,
    "coexact_trace_proxy": COEXACT_PROXY_TRACE,
    "ratio_to_rank10": RATIO_TO_RANK10,
}, indent=2, ensure_ascii=False))