import itertools
import json
import math

import numpy as np


TOLERANCE = 1.0e-9


def permutation_sign(permutation):
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(4)
        for right in range(left + 1, 4)
    )
    return 1 if inversions % 2 == 0 else -1


def compose(left, right):
    return tuple(left[right[index]] for index in range(4))


def inverse(permutation):
    result = [0] * 4
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def conjugate(group_element, permutation):
    return compose(compose(group_element, permutation), inverse(group_element))


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


def oriented_complement(fixed_point):
    complement = [index for index in range(4) if index != fixed_point]
    for candidate in itertools.permutations(complement):
        if permutation_sign((fixed_point,) + candidate) == 1:
            return candidate
    raise RuntimeError("oriented complement not found")


def oriented_three_cycle(fixed_point, winding):
    first, second, third = oriented_complement(fixed_point)
    permutation = list(range(4))
    if winding == 1:
        permutation[first] = third
        permutation[third] = second
        permutation[second] = first
    else:
        permutation[first] = second
        permutation[second] = third
        permutation[third] = first
    return tuple(permutation)


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
        + (1.0 - math.cos(angle)) * generator @ generator
    )


basis = standard_triplet_basis()
identity = np.eye(4)
angle = 2.0 * math.pi / 3.0
rows = []

for fixed_point in range(4):
    projector = np.zeros((4, 4))
    projector[fixed_point, fixed_point] = 1.0
    family_field = (2.0 / math.sqrt(3.0)) * (projector - identity / 4.0)
    family_vector = np.diag(family_field)
    axis = basis.T @ family_vector
    shifted_involution = math.sqrt(3.0) * family_field - identity / 2.0
    curvature = (
        family_field @ family_field
        - family_field / math.sqrt(3.0)
        - identity / 4.0
    )
    reconstructed_projector = (identity + shifted_involution) / 2.0

    for winding in (1, -1):
        permutation = oriented_three_cycle(fixed_point, winding)
        rotation = basis.T @ permutation_matrix(permutation) @ basis
        reconstructed_rotation = rodrigues(axis, winding * angle)
        generator = winding * angle * cross_matrix(axis)
        rows.append(
            {
                "fixed_point": fixed_point,
                "vortex_winding": winding,
                "permutation": list(permutation),
                "family_vector": family_vector.tolist(),
                "triplet_axis": axis.tolist(),
                "cubic_invariant": float(np.sum(family_vector**3)),
                "family_norm_squared": float(family_vector @ family_vector),
                "curvature_residual": float(np.linalg.norm(curvature)),
                "involution_residual": float(
                    np.linalg.norm(shifted_involution @ shifted_involution - identity)
                ),
                "projector_residual": float(
                    np.linalg.norm(reconstructed_projector - projector)
                ),
                "projector_rank": int(
                    np.linalg.matrix_rank(reconstructed_projector, TOLERANCE)
                ),
                "rotation_trace": float(np.trace(rotation)),
                "rotation_determinant": float(np.linalg.det(rotation)),
                "rotation_residual": float(
                    np.linalg.norm(rotation - reconstructed_rotation)
                ),
                "generator_rank": int(np.linalg.matrix_rank(generator, TOLERANCE)),
                "generator_nullity": int(
                    3 - np.linalg.matrix_rank(generator, TOLERANCE)
                ),
            }
        )

covariance_failures = []
for group_element in itertools.permutations(range(4)):
    sign = permutation_sign(group_element)
    for fixed_point in range(4):
        for winding in (1, -1):
            left = conjugate(
                group_element, oriented_three_cycle(fixed_point, winding)
            )
            right = oriented_three_cycle(
                group_element[fixed_point], sign * winding
            )
            if left != right:
                covariance_failures.append(
                    {
                        "group_element": list(group_element),
                        "fixed_point": fixed_point,
                        "winding": winding,
                        "left": list(left),
                        "right": list(right),
                    }
                )

result = {
    "gate": "version4_family_defect_projector_supercurvature_gate",
    "supercurvature_factorization": {
        "family_field": "H_a=(2/sqrt(3))(P_a-I/4)",
        "curvature": "Q(H)=H^2-H/sqrt(3)-I/4",
        "shifted_square": "Q(H)=(H-I/(2sqrt(3)))^2-I/3",
        "involution": "J=sqrt(3)H-I/2, J^2=I, Tr J=-2",
        "projector_reconstruction": "P=(I+J)/2",
        "native_hessian_eigenvalues": [8.0 / 3.0] * 3,
    },
    "three_cycle_reconstruction": {
        "formula": "C_{a,nu}=rotation about axis H_a by nu*2pi/3",
        "candidate_count": len(rows),
        "covariance_rule": (
            "g C_{a,nu} g^{-1}=C_{g(a),sgn(g)nu}"
        ),
        "covariance_test_count": 24 * 4 * 2,
        "covariance_failure_count": len(covariance_failures),
        "maximum_curvature_residual": max(
            row["curvature_residual"] for row in rows
        ),
        "maximum_involution_residual": max(
            row["involution_residual"] for row in rows
        ),
        "maximum_projector_residual": max(
            row["projector_residual"] for row in rows
        ),
        "maximum_rotation_residual": max(
            row["rotation_residual"] for row in rows
        ),
        "all_projectors_rank_one": all(
            row["projector_rank"] == 1 for row in rows
        ),
        "all_rotations_trace_zero": all(
            abs(row["rotation_trace"]) < TOLERANCE for row in rows
        ),
        "all_rotations_determinant_one": all(
            abs(row["rotation_determinant"] - 1.0) < TOLERANCE for row in rows
        ),
        "all_generators_rank_two": all(
            row["generator_rank"] == 2 for row in rows
        ),
        "all_generators_nullity_one": all(
            row["generator_nullity"] == 1 for row in rows
        ),
    },
    "rows": rows,
    "covariance_failures": covariance_failures,
    "verdict": {
        "positive": (
            "The radial and tetrahedral-axis conditions factor into one "
            "shifted-square curvature equation. Its four solutions are "
            "canonically equivalent to rank-one projectors on the four-state "
            "menu. Vortex winding supplies the orientation line and turns each "
            "projector into one of two inverse three-cycles. The resulting "
            "eight holonomies satisfy the full twisted S4 covariance rule and "
            "all leave one Majorana family direction."
        ),
        "open": (
            "The finite curvature equation is now explicit, but the project "
            "still needs one graded boundary superconnection whose curvature "
            "contains Q(H), identifies the physical vortex winding with the "
            "orientation line, and induces the reconstructed three-cycle as an "
            "actual connection holonomy rather than a post-processing map."
        ),
    },
}

with open(
    "s2t_v4_family_defect_projector_supercurvature_gate_results.json",
    "w",
    encoding="utf-8",
) as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, ensure_ascii=False, indent=2))