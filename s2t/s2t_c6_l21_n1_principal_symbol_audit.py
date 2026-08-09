import json
from pathlib import Path

import numpy as np

source = json.loads(Path("s2t_c6_l21_n1_killing_overlap_results.json").read_text())
M = np.array(source["normalized_overlap_matrices"]["traceless_diag_1_minus_1"], dtype=float)
M = (M + M.T) / 2.0

LAMBDA_1 = 4
# Convention used in Tome II: Delta_1 alpha = -nabla^2 alpha + Ric(alpha).
# On the unit S3 Killing shell, Delta_1 alpha = 4 alpha and Ric(alpha)=2 alpha,
# hence nabla^2 alpha = -2 alpha.  For h=2qg, delta g^{ab}=-2q g^{ab};
# the principal-symbol piece of delta(-g^{ab} nabla_a nabla_b) is
# -delta g^{ab} nabla_a nabla_b = 2q nabla^2 = -4 q on this shell.
PRINCIPAL_FACTOR = -4.0
principal_matrix = PRINCIPAL_FACTOR * M
principal_trace_square = float(np.trace(principal_matrix @ principal_matrix)) / (LAMBDA_1 ** 2)
toy_trace_square = float(np.trace(M @ M)) / (LAMBDA_1 ** 2)

results = {
    "status": "n1_principal_symbol_piece_nonzero_requires_cancellation",
    "source_overlap": "s2t_c6_l21_n1_killing_overlap_results.json",
    "conventions": {
        "laplacian": "Delta_1 alpha = -nabla^2 alpha + Ric(alpha)",
        "unit_s3_killing_shell": "Delta_1 alpha=4 alpha, Ric(alpha)=2 alpha, so nabla^2 alpha=-2 alpha",
        "conformal_slice": "h=2qg, delta g^{ab}=-2qg^{ab}",
        "principal_piece_on_killing_shell": "delta(-g^{ab}nabla_a nabla_b)=2q nabla^2=-4q",
    },
    "principal_factor_relative_to_q_overlap": PRINCIPAL_FACTOR,
    "overlap_trace_square": toy_trace_square,
    "principal_trace_square": principal_trace_square,
    "principal_matrix_eigenvalues": [float(x) for x in np.linalg.eigvalsh(principal_matrix)],
    "cancellation_requirement": {
        "needed_for_zero_full_n1_block": "connection + Ricci + projection + Hilbert-metric terms must cancel the principal-symbol matrix, not merely its trace.",
        "needed_for_absorption_route": "the sum of all terms must match the predetermined pi^-4/P02 finite residue without a tunable coefficient.",
        "warning": "principal piece alone is 16 times the q-overlap toy trace-square because the matrix is multiplied by -4 before squaring.",
    },
    "interpretation": [
        {
            "claim": "principal symbol is harmless on Killing n=1 shell",
            "verdict": "fails",
            "reason": "It is proportional to the already nonzero q-overlap matrix with factor -4 in the conformal slice.",
        },
        {
            "claim": "principal piece alone proves C6 fails",
            "verdict": "not_yet",
            "reason": "Other mandatory terms can cancel it; the audit quantifies the cancellation burden only.",
        },
    ],
    "verdict": (
        "In the reduced conformal slice h=2qg, the principal-symbol part of delta Delta_1 on the n=1 Killing shell is -4 times the nonzero q-overlap matrix. "
        "Its weighted trace-square is therefore 1/9, not zero. This is not the full operator, but it shows that any C6 rescue must produce a concrete cancellation from connection, Ricci, projection, and Hilbert-metric terms."
    ),
}

Path("s2t_c6_l21_n1_principal_symbol_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "principal_factor": PRINCIPAL_FACTOR,
    "overlap_trace_square": toy_trace_square,
    "principal_trace_square": principal_trace_square,
    "eigenvalues": results["principal_matrix_eigenvalues"],
}, indent=2, ensure_ascii=False))