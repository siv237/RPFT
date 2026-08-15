import json
import math
from pathlib import Path

import numpy as np


def main():
    # General finite semisimple algebra trace ambiguity.
    block_dimensions = [3, 2, 1]
    primitive_trace_weight_count = len(block_dimensions)
    normalized_free_weight_count = primitive_trace_weight_count - 1

    # Family menu projectors.
    identity4 = np.eye(4)
    all_ones4 = np.ones((4, 4))
    family_singlet = all_ones4 / 4.0
    family_triplet = identity4 - family_singlet

    family_loop_weights = {
        "singlet": float(np.trace(family_singlet)),
        "triplet": float(np.trace(family_triplet)),
    }
    family_normalized_state_weights = {
        name: value / value for name, value in family_loop_weights.items()
    }

    # SU(5) fundamental hypercharge normalization.
    y_fundamental = np.array(
        [-1.0 / 3.0, -1.0 / 3.0, -1.0 / 3.0, 1.0 / 2.0, 1.0 / 2.0]
    )
    trace_y_squared_fundamental = float(np.sum(y_fundamental**2))
    fundamental_nonabelian_index = 0.5
    hypercharge_normalization = (
        trace_y_squared_fundamental / fundamental_nonabelian_index
    )
    physical_gY_squared_over_unified = 1.0 / hypercharge_normalization
    sin2_unification = physical_gY_squared_over_unified / (
        1.0 + physical_gY_squared_over_unified
    )

    # One generation 10 + bar5 trace indices.
    states = [
        {"label": "Q", "multiplicity": 6, "Y": 1.0 / 6.0},
        {"label": "u_c", "multiplicity": 3, "Y": -2.0 / 3.0},
        {"label": "e_c", "multiplicity": 1, "Y": 1.0},
        {"label": "d_c", "multiplicity": 3, "Y": 1.0 / 3.0},
        {"label": "L", "multiplicity": 2, "Y": -1.0 / 2.0},
    ]
    raw_u1_index = sum(row["multiplicity"] * row["Y"] ** 2 for row in states)
    gut_u1_index = (3.0 / 5.0) * raw_u1_index
    su3_index = (
        2.0 * 0.5  # Q has two weak components
        + 0.5  # u_c
        + 0.5  # d_c
    )
    su2_index = (
        3.0 * 0.5  # Q has three colors
        + 0.5  # L
    )

    # Normalized constant-state matrix elements versus raw integrated norms.
    vol_rp3 = math.pi**2
    length_s1 = 2.0 * math.pi
    normalized_constant_matrix_elements = {
        "RP3": vol_rp3 * (1.0 / math.sqrt(vol_rp3)) ** 2,
        "S1": length_s1 * (1.0 / math.sqrt(length_s1)) ** 2,
    }
    raw_background_norms = {"RP3": vol_rp3, "S1": length_s1}

    results = {
        "status": "derived_multi_trace_scheme_passes_as_measure_bookkeeping_primitive_sector_traces_fail_hidden_weight_gate",
        "date": "2026-08-04",
        "hypothesis": (
            "Different sectors may use different measures because they are different reductions of "
            "one parent state/trace, not because each sector owns an independent normalization."
        ),
        "primitive_multi_trace_no_go": {
            "algebra": "A=direct sum_i M_ni(C)",
            "general_positive_trace": "tau(a)=sum_i w_i Tr_i(a_i), w_i>0",
            "example_block_dimensions": block_dimensions,
            "primitive_weights": primitive_trace_weight_count,
            "free_weights_after_tau(1)=1": normalized_free_weight_count,
            "verdict": (
                "Independent sector traces reintroduce continuous hidden parameters and are not an "
                "acceptable unification mechanism."
            ),
        },
        "derived_trace_dictionary": {
            "loop_trace": (
                "Tr(P O P): sums over all internal states and retains rank/multiplicity"
            ),
            "normalized_sector_average": (
                "Tr(P O P)/Tr(P): describes an average per normalized state and removes rank"
            ),
            "pure_state_expectation": "<psi,O psi> with ||psi||=1",
            "topological_period": (
                "integral of a connection around a quantized cycle; this is not a Hilbert trace"
            ),
            "rule": (
                "The observable type fixes which reduction is used; choosing between them after "
                "seeing a target is forbidden."
            ),
        },
        "family_menu_example": {
            "loop_weights": family_loop_weights,
            "normalized_state_weights": family_normalized_state_weights,
            "finding": (
                "The same parent trace counts three family modes in a loop but gives unit weight to "
                "a normalized state. The difference is discrete and not a fitted coefficient."
            ),
        },
        "SU5_gauge_trace": {
            "Tr5_Y2": trace_y_squared_fundamental,
            "Tr5_nonabelian_generator_squared": fundamental_nonabelian_index,
            "hypercharge_normalization_kY": hypercharge_normalization,
            "physical_gY2_over_unified_g2": physical_gY_squared_over_unified,
            "sin2_thetaW_at_unification": sin2_unification,
            "one_generation_indices": {
                "SU3": su3_index,
                "SU2": su2_index,
                "U1_GUT_normalized": gut_u1_index,
            },
            "finding": (
                "One SU5 representation trace induces different-looking subgroup traces but fixes "
                "their relative normalization: all one-generation indices equal 2 and kY=5/3."
            ),
        },
        "old_normalization_conflict": {
            "raw_background_norms": raw_background_norms,
            "normalized_constant_matrix_elements": normalized_constant_matrix_elements,
            "finding": (
                "Raw volumes belong to unnormalized background/loop norms. A normalized particle "
                "matrix element gives 1 on each factor. The multi-trace principle therefore does "
                "not rescue the old tau seed; it explains why using raw volumes there was a category error."
            ),
        },
        "gates": {
            "independent_sector_measures": {
                "passes": False,
                "finding": "a semisimple algebra with three blocks has two free normalized central weights",
            },
            "one_parent_trace_with_projectors": {
                "passes": True,
                "finding": "sector weights become fixed ranks, representation indices or normalized expectations",
            },
            "SU5_relative_gauge_normalization": {
                "passes": True,
                "finding": "one parent trace yields kY=5/3 and equal generation indices (2,2,2)",
            },
            "old_tau_volume_seed": {
                "passes": False,
                "finding": "particle-state normalization removes the RP3 and S1 volume factors",
            },
            "new_empirical_prediction": {
                "passes": False,
                "finding": "the scheme organizes measures but does not yet predict a new low-energy observable",
            },
        },
        "scientific_verdict": {
            "positive": (
                "The second wild hypothesis survives in a restricted form: different effective "
                "measures can be derived from one parent trace by observable type and fixed projectors."
            ),
            "negative": (
                "Primitive independent traces are hidden parameters, and the construction does not "
                "restore the rejected tau/Svac formulas."
            ),
            "next_gate": (
                "Build one total algebra A_menu tensor End(10+bar5) and verify that the family rank-one "
                "operator and SU5 gauge kinetic trace arise from the same normalized parent state."
            ),
        },
    }

    assert normalized_free_weight_count == 2
    assert abs(family_loop_weights["singlet"] - 1.0) < 1e-12
    assert abs(family_loop_weights["triplet"] - 3.0) < 1e-12
    assert abs(hypercharge_normalization - 5.0 / 3.0) < 1e-12
    assert abs(sin2_unification - 3.0 / 8.0) < 1e-12
    assert abs(su3_index - 2.0) < 1e-12
    assert abs(su2_index - 2.0) < 1e-12
    assert abs(gut_u1_index - 2.0) < 1e-12
    assert all(
        abs(value - 1.0) < 1e-12
        for value in normalized_constant_matrix_elements.values()
    )

    Path("s2t_multi_trace_measure_hypothesis_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "free_primitive_trace_weights": normalized_free_weight_count,
                "family_loop_weights": family_loop_weights,
                "SU5_indices": results["SU5_gauge_trace"]["one_generation_indices"],
                "kY": hypercharge_normalization,
                "sin2_unification": sin2_unification,
                "tau_seed_rescued": results["gates"]["old_tau_volume_seed"]["passes"],
                "next_gate": results["scientific_verdict"]["next_gate"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()