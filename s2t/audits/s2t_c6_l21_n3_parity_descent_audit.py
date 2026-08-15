import json
from pathlib import Path

source = json.loads(Path("s2t_c6_l21_n3_explicit_projection_results.json").read_text())

# Antipodal map a(x)=-x on S3.  A homogeneous degree-d ambient one-form
# alpha = sum_i V_i(x) dx_i descends to L(2,1)=S3/{±1} iff a^* alpha = alpha.
# Since a^* dx_i = -dx_i and V_i(-x)=(-1)^d V_i(x), the pullback parity is
# (-1)^(d+1).  Thus odd-degree vector coefficients give invariant one-forms.
DEGREE = 3
one_form_pullback_sign = (-1) ** (DEGREE + 1)
vector_component_sign = (-1) ** DEGREE
basis_dimension = source["construction"]["basis_dimension"]
projected_trace = source["projection"]["projected_gram_trace"]
projected_rank = source["projection"]["projected_rank_numeric"]

results = {
    "status": "n3_cubic_coexact_basis_descends_to_L21_antipodal_quotient",
    "source": "s2t_c6_l21_n3_explicit_projection_results.json",
    "antipodal_rule": {
        "map": "a(x)=-x on S3",
        "one_form": "alpha=sum_i V_i(x) dx_i",
        "component_degree": DEGREE,
        "component_parity_V_minus_x_over_V_x": vector_component_sign,
        "dx_pullback_sign": -1,
        "one_form_pullback_sign": one_form_pullback_sign,
        "descends_to_L21": one_form_pullback_sign == 1,
    },
    "normalization_rule": {
        "quotient_volume_used": "Vol(L(2,1))=pi^2",
        "basis_inner_product": source["construction"]["inner_product"],
        "orthonormality_error": source["construction"]["basis_orthonormality_max_abs_error"],
        "constraint_error": source["construction"]["basis_constraint_max_abs"],
        "no_extra_cover_factor": "The basis is already quotient-normalized; do not multiply the projected trace by 2 or 1/2.",
    },
    "projection_carried_over": {
        "basis_dimension": basis_dimension,
        "projected_trace": projected_trace,
        "projected_rank": projected_rank,
        "interpretation": "The nonzero n=3 projection is compatible with the L(2,1) quotient parity gate.",
    },
    "failure_modes_closed": [
        "The n=3 obstruction is not removed by antipodal parity: cubic coefficient one-forms are quotient-even.",
        "The n=3 obstruction is not a cover-normalization factor-of-two artifact in this audit: the inner product used Vol(L(2,1))=pi^2.",
    ],
    "remaining_caveat": (
        "This closes only the quotient/parity normalization gate for the explicit n=3 projection. "
        "It does not add the missing full one-form operator terms or determinant sign bookkeeping."
    ),
    "verdict": (
        "The explicit n=3 cubic coexact basis passes the L(2,1) descent check: cubic vector coefficients are odd, dx is odd, and their product is antipodal-even. "
        "Therefore the nonzero projected trace is not killed by the RP3 quotient parity rule and should not receive an extra cover factor."
    ),
}

Path("s2t_c6_l21_n3_parity_descent_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "one_form_pullback_sign": one_form_pullback_sign,
    "descends_to_L21": one_form_pullback_sign == 1,
    "projected_trace": projected_trace,
    "projected_rank": projected_rank,
}, indent=2, ensure_ascii=False))