#!/usr/bin/env python3
import json
from pathlib import Path


OUTPUT_PATH = Path("s2t_v4_pati_salam_restricted_potential_gate_results.json")


def main():
    required_goldstones = 9
    unwanted_massless_scalars = 6

    output = {
        "gate": "version4_pati_salam_restricted_potential",
        "date": "2026-08-13",
        "source": "arXiv:1905.04533",
        "representation_correction": {
            "current_Sigma": "(2_R,2_L,1+15_4)",
            "previously_desired_block": "(1_R,1_L,1+15_4)",
            "true_four_color_adjoint_target": "(1_R,1_L,15_4)",
            "true_adjoint_present_in_general_fundamental_menu": False,
            "true_adjoint_present_in_composite_first_order_branch": True,
            "reason_current_Sigma_cannot_take_high_scale_vev": (
                "a nonzero vector in the SU(2)_L doublet has no invariant direction under "
                "the full SU(2)_L group"
            ),
        },
        "restricted_potential": {
            "canonical_form": (
                "-M^2/2 Tr(Hdot^2+Sigma^2+H^2) + g^2/4 Tr(2 Hdot^4 + "
                "2 H^4 + 4|Hdotbar Sigma|^2 + 4|Hbar Sigma|^2 + "
                "|Sigma Sigmabar|^2 + mixed terms)"
            ),
            "required_goldstones": required_goldstones,
            "unwanted_massless_scalars": unwanted_massless_scalars,
            "total_massless_at_candidate": required_goldstones
            + unwanted_massless_scalars,
            "negative_hessian_directions_exist": True,
            "candidate_is_local_minimum": False,
            "candidate_is_local_maximum": True,
            "missing_invariants": [
                "(Tr(Hdot^2))^2",
                "Tr(Hdot^2) Tr(Sigma^2)",
            ],
        },
        "fermion_gate": {
            "Sigma_connects_left_and_right_fermions": True,
            "high_scale_bidoublet_vev_preserves_SU2L": False,
            "high_scale_bidoublet_vev_is_acceptable": False,
        },
        "verdict": {
            "general_fundamental_1_plus_15_candidate_passed": False,
            "composite_first_order_adjoint_branch_closed": False,
            "casimir_sensitivity_result_survives_as_design_requirement": True,
            "minimal_model_improvement": (
                "derive the composite weak-singlet adjoint from an explicit project "
                "Pati-Salam Dirac block or expand the geometry with connected diagonal "
                "fields; then compute the full potential"
            ),
            "next_gate": (
                "construct the project Pati-Salam finite block and audit the legitimacy of "
                "the composite (1,1,15) plus a diagonal-real-singlet extension"
            ),
        },
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")

    print("required Goldstones:", required_goldstones)
    print("unwanted massless scalars:", unwanted_massless_scalars)
    print("total massless:", required_goldstones + unwanted_massless_scalars)
    print("current Sigma high-scale VEV preserves SU(2)_L: False")
    print("general fundamental 1+15 candidate passed: False")


if __name__ == "__main__":
    main()