import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
BASE_ABSORPTION = (math.pi**2 / 2) * T_RP3 / S_GEO
N_NEED = 24 * S_GEO * (1 - PI4_TERM / BASE_ABSORPTION)
P02_RANK = 10
P02_TERM = BASE_ABSORPTION * (1 - P02_RANK / (24 * S_GEO))

conditions = [
    {
        "id": "C1_lens_pform_framework",
        "question": "Are L(2,1)=RP3 p-form spectra the correct external reference class?",
        "status": "pass",
        "evidence": "Ikeda--Yamamoto and Lauret/L-M-R provide the lens-space p-spectrum framework; internal RP3 parity tables are compatible as a working convention.",
        "blocks_theorem": False,
    },
    {
        "id": "C2_coexact_tower_nonzero",
        "question": "Does ordinary Maxwell--ghost/Hodge bookkeeping erase the transverse coexact tower?",
        "status": "fail_for_cancellation",
        "evidence": "Exact/scalar ghosts pair longitudinal modes; coexact transverse modes remain. T_coex^RP3 is nonzero and dominated by the first surviving mode.",
        "blocks_theorem": False,
    },
    {
        "id": "C3_volume_half_normalization",
        "question": "Is the natural bosonic volume-half factor pi^2/2 close to the pi^-4 term?",
        "status": "pass_numerically_not_derived",
        "evidence": "Base absorption overshoots pi^-4 by 0.3053%; the factors 1/2 and Vol(RP3)=pi^2 are natural but not yet derived from the full determinant.",
        "blocks_theorem": True,
    },
    {
        "id": "C4_p02_rank_selection",
        "question": "Is rank 10 derived without a shell cutoff?",
        "status": "conditional_pass_inside_first_ambient_strain",
        "evidence": "Sym^2(R4) has rank 10 and decomposes as ell=0 plus ell=2. This excludes ell>=4 only if the mixed perturbation is the first ambient strain channel.",
        "blocks_theorem": True,
    },
    {
        "id": "C5_exact_rank_identity",
        "question": "Does the absorption formula equal pi^-4 exactly with rank 10?",
        "status": "fail_exact_identity",
        "evidence": f"The exact required rank is {N_NEED:.10f}; rank 10 leaves relative mismatch {(P02_TERM-PI4_TERM)/PI4_TERM:.6e}.",
        "blocks_theorem": True,
    },
    {
        "id": "C6_mixed_trace_operator",
        "question": "Has the gauge-fixed Maxwell--ghost mixed trace been explicitly computed with sign, det-prime and zero modes?",
        "status": "open_core_gap",
        "evidence": "Existing scripts identify the finite-strain candidate; they do not compute the full operator trace from first principles.",
        "blocks_theorem": True,
    },
]

routes = [
    {
        "route": "A_absorption",
        "current_status": "strong_candidate",
        "upgrade_condition": "Compute the L(2,1)xS1 Maxwell--ghost mixed trace and derive pi^2/2, the negative second-order sign, det-prime zero-mode convention, and P02 rank 10.",
        "failure_condition": "If the trace demands the full even scalar/exact tower or rank 10.009970... cannot be interpreted as a finite scheme residue, downgrade pi^-4 to phenomenological compression.",
    },
    {
        "route": "B_new_paired_sector",
        "current_status": "not_found",
        "upgrade_condition": "Find a symmetry or determinant sector with the coexact rho=n+1 tower and opposite signed multiplicity without fitted coefficient.",
        "failure_condition": "Dirac/spin-cover and ordinary exact/scalar ghosts do not satisfy this condition.",
    },
    {
        "route": "C_independent_delta",
        "current_status": "disfavored",
        "upgrade_condition": "Derive a sign and normalization that improves rather than worsens alpha^-1 and is not fitted.",
        "failure_condition": "Simple normalizations worsen the current error by about 15x to 156x.",
    },
    {
        "route": "D_downgrade",
        "current_status": "safe_fallback",
        "upgrade_condition": "Not an upgrade route; it preserves scientific honesty by marking pi^-4 as compression.",
        "failure_condition": "Use if A and B fail.",
    },
]

results = {
    "status": "mixed_trace_closure_matrix_A_not_closed",
    "numbers": {
        "S_geo": S_GEO,
        "T_coex_RP3": T_RP3,
        "pi4_term": PI4_TERM,
        "base_absorption_pi2_over_2_T_over_S": BASE_ABSORPTION,
        "base_overshoot_relative": (BASE_ABSORPTION - PI4_TERM) / PI4_TERM,
        "N_need": N_NEED,
        "P02_rank": P02_RANK,
        "P02_term": P02_TERM,
        "P02_relative_error_vs_pi4": (P02_TERM - PI4_TERM) / PI4_TERM,
    },
    "conditions": conditions,
    "routes": routes,
    "first_blocking_gap": "C6_mixed_trace_operator",
    "decision": "Continue with route A only if the next work is an explicit operator trace, not another numerical fit. Otherwise preserve conditional S_vac and prepare route D wording.",
}

Path("s2t_mixed_trace_closure_matrix_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "first_blocking_gap": results["first_blocking_gap"],
    "N_need": N_NEED,
    "P02_relative_error_vs_pi4": (P02_TERM - PI4_TERM) / PI4_TERM,
    "decision": results["decision"],
}, indent=2, ensure_ascii=False))