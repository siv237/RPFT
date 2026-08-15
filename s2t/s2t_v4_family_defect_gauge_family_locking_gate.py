import json
import math

import numpy as np
from scipy.linalg import expm


TOLERANCE = 1.0e-9


def matrix_basis():
    basis = []
    labels = []
    for row in range(3):
        matrix = np.zeros((3, 3))
        matrix[row, row] = 1.0
        basis.append(matrix)
        labels.append(f"diag_{row}")
    for row in range(3):
        for column in range(row + 1, 3):
            symmetric = np.zeros((3, 3))
            symmetric[row, column] = 1.0 / math.sqrt(2.0)
            symmetric[column, row] = 1.0 / math.sqrt(2.0)
            basis.append(symmetric)
            labels.append(f"sym_{row}{column}")
    for row in range(3):
        for column in range(row + 1, 3):
            antisymmetric = np.zeros((3, 3))
            antisymmetric[row, column] = 1.0 / math.sqrt(2.0)
            antisymmetric[column, row] = -1.0 / math.sqrt(2.0)
            basis.append(antisymmetric)
            labels.append(f"skew_{row}{column}")
    return basis, labels


def skew_basis():
    return matrix_basis()[0][-3:]


def random_so3(generator):
    coefficients = generator.normal(size=3)
    algebra_element = sum(
        coefficient * basis_element
        for coefficient, basis_element in zip(coefficients, skew_basis())
    )
    return expm(algebra_element)


def locking_potential(matrix):
    identity = np.eye(3)
    gram = matrix.T @ matrix - identity
    return 0.25 * np.sum(gram * gram) + 0.25 * (np.linalg.det(matrix) - 1.0) ** 2


def finite_difference_hessian(function, point, directions, step=2.0e-5):
    dimension = len(directions)
    hessian = np.zeros((dimension, dimension))
    center = function(point)
    for left in range(dimension):
        for right in range(left, dimension):
            if left == right:
                plus = function(point + step * directions[left])
                minus = function(point - step * directions[left])
                value = (plus - 2.0 * center + minus) / step**2
            else:
                plus_plus = function(
                    point + step * directions[left] + step * directions[right]
                )
                plus_minus = function(
                    point + step * directions[left] - step * directions[right]
                )
                minus_plus = function(
                    point - step * directions[left] + step * directions[right]
                )
                minus_minus = function(
                    point - step * directions[left] - step * directions[right]
                )
                value = (
                    plus_plus - plus_minus - minus_plus + minus_minus
                ) / (4.0 * step**2)
            hessian[left, right] = value
            hessian[right, left] = value
    return hessian


def pairing_minimum(mass_squared, quartic, cross_coupling, trace_gram=3.0):
    effective_mass = mass_squared + cross_coupling * trace_gram
    radius_squared = max(0.0, -effective_mass / quartic)
    return effective_mass, radius_squared


identity = np.eye(3)
directions, direction_labels = matrix_basis()
hessian = finite_difference_hessian(locking_potential, identity, directions)
hessian_eigenvalues = np.linalg.eigvalsh(hessian)

gauge_mass_matrix = np.array(
    [
        [2.0 * np.trace(left.T @ right) for right in skew_basis()]
        for left in skew_basis()
    ]
)
gauge_mass_eigenvalues = np.linalg.eigvalsh(gauge_mass_matrix)

generator = np.random.default_rng(20260815)
invariance_residuals = []
for _ in range(64):
    left_rotation = random_so3(generator)
    right_rotation = random_so3(generator)
    perturbation = generator.normal(size=(3, 3))
    matrix = identity + 0.15 * perturbation
    transformed = left_rotation @ matrix @ right_rotation.T
    invariance_residuals.append(
        abs(locking_potential(transformed) - locking_potential(matrix))
    )

pairing_examples = []
for name, mass_squared, quartic, cross_coupling in (
    ("uncondensed", 1.0, 1.0, 0.0),
    ("condensed", 1.0, 1.0, -1.0),
):
    effective_mass, radius_squared = pairing_minimum(
        mass_squared, quartic, cross_coupling
    )
    pairing_examples.append(
        {
            "name": name,
            "mass_squared": mass_squared,
            "quartic": quartic,
            "cross_coupling": cross_coupling,
            "effective_mass_at_locked_vacuum": effective_mass,
            "pairing_radius_squared": radius_squared,
        }
    )

special_square_coefficients = {
    "pairing_quartic": 1.0,
    "mixed_r2_trace_xdaggerx": -2.0 / 3.0,
    "trace_xdaggerx_squared": 1.0 / 9.0,
    "locked_pairing_radius_squared": 1.0,
    "locked_pairing_radial_hessian": 8.0,
}

result = {
    "gate": "version4_family_defect_gauge_family_locking_gate",
    "locking_block": {
        "field": "X in Mat_3(R), X -> g_gauge X f_global^{-1}",
        "potential": (
            "V_lock=1/4||X^T X-I||_F^2+1/4(det X-1)^2"
        ),
        "vacuum": "X in SO(3), gauge-fixed representative X=I",
        "unbroken_group": "diagonal global SO(3)_{gauge+family}",
        "tetrahedral_reduction": (
            "a spin-three family tensor reduces the diagonal group to A4; "
            "the projector then leaves Z3"
        ),
    },
    "checks": {
        "maximum_locking_invariance_residual": max(invariance_residuals),
        "locking_hessian_eigenvalues": hessian_eigenvalues.tolist(),
        "locking_hessian_positive_count": int(
            np.sum(hessian_eigenvalues > 1.0e-6)
        ),
        "locking_hessian_zero_count": int(
            np.sum(np.abs(hessian_eigenvalues) <= 1.0e-6)
        ),
        "locking_hessian_negative_count": int(
            np.sum(hessian_eigenvalues < -1.0e-6)
        ),
        "gauge_mass_eigenvalues": gauge_mass_eigenvalues.tolist(),
        "all_gauge_modes_massive": bool(
            np.min(gauge_mass_eigenvalues) > TOLERANCE
        ),
        "same_symmetry_allows_both_pairing_phases": (
            pairing_examples[0]["pairing_radius_squared"] == 0.0
            and pairing_examples[1]["pairing_radius_squared"] > 0.0
        ),
        "real_so3_center_order": 1,
        "su3_center_order": 3,
        "determinant_connector_scalar_dimension": 3,
        "determinant_majorana_operator_dimension_4d": 6,
    },
    "pairing_examples": pairing_examples,
    "special_norm_locking_square": {
        "formula": "V_mu=(|Phi|^2-Tr(X^T X)/3)^2",
        "coefficients": special_square_coefficients,
        "interpretation": (
            "this square forces a nonzero pairing radius in the locked vacuum, "
            "but its three coefficient relations are not fixed by gauge-family "
            "symmetry alone and require a common supertrace or moment-map derivation"
        ),
    },
    "candidate_menu": {
        "real_SO3_bifundamental": {
            "pass": "resolves the gauge/global axis fork by diagonal locking",
            "fail": "does not fix the sign of the pairing effective mass",
        },
        "SU3_color_flavor_locking": {
            "pass": "has a central Z3 and standard one-third vortex architecture",
            "fail": "adds an SU3 family gauge algebra and extra gauge modes absent from the project",
        },
        "determinant_connector": {
            "pass": "det X can carry the composite charge-two pairing phase",
            "fail": "det(X) N^c N^c is a dimension-six four-dimensional operator",
        },
    },
    "status": {
        "gauge_global_fork": "pass_by_real_bifundamental_diagonal_locking",
        "pairing_condensate": "not_selected_by_symmetry",
        "remaining_gate": (
            "derive the special norm-locking square, or an equivalent negative "
            "pairing Hessian, from one finite graded supertrace without a fitted portal"
        ),
    },
}

with open(
    "s2t_v4_family_defect_gauge_family_locking_gate_results.json",
    "w",
    encoding="utf-8",
) as output_file:
    json.dump(result, output_file, indent=2)

print(json.dumps(result["checks"], indent=2))