import itertools
import json
import math

import numpy as np
from scipy.linalg import expm


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


def commutator(left, right):
    return compose(compose(compose(left, right), inverse(left)), inverse(right))


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


def transform_rank_three(tensor, rotation):
    return np.einsum("ia,jb,kc,abc->ijk", rotation, rotation, rotation, tensor)


def quaternion_multiply(left, right):
    left_scalar, left_vector = left[0], np.array(left[1:])
    right_scalar, right_vector = right[0], np.array(right[1:])
    scalar = left_scalar * right_scalar - left_vector @ right_vector
    vector = (
        left_scalar * right_vector
        + right_scalar * left_vector
        + np.cross(left_vector, right_vector)
    )
    return np.concatenate(([scalar], vector))


def quaternion_power(quaternion, power):
    result = np.array([1.0, 0.0, 0.0, 0.0])
    for _ in range(power):
        result = quaternion_multiply(result, quaternion)
    return result


basis = standard_triplet_basis()
identity4 = np.eye(4)
identity3 = np.eye(3)
uniform_singlet = np.ones(4) / 2.0

axes = []
for fixed_point in range(4):
    projector = np.zeros((4, 4))
    projector[fixed_point, fixed_point] = 1.0
    family_field = (2.0 / math.sqrt(3.0)) * (projector - identity4 / 4.0)
    axes.append(basis.T @ np.diag(family_field))
axes = np.array(axes)

tetrahedral_tensor = sum(np.einsum("i,j,k->ijk", axis, axis, axis) for axis in axes)
trace_contraction = np.einsum("iik->k", tetrahedral_tensor)

permutations = list(itertools.permutations(range(4)))
even_permutations = [value for value in permutations if permutation_sign(value) == 1]
tetrahedral_rows = []
for permutation in permutations:
    permutation_representation = basis.T @ permutation_matrix(permutation) @ basis
    transformed_tensor = transform_rank_three(
        tetrahedral_tensor, permutation_representation
    )
    tetrahedral_rows.append(
        {
            "permutation": list(permutation),
            "sign": permutation_sign(permutation),
            "triplet_determinant": float(np.linalg.det(permutation_representation)),
            "orthogonality_residual": float(
                np.linalg.norm(
                    permutation_representation.T @ permutation_representation - identity3
                )
            ),
            "tetrahedral_tensor_residual": float(
                np.linalg.norm(transformed_tensor - tetrahedral_tensor)
            ),
        }
    )

commutator_subgroup = {
    commutator(left, right)
    for left in even_permutations
    for right in even_permutations
}

branch_rows = []
for fixed_point, axis in enumerate(axes):
    stabilizer = [
        permutation
        for permutation in even_permutations
        if permutation[fixed_point] == fixed_point
    ]
    expected_cycles = {
        tuple(range(4)),
        oriented_three_cycle(fixed_point, 1),
        oriented_three_cycle(fixed_point, -1),
    }
    stabilizer_rotations = [
        basis.T @ permutation_matrix(permutation) @ basis
        for permutation in stabilizer
    ]

    for winding in (1, -1):
        cycle = oriented_three_cycle(fixed_point, winding)
        rotation = basis.T @ permutation_matrix(cycle) @ basis
        quaternion = np.concatenate(
            (
                [math.cos(math.pi / 3.0)],
                winding * math.sin(math.pi / 3.0) * axis,
            )
        )
        branch_rows.append(
            {
                "fixed_point": fixed_point,
                "winding": winding,
                "cycle": list(cycle),
                "axis": axis.tolist(),
                "stabilizer_order": len(stabilizer),
                "stabilizer_is_expected_z3": set(stabilizer) == expected_cycles,
                "maximum_axis_stabilizer_residual": float(
                    max(
                        np.linalg.norm(stabilizer_rotation @ axis - axis)
                        for stabilizer_rotation in stabilizer_rotations
                    )
                ),
                "cycle_order_three_residual": float(
                    np.linalg.norm(np.linalg.matrix_power(rotation, 3) - identity3)
                ),
                "cycle_nontrivial_residual": float(np.linalg.norm(rotation - identity3)),
                "su2_lift_cube_residual": float(
                    np.linalg.norm(
                        quaternion_power(quaternion, 3)
                        - np.array([-1.0, 0.0, 0.0, 0.0])
                    )
                ),
                "su2_lift_sixth_residual": float(
                    np.linalg.norm(
                        quaternion_power(quaternion, 6)
                        - np.array([1.0, 0.0, 0.0, 0.0])
                    )
                ),
                "exponential_rotation_residual": float(
                    np.linalg.norm(
                        expm(
                            winding
                            * 2.0
                            * math.pi
                            / 3.0
                            * np.array(
                                [
                                    [0.0, -axis[2], axis[1]],
                                    [axis[2], 0.0, -axis[0]],
                                    [-axis[1], axis[0], 0.0],
                                ]
                            )
                        )
                        - rotation
                    )
                ),
            }
        )

result = {
    "gate": "version4_family_defect_tetrahedral_residual_bundle_gate",
    "construction": {
        "tetrahedral_axes": "n_a=B^T diag[(2/sqrt(3))(P_a-I/4)]",
        "spin_three_tensor": "T_ijk=sum_a n_ai n_aj n_ak",
        "continuous_breaking": "SO(3)_F -> Stab(T)=A4",
        "projector_breaking": "A4 -> Stab(P_a)=Z3",
        "binary_lift": "pi1(SO(3)/Z3)=preimage(Z3 in SU2)=Z6",
    },
    "checks": {
        "axis_count": len(axes),
        "axis_norm_residual": float(
            max(abs(axis @ axis - 1.0) for axis in axes)
        ),
        "axis_sum_residual": float(np.linalg.norm(np.sum(axes, axis=0))),
        "tetrahedral_tensor_trace_residual": float(np.linalg.norm(trace_contraction)),
        "tetrahedral_rotation_stabilizer_order": sum(
            row["sign"] == 1
            and row["tetrahedral_tensor_residual"] < TOLERANCE
            for row in tetrahedral_rows
        ),
        "maximum_even_tensor_residual": max(
            row["tetrahedral_tensor_residual"]
            for row in tetrahedral_rows
            if row["sign"] == 1
        ),
        "maximum_triplet_orthogonality_residual": max(
            row["orthogonality_residual"] for row in tetrahedral_rows
        ),
        "a4_order": len(even_permutations),
        "a4_commutator_subgroup_order": len(commutator_subgroup),
        "a4_abelianization_order": len(even_permutations) // len(commutator_subgroup),
        "all_projector_stabilizers_z3": all(
            row["stabilizer_order"] == 3 and row["stabilizer_is_expected_z3"]
            for row in branch_rows
        ),
        "maximum_axis_stabilizer_residual": max(
            row["maximum_axis_stabilizer_residual"] for row in branch_rows
        ),
        "maximum_cycle_order_three_residual": max(
            row["cycle_order_three_residual"] for row in branch_rows
        ),
        "maximum_su2_lift_cube_residual": max(
            row["su2_lift_cube_residual"] for row in branch_rows
        ),
        "maximum_su2_lift_sixth_residual": max(
            row["su2_lift_sixth_residual"] for row in branch_rows
        ),
        "maximum_exponential_rotation_residual": max(
            row["exponential_rotation_residual"] for row in branch_rows
        ),
        "charge_two_abelian_higgs_residual_group_order": 2,
        "charge_three_abelian_higgs_residual_group_order": 3,
    },
    "status": {
        "z3_denominator_origin": "pass_as_projector_stabilizer_inside_A4",
        "binary_tetrahedral_consistency": (
            "the SU2 lift of every order-three SO3 holonomy has order six, "
            "and A4 abelianization has order three"
        ),
        "gauge_global_fork": {
            "global_A4": "retains physical axes but does not produce a gauge bundle",
            "gauged_A4": (
                "produces residual Z3 flux, but the four projector axes are gauge-related "
                "unless boundary framing or additional matter makes them observable"
            ),
        },
        "remaining_gap": (
            "derive a gauged or boundary-framed tetrahedral carrier and the nonzero "
            "ordinary charge-two defect condensate from one finite graded parent action"
        ),
    },
    "tetrahedral_rows": tetrahedral_rows,
    "branch_rows": branch_rows,
}

with open(
    "s2t_v4_family_defect_tetrahedral_residual_bundle_gate_results.json",
    "w",
    encoding="utf-8",
) as output_file:
    json.dump(result, output_file, indent=2)

print(json.dumps(result["checks"], indent=2))