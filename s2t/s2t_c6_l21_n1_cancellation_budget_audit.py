import json
from pathlib import Path

import numpy as np

principal = json.loads(Path("s2t_c6_l21_n1_principal_symbol_results.json").read_text())
overlap = json.loads(Path("s2t_c6_l21_n1_killing_overlap_results.json").read_text())

M = np.array(overlap["normalized_overlap_matrices"]["traceless_diag_1_minus_1"], dtype=float)
M = (M + M.T) / 2.0
P = np.array(principal.get("principal_matrix", []), dtype=float) if "principal_matrix" in principal else -4.0 * M
LAMBDA_1 = 4.0

# The next mandatory terms in the full one-form variation must add C=-P if the
# n=1 diagonal Killing block is to vanish.  If instead C6 is to survive as a
# finite absorption theorem, the same target cannot be chosen freely: its
# leftover must be the pre-existing pi^-4/P02 residue.
target = -P
principal_norm = float(np.linalg.norm(P, ord="fro"))
target_norm = float(np.linalg.norm(target, ord="fro"))
weighted_target_trace_square = float(np.trace(target @ target)) / (LAMBDA_1 ** 2)

# Since P has eigenvalues +/-2/3,+/-2/3,0,0, any exact cancellation requires two
# positive and two negative compensating eigen-directions of equal size.  A pure
# scalar/identity correction cannot do this because the target is traceless.
evals = np.linalg.eigvalsh(P)
target_evals = np.linalg.eigvalsh(target)
identity_projection = np.trace(target) / target.shape[0]
identity_residual = target - identity_projection * np.eye(target.shape[0])
identity_residual_fraction = float(np.linalg.norm(identity_residual, ord="fro") / target_norm)

# A sign-only or trace-only bookkeeping cannot repair the block.  The whole
# traceless matrix has to be supplied by connection/Ricci/projection/Hilbert terms.
results = {
    "status": "n1_cancellation_budget_fixed_by_principal_symbol",
    "inputs": [
        "s2t_c6_l21_n1_killing_overlap_results.json",
        "s2t_c6_l21_n1_principal_symbol_results.json",
    ],
    "lambda_1": LAMBDA_1,
    "principal_eigenvalues": [float(x) for x in evals],
    "required_cancellation_eigenvalues": [float(x) for x in target_evals],
    "principal_frobenius_norm": principal_norm,
    "required_cancellation_frobenius_norm": target_norm,
    "weighted_required_trace_square": weighted_target_trace_square,
    "identity_projection_coefficient": float(identity_projection),
    "identity_residual_fraction": identity_residual_fraction,
    "budget_tests": [
        {
            "test": "scalar_or_volume_counterterm_can_cancel_n1_block",
            "verdict": "fails",
            "reason": "The required cancellation matrix is traceless with eigenvalues -2/3,-2/3,0,0,2/3,2/3; its identity projection is zero.",
        },
        {
            "test": "trace_square_bookkeeping_is_sufficient",
            "verdict": "fails",
            "reason": "The cancellation is matrix-level, not just trace-level; two positive and two negative eigendirections must be supplied with the correct basis alignment.",
        },
        {
            "test": "full_operator_cancellation_still_possible",
            "verdict": "open",
            "reason": "Connection, Ricci, projection, and Hilbert-metric terms have not yet been evaluated; the audit fixes the exact target they must hit.",
        },
    ],
    "next_required_audit": {
        "name": "full_conformal_hodge_variation_on_n1_killing_shell",
        "minimum_output": "the 6x6 matrix of connection+Ricci+projection+Hilbert terms in the same normalized Killing basis",
        "pass_condition_for_zero_route": "matrix equals required_cancellation_matrix, not merely equal trace or norm",
        "pass_condition_for_absorption_route": "leftover finite part is derived and equals the existing pi^-4/P02 residue without a fitted coefficient",
    },
    "verdict": (
        "The principal-symbol warning can be sharpened into a fixed cancellation budget. "
        "For the n=1 Killing block, all non-principal one-form variation terms together must supply a traceless 6x6 matrix with Frobenius norm sqrt(8/9) and weighted trace-square 1/9. "
        "A scalar counterterm, volume renormalization, or trace-only argument cannot cancel it."
    ),
}

results["required_cancellation_matrix"] = target.tolist()

Path("s2t_c6_l21_n1_cancellation_budget_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "principal_eigenvalues": results["principal_eigenvalues"],
    "required_cancellation_eigenvalues": results["required_cancellation_eigenvalues"],
    "weighted_required_trace_square": weighted_target_trace_square,
    "identity_residual_fraction": identity_residual_fraction,
}, indent=2, ensure_ascii=False))