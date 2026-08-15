#!/usr/bin/env python3
import json
from itertools import product
from pathlib import Path

import numpy as np


TOLERANCE = 1.0e-9
RANDOM_SEEDS = [20260815, 20260816, 20260817, 20260818]


def block_diagonal(blocks):
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), dtype=complex)
    offset = 0
    for block in blocks:
        block_size = block.shape[0]
        result[offset : offset + block_size, offset : offset + block_size] = block
        offset += block_size
    return result


def particle_dirac(locking, pairing):
    zero = np.zeros((3, 3), dtype=complex)
    pairing_block = pairing * np.eye(3)
    return np.block(
        [
            [zero, locking.conj().T, zero],
            [locking, zero, pairing_block.conj().T],
            [zero, pairing_block, zero],
        ]
    )


def algebra_representation(matrix_part, scalar_left, scalar_right):
    identity = np.eye(3)
    return block_diagonal(
        [
            scalar_left * identity,
            matrix_part,
            matrix_part,
            np.conj(scalar_left) * identity,
            np.conj(scalar_left) * identity,
            np.conj(scalar_right) * identity,
        ]
    )


def algebra_basis():
    basis = []
    for row in range(3):
        for column in range(3):
            matrix = np.zeros((3, 3))
            matrix[row, column] = 1.0
            basis.append((matrix, 0.0, 0.0))
    basis.append((np.zeros((3, 3)), 1.0, 0.0))
    basis.append((np.zeros((3, 3)), 0.0, 1.0))
    basis.append((np.zeros((3, 3)), 0.0, 1.0j))
    return basis


def commutator(left, right):
    return left @ right - right @ left


def orthonormal_span(columns, tolerance=TOLERANCE):
    if columns.shape[1] == 0:
        return np.zeros((columns.shape[0], 0), dtype=columns.dtype)
    left_vectors, singular_values, _ = np.linalg.svd(columns, full_matrices=False)
    return left_vectors[:, singular_values > tolerance]


def nullspace(columns, tolerance=TOLERANCE):
    _, singular_values, right_vectors = np.linalg.svd(columns, full_matrices=True)
    rank = int(np.sum(singular_values > tolerance))
    return right_vectors[rank:].conj().T


def realify(columns):
    return np.vstack([columns.real, columns.imag])


def complexify_real_vectors(columns):
    half = columns.shape[0] // 2
    return columns[:half] + 1j * columns[half:]


def quotient_basis(represented_basis, junk_basis):
    residual = represented_basis
    if junk_basis.shape[1]:
        residual = residual - junk_basis @ (junk_basis.conj().T @ residual)
    return orthonormal_span(residual)


def block_projection(columns, block_pairs, matrix_size=18, block_size=3):
    projected = []
    for column in columns.T:
        matrix = column.reshape(matrix_size, matrix_size)
        coordinates = []
        for block_row, block_column in block_pairs:
            row_slice = slice(block_size * block_row, block_size * (block_row + 1))
            column_slice = slice(
                block_size * block_column, block_size * (block_column + 1)
            )
            coordinates.append(matrix[row_slice, column_slice].reshape(-1))
        projected.append(np.concatenate(coordinates))
    if not projected:
        return np.zeros((len(block_pairs) * block_size**2, 0), dtype=complex)
    return np.stack(projected, axis=1)


def span_residual(columns, span_basis):
    if columns.shape[1] == 0:
        return 0.0
    if span_basis.shape[1] == 0:
        return float(np.linalg.norm(columns))
    residual = columns - span_basis @ (span_basis.conj().T @ columns)
    return float(np.linalg.norm(residual))


def target_residual(target, span_basis):
    vector = target.reshape(-1)
    if span_basis.shape[1] == 0:
        return float(np.linalg.norm(vector))
    return float(np.linalg.norm(vector - span_basis @ (span_basis.conj().T @ vector)))


def represented_calculus(dirac, representations):
    commutators = [commutator(dirac, representation) for representation in representations]
    one_generators = []
    differentials = []
    for first, second in product(range(len(representations)), repeat=2):
        one_generators.append(representations[first] @ commutators[second])
        differentials.append(commutators[first] @ commutators[second])

    one_matrix = np.stack([matrix.reshape(-1) for matrix in one_generators], axis=1)
    one_kernel = nullspace(one_matrix)
    junk_matrix = np.stack(
        [
            sum(
                one_kernel[index, kernel_index] * differentials[index]
                for index in range(len(differentials))
            ).reshape(-1)
            for kernel_index in range(one_kernel.shape[1])
        ],
        axis=1,
    )

    two_generators = []
    for first, second, third in product(range(len(representations)), repeat=3):
        two_generators.append(
            representations[first] @ commutators[second] @ commutators[third]
        )
    two_matrix = np.stack([matrix.reshape(-1) for matrix in two_generators], axis=1)

    one_basis = orthonormal_span(one_matrix)
    junk_basis = orthonormal_span(junk_matrix)
    two_basis = orthonormal_span(two_matrix)
    quotient = quotient_basis(two_basis, junk_basis)

    real_one_matrix = realify(one_matrix)
    real_one_kernel = nullspace(real_one_matrix).real
    real_junk_matrix = np.stack(
        [
            sum(
                real_one_kernel[index, kernel_index] * differentials[index]
                for index in range(len(differentials))
            ).reshape(-1)
            for kernel_index in range(real_one_kernel.shape[1])
        ],
        axis=1,
    )
    real_one_basis = orthonormal_span(real_one_matrix)
    real_junk_basis_realified = orthonormal_span(realify(real_junk_matrix))
    real_two_basis_realified = orthonormal_span(realify(two_matrix))
    real_quotient_realified = quotient_basis(
        real_two_basis_realified, real_junk_basis_realified
    )
    real_junk_basis = complexify_real_vectors(real_junk_basis_realified)
    real_two_basis = complexify_real_vectors(real_two_basis_realified)
    real_quotient = complexify_real_vectors(real_quotient_realified)

    return {
        "one_basis": one_basis,
        "junk_basis": junk_basis,
        "two_basis": two_basis,
        "quotient_basis": quotient,
        "real_one_rank": real_one_basis.shape[1],
        "real_one_kernel_dimension": real_one_kernel.shape[1],
        "real_junk_basis": real_junk_basis,
        "real_two_basis": real_two_basis,
        "real_quotient_basis": real_quotient,
        "one_kernel_dimension": one_kernel.shape[1],
        "junk_outside_twoforms": span_residual(junk_basis, two_basis),
    }


def audit_background(locking, pairing, label):
    particle = particle_dirac(locking, pairing)
    dirac = block_diagonal([particle, particle.conj()])
    representations = [
        algebra_representation(*basis_element) for basis_element in algebra_basis()
    ]
    calculus = represented_calculus(dirac, representations)

    middle_pairs = [(1, 1), (4, 4)]
    particle_middle_pairs = [(1, 1)]
    conjugate_middle_pairs = [(4, 4)]
    endpoint_pairs = [(0, 2), (2, 0), (3, 5), (5, 3)]
    diagonal_pairs = [(index, index) for index in range(6)]

    middle_two = block_projection(calculus["two_basis"], middle_pairs)
    middle_junk = block_projection(calculus["junk_basis"], middle_pairs)
    middle_quotient = block_projection(calculus["quotient_basis"], middle_pairs)
    middle_junk_span = orthonormal_span(middle_junk)

    particle_middle_quotient = block_projection(
        calculus["quotient_basis"], particle_middle_pairs
    )
    conjugate_middle_quotient = block_projection(
        calculus["quotient_basis"], conjugate_middle_pairs
    )
    conjugate_middle_central = []
    conjugate_middle_traceless = []
    for column in conjugate_middle_quotient.T:
        matrix = column.reshape(3, 3)
        symmetric = 0.5 * (matrix + matrix.T)
        central = np.trace(symmetric) * np.eye(3) / 3.0
        conjugate_middle_central.append(central.reshape(-1))
        conjugate_middle_traceless.append((symmetric - central).reshape(-1))
    conjugate_middle_central = np.stack(conjugate_middle_central, axis=1)
    conjugate_middle_traceless = np.stack(conjugate_middle_traceless, axis=1)

    real_middle_two = realify(block_projection(calculus["real_two_basis"], middle_pairs))
    real_middle_junk = realify(block_projection(calculus["real_junk_basis"], middle_pairs))
    real_middle_quotient = realify(
        block_projection(calculus["real_quotient_basis"], middle_pairs)
    )

    moment = locking @ locking.T - abs(pairing) ** 2 * np.eye(3)
    target = np.zeros((18, 18), dtype=complex)
    target[3:6, 3:6] = moment
    target[12:15, 12:15] = moment

    return {
        "label": label,
        "locking_rank": int(np.linalg.matrix_rank(locking)),
        "pairing_absolute_value": float(abs(pairing)),
        "complexified_calculus": {
            "represented_one_rank": calculus["one_basis"].shape[1],
            "one_form_kernel_dimension": calculus["one_kernel_dimension"],
            "represented_two_rank": calculus["two_basis"].shape[1],
            "degree_two_junk_rank": calculus["junk_basis"].shape[1],
            "quotient_rank": calculus["quotient_basis"].shape[1],
            "junk_outside_twoforms": calculus["junk_outside_twoforms"],
            "middle_two_image_rank": orthonormal_span(middle_two).shape[1],
            "middle_junk_image_rank": middle_junk_span.shape[1],
            "middle_two_outside_middle_junk": span_residual(
                middle_two, middle_junk_span
            ),
            "canonical_quotient_middle_rank": orthonormal_span(
                middle_quotient
            ).shape[1],
            "canonical_quotient_particle_middle_rank": orthonormal_span(
                particle_middle_quotient
            ).shape[1],
            "canonical_quotient_conjugate_middle_rank": orthonormal_span(
                conjugate_middle_quotient
            ).shape[1],
            "canonical_quotient_conjugate_middle_central_rank": orthonormal_span(
                conjugate_middle_central
            ).shape[1],
            "canonical_quotient_conjugate_middle_traceless_symmetric_rank": orthonormal_span(
                conjugate_middle_traceless
            ).shape[1],
            "canonical_quotient_endpoint_rank": orthonormal_span(
                block_projection(calculus["quotient_basis"], endpoint_pairs)
            ).shape[1],
            "canonical_quotient_diagonal_rank": orthonormal_span(
                block_projection(calculus["quotient_basis"], diagonal_pairs)
            ).shape[1],
            "moment_target_outside_twoforms": target_residual(
                target, calculus["two_basis"]
            ),
            "moment_target_outside_junk": target_residual(
                target, calculus["junk_basis"]
            ),
            "moment_target_outside_canonical_quotient": target_residual(
                target, calculus["quotient_basis"]
            ),
        },
        "real_linear_calculus": {
            "represented_one_rank": calculus["real_one_rank"],
            "one_form_kernel_dimension": calculus["real_one_kernel_dimension"],
            "represented_two_rank": calculus["real_two_basis"].shape[1],
            "degree_two_junk_rank": calculus["real_junk_basis"].shape[1],
            "quotient_rank": calculus["real_quotient_basis"].shape[1],
            "middle_two_image_rank": orthonormal_span(real_middle_two).shape[1],
            "middle_junk_image_rank": orthonormal_span(real_middle_junk).shape[1],
            "middle_two_outside_middle_junk": span_residual(
                real_middle_two, orthonormal_span(real_middle_junk)
            ),
            "canonical_quotient_middle_rank": orthonormal_span(
                real_middle_quotient
            ).shape[1],
        },
    }


def particle_half_audit(locking, pairing):
    dirac = particle_dirac(locking, pairing)
    identity = np.eye(3)
    representations = [
        block_diagonal([scalar_left * identity, matrix_part, matrix_part])
        for matrix_part, scalar_left, _ in algebra_basis()
    ]
    calculus = represented_calculus(dirac, representations)
    particle_middle = block_projection(
        calculus["quotient_basis"], [(1, 1)], matrix_size=9
    )
    particle_middle_two = block_projection(
        calculus["two_basis"], [(1, 1)], matrix_size=9
    )
    particle_middle_junk = block_projection(
        calculus["junk_basis"], [(1, 1)], matrix_size=9
    )
    return {
        "represented_one_rank": calculus["one_basis"].shape[1],
        "represented_two_rank": calculus["two_basis"].shape[1],
        "degree_two_junk_rank": calculus["junk_basis"].shape[1],
        "quotient_rank": calculus["quotient_basis"].shape[1],
        "middle_two_image_rank": orthonormal_span(particle_middle_two).shape[1],
        "middle_junk_image_rank": orthonormal_span(particle_middle_junk).shape[1],
        "canonical_quotient_middle_rank": orthonormal_span(
            particle_middle
        ).shape[1],
    }


def three_point_control(first_weight, second_weight):
    size = 3
    dirac = np.zeros((size, size), dtype=complex)
    dirac[0, 1] = first_weight
    dirac[1, 0] = np.conj(first_weight)
    dirac[1, 2] = second_weight
    dirac[2, 1] = np.conj(second_weight)
    representations = []
    for index in range(size):
        representation = np.zeros((size, size), dtype=complex)
        representation[index, index] = 1.0
        representations.append(representation)
    calculus = represented_calculus(dirac, representations)
    endpoint = np.zeros((size, size), dtype=complex)
    endpoint[0, 2] = 1.0
    return {
        "weights": [str(first_weight), str(second_weight)],
        "represented_one_rank": calculus["one_basis"].shape[1],
        "represented_two_rank": calculus["two_basis"].shape[1],
        "degree_two_junk_rank": calculus["junk_basis"].shape[1],
        "quotient_rank": calculus["quotient_basis"].shape[1],
        "endpoint_outside_junk": target_residual(endpoint, calculus["junk_basis"]),
    }


def main():
    backgrounds = []
    for seed in RANDOM_SEEDS:
        rng = np.random.default_rng(seed)
        backgrounds.append(
            audit_background(
                rng.normal(size=(3, 3)),
                0.37 + 0.21j,
                f"generic_seed_{seed}",
            )
        )
    backgrounds.append(audit_background(np.eye(3), 1.0, "radial_unit"))
    backgrounds.append(audit_background(0.73 * np.eye(3), 0.23, "radial_condensed"))
    particle_half = particle_half_audit(
        np.random.default_rng(RANDOM_SEEDS[0]).normal(size=(3, 3)),
        0.37 + 0.21j,
    )

    controls = [
        three_point_control(1.0, 1.0),
        three_point_control(0.7 + 0.2j, 1.3 - 0.4j),
    ]

    generic = [row for row in backgrounds if row["label"].startswith("generic")]
    stable_complex_ranks = {
        key: sorted(
            {
                row["complexified_calculus"][key]
                for row in generic
            }
        )
        for key in [
            "represented_one_rank",
            "represented_two_rank",
            "degree_two_junk_rank",
            "quotient_rank",
            "middle_two_image_rank",
            "middle_junk_image_rank",
            "canonical_quotient_middle_rank",
            "canonical_quotient_particle_middle_rank",
            "canonical_quotient_conjugate_middle_rank",
            "canonical_quotient_conjugate_middle_central_rank",
            "canonical_quotient_conjugate_middle_traceless_symmetric_rank",
        ]
    }
    maximum_middle_residual = max(
        row["complexified_calculus"]["middle_two_outside_middle_junk"]
        for row in generic
    )
    maximum_real_middle_residual = max(
        row["real_linear_calculus"]["middle_two_outside_middle_junk"]
        for row in generic
    )

    results = {
        "date": "2026-08-15",
        "gate": "version4_family_defect_degree_two_junk_gate",
        "finite_geometry": {
            "algebra": "R_0 direct_sum M3(R)_G direct_sum C_2",
            "complex_hilbert_dimension": 18,
            "calculus": "represented universal forms modulo d(ker pi_1)",
            "algebra_real_basis_dimension": len(algebra_basis()),
        },
        "three_point_controls": controls,
        "particle_half_control": particle_half,
        "backgrounds": backgrounds,
        "generic_stability": {
            "complex_rank_sets": stable_complex_ranks,
            "maximum_middle_two_outside_middle_junk": maximum_middle_residual,
            "maximum_real_middle_two_outside_middle_junk": maximum_real_middle_residual,
        },
        "interpretation": {
            "complexified_generic_result": (
                "rank Omega1=20, represented Omega2=20, junk2=9, quotient OmegaD2=11"
            ),
            "middle_block_result": (
                "the particle middle M3 block is entirely junk; the doubled quotient retains only one central complex direction on the conjugate middle block"
            ),
            "symmetric_module_result": (
                "no traceless symmetric direction, hence no six-dimensional Sym3(R) curvature module, survives in the ordinary quotient"
            ),
            "control_result": (
                "the implementation reproduces the existing C^3 three-node result that the length-two endpoint matrix unit is junk"
            ),
        },
        "verdict": {
            "ordinary_degree_two_junk_route": "closed",
            "self_adjoint_Sym3_auxiliary_as_ordinary_represented_curvature": "failed",
            "real_classical_auxiliary_route": "closed_by_sign",
            "imaginary_HS_measure_route": "conditional_open",
            "modified_differential_calculus": "new_architecture_only",
            "physical_parent": "not_derived",
        },
    }

    assert all(control["endpoint_outside_junk"] < TOLERANCE for control in controls)
    assert all(values == [values[0]] for values in stable_complex_ranks.values())
    assert stable_complex_ranks["canonical_quotient_middle_rank"] == [1]
    assert stable_complex_ranks["canonical_quotient_particle_middle_rank"] == [0]
    assert stable_complex_ranks[
        "canonical_quotient_conjugate_middle_central_rank"
    ] == [1]
    assert stable_complex_ranks[
        "canonical_quotient_conjugate_middle_traceless_symmetric_rank"
    ] == [0]
    assert particle_half["canonical_quotient_middle_rank"] == 0

    Path("s2t_v4_family_defect_degree_two_junk_gate_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()