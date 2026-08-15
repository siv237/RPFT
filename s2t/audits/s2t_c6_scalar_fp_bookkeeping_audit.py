import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
VOL_RP3 = math.pi**2
P02_RANK = 10
BASE = (VOL_RP3 / 2) * T_RP3 / S_GEO
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)

# Effective action convention: Gamma = -log Z.
# A real bosonic determinant contributes +1/2 log det to Gamma.
# A complex FP ghost determinant contributes -1 log det to Gamma.
# Hodge split of the full one-form determinant has
# det' Delta_1 = det' Delta_1,coex * det' Delta_0 on exact one-forms.
# Therefore standard covariant FP gives
# Gamma_std = 1/2 log det' Delta_1,coex - 1/2 log det' Delta_0 + zero/gauge/local terms.
# The scalar residual power is -1/2, not zero, before extra volume/Jacobian cancellations are proven.

schemes = [
    {
        "scheme": "physical_transverse_quotient",
        "gamma_coexact_logdet_power": 0.5,
        "gamma_scalar_logdet_power": 0.0,
        "requires_extra_cancellation": False,
        "classification": "viable_conditional_definition",
        "formula": "Gamma = 1/2 log det' Delta_1,coex + zero/gauge/local",
        "meaning": "P02 may be counted only in the coexact bosonic insertion if the physical quotient is the defining determinant scheme.",
    },
    {
        "scheme": "standard_covariant_FP_full_one_form",
        "gamma_full_one_form_power": 0.5,
        "gamma_fp_ghost_power": -1.0,
        "hodge_exact_scalar_power_from_Delta1": 0.5,
        "gamma_scalar_logdet_power_after_hodge": -0.5,
        "requires_extra_cancellation": True,
        "classification": "residual_scalar_half_power",
        "formula": "Gamma = 1/2 log det' Delta_1,coex - 1/2 log det' Delta_0 + zero/gauge/local",
        "meaning": "Standard FP/Hodge bookkeeping leaves a scalar half-determinant in Gamma unless zero/gauge/Jacobian normalization cancels it explicitly.",
    },
    {
        "scheme": "standard_FP_plus_unproven_scalar_cancellation",
        "gamma_coexact_logdet_power": 0.5,
        "gamma_scalar_logdet_power": 0.0,
        "requires_extra_cancellation": "must_be_proven",
        "classification": "desired_but_not_derived",
        "formula": "Gamma_scalar_residual -> kappa_Cas branch only, no P02 trace-square",
        "meaning": "This is the needed isolation lemma, not a consequence of the bare covariant FP determinant.",
    },
]

# Simplified rank-flow diagnostic for the P02 suppression factor.
# If the scalar residual carries the same first-strain P02 trace-square, its Grassmann/FP sign is opposite to the coexact bosonic suppression.
rank_scenarios = [
    {
        "scenario": "coexact_only",
        "coexact_rank": P02_RANK,
        "scalar_residual_power": 0.0,
        "effective_rank": P02_RANK,
        "factor": 1 - P02_RANK / (24 * S_GEO),
        "classification": "desired_C6_route",
    },
    {
        "scenario": "standard_FP_half_scalar_residual_carries_P02",
        "coexact_rank": P02_RANK,
        "scalar_residual_power": -0.5,
        "effective_rank": P02_RANK / 2,
        "factor": 1 - (P02_RANK / 2) / (24 * S_GEO),
        "classification": "wrong_factor_if_not_cancelled",
    },
    {
        "scenario": "full_ghost_like_scalar_P02_leakage",
        "coexact_rank": P02_RANK,
        "scalar_residual_power": -1.0,
        "effective_rank": 0,
        "factor": 1.0,
        "classification": "suppression_cancelled",
    },
]

for row in rank_scenarios:
    row["absorption_value"] = BASE * row["factor"]
    row["relative_error_vs_pi4"] = (row["absorption_value"] - PI4_TERM) / PI4_TERM

obligations = [
    {
        "obligation": "derive_Hodge_measure_and_gauge_volume",
        "status": "open",
        "test": "Show zero/gauge/Jacobian factors cancel the -1/2 log det' Delta0 residual in the same normalization, or keep it.",
    },
    {
        "obligation": "compute_scalar_second_variation",
        "status": "open",
        "test": "Compute delta_g^2 log det' Delta0 under first ambient strain and project to Sym^2(R4)=P02.",
    },
    {
        "obligation": "separate_kappa_Cas_from_P02_trace_square",
        "status": "open",
        "test": "Prove the retained scalar branch contributes only kappa_Cas=1/24 and no finite P02 trace-square.",
    },
]

results = {
    "status": "standard_covariant_FP_leaves_scalar_half_power_unless_cancelled",
    "numbers": {
        "S_geo": S_GEO,
        "P02_rank": P02_RANK,
        "base_volume_half_absorption": BASE,
        "pi4_term": PI4_TERM,
    },
    "schemes": schemes,
    "rank_scenarios": rank_scenarios,
    "obligations": obligations,
    "verdict": (
        "Bare standard covariant FP/Hodge bookkeeping gives Gamma = 1/2 log det' Delta_1,coex - 1/2 log det' Delta0, "
        "so exact/scalar cancellation is not zero by default. If that residual scalar half-determinant carries the same P02 trace-square, "
        "the desired rank-10 suppression is reduced to an effective rank 5 in the simplified sign model. Therefore C6 requires an additional "
        "cancellation or selection lemma: either work in the physical transverse quotient as the defining scheme, or prove that the standard-FP "
        "scalar residual is only the kappa_Cas=1/24 branch and has no P02 leakage."
    ),
}

Path("s2t_c6_scalar_fp_bookkeeping_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "standard_FP_scalar_power": -0.5,
    "coexact_only_factor": rank_scenarios[0]["factor"],
    "half_scalar_leakage_factor": rank_scenarios[1]["factor"],
    "half_scalar_leakage_relative_error_vs_pi4": rank_scenarios[1]["relative_error_vs_pi4"],
}, indent=2, ensure_ascii=False))