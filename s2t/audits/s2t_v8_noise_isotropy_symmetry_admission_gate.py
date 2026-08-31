#!/usr/bin/env python3
"""Test whether physical symmetries force isotropy of the 19D noise quotient."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import block_diag, eigvalsh, expm, svdvals


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_noise_isotropy_symmetry_admission_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v8_canonical_noise_frame_common_trace_gate import (  # noqa: E402
    gauge_components,
    gauge_generator,
    transfer_generator,
    whiten_gauge,
    whiten_maps,
)
from s2t_v8_kms_nontracial_relative_rate_selector_gate import (  # noqa: E402
    assemble,
    block_diagonal,
    central_density,
    pair_vector,
)
from s2t_v7_derived_relative_involution_curvature_norm_gate import (  # noqa: E402
    physical_blocks,
)


def transfer_gram(
    maps: list[np.ndarray], source_density: float, target_density: float
) -> np.ndarray:
    return np.array(
        [
            [
                (source_density + target_density)
                * np.trace(left.conj().T @ right)
                for right in maps
            ]
            for left in maps
        ]
    )


def gauge_gram(
    sources: list[np.ndarray],
    targets: list[np.ndarray],
    source_density: float,
    target_density: float,
) -> np.ndarray:
    return np.array(
        [
            [
                source_density * np.trace(left_s.conj().T @ right_s)
                + target_density * np.trace(left_t.conj().T @ right_t)
                for right_s, right_t in zip(sources, targets)
            ]
            for left_s, left_t in zip(sources, targets)
        ]
    )


def representation_matrices(
    unitary_source: np.ndarray,
    unitary_target: np.ndarray,
    transfers: list[np.ndarray],
    gauge_sources: list[np.ndarray],
    gauge_targets: list[np.ndarray],
    source_density: float,
    target_density: float,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    rt = np.zeros((len(transfers), len(transfers)), complex)
    transfer_residual = 0.0
    for column, operator in enumerate(transfers):
        transformed = unitary_target @ operator @ unitary_source.conj().T
        coefficients = np.array(
            [
                (source_density + target_density)
                * np.trace(frame.conj().T @ transformed)
                for frame in transfers
            ]
        )
        rt[:, column] = coefficients
        reconstructed = sum(
            (coefficients[i] * transfers[i] for i in range(len(transfers))),
            np.zeros_like(transfers[0]),
        )
        transfer_residual = max(
            transfer_residual, float(np.linalg.norm(transformed - reconstructed))
        )

    rg = np.zeros((len(gauge_sources), len(gauge_sources)), complex)
    gauge_residual = 0.0
    for column, (source, target) in enumerate(zip(gauge_sources, gauge_targets)):
        transformed_source = unitary_source @ source @ unitary_source.conj().T
        transformed_target = unitary_target @ target @ unitary_target.conj().T
        coefficients = np.array(
            [
                source_density * np.trace(frame_s.conj().T @ transformed_source)
                + target_density * np.trace(frame_t.conj().T @ transformed_target)
                for frame_s, frame_t in zip(gauge_sources, gauge_targets)
            ]
        )
        rg[:, column] = coefficients
        reconstructed_source = sum(
            (coefficients[i] * gauge_sources[i] for i in range(len(gauge_sources))),
            np.zeros_like(gauge_sources[0]),
        )
        reconstructed_target = sum(
            (coefficients[i] * gauge_targets[i] for i in range(len(gauge_targets))),
            np.zeros_like(gauge_targets[0]),
        )
        gauge_residual = max(
            gauge_residual,
            float(np.linalg.norm(transformed_source - reconstructed_source)),
            float(np.linalg.norm(transformed_target - reconstructed_target)),
        )
    return rt, rg, transfer_residual, gauge_residual


def commutant_dimension(matrices: list[np.ndarray]) -> tuple[int, list[float]]:
    dimension = matrices[0].shape[0]
    identity = np.eye(dimension)
    constraints = np.vstack(
        [
            np.kron(matrix.T, identity) - np.kron(identity, matrix)
            for matrix in matrices
        ]
    )
    singular_values = svdvals(constraints)
    threshold = max(TOL, 1.0e-10 * singular_values[0])
    nullity = dimension**2 - int(np.sum(singular_values > threshold))
    return nullity, [float(value) for value in singular_values[-12:]]


def kernel_dimension(matrix: np.ndarray) -> int:
    values = svdvals(matrix)
    return int(np.sum(values < max(TOL, 1.0e-11 * values[0])))


def orthonormal_map_span(maps: list[np.ndarray]) -> list[np.ndarray]:
    flattened = np.stack([matrix.reshape(-1) for matrix in maps], axis=1)
    vectors, values, _ = np.linalg.svd(flattened, full_matrices=False)
    rank = int(np.sum(values > 1.0e-10 * values[0]))
    return [vectors[:, index].reshape(maps[0].shape) for index in range(rank)]


def lie_orbit_closure(
    seed: list[np.ndarray],
    gauge_sources: list[np.ndarray],
    gauge_targets: list[np.ndarray],
) -> tuple[list[np.ndarray], list[int]]:
    basis = orthonormal_map_span(seed)
    dimensions = [len(basis)]
    for _ in range(12):
        generated = basis + [
            target @ operator - operator @ source
            for operator in basis
            for source, target in zip(gauge_sources, gauge_targets)
        ]
        basis = orthonormal_map_span(generated)
        dimensions.append(len(basis))
        if dimensions[-1] == dimensions[-2]:
            break
    return basis, dimensions


def incidence_stabilizer_generators(
    incidence: np.ndarray,
    gauge_sources: list[np.ndarray],
    gauge_targets: list[np.ndarray],
) -> tuple[list[tuple[np.ndarray, np.ndarray]], int]:
    tangent = np.stack(
        [
            (target @ incidence - incidence @ source).reshape(-1)
            for source, target in zip(gauge_sources, gauge_targets)
        ],
        axis=1,
    )
    _, values, right = np.linalg.svd(tangent, full_matrices=True)
    rank = int(np.sum(values > 1.0e-10 * values[0]))
    null_vectors = right[rank:].conj().T
    generators = []
    for column in range(null_vectors.shape[1]):
        source = sum(
            (
                null_vectors[index, column] * gauge_sources[index]
                for index in range(len(gauge_sources))
            ),
            np.zeros_like(gauge_sources[0]),
        )
        target = sum(
            (
                null_vectors[index, column] * gauge_targets[index]
                for index in range(len(gauge_targets))
            ),
            np.zeros_like(gauge_targets[0]),
        )
        generators.append((source, target))
    return generators, rank


def main() -> None:
    _, _, transfer_families = assemble()
    ratio = float(np.exp(-2.0))
    source_density, target_density = central_density(ratio)
    raw_transfers = sum(
        (transfer_families[name] for name in ("linking", "QLYR", "XLdR")),
        [],
    )
    raw_gauge_labels, raw_gauge_sources, raw_gauge_targets = gauge_components()
    selected_white_transfers = whiten_maps(
        raw_transfers,
        transfer_gram(raw_transfers, source_density, target_density),
    )
    white_gauge_sources, white_gauge_targets = whiten_gauge(
        raw_gauge_sources,
        raw_gauge_targets,
        gauge_gram(
            raw_gauge_sources,
            raw_gauge_targets,
            source_density,
            target_density,
        ),
    )
    assert len(selected_white_transfers) == 7
    assert len(white_gauge_sources) == 12

    selected_orbit_basis, selected_orbit_dimensions = lie_orbit_closure(
        selected_white_transfers, raw_gauge_sources, raw_gauge_targets
    )
    assert selected_orbit_dimensions == [7, 10, 11, 11]

    incidence, variations, labels, _ = physical_blocks()
    heavy_variations = variations[7:]
    heavy_span = orthonormal_map_span(heavy_variations)
    heavy_orbit, heavy_orbit_dimensions = lie_orbit_closure(
        heavy_span, raw_gauge_sources, raw_gauge_targets
    )
    incidence_orbit, incidence_orbit_dimensions = lie_orbit_closure(
        [incidence], raw_gauge_sources, raw_gauge_targets
    )
    assert heavy_orbit_dimensions == [10, 10]
    assert incidence_orbit_dimensions == [1, 4, 5, 5]
    full_gauge_closed_span = orthonormal_map_span(incidence_orbit + heavy_orbit)
    assert len(full_gauge_closed_span) == 15
    full_white_transfers = whiten_maps(
        full_gauge_closed_span,
        transfer_gram(full_gauge_closed_span, source_density, target_density),
    )
    assert len(full_white_transfers) == 15

    stabilizer_generators, incidence_orbit_tangent_rank = incidence_stabilizer_generators(
        incidence, raw_gauge_sources, raw_gauge_targets
    )
    assert incidence_orbit_tangent_rank == 3
    assert len(stabilizer_generators) == 9

    selected_span = orthonormal_map_span(raw_transfers)
    added_label_rows = []
    for label, variation in zip(labels, heavy_variations):
        norm = float(np.linalg.norm(variation))
        coefficients = np.array(
            [np.trace(frame.conj().T @ variation) for frame in selected_span]
        )
        reconstructed = sum(
            (coefficients[i] * selected_span[i] for i in range(len(selected_span))),
            np.zeros_like(variation),
        )
        relative_residual = float(np.linalg.norm(variation - reconstructed) / norm)
        if relative_residual > 1.0e-8:
            added_label_rows.append(
                {"label": label, "relative_residual_from_selected_span": relative_residual}
            )
    added_families = sorted({row["label"].split("_")[0] for row in added_label_rows})
    assert added_families == ["LLXR", "YLeR"]

    rng = np.random.default_rng(20260829)
    selected_closure_rows = []
    full_symmetry_matrices = []
    full_representation_rows = []
    for sample in range(12):
        coefficients = rng.normal(scale=0.7, size=12)
        source_generator = sum(
            (coefficients[i] * raw_gauge_sources[i] for i in range(12)),
            np.zeros_like(raw_gauge_sources[0]),
        )
        target_generator = sum(
            (coefficients[i] * raw_gauge_targets[i] for i in range(12)),
            np.zeros_like(raw_gauge_targets[0]),
        )
        unitary_source = expm(1j * source_generator)
        unitary_target = expm(1j * target_generator)
        selected_rt, _, selected_transfer_residual, _ = representation_matrices(
            unitary_source,
            unitary_target,
            selected_white_transfers,
            white_gauge_sources,
            white_gauge_targets,
            source_density,
            target_density,
        )
        selected_unitarity = float(
            np.linalg.norm(selected_rt.conj().T @ selected_rt - np.eye(7))
        )
        selected_closure_rows.append(
            {
                "sample": sample,
                "transfer_closure_residual": selected_transfer_residual,
                "projected_unitarity_residual": selected_unitarity,
            }
        )

        rt, rg, transfer_residual, gauge_residual = representation_matrices(
            unitary_source,
            unitary_target,
            full_white_transfers,
            white_gauge_sources,
            white_gauge_targets,
            source_density,
            target_density,
        )
        gauge_unitarity = float(np.linalg.norm(rg.conj().T @ rg - np.eye(12)))
        transfer_unitarity = float(np.linalg.norm(rt.conj().T @ rt - np.eye(15)))
        assert transfer_residual < TOL
        assert gauge_residual < TOL
        assert transfer_unitarity < TOL
        assert gauge_unitarity < TOL
        full = block_diag(rt, rg)
        full_symmetry_matrices.append(full)
        full_representation_rows.append(
            {
                "sample": sample,
                "transfer_closure_residual": transfer_residual,
                "gauge_closure_residual": gauge_residual,
                "transfer_unitarity_residual": transfer_unitarity,
                "gauge_unitarity_residual": gauge_unitarity,
            }
        )

    stabilizer_symmetry_matrices = []
    stabilizer_representation_rows = []
    for sample in range(10):
        coefficients = rng.normal(scale=0.7, size=len(stabilizer_generators))
        source_generator = sum(
            (
                coefficients[index] * stabilizer_generators[index][0]
                for index in range(len(stabilizer_generators))
            ),
            np.zeros_like(raw_gauge_sources[0]),
        )
        target_generator = sum(
            (
                coefficients[index] * stabilizer_generators[index][1]
                for index in range(len(stabilizer_generators))
            ),
            np.zeros_like(raw_gauge_targets[0]),
        )
        unitary_source = expm(1j * source_generator)
        unitary_target = expm(1j * target_generator)
        rt, rg, transfer_residual, gauge_residual = representation_matrices(
            unitary_source,
            unitary_target,
            selected_white_transfers,
            white_gauge_sources,
            white_gauge_targets,
            source_density,
            target_density,
        )
        transfer_unitarity = float(np.linalg.norm(rt.conj().T @ rt - np.eye(7)))
        gauge_unitarity = float(np.linalg.norm(rg.conj().T @ rg - np.eye(12)))
        assert transfer_residual < TOL
        assert gauge_residual < TOL
        assert transfer_unitarity < TOL
        assert gauge_unitarity < TOL
        stabilizer_symmetry_matrices.append(block_diag(rt, rg))
        stabilizer_representation_rows.append(
            {
                "sample": sample,
                "transfer_closure_residual": transfer_residual,
                "gauge_closure_residual": gauge_residual,
                "transfer_unitarity_residual": transfer_unitarity,
                "gauge_unitarity_residual": gauge_unitarity,
            }
        )

    # Chain/modular degree separates transfer (degree two) and gauge
    # (degree zero) noise.  Include it in the physical symmetry algebra.
    assert max(row["transfer_closure_residual"] for row in selected_closure_rows) > 1.0
    full_degree = np.diag([2.0] * 15 + [0.0] * 12)
    full_commutant_dim, full_tail = commutant_dimension(
        full_symmetry_matrices + [full_degree]
    )
    stabilizer_degree = np.diag([2.0] * 7 + [0.0] * 12)
    stabilizer_commutant_dim, stabilizer_tail = commutant_dimension(
        stabilizer_symmetry_matrices + [stabilizer_degree]
    )
    assert full_commutant_dim > 1
    assert stabilizer_commutant_dim > 1

    transfer_projector = np.diag([1.0] * 15 + [0.0] * 12)
    gauge_projector = np.eye(27) - transfer_projector
    projector_commutator_residual = max(
        float(np.linalg.norm(transfer_projector @ matrix - matrix @ transfer_projector))
        for matrix in full_symmetry_matrices + [full_degree]
    )
    assert projector_commutator_residual < TOL

    transfer_part = transfer_generator(full_white_transfers, ratio)
    gauge_part = gauge_generator(white_gauge_sources, white_gauge_targets)
    kms_metric = block_diagonal(
        [source_density * np.eye(121), target_density * np.eye(100)]
    )
    sqrt_metric = block_diagonal(
        [
            np.sqrt(source_density) * np.eye(121),
            np.sqrt(target_density) * np.eye(100),
        ]
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
    eta_rows = []
    for eta in np.logspace(-3.0, 3.0, 13):
        generator = eta * transfer_part + gauge_part
        kms_residual = float(
            np.linalg.norm(kms_metric @ generator - generator.conj().T @ kms_metric)
        )
        stationarity_residual = float(
            np.linalg.norm(generator.conj().T @ density_vector)
        )
        fixed_dimension = kernel_dimension(generator)
        symmetric = sqrt_metric @ generator @ inverse_sqrt_metric
        spectrum = eigvalsh((symmetric + symmetric.conj().T) / 2.0)
        gap = float(-spectrum[-fixed_dimension - 1])
        assert kms_residual < TOL
        assert stationarity_residual < TOL
        assert fixed_dimension == 1
        eta_rows.append(
            {
                "transfer_to_gauge_isotropy_weight": float(eta),
                "fixed_algebra_dimension": fixed_dimension,
                "KMS_symmetry_residual": kms_residual,
                "stationarity_residual": stationarity_residual,
                "decay_gap": gap,
            }
        )

    # A generic U(27) rotation would enforce scalar commutant, but it mixes
    # the two exact degree sectors and hence is not a physical symmetry.
    random_matrix = rng.normal(size=(27, 27)) + 1j * rng.normal(size=(27, 27))
    q, r = np.linalg.qr(random_matrix)
    phases = np.diag(r)
    enlarged_unitary = q @ np.diag(np.conj(phases) / np.abs(phases))
    enlarged_degree_commutator = float(
        np.linalg.norm(enlarged_unitary @ full_degree - full_degree @ enlarged_unitary)
    )
    assert enlarged_degree_commutator > 1.0

    prior = json.loads(
        (ROOT / "s2t/results/s2t_v8_canonical_noise_frame_common_trace_gate_results.json").read_text()
    )
    assert prior["verdict"]["canonical_relative_generator_representative_obtained"]
    assert not prior["status_boundary"]["trace_isotropy_forced_by_physical_symmetry"]

    result = {
        "date": "2026-08-29",
        "gate": "version8_noise_isotropy_symmetry_admission_gate",
        "physical_noise_representation": {
            "group": "represented SU3 x SU2 x U1 endpoint gauge group plus chain degree",
            "previous_selected_noise_dimension": 19,
            "selected_transfer_dimension": 7,
            "selected_transfer_full_gauge_orbit_dimension": 11,
            "heavy_transfer_dimension": 10,
            "heavy_transfer_full_gauge_orbit_dimension": 10,
            "linking_incidence_full_gauge_orbit_dimension": 5,
            "gauge_closed_noise_quotient_dimension": 27,
            "gauge_closed_transfer_dimension": 15,
            "gauge_dimension": 12,
            "incidence_orbit_tangent_rank": incidence_orbit_tangent_rank,
            "incidence_stabilizer_dimension": len(stabilizer_generators),
            "selected_transfer_closure_failure_samples": selected_closure_rows,
            "selected_transfer_maximum_closure_residual": max(
                row["transfer_closure_residual"] for row in selected_closure_rows
            ),
            "selected_Lie_orbit_dimension_sequence": selected_orbit_dimensions,
            "incidence_Lie_orbit_dimension_sequence": incidence_orbit_dimensions,
            "heavy_Lie_orbit_dimension_sequence": heavy_orbit_dimensions,
            "added_variation_labels": added_label_rows,
            "added_families": added_families,
            "full_gauge_closed_samples": full_representation_rows,
            "stabilizer_19D_samples": stabilizer_representation_rows,
            "full_gauge_actions_close_only_after_27D_completion": True,
            "19D_selected_module_closes_under_incidence_stabilizer": True,
        },
        "commutant_test": {
            "full_gauge_27D_complex_commutant_dimension": full_commutant_dim,
            "full_gauge_smallest_constraint_singular_values": full_tail,
            "stabilizer_19D_complex_commutant_dimension": stabilizer_commutant_dim,
            "stabilizer_smallest_constraint_singular_values": stabilizer_tail,
            "scalar_only_in_either_branch": False,
            "transfer_projector_commutes_with_all_symmetries": True,
            "projector_commutator_residual": projector_commutator_residual,
            "minimum_invariant_metric_family": "G_eta=eta P_transfer + P_gauge, eta>0",
        },
        "invariant_metric_scan": {
            "eta_samples": eta_rows,
            "all_positive_eta_primitive": True,
            "all_positive_eta_KMS_symmetric": True,
            "gap_minimum": min(row["decay_gap"] for row in eta_rows),
            "gap_maximum": max(row["decay_gap"] for row in eta_rows),
            "symmetry_selects_eta_one": False,
        },
        "enlarged_symmetry_control": {
            "full_U27_would_force_scalar_metric": True,
            "generic_U27_preserves_chain_degree": False,
            "generic_U27_degree_commutator_norm": enlarged_degree_commutator,
            "admitting_U27_would_mix_Bohr_zero_and_two_sectors": True,
        },
        "verdict": {
            "previous_19D_trace_Casimir_is_fully_gauge_admissible": False,
            "minimal_gauge_closed_noise_dimension": 27,
            "gauge_closed_trace_Casimir_obtained": True,
            "physical_symmetry_forces_trace_isotropy": False,
            "trace_isotropic_gauge_closed_Casimir_is_canonical_representative": True,
            "at_least_one_relative_transfer_gauge_weight_remains": True,
            "status": "selected_noise_module_gauge_closure_correction_and_trace_isotropy_no_go",
            "next_gate": "version8_gauge_closed_noise_parent_hessian_gate",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()