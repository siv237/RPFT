import json
from pathlib import Path

priority = json.loads(Path("s2t_c6_l21_delta2_trace_phase_priority_results.json").read_text())
finite_spec = json.loads(Path("s2t_c6_l21_delta2_finite_block_spec_results.json").read_text())
coexact_basis = json.loads(Path("s2t_c6_l21_coexact_basis_results.json").read_text())
normalization = json.loads(Path("s2t_c6_l21_normalization_results.json").read_text())
ambient = json.loads(Path("s2t_c6_l21_delta2_ambient_path_formula_results.json").read_text())

subblock_files = [
    "s2t_c6_l21_delta2_principal_second_symbol_formula_results.json",
    "s2t_c6_l21_delta2_second_connection_formula_results.json",
    "s2t_c6_l21_delta2_second_ricci_formula_results.json",
    "s2t_c6_l21_delta2_second_projector_formula_results.json",
    "s2t_c6_l21_delta2_second_hilbert_formula_results.json",
    "s2t_c6_l21_delta2_local_counterterm_classifier_results.json",
]
subblocks = [json.loads(Path(filename).read_text()) for filename in subblock_files]

n1_shell = next(row for row in coexact_basis["shell_table"] if row["n"] == 1)
c11_spec = next(row for row in finite_spec["direct_trace_blocks_required_first"] if row["block"] == "C_delta2[1,1]")

results = {
    "status": "delta2_C11_setup_fixed_inputs_ready_matrix_not_evaluated",
    "inputs": [
        "s2t_c6_l21_delta2_trace_phase_priority_results.json",
        "s2t_c6_l21_delta2_finite_block_spec_results.json",
        "s2t_c6_l21_coexact_basis_results.json",
        "s2t_c6_l21_normalization_results.json",
        "s2t_c6_l21_delta2_ambient_path_formula_results.json",
        *subblock_files,
    ],
    "target_block": {
        "name": "C_delta2[1,1]",
        "shell": "n=1 coexact Killing one-forms on L(2,1)",
        "degeneracy": n1_shell["l21_coexact_degeneracy"],
        "lambda": n1_shell["lambda_unit_radius"],
        "matrix_shape_per_symmetric_deformation_pair": c11_spec["matrix_shape_per_symmetric_deformation_pair"],
        "entries_per_pair": c11_spec["entries_per_symmetric_deformation_pair"],
        "trace_weight_lambda_inverse": c11_spec["trace_weight_lambda_inverse"],
        "deformation_pairs": finite_spec["counts"]["symmetric_deformation_pairs_A_B"],
        "raw_entries_all_pairs": c11_spec["entries_per_symmetric_deformation_pair"] * finite_spec["counts"]["symmetric_deformation_pairs_A_B"],
    },
    "locked_conventions": {
        "ambient_path": ambient["selected_path"],
        "metric_derivatives": ambient["metric_derivatives"],
        "normalization_status": normalization["status"],
        "normalization_rule": "quotient-orthonormal states; no extra global cover factor in trace",
        "basis_labels_expected": ["E01", "E02", "E03", "E12", "E13", "E23"],
    },
    "required_operator_pieces": [
        {
            "piece": "principal_second_symbol",
            "source": subblock_files[0],
            "status": subblocks[0]["status"],
            "C11_ready": "formula_fixed" in subblocks[0]["status"],
        },
        {
            "piece": "second_connection",
            "source": subblock_files[1],
            "status": subblocks[1]["status"],
            "C11_ready": False,
        },
        {
            "piece": "second_ricci_curvature",
            "source": subblock_files[2],
            "status": subblocks[2]["status"],
            "C11_ready": False,
        },
        {
            "piece": "second_coexact_projector",
            "source": subblock_files[3],
            "status": subblocks[3]["status"],
            "C11_ready": False,
        },
        {
            "piece": "second_hilbert_basis",
            "source": subblock_files[4],
            "status": subblocks[4]["status"],
            "C11_ready": False,
        },
        {
            "piece": "local_counterterm_classifier",
            "source": subblock_files[5],
            "status": subblocks[5]["status"],
            "C11_ready": False,
        },
    ],
    "assembly_formula_schematic": "C_delta2[1,1]_{ij}(A,B)=<e_i, (delta2_principal+delta2_connection+delta2_Ricci+delta2_projector+delta2_Hilbert/basis)_AB e_j> plus allowed same-scheme local bookkeeping, in quotient-orthonormal n=1 basis",
    "blocked_by": [
        "full delta2 Gamma_AB expansion missing",
        "full delta2 Ricci_AB expansion missing",
        "delta2 Pi_coex expansion and self-adjoint reduced representation missing",
        "Hilbert basis transport / second Gram correction missing",
        "local heat-kernel or same-scheme compensation proof missing",
    ],
    "pass_fail": [
        {
            "test": "target_block_identified",
            "status": "pass",
            "meaning": "C_delta2[1,1] is the first trace-phase block and has 36 entries per deformation pair.",
        },
        {
            "test": "basis_and_normalization_locked",
            "status": "pass",
            "meaning": "n=1 has six quotient-normalized coexact Killing states and no extra cover factor.",
        },
        {
            "test": "all_operator_pieces_matrix_ready",
            "status": "fail_open",
            "meaning": "Only the principal second-symbol has formula-level readiness; other pieces remain skeleton-level.",
        },
        {
            "test": "C11_values_evaluated",
            "status": "not_yet",
            "meaning": "No C_delta2[1,1] matrix entries or trace values have been computed.",
        },
    ],
    "plain_language": "The first box is on the table. We know its size, labels, weights, and ruler, but most tools needed to fill the numbers are still missing.",
    "verdict": "The C_delta2[1,1] setup is fixed: use the six quotient-normalized n=1 Killing one-forms, the locked ambient linear embedding path, and 55 symmetric deformation pairs, giving 1,980 raw entries before reductions. This is a setup gate, not a computation. The C11 matrix cannot be evaluated until second connection, Ricci, projector, Hilbert/basis, and local/compensation pieces are expanded in the same convention.",
}

Path("s2t_c6_l21_delta2_c11_setup_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "target": results["target_block"]["name"],
    "entries_per_pair": results["target_block"]["entries_per_pair"],
    "raw_entries_all_pairs": results["target_block"]["raw_entries_all_pairs"],
    "C11_values_evaluated": False,
}, indent=2, ensure_ascii=False))