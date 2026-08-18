#!/usr/bin/env python3
"""Real-scalar flip representation, twisted order and support audit."""

import json
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_real_scalar_flip_twisted_ko6_gate_results.json"
TOL = 1.0e-9


def block_diag(blocks):
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), dtype=complex)
    offset = 0
    for block in blocks:
        width = block.shape[0]
        result[offset : offset + width, offset : offset + width] = block
        offset += width
    return result


I3 = np.eye(3)
Z3 = np.zeros((3, 3), dtype=complex)
I9 = np.eye(9)
Z9 = np.zeros((9, 9))
J_MATRIX = np.block([[Z9, I9], [I9, Z9]])


def representation(element):
    lambda_plus, lambda_minus, matrix_part, complex_part = element
    return block_diag(
        [
            lambda_plus * I3,
            matrix_part,
            matrix_part,
            lambda_minus * I3,
            lambda_plus * I3,
            np.conj(complex_part) * I3,
        ]
    )


def twist(element):
    lambda_plus, lambda_minus, matrix_part, complex_part = element
    return lambda_minus, lambda_plus, matrix_part, complex_part


def star(element):
    lambda_plus, lambda_minus, matrix_part, complex_part = element
    return (
        np.conj(lambda_plus),
        np.conj(lambda_minus),
        matrix_part.conj().T,
        np.conj(complex_part),
    )


def opposite(element):
    return J_MATRIX @ representation(star(element)).conj() @ J_MATRIX


def opposite_twist(element):
    return opposite(twist(element))


def algebra_basis():
    basis = [
        (1.0, 0.0, np.zeros((3, 3)), 0.0),
        (0.0, 1.0, np.zeros((3, 3)), 0.0),
    ]
    for row in range(3):
        for column in range(3):
            matrix = np.zeros((3, 3))
            matrix[row, column] = 1.0
            basis.append((0.0, 0.0, matrix, 0.0))
    basis.extend(
        [
            (0.0, 0.0, np.zeros((3, 3)), 1.0),
            (0.0, 0.0, np.zeros((3, 3)), 1.0j),
        ]
    )
    return basis


def particle_dirac(X, phi):
    return np.block(
        [
            [Z3, X.conj().T, Z3],
            [X, Z3, np.conj(phi) * I3],
            [Z3, phi * I3, Z3],
        ]
    )


rng = np.random.default_rng(20260816)
X = rng.normal(size=(3, 3))
phi = 0.43 + 0.17j
particle = particle_dirac(X, phi)
D = block_diag([particle, particle.conj()])
basis = algebra_basis()

representation_columns = np.stack(
    [representation(item).reshape(-1) for item in basis], axis=1
)
real_representation_matrix = np.vstack(
    [representation_columns.real, representation_columns.imag]
)
real_representation_rank = int(np.linalg.matrix_rank(real_representation_matrix, tol=TOL))
assert real_representation_rank == 13

zero_order_residuals = []
twisted_first_order_residuals = []
untwisted_first_order_residuals = []
twisted_forms = []

for a in basis:
    pi_a = representation(a)
    pi_rho_a = representation(twist(a))
    twisted_commutator = D @ pi_a - pi_rho_a @ D
    ordinary_commutator = D @ pi_a - pi_a @ D
    for left in basis:
        twisted_forms.append(representation(left) @ twisted_commutator)
    for b in basis:
        b_opposite = opposite(b)
        rho_b_opposite = opposite_twist(b)
        zero_order_residuals.append(
            np.linalg.norm(pi_a @ b_opposite - b_opposite @ pi_a)
        )
        twisted_first_order_residuals.append(
            np.linalg.norm(
                twisted_commutator @ b_opposite
                - rho_b_opposite @ twisted_commutator
            )
        )
        untwisted_first_order_residuals.append(
            np.linalg.norm(
                ordinary_commutator @ b_opposite
                - b_opposite @ ordinary_commutator
            )
        )

assert max(zero_order_residuals) < TOL
assert max(twisted_first_order_residuals) < TOL
assert max(untwisted_first_order_residuals) > 1.0e-3

form_columns = np.stack([form.reshape(-1) for form in twisted_forms], axis=1)
twisted_form_complex_rank = int(np.linalg.matrix_rank(form_columns, tol=TOL))

block_support = []
for row in range(6):
    for column in range(6):
        maximum = max(
            np.linalg.norm(
                form[3 * row : 3 * row + 3, 3 * column : 3 * column + 3]
            )
            for form in twisted_forms
        )
        if maximum > TOL:
            block_support.append([row, column])

expected_support = [[0, 1], [1, 0], [4, 5], [5, 4]]
assert block_support == expected_support

j_completed_support = sorted(
    {tuple(item) for item in block_support}
    | {((row + 3) % 6, (column + 3) % 6) for row, column in block_support}
)
expected_completed = sorted(
    [(0, 1), (1, 0), (1, 2), (2, 1), (3, 4), (4, 3), (4, 5), (5, 4)]
)
assert j_completed_support == expected_completed
assert all(row != column for row, column in j_completed_support)
assert all(abs(row - column) == 1 for row, column in j_completed_support)

rho_symbol, r_symbol = sp.symbols("rho r", real=True)
ordinary_radial = sp.expand(6 * (rho_symbol**2 + r_symbol**2) ** 2)
target_radial = sp.expand((rho_symbol**2 - r_symbol**2) ** 2)
ordinary_mixed_coefficient = ordinary_radial.coeff(rho_symbol, 2).coeff(r_symbol, 2)
target_mixed_coefficient = target_radial.coeff(rho_symbol, 2).coeff(r_symbol, 2)
assert ordinary_mixed_coefficient == 12
assert target_mixed_coefficient == -2

X_test = sp.Matrix([[1, 2], [0, 1]])
Y_test = sp.Matrix([[2, 0], [1, 1]])
A_test = X_test * X_test.T
B_test = Y_test.T * Y_test
positive_cross = 2 * sp.trace((A_test + B_test) ** 2)
directed_target = sp.trace((A_test - B_test) ** 2)
assert positive_cross != directed_target

result = {
    "date": "2026-08-16",
    "gate": "version5_real_scalar_flip_twisted_ko6_gate",
    "algebra": "R0_plus direct_sum R0_minus direct_sum M3(R)_G direct_sum C_2",
    "twist": "swap R0_plus and R0_minus",
    "representation": {
        "complex_Hilbert_dimension": 18,
        "real_algebra_dimension": 13,
        "real_representation_rank": real_representation_rank,
        "faithful": True,
        "new_fermion_dimensions": 0,
    },
    "order_conditions": {
        "maximum_zero_order_residual": max(zero_order_residuals),
        "maximum_twisted_first_order_residual": max(twisted_first_order_residuals),
        "maximum_untwisted_first_order_residual": max(untwisted_first_order_residuals),
        "twisted_first_order_pass": True,
        "ordinary_first_order_on_duplicated_algebra": False,
    },
    "twisted_one_forms": {
        "complex_span_rank": twisted_form_complex_rank,
        "raw_block_support": block_support,
        "J_completed_block_support": [list(item) for item in j_completed_support],
        "diagonal_blocks": False,
        "endpoint_length_two_blocks": False,
        "graph_type_after_self_adjoint_fluctuation": "same nearest-neighbour odd chain",
    },
    "quartic_sign": {
        "ordinary_radial": str(ordinary_radial),
        "target_radial": str(target_radial),
        "ordinary_mixed_coefficient": int(ordinary_mixed_coefficient),
        "target_mixed_coefficient": int(target_mixed_coefficient),
        "matrix_positive_cross_witness": str(positive_cross),
        "matrix_directed_target_witness": str(directed_target),
        "sign_repaired": False,
    },
    "verdict": {
        "faithful_twisted_KO6_representation": "pass",
        "twisted_first_order": "pass",
        "new_curvature_support": "absent",
        "ordinary_spectral_moment_map_sign": "fail",
        "real_scalar_flip_with_ordinary_trace": "closed_dynamically",
        "physical_closure": False,
    },
    "next_gate": "version5_flip_twisted_trace_positivity_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))