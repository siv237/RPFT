#!/usr/bin/env python3
import cmath
import json
from pathlib import Path


def phase_label(value):
    rounded = complex(round(value.real), round(value.imag))
    return {
        1.0 + 0.0j: "+1",
        -1.0 + 0.0j: "-1",
        0.0 + 1.0j: "+i",
        0.0 - 1.0j: "-i",
    }.get(rounded, str(value))


def main():
    consistency = json.loads(
        Path("s2t_bl_root_condensate_consistency_results.json").read_text(
            encoding="utf-8"
        )
    )

    root_phase = 1j
    bilinear_phase = root_phase**2
    ordinary_pair_phase = bilinear_phase.conjugate()
    torsion_phase = -1.0 + 0.0j
    twisted_pair_phase = ordinary_pair_phase * torsion_phase

    ordinary_vertex_phase = ordinary_pair_phase * bilinear_phase
    twisted_vertex_phase = twisted_pair_phase * bilinear_phase
    torsion_yukawa_phase = torsion_phase
    fully_twisted_vertex_phase = (
        torsion_yukawa_phase * twisted_pair_phase * bilinear_phase
    )

    constraints = {
        "root": root_phase,
        "bilinear": bilinear_phase,
        "ordinary_pair": ordinary_pair_phase,
        "twisted_pair": twisted_pair_phase,
        "ordinary_vertex": ordinary_vertex_phase,
        "twisted_vertex": twisted_vertex_phase,
        "torsion_yukawa": torsion_yukawa_phase,
        "fully_twisted_vertex": fully_twisted_vertex_phase,
    }

    results = {
        "status": "root_mass_uniform_condensate_trilemma_the_torsion_twist_moves_rather_than_removes_the_obstruction",
        "date": "2026-08-06",
        "closed_generator_phase_table": {
            name: phase_label(value) for name, value in constraints.items()
        },
        "three_requirements": {
            "order_four_sterile_root": {
                "condition": "r=+i",
                "passes": phase_label(root_phase) == "+i",
            },
            "ordinary_linear_Majorana_vertex": {
                "condition": "phi*r^2=+1",
                "required_pair_phase": phase_label(ordinary_pair_phase),
                "passes": phase_label(ordinary_vertex_phase) == "+1",
            },
            "uniform_parallel_pairing_vacuum": {
                "condition": "phi=+1 on the closed complement generator",
                "ordinary_pair_passes": phase_label(ordinary_pair_phase) == "+1",
                "torsion_twisted_pair_passes": phase_label(twisted_pair_phase)
                == "+1",
            },
        },
        "trilemma": {
            "ordinary_pairing": {
                "Yukawa_vertex_invariant": phase_label(ordinary_vertex_phase)
                == "+1",
                "uniform_parallel_condensate": phase_label(ordinary_pair_phase)
                == "+1",
                "finding": (
                    "The ordinary charge-minus-two field makes Phi N_c N_c invariant "
                    "but carries holonomy -1, so it cannot be a uniform parallel vacuum."
                ),
            },
            "torsion_twisted_pairing": {
                "uniform_parallel_condensate": phase_label(twisted_pair_phase)
                == "+1",
                "Yukawa_vertex_invariant_with_scalar_coupling": phase_label(
                    twisted_vertex_phase
                )
                == "+1",
                "finding": (
                    "The ambient torsion twist makes the pairing field parallel, but the "
                    "linear vertex then carries the residual torsion sign -1."
                ),
            },
            "torsion_twisted_yukawa_spurion": {
                "vertex_invariant": phase_label(fully_twisted_vertex_phase)
                == "+1",
                "spurion_parallel_and_nonzero": phase_label(torsion_yukawa_phase)
                == "+1",
                "finding": (
                    "A torsion-odd Yukawa coefficient restores the vertex algebraically "
                    "but is itself nontrivial on the closed generator. The obstruction is "
                    "moved into a new defect, zero, or chosen trivialization."
                ),
            },
        },
        "logical_no_go": {
            "simultaneously_possible_with_scalar_Yukawa": False,
            "statement": (
                "For r=i, vertex invariance requires phi=r^(-2)=-1, whereas a "
                "uniform parallel condensate requires phi=+1. No ordinary scalar "
                "assignment satisfies both."
            ),
            "allowed_nonuniform_route": (
                "Retain phi=-1 as a section with forced gradient/defect texture; the "
                "Majorana mass is then localized or spatially varying rather than a "
                "homogeneous bulk parameter."
            ),
        },
        "revision_of_torsion_rescue": {
            "previous_total_pair_holonomy": consistency[
                "torsion_twisted_pairing_scalar"
            ]["total_holonomy_on_y"],
            "condensate_compatibility_retained": True,
            "vertex_invariance_claim_retained": False,
            "corrected_status": (
                "The torsion twist solves the condensate holonomy only by transferring "
                "the nontrivial sign to the Yukawa map. It is not a complete rescue."
            ),
        },
        "scientific_verdict": {
            "negative": (
                "Minimal B-L plus a single ordinary or torsion-twisted charge-two field "
                "cannot provide all three of: an order-four sterile root, a scalar "
                "linear Majorana vertex, and a uniform parallel condensate."
            ),
            "surviving_branch": (
                "The root can still support a nonuniform class-D defect pairing texture, "
                "which is consistent with the earlier rank-one route but not with a "
                "homogeneous Majorana mass."
            ),
            "next_gate": (
                "Construct the lowest-action nonuniform twisted section and test whether "
                "its BdG kernel and fluctuation determinant remain rank one without a "
                "fitted Yukawa spurion."
            ),
        },
    }

    assert phase_label(bilinear_phase) == "-1"
    assert phase_label(ordinary_pair_phase) == "-1"
    assert phase_label(ordinary_vertex_phase) == "+1"
    assert phase_label(twisted_pair_phase) == "+1"
    assert phase_label(twisted_vertex_phase) == "-1"
    assert phase_label(fully_twisted_vertex_phase) == "+1"
    assert results["logical_no_go"]["simultaneously_possible_with_scalar_Yukawa"] is False
    assert results["revision_of_torsion_rescue"]["vertex_invariance_claim_retained"] is False

    Path("s2t_root_mass_condensate_trilemma_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()