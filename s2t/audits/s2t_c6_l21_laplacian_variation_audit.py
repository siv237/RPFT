import json
from pathlib import Path

# Structural audit for the first metric variation of the Hodge Laplacian on one-forms.
# This is the next layer after fixing the L(2,1) coexact shells.
# It does not compute matrix elements; it fixes the operator terms that must be included.

operator_identity = {
    "operator": "Hodge Laplacian on one-forms",
    "formula": "Delta_1 alpha = (d delta + delta d) alpha = -nabla^2 alpha + Ric(alpha) in the chosen sign convention",
    "domain": "coexact one-forms on L(2,1), with delta alpha=0 before variation",
    "variation_parameter": "h_A, the metric variation induced by A in Sym^2(R4)",
}

variation_terms = [
    {
        "term": "principal_symbol_term",
        "schematic_form": "- delta g^{ab} nabla_a nabla_b alpha_c",
        "depends_on": "quadratic strain h_A",
        "status": "must_include",
        "why": "This is the highest-derivative part and controls the main shell couplings.",
    },
    {
        "term": "connection_variation_terms",
        "schematic_form": "terms with delta Gamma * nabla alpha and nabla(delta Gamma) * alpha",
        "depends_on": "first derivatives of h_A",
        "status": "must_include",
        "why": "One-form Laplacian is not just a scalar Laplacian acting componentwise.",
    },
    {
        "term": "curvature_variation_term",
        "schematic_form": "delta Ric_c^d alpha_d plus index-raising changes",
        "depends_on": "second derivatives and traces of h_A",
        "status": "must_include",
        "why": "On curved S3/RP3 background, the Weitzenbock curvature term contributes at the same order.",
    },
    {
        "term": "coexact_projection_term",
        "schematic_form": "Pi_coex delta(Delta_1) Pi_coex plus variation of the slice if the inner product changes",
        "depends_on": "Hodge decomposition and metric-dependent codifferential",
        "status": "must_include_or_justify_absence",
        "why": "A metric variation can move a representative out of the coexact slice; the physical determinant needs the reduced operator.",
    },
    {
        "term": "measure_inner_product_term",
        "schematic_form": "variation of sqrt(g) and of the one-form inner product in matrix elements",
        "depends_on": "trace of h_A and normalization of eigenforms on L(2,1)",
        "status": "must_include",
        "why": "Rank and volume factors cannot be trusted unless matrix elements use the varied Hilbert-space metric consistently.",
    },
]

first_strain_structure = [
    {
        "component": "trace_direction",
        "space": "one-dimensional part of Sym^2(R4)",
        "expected_role": "constant rescaling / volume direction",
        "risk": "can mix with zero/gauge normalization rather than finite P02 trace",
    },
    {
        "component": "traceless_quadratic_direction",
        "space": "nine-dimensional harmonic quadratic part",
        "expected_role": "ell=2 metric strain channel",
        "risk": "must be shown to act through coexact matrix elements with the required trace-square sign",
    },
]

forbidden_shortcuts = [
    {
        "shortcut": "use_scalar_laplacian_variation_componentwise",
        "verdict": "not_allowed",
        "reason": "One-forms have connection and curvature terms absent from scalar functions.",
    },
    {
        "shortcut": "ignore_coexact_projection",
        "verdict": "not_allowed_without_proof",
        "reason": "The physical determinant is on a metric-dependent transverse slice.",
    },
    {
        "shortcut": "identify_rank_10_before_matrix_elements",
        "verdict": "not_allowed",
        "reason": "Rank 10 is deformation-space rank; the operator trace may still contain the full coexact tower.",
    },
    {
        "shortcut": "drop_curvature_term_on_RP3",
        "verdict": "not_allowed",
        "reason": "RP3 has constant positive curvature inherited from S3, so Ricci terms are part of Delta_1.",
    },
]

minimal_next_computation = [
    {
        "step": 1,
        "task": "write h_A explicitly on S3/RP3",
        "output": "Formula for h_ab from the ambient quadratic strain A.",
    },
    {
        "step": 2,
        "task": "derive delta Gamma and delta Ric for h_A",
        "output": "Local tensor formula for delta_A Delta_1 on one-forms.",
    },
    {
        "step": 3,
        "task": "project to coexact slice",
        "output": "Reduced operator Pi_coex delta_A Delta_1 Pi_coex with normalization conventions.",
    },
    {
        "step": 4,
        "task": "evaluate first shell matrix elements",
        "output": "Numbers or symbolic coefficients for n=1 to n=1 and n=1 to n=3 couplings.",
    },
]

pass_fail_tests = [
    {
        "test": "operator_formula_complete",
        "status": "not_yet",
        "needed_to_pass": "All five variation term classes are written explicitly with signs.",
    },
    {
        "test": "projection_consistent",
        "status": "not_yet",
        "needed_to_pass": "The varied operator is self-adjoint on the chosen coexact inner product.",
    },
    {
        "test": "rank_collapse_testable",
        "status": "not_yet",
        "needed_to_pass": "Matrix elements are explicit enough to sum over A in Sym^2(R4) and over coexact shells.",
    },
]

results = {
    "status": "laplacian_variation_terms_fixed_matrix_elements_still_missing",
    "operator_identity": operator_identity,
    "variation_terms": variation_terms,
    "first_strain_structure": first_strain_structure,
    "forbidden_shortcuts": forbidden_shortcuts,
    "minimal_next_computation": minimal_next_computation,
    "pass_fail_tests": pass_fail_tests,
    "verdict": (
        "The next C6 calculation cannot use a scalar shortcut. The one-form Hodge Laplacian variation contains principal-symbol, connection, curvature, coexact-projection, and inner-product terms. "
        "All must be included before any claim that the L(2,1) coexact mixed trace collapses to P02 rank 10. The immediate next computation is to write h_A, derive delta Gamma and delta Ric, project to the coexact slice, and evaluate the first-shell matrix elements."
    ),
}

Path("s2t_c6_l21_laplacian_variation_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "variation_term_count": len(variation_terms),
    "forbidden_shortcuts": [row["shortcut"] for row in forbidden_shortcuts],
}, indent=2, ensure_ascii=False))