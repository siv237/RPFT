import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
P02_RANK = 10
T_COEX_RP3 = 1.5227161455271536e-05
BASE_VOLUME_HALF = (math.pi**2 / 2) * T_COEX_RP3 / S_GEO
N_NEED = 24 * S_GEO * (1 - PI4_TERM / BASE_VOLUME_HALF)
P02_ABSORPTION = BASE_VOLUME_HALF * (1 - P02_RANK / (24 * S_GEO))

# Structural check of the requested theorem-level task:
# compute the L(2,1) coexact mixed trace in the primary physical determinant scheme.
# This script does not pretend to know the missing eigenform matrix elements. It isolates exactly
# what must be computed and what can already be concluded from previous audits.


def coexact_shells(n_max=9):
    rows = []
    for n in range(1, n_max + 1):
        degeneracy_s3 = 2 * n * (n + 2)
        kept_on_rp3 = n % 2 == 1
        rows.append({
            "n": n,
            "rho": n + 1,
            "lambda_one_form_unit_s3": (n + 1) ** 2,
            "degeneracy_s3_coexact_candidate": degeneracy_s3,
            "rp3_projection_rule_used_in_prior_audit": "keep odd n only",
            "degeneracy_rp3_candidate": degeneracy_s3 if kept_on_rp3 else 0,
            "kept_on_rp3": kept_on_rp3,
        })
    return rows

required_operator_formula = {
    "physical_determinant": "Gamma_EM^phys[g] = 1/2 log det' Delta_1,coex[g] + Gamma_zero/gauge[g] + Gamma_local[g]",
    "first_variation": "delta_A Delta_1,coex must be written for A in Sym^2(R4) restricted to RP3",
    "mixed_trace": "C_AA = Tr_coex(Delta_1,coex^{-1} delta_A Delta_1,coex Delta_1,coex^{-1} delta_A Delta_1,coex)",
    "rank_reduction_needed": "sum_A C_AA must reduce to a universal constant times Tr(P02)=10, not to a full coexact tower-dependent tensor",
}

already_supported = [
    {
        "claim": "coexact domain removes nonzero scalar residual by definition",
        "status": "supported_if_physical_quotient_is_primary",
        "reason": "The scalar tower is not part of the coexact one-form determinant domain.",
    },
    {
        "claim": "second variation has the right bosonic sign",
        "status": "formally_supported",
        "reason": "For a real bosonic 1/2 log determinant, the trace-square term carries the needed negative sign after expansion.",
    },
    {
        "claim": "P02 has natural rank 10",
        "status": "supported_as_first_ambient_strain_space",
        "reason": "Sym^2(R4)=1+9 gives the trace plus traceless quadratic deformations.",
    },
    {
        "claim": "coexact tower is not zero",
        "status": "supported_by_prior_positive_tail_audit",
        "reason": "Positive coexact Bessel contributions cannot disappear by sign cancellation inside a single ordinary coexact sector.",
    },
]

blocking_unknowns = [
    {
        "unknown": "explicit_coexact_eigenform_matrix_elements",
        "needed": "Matrix elements of delta_A Delta_1,coex between coexact vector harmonics on L(2,1)",
        "current_status": "not_computed",
        "consequence": "No theorem-level mixed trace yet.",
    },
    {
        "unknown": "projection_of_first_ambient_strain_on_coexact_forms",
        "needed": "Proof that only P02 enters the finite mixed residue and higher shells are outside the II.A insertion",
        "current_status": "conditional_selection_rule",
        "consequence": "Rank 10 remains a structural selection, not an operator trace result.",
    },
    {
        "unknown": "normalization_of_volume_half_factor",
        "needed": "Derive pi^2/2 from normalized L(2,1) eigenforms and the real bosonic determinant power",
        "current_status": "plausible_not_derived_here",
        "consequence": "Overall C6 coefficient is not yet a theorem.",
    },
    {
        "unknown": "small_gap_N_need_minus_10",
        "needed": "Explain 0.0099700224 as a finite scheme residue or prove it below target precision",
        "current_status": "open",
        "consequence": "Even rank 10 gives a near miss, not exact equality.",
    },
]

possible_outcomes = [
    {
        "outcome": "operator_trace_equals_P02_rank_with_allowed_scheme_gap",
        "C6_status": "promote_to_conditional_theorem_candidate",
        "meaning": "The physical coexact route survives and the remaining gap can be treated as a derived finite normalization issue.",
    },
    {
        "outcome": "operator_trace_contains_full_coexact_tower_tensor",
        "C6_status": "blocked_as_theorem",
        "meaning": "The rank-10 story is only a compression, because the real coexact trace does not collapse to P02.",
    },
    {
        "outcome": "operator_trace_has_wrong_sign_or_volume_power",
        "C6_status": "failed_route",
        "meaning": "The physical quotient does not reproduce the pi^-4 subtraction structure.",
    },
    {
        "outcome": "operator_trace_requires_new_finite_counterterm",
        "C6_status": "downgrade_unless_counterterm_is_derived",
        "meaning": "A new finite term is allowed only if forced by geometry or regularization, not chosen after seeing the target number.",
    },
]

work_plan = [
    {
        "step": 1,
        "task": "choose_coexact_vector_harmonic_basis_on_L21",
        "deliverable": "Explicit basis and multiplicities for the first shells, with RP3 parity rule fixed.",
    },
    {
        "step": 2,
        "task": "write_metric_first_variation_of_Hodge_Laplacian_on_one_forms",
        "deliverable": "Formula for delta_A Delta_1 acting on coexact forms before projection back to coexact slice.",
    },
    {
        "step": 3,
        "task": "compute_shell_matrix_elements",
        "deliverable": "Finite-shell table for Tr(Delta^-1 delta Delta Delta^-1 delta Delta) over A in Sym^2(R4).",
    },
    {
        "step": 4,
        "task": "test_rank_collapse",
        "deliverable": "Decision whether the trace collapses to rank 10 or contains the full tower structure.",
    },
]

results = {
    "status": "L21_coexact_mixed_trace_not_computed_root_obligation_is_explicit_operator_matrix_elements",
    "numbers": {
        "S_geo": S_GEO,
        "pi4_term": PI4_TERM,
        "T_coex_RP3": T_COEX_RP3,
        "base_volume_half_absorption": BASE_VOLUME_HALF,
        "N_need": N_NEED,
        "P02_rank": P02_RANK,
        "N_need_minus_P02": N_NEED - P02_RANK,
        "P02_absorption": P02_ABSORPTION,
        "P02_relative_error_vs_pi4": (P02_ABSORPTION - PI4_TERM) / PI4_TERM,
    },
    "first_coexact_shells": coexact_shells(),
    "required_operator_formula": required_operator_formula,
    "already_supported": already_supported,
    "blocking_unknowns": blocking_unknowns,
    "possible_outcomes": possible_outcomes,
    "work_plan": work_plan,
    "verdict": (
        "The physical coexact route has reached the real theorem bottleneck: explicit L(2,1) coexact eigenform matrix elements of the first metric variation are missing. "
        "Current evidence supports the domain choice, the bosonic sign, and the natural P02 rank, but it does not yet prove that the actual coexact mixed trace collapses to rank 10. "
        "Therefore C6 remains a sharply posed calculation, not a theorem. The next step is to compute coexact vector-harmonic matrix elements shell by shell."
    ),
}

Path("s2t_c6_l21_coexact_mixed_trace_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "N_need_minus_P02": results["numbers"]["N_need_minus_P02"],
    "relative_error_vs_pi4": results["numbers"]["P02_relative_error_vs_pi4"],
    "next_missing_object": "coexact_eigenform_matrix_elements_of_delta_A_Delta_1_on_L21",
}, indent=2, ensure_ascii=False))