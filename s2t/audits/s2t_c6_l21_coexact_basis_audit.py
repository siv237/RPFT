import json
import math
from pathlib import Path

# Preparatory basis audit for the L(2,1) coexact mixed-trace calculation.
# It fixes the shell labels, projection rule, degeneracies, and the exact missing matrix element problem.


def coexact_shells(n_max=15):
    rows = []
    cumulative = 0
    for n in range(1, n_max + 1):
        degeneracy_s3 = 2 * n * (n + 2)
        kept = n % 2 == 1
        degeneracy_l21 = degeneracy_s3 if kept else 0
        cumulative += degeneracy_l21
        rows.append({
            "n": n,
            "rho": n + 1,
            "lambda_unit_radius": (n + 1) ** 2,
            "s3_coexact_degeneracy": degeneracy_s3,
            "l21_projection_parity": "kept" if kept else "projected_out",
            "l21_coexact_degeneracy": degeneracy_l21,
            "cumulative_l21_degeneracy": cumulative,
            "dominant_candidate": n == 1,
        })
    return rows

shells = coexact_shells()
kept_shells = [row for row in shells if row["l21_coexact_degeneracy"] > 0]

basis_requirements = [
    {
        "item": "coexact_condition",
        "meaning": "Use one-forms alpha with delta alpha = 0; exact gradients are excluded from the physical determinant domain.",
        "status": "definition_fixed",
    },
    {
        "item": "laplacian_eigenvalue",
        "meaning": "For the convention used in prior tower audits, shell n has lambda=(n+1)^2 and rho=n+1.",
        "status": "convention_fixed",
    },
    {
        "item": "s3_degeneracy",
        "meaning": "The two transverse families together have multiplicity 2 n (n+2).",
        "status": "convention_fixed",
    },
    {
        "item": "l21_projection",
        "meaning": "For L(2,1)=S3/{±1}, prior audits keep odd n and project out even n.",
        "status": "working_projection_rule",
    },
    {
        "item": "normalization",
        "meaning": "Eigenforms must be orthonormal on L(2,1), not inherited with S3 volume normalization by accident.",
        "status": "must_be_checked_in_next_calculation",
    },
]

missing_matrix_data = [
    {
        "object": "delta_A_Delta_1_matrix",
        "needed": "<n,i | delta_A Delta_1 | m,j> for coexact L(2,1) vector harmonics and A in Sym^2(R4)",
        "why": "Without these entries the mixed trace cannot be evaluated.",
    },
    {
        "object": "coexact_projection_after_variation",
        "needed": "Projection of delta_A Delta_1 alpha back to the coexact slice",
        "why": "Metric variation can mix representative components unless the physical slice is handled explicitly.",
    },
    {
        "object": "selection_by_quadratic_strain",
        "needed": "Which shell pairs (n,m) are connected by a quadratic ambient deformation",
        "why": "This decides whether the trace collapses to P02 or spreads over the tower.",
    },
    {
        "object": "orthonormal_l21_integrals",
        "needed": "Integrals of products of two vector harmonics and one quadratic strain over L(2,1)",
        "why": "These integrals are the actual coefficients in the trace-square.",
    },
]

first_shell_diagnostic = {
    "first_kept_shell_n": kept_shells[0]["n"],
    "first_kept_shell_lambda": kept_shells[0]["lambda_unit_radius"],
    "first_kept_shell_degeneracy": kept_shells[0]["l21_coexact_degeneracy"],
    "diagnostic": (
        "The first surviving coexact shell has degeneracy 6, not 10. Therefore the desired P02 rank 10 cannot be read off from the first coexact eigenvalue multiplicity. "
        "It must arise from the deformation space Sym^2(R4), or it does not arise at all."
    ),
}

route_tests = [
    {
        "test": "rank_10_from_eigenvalue_multiplicity",
        "result": "fails",
        "reason": "First kept coexact shell has multiplicity 6; cumulative kept multiplicities are 6, 36, 106, ... not 10.",
    },
    {
        "test": "rank_10_from_deformation_space",
        "result": "still_possible",
        "reason": "Sym^2(R4) has dimension 10, so rank 10 can only come from summing over allowed first metric deformations, not from counting coexact modes.",
    },
    {
        "test": "tower_absence_by_projection",
        "result": "fails",
        "reason": "The L(2,1) projection removes even n but leaves infinitely many odd n shells.",
    },
    {
        "test": "finite_trace_without_matrix_elements",
        "result": "not_allowed",
        "reason": "A finite P02 answer must follow from matrix elements and selection rules, not from replacing the tower by rank 10 by declaration.",
    },
]

results = {
    "status": "L21_coexact_basis_fixed_rank10_not_from_mode_count",
    "shell_table": shells,
    "basis_requirements": basis_requirements,
    "missing_matrix_data": missing_matrix_data,
    "first_shell_diagnostic": first_shell_diagnostic,
    "route_tests": route_tests,
    "verdict": (
        "The L(2,1) coexact basis layer is now fixed at the shell-counting level: odd n shells survive with degeneracy 2n(n+2), even n shells are projected out. "
        "This immediately shows that rank 10 is not an eigenmode multiplicity: the first surviving coexact shell has degeneracy 6 and the tower remains infinite. "
        "Therefore C6 can only be saved if the mixed trace over metric deformations Sym^2(R4) collapses to P02 through explicit matrix elements. The next missing data are the integrals <n,i|delta_A Delta_1|m,j>."
    ),
}

Path("s2t_c6_l21_coexact_basis_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "first_kept_shell": first_shell_diagnostic,
    "kept_shells_first_four": kept_shells[:4],
}, indent=2, ensure_ascii=False))