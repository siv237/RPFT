import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
P02_RANK = 10
TRACELESS_RANK = 9
TRACE_RANK = 1
FIRST_NONZERO_ELL = 2
FIRST_NONZERO_MULT = (FIRST_NONZERO_ELL + 1) ** 2
FIRST_NONZERO_LAMBDA_S3_SCALAR = FIRST_NONZERO_ELL * (FIRST_NONZERO_ELL + 2)

# This audit tests the two rescue routes requested after scalar P02 leakage was found selection-rule allowed.
# Rescue A: prove scalar trace-square is fully local/subtracted in Gamma_loc.ct or Gamma_zero/gauge.
# Rescue B: prove cancellation through zero/gauge/Jacobian factors.
#
# We use only structural facts already used in Tome II:
# - Local heat-kernel counterterms come from zero-winding / UV asymptotics.
# - Massive nonzero eigenvalues on RP3 x S1 generate finite nonlocal Bessel tails after Poisson summation.
# - Zero/gauge/Jacobian terms are finite-dimensional or determinant-power bookkeeping; they cannot cancel a mode-dependent nonlocal tower unless an equal opposite tower is explicitly present.

rescue_locality_tests = [
    {
        "test": "is_P02_scalar_trace_square_pure_heat_kernel_local",
        "status": "fail_not_proven_and_structurally_unlikely",
        "reason": (
            "The nonzero scalar tower has positive RP3 eigenvalues. After summing over S1 momenta, each positive eigenvalue yields "
            "a local zero-winding part plus a finite nonlocal Bessel/winding part. Local counterterms can remove only the former."
        ),
    },
    {
        "test": "first_nonzero_shell_generates_nonlocal_candidate",
        "status": "blocking",
        "ell": FIRST_NONZERO_ELL,
        "multiplicity": FIRST_NONZERO_MULT,
        "lambda_scalar_unit_S3": FIRST_NONZERO_LAMBDA_S3_SCALAR,
        "reason": (
            "The first nonzero even scalar shell ell=2 is allowed on RP3, has multiplicity 9, and couples to ell=2/P02. "
            "Since lambda>0, its S1 determinant has a nonlocal finite part unless cancelled by another sector."
        ),
    },
    {
        "test": "can_Gamma_zero_gauge_absorb_nonlocal_tower",
        "status": "fail",
        "reason": "Gamma_zero/gauge controls removed zero modes and gauge volume; it is finite-dimensional/global and cannot absorb an infinite mode-dependent Bessel tower.",
    },
]

rescue_jacobian_tests = [
    {
        "test": "hodge_jacobian_changes_determinant_power",
        "status": "already_accounted_in_standard_FP_power_count",
        "reason": (
            "The Hodge split determinant identity det' Delta1 = det' Delta1,coex * det' Delta0 is exactly what produced "
            "the residual -1/2 log det' Delta0 in Gamma. Reusing it cannot also cancel the same residual without an additional derived factor."
        ),
    },
    {
        "test": "gauge_volume_cancels_nonzero_scalar_modes",
        "status": "fail",
        "reason": "Gauge volume removes the constant gauge orbit / zero mode. It does not provide eigenvalue-by-eigenvalue factors over nonzero scalar shells ell=2,4,... .",
    },
    {
        "test": "zero_mode_prime_det_cancels_nonzero_tower",
        "status": "fail",
        "reason": "The det-prime rule removes the true scalar zero mode only; it does not remove the nonzero ell=2 scalar shell or its S1 tower.",
    },
    {
        "test": "possible_additional_BRST_or_NK_ghost",
        "status": "not_present_in_current_model",
        "reason": "No extra determinant sector with the same scalar spectrum and opposite half-power is defined in Tome II. Adding one would be a new model ingredient, not a proof of the existing standard-FP route.",
    },
]

route_verdicts = [
    {
        "route": "local_subtracted_in_Gamma_loc_ct",
        "verdict": "not_proven_fails_as_general_claim",
        "required_to_rescue": "Show the P02 scalar trace-square has no finite nonlocal winding/Bessel part, not merely subtract its UV heat-kernel part.",
    },
    {
        "route": "zero_gauge_jacobian_cancellation",
        "verdict": "fails_for_nonzero_tower_in_current_bookkeeping",
        "required_to_rescue": "Derive an additional nonzero-mode determinant factor with exactly +1/2 log det' Delta0 and matching P02 second variation.",
    },
    {
        "route": "physical_transverse_quotient",
        "verdict": "remains_viable_as_defining_scheme",
        "required_to_rescue": "Declare/derive that the determinant is defined on the coexact quotient before scalar FP residual is counted.",
    },
]

results = {
    "status": "standard_FP_rescue_routes_not_closed",
    "numbers": {
        "S_geo": S_GEO,
        "P02_rank": P02_RANK,
        "traceless_rank": TRACELESS_RANK,
        "trace_rank": TRACE_RANK,
        "first_nonzero_scalar_ell": FIRST_NONZERO_ELL,
        "first_nonzero_scalar_multiplicity": FIRST_NONZERO_MULT,
        "first_nonzero_scalar_lambda_unit_S3": FIRST_NONZERO_LAMBDA_S3_SCALAR,
    },
    "rescue_locality_tests": rescue_locality_tests,
    "rescue_jacobian_tests": rescue_jacobian_tests,
    "route_verdicts": route_verdicts,
    "verdict": (
        "Neither requested standard-FP rescue route is proven. Local heat-kernel subtraction cannot by itself remove the finite nonlocal "
        "Bessel/winding part generated by positive scalar eigenvalues, and the first nonzero RP3 scalar shell ell=2 is P02-coupling allowed. "
        "Zero/gauge/Jacobian factors remove zero modes and set determinant powers, but in the current bookkeeping they do not provide an opposite "
        "nonzero scalar tower cancelling -1/2 log det' Delta0. Therefore standard covariant FP remains blocked; the clean surviving route is the physical transverse quotient, "
        "or else pi^-4 must be downgraded to structural compression until a new analytic cancellation is derived."
    ),
}

Path("s2t_c6_scalar_rescue_routes_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "local_subtracted_route": route_verdicts[0]["verdict"],
    "zero_gauge_jacobian_route": route_verdicts[1]["verdict"],
    "surviving_route": "physical_transverse_quotient_or_new_cancellation",
}, indent=2, ensure_ascii=False))