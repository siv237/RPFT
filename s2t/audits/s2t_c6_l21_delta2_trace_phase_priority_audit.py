import json
from pathlib import Path

completion = json.loads(Path("s2t_c6_l21_delta2_skeleton_completion_results.json").read_text())
finite_spec = json.loads(Path("s2t_c6_l21_delta2_finite_block_spec_results.json").read_text())
ambient = json.loads(Path("s2t_c6_l21_delta2_ambient_path_formula_results.json").read_text())

counts = finite_spec["counts"]
direct_blocks = finite_spec["direct_trace_blocks_required_first"]
archive_blocks = finite_spec["mixed_blocks_to_archive_not_primary_trace"]

results = {
    "status": "delta2_trace_phase_priority_fixed_diagonal_blocks_first",
    "inputs": [
        "s2t_c6_l21_delta2_skeleton_completion_results.json",
        "s2t_c6_l21_delta2_finite_block_spec_results.json",
        "s2t_c6_l21_delta2_ambient_path_formula_results.json",
    ],
    "phase_context": {
        "previous_phase": completion["status"],
        "selected_path": ambient["selected_path"]["path_id"],
        "metric_path_locked": True,
        "reason": "C_delta2 numbers are not allowed to choose the second-variation path after the fact.",
    },
    "priority_order": [
        {
            "rank": 1,
            "task": "assemble diagonal C_delta2[1,1] trace per symmetric deformation pair",
            "shell": "n=1 coexact",
            "dimension": direct_blocks[0]["matrix_shape_per_symmetric_deformation_pair"][0],
            "entries_per_pair": direct_blocks[0]["entries_per_symmetric_deformation_pair"],
            "trace_weight_lambda_inverse": direct_blocks[0]["trace_weight_lambda_inverse"],
            "why_first": "smallest diagonal block and direct contribution to Tr(Delta^-1 delta2 Delta)",
            "status": "not_evaluated",
        },
        {
            "rank": 2,
            "task": "assemble diagonal C_delta2[3,3] trace per symmetric deformation pair",
            "shell": "n=3 coexact",
            "dimension": direct_blocks[1]["matrix_shape_per_symmetric_deformation_pair"][0],
            "entries_per_pair": direct_blocks[1]["entries_per_symmetric_deformation_pair"],
            "trace_weight_lambda_inverse": direct_blocks[1]["trace_weight_lambda_inverse"],
            "why_second": "larger but still direct diagonal trace contribution; needed before judging finite residual size",
            "status": "not_evaluated",
        },
        {
            "rank": 3,
            "task": "archive C_delta2[1,3] and C_delta2[3,1] for self-adjointness and representation checks",
            "blocks": [row["block"] for row in archive_blocks],
            "entries_per_pair": counts["optional_archive_mixed_entries_per_pair"],
            "why_not_primary": "off-diagonal blocks do not enter the simple direct Tr(Delta^-1 delta2 Delta) without an additional pairing convention",
            "status": "archive_after_diagonal_priority",
        },
    ],
    "work_size": {
        "symmetric_deformation_pairs_A_B": counts["symmetric_deformation_pairs_A_B"],
        "diagonal_entries_per_pair": counts["required_diagonal_entries_per_pair"],
        "diagonal_entries_all_pairs": counts["required_diagonal_entries_all_pairs"],
        "optional_archive_mixed_entries_all_pairs": counts["optional_archive_mixed_entries_all_pairs"],
    },
    "guardrails": [
        "do not use mixed 1<->3 archive blocks as a substitute for direct diagonal C_delta2 traces",
        "do not compare with alpha until local/compensation and Hilbert/self-adjoint conventions are fixed",
        "do not introduce direction-dependent finite counterterms after seeing trace values",
        "report zero, cancellation, or nonzero residual per block without changing the locked ambient path",
    ],
    "completion_flags": {
        "trace_phase_started": True,
        "priority_order_fixed": True,
        "C_delta2_11_evaluated": False,
        "C_delta2_33_evaluated": False,
        "mixed_archive_evaluated": False,
        "C6_status_upgrade_allowed": False,
    },
    "plain_language": "The measuring order is fixed. First weigh the small diagonal box, then the big diagonal box; the side boxes are useful checks but not the main scale.",
    "verdict": "The delta2 trace phase now has a fixed priority order. Direct determinant trace work begins with diagonal C_delta2[1,1] and C_delta2[3,3] over 55 symmetric deformation pairs, totaling 51,480 required diagonal entries before reductions. Mixed C_delta2[1,3] and C_delta2[3,1] blocks are archived for self-adjointness and representation checks, but they are not a substitute for the direct Tr(Delta^-1 delta2 Delta) diagonal traces. No C6 status upgrade is allowed until these traces or a same-scheme locality/compensation proof are supplied.",
}

Path("s2t_c6_l21_delta2_trace_phase_priority_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "trace_phase_started": True,
    "priority_order_fixed": True,
    "diagonal_entries_all_pairs": counts["required_diagonal_entries_all_pairs"],
    "C6_status_upgrade_allowed": False,
}, indent=2, ensure_ascii=False))