#!/usr/bin/env python3
"""Test the chain-number operator as an internal modular Bohr Hamiltonian."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh, svdvals


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_modular_bohr_parent_origin_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import physical_blocks  # noqa: E402
from s2t_v8_kms_nontracial_relative_rate_selector_gate import (  # noqa: E402
    assemble,
    block_diagonal,
    central_density,
    pair_vector,
)


def directed_transfer_generator(
    incidence: np.ndarray, upward_rate: float, downward_rate: float
) -> np.ndarray:
    """Heisenberg generator for source->target V and target->source V*."""
    target_dimension, source_dimension = incidence.shape
    source_gram = incidence.conj().T @ incidence
    target_gram = incidence @ incidence.conj().T
    zero_st = np.zeros((source_dimension**2, target_dimension**2), complex)
    zero_ts = np.zeros((target_dimension**2, source_dimension**2), complex)
    upward = np.block(
        [
            [
                -0.5 * np.kron(np.eye(source_dimension), source_gram)
                - 0.5 * np.kron(source_gram.T, np.eye(source_dimension)),
                np.kron(incidence.T, incidence.conj().T),
            ],
            [zero_ts, np.zeros((target_dimension**2, target_dimension**2))],
        ]
    )
    downward = np.block(
        [
            [np.zeros((source_dimension**2, source_dimension**2)), zero_st],
            [
                np.kron(incidence.conj(), incidence),
                -0.5 * np.kron(np.eye(target_dimension), target_gram)
                - 0.5 * np.kron(target_gram.T, np.eye(target_dimension)),
            ],
        ]
    )
    return upward_rate * upward + downward_rate * downward


def directed_family_generator(
    operators: list[np.ndarray], upward_rate: float, downward_rate: float
) -> np.ndarray:
    return sum(
        (
            directed_transfer_generator(operator, upward_rate, downward_rate)
            for operator in operators
        ),
        np.zeros((221, 221), complex),
    )


def kernel_dimension(matrix: np.ndarray) -> int:
    singular_values = svdvals(matrix)
    threshold = max(TOL, 1.0e-11 * float(singular_values[0]))
    return int(np.sum(singular_values <= threshold))


def orientation_row(
    name: str,
    beta_delta: float,
    terms: dict[str, np.ndarray],
    transfers: dict[str, list[np.ndarray]],
) -> dict:
    ratio = float(np.exp(-beta_delta))
    source_density, target_density = central_density(ratio)
    generator = terms["SU3"] + terms["SU2"] + terms["U1"]
    for family in ("linking", "QLYR", "XLdR"):
        generator += directed_family_generator(
            transfers[family], upward_rate=ratio, downward_rate=1.0
        )

    metric = block_diagonal(
        [source_density * np.eye(121), target_density * np.eye(100)]
    )
    sqrt_metric = block_diagonal(
        [np.sqrt(source_density) * np.eye(121), np.sqrt(target_density) * np.eye(100)]
    )
    inverse_sqrt_metric = block_diagonal(
        [
            np.eye(121) / np.sqrt(source_density),
            np.eye(100) / np.sqrt(target_density),
        ]
    )
    density_vector = pair_vector(
        source_density * np.eye(11), target_density * np.eye(10)
    )
    identity_vector = pair_vector(np.eye(11), np.eye(10))
    kms_residual = float(
        np.linalg.norm(metric @ generator - generator.conj().T @ metric)
    )
    stationarity_residual = float(
        np.linalg.norm(generator.conj().T @ density_vector)
    )
    unital_residual = float(np.linalg.norm(generator @ identity_vector))
    symmetric = sqrt_metric @ generator @ inverse_sqrt_metric
    similarity_self_adjoint_residual = float(
        np.linalg.norm(symmetric - symmetric.conj().T)
    )
    spectrum = eigvalsh((symmetric + symmetric.conj().T) / 2.0)
    fixed_dimension = kernel_dimension(generator)
    gap = float(-spectrum[-fixed_dimension - 1])

    assert kms_residual < TOL
    assert stationarity_residual < TOL
    assert unital_residual < TOL
    assert similarity_self_adjoint_residual < TOL
    assert fixed_dimension == 1
    assert gap > 0.0
    assert np.max(spectrum) < TOL

    source_probability = 11.0 * source_density
    target_probability = 10.0 * target_density
    entropy = float(
        -11.0 * source_density * np.log(source_density)
        - 10.0 * target_density * np.log(target_density)
    )
    return {
        "orientation": name,
        "endpoint_chain_number": (
            "0*I11 direct_sum 2*I10"
            if beta_delta > 0
            else "2*I11 direct_sum 0*I10"
        ),
        "beta_Delta": beta_delta,
        "target_to_source_density_ratio": ratio,
        "upward_to_downward_rate_ratio": ratio,
        "source_density_per_state": source_density,
        "target_density_per_state": target_density,
        "source_total_probability": source_probability,
        "target_total_probability": target_probability,
        "stationary_entropy": entropy,
        "KMS_symmetry_residual": kms_residual,
        "stationarity_residual": stationarity_residual,
        "unital_residual": unital_residual,
        "KMS_similarity_self_adjoint_residual": similarity_self_adjoint_residual,
        "fixed_algebra_dimension": fixed_dimension,
        "decay_gap": gap,
        "minimum_eigenvalue": float(spectrum[0]),
        "maximum_eigenvalue": float(spectrum[-1]),
        "primitive": True,
    }


def best_bohr_fit(
    operator: np.ndarray, source_hamiltonian: np.ndarray, target_hamiltonian: np.ndarray
) -> dict:
    image = target_hamiltonian @ operator - operator @ source_hamiltonian
    norm_squared = float(np.linalg.norm(operator) ** 2)
    frequency = float(np.real(np.vdot(operator, image)) / norm_squared)
    residual = float(np.linalg.norm(image - frequency * operator) / np.linalg.norm(operator))
    return {"best_frequency": frequency, "relative_residual": residual}


def main() -> None:
    terms, _, transfers = assemble()
    reference, _, _, _ = physical_blocks()

    forward = orientation_row(
        "coisometry_direction_11_to_10", 2.0, terms, transfers
    )
    reverse = orientation_row(
        "reversed_chain_direction_10_to_11", -2.0, terms, transfers
    )

    # At zero gap the directed construction returns the symmetric generator.
    trace_generator = terms["SU3"] + terms["SU2"] + terms["U1"]
    for family in ("linking", "QLYR", "XLdR"):
        trace_generator += directed_family_generator(transfers[family], 1.0, 1.0)
    original_generator = sum(terms.values(), np.zeros((221, 221), complex))
    trace_recovery_residual = float(np.linalg.norm(trace_generator - original_generator))
    assert trace_recovery_residual < TOL

    # The polar Gram pair intertwines the reference incidence at zero Bohr
    # frequency, but it does not give a common eigenfrequency to cross arrows.
    source_gram = reference.conj().T @ reference
    target_gram = reference @ reference.conj().T
    gram_tests = {}
    for family, operators in transfers.items():
        gram_tests[family] = [
            best_bohr_fit(operator, source_gram, target_gram)
            for operator in operators
        ]
    assert gram_tests["linking"][0]["relative_residual"] < TOL
    cross_gram_minimum_residual = min(
        row["relative_residual"]
        for family in ("QLYR", "XLdR")
        for row in gram_tests[family]
    )
    assert cross_gram_minimum_residual > 1.0e-3

    chain_source = np.zeros((11, 11))
    chain_target = 2.0 * np.eye(10)
    chain_bohr_tests = {
        family: [
            best_bohr_fit(operator, chain_source, chain_target)
            for operator in operators
        ]
        for family, operators in transfers.items()
    }
    maximum_chain_bohr_residual = max(
        row["relative_residual"]
        for rows in chain_bohr_tests.values()
        for row in rows
    )
    assert maximum_chain_bohr_residual < TOL
    assert all(
        abs(row["best_frequency"] - 2.0) < TOL
        for rows in chain_bohr_tests.values()
        for row in rows
    )

    prior_chain = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v7_linking_chain_degree_two_curvature_quotient_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    prior_kms = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v8_kms_nontracial_relative_rate_selector_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert prior_chain["chain_number_relative_derivation"]["endpoint_degree_gap"] == 2
    assert prior_chain["chain_number_relative_derivation"][
        "unique_up_to_additive_constant_and_orientation"
    ]
    assert not prior_kms["verdict"]["nontracial_KMS_state_exists_for_current_generator"]

    result = {
        "date": "2026-08-29",
        "gate": "version8_modular_bohr_parent_origin_gate",
        "candidate_ledger": {
            "chain_number": {
                "operator_on_full_chain": "N=diag(0*I11,1*I21,2*I10)",
                "endpoint_restriction": "N_end=0*I11 direct_sum 2*I10",
                "endpoint_gap": 2,
                "gauge_invariant": True,
                "correct_endpoint_type": True,
                "common_Bohr_frequency_for_all_transfer_arrows": True,
                "maximum_Bohr_residual": maximum_chain_bohr_residual,
                "continuous_parameter_added": False,
                "ambiguity": "N versus 2I-N",
            },
            "polar_Gram_pair": {
                "operators": "A0* A0 on C11 and A0 A0* on C10",
                "reference_linking_frequency": gram_tests["linking"][0],
                "cross_arrow_tests": {
                    "QLYR": gram_tests["QLYR"],
                    "XLdR": gram_tests["XLdR"],
                },
                "common_Bohr_parent": False,
            },
            "Hodge_metric": {
                "correct_endpoint_type": True,
                "gap": "log eta",
                "eta_derived": False,
            },
            "version4_family_Gibbs_state": {
                "carrier": "M3 family space",
                "canonical_endpoint_lift": False,
            },
            "full_QMS_stationary_state": {
                "state": "I21/21",
                "modular_gap": 0,
            },
        },
        "directed_chain_number_QMS": {
            "forward_orientation": forward,
            "reverse_orientation": reverse,
            "zero_gap_recovers_symmetric_generator_residual": trace_recovery_residual,
            "Lindblad_complete_positivity": True,
            "endpoint_algebra_preserved": True,
            "both_orientations_are_primitive_KMS_processes": True,
        },
        "orientation_audit": {
            "coisometry_direction": "C11 to C10",
            "rank_defect": 1,
            "chain_action_norm_is_orientation_blind": True,
            "KMS_state_is_orientation_sensitive": True,
            "forward_density_ratio": forward["target_to_source_density_ratio"],
            "reverse_density_ratio": reverse["target_to_source_density_ratio"],
            "orientation_selected_by_existing_parent_action": False,
            "orientation_is_continuous_freedom": False,
            "remaining_ambiguity": "twofold discrete orientation",
        },
        "interpretation_boundary": {
            "parameter_free_dimensionless_Bohr_gap_candidate_found": True,
            "unique_oriented_modular_state_derived": False,
            "physical_energy_unit_derived": False,
            "physical_inverse_temperature_derived": False,
            "absolute_time_scale_derived": False,
            "status": "chain_number_Bohr_parent_conditional_pass_twofold_orientation_open",
        },
        "verdict": {
            "old_current_generator_must_be_replaced_by_directed_pairs": True,
            "chain_number_supplies_correct_common_Bohr_grading": True,
            "one_unique_physical_KMS_generator_derived": False,
            "next_gate": "version8_chain_orientation_index_defect_selector_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()