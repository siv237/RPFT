#!/usr/bin/env python3
import json
from pathlib import Path


OUTPUT_PATH = Path("s2t_v4_pati_salam_diagonal_connector_menu_results.json")


def main():
    required_goldstone = {
        "name": "G",
        "SU2R_isospin": 1,
        "SU4_representation": "10_symmetric",
        "C2_SU2R": 2.0,
        "C2_SU4": 4.5,
    }
    unwanted_mode = {
        "name": "X",
        "SU2R_isospin": 0,
        "SU4_representation": "6_antisymmetric",
        "C2_SU2R": 0.0,
        "C2_SU4": 2.5,
    }

    operators = {
        "identity_singlet": {
            "eigenvalue_G": 1.0,
            "eigenvalue_X": 1.0,
            "candidate_block": "real singlet",
            "representation_dimension": 1,
        },
        "SU2R_Casimir": {
            "eigenvalue_G": required_goldstone["C2_SU2R"],
            "eigenvalue_X": unwanted_mode["C2_SU2R"],
            "candidate_block": "right-adjoint (3,1,1)",
            "representation_dimension": 3,
        },
        "SU4_Casimir": {
            "eigenvalue_G": required_goldstone["C2_SU4"],
            "eigenvalue_X": unwanted_mode["C2_SU4"],
            "candidate_block": "four-color adjoint (1,1,15)",
            "representation_dimension": 15,
        },
        "combined_Casimir": {
            "eigenvalue_G": required_goldstone["C2_SU2R"]
            + required_goldstone["C2_SU4"],
            "eigenvalue_X": unwanted_mode["C2_SU2R"]
            + unwanted_mode["C2_SU4"],
            "candidate_block": "combined right/four-color diagonal block",
            "representation_dimension": 18,
        },
    }

    for operator in operators.values():
        operator["casimir_difference_X_minus_G"] = (
            operator["eigenvalue_X"] - operator["eigenvalue_G"]
        )
        operator["representations_distinguished_by_this_invariant"] = (
            operator["casimir_difference_X_minus_G"] != 0.0
        )

    output = {
        "gate": "version4_pati_salam_diagonal_connector_menu",
        "date": "2026-08-13",
        "mode_ledger": {
            "required_goldstone": required_goldstone,
            "unwanted_pseudogoldstone": unwanted_mode,
        },
        "operator_menu": operators,
        "minimal_dimension_sensitive_operator": "SU2R_Casimir",
        "preferred_target_scale_and_split_block": {
            "block": "Hermitian four-color diagonal block 1+15",
            "reason": (
                "its trace singlet can participate in scale transmutation while the 10 and "
                "6 sectors have different SU4 Casimirs; an actual VEV mass matrix is still "
                "uncomputed"
            ),
            "casimir_difference": operators["SU4_Casimir"][
                "casimir_difference_X_minus_G"
            ],
            "present_in_general_fundamental_branch": False,
            "present_in_constrained_composite_branch": True,
            "general_fundamental_Sigma_is_instead": "(2_R,2_L,1+15_4)",
            "high_scale_vev_and_potential_are_not_yet_derived": True,
        },
        "verdict": {
            "universal_singlet_rejected": True,
            "representation_separation_diagnostic_nonempty": True,
            "actual_adjoint_vev_mass_splitting_computed": False,
            "first_target_candidate": "weak-singlet four-color diagonal 1+15 block",
            "next_gate": (
                "derive the composite weak-singlet 15 from an explicit project finite "
                "Dirac block, then test its full potential and fermion masses"
            ),
        },
        "sources": ["arXiv:1304.8050", "arXiv:1801.00260", "arXiv:1905.04533"],
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")

    for name, operator in operators.items():
        print(
            name,
            "sensitivity=",
            operator["casimir_difference_X_minus_G"],
            "distinguished=",
            operator["representations_distinguished_by_this_invariant"],
        )
    print("first target candidate: weak-singlet four-color diagonal 1+15 block")


if __name__ == "__main__":
    main()