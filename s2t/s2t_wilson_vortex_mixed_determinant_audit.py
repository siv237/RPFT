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
    axis = np.array([1.0, 2.0, 3.0])
    axis /= np.linalg.norm(axis)
    angle = math.acos((26.0 - 9.0 * math.sqrt(15.0)) / 11.0)
    generator = angle * cross_matrix(axis)

    phases = [0.1, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0]
    potential_rows = []
    for phase in phases:
        determinant_abs = abs(2.0 * math.sin(phase / 2.0))
        potential_rows.append(
            {
                "phase": phase,
                "log_abs_det": math.log(determinant_abs),
                "fermion_effective_action": -math.log(determinant_abs),
            }
        )

    projected_connection = float(axis @ generator @ axis)
    kernel_residual = float(np.linalg.norm(generator @ axis))
    spectrum_plus = np.linalg.eigvalsh(1j * generator)
    spectrum_minus = np.linalg.eigvalsh(-1j * generator)
    nonzero_pair_abs_det = 4.0 * math.sin(angle / 2.0) ** 2

    results = {
        "status": "projected_line_determinant_fail_orientation_even_full_bundle",
        "date": "2026-08-07",
        "projected_line_gate": {
            "u_transpose_K_u": projected_connection,
            "K_u_norm": kernel_residual,
            "continuous_real_line_connection_dimension": 0,
            "finding": (
                "For a real antisymmetric SO(3) connection and its kernel axis, "
                "u^T K u=0 and K u=0. A real one-dimensional Majorana line has "
                "structure group O(1), whose Lie algebra is zero, so it carries "
                "no continuous projected U(1) holonomy."
            ),
        },
        "determinant_sign_gate": {
            "complex_periodic_abs_det": "2*abs(sin(phi/2))",
            "complex_effective_action": "-log(2*abs(sin(phi/2)))",
            "majorana_effective_action": "-(1/2)*log(2*abs(sin(phi/2)))",
            "minimum_on_0_to_2pi": "phi=pi",
            "not_a_minimum": "phi=pi/2",
            "rows": potential_rows,
        },
        "full_three_mode_gate": {
            "spectrum_for_k_plus": spectrum_plus.tolist(),
            "spectrum_for_k_minus": spectrum_minus.tolist(),
            "spectra_equal_as_sets": bool(
                np.allclose(spectrum_plus, spectrum_minus, atol=1e-12)
            ),
            "periodic_axis_zero_mode_present": True,
            "primed_nonzero_pair_abs_det": nonzero_pair_abs_det,
            "orientation_even": True,
            "finding": (
                "After removing the persistent axis zero mode, the nonzero pair "
                "contributes 4*sin(theta/2)^2. It is even under k->-k and cannot "
                "lock vortex and Wilson orientations."
            ),
        },
        "verdict": {
            "mixed_term_derived": False,
            "rank_23_promoted": False,
            "two_sector_gate_passed": False,
            "next_possible_route": (
                "Only an orientation-odd Pfaffian phase or anomaly-inflow term "
                "could distinguish the joint orientation. Its coefficient and "
                "reality properties must be derived from a bulk-boundary system; "
                "an absolute determinant cannot do so."
            ),
        },
    }

    assert abs(projected_connection) < 1e-12
    assert kernel_residual < 1e-12
    assert results["full_three_mode_gate"]["spectra_equal_as_sets"]
    Path("s2t_wilson_vortex_mixed_determinant_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results["verdict"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()