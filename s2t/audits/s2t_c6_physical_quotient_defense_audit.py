import json
from pathlib import Path

# This audit tests the last clean non-phenomenological route left by the C6 closure matrix:
# define the EM determinant directly on the physical transverse/coexact quotient rather than
# deriving C6 from bare standard covariant FP after a scalar residual has already appeared.

criteria = [
    {
        "criterion": "configuration_space_definition",
        "requirement": "The one-loop EM determinant must be defined on gauge equivalence classes A/G, represented by coexact transverse one-forms.",
        "status": "viable_as_definition",
        "risk": "must be stated before C6 is evaluated, not introduced after scalar leakage is found",
    },
    {
        "criterion": "hodge_slice_validity",
        "requirement": "On RP3 the harmonic one-form sector is absent for b1=0, so the coexact slice is a clean representative of physical transverse modes up to zero/gauge factors.",
        "status": "structurally_supported",
        "risk": "full RP3 x S1 product may still carry circle/global zero-mode bookkeeping that must remain outside P02 trace-square",
    },
    {
        "criterion": "fp_equivalence_or_declared_scheme",
        "requirement": "Either prove equivalence to covariant FP including Hodge measure, ghost determinant, det-prime and gauge volume, or declare the quotient determinant as the defining II.A scheme.",
        "status": "open_theorem_obligation",
        "risk": "without this, quotient route is a normalization choice rather than a theorem derived from standard FP",
    },
    {
        "criterion": "kappa_branch_separation",
        "requirement": "The retained scalar periodic coefficient kappa_Cas=1/24 must remain a zero/IR branch and not a nonzero scalar P02 trace-square insertion.",
        "status": "partially_supported_by_constant_branch_audit",
        "risk": "trace/volume direction still needs explicit normalization statement",
    },
    {
        "criterion": "nonzero_scalar_absence",
        "requirement": "The nonzero scalar half-determinant residual from standard FP must be absent by definition of the quotient, not cancelled by a hidden extra sector.",
        "status": "viable_only_if_quotient_is_primary",
        "risk": "if standard FP is treated as primary, the residual returns and C6 remains blocked",
    },
    {
        "criterion": "external_literature_gate",
        "requirement": "External determinant literature must allow a physical transverse determinant or explicitly relate it to the gauge-fixed determinant with zero/gauge/torsion factors separated.",
        "status": "needs_external_writeup",
        "risk": "if literature requires the full covariant FP scalar residual in the same finite metric variation, quotient route fails as theorem",
    },
    {
        "criterion": "no_new_parameter",
        "requirement": "The quotient cannot introduce a tunable coefficient; it only changes the domain of the determinant to physical coexact modes.",
        "status": "passes_if_declared_geometric_domain",
        "risk": "any extra weight assigned to quotient vs FP is hidden fitting",
    },
]

route_comparison = [
    {
        "route": "standard_covariant_FP_primary",
        "scalar_nonzero_residual": "present_unless_cancellation_proven",
        "C6_status": "blocked",
        "manager_verdict": "do_not_invest_more_without_new_identity",
    },
    {
        "route": "physical_transverse_quotient_primary",
        "scalar_nonzero_residual": "absent_by_domain_definition",
        "C6_status": "viable_conditional",
        "manager_verdict": "best_next_research_route",
    },
    {
        "route": "new_paired_sector",
        "scalar_nonzero_residual": "cancelled_only_if_mandatory_same_spectrum_opposite_power",
        "C6_status": "not_found",
        "manager_verdict": "park_until_new_BRS_topological_EFT_reason_appears",
    },
    {
        "route": "phenomenological_compression",
        "scalar_nonzero_residual": "not_resolved",
        "C6_status": "honest_downgrade",
        "manager_verdict": "acceptable_fallback_not_theorem",
    },
]

definition_obligations = [
    {
        "obligation": "state_primary_domain",
        "text_to_add": "Define Gamma_EM^phys[g] = 1/2 log det' Delta_1,coex + Gamma_zero/gauge + Gamma_loc.ct. as the II.A physical determinant, not as a late cancellation.",
    },
    {
        "obligation": "separate_kappa_Cas",
        "text_to_add": "Treat kappa_Cas=1/24 as the periodic scalar/IR branch after det-prime zero removal, external to finite P02 trace-square.",
    },
    {
        "obligation": "external_gate_condition",
        "text_to_add": "Require literature-compatible equivalence between physical transverse determinant and gauge-fixed Maxwell partition function modulo local, zero-mode and gauge-volume factors.",
    },
    {
        "obligation": "failure_condition",
        "text_to_add": "If the external gate forces a nonzero scalar residual into the same finite P02 second variation, the quotient defense fails and pi^-4 is downgraded.",
    },
]

results = {
    "status": "physical_transverse_quotient_viable_but_requires_primary_definition_and_external_gate",
    "criteria": criteria,
    "route_comparison": route_comparison,
    "definition_obligations": definition_obligations,
    "recommended_next_text_change": "Update the 4->5 threshold and C6 status language: mixed-trace derivation, primary physical quotient, or mandatory paired sector; otherwise downgrade pi^-4.",
    "verdict": (
        "The physical transverse/coexact quotient is the best remaining non-phenomenological C6 route, but only if it is made primary. "
        "It cannot be advertised as a derived cancellation of the standard covariant FP scalar residual unless the full FP/Hodge/gauge-volume equivalence is proven. "
        "As a primary determinant domain, it removes nonzero scalar P02 leakage by construction, preserves the coexact bosonic sign, and keeps kappa_Cas=1/24 as a separate IR/zero branch. "
        "The remaining obligation is the external spectral-determinant gate: show that this physical determinant is literature-compatible modulo local, zero-mode and gauge-volume factors."
    ),
}

Path("s2t_c6_physical_quotient_defense_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "criteria_checked": len(criteria),
    "best_route": "physical_transverse_quotient_primary",
    "blocking_condition": "external_gate_forces_nonzero_scalar_P02_residual",
}, indent=2, ensure_ascii=False))