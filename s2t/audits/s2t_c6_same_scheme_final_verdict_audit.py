import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text())


ricci = load("s2t_c6_l21_delta2_ricci_C11_gauss_results.json")
scalar_fp = load("s2t_c6_scalar_fp_bookkeeping_results.json")
scalar_rescue = load("s2t_c6_scalar_rescue_routes_results.json")
paired = load("s2t_c6_paired_sector_search_results.json")
physical = load("s2t_c6_physical_quotient_defense_results.json")
finite_counterterm = load("s2t_c6_l21_n3_finite_counterterm_gate_results.json")
locality = load("s2t_c6_l21_coexact_locality_gate_results.json")
projector = load("s2t_c6_projector_t5_quotient_contraction_results.json")
hilbert = load("s2t_c6_hilbert_similarity_invariance_results.json")


tests = [
    {
        "sector": "geometric_second_variation",
        "requirement": "principal, connection and Ricci blocks cancel in the same C11 table",
        "observed": {
            "combined_zero_pair_count": len(ricci["combined_table"]["zero_pairs"]),
            "combined_rank_distribution": ricci["combined_table"]["rank_distribution"],
        },
        "status": "fail_no_cancellation",
    },
    {
        "sector": "coexact_projector",
        "requirement": "projector transport supplies an opposite finite determinant contribution",
        "observed": {
            "direct_T5_rank": projector["T5_table"]["numeric_rank_at_1e_10"],
            "structural_reason": projector["conventions"]["structural_identity"],
        },
        "status": "neutral_exact_coexact_orthogonality",
    },
    {
        "sector": "hilbert_basis_transport",
        "requirement": "basis transport changes the log-determinant Hessian",
        "observed": {
            "raw_logdet_hessian": hilbert["trace_terms"]["raw_logdet_hessian"],
            "selfadjoint_logdet_hessian": hilbert["trace_terms"]["selfadjoint_logdet_hessian"],
            "difference": hilbert["trace_terms"]["hessian_difference"],
        },
        "status": "neutral_similarity_invariance",
    },
    {
        "sector": "standard_covariant_FP_scalar",
        "requirement": "exact and ghost factors cancel the nonzero scalar tower",
        "observed": scalar_fp["schemes"],
        "status": "fail_scalar_half_determinant_remains",
    },
    {
        "sector": "det_prime_zero_gauge_jacobian",
        "requirement": "zero-mode and gauge factors provide an opposite nonzero scalar tower",
        "observed": scalar_rescue["rescue_jacobian_tests"],
        "status": "fail_only_zero_or_power_bookkeeping",
    },
    {
        "sector": "local_counterterms",
        "requirement": "a pre-fixed local subtraction removes the finite low-shell obstruction",
        "observed": {
            "finite_gate": finite_counterterm["status"],
            "coexact_locality_gate": locality["status"],
        },
        "status": "fail_finite_global_spectral_data_not_local",
    },
    {
        "sector": "mandatory_paired_sector",
        "requirement": "an existing mandatory sector has the same spectrum and opposite determinant power",
        "observed": paired["status"],
        "status": "fail_no_known_mandatory_pair",
    },
    {
        "sector": "physical_transverse_quotient",
        "requirement": "the quotient is derived as a same-scheme cancellation rather than selected as a primary domain",
        "observed": physical["status"],
        "status": "conditional_definition_not_compensation",
    },
]


assert tests[0]["observed"]["combined_zero_pair_count"] == 0
assert tests[1]["observed"]["direct_T5_rank"] == 0
assert abs(tests[2]["observed"]["difference"]) < 1e-6
assert abs(hilbert["finite_difference_checks"]["finite_difference_hessian_difference"]) < 1e-12
assert scalar_fp["status"] == "standard_covariant_FP_leaves_scalar_half_power_unless_cancelled"
assert scalar_rescue["status"] == "standard_FP_rescue_routes_not_closed"
assert finite_counterterm["status"] == "n3_finite_low_shell_trace_not_rescuable_by_local_counterterm"
assert paired["status"] == "all_known_paired_candidates_fail_or_are_definitional"


results = {
    "status": "C6_exact_pi4_absorption_downgraded_no_mandatory_same_scheme_compensation",
    "decision_rule": (
        "A rescue counts only if it is mandatory in the already declared Maxwell-ghost scheme, acts on the same "
        "nonzero finite spectral block, and introduces no fitted finite counterterm or late determinant-domain choice."
    ),
    "tests": tests,
    "summary_counts": {
        "failed_rescue_classes": 5,
        "neutral_transport_classes": 2,
        "conditional_definitional_classes": 1,
        "mandatory_compensation_found": 0,
    },
    "theory_effect": {
        "exact_pi4_determinant_theorem": "downgraded_to_structural_compression",
        "S_vac": "remains_conditional_and_must_not_be_used_as_closed_input",
        "independent_results": "S_geo_tau_and_Higgs_EFT_are_unchanged",
        "scientific_value": "increases_because_the_failed_rescue_is_now_explicit_and_falsifiable",
    },
    "reopen_conditions": [
        "derive a new mandatory same-spectrum opposite-sign sector from BRST, topology or EFT",
        "derive an exact no-fit spectral identity that absorbs the finite C11 and low-shell blocks",
        "prove external equivalence of a primary physical quotient together with cancellation of its remaining coexact geometric block",
    ],
    "next_plan": [
        "freeze the exact pi^-4 claim at structural-compression status",
        "prepare a compact reproducibility table claim-to-evidence-to-failure-mode",
        "move the main proof effort to the neutrino overlap lemma",
        "keep the external lens-space determinant gate as an independent reopening test",
        "return to C6 only when a genuinely new identity or mandatory sector appears",
    ],
    "verdict": (
        "No mandatory same-scheme Maxwell-ghost compensation is present in the audited model. The geometric C11 "
        "block remains nonzero; projector and Hilbert transport are determinant-neutral; standard FP leaves a "
        "nonzero scalar half-determinant; det-prime, zero/gauge and Jacobian factors do not cancel the nonzero tower; "
        "local counterterms cannot erase finite low-shell spectral data; and no mandatory paired sector is known. "
        "Therefore exact pi^-4 absorption is not a theorem of the current construction and is downgraded to strong "
        "structural compression. This closes the present C6 rescue branch negatively, not the whole research program."
    ),
}


Path("s2t_c6_same_scheme_final_verdict_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(json.dumps(results["summary_counts"], indent=2, ensure_ascii=False))
print(results["status"])