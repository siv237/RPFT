import json
from pathlib import Path


def shell_data(n):
    kept = n % 2 == 1 and n >= 1
    return {
        "n": n,
        "kept_on_l21": kept,
        "lambda": (n + 1) ** 2,
        "coexact_degeneracy_l21": 2 * n * (n + 2) if kept else 0,
    }

shells = {n: shell_data(n) for n in [1, 3]}
channels = []
for n, m in [(1, 1), (1, 3), (3, 1)]:
    dn = shells[n]["coexact_degeneracy_l21"]
    dm = shells[m]["coexact_degeneracy_l21"]
    lam_n = shells[n]["lambda"]
    lam_m = shells[m]["lambda"]
    channels.append({
        "channel": f"{n}->{m}",
        "matrix_shape_per_deformation_A": [dn, dm],
        "entries_per_deformation_A": dn * dm,
        "trace_square_weight_lambda_inverse": 1 / (lam_n * lam_m),
        "lambda_n": lam_n,
        "lambda_m": lam_m,
        "why_included": "lowest finite/nonlocal channel required by shell-selection and locality-gate audits",
    })

operator_terms = [
    {
        "term": "principal_symbol",
        "schematic": "-delta g^{ab} nabla_a nabla_b alpha_c",
        "must_include": True,
    },
    {
        "term": "connection_variation",
        "schematic": "terms with delta Gamma acting on nabla alpha and alpha",
        "must_include": True,
    },
    {
        "term": "ricci_variation",
        "schematic": "delta Ric_c^d alpha_d",
        "must_include": True,
    },
    {
        "term": "coexact_projection",
        "schematic": "Pi_coex delta_A Delta_1 Pi_coex plus slice correction",
        "must_include": True,
    },
    {
        "term": "inner_product_measure_variation",
        "schematic": "variation of one-form Hilbert metric and volume measure",
        "must_include": True,
    },
]

pass_fail = [
    {
        "outcome": "all_low_shell_coefficients_zero",
        "effect": "strongly supports a coefficient-level collapse theorem, but higher odd shells still require induction/asymptotic proof",
    },
    {
        "outcome": "low_shell_block_nonzero_but_matches_absorption_identity",
        "effect": "keeps C6 viable if normalization is derived and no new parameter is introduced",
    },
    {
        "outcome": "low_shell_block_nonzero_independent_finite_residue",
        "effect": "blocks determinant-theorem status for pi^-4; S_vac remains structural compression or needs downgrade",
    },
    {
        "outcome": "result_depends_on_using_full_hA_vs_reduced_2qAg_slice",
        "effect": "slice-choice theorem becomes mandatory before any C6 claim",
    },
]

results = {
    "status": "low_shell_block_spec_fixed_next_required_calculation",
    "shells": shells,
    "channels": channels,
    "total_entries_per_deformation_A_for_required_low_block": sum(c["entries_per_deformation_A"] for c in channels),
    "deformation_space_dimension": 10,
    "total_entries_if_all_deformations_explicit": 10 * sum(c["entries_per_deformation_A"] for c in channels),
    "operator_terms_required": operator_terms,
    "pass_fail_criteria": pass_fail,
    "verdict": (
        "The next non-rhetorical C6 step is now fixed: compute the finite low-shell matrix block for channels 1->1, 1->3, and 3->1. "
        "The block has degeneracies 6 and 30, hence 36 + 180 + 180 = 396 entries per deformation direction before symmetry reductions, or 3960 entries over Sym^2(R4). "
        "A scalar shortcut is not acceptable; the full one-form Laplacian variation, coexact projection, and inner-product variation must be included."
    ),
}

Path("s2t_c6_l21_low_shell_block_spec_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "channels": channels,
    "total_entries_per_A": results["total_entries_per_deformation_A_for_required_low_block"],
    "total_entries_all_A": results["total_entries_if_all_deformations_explicit"],
}, indent=2, ensure_ascii=False))