import json
import math
from pathlib import Path

import numpy as np


POINTS = [(0, 0), (1, 0), (0, 1), (1, 1)]
POINT_INDEX = {point: index for index, point in enumerate(POINTS)}


def permutation_matrix(action):
    matrix = np.zeros((4, 4))
    for source, point in enumerate(POINTS):
        target = POINT_INDEX[action(*point)]
        matrix[target, source] = 1.0
    return matrix


def generated_group(generators):
    identity = np.eye(generators[0].shape[0])
    group = {tuple(identity.flatten()): identity}
    changed = True
    while changed:
        changed = False
        current = list(group.values())
        for left in current:
            for right in generators + current:
                product = left @ right
                key = tuple(np.rint(product).astype(int).flatten())
                if key not in group:
                    group[key] = product
                    changed = True
    return list(group.values())


def commutant_dimension(representations):
    dimension = representations[0].shape[0]
    equations = []
    for representation in representations:
        equations.append(
            np.kron(representation.T, np.eye(dimension))
            - np.kron(np.eye(dimension), representation)
        )
    rank = np.linalg.matrix_rank(np.vstack(equations), tol=1e-10)
    return int(dimension**2 - rank)


def log_rms(prediction, target):
    prediction = np.array(prediction, dtype=float)
    target = np.array(target, dtype=float)
    return float(np.sqrt(np.mean(np.log(prediction / target) ** 2)))


def main():
    translate_rp3 = permutation_matrix(lambda p, q: ((p + 1) % 2, q))
    translate_s1 = permutation_matrix(lambda p, q: (p, (q + 1) % 2))
    shear = permutation_matrix(lambda p, q: (p, (q + p) % 2))
    identity = np.eye(4)
    triplet_projector = identity - np.ones((4, 4)) / 4.0

    character_basis = np.array(
        [
            [1.0, -1.0, 1.0, -1.0],
            [1.0, 1.0, -1.0, -1.0],
            [1.0, -1.0, -1.0, 1.0],
        ]
    ).T / 2.0
    assert np.allclose(character_basis.T @ character_basis, np.eye(3))
    assert np.allclose(
        character_basis @ character_basis.T, triplet_projector
    )

    restricted_rp3 = character_basis.T @ translate_rp3 @ character_basis
    restricted_s1 = character_basis.T @ translate_s1 @ character_basis
    restricted_shear = character_basis.T @ shear @ character_basis

    geometric_group = generated_group([translate_rp3, translate_s1, shear])
    restricted_group = [
        character_basis.T @ element @ character_basis
        for element in geometric_group
    ]

    length_rp3 = math.pi
    length_s1 = 2.0 * math.pi
    kernels = {
        "inverse_length_laplacian": (
            1.0 / length_rp3,
            1.0 / length_s1,
        ),
        "inverse_square_laplacian": (
            1.0 / length_rp3**2,
            1.0 / length_s1**2,
        ),
        "tunneling_laplacian": (
            math.exp(-length_rp3),
            math.exp(-length_s1),
        ),
    }

    kernel_rows = []
    for name, (weight_rp3, weight_s1) in kernels.items():
        operator = (
            weight_rp3 * (identity - translate_rp3)
            + weight_s1 * (identity - translate_s1)
        )
        restricted = character_basis.T @ operator @ character_basis
        eigenvalues = np.linalg.eigvalsh(restricted)
        kernel_rows.append(
            {
                "kernel": name,
                "weight_rp3": weight_rp3,
                "weight_s1": weight_s1,
                "eigenvalues": eigenvalues.tolist(),
                "normalized_pattern": (eigenvalues / eigenvalues[-1]).tolist(),
            }
        )

    additive_winding_pattern = np.array(
        [
            math.exp(-(length_rp3 + length_s1)),
            math.exp(-length_s1),
            math.exp(-length_rp3),
        ]
    )
    additive_winding_pattern /= additive_winding_pattern[-1]

    observed_patterns = {
        "charged_leptons": np.array(
            [0.51099895 / 1776.93, 105.6583755 / 1776.93, 1.0]
        ),
        "down_quarks_at_declared_scales": np.array(
            [4.67 / 4180.0, 93.4 / 4180.0, 1.0]
        ),
        "up_quarks_at_declared_scales": np.array(
            [2.16 / 172500.0, 1270.0 / 172500.0, 1.0]
        ),
    }
    hierarchy_comparison = {}
    natural_patterns = {
        row["kernel"]: row["normalized_pattern"] for row in kernel_rows
    }
    natural_patterns["additive_winding_amplitudes"] = (
        additive_winding_pattern.tolist()
    )
    for sector, target in observed_patterns.items():
        hierarchy_comparison[sector] = {
            "target": target.tolist(),
            "candidates": {
                name: {
                    "pattern": pattern,
                    "log_RMS": log_rms(pattern[:2], target[:2]),
                    "multiplicative_errors": (
                        np.array(pattern[:2]) / target[:2]
                    ).tolist(),
                }
                for name, pattern in natural_patterns.items()
            },
        }

    results = {
        "status": "factor_translations_supply_second_family_operator_but_kernel_and_mixing_remain_underived",
        "date": "2026-08-05",
        "canonical_operators": {
            "T_RP3": "(p,q)->(p+1,q)",
            "T_S1": "(p,q)->(p,q+1)",
            "shear": "(p,q)->(p,q+p)",
            "translations_commute": bool(
                np.allclose(
                    translate_rp3 @ translate_s1,
                    translate_s1 @ translate_rp3,
                )
            ),
            "restricted_T_RP3": restricted_rp3.tolist(),
            "restricted_T_S1": restricted_s1.tolist(),
            "restricted_shear": restricted_shear.tolist(),
            "joint_character_basis": ["chi_RP3", "chi_S1", "chi_RP3+S1"],
        },
        "geometric_group": {
            "generated_order": len(geometric_group),
            "triplet_commutant_dimension": commutant_dimension(restricted_group),
            "interpretation": (
                "Translations plus the geometric shear generate a D8-type order-eight "
                "action. Full invariance decomposes the triplet as 1+2 and therefore "
                "retains a light-family degeneracy."
            ),
        },
        "factor_laplacian": {
            "general_operator": (
                "L(w3,w1)=w3(I-T_RP3)+w1(I-T_S1)"
            ),
            "exact_triplet_eigenvalues": "{2w3,2w1,2(w3+w1)}",
            "factor_lengths_at_unit_radii": {
                "RP3_systole": length_rp3,
                "S1_circle": length_s1,
            },
            "kernel_tests": kernel_rows,
            "finding": (
                "The factorization supplies enough commuting operators to split all "
                "three family directions, but topology does not choose the map from "
                "cycle length to Yukawa weight."
            ),
        },
        "winding_candidate": {
            "rule": "mass_chi proportional to exp[-pi*p-2pi*q] for nonzero (p,q)",
            "normalized_pattern": additive_winding_pattern.tolist(),
            "interpretation": (
                "Independent additive winding actions produce a parameter-free hierarchy "
                "approximately (e^-2pi,e^-pi,1). It is a candidate kernel, not a derived "
                "Yukawa theorem."
            ),
        },
        "hierarchy_comparison": hierarchy_comparison,
        "mixing_gate": {
            "commuting_factor_algebra": True,
            "consequence": (
                "Every up/down Yukawa that is a function only of T_RP3 and T_S1 is "
                "diagonal in the same character basis, so CKM is exactly the identity."
            ),
            "SU5_parity_effect": (
                "Weak-doublet/singlet parity changes eigenvalues but not the common left "
                "family eigenbasis; it does not generate CKM mixing."
            ),
            "required_new_structure": (
                "A sector-dependent noncommuting shear coefficient or another transition "
                "operator derived from the action."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "A genuine second canonical operator exists: the two factor translations "
                "jointly resolve the three family directions without continuous angles."
            ),
            "negative": (
                "The physical kernel f(length) and the noncommuting source of CKM mixing "
                "are not fixed. Natural kernels do not reproduce all three observed "
                "hierarchies, especially the up sector."
            ),
            "status": (
                "three-family carrier plus parameter-free hierarchy candidate, not a "
                "flavor prediction"
            ),
            "next_gate": (
                "derive the tunneling kernel and a sector-dependent shear insertion from "
                "one menu-SU5 action before comparing another mass ratio"
            ),
        },
    }

    assert len(geometric_group) == 8
    assert commutant_dimension(restricted_group) == 2
    assert np.allclose(
        np.sort(np.diag(restricted_rp3)), [-1.0, -1.0, 1.0]
    )
    assert np.allclose(
        np.sort(np.diag(restricted_s1)), [-1.0, -1.0, 1.0]
    )
    assert np.allclose(
        additive_winding_pattern,
        [math.exp(-2.0 * math.pi), math.exp(-math.pi), 1.0],
    )

    Path("s2t_family_factor_operator_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "geometric_group_order": len(geometric_group),
                "commutant_dimension": commutant_dimension(restricted_group),
                "winding_pattern": additive_winding_pattern.tolist(),
                "lepton_log_RMS": hierarchy_comparison["charged_leptons"][
                    "candidates"
                ]["additive_winding_amplitudes"]["log_RMS"],
                "down_log_RMS": hierarchy_comparison[
                    "down_quarks_at_declared_scales"
                ]["candidates"]["additive_winding_amplitudes"]["log_RMS"],
                "up_log_RMS": hierarchy_comparison[
                    "up_quarks_at_declared_scales"
                ]["candidates"]["additive_winding_amplitudes"]["log_RMS"],
                "CKM": "identity_for_commuting_factor_algebra",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()