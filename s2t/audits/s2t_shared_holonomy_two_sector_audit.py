#!/usr/bin/env python3
import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np


POINTS = [(0, 0), (1, 0), (0, 1), (1, 1)]
POINT_INDEX = {point: index for index, point in enumerate(POINTS)}


def compose(first, second):
    return tuple(first[second[index]] for index in range(len(first)))


def generated_group(generators):
    identity = tuple(range(len(generators[0])))
    group = {identity}
    frontier = [identity]
    while frontier:
        element = frontier.pop()
        for generator in generators:
            for product in [compose(element, generator), compose(generator, element)]:
                if product not in group:
                    group.add(product)
                    frontier.append(product)
    return sorted(group)


def permutation_matrix(permutation):
    matrix = np.zeros((4, 4), dtype=float)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def affine_permutation(matrix, translation):
    permutation = []
    for point in POINTS:
        image = (
            int((matrix[0, 0] * point[0] + matrix[0, 1] * point[1] + translation[0]) % 2),
            int((matrix[1, 0] * point[0] + matrix[1, 1] * point[1] + translation[1]) % 2),
        )
        permutation.append(POINT_INDEX[image])
    return tuple(permutation)


def triplet_basis():
    uniform = np.ones(4) / 2.0
    projector = np.eye(4) - np.outer(uniform, uniform)
    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    return eigenvectors[:, eigenvalues > 0.5]


def restrict(matrix, basis):
    return basis.T @ matrix @ basis


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


def commutant_dimension(generators):
    dimension = generators[0].shape[0]
    equations = [
        np.kron(generator.T, np.eye(dimension))
        - np.kron(np.eye(dimension), generator)
        for generator in generators
    ]
    rank = np.linalg.matrix_rank(np.vstack(equations), tol=1e-10)
    return int(dimension * dimension - rank)


def cycle_type(permutation):
    seen = set()
    lengths = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return "+".join(map(str, sorted(lengths, reverse=True)))


def canonical_phase(value):
    phase = (np.angle(value) / (2.0 * math.pi)) % 1.0
    fractions = [0.0, 0.25, 1.0 / 3.0, 0.5, 2.0 / 3.0, 0.75]
    return min(fractions, key=lambda candidate: abs(candidate - phase))


def spectral_ratio(phase):
    if abs(phase) < 1e-12:
        return 1.0 / 45.0
    return (2.0 + math.cos(2.0 * math.pi * phase)) / (
        3.0 * math.sin(math.pi * phase) ** 4
    )


def main():
    identity2 = np.eye(2, dtype=int)
    shear2 = np.array([[1, 0], [1, 1]], dtype=int)
    translation_x = affine_permutation(identity2, (1, 0))
    translation_y = affine_permutation(identity2, (0, 1))
    shear = affine_permutation(shear2, (0, 0))
    current_group = generated_group([translation_x, translation_y, shear])
    full_group = sorted(itertools.permutations(range(4)))

    basis = triplet_basis()
    current_generators = [
        restrict(permutation_matrix(element), basis)
        for element in [translation_x, translation_y, shear]
    ]

    rows = []
    for permutation in full_group:
        restricted = restrict(permutation_matrix(permutation), basis)
        incidence = 0.5 * (restricted + restricted.T)
        family_generators = current_generators + [incidence]
        family_algebra_dimension = algebra_dimension(family_generators)
        family_commutant_dimension = commutant_dimension(family_generators)
        for sign in [1, -1]:
            eigenvalues = np.linalg.eigvals(sign * restricted)
            phases = sorted(canonical_phase(value) for value in eigenvalues)
            response_ratio = sum(spectral_ratio(phase) for phase in phases)
            rows.append(
                {
                    "permutation": list(permutation),
                    "cycle_type": cycle_type(permutation),
                    "inside_current_D8": permutation in current_group,
                    "central_sign": sign,
                    "triplet_phases": phases,
                    "tensor_response_over_pi4": response_ratio,
                    "relative_error_from_pi4": abs(response_ratio - 1.0),
                    "family_algebra_dimension": family_algebra_dimension,
                    "family_commutant_dimension": family_commutant_dimension,
                    "full_M3": family_algebra_dimension == 9,
                    "exact_pi4": abs(response_ratio - 1.0) < 1e-10,
                }
            )

    exact_tensor = [row for row in rows if row["exact_pi4"]]
    full_m3 = [row for row in rows if row["full_M3"]]
    joint = [row for row in rows if row["exact_pi4"] and row["full_M3"]]
    best_full_m3_error = min(row["relative_error_from_pi4"] for row in full_m3)
    best_full_m3 = [
        row
        for row in full_m3
        if abs(row["relative_error_from_pi4"] - best_full_m3_error) < 1e-12
    ]

    class_summary = []
    for cycle in sorted(set(row["cycle_type"] for row in rows)):
        for sign in [1, -1]:
            class_rows = [
                row
                for row in rows
                if row["cycle_type"] == cycle and row["central_sign"] == sign
            ]
            class_summary.append(
                {
                    "cycle_type": cycle,
                    "central_sign": sign,
                    "count": len(class_rows),
                    "triplet_phases": class_rows[0]["triplet_phases"],
                    "tensor_response_over_pi4": class_rows[0][
                        "tensor_response_over_pi4"
                    ],
                    "full_M3_count": sum(row["full_M3"] for row in class_rows),
                    "exact_pi4_count": sum(row["exact_pi4"] for row in class_rows),
                }
            )

    results = {
        "status": "simple_shared_S4_holonomy_fails_exact_two_sector_gate",
        "date": "2026-08-05",
        "model": {
            "family_carrier": "standard three-dimensional representation of S4 on the sum-zero subspace of four spin-menu states",
            "tensor_carrier": "the same triplet used as three self-dual tensor channels on S1",
            "boundary_rule": "eigenphases of plus or minus the shared holonomy set the S1 shifts",
            "tensor_readout": "sum over channels and the full integer tower of (n+a)^-4, divided by pi^4; periodic zero modes are omitted",
        },
        "scan": {
            "S4_elements": len(full_group),
            "signed_variants": len(rows),
            "current_D8_order": len(current_group),
            "full_M3_signed_variants": len(full_m3),
            "exact_pi4_signed_variants": len(exact_tensor),
            "joint_survivors": len(joint),
        },
        "class_summary": class_summary,
        "exact_tensor_rows": exact_tensor,
        "best_full_M3_rows": best_full_m3,
        "joint_rows": joint,
        "scientific_verdict": {
            "positive": (
                "A single signed S4 element fixes both a family incidence direction and a complete set of tensor boundary phases, so the proposed two-sector gate is parameter-free and exhaustive within this ansatz."
            ),
            "negative": (
                "The only exact pi^4 response is the central antiperiodic holonomy minus identity. Its family action is scalar and leaves the original reducible algebra unchanged. Every outside-D8 incidence that generates full M3 misses pi^4."
            ),
            "best_full_M3_mismatch": best_full_m3_error,
            "consequence": (
                "One common constant S4 holonomy cannot simultaneously explain the tensor Hessian and select a full family-mixing operator. Reopening requires a richer non-Abelian boundary connection, a path-dependent Wilson operator, or a derived relation between distinct representations rather than one shared group element."
            ),
        },
        "rows": rows,
    }

    Path("s2t_shared_holonomy_two_sector_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "signed_variants": len(rows),
                "full_M3_variants": len(full_m3),
                "exact_pi4_variants": len(exact_tensor),
                "joint_survivors": len(joint),
                "best_full_M3_relative_error": best_full_m3_error,
                "exact_tensor_classes": {
                    f"{cycle_type_value};sign={sign}": count
                    for (cycle_type_value, sign), count in Counter(
                        (row["cycle_type"], row["central_sign"])
                        for row in exact_tensor
                    ).items()
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()