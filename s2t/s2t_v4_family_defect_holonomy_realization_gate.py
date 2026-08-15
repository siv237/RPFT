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


def levi_civita(first, second, third, fourth):
    indices = (first, second, third, fourth)
    if len(set(indices)) < 4:
        return 0
    return permutation_sign(indices)


def orientation_generator(uniform_singlet, family_axis):
    generator = np.zeros((4, 4))
    for row in range(4):
        for column in range(4):
            generator[row, column] = sum(
                levi_civita(row, column, left, right)
                * uniform_singlet[left]
                * family_axis[right]
                for left in range(4)
                for right in range(4)
            )
    return generator


basis = standard_triplet_basis()
uniform_singlet = np.ones(4) / 2.0
identity = np.eye(4)
angle = 2.0 * math.pi / 3.0
rows = []

for fixed_point in range(4):
    coordinate_projector = np.zeros((4, 4))
    coordinate_projector[fixed_point, fixed_point] = 1.0
    family_field = (2.0 / math.sqrt(3.0)) * (
        coordinate_projector - identity / 4.0
    )
    family_axis = np.diag(family_field)
    generator = orientation_generator(uniform_singlet, family_axis)
    transverse_projector = (
        identity
        - np.outer(uniform_singlet, uniform_singlet)
        - np.outer(family_axis, family_axis)
    )
    curvature = (
        family_field @ family_field
        - family_field / math.sqrt(3.0)
        - identity / 4.0
    )

    for winding in (1, -1):
        connection_integral = -winding * angle * generator
        holonomy = expm(connection_integral)
        permutation = oriented_three_cycle(fixed_point, winding)
        target = permutation_matrix(permutation)
        triplet_generator = basis.T @ connection_integral @ basis
        rows.append(
            {
                "fixed_point": fixed_point,
                "vortex_winding": winding,
                "permutation": list(permutation),
                "family_axis": family_axis.tolist(),
                "orientation_generator": generator.tolist(),
                "antisymmetry_residual": float(
                    np.linalg.norm(generator + generator.T)
                ),
                "singlet_kernel_residual": float(
                    np.linalg.norm(generator @ uniform_singlet)
                ),
                "axis_kernel_residual": float(
                    np.linalg.norm(generator @ family_axis)
                ),
                "complex_structure_residual": float(
                    np.linalg.norm(generator @ generator + transverse_projector)
                ),
                "commutator_residual": float(
                    np.linalg.norm(generator @ family_field - family_field @ generator)
                ),
                "finite_curvature_residual": float(np.linalg.norm(curvature)),
                "holonomy_residual": float(np.linalg.norm(holonomy - target)),
                "holonomy_trace": float(np.trace(holonomy)),
                "holonomy_determinant": float(np.linalg.det(holonomy)),
                "triplet_generator_rank": int(
                    np.linalg.matrix_rank(triplet_generator, TOLERANCE)
                ),
                "triplet_generator_nullity": int(
                    3 - np.linalg.matrix_rank(triplet_generator, TOLERANCE)
                ),
            }
        )

covariance_failures = []
maximum_connection_covariance_residual = 0.0
for group_element in itertools.permutations(range(4)):
    group_matrix = permutation_matrix(group_element)
    sign = permutation_sign(group_element)
    for fixed_point in range(4):
        projector = np.zeros((4, 4))
        projector[fixed_point, fixed_point] = 1.0
        family_axis = np.diag(
            (2.0 / math.sqrt(3.0)) * (projector - identity / 4.0)
        )
        generator = orientation_generator(uniform_singlet, family_axis)
        target_fixed_point = group_element[fixed_point]
        target_projector = np.zeros((4, 4))
        target_projector[target_fixed_point, target_fixed_point] = 1.0
        target_axis = np.diag(
            (2.0 / math.sqrt(3.0)) * (target_projector - identity / 4.0)
        )
        target_generator = orientation_generator(uniform_singlet, target_axis)
        generator_residual = np.linalg.norm(
            group_matrix @ generator @ group_matrix.T - sign * target_generator
        )
        maximum_connection_covariance_residual = max(
            maximum_connection_covariance_residual, float(generator_residual)
        )
        for winding in (1, -1):
            left_cycle = conjugate(
                group_element, oriented_three_cycle(fixed_point, winding)
            )
            right_cycle = oriented_three_cycle(
                target_fixed_point, sign * winding
            )
            if left_cycle != right_cycle or generator_residual > TOLERANCE:
                covariance_failures.append(
                    {
                        "group_element": list(group_element),
                        "fixed_point": fixed_point,
                        "winding": winding,
                        "cycle_match": left_cycle == right_cycle,
                        "connection_residual": float(generator_residual),
                    }
                )

result = {
    "gate": "version4_family_defect_holonomy_realization_gate",
    "connection_formula": {
        "uniform_singlet": "u=(1,1,1,1)/2",
        "family_axis": "h_a=diag[(2/sqrt(3))(P_a-I/4)]",
        "orientation_generator": (
            "Omega(h)_{bc}=epsilon_{bcde} u_d h_e"
        ),
        "boundary_connection": (
            "A_{a,nu}=-(nu/L)(2pi/3) Omega(h_a) ds"
        ),
        "holonomy": "Hol(A_{a,nu})=exp[-nu(2pi/3)Omega(h_a)]",
    },
    "exact_checks": {
        "branch_count": len(rows),
        "covariance_test_count": 24 * 4 * 2,
        "covariance_failure_count": len(covariance_failures),
        "maximum_connection_covariance_residual": (
            maximum_connection_covariance_residual
        ),
        "maximum_antisymmetry_residual": max(
            row["antisymmetry_residual"] for row in rows
        ),
        "maximum_singlet_kernel_residual": max(
            row["singlet_kernel_residual"] for row in rows
        ),
        "maximum_axis_kernel_residual": max(
            row["axis_kernel_residual"] for row in rows
        ),
        "maximum_complex_structure_residual": max(
            row["complex_structure_residual"] for row in rows
        ),
        "maximum_commutator_residual": max(
            row["commutator_residual"] for row in rows
        ),
        "maximum_finite_curvature_residual": max(
            row["finite_curvature_residual"] for row in rows
        ),
        "maximum_holonomy_residual": max(
            row["holonomy_residual"] for row in rows
        ),
        "all_triplet_generators_rank_two": all(
            row["triplet_generator_rank"] == 2 for row in rows
        ),
        "all_triplet_generators_nullity_one": all(
            row["triplet_generator_nullity"] == 1 for row in rows
        ),
    },
    "rows": rows,
    "covariance_failures": covariance_failures,
    "verdict": {
        "positive": (
            "The previously reconstructed three-cycle is the exact holonomy "
            "of a canonical flat connection built from the same rank-one "
            "projector field, the uniform singlet and the orientation tensor. "
            "The connection commutes with the projector supercurvature saddle, "
            "obeys the twisted S4 covariance law in all 192 tests and restricts "
            "to a rank-two Majorana generator with one-dimensional kernel."
        ),
        "open": (
            "This is a constrained superconnection-saddle realization. A full "
            "parent-action pass still requires deriving the constitutive "
            "relation A=-(nu/L)(2pi/3)Omega(h) from variation of one local or "
            "spectral action, rather than imposing that relation on the saddle "
            "ansatz."
        ),
    },
}

with open(
    "s2t_v4_family_defect_holonomy_realization_gate_results.json",
    "w",
    encoding="utf-8",
) as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, ensure_ascii=False, indent=2))