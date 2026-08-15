import json
from pathlib import Path

import numpy as np


def main():
    menu_dimension = 4
    su5_matter_dimension = 15
    total_dimension = menu_dimension * su5_matter_dimension

    identity4 = np.eye(4)
    all_ones4 = np.ones((4, 4))
    triplet_projector = identity4 - all_ones4 / 4.0

    shear = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
        ]
    )
    odd_projector = 0.5 * (identity4 - shear)
    projector_nesting_error = float(
        np.linalg.norm(triplet_projector @ odd_projector - odd_projector)
    )

    identity15 = np.eye(su5_matter_dimension)
    physical_projector = np.kron(triplet_projector, identity15)
    heavy_family_projector = np.kron(odd_projector, identity15)

    physical_rank = int(np.linalg.matrix_rank(physical_projector, tol=1e-10))
    heavy_family_rank = int(
        np.linalg.matrix_rank(heavy_family_projector, tol=1e-10)
    )
    physical_conditional_heavy_weight = float(
        np.trace(heavy_family_projector) / np.trace(physical_projector)
    )

    # Per-generation SU(5)-normalized subgroup indices from 10+bar5.
    generation_indices = {"SU3": 2.0, "SU2": 2.0, "U1": 2.0}
    three_family_loop_indices = {
        name: float(np.trace(triplet_projector)) * value
        for name, value in generation_indices.items()
    }
    physical_normalized_indices = {
        name: value / physical_rank
        for name, value in three_family_loop_indices.items()
    }

    # Full matrix algebra and the projected physical matrix algebra each have a
    # unique normalized trace. No central sector weights exist inside M_n(C).
    results = {
        "status": "single_tensor_product_parent_trace_consistently_generates_family_rank_one_and_equal_SU5_gauge_indices",
        "date": "2026-08-04",
        "parent_algebra": {
            "Hilbert_space": "C4_spin_menu tensor (10 + bar5)",
            "dimension": total_dimension,
            "full_operator_algebra": "M60(C)",
            "normalized_trace": "tau60(X)=Tr60(X)/60",
            "uniqueness": "M60(C) has a unique normalized tracial state",
        },
        "physical_projection": {
            "projector": "P_phys=P3 tensor I15",
            "rank": physical_rank,
            "projected_algebra": "P_phys M60 P_phys isomorphic to M45(C)",
            "conditional_trace": "tau_phys(X)=Tr(P_phys X P_phys)/45",
            "unique_normalized_trace": True,
        },
        "family_operator": {
            "operator": "P_heavy=P_minus tensor I15",
            "rank": heavy_family_rank,
            "nesting_error_P3_Pminus": projector_nesting_error,
            "conditional_average_weight": physical_conditional_heavy_weight,
            "family_eigen_pattern": "(0,0,1) on the triplet",
            "interpretation": (
                "The same parent trace counts 15 states in the heavy family channel and 45 physical "
                "matter states total, giving the fixed conditional weight 1/3."
            ),
        },
        "gauge_operator": {
            "per_generation_indices": generation_indices,
            "three_family_loop_indices": three_family_loop_indices,
            "physical_normalized_indices": physical_normalized_indices,
            "equality_check": max(three_family_loop_indices.values())
            - min(three_family_loop_indices.values()),
            "interpretation": (
                "The physical triplet multiplies every SU5-normalized subgroup index by the same "
                "rank-three factor, preserving equality without sector weights."
            ),
        },
        "joint_consistency": {
            "relative_trace_parameter_count": 0,
            "family_and_gauge_use_same_parent_trace": True,
            "observable_reductions": {
                "family_mass_texture": "spectrum of P_heavy inside P_phys",
                "gauge_loop": "unnormalized trace of P_phys tensor T_a^2",
                "normalized_state": "conditional trace on M45 or pure-state expectation",
            },
            "finding": (
                "No normalization switch is required: the apparent different measures are fixed "
                "reductions of the unique matrix trace."
            ),
        },
        "gates": {
            "single_parent_trace": {
                "passes": True,
                "finding": "both structures live in the same M60 trace and its M45 conditional trace",
            },
            "no_hidden_relative_weight": {
                "passes": True,
                "finding": "full matrix algebras have unique normalized traces",
            },
            "family_rank_one": {
                "passes": True,
                "finding": "P_minus tensor I15 has rank 15 inside the rank-45 physical sector",
            },
            "equal_gauge_indices": {
                "passes": True,
                "finding": "three-family loop indices are (6,6,6)",
            },
            "dynamical_action": {
                "passes": False,
                "finding": "the trace state is fixed, but no action yet selects the projector scales or Higgs couplings",
            },
        },
        "scientific_verdict": {
            "positive": (
                "The restricted second hypothesis now closes algebraically: one unique parent matrix "
                "trace supports both the SU5 gauge normalization and the rank-one family texture."
            ),
            "limit": (
                "This is a normalization theorem for the III.0 construction, not a low-energy "
                "prediction. Dynamics, symmetry-breaking scales and light-family operators remain open."
            ),
            "next_gate": (
                "Construct the most general action invariant under SU5 x AGL(2,2), then determine "
                "whether the geometric shear term appears with a fixed relative coefficient or "
                "reintroduces a continuous coupling."
            ),
        },
    }

    assert total_dimension == 60
    assert physical_rank == 45
    assert heavy_family_rank == 15
    assert projector_nesting_error < 1e-12
    assert abs(physical_conditional_heavy_weight - 1.0 / 3.0) < 1e-12
    assert three_family_loop_indices == {"SU3": 6.0, "SU2": 6.0, "U1": 6.0}
    assert results["gauge_operator"]["equality_check"] == 0.0

    Path("s2t_parent_trace_tensor_product_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "total_dimension": total_dimension,
                "physical_rank": physical_rank,
                "heavy_family_rank": heavy_family_rank,
                "heavy_conditional_weight": physical_conditional_heavy_weight,
                "gauge_loop_indices": three_family_loop_indices,
                "relative_trace_parameters": 0,
                "next_gate": results["scientific_verdict"]["next_gate"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()