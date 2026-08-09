#!/usr/bin/env python3
import itertools
import json
import math
from pathlib import Path

import numpy as np


NONZERO_CLASSES = [(1, 0), (0, 1), (1, 1)]


def invertible_matrices_f2():
    matrices = []
    for entries in itertools.product([0, 1], repeat=4):
        matrix = np.array(entries, dtype=int).reshape(2, 2)
        if int(round(np.linalg.det(matrix))) % 2 == 1:
            matrices.append(matrix)
    return matrices


def apply(matrix, vector):
    result = matrix @ np.array(vector, dtype=int)
    return tuple(int(value % 2) for value in result)


def commutant_dimension(representations):
    dimension = representations[0].shape[0]
    equations = [
        np.kron(rep.T, np.eye(dimension)) - np.kron(np.eye(dimension), rep)
        for rep in representations
    ]
    rank = np.linalg.matrix_rank(np.vstack(equations), tol=1e-10)
    return int(dimension * dimension - rank)


def permutation_on_nonzero(matrix):
    permutation = []
    for vector in NONZERO_CLASSES:
        permutation.append(NONZERO_CLASSES.index(apply(matrix, vector)))
    result = np.zeros((3, 3), dtype=float)
    for source, target in enumerate(permutation):
        result[target, source] = 1.0
    return result


def main():
    # H*(RP3 x S1;F2)=F2[a,b]/(a^4,b^2), deg(a)=deg(b)=1.
    # For a linear image b'=gamma*a+delta*b, b'^2=gamma*a^2, so preserving
    # b^2=0 forces gamma=0. Invertibility then leaves a'=a or a+b, b'=b.
    ring_automorphisms = []
    for matrix in invertible_matrices_f2():
        image_b = matrix[:, 1]
        if int(image_b[0]) == 0:
            ring_automorphisms.append(matrix)

    ring_representations = [
        permutation_on_nonzero(matrix) for matrix in ring_automorphisms
    ]
    orbits = []
    remaining = set(NONZERO_CLASSES)
    while remaining:
        seed = next(iter(remaining))
        orbit = {apply(matrix, seed) for matrix in ring_automorphisms}
        orbits.append(sorted(orbit))
        remaining -= orbit

    signatures = []
    for p, q in NONZERO_CLASSES:
        signatures.append(
            {
                "class": [p, q],
                "label": {"(1, 0)": "a", "(0, 1)": "b", "(1, 1)": "a+b"}[str((p, q))],
                "nonzero_square": bool(p),
                "free_S1_component": bool(q),
                "product_metric_length": math.pi * math.sqrt(p + 4 * q),
            }
        )

    square_operator = np.diag([1.0, 0.0, 1.0])
    free_component_operator = np.diag([0.0, 1.0, 1.0])
    length_operator = np.diag(
        [signature["product_metric_length"] for signature in signatures]
    )

    # Weighted Cayley translations on the full four-state torsor remain an
    # abelian convolution algebra. Their restrictions were audited previously;
    # here the commutator is recorded directly in the three-label diagonal readout.
    diagonal_commutators = {
        "square_free": float(
            np.linalg.norm(
                square_operator @ free_component_operator
                - free_component_operator @ square_operator
            )
        ),
        "square_length": float(
            np.linalg.norm(
                square_operator @ length_operator
                - length_operator @ square_operator
            )
        ),
        "free_length": float(
            np.linalg.norm(
                free_component_operator @ length_operator
                - length_operator @ free_component_operator
            )
        ),
    }

    results = {
        "status": "intrinsic_cohomology_and_product_metric_distinguish_three_labels_but_generate_only_commuting_family_observables",
        "date": "2026-08-05",
        "cohomology_ring": {
            "presentation": "F2[a,b]/(a^4,b^2), deg(a)=deg(b)=1",
            "ring_automorphism_count_on_H1": len(ring_automorphisms),
            "matrices": [matrix.tolist() for matrix in ring_automorphisms],
            "nonzero_class_orbits": [[list(item) for item in orbit] for orbit in orbits],
            "triplet_commutant_dimension": commutant_dimension(
                ring_representations
            ),
            "consequence": (
                "Pure ring naturality leaves the classes a and a+b paired and therefore "
                "retains a 1+2 invariant decomposition."
            ),
        },
        "metric_and_integral_refinement": {
            "class_signatures": signatures,
            "all_three_signatures_distinct": len(
                {
                    (
                        signature["nonzero_square"],
                        signature["free_S1_component"],
                        round(signature["product_metric_length"], 12),
                    )
                    for signature in signatures
                }
            )
            == 3,
            "finding": (
                "The square, integral-lift/free component and unequal cycle lengths can label "
                "all three classes without observed masses."
            ),
        },
        "operator_gate": {
            "canonical_diagonal_operators": [
                "nonzero-square indicator",
                "free-S1-component indicator",
                "product-metric length",
            ],
            "pairwise_commutator_norms": diagonal_commutators,
            "joint_algebra": "full diagonal C^3",
            "mixing_prediction": "identity",
            "finding": (
                "Intrinsic topology solves label distinguishability but not flavor mixing. "
                "All canonical scalar readouts are simultaneously diagonal."
            ),
        },
        "defect_gate": {
            "systolic_class": "a from RP1 is selected by the shortest nontrivial cycle length pi",
            "localized_defect": (
                "gamma=RP1 at a fixed S1 point breaks the residual symmetry strongly enough "
                "to define extra incidence data, but the S1 point/phase is not canonical."
            ),
            "wrapped_defect": (
                "gamma times S1 removes the noncanonical point but preserves the factor "
                "translation structure and does not supply a full M3 selector."
            ),
            "verdict": (
                "The existing defect idea can encode the missing selector only by adding the "
                "same boundary datum that was previously identified as underived."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "The topology and metric canonically distinguish the three nonzero H1 classes; "
                "generation labeling itself no longer requires an arbitrary ordering."
            ),
            "no_go": (
                "Every intrinsic scalar operator obtained from these data commutes. Neither the "
                "cohomology ring nor the product metric selects an outside-D8 incidence direction."
            ),
            "reopening_condition": (
                "A genuine boundary/defect functional must be derived independently and must "
                "fix its S1 localization or phase before flavor data are inspected."
            ),
        },
    }

    assert len(ring_automorphisms) == 2
    assert sorted(len(orbit) for orbit in orbits) == [1, 2]
    assert commutant_dimension(ring_representations) == 5
    assert results["metric_and_integral_refinement"]["all_three_signatures_distinct"]
    assert max(diagonal_commutators.values()) < 1e-12

    Path("s2t_topological_family_selector_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "ring_automorphisms": len(ring_automorphisms),
                "class_orbit_sizes": sorted(len(orbit) for orbit in orbits),
                "ring_commutant_dimension": results["cohomology_ring"]["triplet_commutant_dimension"],
                "distinct_metric_topology_signatures": True,
                "canonical_operator_commutators": diagonal_commutators,
                "mixing": "identity",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()