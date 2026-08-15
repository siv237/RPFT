import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
VOL_RP3 = math.pi**2
BASE = (VOL_RP3 / 2) * T_RP3 / S_GEO
P02_RANK = 10
P02_SUPPRESSION = 1 - P02_RANK / (24 * S_GEO)
P02_TERM = BASE * P02_SUPPRESSION

# Sign convention for quadratic trace-square contribution in effective action:
# real boson +1/2 log det -> negative trace-square coefficient
# complex Grassmann ghost - log det -> positive trace-square coefficient
# We model only the sign/rank effect of a P02 insertion, not the full determinant.
scenarios = [
    {
        "scenario": "P02_only_in_coexact_bosonic_mixed_block",
        "coexact_rank": P02_RANK,
        "ghost_rank": 0,
        "effective_rank_in_suppression": P02_RANK,
        "factor": 1 - P02_RANK / (24 * S_GEO),
        "status": "desired_conditional_route",
        "reason": "Bosonic coexact second variation supplies negative trace-square; ghost/exact branch contributes only the finite 1/24 scalar Casimir coefficient, not an independent P02 trace-square.",
    },
    {
        "scenario": "same_P02_in_coexact_and_ghost_trace_square",
        "coexact_rank": P02_RANK,
        "ghost_rank": P02_RANK,
        "effective_rank_in_suppression": 0,
        "factor": 1.0,
        "status": "no_suppression_no_pi4_match",
        "reason": "Ghost quadratic sign is opposite, so equal P02 ghost insertion cancels the bosonic suppression in this simplified sign model.",
    },
    {
        "scenario": "P02_in_coexact_plus_full_even_scalar_ghost_leakage_through_ell4",
        "coexact_rank": P02_RANK,
        "ghost_rank": 35,
        "effective_rank_in_suppression": P02_RANK - 35,
        "factor": 1 - (P02_RANK - 35) / (24 * S_GEO),
        "status": "wrong_direction_enhancement",
        "reason": "If ghost/exact leakage includes ell=0,2,4 cumulative rank 35 with opposite sign, the net correction enhances rather than suppresses.",
    },
    {
        "scenario": "ordinary_exact_scalar_pairing_before_P02_insertion",
        "coexact_rank": P02_RANK,
        "ghost_rank": "paired_nonzero_scalar_modes_cancel_exact_branch",
        "effective_rank_in_suppression": P02_RANK,
        "factor": 1 - P02_RANK / (24 * S_GEO),
        "status": "viable_if_P02_is_geometric_coexact_insertion",
        "reason": "The nonzero exact/scalar tower cancels before the coexact first-strain insertion is evaluated; ell>=4 never appears because P02 is not selected from the scalar tower.",
    },
]

for row in scenarios:
    if isinstance(row["factor"], float):
        row["absorption_value"] = BASE * row["factor"]
        row["relative_error_vs_pi4"] = (row["absorption_value"] - PI4_TERM) / PI4_TERM

conditions = [
    {
        "condition": "P02_is_metric_strain_not_ghost_field",
        "status": "required",
        "meaning": "P02 labels the first ambient metric/volume strain insertion in the coexact Maxwell operator, not an independent scalar ghost mode selection.",
    },
    {
        "condition": "exact_scalar_cancellation_before_finite_strain_trace",
        "status": "required",
        "meaning": "The ordinary nonzero exact one-form/scalar ghost tower cancels at the gauge-fixed determinant level before any finite rank P02 trace is counted.",
    },
    {
        "condition": "constant_scalar_branch_reduced_to_kappa_Cas",
        "status": "required",
        "meaning": "The ell=0 scalar branch contributes through the already isolated periodic finite part 1/24, not as a ghost trace-square with opposite sign.",
    },
    {
        "condition": "no_ghost_P02_trace_square",
        "status": "main_open_condition",
        "meaning": "One must prove that the ghost determinant does not carry the same P02 trace-square insertion as the coexact bosonic block.",
    },
]


fp_bookkeeping = [
    {
        "scheme": "physical_transverse_quotient",
        "effective_nonzero_exact_scalar_power": 0.0,
        "constant_scalar_residual_power": 0.0,
        "P02_ghost_trace_square_power": 0.0,
        "classification": "conditional_route_open",
        "meaning": (
            "If the determinant is defined directly on the transverse/coexact quotient and the scalar zero mode is treated only "
            "through the already isolated kappa_Cas finite part, then the desired P02 coexact insertion is not contaminated by "
            "a ghost trace-square. This is a scheme/lemma choice, not an automatic covariant-FP theorem."
        ),
    },
    {
        "scheme": "standard_covariant_FP_Hodge_split",
        "effective_nonzero_exact_scalar_power": "scheme_dependent_after_Jacobian_and_prime_det",
        "constant_scalar_residual_power": "generically_nonzero_or_requires_explicit_volume_normalization",
        "P02_ghost_trace_square_power": "not_excluded_without_delta2_Delta0_computation",
        "classification": "not_closed",
        "meaning": (
            "In a covariant Faddeev--Popov derivation, exact one-forms, scalar ghosts, prime determinants, "
            "Hodge-Jacobians, and gauge-volume factors must be combined explicitly. A leftover scalar determinant or half-power "
            "is possible unless the cancellation is proven in the same normalization. Therefore ghost isolation cannot be marked proven."
        ),
    },
]

lemma_obligations = [
    "derive the Hodge measure Jacobian for A=A_coex+dphi on RP3 x S1",
    "combine the exact one-form determinant, FP ghost determinant, det-prime rule, and gauge-volume factor",
    "show any residual scalar determinant is exactly the kappa_Cas=1/24 branch and not a P02 trace-square",
    "compute delta_g^2 log det prime Delta0 on first ambient strain or prove its P02 trace vanishes by symmetry",
]

results = {
    "status": "ghost_exact_isolation_required_for_C6_not_proven",
    "numbers": {
        "S_geo": S_GEO,
        "base_volume_half_absorption": BASE,
        "P02_rank": P02_RANK,
        "P02_suppression": P02_SUPPRESSION,
        "P02_term": P02_TERM,
        "pi4_term": PI4_TERM,
        "P02_relative_error_vs_pi4": (P02_TERM - PI4_TERM) / PI4_TERM,
    },
    "scenarios": scenarios,
    "conditions": conditions,
    "fp_bookkeeping": fp_bookkeeping,
    "lemma_obligations": lemma_obligations,
    "verdict": (
        "The desired C6 sign survives only if P02 is isolated as a coexact bosonic metric-strain insertion. "
        "The physical transverse quotient keeps this route open as a conditional scheme. In standard covariant FP bookkeeping, however, "
        "a residual scalar determinant/half-power is not excluded until the Hodge Jacobian, det-prime rule, gauge volume, and ghost determinant "
        "are combined explicitly. If the same P02 trace-square appears in the ghost determinant, the opposite Grassmann sign cancels or reverses "
        "the suppression. Therefore the next theorem-level obligation is not numerical: prove exact/scalar ghost cancellation before the finite P02 "
        "coexact trace and prove that the ell=0 scalar branch enters only through kappa_Cas=1/24."
    ),
}

Path("s2t_c6_ghost_exact_isolation_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "desired_factor": P02_SUPPRESSION,
    "same_P02_in_ghost_factor": scenarios[1]["factor"],
    "ell4_leakage_factor": scenarios[2]["factor"],
    "main_open_condition": "no_ghost_P02_trace_square",
    "standard_covariant_FP_status": "not_closed_residual_scalar_possible",
}, indent=2, ensure_ascii=False))