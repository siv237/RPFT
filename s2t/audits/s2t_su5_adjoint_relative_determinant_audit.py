import json
from pathlib import Path

import numpy as np


def main():
    target_data = json.loads(
        Path("s2t_finite_threshold_sign_cone_results.json").read_text()
    )
    relative_data = json.loads(
        Path("s2t_relative_holonomy_determinant_results.json").read_text()
    )
    target = np.array(
        target_data["target_construction"]["required_finite_shift_Y_2_3"],
        dtype=float,
    )
    mixed_index_direction = np.array([5.0, 3.0, 2.0])

    unrestricted_amplitude = float(
        np.dot(target, mixed_index_direction)
        / np.dot(mixed_index_direction, mixed_index_direction)
    )
    unrestricted_fit = unrestricted_amplitude * mixed_index_direction
    unrestricted_residual = target - unrestricted_fit
    unrestricted_relative_residual = float(
        np.linalg.norm(unrestricted_residual) / np.linalg.norm(target)
    )

    positive_amplitude = max(0.0, unrestricted_amplitude)
    positive_fit = positive_amplitude * mixed_index_direction
    positive_relative_residual = float(
        np.linalg.norm(target - positive_fit) / np.linalg.norm(target)
    )

    flat_bundle_unit_response = next(
        row["standard_FP_Gamma_twisted_minus_untwisted_massive"]
        for row in relative_data["RP3_Z2_flat_bundle_winding_radius_sweep"]
        if row["radius_ratio_R1_over_R3"] == 1.0
    )
    illustrative_vector = flat_bundle_unit_response * mixed_index_direction

    results = {
        "status": "SU5_adjoint_relative_determinant_is_scheme_safe_but_wrong_gauge_direction",
        "date": "2026-08-04",
        "construction": {
            "torsion_even_blocks": "C+W+Y, dimensions 8+3+1",
            "torsion_odd_blocks": "X+Xbar, dimensions 6+6",
            "relative_determinant_support": (
                "Only X/Xbar change between the trivial and P-twisted branches; "
                "the unbroken C/W/Y blocks cancel in the ratio."
            ),
            "mixed_pair_GUT_indices_Y_2_3": mixed_index_direction.tolist(),
            "generic_correction": "Delta alpha_inverse = A_rel*(5,3,2)",
            "reason_direction_is_fixed": (
                "X and Xbar are charge conjugates with the same spectrum and indices. "
                "Any common holonomy determinant changes only the scalar amplitude A_rel."
            ),
        },
        "target_comparison": {
            "required_shift_Y_2_3": target.tolist(),
            "required_sign_pattern": ["positive", "negative", "negative"],
            "relative_determinant_ray_sign_pattern_for_positive_A": [
                "positive",
                "positive",
                "positive",
            ],
            "positive_amplitude_best_fit": positive_fit.tolist(),
            "positive_amplitude_relative_L2_residual": positive_relative_residual,
            "unrestricted_best_amplitude": unrestricted_amplitude,
            "unrestricted_best_fit": unrestricted_fit.tolist(),
            "unrestricted_residual": unrestricted_residual.tolist(),
            "unrestricted_relative_L2_residual": unrestricted_relative_residual,
            "interpretation": (
                "The target is outside both the positive ray and the full one-dimensional "
                "span as an accurate approximation. Allowing an arbitrary overall sign "
                "still leaves a large residual."
            ),
        },
        "unit_radius_illustration": {
            "Maxwell_FP_flat_bundle_response": flat_bundle_unit_response,
            "index_weighted_vector_Y_2_3": illustrative_vector.tolist(),
            "warning": (
                "This amplitude is only illustrative because the broken SU5 vector/ghost "
                "complex is not identical to the Abelian Maxwell-FP complex. The direction "
                "no-go is independent of this normalization."
            ),
        },
        "escape_routes": [
            {
                "route": "split_X_multiplet_spectra",
                "status": "requires_new_SM_breaking_structure",
                "reason": (
                    "An irreducible (3,2) block has one common mass before additional "
                    "symmetry breaking. Splitting color and weak components destroys the "
                    "single SU5 projector explanation."
                ),
            },
            {
                "route": "twist_C_W_Y_separately",
                "status": "requires_extra_holonomies",
                "reason": (
                    "The declared P holonomy acts identically on all unbroken blocks. "
                    "Separate phases add new Wilson-line data and relative weights."
                ),
            },
            {
                "route": "add_multiple_representations",
                "status": "returns_to_threshold_cone_problem",
                "reason": (
                    "Additional index rays can span more directions, but their field "
                    "content and masses must be derived. The existing physical threshold "
                    "cone audit already failed for the minimal declared basis."
                ),
            },
        ],
        "scientific_verdict": {
            "positive": (
                "The SU5 twisted/untwisted ratio is a legitimate finite, scheme-safe "
                "topological response with a representation-fixed direction."
            ),
            "negative": (
                "That direction is (5,3,2), while the required low-energy repair has "
                "mixed signs. The minimal adjoint relative determinant cannot close the "
                "EW/QCD observables regardless of normalization or tower multiplicity."
            ),
            "surviving_use": (
                "Retain the relative determinant as a topology diagnostic or future blind "
                "observable, not as a repair term for the current gauge scorecard."
            ),
        },
    }

    assert unrestricted_amplitude < 0.0
    assert positive_relative_residual == 1.0
    assert unrestricted_relative_residual > 0.8

    Path("s2t_su5_adjoint_relative_determinant_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "target": target.tolist(),
                "direction": mixed_index_direction.tolist(),
                "positive_ray_residual": positive_relative_residual,
                "unrestricted_relative_residual": unrestricted_relative_residual,
                "best_amplitude": unrestricted_amplitude,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()