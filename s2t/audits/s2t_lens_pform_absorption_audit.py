import json
import math
from pathlib import Path
from scipy.special import k1

ALPHA_INV = 137.035999177
S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
S_VAC_CURRENT = S_GEO - 1 / (24 * S_GEO) - 1 / (math.pi**4 * S_GEO**2)
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
VOL_RP3 = math.pi**2


def scalar_rp3_modes(ell_max=12):
    rows = []
    for ell in range(ell_max + 1):
        descends = ell % 2 == 0
        degeneracy_s3 = (ell + 1) ** 2
        rows.append({
            "ell": ell,
            "lambda_scalar": ell * (ell + 2),
            "degeneracy_s3": degeneracy_s3,
            "degeneracy_rp3_trivial_flat_branch": degeneracy_s3 if descends else 0,
            "descends_to_RP3": descends,
            "exact_one_form_partner_for_nonzero_scalar": descends and ell > 0,
        })
    return rows


def coexact_rp3_modes(n_max=60):
    rows = []
    for n in range(1, n_max + 1):
        # S^3 transverse/coexact one-form tower in the convention used by the existing S2T audits.
        # The RP^3=L(2,1) antipodal quotient keeps the odd-n branch in this convention.
        degeneracy_s3 = 2 * n * (n + 2)
        keep = n % 2 == 1
        rows.append({
            "n": n,
            "rho": n + 1,
            "lambda_coexact": (n + 1) ** 2,
            "degeneracy_s3": degeneracy_s3,
            "degeneracy_rp3": degeneracy_s3 if keep else 0,
            "descends_to_RP3": keep,
        })
    return rows


def bessel_tail(rho, q_max=2000, tol=1e-20):
    total = 0.0
    used = 0
    for q in range(1, q_max + 1):
        term = k1(2 * math.pi * q * rho) / q
        total += term
        used = q
        if abs(term) < tol:
            break
    return rho * total, used


def coexact_bessel_sum():
    total = 0.0
    first = None
    rows = []
    for row in coexact_rp3_modes():
        tail, q_used = bessel_tail(row["rho"])
        contribution = row["degeneracy_rp3"] * tail
        enriched = {**row, "rho_bessel_tail": tail, "q_used": q_used, "contribution_rp3": contribution}
        rows.append(enriched)
        total += contribution
        if first is None and contribution != 0:
            first = enriched
    return total, first, rows


T_RP3, first_mode, coexact_rows = coexact_bessel_sum()
base_absorption = (VOL_RP3 / 2) * T_RP3 / S_GEO
multiplier_needed = PI4_TERM / base_absorption
epsilon_needed = 1 - multiplier_needed
rank_needed = 24 * S_GEO * epsilon_needed
rank_p02 = 10
rank_p02_multiplier = 1 - rank_p02 / (24 * S_GEO)
rank_p02_absorption = base_absorption * rank_p02_multiplier
rank_p02_abs_error = rank_p02_absorption - PI4_TERM
rank_p02_relative_error = rank_p02_abs_error / PI4_TERM
rank_p02_alpha_error_if_replaces_pi4 = (S_GEO - 1 / (24 * S_GEO) - rank_p02_absorption) - ALPHA_INV

scalar_rows = scalar_rp3_modes()
p02_rows = [row for row in scalar_rows if row["ell"] in (0, 2)]
p02_rank = sum(row["degeneracy_rp3_trivial_flat_branch"] for row in p02_rows)
full_even_rank_through_4 = sum(row["degeneracy_rp3_trivial_flat_branch"] for row in scalar_rows if row["ell"] in (0, 2, 4))

integer_candidates = []
for rank in range(1, 41):
    value = base_absorption * (1 - rank / (24 * S_GEO))
    integer_candidates.append({
        "rank": rank,
        "absorption_value": value,
        "absolute_error_vs_pi4": value - PI4_TERM,
        "relative_error_vs_pi4": (value - PI4_TERM) / PI4_TERM,
    })
integer_candidates.sort(key=lambda row: abs(row["absolute_error_vs_pi4"]))

proof_tests = [
    {
        "test": "external_lens_space_framework",
        "status": "pass_framework_only",
        "reason": "Ikeda--Yamamoto and Lauret/L-M-R make L(2,1) p-form spectra the correct verification class, but they do not by themselves derive the S2T mixed determinant coefficient.",
    },
    {
        "test": "ordinary_hodge_cancellation",
        "status": "fail_as_full_cancellation",
        "reason": "Exact one-forms can pair with nonzero scalar ghosts; coexact transverse modes remain and the first RP3 coexact mode contributes almost the whole Bessel tail.",
    },
    {
        "test": "exact_absorption_identity_with_P02_rank_10",
        "status": "fail_as_exact_identity",
        "reason": "The exact rank required is nonintegral, N_need=%.10f; P02 rank 10 leaves a relative pi^-4 mismatch %.6e." % (rank_needed, rank_p02_relative_error),
    },
    {
        "test": "finite_rank_selection",
        "status": "conditional_pass_inside_S2T_first_strain_axiom",
        "reason": "P02 rank equals dim Sym^2(R^4)=10=1+9, but this selects the first ambient strain channel, not the full scalar/exact tower demanded by a generic metric perturbation.",
    },
    {
        "test": "upgrade_4_to_5",
        "status": "not_yet",
        "reason": "The absorption formula is numerically excellent and structurally natural, but lacks an explicit Maxwell--ghost mixed-trace derivation of the volume factor, sign, det-prime convention, and rank-10 projector.",
    },
]

results = {
    "status": "absorption_scheme_strong_candidate_not_theorem",
    "inputs": {
        "alpha_inv_reference": ALPHA_INV,
        "S_geo": S_GEO,
        "S_vac_current": S_VAC_CURRENT,
        "S_vac_current_error": S_VAC_CURRENT - ALPHA_INV,
        "pi4_term": PI4_TERM,
        "Vol_RP3": VOL_RP3,
    },
    "literature_gate": {
        "checked_anchor_lines": [
            "Ikeda--Yamamoto: spectra of three-dimensional lens spaces.",
            "Lauret / Lauret--Miatello--Rossetti: lens-space p-spectra via congruence lattices.",
            "Nash--O'Connor: determinants of Laplacians on lens spaces.",
            "Schwarz / Ray--Singer: gauge determinant, zero-mode and analytic torsion bookkeeping.",
        ],
        "consequence": "These sources validate the verification framework but do not close the S2T coefficient without an explicit L(2,1) Maxwell--ghost determinant calculation.",
    },
    "rp3_mode_tables": {
        "scalar_first_modes": scalar_rows[:9],
        "coexact_first_modes": coexact_rows[:8],
        "first_surviving_coexact_mode": first_mode,
    },
    "absorption_numbers": {
        "T_coex_RP3": T_RP3,
        "first_surviving_mode_fraction": first_mode["contribution_rp3"] / T_RP3,
        "base_volume_half_absorption": base_absorption,
        "base_relative_overshoot_vs_pi4": (base_absorption - PI4_TERM) / PI4_TERM,
        "epsilon_needed": epsilon_needed,
        "rank_needed": rank_needed,
        "P02_rank_from_scalar_ell_0_2": p02_rank,
        "rank_if_ell_0_2_4_included": full_even_rank_through_4,
        "P02_multiplier": rank_p02_multiplier,
        "P02_absorption_value": rank_p02_absorption,
        "P02_absolute_error_vs_pi4": rank_p02_abs_error,
        "P02_relative_error_vs_pi4": rank_p02_relative_error,
        "alpha_error_if_P02_absorption_replaces_pi4": rank_p02_alpha_error_if_replaces_pi4,
    },
    "best_integer_ranks": integer_candidates[:10],
    "proof_tests": proof_tests,
    "verdict": (
        "Option A remains the best path, but it is not closed. The RP3 coexact tower is nonzero; "
        "the volume-weighted half determinant nearly equals the existing pi^-4 term; the P02/Casimir "
        "rank-10 correction reduces the mismatch to the 3e-6 relative level. However, the rank required "
        "for exact equality is 10.0099700224, not an integer, and no external lens-space determinant formula "
        "checked here derives the S2T rank-10 mixed trace. Therefore Tome II must keep S_vac at conditional "
        "determinant success unless a full L(2,1) Maxwell--ghost mixed-trace derivation is added."
    ),
}

Path("s2t_lens_pform_absorption_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "T_coex_RP3": T_RP3,
    "rank_needed": rank_needed,
    "P02_rank": p02_rank,
    "P02_relative_error_vs_pi4": rank_p02_relative_error,
    "upgrade_4_to_5": "not_yet",
}, indent=2, ensure_ascii=False))