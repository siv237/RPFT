import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
BASE = (math.pi**2 / 2) * T_RP3 / S_GEO
N_NEED = 24 * S_GEO * (1 - PI4_TERM / BASE)
P02_RANK = 10
P02_TERM = BASE * (1 - P02_RANK / (24 * S_GEO))

# The skeleton is not a new fit. It records the formal determinant expansion that
# must be proven to upgrade the absorption route.
operator_blocks = [
    {
        "block": "coexact_transverse_Maxwell",
        "operator": "Delta_1^coex on L(2,1) times periodic -partial_tau^2 on S1",
        "det_power": "+1/2 log det'",
        "role": "source of the nonzero Bessel tower T_coex^RP3",
        "known_status": "nonzero; not canceled by scalar ghosts",
    },
    {
        "block": "exact_longitudinal_Maxwell",
        "operator": "d Delta_0^positive d* inherited scalar branch",
        "det_power": "gauge-dependent before FP cancellation",
        "role": "pairs with nonzero scalar ghosts in ordinary Hodge bookkeeping",
        "known_status": "cannot by itself select ell=0,2; generic inheritance gives ell=2,4,6,...",
    },
    {
        "block": "Faddeev_Popov_scalar_ghost",
        "operator": "Delta_0 with det-prime zero-mode convention",
        "det_power": "- log det' for complex Grassmann ghost, scheme-dependent normalization in reduced scalar branch",
        "role": "cancels gauge volume/exact branch; leaves the periodic constant finite part behind only under the selected det-prime scheme",
        "known_status": "supports kappa_Cas=1/24 for the constant periodic branch",
    },
    {
        "block": "first_ambient_strain_projector",
        "operator": "P02 acting on q_A(x)=A_ab x^a x^b, A=A^T, on S3/RP3",
        "det_power": "must enter through second variation of the gauge-fixed determinant",
        "role": "candidate finite-rank insertion in the mixed trace",
        "known_status": "rank 10 representation-theoretically; not yet derived as the actual determinant insertion",
    },
]

required_identity = {
    "target": "pi^-4 absorption identity at C6 level",
    "formal_shape": "Delta_pi4 = (Vol(RP3)/2) * T_coex^RP3/S_geo * (1 - Tr(P02)/(24*S_geo))",
    "expanded_requirements": [
        "The coexact transverse determinant supplies T_coex^RP3 with positive tower multiplicities.",
        "The bosonic determinant and volume normalization supply Vol(RP3)/2 = pi^2/2.",
        "The second-order determinant expansion supplies the minus sign in 1 - N/(24*S_geo).",
        "The scalar/ghost Casimir branch supplies the universal factor 1/(24*S_geo).",
        "The admissible mixed insertion is P02, so Tr(P02)=10 and not the full scalar tower.",
        "The remaining nonintegral gap N_need-10 is explained by a derived finite local scheme residue, or else the identity is not exact.",
    ],
}

trace_tests = [
    {
        "test": "T1_second_variation_sign",
        "needed_formula": "delta^2 Gamma = -1/4 Tr((Delta^{-1} delta Delta)^2) plus ghost/exact corrections, reducible to the model's -N/(24*S_geo) sign convention",
        "status": "open",
        "why": "The sign is standard in logdet expansion, but the combined Maxwell--ghost reduced operator has not been written explicitly.",
    },
    {
        "test": "T2_volume_factor",
        "needed_formula": "integral over RP3 of the normalized local insertion gives Vol(RP3)=pi^2; bosonic logdet gives 1/2",
        "status": "plausible_open",
        "why": "The factors are natural but not yet derived from normalized eigenfunctions and measure conventions.",
    },
    {
        "test": "T3_projector_rank",
        "needed_formula": "Tr over admissible first-strain insertion space equals dim Sym^2(R4)=10",
        "status": "conditional_pass",
        "why": "This follows if and only if the insertion space is first ambient strain rather than generic internal metric variations.",
    },
    {
        "test": "T4_no_full_scalar_tower_leakage",
        "needed_formula": "P02 is applied before scalar/exact spectral summation; ell>=4 are higher ambient strains outside II.A",
        "status": "conditional_pass_inside_S2T",
        "why": "Already supported by first-strain selection, but not a theorem of ordinary Maxwell theory.",
    },
    {
        "test": "T5_exact_equality_or_scheme_residue",
        "needed_formula": "N_need - 10 = 0.0099700224 is derived as a finite scheme residue, omitted subleading determinant term, or proven irrelevant under the target precision rule",
        "status": "fail_as_exact_identity_now",
        "why": "With current exact Bessel tail and rank 10, the equality is not exact; relative pi^-4 mismatch is 3.04e-6.",
    },
]

routes_after_skeleton = [
    {
        "next_step": "derive_reduced_operator",
        "description": "Write the gauge-fixed abelian one-loop functional Gamma[A,g] on RP3xS1 and define the first-strain variation delta_g Delta explicitly.",
        "expected_output": "A formula for delta^2 Gamma_mix with Maxwell and ghost terms before inserting P02.",
    },
    {
        "next_step": "normalize_P02_basis",
        "description": "Choose an orthonormal basis of Sym^2(R4) restricted to S3/RP3 and compute Tr(P02) with the RP3 volume measure.",
        "expected_output": "A normalization check for the pi^2/2 volume factor and rank 10.",
    },
    {
        "next_step": "evaluate_scheme_gap",
        "description": "Track the small N_need-10 gap through zero-mode subtraction, local finite counterterms, and omitted subleading Bessel levels.",
        "expected_output": "Either a derived finite residue or a forced downgrade of exact absorption.",
    },
]

results = {
    "status": "C6_operator_trace_skeleton_built_not_closed",
    "numbers": {
        "S_geo": S_GEO,
        "T_coex_RP3": T_RP3,
        "pi4_term": PI4_TERM,
        "base_volume_half_absorption": BASE,
        "N_need": N_NEED,
        "P02_rank": P02_RANK,
        "N_need_minus_P02": N_NEED - P02_RANK,
        "P02_absorption": P02_TERM,
        "P02_relative_error_vs_pi4": (P02_TERM - PI4_TERM) / PI4_TERM,
    },
    "operator_blocks": operator_blocks,
    "required_identity": required_identity,
    "trace_tests": trace_tests,
    "routes_after_skeleton": routes_after_skeleton,
    "verdict": "C6 is now localized: the missing proof is the explicit second variation of the gauge-fixed Maxwell--ghost determinant under first ambient strain. P02 rank 10 is conditionally derived, but the volume factor, combined sign, det-prime bookkeeping, and N_need-10 scheme gap remain open.",
}

Path("s2t_c6_operator_trace_skeleton_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "N_need_minus_P02": results["numbers"]["N_need_minus_P02"],
    "P02_relative_error_vs_pi4": results["numbers"]["P02_relative_error_vs_pi4"],
    "open_tests": [t["test"] for t in trace_tests if "open" in t["status"] or "fail" in t["status"]],
}, indent=2, ensure_ascii=False))