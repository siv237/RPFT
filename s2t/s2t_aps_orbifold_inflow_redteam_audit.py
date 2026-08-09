#!/usr/bin/env python3
import json
from fractions import Fraction
from pathlib import Path


def exterior_degree(*degrees):
    return sum(degrees)


def main():
    spin = json.loads(
        Path("s2t_spin_generation_selector_results.json").read_text(
            encoding="utf-8"
        )
    )
    projection = json.loads(
        Path("s2t_anomaly_free_holonomy_projection_results.json").read_text(
            encoding="utf-8"
        )
    )
    susceptibility = json.loads(
        Path("s2t_six_channel_inverse_susceptibility_results.json").read_text(
            encoding="utf-8"
        )
    )

    proposed_parity = (-1, -1, -1, 1, 1)
    corrected_parity = (1, 1, 1, -1, -1)
    proposed_determinant = 1
    corrected_determinant = 1
    for value in proposed_parity:
        proposed_determinant *= value
    for value in corrected_parity:
        corrected_determinant *= value

    eta_values = spin["spectral_cross_check"]["RP3_spin_eta_invariants"]
    aps_terms = [-(Fraction(str(value)) / 2) for value in eta_values]
    zeta_minus_one = Fraction(-1, 12)
    proposed_decomposition = Fraction(1, 4) + abs(zeta_minus_one)

    proposed_cs_degrees = {
        "A_wedge_dA": exterior_degree(1, 2),
        "A_cubed": exterior_degree(1, 1, 1),
    }
    correct_cs5_degrees = {
        "A_F_F": exterior_degree(1, 2, 2),
        "A3_F": exterior_degree(1, 1, 1, 2),
        "A5": exterior_degree(1, 1, 1, 1, 1),
    }

    beta = projection["zero_mode_content"]["beta_vector_Y_2_3"]
    target_beta = projection["zero_mode_content"][
        "target_beta_vector_Y_2_3"
    ]
    beta_error = max(abs(left - right) for left, right in zip(beta, target_beta))

    results = {
        "status": "APS_orbifold_inflow_reframing_contains_useful_candidates_but_does_not_close_the_operator_and_parent_action_gates",
        "date": "2026-08-06",
        "exact_checks": {
            "arithmetic_one_third": {
                "one_quarter_plus_abs_zeta_minus_one": str(proposed_decomposition),
                "passes": proposed_decomposition == Fraction(1, 3),
                "scope": "arithmetic identity only",
            },
            "proposed_SU5_parity": {
                "matrix": list(proposed_parity),
                "determinant": proposed_determinant,
                "belongs_to_SU5": proposed_determinant == 1,
            },
            "corrected_SU5_parity": {
                "matrix": list(corrected_parity),
                "determinant": corrected_determinant,
                "belongs_to_SU5": corrected_determinant == 1,
                "matches_existing_gate": True,
            },
            "form_degree": {
                "proposed_integrand_degrees": proposed_cs_degrees,
                "is_five_form": all(
                    degree == 5 for degree in proposed_cs_degrees.values()
                ),
                "correct_CS5_monomial_degrees": correct_cs5_degrees,
                "correct_template_is_five_form": all(
                    degree == 5 for degree in correct_cs5_degrees.values()
                ),
            },
            "existing_split_projection": {
                "beta_vector_Y_2_3": beta,
                "target": target_beta,
                "max_error": beta_error,
                "passes": beta_error < 1e-12,
                "required_structure": "RP3 Z2 parity plus S1 Z4 holonomy plus multiplet flat characters",
            },
            "six_channel_identity": {
                "inverse_collective_hessian": susceptibility["exact_identity"][
                    "inverse_collective_hessian"
                ],
                "target_one_over_pi4": susceptibility["exact_identity"][
                    "target_one_over_pi4"
                ],
                "passes": susceptibility["exact_identity"]["absolute_error"] == 0,
            },
        },
        "APS_mu_tau_gate": {
            "pi1_product": "pi1(RP3 x S1)=Z2 x Z",
            "finding": (
                "The torsion holonomy and the circle spin sign belong to independent "
                "generators. Their product is the holonomy of a chosen diagonal loop, "
                "not an automatic total compact holonomy."
            ),
            "project_eta_values_for_untwisted_RP3_spin_structures": eta_values,
            "corresponding_APS_terms_if_h_zero": [str(value) for value in aps_terms],
            "claimed_eta_minus_one_half_is_derived": False,
            "zeta_gate": (
                "zeta(-1) regularizes a linear mode sum; det-prime is controlled by a "
                "spectral-zeta derivative. Taking an absolute value and adding the two "
                "quantities requires one common relative mass operator."
            ),
            "family_assignment": (
                "Assigning the nontrivial torsion line to mu but not tau is a family "
                "selector and remains underived."
            ),
            "passes": False,
        },
        "majorana_23_gate": {
            "dimension_identity": "24-1=23",
            "finding": (
                "Gauge fixing quotients field configurations by a gauge orbit; it is not "
                "automatically subtraction of one vector from a 24-dimensional Majorana "
                "module. The conformal factor, an S1 isometry zero mode, and a finite "
                "Majorana component are different complexes."
            ),
            "Ahat_denominator_implication": False,
            "required_calculation": (
                "Write the quadratic Majorana/gravity or gauge complex on RP3 x S1, "
                "identify kernels and ghosts, and compute the physical index/rank."
            ),
            "passes": False,
        },
        "orbifold_gate": {
            "simple_claim_status": "incorrect_as_written",
            "reasons": [
                "diag(-1,-1,-1,+1,+1) has determinant -1 and is not an SU5 element",
                "one parity matrix fixes adjoint breaking but not all fundamental multiplet intrinsic parities",
                "the displayed simple table does not itself yield one vectorlike U plus two vectorlike D",
            ],
            "existing_stronger_candidate": projection["verdict"],
            "remaining_gaps": projection["caveats"],
            "passes_representation_direction": True,
            "passes_threshold_magnitude": False,
        },
        "inflow_gate": {
            "proposed_action_status": "dimensionally_invalid",
            "correct_gauge_CS5_template": "omega5(A)=Tr(A F^2 - 1/2 A^3 F + 1/10 A^5), up to convention and exact forms",
            "APS_dimension_issue": (
                "If the APS filling has boundary RP3, it is four-dimensional. If the "
                "boundary is RP3 x S1, the boundary eta operator and index problem must "
                "be specified in the corresponding five-dimensional setup; eta_D(RP3) "
                "cannot simply be inserted unchanged."
            ),
            "anomaly_polynomial_required": True,
            "vectorlike_warning": (
                "The existing U+2D fermion survivors are vectorlike, so their four-dimensional "
                "gauge anomaly cancels and does not by itself fix a nonzero inflow level."
            ),
            "real_response_warning": (
                "Anomaly inflow fixes anomalous variations/phases. It does not by itself "
                "fix the real finite coefficients 1/(24 Sgeo) or 1/(pi^4 Sgeo^2)."
            ),
            "passes": False,
        },
        "revised_verdict": {
            "retained": [
                "APS eta data are a legitimate candidate discriminator of spin/twist sectors",
                "the anomaly-free Z2/Z4 SU5 projection exactly realizes the U+2D+H beta direction",
                "the selfdual six-channel half-shifted inverse susceptibility exactly equals pi^-4",
                "a bulk-boundary-defect formulation is a legitimate II.B search class",
            ],
            "not_closed": [
                "the coefficient one third as one relative mass correction",
                "the muon/tau family holonomy assignment",
                "the subtraction 24-1 as a physical Majorana rank",
                "the absolute EW/QCD threshold magnitude and sign",
                "the anomaly polynomial and a correctly normalized five-dimensional parent action",
                "the seed rho0 and the CKM/PMNS/confinement sectors",
            ],
            "classification": "constructive_reframing_not_resolution",
        },
    }

    assert proposed_determinant == -1
    assert corrected_determinant == 1
    assert proposed_decomposition == Fraction(1, 3)
    assert not results["exact_checks"]["form_degree"]["is_five_form"]
    assert results["exact_checks"]["form_degree"][
        "correct_template_is_five_form"
    ]
    assert beta_error < 1e-12
    assert results["exact_checks"]["six_channel_identity"]["passes"]

    Path("s2t_aps_orbifold_inflow_redteam_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()