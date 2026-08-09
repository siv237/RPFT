import json
import math
from pathlib import Path
from scipy.special import k1

ALPHA_INV = 137.035999177
S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
S_VAC_CURRENT = S_GEO - 1 / (24 * S_GEO) - 1 / (math.pi**4 * S_GEO**2)
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
VOL_RP3 = math.pi**2


def coexact_modes(n_max):
    for n in range(1, n_max + 1):
        degeneracy_s3 = 2 * n * (n + 2)
        keep_rp3 = n % 2 == 1
        yield {
            "n": n,
            "rho": n + 1,
            "lambda": (n + 1) ** 2,
            "degeneracy_s3": degeneracy_s3,
            "degeneracy_rp3": degeneracy_s3 if keep_rp3 else 0,
            "rp3_kept": keep_rp3,
        }


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


def tower(n_max=120):
    rows = []
    total_s3 = 0.0
    total_rp3 = 0.0
    for mode in coexact_modes(n_max):
        tail, q_used = bessel_tail(mode["rho"])
        c_s3 = mode["degeneracy_s3"] * tail
        c_rp3 = mode["degeneracy_rp3"] * tail
        rows.append({**mode, "rho_bessel_tail": tail, "q_used": q_used, "contribution_s3": c_s3, "contribution_rp3": c_rp3})
        total_s3 += c_s3
        total_rp3 += c_rp3
    return rows, total_s3, total_rp3

rows, T_S3, T_RP3 = tower()

normalizations = [
    ("raw_T_over_S", T_RP3 / S_GEO),
    ("half_raw_T_over_S", 0.5 * T_RP3 / S_GEO),
    ("volume_weighted_half", (VOL_RP3 / 2) * T_RP3 / S_GEO),
    ("volume_weighted_full", VOL_RP3 * T_RP3 / S_GEO),
    ("pi2_over_2_casmix_P02", (VOL_RP3 / 2) * T_RP3 / S_GEO * (1 - 10 / (24 * S_GEO))),
]

variants = []
for name, delta_abs in normalizations:
    for sign_name, sign in [("subtract", -1), ("add", 1)]:
        s_vac = S_VAC_CURRENT + sign * delta_abs
        variants.append({
            "normalization": name,
            "sign": sign_name,
            "Delta_abs": delta_abs,
            "Delta_over_pi4_term": delta_abs / PI4_TERM,
            "S_vac_with_delta": s_vac,
            "error_vs_alpha_inv": s_vac - ALPHA_INV,
            "abs_error_vs_alpha_inv": abs(s_vac - ALPHA_INV),
            "error_ratio_vs_current": abs(s_vac - ALPHA_INV) / abs(S_VAC_CURRENT - ALPHA_INV),
        })
variants = sorted(variants, key=lambda row: row["abs_error_vs_alpha_inv"])

paired_candidates = [
    {
        "candidate": "Hodge_exact_scalar_ghost",
        "status": "does_not_cancel_coexact",
        "reason": "Exact one-forms pair with scalar ghost sectors, but coexact transverse modes remain physical Maxwell modes."
    },
    {
        "candidate": "RP3_even_odd_projection",
        "status": "insufficient",
        "reason": "The quotient removes even n coexact levels, but the dominant n=1 level survives; T_RP3/T_S3≈0.994."
    },
    {
        "candidate": "Dirac_or_spin_cover_pairing",
        "status": "not_available_in_EM_determinant",
        "reason": "A fermionic determinant can affect full QED scale anomalies, but it is not a gauge-invariant cancellation of the pure Maxwell coexact Bessel tail without a derived supersymmetric/BRST pairing."
    },
    {
        "candidate": "first_ambient_strain_P02",
        "status": "explains_pi4_residue_not_full_tower_cancellation",
        "reason": "P02 explains the finite-rank mixed pi^-4 residue, but does not remove the ordinary transverse coexact tower unless the tower is reinterpreted as already summarized by that mixed residue."
    },
]

results = {
    "status": "full_coexact_delta_nonzero_normalization_decides_closure",
    "inputs": {
        "alpha_inv_reference": ALPHA_INV,
        "S_geo": S_GEO,
        "S_vac_current": S_VAC_CURRENT,
        "current_error": S_VAC_CURRENT - ALPHA_INV,
        "pi4_term": PI4_TERM,
        "Vol_RP3": VOL_RP3,
    },
    "tower": {
        "T_coex_S3": T_S3,
        "T_coex_RP3": T_RP3,
        "RP3_over_S3": T_RP3 / T_S3,
        "first_rp3_mode_fraction": rows[0]["contribution_rp3"] / T_RP3,
        "first_modes": rows[:8],
    },
    "normalization_variants_ranked": variants,
    "paired_candidates": paired_candidates,
    "verdict": (
        "The full RP3 coexact Bessel tower is nonzero and dominated by the first transverse mode. "
        "Naive raw normalizations are too large compared with the current alpha residual. The only variant close to the existing pi^-4 term is the volume-weighted half determinant with P02/Casimir mixing, which effectively identifies the pi^-4 term as a normalized summary of the coexact tower rather than an additional Delta_tower correction. No standard paired sector cancels the tower in the ordinary Maxwell--ghost determinant."
    ),
}

Path("s2t_full_coexact_delta_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "T_coex_RP3": T_RP3,
    "current_error": S_VAC_CURRENT - ALPHA_INV,
    "best_variant": variants[0],
    "pi4_term": PI4_TERM,
}, indent=2, ensure_ascii=False))