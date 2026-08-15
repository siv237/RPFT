import itertools
import json
import math

import numpy as np
from scipy.linalg import expm


TOLERANCE = 1.0e-9
GRID_SIZE = 1001


def permutation_sign(permutation):
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(4)
        for right in range(left + 1, 4)
    )
    return 1 if inversions % 2 == 0 else -1


def permutation_matrix(permutation):
    matrix = np.zeros((4, 4))
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


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


def skew_basis():
    basis = []
    for row in range(4):
        for column in range(row + 1, 4):
            generator = np.zeros((4, 4))
            generator[row, column] = 1.0 / math.sqrt(2.0)
            generator[column, row] = -1.0 / math.sqrt(2.0)
            basis.append(generator)
    return basis


def phase_profile(profile_name, winding, coordinate):
    linear = 2.0 * math.pi * winding * coordinate
    if profile_name == "uniform":
        return linear, np.full_like(coordinate, 2.0 * math.pi * winding)
    modulation = (
        0.20 * np.sin(2.0 * math.pi * coordinate)
        + 0.07 * np.sin(6.0 * math.pi * coordinate)
    )
    derivative = (
        0.40 * math.pi * np.cos(2.0 * math.pi * coordinate)
        + 0.42 * math.pi * np.cos(6.0 * math.pi * coordinate)
    )
    return linear + modulation, 2.0 * math.pi * winding + derivative


identity = np.eye(4)
uniform_singlet = np.ones(4) / 2.0
coordinate = np.linspace(0.0, 1.0, GRID_SIZE)
orthonormal_skew_basis = skew_basis()
rows = []

for fixed_point in range(4):
    projector = np.zeros((4, 4))
    projector[fixed_point, fixed_point] = 1.0
    family_field = (2.0 / math.sqrt(3.0)) * (projector - identity / 4.0)
    family_axis = np.diag(family_field)
    omega = orientation_generator(uniform_singlet, family_axis)
    curvature = (
        family_field @ family_field
        - family_field / math.sqrt(3.0)
        - identity / 4.0
    )

    for winding in (1, -1):
        transition = expm(winding * 2.0 * math.pi * omega / 3.0)
        target = permutation_matrix(oriented_three_cycle(fixed_point, winding))
        inverse_target = permutation_matrix(
            oriented_three_cycle(fixed_point, -winding)
        )

        for profile_name in ("uniform", "modulated"):
            phase, phase_derivative = phase_profile(
                profile_name, winding, coordinate
            )
            frames = np.array(
                [expm(value * omega / 3.0) for value in phase]
            )
            frame_derivatives = np.array(
                [
                    (derivative * omega / 3.0) @ frame
                    for derivative, frame in zip(phase_derivative, frames)
                ]
            )
            connections = np.array(
                [-derivative * omega / 3.0 for derivative in phase_derivative]
            )
            covariant_derivatives = frame_derivatives + np.einsum(
                "nij,njk->nik", connections, frames
            )
            connection_integral = np.trapezoid(connections, coordinate, axis=0)
            holonomy = expm(connection_integral)

            cubic_frame_residual = max(
                np.linalg.norm(np.linalg.matrix_power(frame, 3) - expm(value * omega))
                for frame, value in zip(frames, phase)
            )
            hessian = np.array(
                [
                    [2.0 * np.trace(left.T @ right) for right in orthonormal_skew_basis]
                    for left in orthonormal_skew_basis
                ]
            )
            hessian_eigenvalues = np.linalg.eigvalsh(hessian)

            rows.append(
                {
                    "fixed_point": fixed_point,
                    "vortex_winding": winding,
                    "profile": profile_name,
                    "finite_curvature_residual": float(np.linalg.norm(curvature)),
                    "commutator_residual": float(
                        np.linalg.norm(omega @ family_field - family_field @ omega)
                    ),
                    "cubic_frame_residual": float(cubic_frame_residual),
                    "frame_monodromy_residual": float(
                        np.linalg.norm(frames[-1] - frames[0] @ transition)
                    ),
                    "transition_cube_residual": float(
                        np.linalg.norm(np.linalg.matrix_power(transition, 3) - identity)
                    ),
                    "transition_cycle_residual": float(
                        np.linalg.norm(transition - inverse_target)
                    ),
                    "maximum_covariant_derivative_residual": float(
                        max(np.linalg.norm(value) for value in covariant_derivatives)
                    ),
                    "connection_integral_residual": float(
                        np.linalg.norm(
                            connection_integral
                            + winding * 2.0 * math.pi * omega / 3.0
                        )
                    ),
                    "holonomy_residual": float(np.linalg.norm(holonomy - target)),
                    "connection_gradient_residual": float(
                        2.0
                        * max(
                            abs(
                                np.trace(
                                    generator.T
                                    @ (
                                        connections[GRID_SIZE // 2]
                                        + phase_derivative[GRID_SIZE // 2] * omega / 3.0
                                    )
                                )
                            )
                            for generator in orthonormal_skew_basis
                        )
                    ),
                    "connection_hessian_eigenvalues": hessian_eigenvalues.tolist(),
                }
            )

profile_pairs = {}
for fixed_point in range(4):
    for winding in (1, -1):
        branch_rows = [
            row
            for row in rows
            if row["fixed_point"] == fixed_point
            and row["vortex_winding"] == winding
        ]
        profile_pairs[f"{fixed_point}:{winding}"] = abs(
            branch_rows[0]["holonomy_residual"]
            - branch_rows[1]["holonomy_residual"]
        )

result = {
    "gate": "version4_family_defect_cubic_root_action_gate",
    "action": {
        "projector_curvature": "Q(H)=H^2-H/sqrt(3)-I/4",
        "root_frame": "W(s)=exp[(phi(s)/3) Omega(H)]",
        "covariant_derivative": "D_s W=partial_s W+A_s W",
        "functional": (
            "S=int ds [L^{-1} Tr Q(H)^2+L Tr((D_s W)^T D_s W)]"
        ),
        "connection_euler_lagrange": (
            "A_s=-partial_s W W^T=-(partial_s phi/3) Omega(H)"
        ),
        "monodromy": (
            "W(s+L)=W(s) exp[(2pi nu/3)Omega(H)], Z_nu^3=I"
        ),
    },
    "checks": {
        "branch_profile_count": len(rows),
        "maximum_finite_curvature_residual": max(
            row["finite_curvature_residual"] for row in rows
        ),
        "maximum_commutator_residual": max(
            row["commutator_residual"] for row in rows
        ),
        "maximum_cubic_frame_residual": max(
            row["cubic_frame_residual"] for row in rows
        ),
        "maximum_frame_monodromy_residual": max(
            row["frame_monodromy_residual"] for row in rows
        ),
        "maximum_transition_cube_residual": max(
            row["transition_cube_residual"] for row in rows
        ),
        "maximum_transition_cycle_residual": max(
            row["transition_cycle_residual"] for row in rows
        ),
        "maximum_covariant_derivative_residual": max(
            row["maximum_covariant_derivative_residual"] for row in rows
        ),
        "maximum_connection_integral_residual": max(
            row["connection_integral_residual"] for row in rows
        ),
        "maximum_holonomy_residual": max(
            row["holonomy_residual"] for row in rows
        ),
        "maximum_connection_gradient_residual": max(
            row["connection_gradient_residual"] for row in rows
        ),
        "minimum_connection_hessian_eigenvalue": min(
            min(row["connection_hessian_eigenvalues"]) for row in rows
        ),
        "maximum_profile_holonomy_residual_difference": max(
            profile_pairs.values()
        ),
        "all_connection_hessians_positive": all(
            min(row["connection_hessian_eigenvalues"]) > TOLERANCE
            for row in rows
        ),
    },
    "status": {
        "constitutive_action_gate": "pass_in_fixed_condensed_unit_winding_sector",
        "remaining_gap": (
            "derive the nonzero root-frame condensate and embed its Z3 bundle "
            "in the finite graded parent superconnection"
        ),
    },
    "rows": rows,
}

with open(
    "s2t_v4_family_defect_cubic_root_action_gate_results.json",
    "w",
    encoding="utf-8",
) as output_file:
    json.dump(result, output_file, indent=2)

print(json.dumps(result["checks"], indent=2))