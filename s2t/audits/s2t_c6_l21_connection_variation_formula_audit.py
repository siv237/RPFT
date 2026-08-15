import json
from pathlib import Path

checklist = json.loads(Path("s2t_c6_l21_full_operator_checklist_results.json").read_text())
projection = json.loads(Path("s2t_c6_l21_n3_explicit_projection_results.json").read_text())

projected_trace = projection["projection"]["projected_gram_trace"]
projected_rank = projection["projection"]["projected_rank_numeric"]

results = {
    "status": "connection_variation_formula_fixed_matrix_evaluation_missing",
    "inputs": [
        "s2t_c6_l21_full_operator_checklist_results.json",
        "s2t_c6_l21_n3_explicit_projection_results.json",
    ],
    "geometric_setup": {
        "slice": "conformal first-strain test h_ab = 2 q_A g_ab on unit S3/RP3",
        "q_A": "x^T A x with A in Sym^2_0(R4) for the traceless P02 test direction",
        "background": "constant-curvature unit S3 descended to L(2,1)",
        "purpose": "fix the first missing full-operator term before evaluating n=1<->n=3 matrix elements",
    },
    "connection_variation_formula": {
        "delta_Gamma": "delta Gamma^k_{ij} = delta^k_j nabla_i q + delta^k_i nabla_j q - g_ij nabla^k q",
        "source": "standard Levi-Civita variation for h_ij = 2 q g_ij",
        "acts_on_one_form_derivative": "delta(nabla_i alpha_j) = - delta Gamma^k_{ij} alpha_k",
        "laplacian_connection_slots": [
            "variation of both covariant derivatives in -g^{ij} nabla_i nabla_j alpha_c",
            "derivative of delta Gamma terms: nabla(delta Gamma) * alpha",
            "delta Gamma times nabla alpha terms",
        ],
        "warning": "This fixes the tensor formula only. It is not yet the evaluated C_conn[1,3] matrix block.",
    },
    "required_matrix_output": {
        "matrix_name": "C_conn[1,3]",
        "domain_basis": "six quotient-normalized n=1 Killing one-forms",
        "target_basis": "30-dimensional quotient-normalized n=3 coexact basis",
        "must_report": [
            "6x30 matrix or equivalent 6x6 Gram contribution after projection",
            "projected trace and rank after adding to the existing conformal/principal-slice contribution",
            "whether the connection block cancels, enlarges, or rotates the trace-80 image",
        ],
    },
    "current_obstruction_context": {
        "projected_trace_before_connection": projected_trace,
        "projected_rank_before_connection": projected_rank,
        "meaning": "The connection block must act on a large, already quotient-valid low-shell obstruction, not a tiny scheme-gap term.",
    },
    "pass_fail": [
        {
            "test": "formula_written",
            "status": "pass",
            "meaning": "delta Gamma is now fixed for the conformal strain slice.",
        },
        {
            "test": "matrix_evaluated",
            "status": "not_yet",
            "meaning": "C_conn[1,3] still must be integrated against the explicit n=3 basis.",
        },
        {
            "test": "cancellation_shown",
            "status": "not_yet",
            "meaning": "No cancellation of trace 80 can be claimed before the matrix block is evaluated and combined with Ricci/projector/Hilbert/delta2 terms.",
        },
    ],
    "plain_language": (
        "We have picked up the first extinguisher and written its nozzle shape. The connection formula is fixed, but it has not yet sprayed the third-floor fire: the C_conn matrix still has to be computed."
    ),
    "verdict": (
        "The connection-variation term is now fixed at formula level for the conformal first-strain slice: delta Gamma^k_ij = delta^k_j nabla_i q + delta^k_i nabla_j q - g_ij nabla^k q. "
        "This advances the full-operator checklist but does not close C6; the required next output is the quotient-normalized n=1<->n=3 connection matrix block and its interference with the trace-80 projection."
    ),
}

Path("s2t_c6_l21_connection_variation_formula_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "formula_written": True,
    "matrix_evaluated": False,
    "projected_trace_before_connection": projected_trace,
}, indent=2, ensure_ascii=False))