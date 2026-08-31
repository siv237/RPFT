#!/usr/bin/env python3
"""Assemble linking, gauge and cross Dirichlet generators into one QMS."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh, expm


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_full_primitive_markov_generator_assembly_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import physical_blocks  # noqa: E402


def block_generator(incidence: np.ndarray) -> np.ndarray:
    target_dimension, source_dimension = incidence.shape
    source_gram = incidence.conj().T @ incidence
    target_gram = incidence @ incidence.conj().T
    return np.block(
        [
            [
                -0.5 * np.kron(np.eye(source_dimension), source_gram)
                - 0.5 * np.kron(source_gram.T, np.eye(source_dimension)),
                np.kron(incidence.T, incidence.conj().T),
            ],
            [
                np.kron(incidence.conj(), incidence),
                -0.5 * np.kron(np.eye(target_dimension), target_gram)
                - 0.5 * np.kron(target_gram.T, np.eye(target_dimension)),
            ],
        ]
    )


def block_diagonal(blocks: list[np.ndarray]) -> np.ndarray:
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), complex)
    offset = 0
    for block in blocks:
        dimension = block.shape[0]
        result[offset : offset + dimension, offset : offset + dimension] = block
        offset += dimension
    return result


def dissipator(operator: np.ndarray) -> np.ndarray:
    dimension = operator.shape[0]
    square = operator @ operator
    return (
        np.kron(operator.T, operator)
        - 0.5 * np.kron(np.eye(dimension), square)
        - 0.5 * np.kron(square.T, np.eye(dimension))
    )


def corner_dissipator(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    return np.block(
        [
            [
                dissipator(source),
                np.zeros((source.shape[0] ** 2, target.shape[0] ** 2)),
            ],
            [
                np.zeros((target.shape[0] ** 2, source.shape[0] ** 2)),
                dissipator(target),
            ],
        ]
    )


def gell_mann_matrices() -> list[np.ndarray]:
    def matrix(entries) -> np.ndarray:
        result = np.zeros((3, 3), complex)
        for row, column, value in entries:
            result[row, column] = value
        return result

    return [
        matrix(((0, 1, 1), (1, 0, 1))),
        matrix(((0, 1, -1j), (1, 0, 1j))),
        matrix(((0, 0, 1), (1, 1, -1))),
        matrix(((0, 2, 1), (2, 0, 1))),
        matrix(((0, 2, -1j), (2, 0, 1j))),
        matrix(((1, 2, 1), (2, 1, 1))),
        matrix(((1, 2, -1j), (2, 1, 1j))),
        np.diag([1.0, 1.0, -2.0]) / np.sqrt(3.0),
    ]


def pair_vector(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    return np.concatenate(
        [source.reshape(-1, order="F"), target.reshape(-1, order="F")]
    )


def vector_pair(vector: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return (
        vector[:121].reshape((11, 11), order="F"),
        vector[121:].reshape((10, 10), order="F"),
    )


def kernel_data(generator: np.ndarray) -> tuple[int, np.ndarray, float]:
    values = eigvalsh(generator)
    scale = max(1.0, float(np.max(np.abs(values))))
    threshold = max(TOL, 1.0e-11 * scale)
    dimension = int(np.sum(np.abs(values) <= threshold))
    gap = float(-values[-dimension - 1]) if dimension < len(values) else 0.0
    return dimension, values, gap


def main() -> None:
    incidence, variations, labels, _ = physical_blocks()
    heavy = variations[7:]
    source_dimension, target_dimension = 11, 10
    zero_source = np.zeros((source_dimension, source_dimension), complex)
    zero_target = np.zeros((target_dimension, target_dimension), complex)

    pauli = [
        np.array([[0, 1], [1, 0]], complex),
        np.array([[0, -1j], [1j, 0]], complex),
        np.array([[1, 0], [0, -1]], complex),
    ]
    source_su3, target_su3 = [], []
    for matrix in gell_mann_matrices():
        source_su3.append(
            block_diagonal(
                [
                    np.kron(matrix / 2.0, np.eye(2)),
                    np.zeros((2, 2)),
                    np.zeros((1, 1)),
                    np.zeros((2, 2)),
                ]
            )
        )
        target_su3.append(
            block_diagonal(
                [
                    matrix / 2.0,
                    matrix / 2.0,
                    np.zeros((1, 1)),
                    np.zeros((1, 1)),
                    np.zeros((2, 2)),
                ]
            )
        )

    source_su2, target_su2 = [], []
    for matrix in pauli:
        source_su2.append(
            block_diagonal(
                [
                    np.kron(np.eye(3), matrix / 2.0),
                    matrix / 2.0,
                    np.zeros((1, 1)),
                    matrix / 2.0,
                ]
            )
        )
        target_su2.append(
            block_diagonal(
                [
                    np.zeros((3, 3)),
                    np.zeros((3, 3)),
                    np.zeros((1, 1)),
                    np.zeros((1, 1)),
                    matrix / 2.0,
                ]
            )
        )

    source_u1 = block_diagonal(
        [
            np.eye(6) / 6.0,
            -np.eye(2) / 2.0,
            -np.eye(1),
            -np.eye(2) / 2.0,
        ]
    )
    target_u1 = block_diagonal(
        [
            2.0 * np.eye(3) / 3.0,
            -np.eye(3) / 3.0,
            -np.eye(1),
            -np.eye(1),
            -np.eye(2) / 2.0,
        ]
    )

    linking = block_generator(incidence)
    su3 = sum(
        (
            corner_dissipator(source, target)
            for source, target in zip(source_su3, target_su3)
        ),
        np.zeros_like(linking),
    )
    su2 = sum(
        (
            corner_dissipator(source, target)
            for source, target in zip(source_su2, target_su2)
        ),
        np.zeros_like(linking),
    )
    u1 = corner_dissipator(source_u1, target_u1)

    qlyr = np.zeros_like(linking)
    xldr = np.zeros_like(linking)
    cross_jumps = []
    for label, variation in zip(labels, heavy):
        if not label.startswith(("QLYR", "XLdR")):
            continue
        normalized = variation / np.linalg.norm(variation, ord="fro")
        contribution = block_generator(normalized)
        if label.startswith("QLYR"):
            qlyr += contribution
        else:
            xldr += contribution
        cross_jumps.append(
            np.block(
                [
                    [zero_source, normalized.conj().T],
                    [normalized, zero_target],
                ]
            )
        )
    assert len(cross_jumps) == 12

    terms = {
        "linking": linking,
        "SU3": su3,
        "SU2": su2,
        "U1": u1,
        "QLYR": qlyr,
        "XLdR": xldr,
    }
    full_generator = sum(terms.values(), np.zeros_like(linking))
    fixed_dimension, full_values, full_gap = kernel_data(full_generator)
    positive_count = int(np.sum(full_values > TOL))
    identity_vector = pair_vector(np.eye(11), np.eye(10))
    unital_residual = float(np.linalg.norm(full_generator @ identity_vector))
    trace_residual = float(np.linalg.norm(identity_vector.conj() @ full_generator))
    self_adjoint_residual = float(
        np.linalg.norm(full_generator - full_generator.conj().T)
    )
    assert fixed_dimension == 1
    assert positive_count == 0
    assert full_gap > 0.0
    assert unital_residual < TOL
    assert trace_residual < TOL
    assert self_adjoint_residual < TOL

    omission_tests = {}
    for omitted in terms:
        candidate = sum(
            (matrix for name, matrix in terms.items() if name != omitted),
            np.zeros_like(linking),
        )
        dimension, values, gap = kernel_data(candidate)
        omission_tests[omitted] = {
            "fixed_dimension": dimension,
            "positive_eigenvalue_count": int(np.sum(values > TOL)),
            "decay_gap": gap,
        }
    assert omission_tests["QLYR"]["fixed_dimension"] == 1
    assert omission_tests["XLdR"]["fixed_dimension"] == 1
    assert kernel_data(linking + su3 + su2 + u1)[0] == 2

    rng = np.random.default_rng(20260828)
    weight_scan = []
    for _ in range(48):
        weights = 10.0 ** rng.uniform(-3.0, 3.0, size=len(terms))
        candidate = sum(
            (weight * matrix for weight, matrix in zip(weights, terms.values())),
            np.zeros_like(linking),
        )
        dimension, values, gap = kernel_data(candidate)
        assert dimension == 1
        assert np.sum(values > 1.0e-7 * max(1.0, np.max(np.abs(values)))) == 0
        weight_scan.append(
            {
                "weights_linking_SU3_SU2_U1_QLYR_XLdR": [
                    float(value) for value in weights
                ],
                "fixed_dimension": dimension,
                "decay_gap": gap,
            }
        )

    # Every term is a symmetric Dirichlet generator and therefore satisfies
    # detailed balance for the normalized trace separately.  This proves at
    # once that detailed balance cannot select their relative coefficients.
    termwise_symmetry = {
        name: float(np.linalg.norm(matrix - matrix.conj().T))
        for name, matrix in terms.items()
    }
    assert max(termwise_symmetry.values()) < TOL

    # Algebraic complete-positivity certificate: the restriction is induced
    # by 25 self-adjoint Lindblad jump operators on C^21.
    linking_jump = np.block(
        [[zero_source, incidence.conj().T], [incidence, zero_target]]
    )
    gauge_jumps = [
        block_diagonal([source, target])
        for source, target in (
            list(zip(source_su3, target_su3))
            + list(zip(source_su2, target_su2))
            + [(source_u1, target_u1)]
        )
    ]
    all_jumps = [linking_jump] + gauge_jumps + cross_jumps
    assert len(all_jumps) == 25
    assert max(np.linalg.norm(jump - jump.conj().T) for jump in all_jumps) < TOL

    # Compare the full-M21 Lindblad action with the assembled endpoint matrix.
    source_seed = rng.normal(size=(11, 11)) + 1j * rng.normal(size=(11, 11))
    target_seed = rng.normal(size=(10, 10)) + 1j * rng.normal(size=(10, 10))
    source_observable = source_seed + source_seed.conj().T
    target_observable = target_seed + target_seed.conj().T
    observable = block_diagonal([source_observable, target_observable])
    full_action = sum(
        jump @ observable @ jump
        - 0.5 * (jump @ jump @ observable + observable @ jump @ jump)
        for jump in all_jumps
    )
    restricted_action = full_generator @ pair_vector(
        source_observable, target_observable
    )
    restricted_source, restricted_target = vector_pair(restricted_action)
    restriction_residual = float(
        np.linalg.norm(
            full_action - block_diagonal([restricted_source, restricted_target])
        )
    )
    endpoint_offdiagonal_residual = float(
        np.linalg.norm(full_action[:11, 11:])
        + np.linalg.norm(full_action[11:, :11])
    )
    assert restriction_residual < TOL
    assert endpoint_offdiagonal_residual < TOL

    semigroup_tests = []
    for time in (0.1, 1.0):
        semigroup = expm(time * full_generator)
        semigroup_unital_residual = float(
            np.linalg.norm(semigroup @ identity_vector - identity_vector)
        )
        minimum_output_eigenvalue = np.inf
        for _ in range(12):
            source_raw = rng.normal(size=(11, 6)) + 1j * rng.normal(size=(11, 6))
            target_raw = rng.normal(size=(10, 6)) + 1j * rng.normal(size=(10, 6))
            source_positive = source_raw @ source_raw.conj().T
            target_positive = target_raw @ target_raw.conj().T
            output = semigroup @ pair_vector(source_positive, target_positive)
            output_source, output_target = vector_pair(output)
            minimum_output_eigenvalue = min(
                minimum_output_eigenvalue,
                float(eigvalsh(output_source)[0]),
                float(eigvalsh(output_target)[0]),
            )
        assert semigroup_unital_residual < 1.0e-10
        assert minimum_output_eigenvalue > -1.0e-9
        semigroup_tests.append(
            {
                "time": time,
                "unital_residual": semigroup_unital_residual,
                "random_positive_output_minimum_eigenvalue": minimum_output_eigenvalue,
            }
        )
    composition_residual = float(
        np.linalg.norm(
            expm(0.4 * full_generator) @ expm(0.7 * full_generator)
            - expm(1.1 * full_generator)
        )
    )
    assert composition_residual < 1.0e-10

    prior = {
        name: json.loads((ROOT / path).read_text(encoding="utf-8"))
        for name, path in {
            "linking": "s2t/results/s2t_v8_linking_dirichlet_quantum_markov_semigroup_gate_results.json",
            "gauge": "s2t/results/s2t_v8_markov_fixed_algebra_selector_gate_results.json",
            "cross": "s2t/results/s2t_v8_gauge_twirl_cross_sector_kraus_bridge_gate_results.json",
        }.items()
    }
    assert prior["linking"]["fixed_algebra"]["dimension"] == 41
    assert prior["gauge"]["final_fixed_algebra"]["dimension"] == 2
    assert not prior["cross"]["verdict"]["C2_superselection_survives"]

    result = {
        "date": "2026-08-28",
        "gate": "version8_full_primitive_markov_generator_assembly_gate",
        "assembled_generator": {
            "formula": "L_full=L_link+L_SU3+L_SU2+L_U1+L_QLYR+L_XLdR",
            "observable_algebra": "M11(C) direct_sum M10(C)",
            "matrix_dimension": 221,
            "self_adjoint_lindblad_jump_count": len(all_jumps),
            "self_adjoint_residual": self_adjoint_residual,
            "unital_residual": unital_residual,
            "trace_preserving_residual": trace_residual,
            "endpoint_restriction_residual": restriction_residual,
            "endpoint_offdiagonal_residual": endpoint_offdiagonal_residual,
            "semigroup_composition_residual": composition_residual,
            "semigroup_tests": semigroup_tests,
        },
        "fixed_algebra": {
            "dimension": fixed_dimension,
            "algebra": "C I21",
            "unit_weight_decay_gap": full_gap,
            "largest_decay": float(-full_values[0]),
            "unique_faithful_stationary_state": "I21/21",
            "primitive": True,
        },
        "dependency_tests": {
            "without_cross_fixed_dimension": kernel_data(
                linking + su3 + su2 + u1
            )[0],
            "omit_one_named_term": omission_tests,
            "either_complete_cross_multiplet_alone_closes_previous_C2": True,
        },
        "positive_weight_robustness": {
            "samples": len(weight_scan),
            "independent_weight_range": "1e-3 through 1e3",
            "fixed_dimension_always_one": True,
            "decay_gap_minimum": min(row["decay_gap"] for row in weight_scan),
            "decay_gap_maximum": max(row["decay_gap"] for row in weight_scan),
            "sample_rows": weight_scan,
        },
        "detailed_balance": {
            "reference_state": "normalized trace I21/21",
            "termwise_Hilbert_Schmidt_self_adjoint_residuals": termwise_symmetry,
            "full_generator_is_trace_detailed_balanced": True,
            "all_positive_relative_weights_remain_trace_detailed_balanced": True,
            "trace_detailed_balance_selects_relative_weights": False,
        },
        "verdict": {
            "one_unweighted_primitive_qms_exists": True,
            "full_fixed_algebra_is_scalar": True,
            "complete_positivity_has_lindblad_jump_certificate": True,
            "qualitative_primitivity_independent_of_positive_weights": True,
            "unique_relative_rate_metric_derived": False,
            "absolute_physical_rate_derived": False,
            "status": "primitive_markov_universality_class_closed_rate_metric_open",
            "next_gate": "version8_kms_nontracial_relative_rate_selector_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()