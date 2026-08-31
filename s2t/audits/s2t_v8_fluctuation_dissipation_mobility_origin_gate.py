#!/usr/bin/env python3
"""Test common-trace fluctuation-dissipation candidates for QMS mobility."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_fluctuation_dissipation_mobility_origin_gate_results.json"
TOL = 1.0e-10

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v8_common_chain_dirichlet_rate_metric_gate import (  # noqa: E402
    TERM_ORDER,
    generator_diagnostics,
)
from s2t_v8_kms_nontracial_relative_rate_selector_gate import (  # noqa: E402
    assemble,
    block_diagonal,
    central_density,
)
from s2t_v8_modular_bohr_parent_origin_gate import directed_family_generator  # noqa: E402


def normalized(values: np.ndarray) -> list[float]:
    return [float(value) for value in values / np.sum(values)]


def main() -> None:
    symmetric_terms, _, transfers = assemble()
    ratio = float(np.exp(-2.0))
    source_density, target_density = central_density(ratio)
    kms_metric = block_diagonal(
        [source_density * np.eye(121), target_density * np.eye(100)]
    )
    named_terms = {
        "linking": directed_family_generator(transfers["linking"], ratio, 1.0),
        "SU3": symmetric_terms["SU3"],
        "SU2": symmetric_terms["SU2"],
        "U1": symmetric_terms["U1"],
        "QLYR": directed_family_generator(transfers["QLYR"], ratio, 1.0),
        "XLdR": directed_family_generator(transfers["XLdR"], ratio, 1.0),
    }

    component_counts = np.array([1.0, 8.0, 3.0, 1.0, 6.0, 6.0])
    superoperator_norms = np.array(
        [np.linalg.norm(named_terms[name]) for name in TERM_ORDER]
    )
    candidate_vectors = {
        "equal_coefficient_per_family": np.ones(6),
        "equal_mobility_per_noise_component": np.ones(6),
        "equal_total_noise_power_per_family": 1.0 / component_counts,
        "equal_superoperator_HS_length": 1.0 / superoperator_norms,
        "equal_squared_superoperator_HS_length": 1.0 / superoperator_norms**2,
    }
    candidate_rows = []
    normalized_vectors = []
    for name, vector in candidate_vectors.items():
        weights = dict(zip(TERM_ORDER, vector))
        diagnostics = generator_diagnostics(named_terms, weights, kms_metric)
        assert diagnostics["fixed_algebra_dimension"] == 1
        assert diagnostics["KMS_symmetry_residual"] < TOL
        normed = np.array(normalized(vector))
        normalized_vectors.append(normed)
        candidate_rows.append(
            {
                "rule": name,
                "raw_weights": [float(value) for value in vector],
                "normalized_weights": normed.tolist(),
                "decay_gap": diagnostics["decay_gap"],
                "fixed_algebra_dimension": diagnostics["fixed_algebra_dimension"],
                "KMS_symmetry_residual": diagnostics["KMS_symmetry_residual"],
            }
        )
    distinct_vectors = {
        tuple(np.round(vector, 12)) for vector in normalized_vectors
    }
    assert len(distinct_vectors) == 4  # first two are intentionally identical
    pairwise_spread = max(
        float(np.linalg.norm(left - right))
        for i, left in enumerate(normalized_vectors)
        for right in normalized_vectors[i + 1 :]
    )
    assert pairwise_spread > 0.1

    field_metric_result = json.loads(
        (ROOT / "s2t/results/s2t_v7_edge_coherence_field_space_superconnection_gate_results.json").read_text()
    )
    kinetic = field_metric_result["kinetic_metric"]
    kinetic_values = np.array(kinetic["eigenvalues"])
    assert np.linalg.norm(kinetic_values - 3.0) < TOL
    cross_mobility = 1.0 / kinetic_values
    assert np.max(cross_mobility) - np.min(cross_mobility) < TOL

    placement = field_metric_result["placement_in_full_strict_graph"]
    assert placement["selected_new_edges_inside_block"] == 2
    assert placement["selected_new_edges_outside_block"] == 4
    assert not field_metric_result["verdict"]["absolute_spacetime_heat_kernel_normalization_closed"]

    # Equal family coefficients are not frame-invariant.  Rescaling one jump
    # family by s multiplies its dissipator by s^2; compensating its mobility
    # by s^-2 leaves the physical generator unchanged.
    rescaling_tests = []
    reference_weights = np.ones(6)
    reference_generator = sum(
        (reference_weights[i] * named_terms[name] for i, name in enumerate(TERM_ORDER)),
        np.zeros((221, 221), complex),
    )
    for index, scale in enumerate((0.25, 0.5, 2.0, 4.0)):
        name = TERM_ORDER[index]
        rescaled_terms = dict(named_terms)
        rescaled_terms[name] = scale**2 * named_terms[name]
        compensated_weights = reference_weights.copy()
        compensated_weights[index] /= scale**2
        rebuilt = sum(
            (
                compensated_weights[i] * rescaled_terms[family]
                for i, family in enumerate(TERM_ORDER)
            ),
            np.zeros((221, 221), complex),
        )
        residual = float(np.linalg.norm(rebuilt - reference_generator))
        assert residual < TOL
        rescaling_tests.append(
            {
                "family": name,
                "jump_frame_scale": scale,
                "compensated_mobility": float(compensated_weights[index]),
                "generator_invariance_residual": residual,
            }
        )

    assembly_source = (
        ROOT / "s2t/audits/s2t_v8_kms_nontracial_relative_rate_selector_gate.py"
    ).read_text(encoding="utf-8")
    assert "normalized = variation / np.linalg.norm" in assembly_source
    assert "linking = block_generator(incidence)" in assembly_source

    parent_result = json.loads(
        (ROOT / "s2t/results/s2t_v8_physical_correlation_kernel_parent_action_origin_gate_results.json").read_text()
    )
    assert not parent_result["verdict"]["existing_parent_action_uniquely_determines_C_tau"]

    result = {
        "date": "2026-08-29",
        "gate": "version8_fluctuation_dissipation_mobility_origin_gate",
        "common_trace_cross_field_metric": {
            "formula": "Tr(delta D_B delta D_B)=3 Tr(delta B delta B*)",
            "real_dimension": int(len(kinetic_values)),
            "metric_eigenvalue": 3.0,
            "Einstein_mobility_eigenvalue_up_to_common_scale": 1.0 / 3.0,
            "QLYR_XLdR_relative_mobility": 1.0,
            "cross_relative_isotropy_derived_on_B_carrier": True,
            "absolute_heat_kernel_normalization_derived": False,
            "selected_edges_inside_B": placement["selected_new_edges_inside_block"],
            "selected_edges_outside_B": placement["selected_new_edges_outside_block"],
            "covers_all_six_QMS_families": False,
        },
        "family_normalization_ambiguity": {
            "family_order": TERM_ORDER,
            "component_counts": [int(value) for value in component_counts],
            "superoperator_HS_norms": [float(value) for value in superoperator_norms],
            "candidate_rules": candidate_rows,
            "distinct_normalized_rate_vectors": len(distinct_vectors),
            "maximum_pairwise_normalized_weight_distance": pairwise_spread,
            "all_candidates_primitive_and_KMS": True,
            "one_rule_selected_by_common_trace_alone": False,
        },
        "noise_frame_rescaling": {
            "identity": "D[sV]=s^2 D[V], kappa' = kappa/s^2",
            "tests": rescaling_tests,
            "equal_coefficients_are_frame_invariant_without_canonical_jump_norm": False,
            "current_assembly_normalizes_cross_variations_but_not_linking_incidence_by_same_rule": True,
        },
        "fluctuation_dissipation_scope": {
            "KMS_state_fixes_forward_backward_ratio": True,
            "trace_kinetic_metric_partially_fixes_cross_relative_mobility": True,
            "linking_mobility_derived": False,
            "SU3_mobility_derived": False,
            "SU2_mobility_derived": False,
            "U1_mobility_derived": False,
            "bath_spectral_density_or_canonical_noise_frame_required": True,
        },
        "verdict": {
            "cross_Q_X_relative_mobility_partial_pass": True,
            "single_six_family_mobility_derived": False,
            "absolute_physical_time_derived": False,
            "status": "cross_trace_mobility_partial_pass_full_noise_frame_and_rate_metric_no_go",
            "next_gate": "version8_canonical_noise_frame_common_trace_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()