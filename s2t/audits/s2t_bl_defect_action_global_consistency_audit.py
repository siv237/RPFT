#!/usr/bin/env python3
import cmath
import json
import math
from pathlib import Path


def close_complex(left, right, tolerance=1e-12):
    return abs(left - right) <= tolerance


def main():
    sterile_root = 1j
    sterile_pair_holonomy = sterile_root**2
    ordinary_pairing_holonomy = cmath.exp(-2j * math.pi / 2.0)
    torsion_holonomy = -1.0
    twisted_pairing_holonomy = (
        torsion_holonomy * ordinary_pairing_holonomy
    )

    ordinary_vertex_holonomy = (
        ordinary_pairing_holonomy * sterile_pair_holonomy
    )
    twisted_vertex_holonomy = (
        twisted_pairing_holonomy * sterile_pair_holonomy
    )

    results = {
        "status": "proposed_BL_defect_action_fails_global_bundle_and_derivation_gates_before_claimed_kill_gate",
        "date": "2026-08-07",
        "holonomy_data": {
            "sterile_root": [sterile_root.real, sterile_root.imag],
            "sterile_pair": [
                sterile_pair_holonomy.real,
                sterile_pair_holonomy.imag,
            ],
            "ordinary_charge_minus_two_pairing": [
                ordinary_pairing_holonomy.real,
                ordinary_pairing_holonomy.imag,
            ],
            "torsion_line": torsion_holonomy,
            "twisted_pairing": [
                twisted_pairing_holonomy.real,
                twisted_pairing_holonomy.imag,
            ],
        },
        "root_mass_condensate_trilemma": {
            "ordinary_field": {
                "parallel_nonzero_condensate_allowed": False,
                "Yukawa_vertex_scalar": close_complex(
                    ordinary_vertex_holonomy, 1.0
                ),
                "vertex_holonomy": [
                    ordinary_vertex_holonomy.real,
                    ordinary_vertex_holonomy.imag,
                ],
            },
            "torsion_twisted_field": {
                "parallel_nonzero_condensate_allowed": close_complex(
                    twisted_pairing_holonomy, 1.0
                ),
                "Yukawa_vertex_scalar": close_complex(
                    twisted_vertex_holonomy, 1.0
                ),
                "vertex_holonomy": [
                    twisted_vertex_holonomy.real,
                    twisted_vertex_holonomy.imag,
                ],
            },
            "finding": (
                "The ordinary field gives an invariant Majorana vertex but cannot "
                "be a global parallel condensate. The torsion-twisted field can be "
                "parallel, but its Majorana vertex is torsion-odd."
            ),
        },
        "spectrum_gate": {
            "ordinary_total_holonomy": -1,
            "ordinary_spectrum": "(2*pi*n+pi)/L",
            "twisted_total_holonomy": 1,
            "twisted_spectrum": "2*pi*n/L",
            "collaborator_used": "twisted total holonomy +1 together with half-shifted spectrum",
            "passes": False,
            "reason": (
                "Once the torsion and charge-two holonomies cancel, the covariant "
                "spectrum is integer shifted and contains a zero mode. Keeping the "
                "half shift double-counts the same sign."
            ),
        },
        "action_derivation_gates": {
            "pi_over_2_Wilson_line_selected_by_Maxwell_term": False,
            "reason_Wilson_line": (
                "For a flat Abelian connection f=0, the Maxwell term does not select "
                "one Wilson-line holonomy from the continuous flat moduli."
            ),
            "negative_pairing_mass_derived": False,
            "reason_pairing_mass": (
                "The action defines m_phi^2=-lambda*v^2 as an input, so the desired "
                "negative Hessian is assumed rather than generated."
            ),
            "core_profile_derived": False,
            "reason_core_profile": (
                "The tanh BdG profile and S_core coupling are inserted separately "
                "and are not obtained by solving the displayed global action."
            ),
            "rank24_module_derived": False,
            "reason_rank24": (
                "The displayed action contains the sterile field and pairing sector "
                "but does not construct the external 24-dimensional Majorana module."
            ),
            "canonical_kernel_quotient_weights_derived": False,
        },
        "kinetic_mixing_gate": {
            "trace_coefficient": 8.0 / 3.0,
            "trace_identity_valid": True,
            "second_predicted_observable": False,
            "reason": (
                "The trace coefficient is an algebraic beta-function input. The "
                "physical mixing also requires gauge couplings, boundary value, "
                "matter thresholds and running; these are not predicted by the "
                "displayed core-complement action."
            ),
        },
        "scientific_verdict": {
            "global_action_well_defined_as_written": False,
            "half_shifted_saddle_derived_in_twisted_branch": False,
            "mod2_kernel_status": "conditional_after_choosing_the_ordinary_nonuniform_defect_branch",
            "23_plus_pi_inverse_status": "canonical_metric_readout_not_action_derived",
            "closed_physical_predictions_added": 0,
            "correct_surviving_branch": (
                "Use the ordinary charge-two field with holonomy -1 as a nonuniform "
                "defect texture, keep the scalar Yukawa vertex, and derive its "
                "condensation and core profile dynamically. Do not add the torsion "
                "twist to the same scalar unless a torsion-odd Yukawa map is derived."
            ),
        },
    }

    assert close_complex(sterile_pair_holonomy, -1.0)
    assert close_complex(ordinary_pairing_holonomy, -1.0)
    assert close_complex(twisted_pairing_holonomy, 1.0)
    assert close_complex(ordinary_vertex_holonomy, 1.0)
    assert close_complex(twisted_vertex_holonomy, -1.0)
    assert results["spectrum_gate"]["passes"] is False
    assert (
        results["action_derivation_gates"][
            "pi_over_2_Wilson_line_selected_by_Maxwell_term"
        ]
        is False
    )
    assert results["scientific_verdict"][
        "global_action_well_defined_as_written"
    ] is False

    Path("s2t_bl_defect_action_global_consistency_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()