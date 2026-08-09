import json
from pathlib import Path

SUBBLOCK_FILES = [
    ("principal_second_symbol", "s2t_c6_l21_delta2_principal_second_symbol_formula_results.json"),
    ("second_connection", "s2t_c6_l21_delta2_second_connection_formula_results.json"),
    ("second_ricci_curvature", "s2t_c6_l21_delta2_second_ricci_formula_results.json"),
    ("second_coexact_projector", "s2t_c6_l21_delta2_second_projector_formula_results.json"),
    ("second_hilbert_basis", "s2t_c6_l21_delta2_second_hilbert_formula_results.json"),
    ("local_counterterm_classifier", "s2t_c6_l21_delta2_local_counterterm_classifier_results.json"),
]

decomp = json.loads(Path("s2t_c6_l21_delta2_operator_decomposition_results.json").read_text())
finite_spec = json.loads(Path("s2t_c6_l21_delta2_finite_block_spec_results.json").read_text())

subblocks = []
for name, filename in SUBBLOCK_FILES:
    payload = json.loads(Path(filename).read_text())
    status = payload["status"]
    subblocks.append({
        "block": name,
        "file": filename,
        "status": status,
        "skeleton_or_formula_present": (
            "skeleton_fixed" in status or "formula_fixed" in status
        ),
        "matrix_trace_done": "matrix_missing" not in status and "not_evaluated" not in json.dumps(payload),
        "verdict": payload.get("verdict", ""),
    })

results = {
    "status": "delta2_skeleton_phase_complete_trace_phase_open",
    "inputs": [
        "s2t_c6_l21_delta2_operator_decomposition_results.json",
        "s2t_c6_l21_delta2_finite_block_spec_results.json",
        *[filename for _, filename in SUBBLOCK_FILES],
    ],
    "subblock_summary": subblocks,
    "completion_flags": {
        "six_subblocks_named": len(subblocks) == 6,
        "all_skeletons_or_formulas_present": all(row["skeleton_or_formula_present"] for row in subblocks),
        "full_delta2_operator_formula_complete": False,
        "diagonal_C_delta2_traces_evaluated": False,
        "locality_or_same_scheme_compensation_proven": False,
        "C6_status_upgrade_allowed": False,
    },
    "trace_phase_work_order": [
        "expand delta2 Gamma_AB on the fixed ambient path",
        "expand delta2 Ricci_AB and mixed-index curvature terms",
        "expand delta2 Pi_coex and verify reduced self-adjointness",
        "choose Hilbert basis transport and compute second Gram correction",
        "prove local heat-kernel-only status or same-scheme compensation, otherwise compute finite residuals",
        "assemble diagonal C_delta2[1,1] and C_delta2[3,3] over 55 symmetric deformation pairs",
    ],
    "finite_block_counts": finite_spec["counts"],
    "plain_language": "The map of the six rooms is complete. The doors are labelled, but no one has walked through the rooms with a measuring tape yet.",
    "verdict": "The delta2 Delta_1,coex skeleton phase is complete: principal second-symbol, second connection, second Ricci/curvature, second coexact-projector, second Hilbert/basis, and local-counterterm classifier blocks are all named and scoped. This is not a determinant closure. The full formulas, self-adjoint reduced representation, local/compensation proof, and diagonal C_delta2 trace tables remain open before C6 can be upgraded.",
}

Path("s2t_c6_l21_delta2_skeleton_completion_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "six_subblocks_named": results["completion_flags"]["six_subblocks_named"],
    "all_skeletons_or_formulas_present": results["completion_flags"]["all_skeletons_or_formulas_present"],
    "diagonal_C_delta2_traces_evaluated": results["completion_flags"]["diagonal_C_delta2_traces_evaluated"],
    "C6_status_upgrade_allowed": results["completion_flags"]["C6_status_upgrade_allowed"],
}, indent=2, ensure_ascii=False))