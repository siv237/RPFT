import json
from pathlib import Path

import numpy as np

source = json.loads(Path("s2t_c6_l21_n3_intrinsic_divergence_results.json").read_text())
G_trace = source["tangent_gram_summary"]["trace"]
G_eigs = np.array(source["tangent_gram_summary"]["eigenvalues"], dtype=float)
D_trace = source["divergence_gram_summary"]["trace"]
D_eigs = np.array(source["divergence_gram_summary"]["eigenvalues"], dtype=float)

# The divergence of a cubic tangent vector field from the n=1->3 channel lands in
# the scalar ell=2 sector on S3/RP3.  With the positive scalar Laplacian convention
# used in Tome II, lambda_scalar(ell)=ell(ell+2), hence lambda_2=8.
# The exact/gradient norm removed by the Hodge projector is <div V, Delta_0^{-1} div V>.
SCALAR_ELL = 2
LAMBDA_SCALAR_2 = SCALAR_ELL * (SCALAR_ELL + 2)
exact_trace = D_trace / LAMBDA_SCALAR_2
coexact_trace = G_trace - exact_trace
exact_eigs_proxy = D_eigs / LAMBDA_SCALAR_2
coexact_eigs_proxy = G_eigs - exact_eigs_proxy

# For the second-order n=1<->3 determinant channel, the spectral denominator is
# lambda_3-lambda_1 = 16-4=12.  This is only a proxy until the full normalized
# basis projection and determinant sign convention are assembled.
LAMBDA_1 = 4
LAMBDA_3 = 16
second_order_denominator = (LAMBDA_3 - LAMBDA_1) ** 2
coexact_second_order_proxy = coexact_trace / second_order_denominator

results = {
    "status": "n3_hodge_projection_proxy_leaves_nonzero_coexact_residue",
    "source": "s2t_c6_l21_n3_intrinsic_divergence_results.json",
    "assumptions": {
        "divergence_scalar_shell": "ell=2 scalar sector",
        "scalar_laplacian_eigenvalue": LAMBDA_SCALAR_2,
        "hodge_exact_norm_formula": "||grad f||^2 = <div V, Delta_0^{-1} div V>",
        "warning": "This is a Hodge-projection proxy from Gram traces/eigenvalues, not yet an explicit orthonormal n=3 coexact basis calculation.",
    },
    "trace_bookkeeping": {
        "tangent_trace": G_trace,
        "divergence_trace": D_trace,
        "exact_trace_removed": exact_trace,
        "coexact_trace_proxy": coexact_trace,
        "coexact_fraction_of_tangent_trace": coexact_trace / G_trace if G_trace else None,
    },
    "eigenvalue_proxy": {
        "tangent_eigenvalues": [float(x) for x in G_eigs],
        "exact_removed_eigenvalues_proxy": [float(x) for x in exact_eigs_proxy],
        "coexact_eigenvalues_proxy": [float(x) for x in coexact_eigs_proxy],
        "min_coexact_proxy_eigenvalue": float(np.min(coexact_eigs_proxy)),
    },
    "second_order_proxy": {
        "lambda_1": LAMBDA_1,
        "lambda_3": LAMBDA_3,
        "denominator_squared": second_order_denominator,
        "coexact_trace_over_denominator_squared": coexact_second_order_proxy,
    },
    "interpretation": [
        {
            "claim": "the tangent n=3 signal is purely exact and disappears after Hodge projection",
            "verdict": "fails_in_proxy",
            "reason": "Subtracting the ell=2 gradient norm leaves coexact trace 64 rather than zero.",
        },
        {
            "claim": "this proves the final determinant obstruction",
            "verdict": "not_yet",
            "reason": "The result is a trace-level Hodge proxy. It still needs explicit coexact n=3 basis projection, sign, denominator, and determinant normalization.",
        },
    ],
    "next_required_audit": {
        "name": "explicit_n3_coexact_basis_projection",
        "task": "construct an orthonormal coexact n=3 basis and project the Hodge-filtered image onto it",
        "pass_if": "explicit projected trace equals the proxy trace 64 and is incorporated into determinant bookkeeping, or cancels by a missing projection/Hilbert term",
    },
    "verdict": (
        "The Hodge-projection proxy removes the exact/gradient part inferred from divergence, but it leaves a nonzero coexact trace 64. "
        "Thus the n=1->3 channel is now a serious candidate obstruction, not merely a normal or exact artifact. The result is still proxy-level and must be confirmed with an explicit orthonormal coexact n=3 projection."
    ),
}

Path("s2t_c6_l21_n3_hodge_projection_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "tangent_trace": G_trace,
    "exact_removed": exact_trace,
    "coexact_trace_proxy": coexact_trace,
    "second_order_proxy": coexact_second_order_proxy,
}, indent=2, ensure_ascii=False))