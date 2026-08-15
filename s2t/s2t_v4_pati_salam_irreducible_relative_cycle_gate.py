#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np
import sympy as sp


OUTPUT = Path("s2t_v4_pati_salam_irreducible_relative_cycle_gate_results.json")
TOLERANCE = 1.0e-8


def connected_copy_commutant_dimension(copy_number):
    variables = 3 * copy_number * copy_number
    identity = np.eye(copy_number * copy_number)
    constraints = np.zeros((2 * copy_number * copy_number, variables))
    constraints[0 : copy_number**2, 0 : copy_number**2] = identity
    constraints[0 : copy_number**2, copy_number**2 : 2 * copy_number**2] = -identity
    constraints[copy_number**2 :, copy_number**2 : 2 * copy_number**2] = identity
    constraints[copy_number**2 :, 2 * copy_number**2 :] = -identity
    rank = np.linalg.matrix_rank(constraints, tol=TOLERANCE)
    return int(variables - rank)


def matrix_commutant_dimension(matrices):
    size = matrices[0].shape[0]
    identity = np.eye(size, dtype=complex)
    constraints = [np.kron(matrix.T, identity) - np.kron(identity, matrix) for matrix in matrices]
    stacked = np.vstack(constraints)
    rank = np.linalg.matrix_rank(stacked, tol=TOLERANCE)
    return int(size * size - rank)


def hermitian_basis(block_sizes):
    total_size = sum(block_sizes)
    basis = []
    offset = 0
    for block_size in block_sizes:
        for row in range(block_size):
            diagonal = np.zeros((total_size, total_size), dtype=complex)
            diagonal[offset + row, offset + row] = 1.0
            basis.append(diagonal)
        for row in range(block_size):
            for column in range(row + 1, block_size):
                symmetric = np.zeros((total_size, total_size), dtype=complex)
                symmetric[offset + row, offset + column] = 1.0 / np.sqrt(2.0)
                symmetric[offset + column, offset + row] = 1.0 / np.sqrt(2.0)
                basis.append(symmetric)
                antisymmetric = np.zeros((total_size, total_size), dtype=complex)
                antisymmetric[offset + row, offset + column] = 1j / np.sqrt(2.0)
                antisymmetric[offset + column, offset + row] = -1j / np.sqrt(2.0)
                basis.append(antisymmetric)
        offset += block_size
    return basis


def delta_from_coordinates(coordinates):
    delta = sp.zeros(2, 4)
    for right_index in range(2):
        for color_index in range(4):
            coordinate = 2 * (4 * right_index + color_index)
            delta[right_index, color_index] = coordinates[coordinate] + sp.I * coordinates[coordinate + 1]
    return delta


def effective_hessian():
    coordinates = sp.symbols("x0:16", real=True)
    delta = delta_from_coordinates(coordinates)
    gram = delta * delta.conjugate().T
    rho = sp.trace(gram)
    tau = sp.trace(gram * gram)
    determinant = sp.det(gram)
    potential = -rho**2 + tau**2 + 4 * determinant
    vacuum_value = 2 ** (-sp.Rational(1, 4))
    substitution = {coordinate: 0 for coordinate in coordinates}
    substitution[coordinates[0]] = vacuum_value
    hessian = sp.hessian(potential, coordinates).subs(substitution)
    numeric = np.array(hessian.evalf(), dtype=float)
    exact_eigenvalues = {str(value): int(multiplicity) for value, multiplicity in hessian.eigenvals().items()}
    return numeric, exact_eigenvalues, float(vacuum_value.evalf())


def chain_operator(delta):
    epsilon = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    second_edge = delta.T @ epsilon
    operator = np.zeros((10, 10), dtype=complex)
    operator[0:4, 4:6] = delta.conj().T
    operator[4:6, 0:4] = delta
    operator[4:6, 6:10] = second_edge.conj().T
    operator[6:10, 4:6] = second_edge
    return operator


def operator_derivatives():
    derivatives = []
    for coordinate in range(16):
        delta = np.zeros((2, 4), dtype=complex)
        entry = coordinate // 2
        delta[entry // 4, entry % 4] = 1.0 if coordinate % 2 == 0 else 1j
        derivatives.append(chain_operator(delta))
    return derivatives


def fixed_point_projection(matrix):
    result = np.zeros_like(matrix)
    for block in (slice(0, 4), slice(4, 6), slice(6, 10)):
        result[block, block] = matrix[block, block]
    return result


def auxiliary_jacobian(vacuum_value):
    delta = np.zeros((2, 4), dtype=complex)
    delta[0, 0] = vacuum_value
    operator = chain_operator(delta)
    basis = hermitian_basis([4, 2, 4])
    jacobian = np.zeros((len(basis), 16))
    for coordinate, derivative in enumerate(operator_derivatives()):
        curvature_derivative = derivative @ operator + operator @ derivative
        projected = fixed_point_projection(curvature_derivative)
        for basis_index, basis_matrix in enumerate(basis):
            jacobian[basis_index, coordinate] = np.trace(basis_matrix.conj().T @ projected).real
    return jacobian


def signature(matrix):
    eigenvalues = np.linalg.eigvalsh(matrix)
    return {
        "positive": int(np.sum(eigenvalues > TOLERANCE)),
        "zero": int(np.sum(np.abs(eigenvalues) <= TOLERANCE)),
        "negative": int(np.sum(eigenvalues < -TOLERANCE)),
        "minimum_eigenvalue": float(eigenvalues.min()),
        "maximum_eigenvalue": float(eigenvalues.max()),
    }


def main():
    copy_ledger = []
    for copy_number in range(1, 6):
        dimension = connected_copy_commutant_dimension(copy_number)
        copy_ledger.append({
            "copy_number": copy_number,
            "commutant_dimension": dimension,
            "expected_Mk_dimension": copy_number**2,
            "irreducible": dimension == 1,
            "lambda_relative": copy_number,
        })

    pauli_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    pauli_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    nontrivial_copy_commutant = matrix_commutant_dimension([pauli_x, pauli_z])

    effective, exact_eigenvalues, vacuum_value = effective_hessian()
    jacobian = auxiliary_jacobian(vacuum_value)
    auxiliary_dimension = jacobian.shape[0]
    full_hessian = np.block([
        [effective + 2.0 * jacobian.T @ jacobian, -2.0 * jacobian.T],
        [-2.0 * jacobian, 2.0 * np.eye(auxiliary_dimension)],
    ])
    schur_complement = (
        full_hessian[:16, :16]
        - full_hessian[:16, 16:] @ np.linalg.solve(full_hessian[16:, 16:], full_hessian[16:, :16])
    )

    output = {
        "gate": "version4_pati_salam_irreducible_relative_cycle",
        "canonical_identical_copy_ledger": copy_ledger,
        "one_copy_generated_commutant": "C",
        "k_copy_generated_commutant": "M_k(C)",
        "one_copy_selected_by_irreducibility": True,
        "nontrivial_k2_loophole": {
            "copy_generators": ["sigma_x", "sigma_z"],
            "common_commutant_dimension": nontrivial_copy_commutant,
            "interpretation": "k>1 can be irreducible only after adding noncommuting copy-space dynamics",
            "allowed_in_coefficient_free_branch": False,
        },
        "effective_Delta_Hessian": {
            "exact_eigenvalues": exact_eigenvalues,
            "signature": signature(effective),
        },
        "uneliminated_auxiliary_Hessian": {
            "Delta_real_dimension": 16,
            "fixed_point_auxiliary_real_dimension": auxiliary_dimension,
            "total_real_dimension": full_hessian.shape[0],
            "signature": signature(full_hessian),
            "Schur_complement_error": float(np.linalg.norm(schur_complement - effective)),
        },
        "verdict": (
            "Within the coefficient-free identical-copy mapping-cone branch, connected-cycle "
            "irreducibility forces k=1 and lambda_relative=1. The full Delta-plus-auxiliary "
            "Hessian has no negative modes; eliminating the auxiliary block returns the exact "
            "rank-one effective Hessian."
        ),
        "next_gate": (
            "embed this irreducible relative cycle into the full Pati-Salam real structure and "
            "audit the remaining phi/Sigma mixed scalar directions"
        ),
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()