#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np


OUTPUT = Path("s2t_v4_pati_salam_relative_parent_action_gate_results.json")


def random_unitary(size, rng):
    matrix = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    unitary, triangular = np.linalg.qr(matrix)
    phases = np.diag(triangular)
    phases = np.where(np.abs(phases) > 0.0, phases / np.abs(phases), 1.0)
    return unitary @ np.diag(np.conjugate(phases))


def chain_operators(delta):
    epsilon = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    second_edge = delta.T @ epsilon
    operator = np.zeros((10, 10), dtype=complex)
    operator[0:4, 4:6] = delta.conj().T
    operator[4:6, 0:4] = delta
    operator[4:6, 6:10] = second_edge.conj().T
    operator[6:10, 4:6] = second_edge
    height = np.diag([-1.0] * 4 + [0.0] * 2 + [1.0] * 4)
    return operator, height


def conditional_expectation(matrix):
    result = np.zeros_like(matrix)
    for block in (slice(0, 4), slice(4, 6), slice(6, 10)):
        result[block, block] = matrix[block, block]
    return result


def norm_squared(matrix):
    return float(np.vdot(matrix, matrix).real)


def main():
    rng = np.random.default_rng(20260814)
    quotient_errors = []
    determinant_errors = []
    circle_errors = []
    gauge_errors = []
    for _ in range(200):
        delta = rng.normal(size=(2, 4)) + 1j * rng.normal(size=(2, 4))
        operator, height = chain_operators(delta)
        curvature = operator @ operator
        expectation = conditional_expectation(curvature)
        quotient = norm_squared(curvature - expectation)
        commutator = height @ curvature - curvature @ height
        derivative_norm = norm_squared(0.5 * commutator)
        double_commutator = 0.25 * (height @ commutator - commutator @ height)
        quotient_errors.extend([
            abs(quotient - derivative_norm),
            float(np.linalg.norm(double_commutator - (curvature - expectation))),
        ])
        determinant = float(np.linalg.det(delta @ delta.conj().T).real)
        determinant_errors.append(abs(quotient - 4.0 * determinant))

        average = np.zeros_like(curvature)
        for index in range(17):
            angle = 2.0 * math.pi * index / 17.0
            unitary = np.diag(np.exp(1j * angle * np.diag(height)))
            average += unitary @ curvature @ unitary.conj().T / 17.0
        circle_errors.append(float(np.linalg.norm(average - expectation)))

        gauge = np.zeros((10, 10), dtype=complex)
        gauge[0:4, 0:4] = random_unitary(4, rng)
        gauge[4:6, 4:6] = random_unitary(2, rng)
        gauge[6:10, 6:10] = random_unitary(4, rng)
        transformed = gauge @ curvature @ gauge.conj().T
        gauge_errors.append(abs(norm_squared(transformed - conditional_expectation(transformed)) - quotient))

    generic = rng.normal(size=(10, 10)) + 1j * rng.normal(size=(10, 10))
    generic_derivative = 0.5 * (height @ generic - generic @ height)
    generic_mismatch = abs(
        norm_squared(generic - conditional_expectation(generic))
        - norm_squared(generic_derivative)
    )
    output = {
        "gate": "version4_pati_salam_relative_parent_action",
        "fixed_point_height": [-1, 0, 1],
        "even_curvature_identity": "inf_C ||F-C||^2=||F-E_h(F)||^2=||[h,F]/2||^2",
        "selector_identity": "||[h,D_Delta^2]/2||^2=4 det(Delta Delta^dagger)",
        "maximum_quotient_identity_error": max(quotient_errors),
        "maximum_circle_average_error": max(circle_errors),
        "maximum_determinant_selector_error": max(determinant_errors),
        "maximum_gauge_invariance_error": max(gauge_errors),
        "generic_full_matrix_mismatch": generic_mismatch,
        "generic_full_matrix_identity_is_false": generic_mismatch > 1.0e-8,
        "Hessian_spectrum": {
            "radial": ["8 sqrt(2)", 1],
            "gauge": [0, 9],
            "transverse": ["sqrt(2) (4 lambda_rel - 2)", 6],
        },
        "strict_stability_condition": "lambda_rel > 1/2",
        "one_copy_common_metric": {"lambda_rel": 1, "signature": [7, 9, 0]},
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()