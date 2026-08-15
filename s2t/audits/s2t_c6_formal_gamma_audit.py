import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
VOL_RP3 = math.pi**2
BASE = (VOL_RP3 / 2) * T_RP3 / S_GEO
P02_RANK = 10
P02_TERM = BASE * (1 - P02_RANK / (24 * S_GEO))
N_NEED = 24 * S_GEO * (1 - PI4_TERM / BASE)
GAP = N_NEED - P02_RANK

sectors = [
    {
        "sector": "harmonic_one_forms",
        "space": "H^1(RP3)=0",
        "functional_role": "no continuous one-form zero-mode determinant",
        "status": "closed_by_topology_b1_zero",
    },
    {
        "sector": "coexact_transverse_bosonic",
        "space": "Omega^1_coex(RP3) x periodic S1",
        "functional_role": "+1/2 log det' Delta_1_coex[g]",
        "status": "nonzero_tower_source_and_P02_candidate_insertion",
    },
    {
        "sector": "exact_longitudinal_bosonic",
        "space": "d Omega^0_perp",
        "functional_role": "gauge longitudinal sector paired with scalar ghosts for nonzero scalar modes",
        "status": "must_cancel_before_P02_counting",
    },
    {
        "sector": "scalar_FP_ghost",
        "space": "Omega^0 / constants with det-prime convention plus constant periodic branch",
        "functional_role": "- log det' Delta_0[g]; nonzero branch cancels exact sector; constant periodic branch gives kappa_Cas=1/24",
        "status": "conditional_isolation_required",
    },
    {
        "sector": "zero_modes_and_gauge_volume",
        "space": "constant scalar zero mode and absent b1 harmonic forms",
        "functional_role": "removed by det-prime/gauge volume; m != 0 constant periodic row retained for kappa_Cas",
        "status": "scheme_defined_but_must_be_stated",
    },
]

claims = [
    {
        "claim": "formal_Gamma_Maxwell_ghost_decomposition",
        "status": "written_as_definition",
        "formula": "Gamma=1/2 logdet' Delta_1^coex + Gamma_exact - logdet' Delta_0 + Gamma_zero/gauge + local counterterms",
        "consequence": "This separates coexact, exact, ghost, zero-mode, and local subtraction sectors.",
    },
    {
        "claim": "P02_in_coexact_bosonic_metric_strain",
        "status": "conditional_lemma",
        "formula": "delta_g Delta_1^coex[h_A], h_A from x -> (I+eps A)x, A=A^T; q_A=x^T A x; P02=Sym^2(R4)",
        "consequence": "Rank is 10 and ell>=4 are excluded as higher ambient strains.",
    },
    {
        "claim": "exact_scalar_ghost_cancels_before_P02_counting",
        "status": "required_isolation_lemma_not_fully_proven",
        "formula": "Gamma_exact_nonzero + Gamma_ghost_nonzero = local/gauge-volume terms before finite P02 coexact trace",
        "consequence": "If false, ghost P02 leakage cancels or reverses suppression.",
    },
    {
        "claim": "constant_scalar_branch_only_kappa_Cas",
        "status": "conditional_scheme_statement",
        "formula": "constant m!=0 periodic scalar/ghost row -> kappa_Cas=1/24; true (0,0) zero mode removed by det-prime",
        "consequence": "The scalar constant branch contributes as coefficient 1/24, not as an independent P02 ghost trace-square.",
    },
    {
        "claim": "delta2_Delta_terms_local_or_compensated",
        "status": "open_required_subtraction_lemma",
        "formula": "Tr(Delta^-1 delta_g^2 Delta) in second variation is local/subtracted/canceled",
        "consequence": "If a finite nonlocal term remains, the absorption formula changes.",
    },
    {
        "claim": "gap_N_need_minus_10",
        "status": "downgrade_trigger_unless_derived",
        "formula": f"N_need-10={GAP:.13f}; relative pi4 mismatch={(P02_TERM-PI4_TERM)/PI4_TERM:.6e}",
        "consequence": "Either derive this as a finite scheme/subleading determinant residue or mark pi^-4 absorption as structural compression, not theorem.",
    },
]

results = {
    "status": "formal_Gamma_written_C6_still_conditional",
    "numbers": {
        "S_geo": S_GEO,
        "T_coex_RP3": T_RP3,
        "Vol_RP3_over_2": VOL_RP3 / 2,
        "base_absorption": BASE,
        "P02_rank": P02_RANK,
        "P02_absorption": P02_TERM,
        "pi4_term": PI4_TERM,
        "relative_error_vs_pi4": (P02_TERM - PI4_TERM) / PI4_TERM,
        "N_need": N_NEED,
        "N_need_minus_10": GAP,
    },
    "sectors": sectors,
    "claims": claims,
    "verdict": (
        "A formal Gamma_Maxwell+ghost decomposition can be written and it clarifies the proof obligations. "
        "P02 can be conditionally placed in the coexact bosonic first-strain insertion; exact/scalar cancellation and the 1/24 constant branch must be imposed as isolation lemmas. "
        "C6 is not fully proven because delta^2 Delta locality/compensation and the N_need-10 gap remain open."
    ),
}

Path("s2t_c6_formal_gamma_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "N_need_minus_10": GAP,
    "relative_error_vs_pi4": (P02_TERM - PI4_TERM) / PI4_TERM,
    "open_or_required": [c["claim"] for c in claims if c["status"] not in ("written_as_definition", "conditional_lemma", "conditional_scheme_statement")],
}, indent=2, ensure_ascii=False))