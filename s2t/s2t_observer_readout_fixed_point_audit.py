#!/usr/bin/env python3
import itertools
import json
from pathlib import Path

import numpy as np


POINTS = [(0, 0), (1, 0), (0, 1), (1, 1)]
POINT_INDEX = {point: index for index, point in enumerate(POINTS)}


def invertible_matrices_f2():
    matrices = []
    for entries in itertools.product([0, 1], repeat=4):
        matrix = np.array(entries, dtype=int).reshape(2, 2)
        if int(round(np.linalg.det(matrix))) % 2 == 1:
            matrices.append(matrix)
    return matrices


def affine_permutation(matrix, translation):
    permutation = []
    for point in POINTS:
        image = (
            int(
                (
                    matrix[0, 0] * point[0]
                    + matrix[0, 1] * point[1]
                    + translation[0]
                )
                % 2
            ),
            int(
                (
                    matrix[1, 0] * point[0]
                    + matrix[1, 1] * point[1]
                    + translation[1]
                )
                % 2
            ),
        )
        permutation.append(POINT_INDEX[image])
    return tuple(permutation)


def permutation_matrix(permutation):
    matrix = np.zeros((4, 4), dtype=float)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def translation_matrix(delta):
    return permutation_matrix(
        tuple(
            POINT_INDEX[((point[0] + delta[0]) % 2, (point[1] + delta[1]) % 2)]
            for point in POINTS
        )
    )


def random_unitary(rng, dimension):
    matrix = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    unitary, upper = np.linalg.qr(matrix)
    diagonal = np.diag(upper)
    phases = np.ones_like(diagonal)
    nonzero = np.abs(diagonal) > 0
    phases[nonzero] = diagonal[nonzero] / np.abs(diagonal[nonzero])
    return unitary @ np.diag(phases.conjugate())


def main():
    rng = np.random.default_rng(20260806)
    permutations = sorted(
        {
            affine_permutation(matrix, translation)
            for matrix in invertible_matrices_f2()
            for translation in POINTS
        }
    )
    affine_group = [permutation_matrix(permutation) for permutation in permutations]

    twirl_superoperator = sum(
        np.kron(representation, representation) for representation in affine_group
    ) / len(affine_group)
    twirl_rank = int(np.linalg.matrix_rank(twirl_superoperator, tol=1e-10))
    twirl_idempotence_error = float(
        np.linalg.norm(twirl_superoperator @ twirl_superoperator - twirl_superoperator)
    )

    identity4 = np.eye(4)
    uniform = np.ones(4) / 2.0
    singlet_projector = np.outer(uniform, uniform)
    triplet_projector = identity4 - singlet_projector
    character_basis = (
        np.array(
            [
                [1.0, -1.0, 1.0, -1.0],
                [1.0, 1.0, -1.0, -1.0],
                [1.0, -1.0, -1.0, 1.0],
            ]
        ).T
        / 2.0
    )

    test_operator = rng.normal(size=(4, 4))
    test_operator = (test_operator + test_operator.T) / 2.0
    twirled_operator = sum(
        representation @ test_operator @ representation.T
        for representation in affine_group
    ) / len(affine_group)
    triplet_block = character_basis.T @ twirled_operator @ character_basis
    triplet_scalar = np.trace(triplet_block) / 3.0
    triplet_scalar_error = float(
        np.linalg.norm(triplet_block - triplet_scalar * np.eye(3))
    )

    invariant_state_grid = np.linspace(0.0, 1.0, 101)
    invariant_states = [
        probability * singlet_projector
        + (1.0 - probability) * triplet_projector / 3.0
        for probability in invariant_state_grid
    ]
    invariant_state_trace_error = max(
        abs(np.trace(state) - 1.0) for state in invariant_states
    )
    invariant_state_twirl_error = max(
        np.linalg.norm(
            sum(
                representation @ state @ representation.T
                for representation in affine_group
            )
            / len(affine_group)
            - state
        )
        for state in invariant_states
    )

    channel_weights = rng.random(5)
    channel_weights /= channel_weights.sum()
    channel_unitaries = [random_unitary(rng, 4) for _ in range(5)]
    unital_error = float(
        np.linalg.norm(
            sum(
                weight * unitary.conjugate().T @ unitary
                for weight, unitary in zip(channel_weights, channel_unitaries)
            )
            - identity4
        )
    )
    scalar = 137.035999177
    scalar_operator = scalar * identity4
    scalar_readout = sum(
        weight * unitary.conjugate().T @ scalar_operator @ unitary
        for weight, unitary in zip(channel_weights, channel_unitaries)
    )
    scalar_invariance_error = float(np.linalg.norm(scalar_readout - scalar_operator))

    translate_rp3 = translation_matrix((1, 0))
    translate_s1 = translation_matrix((0, 1))
    restricted_rp3 = character_basis.T @ translate_rp3 @ character_basis
    restricted_s1 = character_basis.T @ translate_s1 @ character_basis
    canonical_compressed_commutator = float(
        np.linalg.norm(
            restricted_rp3 @ restricted_s1 - restricted_s1 @ restricted_rp3
        )
    )

    generic_commutators = []
    for _ in range(256):
        isometry = random_unitary(rng, 4)[:, :3]
        compressed_rp3 = isometry.conjugate().T @ translate_rp3 @ isometry
        compressed_s1 = isometry.conjugate().T @ translate_s1 @ isometry
        generic_commutators.append(
            float(
                np.linalg.norm(
                    compressed_rp3 @ compressed_s1
                    - compressed_s1 @ compressed_rp3
                )
            )
        )

    known_points = [-2, -1, 0, 1, 2]
    unseen_point = 3
    vanishing_polynomial_at_known = [
        int(np.prod([point - other for other in known_points]))
        for point in known_points
    ]
    unseen_perturbation = int(
        np.prod([unseen_point - point for point in known_points])
    )

    residual_axis = json.loads(
        Path("s2t_family_residual_axis_orbit_results.json").read_text(
            encoding="utf-8"
        )
    )

    results = {
        "status": "readout_hypothesis_survives_but_canonical_readout_is_too_coarse_and_noncanonical_readouts_are_nonunique",
        "date": "2026-08-06",
        "formal_candidate": {
            "source_algebra": "A=M4(C) for the finite four-state test",
            "observer_algebra": "B subset A",
            "readout": "a unital completely positive map R:A->B",
            "strong_readout": "an idempotent state-preserving conditional expectation",
            "fixed_point_condition": "R(X)=X for observable X in the image algebra",
        },
        "literature_basis": [
            {
                "source": "A. Jencova, Sufficiency in quantum statistical inference, quant-ph/0604091",
                "use": "unital 2-positive maps as quantum coarse-grainings",
            },
            {
                "source": "K. Furuya, N. Lashkari, S. Ouseph, arXiv:2012.14001",
                "use": "conditional expectations as observable-algebra coarse-graining and RG readout",
            },
            {
                "source": "J. de Boer et al., arXiv:2505.04682",
                "use": "modular invariance and uniqueness once state and subalgebra are fixed",
            },
        ],
        "finite_data_nonidentifiability": {
            "known_points": known_points,
            "vanishing_perturbation_on_known_points": vanishing_polynomial_at_known,
            "unseen_point": unseen_point,
            "perturbation_at_unseen_point": unseen_perturbation,
            "finding": (
                "Adding lambda times the vanishing polynomial preserves every known "
                "value and changes an unseen one. Observations alone cannot identify "
                "a unique readout."
            ),
        },
        "central_scalar_gate": {
            "channel": "deterministic random-unitary unital CP map with five branches",
            "unital_error": unital_error,
            "scalar_invariance_error": scalar_invariance_error,
            "theorem": "Every unital linear readout satisfies R(c I)=c I.",
            "finding": (
                "Coarse-graining cannot repair a wrong centrally represented constant. "
                "A rescue requires noncentral operator encoding or new dynamics."
            ),
        },
        "S4_covariant_conditional_expectation": {
            "group_order": len(affine_group),
            "formula": "E_S4(A)=|S4|^-1 sum_g U_g A U_g^dagger",
            "fixed_algebra_dimension": twirl_rank,
            "idempotence_error": twirl_idempotence_error,
            "triplet_scalar_error": triplet_scalar_error,
            "fixed_algebra": "span{P_singlet,P_triplet}",
            "invariant_state_family": "rho(p)=p P_singlet+(1-p) P_triplet/3",
            "sampled_invariant_states": len(invariant_states),
            "maximum_trace_error": float(invariant_state_trace_error),
            "maximum_twirl_fixed_point_error": float(invariant_state_twirl_error),
            "finding": (
                "The affine-covariant twirl preserves the one-plus-three split but "
                "makes every triplet observable scalar. It cannot select masses, an "
                "axis, or CKM mixing, and its fixed states form a continuum."
            ),
        },
        "compression_fork": {
            "source_factor_operators_commute": True,
            "canonical_triplet_commutator_norm": canonical_compressed_commutator,
            "generic_rank3_UCP_compressions": len(generic_commutators),
            "nonzero_generic_commutators": sum(
                value > 1e-10 for value in generic_commutators
            ),
            "minimum_commutator_norm": min(generic_commutators),
            "median_commutator_norm": float(np.median(generic_commutators)),
            "maximum_commutator_norm": max(generic_commutators),
            "finding": (
                "A nonreducing observer compression can manufacture apparent "
                "noncommutativity and mixing from commuting source operators, but the "
                "compression is free unless derived from state, modular flow, or action."
            ),
        },
        "existing_axis_gate": {
            "single_axis_orbit_unique_modulo_residual_symmetry": residual_axis[
                "orbit_test"
            ]["same_orbit"],
            "remaining_relative_choices": residual_axis["two_sector_gate"][
                "remaining_relative_choices"
            ],
        },
        "scientific_verdict": {
            "positive": (
                "Observer compression can create effective structures absent from the "
                "commuting source presentation."
            ),
            "negative": (
                "The canonical symmetry-preserving readout is too coarse, central "
                "mismatches are invariant, and flexible readouts are infinitely nonunique."
            ),
            "next_gate": (
                "Derive a state omega and observable subalgebra B from the primary source, "
                "verify modular invariance, construct the unique omega-preserving "
                "conditional expectation, and only then compute blind observables."
            ),
        },
    }

    assert len(affine_group) == 24
    assert twirl_rank == 2
    assert twirl_idempotence_error < 1e-12
    assert triplet_scalar_error < 1e-12
    assert scalar_invariance_error < 1e-10
    assert canonical_compressed_commutator < 1e-12
    assert all(value > 1e-10 for value in generic_commutators)
    assert vanishing_polynomial_at_known == [0, 0, 0, 0, 0]
    assert unseen_perturbation == 120
    assert residual_axis["orbit_test"]["same_orbit"]

    Path("s2t_observer_readout_fixed_point_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "twirl_fixed_algebra_dimension": twirl_rank,
                "canonical_commutator": canonical_compressed_commutator,
                "generic_noncommuting_compressions": sum(
                    value > 1e-10 for value in generic_commutators
                ),
                "generic_compression_count": len(generic_commutators),
                "unseen_readout_ambiguity": unseen_perturbation,
                "next_gate": results["scientific_verdict"]["next_gate"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()