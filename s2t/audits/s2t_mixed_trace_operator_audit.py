import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
BASE_TOWER = (math.pi**2 / 2) * T_RP3 / S_GEO
EPS_NEEDED = 1 - PI4_TERM / BASE_TOWER
N_NEED = 24 * S_GEO * EPS_NEEDED


def scalar_even_modes(l_max=12):
    modes = []
    cumulative = 0
    for ell in range(0, l_max + 1, 2):
        degeneracy = (ell + 1) ** 2
        cumulative += degeneracy
        modes.append({
            "ell": ell,
            "lambda_scalar": ell * (ell + 2),
            "degeneracy": degeneracy,
            "cumulative_degeneracy": cumulative,
            "exact_one_form_inherits_if_ell_gt_0": ell > 0,
            "constant_mode_is_gauge_zero_mode": ell == 0,
        })
    return modes


def candidate_error(rank):
    epsilon = rank / (24 * S_GEO)
    term = BASE_TOWER * (1 - epsilon)
    return {
        "rank": rank,
        "epsilon": epsilon,
        "term": term,
        "relative_error_vs_pi4": (term - PI4_TERM) / PI4_TERM,
        "relative_error_vs_N_need": (rank - N_NEED) / N_NEED,
    }

modes = scalar_even_modes()
selection_candidates = []
for row in modes:
    selection_candidates.append({
        "selection": f"scalar_cumulative_through_ell_{row['ell']}",
        **candidate_error(row["cumulative_degeneracy"]),
    })
selection_candidates.extend([
    {"selection": "standard_maxwell_fp_nonzero_scalar_exact_cancelled", **candidate_error(0)},
    {"selection": "scalar_constant_gauge_volume_only", **candidate_error(1)},
    {"selection": "first_nonzero_even_exact_shell_only_ell2", **candidate_error(9)},
    {"selection": "constant_plus_first_nonzero_even_shell_ell0_ell2", **candidate_error(10)},
    {"selection": "through_ell4_control", **candidate_error(35)},
])
selection_candidates = sorted(selection_candidates, key=lambda item: abs(item["relative_error_vs_pi4"]))

bookkeeping = {
    "hodge_split": "Omega^1 = d Omega^0_nonzero ⊕ Omega^1_coexact ⊕ H^1",
    "rp3_b1": 0,
    "exact_nonzero_spectrum": "lambda_exact(ell)=lambda_scalar(ell) for ell>0, with same degeneracy",
    "constant_scalar_ell0": "zero mode/gauge volume; not an exact one-form because d(constant)=0",
    "standard_fp_risk": "Nonzero scalar/exact modes cancel or survive as a full det' Delta_0 factor depending on normalization, but not as a finite ell=2-only projector.",
}

proof_obligations = [
    {
        "obligation": "derive_projector_P_0_2",
        "status": "failed_in_standard_hodge_fp_route",
        "reason": "Standard Hodge/FP bookkeeping supplies full scalar/exact towers or cancellation, not a natural finite projector onto ell=0,2."
    },
    {
        "obligation": "include_constant_mode_d0",
        "status": "not_standard_exact_mode",
        "reason": "ell=0 scalar is a gauge zero mode and does not generate a nonzero exact one-form."
    },
    {
        "obligation": "exclude_higher_even_shells",
        "status": "failed_in_standard_hodge_fp_route",
        "reason": "If ell=2 enters by ordinary scalar/exact inheritance, ell=4,6,... enter by the same mechanism."
    },
    {
        "obligation": "second_order_sign",
        "status": "conditionally_ok",
        "reason": "The formal expansion log det(A+xB) contains -x^2 Tr((A^-1B)^2)/2, but determinant-power conventions still need operator-level verification."
    },
]

results = {
    "status": "mixed_trace_operator_proof_attempt_failed_selection_rule",
    "numbers": {
        "S_geo": S_GEO,
        "T_RP3": T_RP3,
        "pi4_term": PI4_TERM,
        "base_tower": BASE_TOWER,
        "epsilon_needed": EPS_NEEDED,
        "N_need": N_NEED,
        "nearest_integer": round(N_NEED),
    },
    "scalar_even_modes": modes,
    "determinant_bookkeeping": bookkeeping,
    "ranked_selection_candidates": selection_candidates,
    "proof_obligations": proof_obligations,
    "verdict": (
        "The standard Maxwell--Faddeev-Popov/Hodge route does not naturally produce finite rank d0+d2=10. "
        "The nonzero exact spectrum inherits the scalar spectrum for all ell>0; ell=0 is a gauge zero mode. "
        "Therefore a separate finite-rank projector or quadratic-strain mechanism is required."
    ),
}

Path("s2t_mixed_trace_operator_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(results["numbers"], indent=2, ensure_ascii=False))
print(results["verdict"])