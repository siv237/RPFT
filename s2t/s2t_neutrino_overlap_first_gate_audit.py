import json
import math
from pathlib import Path


PI = math.pi
TARGET = PI + 1 / PI

ME_MEV = 0.51099895069
MMU_MEV = 105.6583755
D_NU = 23 + 1 / PI
BASE_EV = ME_MEV**4 / (MMU_MEV**3 * D_NU) * 1e6
MU_NU_EV = TARGET * BASE_EV
DM21_PRED = MU_NU_EV**2
R_NU = D_NU + PI**2 + 2 / 3
DM31_PRED = R_NU * DM21_PRED

# NuFIT 6.0, IC24 with SK-atm, normal ordering.
DM21_NUFIT = 7.49e-5
DM21_NUFIT_SIGMA = 0.19e-5
DM31_NUFIT = 2.513e-3
DM31_NUFIT_SIGMA = 0.020e-3

dirac = json.loads(Path("dirac_spin_holonomy_results.json").read_text())
gauge = json.loads(Path("gauge_holonomy_results.json").read_text())
sectors = json.loads(Path("sector_attribution_results.json").read_text())

alpha_antiperiodic = next(
    row for row in dirac["alpha_sweep"] if row["spin_structure_label"] == "antiperiodic"
)
theta = alpha_antiperiodic["theta"]
gap = alpha_antiperiodic["circle_gap"]


candidate_tests = [
    {
        "candidate": "full_circle_primal_dual_Gram",
        "definition": "Tr diag(L,L^-1) with L=2*pi*R1 and R1=1",
        "value": 2 * PI + 1 / (2 * PI),
        "target_error": 2 * PI + 1 / (2 * PI) - TARGET,
        "status": "fails",
        "reason": "The declared geometric circle has circumference 2*pi, not pi.",
    },
    {
        "candidate": "radius_primal_dual_Gram",
        "definition": "Tr diag(R1,R1^-1) with R1=1",
        "value": 2.0,
        "target_error": 2.0 - TARGET,
        "status": "fails",
        "reason": "The unit-radius modulus gives 2 and contains no pi factor.",
    },
    {
        "candidate": "antiperiodic_gap_norm",
        "definition": "1+gap^2 for the lowest Dirac circle gap gap=1/2",
        "value": 1 + gap**2,
        "target_error": 1 + gap**2 - TARGET,
        "status": "fails",
        "reason": "The standard spectral norm of the lowest antiperiodic mode gives 5/4.",
    },
    {
        "candidate": "half_systole_primal_dual_Gram",
        "definition": "Tr diag(pi,pi^-1)",
        "value": TARGET,
        "target_error": 0.0,
        "status": "algebraic_match_not_derived",
        "reason": (
            "It matches exactly, but the antiperiodic spin structure does not quotient the geometric circle "
            "to a half-length fundamental domain."
        ),
    },
    {
        "candidate": "holonomy_angle_reciprocal_Gram",
        "definition": "Tr diag(theta,theta^-1) at theta=pi",
        "value": theta + 1 / theta,
        "target_error": theta + 1 / theta - TARGET,
        "status": "exact_but_not_gauge_invariant",
        "reason": (
            "Holonomy is the unitary class exp(i theta), while theta+theta^-1 is not periodic under "
            "theta -> theta+2*pi and is singular at the periodic branch."
        ),
    },
]


gauge_branch_values = []
for row in gauge["beta_sweep"]:
    theta_plus = PI * row["theta_plus_over_pi"]
    theta_minus = PI * row["theta_minus_over_pi"]
    reciprocal_trace = None
    if theta_plus != 0 and theta_minus != 0:
        reciprocal_trace = theta_plus + 1 / theta_plus + theta_minus + 1 / theta_minus
    gauge_branch_values.append(
        {
            "beta": row["beta"],
            "theta_plus": theta_plus,
            "theta_minus": theta_minus,
            "reciprocal_trace": reciprocal_trace,
        }
    )


required_target_from_nufit = math.sqrt(DM21_NUFIT) / BASE_EV
ratio_pred = DM31_PRED / DM21_PRED
ratio_nufit = DM31_NUFIT / DM21_NUFIT
ratio_sigma_rel = math.sqrt(
    (DM31_NUFIT_SIGMA / DM31_NUFIT) ** 2
    + (DM21_NUFIT_SIGMA / DM21_NUFIT) ** 2
)
ratio_pull = (ratio_pred - ratio_nufit) / (ratio_nufit * ratio_sigma_rel)


results = {
    "status": "neutrino_overlap_holonomy_only_route_failed_positive_metric_route_conditional",
    "date": "2026-08-03",
    "target": {
        "N_nu_squared": TARGET,
        "N_nu": math.sqrt(TARGET),
        "claimed_role": "Dirac insertion normalization",
    },
    "audited_inputs": {
        "antiperiodic_alpha": alpha_antiperiodic["alpha"],
        "antiperiodic_theta": theta,
        "antiperiodic_gap": gap,
        "spin_heat_coefficient_invariance": dirac["invariance_summary"],
        "gauge_phase_branch_motion": gauge_branch_values,
        "sector_separation_ratio": sectors["summary"]["sector_separation_ratio"],
    },
    "candidate_tests": candidate_tests,
    "structural_no_go": {
        "statement": (
            "No function depending only on the unitary holonomy class U=exp(i theta) can equal "
            "theta+theta^-1 globally, because the latter is not 2*pi-periodic and diverges at theta=0."
        ),
        "consequence": (
            "The target cannot be derived from spin or gauge holonomy alone. A separate positive modulus or "
            "self-adjoint overlap operator is required."
        ),
    },
    "surviving_constructive_candidate": {
        "operator": "Q_cycle=diag(g,g^-1), g>0, det(Q_cycle)=1",
        "target_condition": "g=pi",
        "trace": TARGET,
        "status": "conditional_until_g_is_derived_from_geometry_or_spectral_measure",
        "required_proof": (
            "Construct Q_cycle from a positive primal/dual cycle metric, Dirichlet-to-Neumann map, Hodge metric, "
            "or another self-adjoint operator; do not identify g with a branch-dependent holonomy angle by definition."
        ),
    },
    "phenomenology_check": {
        "source": "NuFIT 6.0 IC24 with SK-atm normal-ordering best fit",
        "predicted_dm21_eV2": DM21_PRED,
        "nufit_dm21_eV2": DM21_NUFIT,
        "nufit_dm21_sigma_eV2": DM21_NUFIT_SIGMA,
        "dm21_pull_sigma": (DM21_PRED - DM21_NUFIT) / DM21_NUFIT_SIGMA,
        "required_N_nu_squared_from_dm21_best_fit": required_target_from_nufit,
        "required_minus_pi_reciprocal": required_target_from_nufit - TARGET,
        "predicted_dm31_eV2": DM31_PRED,
        "nufit_dm31_eV2": DM31_NUFIT,
        "nufit_dm31_sigma_eV2": DM31_NUFIT_SIGMA,
        "predicted_ratio": ratio_pred,
        "nufit_ratio": ratio_nufit,
        "ratio_pull_sigma_approx": ratio_pull,
        "interpretation": (
            "The factor is compatible with current oscillation scales but is not numerically forced by the central "
            "values. Agreement cannot substitute for an operator derivation."
        ),
    },
    "theory_effect": {
        "phase_load_sector_separation": "strengthened",
        "holonomy_only_overlap_claim": "rejected",
        "reciprocal_positive_metric_mechanism": "promising_but_conditional",
        "absolute_neutrino_scale": "remains_conditional",
        "dimensionless_neutrino_ratio": "unchanged",
        "feedback_to_common_source": (
            "A successful common source must contain both a unitary phase sector and a separate positive reciprocal "
            "metric sector; one cannot be substituted for the other."
        ),
    },
    "next_steps": [
        "construct a positive self-adjoint cycle operator Q_cycle from the declared geometry",
        "test whether its determinant-one reciprocal spectrum is protected under radius and holonomy deformations",
        "derive the Dirac insertion as a matrix element of Q_cycle^(1/2), not as a scalar multiplier",
        "if no such operator exists, downgrade the absolute neutrino scale and retain only R_nu",
    ],
    "verdict": (
        "The existing Dirac and gauge holonomy audits do not derive N_nu^2=pi+pi^-1. The exact expression can be "
        "written as the trace of a reciprocal positive Gram operator diag(pi,pi^-1), but identifying its modulus "
        "with the holonomy angle is not gauge invariant. The holonomy-only route is therefore closed negatively. "
        "One constructive route remains: derive a separate positive primal/dual cycle operator with determinant one "
        "and eigenvalues pi and pi^-1. Until that operator is constructed, the absolute neutrino scale remains conditional."
    ),
}


assert abs(theta - PI) < 1e-15
assert abs(candidate_tests[3]["value"] - TARGET) < 1e-15
assert abs(candidate_tests[4]["value"] - TARGET) < 1e-15
assert gauge_branch_values[-1]["reciprocal_trace"] is None

Path("s2t_neutrino_overlap_first_gate_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(json.dumps({
    "status": results["status"],
    "target": TARGET,
    "dm21_pull_sigma": results["phenomenology_check"]["dm21_pull_sigma"],
    "ratio_pull_sigma_approx": ratio_pull,
}, indent=2, ensure_ascii=False))