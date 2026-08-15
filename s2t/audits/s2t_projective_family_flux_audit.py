#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np


POINTS = [(0, 0), (1, 0), (0, 1), (1, 1)]
POINT_INDEX = {point: index for index, point in enumerate(POINTS)}


def algebra_dimension(generators):
    dimension = generators[0].shape[0]
    basis = []

    def add(matrix):
        old_dimension = len(basis)
        trial = basis + [matrix]
        rank = np.linalg.matrix_rank(
            np.stack([item.reshape(-1) for item in trial]), tol=1e-10
        )
        if rank > old_dimension:
            basis.append(matrix)
            return True
        return False

    add(np.eye(dimension))
    for generator in generators:
        add(generator)
    changed = True
    while changed:
        changed = False
        old_basis = list(basis)
        for matrix in old_basis:
            for generator in generators:
                changed = add(matrix @ generator) or changed
    return len(basis)


def commutant_dimension(representations):
    dimension = representations[0].shape[0]
    equations = [
        np.kron(rep.T, np.eye(dimension)) - np.kron(np.eye(dimension), rep)
        for rep in representations
    ]
    rank = np.linalg.matrix_rank(np.vstack(equations), tol=1e-10)
    return int(dimension * dimension - rank)


def main():
    magnetic_rp3 = np.zeros((4, 4), dtype=float)
    magnetic_s1 = np.zeros((4, 4), dtype=float)
    for p, q in POINTS:
        magnetic_rp3[POINT_INDEX[((p + 1) % 2, q)], POINT_INDEX[(p, q)]] = (
            -1.0
        ) ** q
        magnetic_s1[POINT_INDEX[(p, (q + 1) % 2)], POINT_INDEX[(p, q)]] = 1.0

    identity4 = np.eye(4)
    uniform = np.ones(4) / 2.0
    singlet_projector = np.outer(uniform, uniform)
    triplet_projector = identity4 - singlet_projector
    eigenvalues, eigenvectors = np.linalg.eigh(triplet_projector)
    triplet_basis = eigenvectors[:, eigenvalues > 0.5]

    compressed_rp3 = triplet_basis.T @ magnetic_rp3 @ triplet_basis
    compressed_s1 = triplet_basis.T @ magnetic_s1 @ triplet_basis
    rp3_leakage = float(
        np.linalg.norm(singlet_projector @ magnetic_rp3 @ triplet_projector)
    )
    s1_leakage = float(
        np.linalg.norm(singlet_projector @ magnetic_s1 @ triplet_projector)
    )

    results = {
        "status": "nontrivial_Z2_projective_flux_gives_fixed_noncommutativity_but_is_incompatible_with_three_family_triplet",
        "date": "2026-08-05",
        "projective_translation_algebra": {
            "U2_error": float(np.linalg.norm(magnetic_rp3 @ magnetic_rp3 - identity4)),
            "V2_error": float(np.linalg.norm(magnetic_s1 @ magnetic_s1 - identity4)),
            "UV_plus_VU_error": float(
                np.linalg.norm(
                    magnetic_rp3 @ magnetic_s1
                    + magnetic_s1 @ magnetic_rp3
                )
            ),
            "relation": "U^2=V^2=I, UV=-VU",
            "interpretation": (
                "The unique nontrivial projective sign supplies coefficient-free "
                "noncommutativity, equivalent to one Z2 magnetic flux quantum."
            ),
        },
        "odd_dimension_obstruction": {
            "statement": (
                "If UV=-VU on dimension d, determinants imply det(UV)=(-1)^d det(VU). "
                "For invertible U,V and odd d this is impossible."
            ),
            "three_dimensional_projective_representation_exists": False,
            "consequence": (
                "The flux algebra cannot act intrinsically on the three-family carrier."
            ),
        },
        "one_plus_three_compatibility": {
            "RP3_translation_singlet_triplet_leakage": rp3_leakage,
            "S1_translation_singlet_triplet_leakage": s1_leakage,
            "triplet_is_jointly_invariant": False,
            "finding": (
                "At least one magnetic translation mixes the uniform reference state with "
                "the family triplet, so the canonical C4=1+3 split is lost."
            ),
        },
        "compressed_triplet_test": {
            "compressed_U_eigenvalues": np.linalg.eigvalsh(compressed_rp3).tolist(),
            "compressed_V_eigenvalues": np.linalg.eigvalsh(compressed_s1).tolist(),
            "generated_algebra_dimension": algebra_dimension(
                [compressed_rp3, compressed_s1]
            ),
            "commutant_dimension": commutant_dimension(
                [compressed_rp3, compressed_s1]
            ),
            "finding": (
                "Projection back to the triplet breaks the projective group law and still "
                "leaves a reducible 1+2 algebra rather than a canonical full M3 mixing algebra."
            ),
        },
        "decoupling_cost": {
            "proposal": "keep the four-state flux carrier and make the reference state heavy",
            "obstruction": (
                "The reference state is not invariant under the flux translations. Its "
                "elimination requires an additional heavy scale and produces a scale-dependent "
                "Schur complement, reintroducing the coefficient that the construction sought to avoid."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "A topological Z2 cocycle is the first mechanism found here that creates exact "
                "noncommutativity without a continuously fitted coefficient."
            ),
            "no_go": (
                "Its irreducible representations are even-dimensional, so it cannot preserve "
                "the current three-generation triplet. The minimal flux rescue and the 1+3 "
                "generation mechanism are mutually incompatible."
            ),
            "fork": (
                "Either retain the three-family menu and seek a richer discrete incidence "
                "structure, or abandon the 1+3 mechanism and rebuild generation counting in "
                "an even-dimensional projective carrier."
            ),
        },
    }

    assert results["projective_translation_algebra"]["U2_error"] < 1e-12
    assert results["projective_translation_algebra"]["V2_error"] < 1e-12
    assert results["projective_translation_algebra"]["UV_plus_VU_error"] < 1e-12
    assert rp3_leakage > 0.9
    assert not results["odd_dimension_obstruction"]["three_dimensional_projective_representation_exists"]
    assert results["compressed_triplet_test"]["generated_algebra_dimension"] == 5
    assert results["compressed_triplet_test"]["commutant_dimension"] == 2

    Path("s2t_projective_family_flux_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "flux_relation_error": results["projective_translation_algebra"]["UV_plus_VU_error"],
                "triplet_leakage": rp3_leakage,
                "compressed_algebra_dimension": results["compressed_triplet_test"]["generated_algebra_dimension"],
                "compressed_commutant_dimension": results["compressed_triplet_test"]["commutant_dimension"],
                "odd_dimensional_representation": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()