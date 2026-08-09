import json
import math
from pathlib import Path

import numpy as np

VOL_S3 = 2 * math.pi ** 2
VOL_L21 = math.pi ** 2


def antisym_basis_4():
    basis = []
    labels = []
    for a in range(4):
        for b in range(a + 1, 4):
            m = np.zeros((4, 4), dtype=float)
            m[a, b] = 1.0
            m[b, a] = -1.0
            basis.append(m)
            labels.append(f"E{a}{b}")
    return labels, basis


def sphere_moment_q_b(a_sym, b_mat):
    """Integral over L(2,1) of (x^T A x)(x^T B x) for unit S3 quotient.

    For uniform S3, E[x_i x_j x_k x_l] = (delta_ij delta_kl + delta_ik delta_jl + delta_il delta_jk)/24.
    Since q_A and x^T B x are even, quotient integral over L(2,1) is half of S3 integral,
    equivalently Vol(L21) times the S3 expectation.
    """
    tr_a = float(np.trace(a_sym))
    tr_b = float(np.trace(b_mat))
    return VOL_L21 * (tr_a * tr_b + float(np.trace(a_sym @ b_mat)) + float(np.trace(a_sym @ b_mat.T))) / 24.0


labels, basis = antisym_basis_4()
# A traceless P02 deformation. q_A = x0^2 - x1^2.
A_trace = np.eye(4)
A_traceless = np.diag([1.0, -1.0, 0.0, 0.0])

matrices = {}
for name, A in [("trace_direction", A_trace), ("traceless_diag_1_minus_1", A_traceless)]:
    mat = np.zeros((6, 6), dtype=float)
    for i, M in enumerate(basis):
        for j, N in enumerate(basis):
            # Killing 1-form pointwise pairing is <Mx,Nx> = x^T M^T N x.
            B = M.T @ N
            mat[i, j] = sphere_moment_q_b(A, B)
    matrices[name] = mat

# Normalize by the n=1 quotient norm of these Killing forms.
# Integral_L21 |Mx|^2 = Vol(L21) * E[x^T M^T M x] = Vol(L21)*Tr(M^T M)/4 = pi^2/2 for this basis.
norm_sq = VOL_L21 * float(np.trace(basis[0].T @ basis[0])) / 4.0
normalized = {name: mat / norm_sq for name, mat in matrices.items()}

def matrix_summary(mat):
    return {
        "rank_numeric": int(np.linalg.matrix_rank(mat, tol=1e-12)),
        "frobenius_norm": float(np.linalg.norm(mat)),
        "max_abs_entry": float(np.max(np.abs(mat))),
        "nonzero_entries_gt_1e-12": int(np.sum(np.abs(mat) > 1e-12)),
        "eigenvalues": [float(x) for x in np.linalg.eigvalsh((mat + mat.T) / 2.0)],
    }

summaries = {name: matrix_summary(mat) for name, mat in normalized.items()}

results = {
    "status": "n1_killing_overlap_not_symmetry_zero_for_p02_conformal_pairing",
    "basis_labels": labels,
    "geometric_identification": {
        "n1_shell": "six Killing one-forms from antisymmetric 4x4 generators on S3",
        "degeneracy": 6,
        "lambda": 4,
        "descends_to_L21": True,
        "note": "This checks a necessary overlap in the reduced conformal q_A pairing, not the full delta_A Delta_1 operator.",
    },
    "normalization": {
        "raw_basis_norm_sq_on_L21": norm_sq,
        "normalized_basis_rule": "divide overlap matrix by raw_basis_norm_sq_on_L21 for this basis",
    },
    "tested_deformations": {
        "trace_direction": "A=I, q_A=1",
        "traceless_diag_1_minus_1": "A=diag(1,-1,0,0), q_A=x0^2-x1^2",
    },
    "normalized_overlap_summaries": summaries,
    "normalized_overlap_matrices": {name: mat.tolist() for name, mat in normalized.items()},
    "interpretation": [
        {
            "claim": "n=1 diagonal block vanishes by parity or representation symmetry",
            "verdict": "fails_for_qA_pairing",
            "reason": "The traceless P02 deformation has a nonzero normalized overlap matrix on the six Killing one-forms.",
        },
        {
            "claim": "this proves full C6 low-shell obstruction",
            "verdict": "not_yet",
            "reason": "The full one-form Laplacian variation includes principal, connection, Ricci, projection, and inner-product terms that may cancel this pairing.",
        },
        {
            "claim": "next calculation can ignore n=1 diagonal channel",
            "verdict": "forbidden",
            "reason": "There is no symmetry-zero at the basic P02/Killing overlap level; explicit coefficient cancellation must be shown if the full block vanishes.",
        },
    ],
    "verdict": (
        "The first coexact shell is concretely the six Killing one-forms. A traceless P02 quadratic deformation has nonzero diagonal overlap on this shell in the conformal q_A pairing. "
        "Therefore the n=1->1 low-shell channel cannot be dismissed by parity or representation symmetry alone. C6 now needs an explicit full-operator cancellation or absorption calculation for this block."
    ),
}

Path("s2t_c6_l21_n1_killing_overlap_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "basis_labels": labels,
    "norm_sq": norm_sq,
    "traceless_summary": summaries["traceless_diag_1_minus_1"],
}, indent=2, ensure_ascii=False))