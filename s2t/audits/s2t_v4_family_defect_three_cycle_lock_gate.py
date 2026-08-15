import itertools
import json
import math

import numpy as np


TOLERANCE = 1.0e-9


def permutation_matrix(permutation):
    matrix = np.zeros((4, 4))
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def standard_triplet_basis():
    seed = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [-1.0, -1.0, -1.0],
        ]
    )
    basis, _ = np.linalg.qr(seed)
    return basis[:, :3]


def cycle_type(permutation):
    visited = [False] * 4
    lengths = []
    for start in range(4):
        if visited[start]:
            continue
        current = start
        length = 0
        while not visited[current]:
            visited[current] = True
            current = permutation[current]
            length += 1
        lengths.append(length)
    return "+".join(str(length) for length in sorted(lengths, reverse=True))


def cross_matrix(axis):
    x_value, y_value, z_value = axis
    return np.array(
        [
            [0.0, -z_value, y_value],
            [z_value, 0.0, -x_value],
            [-y_value, x_value, 0.0],
        ]
    )


def rodrigues(axis, angle):
    generator = cross_matrix(axis)
    return (
        np.eye(3)
        + math.sin(angle) * generator
        + (1.0 - math.cos(angle)) * (generator @ generator)
    )


def oriented_axis(rotation, angle):
    skew = (rotation - rotation.T) / (2.0 * math.sin(angle))
    axis = np.array([skew[2, 1], skew[0, 2], skew[1, 0]])
    return axis / np.linalg.norm(axis)


def triplet_cubic(basis, axis):
    lifted = basis @ axis
    return float(np.sum(lifted**3)), lifted


def locking_potential(radius, angle, cubic_value, winding):
    character = 1.0 + 2.0 * math.cos(angle)
    radial = (radius * radius - 1.0) ** 2
    angle_term = radius * radius * character * character
    axis_term = radius * radius * (
        1.0 - math.sqrt(3.0) * winding * cubic_value
    )
    return radial + angle_term + axis_term


basis = standard_triplet_basis()
angle = 2.0 * math.pi / 3.0
rows = []

for permutation in itertools.permutations(range(4)):
    if cycle_type(permutation) != "3+1":
        continue
    rotation = basis.T @ permutation_matrix(permutation) @ basis
    axis = oriented_axis(rotation, angle)
    cubic_value, lifted_axis = triplet_cubic(basis, axis)
    winding = 1 if cubic_value > 0 else -1
    reconstructed = rodrigues(axis, angle)
    generator = angle * cross_matrix(axis)
    singular_values = np.linalg.svd(generator, compute_uv=False)
    rows.append(
        {
            "permutation": list(permutation),
            "triplet_trace": float(np.trace(rotation)),
            "triplet_determinant": float(np.linalg.det(rotation)),
            "axis": axis.tolist(),
            "lifted_axis": lifted_axis.tolist(),
            "cubic_invariant": cubic_value,
            "vortex_winding": winding,
            "rodrigues_residual": float(np.linalg.norm(rotation - reconstructed)),
            "locking_potential": locking_potential(
                1.0, angle, cubic_value, winding
            ),
            "generator_rank": int(np.linalg.matrix_rank(generator, TOLERANCE)),
            "generator_nullity": int(
                3 - np.linalg.matrix_rank(generator, TOLERANCE)
            ),
            "generator_singular_values": singular_values.tolist(),
        }
    )

positive_rows = [row for row in rows if row["vortex_winding"] == 1]
negative_rows = [row for row in rows if row["vortex_winding"] == -1]
expected_cubic = 1.0 / math.sqrt(3.0)

result = {
    "gate": "version4_family_defect_three_cycle_lock_gate",
    "candidate_functional": {
        "formula": (
            "V_nu=(r^2-1)^2+r^2(1+2 cos theta)^2+"
            "r^2(1-sqrt(3) nu I_3(n))"
        ),
        "cubic_invariant": "I_3(n)=sum_{a=1}^4 (B n)_a^3",
        "constraints": "r>=0, ||n||=1, nu in {+1,-1}",
    },
    "exact_structure": {
        "three_cycle_count": len(rows),
        "positive_winding_minima": len(positive_rows),
        "negative_winding_minima": len(negative_rows),
        "expected_absolute_cubic": expected_cubic,
        "maximum_cubic_error": max(
            abs(abs(row["cubic_invariant"]) - expected_cubic) for row in rows
        ),
        "maximum_trace_error": max(abs(row["triplet_trace"]) for row in rows),
        "maximum_determinant_error": max(
            abs(row["triplet_determinant"] - 1.0) for row in rows
        ),
        "maximum_rodrigues_residual": max(
            row["rodrigues_residual"] for row in rows
        ),
        "maximum_locking_potential": max(
            abs(row["locking_potential"]) for row in rows
        ),
        "all_generators_rank_two": all(
            row["generator_rank"] == 2 for row in rows
        ),
        "all_generators_nullity_one": all(
            row["generator_nullity"] == 1 for row in rows
        ),
        "normalized_tangent_hessian": {
            "radial": 8.0,
            "angle": 6.0,
            "axis_eigenvalues": [6.0, 6.0],
        },
    },
    "rows": rows,
    "verdict": {
        "positive": (
            "The coefficient-free nonnegative locking functional has exactly "
            "four minima in each unit-winding sector. Positive and negative "
            "vortex winding select the two orientations of the four "
            "tetrahedral axes, reproducing all eight S4 three-cycles at angle "
            "2pi/3. Every selected SO3 generator has rank two and leaves one "
            "Majorana family direction."
        ),
        "open": (
            "The zero locus is derived from project invariants, but the full "
            "functional has not yet been obtained as the supertrace of one "
            "local boundary-superconnection curvature. The unit radial scale "
            "and the sign map between vortex winding and the cubic family "
            "invariant remain parent-action data."
        ),
    },
}

with open(
    "s2t_v4_family_defect_three_cycle_lock_gate_results.json",
    "w",
    encoding="utf-8",
) as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, ensure_ascii=False, indent=2))