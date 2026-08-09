import json
from pathlib import Path

gate = json.loads(Path("s2t_c6_l21_delta2_delta_gate_results.json").read_text())
projection = json.loads(Path("s2t_c6_l21_n3_explicit_projection_results.json").read_text())

shells = {
    "1": {"n": 1, "lambda": 4, "coexact_degeneracy_l21": 6},
    "3": {"n": 3, "lambda": 16, "coexact_degeneracy_l21": 30},
}

diagonal_trace_blocks = []
for key, shell in shells.items():
    dim = shell["coexact_degeneracy_l21"]
    diagonal_trace_blocks.append({
        "block": f"C_delta2[{key},{key}]",
        "matrix_shape_per_symmetric_deformation_pair": [dim, dim],
        "entries_per_symmetric_deformation_pair": dim * dim,
        "trace_weight_lambda_inverse": 1 / shell["lambda"],
        "why_included": "Tr(Delta^-1 delta^2 Delta) reads diagonal spectral-shell traces directly.",
    })

mixed_archive_blocks = [
    {
        "block": "C_delta2[1,3]",
        "matrix_shape_per_symmetric_deformation_pair": [6, 30],
        "entries_per_symmetric_deformation_pair": 180,
        "direct_trace_role": "not_directly_in_Tr_Delta_inverse_delta2_Delta",
        "why_archive": "Useful for self-adjointness and full reduced-operator bookkeeping, but it does not by itself enter the simple trace unless paired by another operator or projection convention.",
    },
    {
        "block": "C_delta2[3,1]",
        "matrix_shape_per_symmetric_deformation_pair": [30, 6],
        "entries_per_symmetric_deformation_pair": 180,
        "direct_trace_role": "not_directly_in_Tr_Delta_inverse_delta2_Delta",
        "why_archive": "Hermitian partner/archive block for consistency checks.",
    },
]

deformation_dimension = 10
symmetric_pairs = deformation_dimension * (deformation_dimension + 1) // 2
required_entries_per_pair = sum(block["entries_per_symmetric_deformation_pair"] for block in diagonal_trace_blocks)
archive_entries_per_pair = sum(block["entries_per_symmetric_deformation_pair"] for block in mixed_archive_blocks)

results = {
    "status": "delta2_finite_block_spec_fixed_diagonal_trace_first",
    "inputs": [
        "s2t_c6_l21_delta2_delta_gate_results.json",
        "s2t_c6_l21_n3_explicit_projection_results.json",
    ],
    "determinant_role": gate["determinant_identity"],
    "path_dependence_warning": {
        "issue": "delta^2 Delta is not defined by the tangent h alone; it depends on the chosen one-parameter metric/embedding path unless a covariant second-variation convention is fixed.",
        "required_convention": "Use the same ambient first-strain path and quotient normalization as the trace-square audits, or state a scheme-fixed geodesic/conformal path before looking at alpha.",
    },
    "direct_trace_blocks_required_first": diagonal_trace_blocks,
    "mixed_blocks_to_archive_not_primary_trace": mixed_archive_blocks,
    "counts": {
        "deformation_space_dimension": deformation_dimension,
        "symmetric_deformation_pairs_A_B": symmetric_pairs,
        "required_diagonal_entries_per_pair": required_entries_per_pair,
        "required_diagonal_entries_all_pairs": required_entries_per_pair * symmetric_pairs,
        "optional_archive_mixed_entries_per_pair": archive_entries_per_pair,
        "optional_archive_mixed_entries_all_pairs": archive_entries_per_pair * symmetric_pairs,
    },
    "current_obstruction_context": {
        "trace_square_projected_trace": projection["projection"]["projected_gram_trace"],
        "trace_square_projected_rank": projection["projection"]["projected_rank_numeric"],
        "meaning": "The trace-square obstruction is off-diagonal 1<->3; delta2 can compensate only through the full second-variation scalar coefficient after diagonal traces are included in the same scheme.",
    },
    "pass_fail": [
        {
            "outcome": "diagonal_delta2_traces_local_or_zero",
            "effect": "returns the burden to connection/Ricci/projector/Hilbert trace-square cancellation.",
        },
        {
            "outcome": "diagonal_delta2_traces_finite_and_cancel_trace_square_coefficient",
            "effect": "keeps C6 alive if the path and subtraction scheme are fixed before fitting.",
        },
        {
            "outcome": "diagonal_delta2_traces_finite_and_do_not_cancel",
            "effect": "C6 remains blocked as mature determinant theorem.",
        },
        {
            "outcome": "delta2_result_changes_with_unfixed_path_choice",
            "effect": "path-choice theorem becomes mandatory; no numerical status upgrade is allowed.",
        },
    ],
    "plain_language": "The fifth extinguisher does not spray across floors first; it changes the heat on each floor. Count the n=1 and n=3 diagonal heat first, then archive cross-floor pieces for consistency.",
    "verdict": "The finite C_delta2 task is now scoped more precisely. For Tr(Delta^-1 delta^2 Delta), the primary required data are diagonal shell traces C_delta2[1,1] and C_delta2[3,3] for the 55 symmetric deformation pairs, i.e. 36+900=936 entries per pair before trace reductions. Off-diagonal C_delta2[1,3] and C_delta2[3,1] should be archived for self-adjointness and reduced-operator consistency, but they are not the direct trace term. A fixed second-variation path is mandatory before any finite number can be used in C6.",
}

Path("s2t_c6_l21_delta2_finite_block_spec_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "symmetric_pairs": symmetric_pairs,
    "required_diagonal_entries_per_pair": required_entries_per_pair,
    "required_diagonal_entries_all_pairs": required_entries_per_pair * symmetric_pairs,
    "path_choice_fixed": False,
}, indent=2, ensure_ascii=False))