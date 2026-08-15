import json
from pathlib import Path

import numpy as np


def main():
    # Point order: (0,0), (1,0), (0,1), (1,1).
    # The geometric shear (p,q)->(p,q+p) swaps points 1 and 3.
    shear = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
        ]
    )
    identity = np.eye(4)
    all_ones = np.ones((4, 4))
    singlet_projector = all_ones / 4.0
    triplet_projector = identity - singlet_projector
    odd_projector = 0.5 * (identity - shear)

    triplet_odd_projector = triplet_projector @ odd_projector @ triplet_projector
    triplet_odd_projector = 0.5 * (
        triplet_odd_projector + triplet_odd_projector.T
    )

    shear_eigenvalues = np.linalg.eigvalsh(shear)
    triplet_odd_eigenvalues = np.linalg.eigvalsh(triplet_odd_projector)

    # Extract an orthonormal triplet basis from the projector eigenvectors.
    eigenvalues, eigenvectors = np.linalg.eigh(triplet_projector)
    triplet_basis = eigenvectors[:, eigenvalues > 0.5]
    restricted_shear = triplet_basis.T @ shear @ triplet_basis
    restricted_odd = triplet_basis.T @ odd_projector @ triplet_basis
    restricted_shear_eigenvalues = np.linalg.eigvalsh(restricted_shear)
    restricted_odd_eigenvalues = np.linalg.eigvalsh(restricted_odd)

    # Leading universal Yukawa texture, up to one overall sector scale.
    leading_texture = restricted_odd
    texture_rank = int(np.linalg.matrix_rank(leading_texture, tol=1e-10))
    texture_eigenvalues = np.linalg.eigvalsh(leading_texture)

    # If the same family projector appears in up and down sectors, their left
    # diagonalization bases can be aligned and CKM is the identity at leading order.
    ckm_leading = np.eye(3)

    results = {
        "status": "geometric_shear_projects_to_canonical_rank_one_family_texture_one_heavy_two_massless",
        "date": "2026-08-04",
        "input": {
            "family_space": "canonical S4 triplet im(I-J/4)",
            "geometric_subgroup": "Z2 shear induced by Aut(Z2 x Z)",
            "shear_action": "(p,q)->(p,q+p)",
        },
        "four_state_action": {
            "shear_matrix": shear.tolist(),
            "shear_eigenvalues": shear_eigenvalues.tolist(),
            "odd_projector": "P_minus=(I-S)/2",
            "odd_projector_rank_in_C4": int(
                np.linalg.matrix_rank(odd_projector, tol=1e-10)
            ),
            "uniform_singlet_is_even": float(
                np.linalg.norm(odd_projector @ np.ones(4))
            )
            < 1e-12,
        },
        "triplet_restriction": {
            "restricted_shear_eigenvalues": restricted_shear_eigenvalues.tolist(),
            "restricted_odd_projector_eigenvalues": restricted_odd_eigenvalues.tolist(),
            "triplet_odd_projector_full_C4_eigenvalues": triplet_odd_eigenvalues.tolist(),
            "rank": texture_rank,
            "pattern": "2 even family directions + 1 odd family direction",
        },
        "leading_family_texture": {
            "operator": "Y_family proportional to P_minus restricted to triplet",
            "eigenvalues_up_to_overall_scale": texture_eigenvalues.tolist(),
            "rank": texture_rank,
            "mass_pattern": "(0,0,1) up to permutation and overall scale",
            "interpretation": (
                "At exact geometric-subgroup order, one family can be massive while two remain "
                "massless. This is a canonical rank-one leading texture, not a fitted hierarchy."
            ),
        },
        "mixing": {
            "universal_projector_assumption": (
                "the same P_minus acts in up, down and charged-lepton family spaces"
            ),
            "leading_CKM": ckm_leading.tolist(),
            "interpretation": (
                "Aligned rank-one textures give identity CKM at leading order; observed small mixing "
                "would require controlled subleading breaking."
            ),
        },
        "gates": {
            "one_heavy_family": {
                "passes": True,
                "finding": "the unique odd projector has rank one on the canonical triplet",
            },
            "two_light_families": {
                "passes": True,
                "finding": "the even eigenspace has dimension two and is massless at leading order",
            },
            "full_hierarchy": {
                "passes": False,
                "finding": "no second parameter-free geometric operator splits the even doublet",
            },
            "realistic_mixing": {
                "passes": False,
                "finding": "the universal leading projector predicts exact alignment",
            },
        },
        "scientific_verdict": {
            "positive": (
                "The menu construction now derives a standard qualitative flavor pattern: one heavy "
                "family and two light families from a canonical rank-one projector."
            ),
            "limit": (
                "It does not derive nonzero first/second-family masses, their ratio, CKM angles or "
                "different textures across fermion sectors."
            ),
            "stop_rule": (
                "Do not fit a generic perturbation matrix. Reopen only if another discrete operator "
                "already present in the menu or SU5 fiber splits the even two-dimensional subspace."
            ),
        },
    }

    assert np.allclose(shear @ shear, identity)
    assert np.allclose(shear_eigenvalues, [-1.0, 1.0, 1.0, 1.0])
    assert np.allclose(restricted_shear_eigenvalues, [-1.0, 1.0, 1.0])
    assert np.allclose(restricted_odd_eigenvalues, [0.0, 0.0, 1.0])
    assert texture_rank == 1
    assert np.linalg.norm(odd_projector @ np.ones(4)) < 1e-12

    Path("s2t_family_rank_one_breaking_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "restricted_shear_eigenvalues": restricted_shear_eigenvalues.tolist(),
                "family_texture_eigenvalues": texture_eigenvalues.tolist(),
                "texture_rank": texture_rank,
                "mass_pattern": results["leading_family_texture"]["mass_pattern"],
                "stop_rule": results["scientific_verdict"]["stop_rule"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()