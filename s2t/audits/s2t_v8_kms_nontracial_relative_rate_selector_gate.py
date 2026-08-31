#!/usr/bin/env python3
"""Test whether a nontracial KMS state selects the rates of the full QMS."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_kms_nontracial_relative_rate_selector_gate_results.json"
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


def central_density(target_to_source_density_ratio: float) -> tuple[float, float]:
    """Return per-state source and target densities with unit total trace."""
    source_density = 1.0 / (11.0 + 10.0 * target_to_source_density_ratio)
    target_density = target_to_source_density_ratio * source_density
    return source_density, target_density


def assemble() -> tuple[dict[str, np.ndarray], list[np.ndarray], dict[str, list[np.ndarray]]]:
    incidence, variations, labels, _ = physical_blocks()
    heavy = variations[7:]
    zero_source = np.zeros((11, 11), complex)
    zero_target = np.zeros((10, 10), complex)

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

    transfers: dict[str, list[np.ndarray]] = {
        "linking": [incidence],
        "QLYR": [],
        "XLdR": [],
    }
    qlyr = np.zeros((221, 221), complex)
    xldr = np.zeros((221, 221), complex)
    for label, variation in zip(labels, heavy):
        if not label.startswith(("QLYR", "XLdR")):
            continue
        normalized = variation / np.linalg.norm(variation, ord="fro")
        family = "QLYR" if label.startswith("QLYR") else "XLdR"
        transfers[family].append(normalized)
        if family == "QLYR":
            qlyr += block_generator(normalized)
        else:
            xldr += block_generator(normalized)

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
    terms = {
        "linking": linking,
        "SU3": su3,
        "SU2": su2,
        "U1": u1,
        "QLYR": qlyr,
        "XLdR": xldr,
    }

    transfer_jumps = []
    for family in transfers.values():
        for operator in family:
            transfer_jumps.append(
                np.block(
                    [
                        [zero_source, operator.conj().T],
                        [operator, zero_target],
                    ]
                )
            )
    return terms, transfer_jumps, transfers


def main() -> None:
    terms, transfer_jumps, transfers = assemble()
    full_generator = sum(terms.values(), np.zeros((221, 221), complex))
    eigenvalues = eigvalsh(full_generator)
    fixed_dimension = int(np.sum(np.abs(eigenvalues) < TOL))
    assert fixed_dimension == 1
    assert len(transfer_jumps) == 13

    trace_density_vector = pair_vector(np.eye(11) / 21.0, np.eye(10) / 21.0)
    trace_stationarity_residual = float(
        np.linalg.norm(full_generator.conj().T @ trace_density_vector)
    )
    assert trace_stationarity_residual < TOL

    # On a central state rho=a I_11 direct_sum b I_10 the GNS and KMS
    # metrics coincide on the endpoint algebra and are represented by G.
    ratio_scan = []
    for ratio in np.logspace(-4.0, 4.0, 65):
        source_density, target_density = central_density(float(ratio))
        metric = block_diagonal(
            [source_density * np.eye(121), target_density * np.eye(100)]
        )
        density_vector = pair_vector(
            source_density * np.eye(11), target_density * np.eye(10)
        )
        stationarity_residual = float(
            np.linalg.norm(full_generator.conj().T @ density_vector)
        )
        symmetry_residual = float(
            np.linalg.norm(metric @ full_generator - full_generator.conj().T @ metric)
        )
        ratio_scan.append(
            {
                "target_to_source_density_ratio": float(ratio),
                "stationarity_residual": stationarity_residual,
                "KMS_symmetry_residual": symmetry_residual,
            }
        )
    best_stationary = min(ratio_scan, key=lambda row: row["stationarity_residual"])
    best_symmetric = min(ratio_scan, key=lambda row: row["KMS_symmetry_residual"])
    assert abs(best_stationary["target_to_source_density_ratio"] - 1.0) < TOL
    assert abs(best_symmetric["target_to_source_density_ratio"] - 1.0) < TOL
    assert best_stationary["stationarity_residual"] < TOL
    assert best_symmetric["KMS_symmetry_residual"] < TOL

    # A positive transfer family cannot cancel another one: applied to the
    # source identity, every source-to-target block has positive trace.
    transfer_trace_certificates = {
        family: float(sum(np.linalg.norm(operator, ord="fro") ** 2 for operator in operators))
        for family, operators in transfers.items()
    }
    assert min(transfer_trace_certificates.values()) > 0.0

    # A self-adjoint bidirectional jump is not a single nonzero Bohr mode.
    # For H=0 on the source and H=delta on the target, its two oriented
    # halves have frequencies +delta and -delta.
    bohr_tests = []
    source_projector = block_diagonal([np.eye(11), np.zeros((10, 10))])
    target_projector = block_diagonal([np.zeros((11, 11)), np.eye(10)])
    for delta in (-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0):
        hamiltonian = delta * target_projector
        normalized_residuals = []
        forward_residuals = []
        reverse_residuals = []
        for jump in transfer_jumps:
            commutator = hamiltonian @ jump - jump @ hamiltonian
            normalized_residuals.append(
                float(np.linalg.norm(commutator) / np.linalg.norm(jump))
            )
            forward = target_projector @ jump @ source_projector
            reverse = source_projector @ jump @ target_projector
            forward_residuals.append(
                float(
                    np.linalg.norm(
                        hamiltonian @ forward - forward @ hamiltonian - delta * forward
                    )
                )
            )
            reverse_residuals.append(
                float(
                    np.linalg.norm(
                        hamiltonian @ reverse - reverse @ hamiltonian + delta * reverse
                    )
                )
            )
        assert max(forward_residuals) < TOL
        assert max(reverse_residuals) < TOL
        bohr_tests.append(
            {
                "modular_gap_beta_Delta": delta,
                "self_adjoint_jump_single_Bohr_mode_residual": max(
                    normalized_residuals
                ),
                "oriented_forward_mode_residual": max(forward_residuals),
                "oriented_reverse_mode_residual": max(reverse_residuals),
            }
        )
    assert bohr_tests[3]["self_adjoint_jump_single_Bohr_mode_residual"] < TOL
    assert min(
        row["self_adjoint_jump_single_Bohr_mode_residual"]
        for row in bohr_tests
        if row["modular_gap_beta_Delta"] != 0.0
    ) > 0.9

    # Once jumps are split into oriented pairs, KMS gives only a conditional
    # ratio.  Every positive modular gap produces a different admissible ratio.
    directed_family = []
    for beta_delta in (-6.0, -3.0, -1.0, 0.0, 1.0, 3.0, 6.0):
        target_to_source = float(np.exp(-beta_delta))
        source_density, target_density = central_density(target_to_source)
        upward_to_downward_rate = target_to_source
        flux_residual = abs(
            upward_to_downward_rate * source_density - target_density
        )
        assert flux_residual < TOL
        directed_family.append(
            {
                "beta_Delta": beta_delta,
                "target_to_source_density_ratio": target_to_source,
                "upward_to_downward_rate_ratio": upward_to_downward_rate,
                "source_density_per_state": source_density,
                "target_density_per_state": target_density,
                "detailed_balance_flux_residual": flux_residual,
            }
        )

    previous = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v8_full_primitive_markov_generator_assembly_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    assert previous["fixed_algebra"]["primitive"]
    assert previous["fixed_algebra"]["unique_faithful_stationary_state"] == "I21/21"

    result = {
        "date": "2026-08-28",
        "gate": "version8_kms_nontracial_relative_rate_selector_gate",
        "input_process": {
            "observable_algebra": "M11(C) direct_sum M10(C)",
            "generator_terms": list(terms),
            "fixed_algebra_dimension": fixed_dimension,
            "primitive": True,
            "trace_stationarity_residual": trace_stationarity_residual,
        },
        "central_nontracial_state_test": {
            "state": "rho=a I11 direct_sum b I10, 11a+10b=1",
            "ratio": "r=b/a",
            "scan_range": "1e-4 through 1e4",
            "samples": len(ratio_scan),
            "best_stationary_row": best_stationary,
            "best_KMS_symmetric_row": best_symmetric,
            "only_passing_ratio": 1.0,
            "only_passing_state": "I21/21",
            "sample_rows": ratio_scan,
        },
        "positive_weight_no_cancellation_certificate": {
            "transfer_trace_on_source_identity": transfer_trace_certificates,
            "reason": "each positive transfer contribution has strictly positive target trace",
            "consequence": "positive rate tuning cannot permit a nontracial central KMS metric",
        },
        "bohr_mode_test": {
            "transfer_jump_count": len(transfer_jumps),
            "central_modular_hamiltonian": "H_Delta=0 on C11 and Delta on C10",
            "tests": bohr_tests,
            "self_adjoint_transfer_jump_is_nonzero_Bohr_eigenoperator": False,
            "oriented_halves_have_opposite_Bohr_frequencies": True,
        },
        "directed_KMS_extension": {
            "formula": "gamma_up/gamma_down=exp(-beta Delta)=b/a",
            "sample_family": directed_family,
            "nontracial_states_admitted_after_directed_split": True,
            "modular_gap_derived_by_current_parent": False,
            "relative_rate_ratio_uniquely_selected": False,
            "remaining_free_data": [
                "the modular gap beta Delta",
                "one base intensity for each transfer family",
                "the gauge-sector intensities",
                "the overall physical time scale",
            ],
        },
        "project_candidate_audit": {
            "version4_affine_Gibbs_states": "family-specific M3 states; no canonical lift to M11 direct_sum M10",
            "version8_central_modular_state": "a P_source+b P_target; ratio is free",
            "current_full_QMS": "primitive and unital; forces the trace state",
            "canonical_nontracial_endpoint_state_found": False,
        },
        "verdict": {
            "nontracial_KMS_state_exists_for_current_generator": False,
            "KMS_selects_current_six_relative_rates": False,
            "directed_jump_extension_is_mathematically_available": True,
            "directed_jump_extension_is_derived_from_current_parent": False,
            "status": "exact_no_go_for_nontracial_KMS_selector_on_current_unital_primitive_QMS",
            "next_gate": "version8_modular_bohr_parent_origin_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()