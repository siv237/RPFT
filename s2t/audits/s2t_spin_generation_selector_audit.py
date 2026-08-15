import itertools
import json
from pathlib import Path

import numpy as np


def matrix_tuple(matrix):
    return tuple(int(value) for value in matrix.flatten())


def apply(matrix, vector):
    result = matrix @ np.array(vector, dtype=int)
    return tuple(int(value % 2) for value in result)


def orbit(group, vector):
    return sorted({apply(matrix, vector) for matrix in group})


def main():
    vectors = [(0, 0), (1, 0), (0, 1), (1, 1)]
    nonzero_vectors = [vector for vector in vectors if vector != (0, 0)]

    gl22 = []
    for entries in itertools.product([0, 1], repeat=4):
        matrix = np.array(entries, dtype=int).reshape(2, 2)
        determinant_mod2 = int(round(np.linalg.det(matrix))) % 2
        if determinant_mod2 == 1:
            gl22.append(matrix)

    # Geometric automorphisms induced from Aut(Z2 x Z) preserve the torsion
    # subgroup. On spin labels (p,q), they act as (p,q)->(p,q+epsilon*p).
    geometric_group = [
        np.array([[1, 0], [0, 1]], dtype=int),
        np.array([[1, 0], [1, 1]], dtype=int),
    ]

    full_orbit = orbit(gl22, (1, 0))
    geometric_orbits = []
    unseen = set(nonzero_vectors)
    while unseen:
        seed = sorted(unseen)[0]
        current = orbit(geometric_group, seed)
        geometric_orbits.append(current)
        unseen -= set(current)

    # Factorwise standard fillings select one reference spin structure.
    # RP3 bounds the even Euler-number disk bundle over S2; S1 bounds D2.
    spin_structures_total = 4
    factorwise_bounding_reference_count = 1
    nonreference_count = spin_structures_total - factorwise_bounding_reference_count

    results = {
        "status": "bounding_reference_gives_three_nonreference_spin_sectors_but_geometry_splits_them_into_one_plus_two",
        "date": "2026-08-04",
        "spin_label_space": {
            "torsor": "H1(K,Z2)=F2^2",
            "labels_after_reference_choice": vectors,
            "reference": [0, 0],
            "nonreference": [list(vector) for vector in nonzero_vectors],
            "total_count": spin_structures_total,
            "nonreference_count": nonreference_count,
        },
        "reference_selector": {
            "RP3_filling": (
                "oriented disk bundle over S2 with Euler number 2; it retracts to S2, is spin "
                "because the Euler class is even, and has H1=0, so it induces one boundary spin structure"
            ),
            "S1_filling": "D2 selects the bounding (antiperiodic) spin structure",
            "product_rule": (
                "the pair of factorwise bounding structures is the unique reference among the four product structures"
            ),
            "status": "conditional_geometric_reference_if_standard_factor_fillings_are_part_of_the_model",
        },
        "abstract_affine_symmetry": {
            "group": "GL(2,2)",
            "order": len(gl22),
            "isomorphic_to": "S3",
            "nonzero_orbit": [list(vector) for vector in full_orbit],
            "transitive_on_three_nonzero_labels": len(full_orbit) == 3,
            "interpretation": (
                "If the theory possessed the full affine-label symmetry, the three nonreference "
                "spin sectors would form one generation triplet."
            ),
        },
        "geometric_automorphism_gate": {
            "integral_fundamental_group": "Z2 x Z",
            "constraint": "automorphisms preserve the unique torsion subgroup Z2",
            "induced_mod2_group_order": len(geometric_group),
            "matrices": [list(matrix_tuple(matrix)) for matrix in geometric_group],
            "nonzero_orbits": [
                [list(vector) for vector in current] for current in geometric_orbits
            ],
            "orbit_sizes": sorted(len(current) for current in geometric_orbits),
            "transitive_on_three_nonzero_labels": len(geometric_orbits) == 1,
            "interpretation": (
                "The natural automorphisms of K distinguish the pure circle spin twist from the "
                "two sectors carrying the RP3 torsion twist. The orbit pattern is 1+2, not 3."
            ),
        },
        "spectral_cross_check": {
            "RP3_spin_eta_invariants": [-0.25, 0.25],
            "S1_bounding_gap": 0.5,
            "S1_nonbounding_gap": 0.0,
            "interpretation": (
                "The four structures are spectrally distinguishable rather than automatically degenerate."
            ),
        },
        "gates": {
            "three_sector_count": {
                "passes": True,
                "finding": "one factorwise bounding reference leaves exactly three nonreference spin sectors",
            },
            "three_sector_equivalence_from_K": {
                "passes": False,
                "finding": "Aut(Z2 x Z) induces only a two-element subgroup with nonzero orbit split 1+2",
            },
            "generation_triplet": {
                "passes": False,
                "finding": (
                    "three equivalent generations require an extra emergent GL(2,2)=S3 flavor "
                    "symmetry or another operator that restores transitivity"
                ),
            },
        },
        "scientific_verdict": {
            "positive": (
                "The count three can be obtained geometrically once standard factor fillings define "
                "a unique bounding reference spin structure."
            ),
            "negative": (
                "The topology of K alone does not make the remaining three sectors equivalent; it "
                "distinguishes one from a pair."
            ),
            "next_gate": (
                "Derive or reject an emergent S3 action on the three nonreference sectors from the "
                "SU(5) fiber/transition algebra, without postulating family symmetry separately."
            ),
        },
    }

    assert len(gl22) == 6
    assert len(full_orbit) == 3
    assert spin_structures_total == 4
    assert nonreference_count == 3
    assert sorted(len(current) for current in geometric_orbits) == [1, 2]
    assert not results["geometric_automorphism_gate"][
        "transitive_on_three_nonzero_labels"
    ]

    Path("s2t_spin_generation_selector_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "nonreference_count": nonreference_count,
                "GL22_order": len(gl22),
                "abstract_nonzero_orbit": full_orbit,
                "geometric_orbits": geometric_orbits,
                "next_gate": results["scientific_verdict"]["next_gate"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()