#!/usr/bin/env python3
"""Минимальная физически инвариантная опора спектрального дефекта H15."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_minimal_support_gate_results.json"


def load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def commutant_dimension(generators: list[np.ndarray], tol: float = 1.0e-10) -> int:
    """Complex dimension of the simultaneous matrix commutant."""
    n = generators[0].shape[0]
    identity = np.eye(n, dtype=complex)
    constraints = [
        np.kron(generator.T, identity) - np.kron(identity, generator)
        for generator in generators
    ]
    stacked = np.vstack(constraints)
    return n * n - int(np.linalg.matrix_rank(stacked, tol=tol))


def block_generators(blocks: list[tuple[str, int]]) -> tuple[list[np.ndarray], dict[str, slice]]:
    """Generators whose associative closure is a full matrix algebra per block."""
    total = sum(size for _, size in blocks)
    generators: list[np.ndarray] = []
    slices: dict[str, slice] = {}
    offset = 0
    for name, size in blocks:
        sl = slice(offset, offset + size)
        slices[name] = sl

        projection = np.zeros((total, total), dtype=complex)
        projection[sl, sl] = np.eye(size)
        generators.append(projection)

        if size > 1:
            diagonal = np.zeros((total, total), dtype=complex)
            diagonal[sl, sl] = np.diag(np.arange(1, size + 1, dtype=float))
            generators.append(diagonal)

            cycle = np.zeros((total, total), dtype=complex)
            for local_index in range(size):
                i = offset + local_index
                j = offset + ((local_index + 1) % size)
                cycle[i, j] = 1.0
            generators.append(cycle)

        offset += size
    return generators, slices


def bridge(total: int, source: slice, target: slice) -> np.ndarray:
    """One nonzero self-adjoint intertwiner; block irreducibility spreads it."""
    matrix = np.zeros((total, total), dtype=complex)
    i = source.start
    j = target.start
    matrix[i, j] = 1.0
    matrix[j, i] = 1.0
    return matrix


def projector(total: int, slices: dict[str, slice], names: list[str]) -> np.ndarray:
    result = np.zeros((total, total), dtype=complex)
    for name in names:
        sl = slices[name]
        result[sl, sl] = np.eye(sl.stop - sl.start)
    return result


def max_commutator_residual(projection: np.ndarray, generators: list[np.ndarray]) -> float:
    return max(float(np.linalg.norm(projection @ g - g @ projection)) for g in generators)


def main() -> None:
    h15 = load("s2t_v5_h15_neutrino_degree_split_gate_results.json")
    oneforms = load("s2t_v5_h15_physical_oneform_bimodule_gate_results.json")
    toeplitz = load("s2t_v5_one_seventh_toeplitz_boundary_map_gate_results.json")
    real = load("s2t_v5_real_toeplitz_ko6_parent_lift_gate_results.json")
    transfer = load("s2t_v5_local_defect_transfer_operator_gate_results.json")

    observed = h15["architecture_comparison"]["H15"]["observed_blocks"]
    blocks = [(name, int(observed[name])) for name in ("Q_L", "L_L", "u_R", "d_R", "e_R")]
    total = sum(size for _, size in blocks)
    gauge_generators, slices = block_generators(blocks)

    charged_edges = [("Q_L", "u_R"), ("Q_L", "d_R"), ("L_L", "e_R")]
    yukawa_generators = [bridge(total, slices[left], slices[right]) for left, right in charged_edges]
    physical_generators = gauge_generators + yukawa_generators

    full_diagonal = np.diag(np.arange(1, total + 1, dtype=float)).astype(complex)
    full_cycle = np.zeros((total, total), dtype=complex)
    for i in range(total):
        full_cycle[i, (i + 1) % total] = 1.0

    p_quark = projector(total, slices, ["Q_L", "u_R", "d_R"])
    p_lepton = projector(total, slices, ["L_L", "e_R"])
    grading = projector(total, slices, ["Q_L", "L_L"]) - projector(
        total, slices, ["u_R", "d_R", "e_R"]
    )

    real_swap = np.block(
        [
            [np.zeros((total, total)), np.eye(total)],
            [np.eye(total), np.zeros((total, total))],
        ]
    )
    p_quark_real = np.block(
        [[p_quark, np.zeros_like(p_quark)], [np.zeros_like(p_quark), p_quark]]
    )
    p_lepton_real = np.block(
        [[p_lepton, np.zeros_like(p_lepton)], [np.zeros_like(p_lepton), p_lepton]]
    )

    gauge_commutant = commutant_dimension(gauge_generators)
    physical_commutant = commutant_dimension(physical_generators)
    control_commutant = commutant_dimension([full_diagonal, full_cycle])

    component_ranks = {
        "quark_Q_L_plus_u_R_plus_d_R": int(round(np.trace(p_quark).real)),
        "lepton_L_L_plus_e_R": int(round(np.trace(p_lepton).real)),
    }
    oriented_indices = {
        name: {"positive_winding": -rank, "negative_winding": rank}
        for name, rank in component_ranks.items()
    }
    coefficient_ambient_rank = int(toeplitz["coefficient_projection"]["ambient_rank"])
    component_weights = {
        name: rank / coefficient_ambient_rank for name, rank in component_ranks.items()
    }

    result = {
        "gate": "version6_spectral_transition_minimal_support_gate",
        "input_certificates": {
            "H15_observed_blocks": dict(blocks),
            "charged_edges": [list(edge) for edge in charged_edges],
            "charged_edge_count": len(oneforms["charged_edge_multiplicity_space"]["edges"]),
            "coefficient_projection_rank": toeplitz["coefficient_projection"]["rank"],
            "balanced_real_defect_rank": real["balanced_real_cycle"]["total_compact_defect_rank"],
            "transfer_internal_action": transfer["bimodule_intertwiner_classification"]["consequence_for_M20x15"],
        },
        "algebra_boundary": {
            "full_control_corner": "M15(C)",
            "full_control_corner_commutant_dimension": control_commutant,
            "full_control_corner_irreducible": control_commutant == 1,
            "full_control_corner_is_physical_coordinate_algebra": False,
            "reason": "the Morita linking gate explicitly keeps M15 as a full control reading; promoting it would allow arbitrary quark-lepton mixing",
        },
        "physical_support_classification": {
            "gauge_irreducible_block_ranks": sorted(size for _, size in blocks),
            "gauge_commutant_dimension": gauge_commutant,
            "nonzero_charged_Yukawa_graph_components": {
                "quark": ["Q_L", "u_R", "d_R"],
                "lepton": ["L_L", "e_R"],
            },
            "component_ranks": component_ranks,
            "physical_gauge_plus_Yukawa_commutant_dimension": physical_commutant,
            "quark_projector_rank": component_ranks["quark_Q_L_plus_u_R_plus_d_R"],
            "lepton_projector_rank": component_ranks["lepton_L_L_plus_e_R"],
            "projectors_sum_to_identity_residual": float(np.linalg.norm(p_quark + p_lepton - np.eye(total))),
            "projectors_orthogonality_residual": float(np.linalg.norm(p_quark @ p_lepton)),
            "quark_physical_commutator_residual": max_commutator_residual(p_quark, physical_generators),
            "lepton_physical_commutator_residual": max_commutator_residual(p_lepton, physical_generators),
            "quark_grading_commutator_residual": float(np.linalg.norm(p_quark @ grading - grading @ p_quark)),
            "lepton_grading_commutator_residual": float(np.linalg.norm(p_lepton @ grading - grading @ p_lepton)),
            "rank_15_physically_irreducible": physical_commutant == 1,
            "minimal_connected_support_rank_if_all_three_charged_edges_are_nonzero": min(component_ranks.values()),
            "minimal_gauge_only_support_rank": min(size for _, size in blocks),
            "conditionality": "the 12+3 split is preserved even when all three allowed charged edges are active; vanishing edge amplitudes can only split it further",
        },
        "real_grading_and_boundary_checks": {
            "KO6_preserves_quark_lepton_label": True,
            "real_quark_rank": int(round(np.trace(p_quark_real).real)),
            "real_lepton_rank": int(round(np.trace(p_lepton_real).real)),
            "real_projectors_commute_with_orientation_swap_residual": {
                "quark": float(np.linalg.norm(p_quark_real @ real_swap - real_swap @ p_quark_real)),
                "lepton": float(np.linalg.norm(p_lepton_real @ real_swap - real_swap @ p_lepton_real)),
            },
            "oriented_component_indices": oriented_indices,
            "component_normalized_weights": component_weights,
            "component_weight_sum": sum(component_weights.values()),
            "full_oriented_indices_reconstructed": {
                "positive_winding": sum(item["positive_winding"] for item in oriented_indices.values()),
                "negative_winding": sum(item["negative_winding"] for item in oriented_indices.values()),
            },
            "each_real_component_integer_index": 0,
            "Toeplitz_boundary_binds_components_together": False,
        },
        "transfer_check": {
            "transfer_is_scalar_on_internal_Morita_carrier": True,
            "commutes_with_quark_and_lepton_projectors": True,
            "mixes_quark_and_lepton_components": False,
            "protects_rank_15_as_one_packet": False,
            "nonzero_component_gaps_derived": False,
        },
        "verdict": {
            "rank_15_is_algebraically_composite": True,
            "rank_15_is_composite_under_current_physical_algebra": True,
            "full_M15_irreducibility_is_physically_admissible_proof": False,
            "strongest_current_nonzero_edge_decomposition": "15=12+3",
            "minimal_current_connected_complex_support_rank": 3,
            "rank_3_declared_elementary_particle": False,
            "rank_15_interpretation": "one-generation charged matter package, not a demonstrated elementary spectral atom",
            "physical_closure": False,
            "status": "the null hypothesis fails: current physical symmetries preserve proper rank-12 and rank-3 subprojections; topology, KO6 and scalar transfer do not resew them",
        },
        "next_gate": "version6_spectral_transition_component_boundary_gate",
    }

    assert total == 15
    assert gauge_commutant == 5
    assert physical_commutant == 2
    assert control_commutant == 1
    assert component_ranks == {
        "quark_Q_L_plus_u_R_plus_d_R": 12,
        "lepton_L_L_plus_e_R": 3,
    }
    assert result["physical_support_classification"]["projectors_sum_to_identity_residual"] < 1.0e-12
    assert result["physical_support_classification"]["projectors_orthogonality_residual"] < 1.0e-12
    assert result["physical_support_classification"]["quark_physical_commutator_residual"] < 1.0e-12
    assert result["physical_support_classification"]["lepton_physical_commutator_residual"] < 1.0e-12
    assert result["real_grading_and_boundary_checks"]["real_quark_rank"] == 24
    assert result["real_grading_and_boundary_checks"]["real_lepton_rank"] == 6
    assert result["real_grading_and_boundary_checks"]["full_oriented_indices_reconstructed"] == {
        "positive_winding": -15,
        "negative_winding": 15,
    }
    assert abs(result["real_grading_and_boundary_checks"]["component_weight_sum"] - 1.0 / 7.0) < 1.0e-15

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()