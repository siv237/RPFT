import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
VOL_RP3 = math.pi**2
BASE = (VOL_RP3 / 2) * T_RP3 / S_GEO
N = 10
SUPPRESSION = 1 - N / (24 * S_GEO)
TERM_WITH_SUPPRESSION = BASE * SUPPRESSION

# Formal second variation for a determinant block c log det(A + eps B), with delta^2 A ignored:
# c * log det = c[log det A + eps Tr(A^-1 B) - eps^2/2 Tr((A^-1 B)^2)+...]
# quadratic_sign = -c/2 times positive trace-square.
blocks = [
    {
        "block": "real_bosonic_coexact_Maxwell",
        "effective_action_piece": "+1/2 log det Delta_1_coex",
        "c": 0.5,
        "quadratic_coefficient_minus_c_over_2": -0.25,
        "sign_for_positive_trace_square": "negative",
        "compatibility_with_required_suppression": "compatible",
        "comment": "A positive P02 trace-square insertion decreases the effective term, matching the suppression factor 1-N/(24S_geo).",
    },
    {
        "block": "complex_Grassmann_FP_ghost",
        "effective_action_piece": "- log det Delta_0_prime in Gamma=-log Z convention",
        "c": -1.0,
        "quadratic_coefficient_minus_c_over_2": 0.5,
        "sign_for_positive_trace_square": "positive",
        "compatibility_with_required_suppression": "opposite_if_same_B",
        "comment": "If the same P02 insertion sits in the ghost determinant with the same positive trace-square, it would reduce or cancel the bosonic suppression.",
    },
    {
        "block": "gauge_longitudinal_exact_pair",
        "effective_action_piece": "cancels against FP ghost after gauge fixing for nonzero scalar modes",
        "c": "net_zero_for_paired_nonzero_scalar_branch",
        "quadratic_coefficient_minus_c_over_2": "net_zero_if_pairing_exact",
        "sign_for_positive_trace_square": "canceled",
        "compatibility_with_required_suppression": "does_not_supply_suppression",
        "comment": "Ordinary exact/scalar inherited tower cannot be the source of the finite P02 suppression unless the cancellation is modified by the first-strain projection.",
    },
    {
        "block": "periodic_scalar_Casimir_branch",
        "effective_action_piece": "finite scalar/ghost residue kappa_Cas=1/24 after det-prime zero-mode convention",
        "c": "reduced_finite_part",
        "quadratic_coefficient_minus_c_over_2": "enters as the factor 1/(24S_geo) in the S2T ansatz",
        "sign_for_positive_trace_square": "must couple with bosonic coexact negative sign",
        "compatibility_with_required_suppression": "conditional",
        "comment": "The S2T formula is sign-compatible if the finite 1/24 branch multiplies the bosonic coexact second variation rather than appearing as an independent positive ghost trace-square.",
    },
]

sign_tests = [
    {
        "test": "formal_logdet_sign",
        "status": "pass",
        "reason": "For +1/2 log det of a real bosonic coexact operator, the B^2 term is negative: -1/4 Tr((A^-1 B)^2). This gives suppression, not enhancement.",
    },
    {
        "test": "matches_required_factor_direction",
        "status": "pass_conditionally",
        "reason": f"The desired factor is {SUPPRESSION:.12f}<1, so a negative bosonic second variation has the correct direction.",
    },
    {
        "test": "ghost_does_not_flip_sign",
        "status": "open",
        "reason": "A ghost determinant with the same P02 insertion has the opposite quadratic sign in effective action. Closure requires the relevant P02 insertion to be in the coexact bosonic block, while the scalar/ghost branch contributes only the finite 1/24 coefficient after exact-mode cancellation.",
    },
    {
        "test": "delta2_operator_terms",
        "status": "open",
        "reason": "If the Laplacian variation includes a genuine second derivative delta^2 Delta, the term +c Tr(A^-1 delta^2 Delta)/2 can alter the sign. The S2T ansatz implicitly assumes the mixed residue is dominated by the trace-square piece or that delta^2 terms are local/subtracted.",
    },
]

results = {
    "status": "second_variation_sign_formally_compatible_not_full_proof",
    "numbers": {
        "S_geo": S_GEO,
        "base_volume_half_absorption": BASE,
        "N": N,
        "suppression_factor_1_minus_N_over_24S": SUPPRESSION,
        "suppressed_absorption": TERM_WITH_SUPPRESSION,
        "pi4_term": PI4_TERM,
        "relative_error_vs_pi4": (TERM_WITH_SUPPRESSION - PI4_TERM) / PI4_TERM,
    },
    "blocks": blocks,
    "sign_tests": sign_tests,
    "verdict": (
        "The required minus sign is formally compatible with the real bosonic coexact Maxwell second variation: +1/2 logdet gives a negative trace-square term. "
        "This supports the direction of the factor 1-N/(24S_geo). However, it is not a full C6 proof because ghost determinants have the opposite quadratic sign if the same insertion acts there, and genuine delta^2 Delta terms may contribute unless shown to be local/subtracted. "
        "Thus the sign subtest is a conditional pass for the coexact bosonic block, with two explicit remaining caveats."
    ),
}

Path("s2t_c6_second_variation_sign_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "suppression_factor": SUPPRESSION,
    "bosonic_quadratic_sign": blocks[0]["sign_for_positive_trace_square"],
    "ghost_quadratic_sign": blocks[1]["sign_for_positive_trace_square"],
    "open_tests": [t["test"] for t in sign_tests if t["status"] == "open"],
}, indent=2, ensure_ascii=False))