import json
from pathlib import Path


def main():
    coexact = json.loads(Path("s2t_coexact_tower_results.json").read_text())
    winding = json.loads(
        Path("external_rp3xs1_winding_determinant_results.json").read_text()
    )
    paired = json.loads(
        Path("s2t_c6_paired_sector_search_results.json").read_text()
    )
    rank_no_go = json.loads(
        Path("s2t_neutrino_rank_one_selector_no_go_results.json").read_text()
    )
    majorana = json.loads(
        Path("s2t_neutrino_twisted_majorana_defect_results.json").read_text()
    )
    denominator = json.loads(
        Path("s2t_neutrino_global_action_denominator_gate_results.json").read_text()
    )
    parent_action = json.loads(
        Path("s2t_parent_action_normalization_gate_results.json").read_text()
    )

    t_coexact = coexact["dimensionless_positive_sum"]["rp3_projected"]
    gamma_winding = winding["numbers"]["bosonic_Gamma_winding"]

    tests = [
        {
            "test": "hodge_spectral_map",
            "status": "partial_pass_nonzero_modes_only",
            "result": (
                "For a co-closed one-form eigenmode A with lambda>0, "
                "lambda^(-1/2)*star*dA is a co-closed two-form eigenmode with "
                "the same eigenvalue. This supports isospectrality, not cancellation."
            ),
        },
        {
            "test": "isolated_one_form_ghost",
            "status": "fail_incomplete_bv_complex",
            "result": (
                "A bosonic two-form gauge field has a reducible gauge symmetry. Its "
                "one-form Grassmann ghost is accompanied by the two-form determinant "
                "and scalar ghost-for-ghost factors. Keeping only the favorable "
                "one-form determinant is not a BRST-complete partition function."
            ),
            "full_p2_oscillator_factor": (
                "Z_2 proportional to det'(Delta_2^T)^(-1/2) "
                "det'(Delta_1^T)^(+1/2) det'(Delta_0)^(-1/2)"
            ),
        },
        {
            "test": "nielsen_kallosh_identification",
            "status": "fail_not_automatic",
            "result": (
                "The ordinary one-form ghost of a two-form gauge symmetry is not by "
                "itself an extra Nielsen-Kallosh sector. A Nielsen-Kallosh third ghost "
                "depends on the chosen differential gauge-fixing metric and cannot be "
                "inserted as a universal duplicate of the Maxwell coexact tower."
            ),
        },
        {
            "test": "pure_BF_branch",
            "status": "fail_removes_Maxwell_sector",
            "result": (
                "With no kinetic term for B, variation of integral B wedge F_A imposes "
                "F_A=0. The Maxwell transverse tower is constrained away rather than "
                "retained with a compensating ghost determinant."
            ),
        },
        {
            "test": "dynamical_BF_branch",
            "status": "fail_changes_operator_spectrum",
            "result": (
                "Adding a kinetic term for B makes a new propagating vector-tensor "
                "model. BF mixing changes the eigenvalues and can generate a topological "
                "mass, so its determinants are not minus the original massless Maxwell tower."
            ),
        },
        {
            "test": "localized_BF_branch",
            "status": "fail_global_isospectrality_lost",
            "result": (
                "A coupling supported near gamma times S1 introduces defect boundary "
                "conditions and a singular or position-dependent kinetic operator. Its "
                "ghost modes are not the global RP3 coexact harmonics used in T_coex."
            ),
        },
        {
            "test": "flux_statement",
            "status": "fail_form_degree_and_de_rham_torsion",
            "result": (
                "A two-form cannot be integrated over the one-cycle gamma. The natural "
                "surface gamma times S1 represents a Z2 torsion two-cycle in K, while "
                "H2(K;R)=0. A smooth closed real two-form has zero de Rham period on it; "
                "only a discrete gerbe holonomy could detect the torsion class."
            ),
            "homology": {
                "H2_RP3xS1_Z": "Z2",
                "H2_RP3xS1_R": "0",
            },
        },
        {
            "test": "rank_24_to_23",
            "status": "fail_BF_flux_does_not_supply_mod_two_index",
            "result": (
                "Aharonov-Bohm holonomy shifts boundary conditions but does not by "
                "itself remove exactly one real state from R24. The existing audit "
                "needed an odd-winding class-D Majorana mass defect and a mod-two index; "
                "that new mass operator and its embedding remain conditional."
            ),
            "previous_exact_symmetry_status": rank_no_go["status"],
            "existing_conditional_route": majorana["verdict"],
        },
        {
            "test": "rank_23_denominator",
            "status": "fail_rank_alone_not_denominator",
            "result": (
                "Even a consistent rank-23 heavy quotient does not produce a tree-level "
                "denominator 23. Canonical coupling removes the rank; democratic "
                "unnormalized coupling puts it in the numerator."
            ),
            "previous_gate": denominator["verdict"],
        },
        {
            "test": "C6_numeric_object",
            "status": "fail_wrong_functional_identification",
            "result": (
                "The positive K1 sum T_coex is a Casimir-energy kernel. The Euclidean "
                "winding log-determinant is a different function and magnitude. Therefore "
                "writing a ghost contribution equal to -T_coex does not prove cancellation "
                "of the one-loop determinant used in a spectral action."
            ),
            "T_coex": t_coexact,
            "bosonic_Gamma_winding": gamma_winding,
            "absolute_Gamma_over_T": abs(gamma_winding) / t_coexact,
        },
        {
            "test": "local_heat_kernel_preservation",
            "status": "fail_new_field_content_changes_local_coefficients",
            "result": (
                "A new two-form field, its ghost tower, defect support and BF mixing alter "
                "the full heat-kernel and zero-mode bookkeeping. The old 1/24 term cannot "
                "be declared unchanged without recomputing the combined complex."
            ),
        },
    ]

    status_counts = {}
    for test in tests:
        status_counts[test["status"]] = status_counts.get(test["status"], 0) + 1

    results = {
        "status": "BF_NK_proposal_does_not_rescue_C6_or_derive_23",
        "date": "2026-08-04",
        "proposal": (
            "A localized BF two-form sector and its purported one-form "
            "Nielsen-Kallosh ghost cancel the Maxwell coexact tower and create the "
            "neutrino rank-one defect."
        ),
        "previous_audit_overlap": {
            "paired_sector_status": paired["status"],
            "paired_sector_verdict": paired["verdict"],
            "parent_action_status": parent_action["status"],
            "interpretation": (
                "The proposal is a concrete new paired-sector model, but the relevant "
                "sign, spectrum, rank-one and parent-action gates were already isolated "
                "and tested in the previous audit program."
            ),
        },
        "tests": tests,
        "summary_counts": status_counts,
        "scientific_verdict": {
            "positive": (
                "The nonzero Hodge map between one-form and two-form eigenmodes is real, "
                "and a BF/gerbe defect is a legitimate new II.B research direction."
            ),
            "negative": (
                "The claimed exact cancellation isolates one favorable ghost while "
                "discarding the rest of the BV complex, confuses a Casimir kernel with "
                "the Euclidean determinant, and assigns a rank-one fermion index to a "
                "bosonic torsion flux without deriving a Majorana defect operator."
            ),
            "maturity_effect": (
                "No increase from R_sci=4 follows. At best this is a new model extension "
                "that must restart the full same-scheme determinant and parent-action audits."
            ),
            "required_reopening_calculation": [
                "write one globally gauge-invariant bulk/defect action",
                "derive the complete BV complex including ghost-for-ghost fields",
                "compute the full combined heat kernel and winding log determinant",
                "derive a mod-two fermion index from the same action",
                "show the resulting rank enters the collective stiffness denominator",
            ],
        },
    }

    assert t_coexact > 0
    assert abs(abs(gamma_winding) / t_coexact - 1.3741533859178428) < 1e-12
    assert status_counts["partial_pass_nonzero_modes_only"] == 1
    assert len(tests) == 11

    Path("s2t_bf_nielsen_kallosh_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "tests": len(tests),
                "partial_passes": 1,
                "failed_or_unclosed": len(tests) - 1,
                "T_coex": t_coexact,
                "Gamma_winding": gamma_winding,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()