#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np


def cross_matrix(axis):
    x, y, z = axis
    return np.array(
        [[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]], dtype=float
    )


def main():
    source = json.loads(
        Path("s2t_continuous_wilson_gap_action_results.json").read_text(
            encoding="utf-8"
        )
    )
    axes = source["factor_axis_selector"]["summary"]["inverse_square"][
        "selected_axes"
    ]
    cosine = (26.0 - 9.0 * math.sqrt(15.0)) / 11.0
    angle = math.acos(cosine)

    rows = []
    for axis_values in axes:
        axis = np.array(axis_values, dtype=float)
        axis /= np.linalg.norm(axis)
        generator = angle * cross_matrix(axis)
        rank = int(np.linalg.matrix_rank(generator, tol=1e-10))
        kernel_projector = np.outer(axis, axis)
        reversed_projector = np.outer(-axis, -axis)
        rows.append(
            {
                "axis": axis.tolist(),
                "generator": generator.tolist(),
                "antisymmetric_error": float(
                    np.linalg.norm(generator + generator.T)
                ),
                "rank": rank,
                "nullity": 3 - rank,
                "singular_values": np.linalg.svd(
                    generator, compute_uv=False
                ).tolist(),
                "i_generator_eigenvalues": np.linalg.eigvalsh(
                    1j * generator
                ).tolist(),
                "kernel_residual": float(np.linalg.norm(generator @ axis)),
                "orientation_reversal_projector_error": float(
                    np.linalg.norm(kernel_projector - reversed_projector)
                ),
            }
        )

    all_rank_two = all(row["rank"] == 2 for row in rows)
    all_nullity_one = all(row["nullity"] == 1 for row in rows)
    all_orientation_independent = all(
        row["orientation_reversal_projector_error"] < 1e-12 for row in rows
    )

    results = {
        "status": "algebraic_generation_selector_pass_parent_action_conditional",
        "date": "2026-08-07",
        "input": {
            "core_majorana_multiplicity": 3,
            "wilson_cosine": "(26-9*sqrt(15))/11",
            "wilson_angle": angle,
            "geometrically_minimal_axis_count": len(axes),
        },
        "construction": {
            "core_action": "S_core,fam=(i/2) integral_gamma chi^T K_n chi",
            "generator": "K_n=theta_* [n]_cross=Log R_n(theta_*)",
        },
        "checks": {
            "all_selected_axes_rank_two": all_rank_two,
            "all_selected_axes_nullity_one": all_nullity_one,
            "orientation_reversal_preserves_kernel_projector": (
                all_orientation_independent
            ),
            "core_zero_modes_before_coupling": 3,
            "core_zero_modes_after_coupling": 1 if all_nullity_one else None,
            "ambient_complement_rank_if_restriction_map_exists": 23,
        },
        "rows": rows,
        "verdict": {
            "positive": (
                "The existing oriented SO(3) Wilson generator gives a rank-two "
                "antisymmetric coupling on three vortex Majorana modes and leaves "
                "one real core mode for either symmetry-related minimum."
            ),
            "open": (
                "A common action must still derive the restriction of the family "
                "Wilson connection to the B-L core, the ambient-to-core map and "
                "the 23+pi^-1 stiffness."
            ),
        },
    }

    assert all_rank_two
    assert all_nullity_one
    assert all_orientation_independent
    Path("s2t_family_wilson_majorana_core_selector_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results["checks"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()