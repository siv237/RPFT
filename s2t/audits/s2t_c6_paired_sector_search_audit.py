import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
P02_RANK = 10
TRACE_RANK = 1
TRACELESS_RANK = 9
FIRST_NONZERO_EVEN_SCALAR_ELL = 2
FIRST_NONZERO_EVEN_SCALAR_MULT = (FIRST_NONZERO_EVEN_SCALAR_ELL + 1) ** 2
FIRST_NONZERO_EVEN_SCALAR_LAMBDA_S3 = FIRST_NONZERO_EVEN_SCALAR_ELL * (FIRST_NONZERO_EVEN_SCALAR_ELL + 2)

REQUIRED_GAMMA_SCALAR_POWER = 0.5
REQUIRED_SPECTRUM = "same nonzero even scalar Delta0 spectrum on RP3 x S1, including ell=2,4,... and S1 momenta"
REQUIRED_COUPLING = "same P02=Sym^2(R4)=1+9 second-variation trace-square, with opposite sign to the scalar FP residual"

# Context: standard covariant FP/Hodge bookkeeping leaves
#   Gamma_std = 1/2 log det' Delta_1,coex - 1/2 log det' Delta_0 + zero/gauge/local.
# To restore the coexact-only C6 branch without declaring a physical transverse quotient, an additional paired
# sector must provide +1/2 log det' Delta_0 for the nonzero even scalar tower, with the same P02 coupling.

candidates = [
    {
        "candidate_sector": "standard_FP_ghost_recount",
        "required_gamma_scalar_power": REQUIRED_GAMMA_SCALAR_POWER,
        "actual_gamma_scalar_power_available": 0.0,
        "spectrum_match": "not_an_extra_sector",
        "sign_match": False,
        "P02_coupling_match": "already_used_to_create_residual",
        "new_parameter": False,
        "status": "fail_double_counting",
        "verdict": (
            "The FP determinant and Hodge exact determinant are already the source of the -1/2 scalar residual. "
            "Reusing the same bookkeeping cannot also supply an independent +1/2 determinant."
        ),
    },
    {
        "candidate_sector": "BRST_Nielsen_Kallosh_like_ghost",
        "required_gamma_scalar_power": REQUIRED_GAMMA_SCALAR_POWER,
        "actual_gamma_scalar_power_available": "absent_for_ordinary_Abelian_Maxwell_Lorenz_gauge",
        "spectrum_match": "would_match_only_if_an_extra_scalar_auxiliary_or_ghost_is_added",
        "sign_match": "possible_only_with_bosonic_auxiliary_half_determinant",
        "P02_coupling_match": "unproven",
        "new_parameter": "new_field_or_gauge_condition",
        "status": "fail_not_in_current_model",
        "verdict": (
            "Nielsen-Kallosh determinants arise in more constrained or nontrivial gauge systems, not as a mandatory extra sector "
            "in the present Abelian one-form determinant. Adding it would be a new model ingredient."
        ),
    },
    {
        "candidate_sector": "longitudinal_exact_Hodge_remnant",
        "required_gamma_scalar_power": REQUIRED_GAMMA_SCALAR_POWER,
        "actual_gamma_scalar_power_available": "already_accounted_as_plus_half_inside_det_Delta1_then_cancelled_by_FP_to_minus_half",
        "spectrum_match": True,
        "sign_match": "wrong_as_independent_cancellation",
        "P02_coupling_match": True,
        "new_parameter": False,
        "status": "fail_no_independent_remnant",
        "verdict": (
            "The exact one-form spectrum is isospectral to nonzero scalars, but it is already included in det' Delta1. "
            "After FP division it leaves -1/2, not an additional +1/2."
        ),
    },
    {
        "candidate_sector": "Ray_Singer_torsion_topological_sector",
        "required_gamma_scalar_power": REQUIRED_GAMMA_SCALAR_POWER,
        "actual_gamma_scalar_power_available": "topological_combination_not_targeted_nonzero_scalar_half_power",
        "spectrum_match": "mixed_p_form_alternating_product_not_scalar_only",
        "sign_match": "depends_on_full_torsion_combination",
        "P02_coupling_match": False,
        "new_parameter": False,
        "status": "fail_not_P02_local_metric_residual",
        "verdict": (
            "Analytic torsion pairs p-form determinants in an alternating topological product. It is not a selective local "
            "P02 trace-square cancellation of the nonzero scalar tower on RP3 x S1."
        ),
    },
    {
        "candidate_sector": "Maxwell_scalar_duality_sector",
        "required_gamma_scalar_power": REQUIRED_GAMMA_SCALAR_POWER,
        "actual_gamma_scalar_power_available": "duality_rewrites_physical_modes_not_adds_modes",
        "spectrum_match": "partial_dimension_dependent_dual_description",
        "sign_match": "not_an_extra_opposite_sign_determinant",
        "P02_coupling_match": "unproven_and_risks_double_counting",
        "new_parameter": False,
        "status": "fail_duality_not_additive",
        "verdict": (
            "Duality can reformulate the physical determinant but does not add an independent compensating determinant "
            "without doubling degrees of freedom."
        ),
    },
    {
        "candidate_sector": "Dirac_spin_cover_sector",
        "required_gamma_scalar_power": REQUIRED_GAMMA_SCALAR_POWER,
        "actual_gamma_scalar_power_available": "fermionic_logdet_with_different_operator_and_multiplicities",
        "spectrum_match": False,
        "sign_match": "fermionic_sign_generically_opposite_but_wrong_spectrum_prefactor",
        "P02_coupling_match": False,
        "new_parameter": "new_spin_matter_content",
        "status": "fail_wrong_spectrum_new_matter",
        "verdict": (
            "A Dirac/spin-cover determinant is not isospectral to the even scalar Laplacian with the required half-power. "
            "It would introduce new matter rather than close the existing C6 proof."
        ),
    },
    {
        "candidate_sector": "physical_transverse_quotient_definition",
        "required_gamma_scalar_power": "avoid_residual_rather_than_cancel_it",
        "actual_gamma_scalar_power_available": "sets_scalar_power_to_zero_by_definition_before_FP_residual_is_introduced",
        "spectrum_match": "not_applicable",
        "sign_match": "not_applicable",
        "P02_coupling_match": "coexact_only",
        "new_parameter": False,
        "status": "viable_conditional_definition_not_paired_sector",
        "verdict": (
            "This remains the clean route if the theory defines the one-loop determinant directly on the transverse/coexact quotient. "
            "It is not an additional paired cancellation sector."
        ),
    },
]

summary_counts = {}
for candidate in candidates:
    summary_counts[candidate["status"]] = summary_counts.get(candidate["status"], 0) + 1

hard_requirements = [
    {
        "requirement": "opposite_nonzero_scalar_half_power",
        "needed": "+1/2 log det' Delta0_nonzero in Gamma",
        "reason": "Only this cancels the standard-FP residual -1/2 log det' Delta0 mode-by-mode.",
    },
    {
        "requirement": "same_even_RP3_x_S1_spectrum",
        "needed": REQUIRED_SPECTRUM,
        "reason": "A local or finite-dimensional factor cannot cancel the nonlocal Bessel/winding tower from ell=2,4,... .",
    },
    {
        "requirement": "same_P02_trace_square",
        "needed": REQUIRED_COUPLING,
        "reason": "Cancellation must occur in the same first-strain P02 channel, not merely in an integrated scalar constant.",
    },
    {
        "requirement": "no_new_tunable_ingredient",
        "needed": "mandatory consequence of existing gauge/topological structure",
        "reason": "Otherwise C6 becomes a model-extension assumption rather than a theorem route.",
    },
]

results = {
    "status": "all_known_paired_candidates_fail_or_are_definitional",
    "numbers": {
        "S_geo": S_GEO,
        "P02_rank": P02_RANK,
        "trace_rank": TRACE_RANK,
        "traceless_rank": TRACELESS_RANK,
        "first_nonzero_even_scalar_ell": FIRST_NONZERO_EVEN_SCALAR_ELL,
        "first_nonzero_even_scalar_multiplicity": FIRST_NONZERO_EVEN_SCALAR_MULT,
        "first_nonzero_even_scalar_lambda_unit_S3": FIRST_NONZERO_EVEN_SCALAR_LAMBDA_S3,
        "required_gamma_scalar_power": REQUIRED_GAMMA_SCALAR_POWER,
    },
    "hard_requirements": hard_requirements,
    "candidate_table": candidates,
    "summary_counts": summary_counts,
    "verdict": (
        "No existing paired/cancellation sector in the current C6 bookkeeping supplies the required independent "
        "+1/2 log det' Delta0_nonzero with the same even RP3 x S1 scalar spectrum and P02 trace-square coupling. "
        "Standard FP and exact Hodge pieces are already exhausted, zero/gauge/Jacobian factors cannot cancel the nonzero tower, "
        "torsion/duality do not provide an additive scalar half-determinant, and Dirac/spin-cover matter has the wrong spectrum. "
        "Thus C6 is not rescued by a known paired sector; the viable non-phenomenological route remains a physical transverse quotient, "
        "or else pi^-4 must stay downgraded until a genuinely new mandatory sector is derived."
    ),
}

Path("s2t_c6_paired_sector_search_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "candidates_checked": len(candidates),
    "blocking_requirement": "+1/2 log det' Delta0_nonzero with same P02 trace-square",
    "surviving_route": "physical_transverse_quotient_or_new_mandatory_sector",
}, indent=2, ensure_ascii=False))