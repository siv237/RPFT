import json
from pathlib import Path

connection = json.loads(Path("s2t_c6_l21_connection_variation_formula_results.json").read_text())
projection = json.loads(Path("s2t_c6_l21_n3_explicit_projection_results.json").read_text())

projected_trace = projection["projection"]["projected_gram_trace"]
projected_rank = projection["projection"]["projected_rank_numeric"]

results = {
    "status": "ricci_variation_formula_fixed_matrix_evaluation_missing",
    "inputs": [
        "s2t_c6_l21_connection_variation_formula_results.json",
        "s2t_c6_l21_n3_explicit_projection_results.json",
    ],
    "geometric_setup": {
        "slice": "conformal first-strain test h_ab = 2 q_A g_ab on unit S3/RP3",
        "dimension": 3,
        "background_Ricci": "Ric_ab = 2 g_ab on the unit constant-curvature background",
        "q_A": "traceless harmonic quadratic test direction, with scalar positive Laplacian eigenvalue 8 under the Tome II convention",
    },
    "ricci_variation_formula": {
        "covariant_Ricci_variation": "delta Ric_ab = - nabla_a nabla_b q - g_ab nabla^2 q in dimension 3 for h=2qg, using geometric nabla^2 sign",
        "mixed_Ricci_operator_variation": "delta(Ric_a^b alpha_b) = (delta Ric_a^b) alpha_b + (delta g^{bc}) Ric_ac alpha_b",
        "index_raising_piece_on_unit_S3": "(delta g^{bc}) Ric_ac alpha_b = -4 q alpha_a",
        "positive_laplacian_translation": "if Delta_0 = -nabla^2 and q is ell=2, then nabla^2 q = -8 q; signs must be kept in the same convention as Delta_1 = -nabla^2 + Ric",
        "warning": "This fixes the tensor formula only. It is not yet the evaluated C_Ric[1,3] matrix block.",
    },
    "required_matrix_output": {
        "matrix_name": "C_Ric[1,3]",
        "domain_basis": "six quotient-normalized n=1 Killing one-forms",
        "target_basis": "30-dimensional quotient-normalized n=3 coexact basis",
        "must_report": [
            "6x30 matrix or equivalent 6x6 Gram contribution after projection",
            "sign convention used for nabla^2 versus positive Delta_0",
            "projected trace/rank after adding principal + connection + Ricci blocks",
        ],
    },
    "current_obstruction_context": {
        "projected_trace_before_Ricci": projected_trace,
        "projected_rank_before_Ricci": projected_rank,
        "connection_formula_status": connection["status"],
        "meaning": "Ricci is the second full-operator block; it can only rescue C6 after matrix evaluation and combination with the other blocks.",
    },
    "pass_fail": [
        {
            "test": "formula_written",
            "status": "pass",
            "meaning": "delta Ric and index-raising pieces are fixed at formula level for the conformal strain slice.",
        },
        {
            "test": "matrix_evaluated",
            "status": "not_yet",
            "meaning": "C_Ric[1,3] still must be integrated against the explicit n=3 basis.",
        },
        {
            "test": "combined_cancellation_shown",
            "status": "not_yet",
            "meaning": "No cancellation of trace 80 can be claimed before principal, connection, Ricci, projector, Hilbert, and delta2 terms are combined.",
        },
    ],
    "plain_language": (
        "The second extinguisher now has a label and formula. Ricci curvature cannot be ignored on RP3, but it has not yet been aimed at the trace-80 fire because C_Ric[1,3] is still uncomputed."
    ),
    "verdict": (
        "The Ricci/curvature variation is now fixed at formula level for the conformal first-strain slice. In dimension 3, delta Ric_ab = -nabla_a nabla_b q - g_ab nabla^2 q, with the mixed Ricci operator also receiving the index-raising piece -4q alpha_a on the unit background. "
        "This advances the full-operator checklist but does not close C6; the required next output is the quotient-normalized n=1<->n=3 Ricci matrix block and its interference with the existing trace-80 obstruction."
    ),
}

Path("s2t_c6_l21_ricci_variation_formula_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "formula_written": True,
    "matrix_evaluated": False,
    "projected_trace_before_Ricci": projected_trace,
}, indent=2, ensure_ascii=False))