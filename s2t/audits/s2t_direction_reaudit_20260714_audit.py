import json
from pathlib import Path

closure = json.loads(Path("s2t_c6_closure_matrix_results.json").read_text())
svac = json.loads(Path("s2t_tome2_results.json").read_text())
absorption = json.loads(Path("s2t_lens_pform_absorption_results.json").read_text())
casmix = json.loads(Path("s2t_determinant_casmix_results.json").read_text())
n3_scale = json.loads(Path("s2t_c6_l21_n3_obstruction_scale_results.json").read_text())
priority = json.loads(Path("s2t_c6_l21_delta2_trace_phase_priority_results.json").read_text())
c11 = json.loads(Path("s2t_c6_l21_delta2_c11_setup_results.json").read_text())
external = json.loads(Path("external_literature_spectral_determinants_results.json").read_text())

wiki_pages_reviewed = [
    "wiki/syntheses/current-status-and-next-vectors.md",
    "wiki/syntheses/s2t-closure-roadmap.md",
    "wiki/syntheses/tome2-svac-em-block-audit.md",
    "wiki/questions/coexact-tower-delta.md",
    "wiki/questions/kappa-cas-one-over-24.md",
    "wiki/sources/external-literature-spectral-determinants.md",
    "wiki/syntheses/tome2-proof-chain.md",
    "wiki/questions/neutrino-overlap-lemma.md",
    "wiki/questions/ew-qcd-threshold-closure.md",
    "wiki/concepts/spectral-correlational-source.md",
]
material_sources_reviewed = [
    "tome2_s2t_spectral_closure.tex",
    "main.tex",
    "theory_completion_program.tex",
    "research_protocol_toe_ugsm.tex",
    "root-level *_results.json audit layer",
]

continue_signals = [
    {
        "signal": "S_vac numerical and structural spine remains strong",
        "evidence": "s2t_tome2_results closed rows plus wiki status: carrier geometry, S_geo, kappa branch, P02 rank, pi^2/2 prefactor, and sign direction remain positive inputs",
        "meaning": "do not abandon the program as numerology yet",
    },
    {
        "signal": "rank-10 trace lead is nontrivial",
        "evidence": casmix["verdict"],
        "meaning": "the N≈10 result is a real clue, but not proof",
    },
    {
        "signal": "absorption route is best known route",
        "evidence": absorption["status"],
        "meaning": "if C6 is pursued, pursue it as full operator/absorption, not independent correction",
    },
    {
        "signal": "problem is localized rather than diffuse",
        "evidence": f"closure matrix has {len(closure['closure_matrix'])} nodes with explicit blockers and trace priorities",
        "meaning": "a short focused C6 sprint can still falsify or rescue the path efficiently",
    },
]

switch_signals = [
    {
        "signal": "n=3 obstruction is large",
        "evidence": n3_scale["verdict"],
        "meaning": "do not expect a tiny scheme-gap explanation",
    },
    {
        "signal": "known paired sectors failed",
        "evidence": "paired-sector search and wiki pages reject ready-made Maxwell--ghost--Dirac pairing or scalar inheritance as closure",
        "meaning": "a rescue probably needs full operator cancellation or a genuinely new mandatory sector",
    },
    {
        "signal": "local counterterms cannot erase finite low-shell data",
        "evidence": "local-counterterm classifier and n3 finite-counterterm gate forbid post-hoc finite subtraction",
        "meaning": "no cheap subtraction escape remains",
    },
    {
        "signal": "trace phase is not yet computation",
        "evidence": f"{priority['status']}; {c11['status']}",
        "meaning": "continued C6 work is costly unless it attacks actual missing operator pieces",
    },
]

candidate_vectors = [
    {
        "vector": "A_C6_timeboxed_operator_sprint",
        "recommendation": "continue, but only with a stop condition",
        "next_test": "expand one missing delta2/full-operator piece enough to produce a real C11 contribution or prove same-scheme compensation/locality",
        "stop_if": "after the next concrete operator expansion there is still no route to C11/C33 values or cancellation mechanism",
        "expected_value": "highest upside for mature S_vac theorem, highest difficulty",
    },
    {
        "vector": "B_external_literature_gate",
        "recommendation": "run in parallel or as fallback",
        "next_test": "check lens-space p-form / Maxwell determinant formulas against the S2T quotient/coexact normalization and P02 trace claim",
        "stop_if": "external formula forces additional same-order shells or gauge-choice dependence",
        "expected_value": "can validate/demote C6 faster than doing all matrices",
    },
    {
        "vector": "C_neutrino_overlap_lemma",
        "recommendation": "good switch target if C6 stalls",
        "next_test": "derive or reject N_nu^2 = pi + pi^-1 from Dirac/spin/gauge overlap space",
        "stop_if": "identity requires a fitted residual rather than a defined inner product",
        "expected_value": "smaller proof surface than C6; can strengthen an independent II.B row",
    },
    {
        "vector": "D_EW_QCD_threshold_solver",
        "recommendation": "secondary switch target, not immediate rescue",
        "next_test": "build explicit threshold-spectrum solver with one/two-loop comparison",
        "stop_if": "requires hidden mass/scale fitting",
        "expected_value": "important for maturity, but likely broader than neutrino lemma",
    },
]

results = {
    "status": "direction_reaudit_continue_C6_timeboxed_with_parallel_fallbacks",
    "date": "2026-07-14",
    "wiki_pages_reviewed": wiki_pages_reviewed,
    "material_sources_reviewed": material_sources_reviewed,
    "current_dashboard": {
        "C6_nodes": len(closure["closure_matrix"]),
        "blocking_or_failed_nodes": sum("fail" in row["status"] or "blocking" in row["status"] for row in closure["closure_matrix"]),
        "primary_blocker": "full_one_form_operator_rescue_after_nonzero_n3_projection",
        "note": "Current disk state is 37-node matrix with C11 setup present; C33 package is not present in the checked workspace state.",
    },
    "continue_signals": continue_signals,
    "switch_signals": switch_signals,
    "candidate_vectors": candidate_vectors,
    "decision": {
        "primary_recommendation": "do_not_fully_switch_yet",
        "operational_rule": "give C6 one timeboxed operator sprint focused on actual C11/C33-enabling formulas, while preparing external literature and neutrino fallback tracks",
        "why": "The evidence is too structured to abandon, but the n=3 obstruction and missing delta2/full-operator pieces are too serious to keep doing only scoping work.",
        "plain_language": "Keep digging this mine, but set a rope and an exit. One more real shaft toward numbers; if we hit only more fog, move part of the crew to neutrino/external gates.",
    },
    "verdict": "The wiki/material re-audit supports continuing in the current direction only as a timeboxed, computation-facing C6 sprint. The program should not switch away wholesale because S_vac, P02 rank 10, kappa_Cas, volume/sign structure, and localization of the blocker remain strong. But it should stop adding C6 labels without numbers: the n=3 obstruction is large, local/paired escapes failed, and C_delta2 values or same-scheme compensation are required. Best strategy: one focused C6 operator sprint, plus parallel external-literature check and a prepared fallback to the neutrino overlap lemma if C6 remains blocked.",
}

Path("s2t_direction_reaudit_20260714_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "primary_recommendation": results["decision"]["primary_recommendation"],
    "operational_rule": results["decision"]["operational_rule"],
    "C6_nodes": results["current_dashboard"]["C6_nodes"],
    "blocking_or_failed_nodes": results["current_dashboard"]["blocking_or_failed_nodes"],
}, indent=2, ensure_ascii=False))