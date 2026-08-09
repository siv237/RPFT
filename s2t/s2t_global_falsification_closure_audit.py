import json
from pathlib import Path


def claim(
    name,
    claim_type,
    mathematically_valid,
    empirical_observable,
    operator_fixed,
    measure_fixed,
    prospective_blind,
    unified_parent,
    external_reproduction,
    verdict,
    reason,
):
    closed_physical_prediction = all(
        [
            mathematically_valid,
            empirical_observable,
            operator_fixed,
            measure_fixed,
            prospective_blind,
            unified_parent,
        ]
    )
    return {
        "claim": name,
        "type": claim_type,
        "mathematically_valid_in_declared_model": mathematically_valid,
        "empirical_observable": empirical_observable,
        "operator_fixed_before_comparison": operator_fixed,
        "measure_fixed_before_comparison": measure_fixed,
        "demonstrably_prospective_blind": prospective_blind,
        "generated_by_surviving_unified_parent": unified_parent,
        "externally_reproduced_where_applicable": external_reproduction,
        "closed_physical_prediction": closed_physical_prediction,
        "verdict": verdict,
        "reason": reason,
    }


def main():
    claims = [
        claim(
            "K=RP3 x S1 selected in the minimal carrier class",
            "conditional_geometry_theorem",
            True,
            False,
            True,
            True,
            False,
            False,
            True,
            "mathematical_model_choice_not_physical_prediction",
            (
                "The uniqueness statement follows only after imposing the target conditions "
                "Vol(RP3)=pi^2 and phase step pi. It is valid inside that restricted class, "
                "but it does not independently show that nature chooses the carrier."
            ),
        ),
        claim(
            "RP3 scalar and coexact spectra and scalar determinant",
            "reproduced_known_mathematics",
            True,
            False,
            True,
            True,
            True,
            False,
            True,
            "positive_mathematical_validation_not_new_physics",
            (
                "The external reproduction validates the implementation of known lens-space "
                "spectral mathematics. It is not an empirical prediction of S2T."
            ),
        ),
        claim(
            "S_geo=4pi^3+pi^2+pi",
            "geometric_compression",
            True,
            False,
            True,
            True,
            False,
            False,
            False,
            "defined_geometric_scalar_without_observable_map",
            (
                "The combination is reproducible from declared volumes and holonomy, but no "
                "independent action maps it to a measured observable. Alpha inverse is a train input."
            ),
        ),
        claim(
            "periodic one-dimensional determinant coefficient 1/24",
            "standard_finite_branch",
            True,
            False,
            True,
            True,
            True,
            False,
            True,
            "valid_local_branch_not_full_electromagnetic_theorem",
            (
                "The branch coefficient is standard, but its assembly into S_vac is not derived "
                "from the full Maxwell-ghost determinant."
            ),
        ),
        claim(
            "exact S_vac reproduction of alpha inverse",
            "train_anchor_reproduction",
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            "not_a_blind_prediction",
            (
                "Alpha inverse is explicitly in the training set and the exact pi^-4 closure "
                "failed the same-scheme determinant audit."
            ),
        ),
        claim(
            "tau mass relation",
            "conditional_numerical_relation",
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            "strong_postdictive_pattern_not_derived_prediction",
            (
                "The low-complexity relation is numerically nontrivial, but rho0 is assumed, "
                "the compact loop does not yield 1/3 canonically, and no prospective preregistration exists."
            ),
        ),
        claim(
            "Higgs lambda and absolute mass bridge",
            "conditional_scalar_ansatz",
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            "not_independent_and_zero_matching_fails",
            (
                "Lambda_H is introduced by a chosen averaging formula, while v and M_H inherit "
                "tau and S_vac. The independent G_F zero-matching test fails by 0.184 percent."
            ),
        ),
        claim(
            "Qcycle=diag(pi,pi^-1) and norm pi+pi^-1",
            "geometric_gram_identity",
            True,
            False,
            True,
            True,
            True,
            False,
            False,
            "valid_identity_without_physical_vertex_derivation",
            (
                "The reciprocal Gram norm follows from the selected integral normalization, but "
                "the physical Dirac vertex using it is not derived from the unified action."
            ),
        ),
        claim(
            "one real Majorana core zero line",
            "conditional_defect_theorem",
            True,
            False,
            True,
            True,
            True,
            False,
            False,
            "theorem_inside_added_defect_model",
            (
                "Core gluing is consistent once the square-root-torsion defect is declared, but "
                "the defect is additional structure not forced by the parent S2T action."
            ),
        ),
        claim(
            "neutrino collective norm 23+pi^-1",
            "conditional_configuration_metric_identity",
            True,
            False,
            True,
            True,
            True,
            False,
            False,
            "valid_submodel_normalization_not_unified_prediction",
            (
                "The norm is exact in the canonical affine configuration metric, but generic "
                "spectral kernels split the weights and the same parent metric fails the tau sector."
            ),
        ),
        claim(
            "neutrino mass splittings",
            "conditional_phenomenology",
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            "not_closed_empirical_predictions",
            (
                "The absolute Dirac insertion and unified action are open, so agreement of the "
                "splittings has low evidential weight."
            ),
        ),
        claim(
            "EW and QCD low-energy observables",
            "failed_empirical_sector",
            False,
            True,
            True,
            True,
            True,
            False,
            False,
            "closed_negatively_for_minimal_realization",
            (
                "G_F, sin^2 theta_W, alpha_s, M_W and M_Z fail the frozen scorecard; correct-sign "
                "running and the minimal finite-threshold cone do not repair them."
            ),
        ),
    ]

    mathematical_content = [
        row["claim"] for row in claims if row["mathematically_valid_in_declared_model"]
    ]
    empirical_claims = [row for row in claims if row["empirical_observable"]]
    closed_predictions = [row for row in claims if row["closed_physical_prediction"]]
    conditional_or_failed_empirical = [
        row["claim"]
        for row in empirical_claims
        if not row["closed_physical_prediction"]
    ]

    results = {
        "status": "current_s2t_IIA_closed_negatively_as_unified_predictive_physical_theory_mathematical_content_nonempty",
        "date": "2026-08-04",
        "audit_rule": (
            "A surviving physical prediction must be an empirical observable with a fixed operator, "
            "fixed measure, demonstrably prospective blind status, and derivation from the surviving "
            "unified parent action."
        ),
        "claims": claims,
        "counts": {
            "total_claims": len(claims),
            "mathematically_valid_in_declared_models": len(mathematical_content),
            "empirical_claims": len(empirical_claims),
            "closed_independent_physical_predictions": len(closed_predictions),
            "conditional_or_failed_empirical_claims": len(
                conditional_or_failed_empirical
            ),
        },
        "closed_independent_physical_predictions": [
            row["claim"] for row in closed_predictions
        ],
        "surviving_mathematical_content": mathematical_content,
        "conditional_or_failed_empirical_claims": conditional_or_failed_empirical,
        "global_verdict": {
            "current_version_IIA": (
                "Reject as a closed unified predictive physical theory: it has zero surviving "
                "closed independent empirical predictions under the frozen evidence rule."
            ),
            "minimal_realization": (
                "Falsified/closed negatively in its gauge sector and unified-normalization gate."
            ),
            "broader_ontology": (
                "Not falsified because it is not a unique quantitative theory; it remains a "
                "geometric-philosophical research hypothesis."
            ),
            "mathematical_value": (
                "Nonempty: carrier bookkeeping, reproduced lens-space spectra, Gram identities, "
                "conditional defect theorems and several no-go results remain valid mathematics."
            ),
            "stop_rule": (
                "Do not pursue further phenomenological numerology. Reopen physical status only "
                "after a preregistered parent action yields two independent observables."
            ),
        },
    }

    assert results["counts"]["total_claims"] == 12
    assert results["counts"]["closed_independent_physical_predictions"] == 0
    assert results["counts"]["empirical_claims"] == 5
    assert len(results["surviving_mathematical_content"]) > 0

    Path("s2t_global_falsification_closure_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "counts": results["counts"],
                "global_verdict": results["global_verdict"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()