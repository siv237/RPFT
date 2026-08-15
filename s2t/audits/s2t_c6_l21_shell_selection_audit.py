import json
from pathlib import Path


def kept_coexact_shell(n):
    return n >= 1 and n % 2 == 1


def degeneracy_l21(n):
    if not kept_coexact_shell(n):
        return 0
    return 2 * n * (n + 2)


def allowed_by_quadratic_strain(n, m):
    """Necessary SO(4)/spherical-harmonic style selection rule.

    A quadratic even strain has scalar degree ell=0 or ell=2.  Multiplication / first-order
    metric variation can only connect shells with the same parity and distance at most two
    at the representation-label level.  This is not a coefficient calculation; it is a
    conservative necessary-channel audit.
    """
    if not (kept_coexact_shell(n) and kept_coexact_shell(m)):
        return False
    return abs(n - m) in (0, 2)


n_max = 17
kept_shells = [n for n in range(1, n_max + 1) if kept_coexact_shell(n)]
channels = []
for n in kept_shells:
    for m in kept_shells:
        if allowed_by_quadratic_strain(n, m):
            channels.append({
                "n": n,
                "m": m,
                "lambda_n": (n + 1) ** 2,
                "lambda_m": (m + 1) ** 2,
                "degeneracy_n": degeneracy_l21(n),
                "degeneracy_m": degeneracy_l21(m),
                "channel_type": "diagonal" if n == m else "nearest_kept_shell",
            })

per_shell = []
for n in kept_shells:
    targets = [m for m in kept_shells if allowed_by_quadratic_strain(n, m)]
    per_shell.append({
        "n": n,
        "targets": targets,
        "target_count": len(targets),
        "has_diagonal_channel": n in targets,
        "has_off_diagonal_channel": any(m != n for m in targets),
    })

failure_modes = [
    {
        "claim": "quadratic_strain_only_hits_first_shell",
        "result": "fails",
        "reason": "The same necessary rule gives diagonal n->n channels for every surviving odd n.",
    },
    {
        "claim": "RP3_parity_removes_quadratic_off_diagonal_tower",
        "result": "fails",
        "reason": "The ell=2 even insertion preserves parity, so odd surviving shells couple to odd shells n±2.",
    },
    {
        "claim": "rank_10_follows_from_shell_selection_alone",
        "result": "fails",
        "reason": "Selection leaves infinitely many shell channels; rank 10 is only the deformation-space rank unless coefficients cancel or renormalize the tower.",
    },
]

next_obligations = [
    {
        "task": "compute_actual_vector_harmonic_coefficients",
        "why": "The necessary selection rule shows which channels can exist but not whether their coefficients vanish after the full one-form Laplacian variation and coexact projection.",
    },
    {
        "task": "separate_local_heat_kernel_from_nonlocal_finite_part",
        "why": "Diagonal all-shell contributions may be local/subtractable, but finite winding/Bessel pieces cannot be discarded without proof.",
    },
    {
        "task": "test_first_shell_dominance_after_coefficients",
        "why": "Prior coexact Bessel tail is dominated by n=1; the real mixed trace could still be numerically dominated even if not exactly finite-rank.",
    },
]

results = {
    "status": "quadratic_strain_selection_allows_infinite_coexact_shell_channels",
    "rule": {
        "strain_space": "P_0,2 = scalar ell 0 plus ell 2 from Sym^2(R4)",
        "l21_projection": "keep odd coexact n only",
        "necessary_channel_rule": "surviving odd n may connect to odd m with |n-m| in {0,2}",
        "important_limit": "This is a necessary representation-level rule, not the final coefficient calculation.",
    },
    "kept_shells_checked": kept_shells,
    "per_shell_channels": per_shell,
    "channels": channels,
    "failure_modes": failure_modes,
    "next_obligations": next_obligations,
    "verdict": (
        "Quadratic first ambient strain is even and therefore preserves the L(2,1) parity sector. "
        "At the necessary representation-selection level it leaves diagonal channels for every surviving odd coexact shell and off-diagonal channels between neighboring surviving odd shells n and n±2. "
        "Therefore the C6 rank-10 result cannot be derived from shell selection alone. It requires an additional coefficient-level theorem: cancellation, locality/subtraction, or physical-quotient renormalization of the infinite allowed coexact channels."
    ),
}

Path("s2t_c6_l21_shell_selection_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "kept_shells_checked": kept_shells,
    "first_three_shell_rules": per_shell[:3],
    "channel_count_checked": len(channels),
}, indent=2, ensure_ascii=False))