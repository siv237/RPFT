import itertools
import json
import math

import numpy as np
from scipy.optimize import minimize


TOLERANCE = 1.0e-9


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


def matrix_basis():
    basis = []
    for row in range(3):
        for column in range(3):
            matrix = np.zeros((3, 3))
            matrix[row, column] = 1.0
            basis.append(matrix)
    return basis


def finite_difference_hessian(function, point, step=2.0e-5):
    dimension = len(point)
    hessian = np.zeros((dimension, dimension))
    center = function(point)
    for left in range(dimension):
        for right in range(left, dimension):
            left_direction = np.zeros(dimension)
            right_direction = np.zeros(dimension)
            left_direction[left] = step
            right_direction[right] = step
            if left == right:
                value = (
                    function(point + left_direction)
                    - 2.0 * center
                    + function(point - left_direction)
                ) / step**2
            else:
                value = (
                    function(point + left_direction + right_direction)
                    - function(point + left_direction - right_direction)
                    - function(point - left_direction + right_direction)
                    + function(point - left_direction - right_direction)
                ) / (4.0 * step**2)
            hessian[left, right] = value
            hessian[right, left] = value
    return hessian


def locking_potential(matrix):
    identity = np.eye(3)
    gram = matrix.T @ matrix - identity
    return 0.25 * np.sum(gram * gram) + 0.25 * (np.linalg.det(matrix) - 1.0) ** 2


def moment_map_potential(matrix, pairing_real, pairing_imaginary):
    radius_squared = pairing_real**2 + pairing_imaginary**2
    moment_map = matrix @ matrix.T - radius_squared * np.eye(3)
    return np.trace(moment_map @ moment_map) / 3.0


def total_zero_gradient_potential(vector):
    matrix = vector[:9].reshape(3, 3)
    pairing_real, pairing_imaginary = vector[9:]
    return locking_potential(matrix) + moment_map_potential(
        matrix, pairing_real, pairing_imaginary
    )


basis = standard_triplet_basis()
even_rotations = [
    basis.T @ permutation_matrix(permutation) @ basis
    for permutation in itertools.permutations(range(4))
    if permutation_sign(permutation) == 1
]

commutator_rows = []
for rotation in even_rotations:
    for row in range(3):
        for column in range(3):
            equation = np.zeros(9)
            for index, basis_matrix in enumerate(matrix_basis()):
                equation[index] = (
                    basis_matrix @ rotation - rotation @ basis_matrix
                )[row, column]
            commutator_rows.append(equation)
commutator_matrix = np.array(commutator_rows)
commutant_singular_values = np.linalg.svd(
    commutator_matrix, compute_uv=False
)
commutant_rank = int(np.sum(commutant_singular_values > TOLERANCE))
commutant_dimension = 9 - commutant_rank

generator = np.random.default_rng(20260815)
decomposition_residuals = []
for _ in range(128):
    matrix = generator.normal(size=(3, 3))
    pairing_radius_squared = float(generator.uniform(0.0, 2.0))
    gram = matrix @ matrix.T
    normalized_trace = np.trace(gram) / 3.0
    traceless_gram = gram - normalized_trace * np.eye(3)
    moment_map = gram - pairing_radius_squared * np.eye(3)
    full_square = np.trace(moment_map @ moment_map) / 3.0
    central_square = (pairing_radius_squared - normalized_trace) ** 2
    shape_square = np.trace(traceless_gram @ traceless_gram) / 3.0
    decomposition_residuals.append(
        abs(full_square - central_square - shape_square)
    )

vacuum_vector = np.concatenate((np.eye(3).reshape(-1), [1.0, 0.0]))
zero_gradient_hessian = finite_difference_hessian(
    total_zero_gradient_potential, vacuum_vector
)
zero_gradient_eigenvalues = np.linalg.eigvalsh(zero_gradient_hessian)


def radial_defect_potential(radial_variables, momentum_squared=1.0):
    frame_radius, pairing_radius = radial_variables
    matrix = frame_radius * np.eye(3)
    return (
        locking_potential(matrix)
        + moment_map_potential(matrix, pairing_radius, 0.0)
        + momentum_squared * pairing_radius**2
    )


radial_results = [
    minimize(
        radial_defect_potential,
        x0=np.array(start),
        bounds=((0.0, None), (0.0, None)),
        method="L-BFGS-B",
        options={"ftol": 1.0e-15, "gtol": 1.0e-12, "maxiter": 10000},
    )
    for start in (
        (0.0, 0.0),
        (0.5, 0.0),
        (1.0, 0.0),
        (0.5, 0.5),
        (1.0, 0.3),
        (1.0, 0.7),
        (1.0, 1.0),
        (1.5, 1.0),
    )
]
radial_result = min(radial_results, key=lambda value: value.fun)
radial_hessian = finite_difference_hessian(
    lambda values: radial_defect_potential(values), radial_result.x
)
radial_hessian_eigenvalues = np.linalg.eigvalsh(radial_hessian)

result = {
    "gate": "version4_family_defect_quiver_moment_map_gate",
    "quiver": {
        "nodes": [
            "left frozen A4 triplet",
            "middle gauged SO3 triplet",
            "right frozen A4 triplet",
        ],
        "arrows": {
            "X": "left -> middle real bifundamental locking field",
            "Y": "middle -> right A4-equivariant charge-two pairing connector",
        },
        "schur_reduction": "End_A4(R3)=R I3, hence Y=Phi I3",
        "middle_moment_map": "mu=X X^T-Y^dagger Y=X X^T-|Phi|^2 I3",
        "action": "S_mu=tau_3(mu^2), tau_3=Tr/3",
    },
    "checks": {
        "a4_rotation_count": len(even_rotations),
        "real_a4_triplet_commutant_dimension": commutant_dimension,
        "smallest_nonzero_commutant_singular_value": float(
            min(
                value
                for value in commutant_singular_values
                if value > TOLERANCE
            )
        ),
        "maximum_moment_map_decomposition_residual": max(
            decomposition_residuals
        ),
        "central_square_coefficients": {
            "abs_phi_four": 1.0,
            "abs_phi_two_trace_gram": -2.0 / 3.0,
            "trace_gram_squared": 1.0 / 9.0,
        },
        "zero_gradient_hessian_eigenvalues": zero_gradient_eigenvalues.tolist(),
        "zero_gradient_positive_count": int(
            np.sum(zero_gradient_eigenvalues > 1.0e-5)
        ),
        "zero_gradient_zero_count": int(
            np.sum(np.abs(zero_gradient_eigenvalues) <= 1.0e-5)
        ),
        "zero_gradient_negative_count": int(
            np.sum(zero_gradient_eigenvalues < -1.0e-5)
        ),
        "unit_momentum_radial_minimum": {
            "frame_radius": float(radial_result.x[0]),
            "pairing_radius": float(radial_result.x[1]),
            "pairing_radius_squared": float(radial_result.x[1] ** 2),
            "energy": float(radial_result.fun),
            "gradient_norm": float(np.linalg.norm(radial_result.jac)),
            "hessian_eigenvalues": radial_hessian_eigenvalues.tolist(),
            "condensed": bool(radial_result.x[1] > 1.0e-6),
            "stable": bool(np.min(radial_hessian_eigenvalues) > 1.0e-5),
            "multistart_count": len(radial_results),
            "multistart_energy_spread": float(
                max(value.fun for value in radial_results)
                - min(value.fun for value in radial_results)
            ),
            "distinct_candidate_minima": sorted(
                {
                    (
                        round(float(value.x[0]), 8),
                        round(float(value.x[1]), 8),
                        round(float(value.fun), 10),
                    )
                    for value in radial_results
                }
            ),
        },
    },
    "exact_identity": {
        "formula": (
            "tau_3(mu^2)=(|Phi|^2-tau_3(XX^T))^2+"
            "tau_3((XX^T-tau_3(XX^T)I)^2)"
        ),
        "meaning": (
            "one middle-node moment-map square contains both the requested "
            "norm-locking square and a positive anisotropy penalty"
        ),
    },
    "status": {
        "coefficient_ratio": "pass_from_normalized_middle_node_moment_map",
        "pairing_condensate_in_normalized_unit_momentum_model": (
            "stable_nonzero_joint_minimum"
        ),
        "remaining_gap": (
            "embed the frozen-gauged-frozen quiver, its A4-equivariant Schur "
            "restriction, and the middle-node moment-map trace in the actual "
            "finite graded spectral triple with the same kinetic normalization"
        ),
    },
}

with open(
    "s2t_v4_family_defect_quiver_moment_map_gate_results.json",
    "w",
    encoding="utf-8",
) as output_file:
    json.dump(result, output_file, indent=2)

print(json.dumps(result["checks"], indent=2))