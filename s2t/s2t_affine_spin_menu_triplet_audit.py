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
        determinant = int(round(np.linalg.det(matrix))) % 2
        if determinant == 1:
            matrices.append(matrix)
    return matrices


def affine_permutation(matrix, translation):
    permutation = []
    for point in POINTS:
        image = (
            int((matrix[0, 0] * point[0] + matrix[0, 1] * point[1] + translation[0]) % 2),
            int((matrix[1, 0] * point[0] + matrix[1, 1] * point[1] + translation[1]) % 2),
        )
        permutation.append(POINT_INDEX[image])
    return tuple(permutation)


def permutation_matrix(permutation):
    matrix = np.zeros((4, 4), dtype=float)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def commutant_dimension(group_matrices):
    equations = []
    for representation in group_matrices:
        # vec(XR-RX)=0.
        equations.append(
            np.kron(representation.T, np.eye(4))
            - np.kron(np.eye(4), representation)
        )
    system = np.vstack(equations)
    rank = np.linalg.matrix_rank(system, tol=1e-10)
    return int(16 - rank)


def main():
    gl22 = invertible_matrices_f2()
    translations = POINTS
    permutations = sorted(
        {
            affine_permutation(matrix, translation)
            for matrix in gl22
            for translation in translations
        }
    )
    group_matrices = [permutation_matrix(permutation) for permutation in permutations]

    identity = np.eye(4)
    all_ones = np.ones((4, 4))
    singlet_projector = all_ones / 4.0
    triplet_projector = identity - singlet_projector
    complete_graph_laplacian = 4.0 * identity - all_ones
    heavy_singlet_operator = all_ones

    laplacian_eigenvalues = np.linalg.eigvalsh(complete_graph_laplacian)
    heavy_singlet_eigenvalues = np.linalg.eigvalsh(heavy_singlet_operator)

    max_singlet_invariance_error = max(
        float(np.linalg.norm(rep @ singlet_projector - singlet_projector @ rep))
        for rep in group_matrices
    )
    max_triplet_invariance_error = max(
        float(np.linalg.norm(rep @ triplet_projector - triplet_projector @ rep))
        for rep in group_matrices
    )
    commutant_dim = commutant_dimension(group_matrices)

    # Tensoring the anomaly-free SU5 generation package with the triplet
    # produces three identical anomaly-free copies.
    single_generation_dimension = 10 + 5
    triplet_matter_dimension = 3 * single_generation_dimension
    su5_anomaly_single = 1 - 1
    su5_anomaly_triplet = 3 * su5_anomaly_single

    results = {
        "status": "affine_spin_menu_has_canonical_one_plus_three_split_and_can_host_three_SU5_generations",
        "date": "2026-08-04",
        "menu": {
            "spin_torsor": "F2^2 with four points",
            "affine_group": "AGL(2,2)=F2^2 semidirect GL(2,2)",
            "group_order": len(permutations),
            "isomorphic_permutation_group": "S4",
            "interpretation": (
                "Unlike geometric automorphisms of K, the intrinsic relabeling group of the abstract "
                "four-state affine menu is the full symmetric group on four points."
            ),
        },
        "canonical_decomposition": {
            "permutation_representation_dimension": 4,
            "singlet_projector": singlet_projector.tolist(),
            "singlet_rank": int(round(np.trace(singlet_projector))),
            "triplet_projector": triplet_projector.tolist(),
            "triplet_rank": int(round(np.trace(triplet_projector))),
            "decomposition": "C4 = 1_uniform + 3_sum_zero",
            "max_singlet_invariance_error": max_singlet_invariance_error,
            "max_triplet_invariance_error": max_triplet_invariance_error,
        },
        "invariant_operator_algebra": {
            "commutant_dimension": commutant_dim,
            "basis": "span{I,J}",
            "consequence": (
                "Every fully affine-invariant Hermitian transition operator has form a I + b J "
                "and therefore preserves the same one-plus-three decomposition."
            ),
            "complete_graph_laplacian": "L=4I-J",
            "laplacian_eigenvalues": laplacian_eigenvalues.tolist(),
            "heavy_singlet_operator": "M=J",
            "heavy_singlet_eigenvalues": heavy_singlet_eigenvalues.tolist(),
            "interpretation": (
                "L has one zero uniform mode and a triply degenerate excited sector; J instead "
                "gives mass only to the uniform singlet and leaves a rank-three kernel."
            ),
        },
        "SU5_tensor_product": {
            "one_generation_representation": "10 + bar5",
            "single_generation_dimension": single_generation_dimension,
            "family_space": "triplet projector image",
            "three_generation_dimension": triplet_matter_dimension,
            "SU5_cubic_anomaly_single": su5_anomaly_single,
            "SU5_cubic_anomaly_three_copies": su5_anomaly_triplet,
            "finding": (
                "Tensoring the anomaly-free SU5 package with the canonical triplet produces three "
                "identical anomaly-free families without selecting three individual spin structures."
            ),
        },
        "gates": {
            "generation_count": {
                "passes": True,
                "finding": "the affine permutation representation canonically contains a rank-three sector",
            },
            "generation_equivalence": {
                "passes": True,
                "finding": "the triplet is an invariant irreducible standard S4 representation",
            },
            "origin_from_bare_geometry": {
                "passes": False,
                "finding": (
                    "full AGL(2,2) is a symmetry of the abstract menu, not the diffeomorphism-induced "
                    "symmetry of K; treating it as physical is the defining new III.0 postulate"
                ),
            },
            "mass_hierarchy_and_mixing": {
                "passes": False,
                "finding": (
                    "exact affine symmetry makes the three families degenerate; observed hierarchy "
                    "requires a derived symmetry-breaking operator"
                ),
            },
        },
        "scientific_verdict": {
            "positive": (
                "The menu interpretation supplies a canonical family-space decomposition 1+3. "
                "Combined with the SU5 fiber, it yields a mathematically clean three-generation carrier."
            ),
            "caveat": (
                "This is a new model principle, not evidence that nature uses the affine menu. "
                "The full affine symmetry must be justified dynamically, and exact symmetry gives no hierarchy."
            ),
            "next_gate": (
                "Use only the previously derived geometric subgroup that splits the three labels as 1+2 "
                "to construct a parameter-free first family-symmetry breaking operator, then test whether "
                "its eigenvalue pattern can support one heavy family and two lighter families."
            ),
        },
    }

    assert len(gl22) == 6
    assert len(permutations) == 24
    assert commutant_dim == 2
    assert abs(np.trace(singlet_projector) - 1.0) < 1e-12
    assert abs(np.trace(triplet_projector) - 3.0) < 1e-12
    assert max_singlet_invariance_error < 1e-12
    assert max_triplet_invariance_error < 1e-12
    assert np.allclose(laplacian_eigenvalues, [0.0, 4.0, 4.0, 4.0])
    assert np.allclose(heavy_singlet_eigenvalues, [0.0, 0.0, 0.0, 4.0])
    assert su5_anomaly_triplet == 0

    Path("s2t_affine_spin_menu_triplet_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "affine_group_order": len(permutations),
                "commutant_dimension": commutant_dim,
                "laplacian_eigenvalues": laplacian_eigenvalues.tolist(),
                "heavy_singlet_eigenvalues": heavy_singlet_eigenvalues.tolist(),
                "triplet_rank": int(round(np.trace(triplet_projector))),
                "next_gate": results["scientific_verdict"]["next_gate"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()